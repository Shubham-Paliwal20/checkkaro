from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List, Dict
from models.schemas import ProductResponse, IngredientItem
import re
from routes.product_all_data import ALL_PRODUCTS
from routes.product_ingredients_full import get_ingredients
from routes.product_images import PRODUCT_IMAGES
from db.supabase_client import supabase
from grading import calculate_grade, grade_to_legacy_score

router = APIRouter()

# ── Ingredient classification (for DB products stored as plain strings) ───────

_BANNED = [
    'triclosan','formaldehyde','hydroquinone','mercury','lead',
    'e128','e216','e217','e240','sudan red','para red',
    'methylparaben','propylparaben','butylparaben','ethylparaben',
    'sodium nitrite','sodium nitrate','potassium bromate',
    'azodicarbonamide','brominated vegetable oil','olestra',
    'asbestos','benzene','vinyl chloride','aflatoxin',
]
_QUESTIONED = [
    # Harsh surfactants
    'sodium lauryl sulfate','sls','sodium laureth sulfate','sles',
    'ammonium laureth sulfate','cocamidopropyl betaine',
    # Synthetic dyes (EU banned/restricted)
    'tartrazine','sunset yellow','carmoisine','allura red','brilliant blue',
    'ponceau','erythrosine','quinoline yellow','brown ht','patent blue','azorubine',
    'e102','e110','e122','e124','e129','e131','e132','e133','e104','e127','e155',
    # Flavor enhancers
    'monosodium glutamate','msg','disodium guanylate','disodium inosinate',
    'e621','e627','e631',
    # Preservatives with serious concerns
    'sodium benzoate','sodium metabisulphite','sulfur dioxide','sodium nitrite','sodium nitrate',
    'e211','e220','e223','e250','e251',
    'bha','bht','tbhq','butylated hydroxyanisole','butylated hydroxytoluene','tert-butylhydroquinone',
    'methylchloroisothiazolinone','methylisothiazolinone','dmdm hydantoin',
    'imidazolidinyl urea','diazolidinyl urea','quaternium-15',
    # Sweeteners
    'aspartame','acesulfame','sucralose','saccharin','e951','e950','e955','e954',
    # Penetration enhancers / chelating agents
    'tetrasodium edta','disodium edta','tetrasodium etidronate',
    'propylene glycol','polyethylene glycol','peg-',
    # EU-banned white pigment
    'titanium dioxide','e171',
    # Gut-inflammation thickener
    'carrageenan','e407',
    # Phthalates / hormone disruptors
    'phthalate','diethyl phthalate','dibutyl phthalate',
    # Caramel class III/IV (4-MEI)
    'caramel colour','caramel color','e150',
    # Phosphoric acid
    'phosphoric acid','e338',
    # Trans fats (banned USA/EU/Canada)
    'partially hydrogenated','trans fat',
    # Emulsifiers with trans fat/glycidol risk
    'mono and diglycerides',
    # Preservatives with severe toxicity concerns
    'benzyl alcohol',
    # Cyclic silicones (EU banned wash-off, endocrine disruption)
    'cyclomethicone','cyclopentasiloxane','cyclohexasiloxane',
    # Petroleum-derived (PAH/MOAH contamination risk)
    'mineral oil','petrolatum','paraffinum liquidum','paraffin wax',
    # Retinoids (teratogenic, sunlight tumour risk)
    'retinol','retinyl palmitate','tretinoin','retinal','hydroxypinacolone retinoate',
    # Beta carotene (lung cancer in smokers at high doses)
    'beta carotene',
    # Fragrance — hidden allergens, phthalates, endocrine disruptors
    'fragrance','parfum','perfume',
    # Artificial flavors — undisclosed synthetic chemicals
    'artificial flavor','artificial flavour',
]
_WORTH = [
    'palm oil','palmolein','vegetable oil','edible vegetable fat',
    'sugar','glucose syrup','high fructose corn syrup','invert sugar','maltodextrin',
    'natural flavor','nature identical',
    'citric acid','emulsifier','stabilizer','stabiliser','thickener',
    'lecithin','soy lecithin','potassium sorbate','e202',
    'polyglycerol','ammonium phosphatides',
    'e322','e471','e466','e412','e410','e476','e162','e160',
    # Phenoxyethanol — mostly safe cosmetic preservative at permitted levels (EU max 1%)
    'phenoxyethanol',
]

def _classify(name: str) -> str:
    n = name.lower()
    for b in _BANNED:
        if b in n: return 'banned'
    for q in _QUESTIONED:
        if q in n: return 'commonly_questioned'
    for w in _WORTH:
        if w in n: return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'banned': return 'Banned or restricted ingredient'
    if cls == 'commonly_questioned':
        if 'sucralose' in n: return 'Artificial sweetener; long-term effects debated'
        if 'e110' in n: return 'Sunset Yellow – artificial colour, restricted in EU'
        if 'e122' in n: return 'Carmoisine – artificial colour, restricted in EU'
        if 'msg' in n or 'monosodium' in n: return 'Flavour enhancer; generally safe in normal amounts'
        if 'sodium benzoate' in n: return 'Preservative; may form benzene with ascorbic acid'
        return 'Commonly questioned ingredient'
    if cls == 'worth_knowing':
        if 'sugar' in n: return 'Sweetener; excess consumption linked to health concerns'
        if 'emulsifier' in n or 'e471' in n: return 'Emulsifier; generally recognised as safe'
        if 'stabilizer' in n or 'stabiliser' in n or 'e407' in n or 'e466' in n or 'e412' in n or 'e410' in n:
            return 'Texture stabilizer; generally recognised as safe'
        if 'e322' in n: return 'Lecithin emulsifier; generally safe'
        if 'vegetable' in n: return 'Processed vegetable fat; quality varies by source'
        if 'palm oil' in n: return 'Common edible oil; environmental concerns'
        if 'nature identical' in n or 'natural flavour' in n or 'artificial flavour' in n:
            return 'Synthetic flavour compound'
        return 'Permitted additive; safe in regulated amounts'
    # generally_recognised
    if 'milk solid' in n: return 'Dairy base; source of protein and calcium'
    if 'cocoa' in n: return 'Natural cocoa; source of antioxidants'
    if 'saffron' in n: return 'Natural spice with antioxidant properties'
    if 'honey' in n: return 'Natural sweetener'
    if 'almond' in n or 'cashew' in n or 'pista' in n or 'pistachio' in n: return 'Natural nut; healthy fats and protein'
    if 'mango' in n or 'strawberry' in n or 'litchi' in n or 'fruit' in n: return 'Natural fruit preparation'
    if 'whey protein' in n: return 'Dairy protein concentrate'
    if 'turmeric' in n: return 'Natural spice with anti-inflammatory properties'
    if 'ashwagandha' in n: return 'Adaptogenic herb used in Ayurveda'
    if 'isabgol' in n or 'psyllium' in n: return 'Natural dietary fibre'
    if 'wheat flour' in n: return 'Contains gluten; avoid if gluten-intolerant'
    if 'cardamom' in n or 'pepper' in n or 'fennel' in n: return 'Natural spice'
    return 'Generally recognised as safe'

def _reg_note(cls: str) -> str:
    if cls == 'banned': return 'Banned or restricted in EU and multiple countries'
    if cls == 'commonly_questioned': return 'Subject to regulatory scrutiny; permitted by FSSAI'
    if cls == 'worth_knowing': return 'Permitted additive under FSSAI regulations'
    return 'Approved under FSSAI/CODEX standards'

def _grade_from_raw(raw: str, ingredients: list) -> str:
    """Calculate grade live — always preferred over any stored DB value."""
    if raw:
        names = _parse_raw(raw)
    else:
        names = []
        for ing in ingredients:
            if isinstance(ing, dict):
                names.append(ing.get('name', ''))
            else:
                names.append(str(ing))
        names = [n for n in names if n]
    classified = [{'name': n, 'classification': _classify(n)} for n in names]
    return calculate_grade(classified)

def _parse_raw(raw: str) -> list:
    """Split ingredients_raw text into individual ingredient strings."""
    raw = raw.strip().rstrip('.')
    depth, current, items = 0, [], []
    for ch in raw:
        if ch in '([': depth += 1
        elif ch in ')]': depth -= 1
        if ch == ',' and depth == 0:
            items.append(''.join(current).strip())
            current = []
        else:
            current.append(ch)
    if current:
        items.append(''.join(current).strip())
    # Strip section prefixes like "Ice Cream:", "Cone:", "Coating:"
    cleaned = []
    for item in items:
        item = re.sub(r'^[A-Za-z\s]+:\s*', '', item).strip()
        if len(item) > 1:
            cleaned.append(item)
    return cleaned

def _build_ingredient_item(ing) -> IngredientItem:
    """Accept either a plain string or a dict (legacy or new format).
    Always re-classifies using _classify() — never trusts stored DB values,
    which may have been set by AI extraction with different rules.
    """
    name = ing if isinstance(ing, str) else ing.get('name', '')
    aliases = '' if isinstance(ing, str) else ing.get('aliases', '')
    cls = _classify(name)
    return IngredientItem(
        name=name,
        aliases=aliases,
        classification=cls,
        one_line_note=_note(name, cls),
        regulatory_note=_reg_note(cls),
    )

def _score_to_grade(score: int) -> str:
    if score >= 85: return 'A'
    if score >= 70: return 'B'
    if score >= 50: return 'C'
    return 'D'

# Convert ALL_PRODUCTS to the format we need
# Calculate real grade from actual ingredients — not from legacy awareness score
SAMPLE_PRODUCTS = {}
for key, (name, brand, category, score, verdict, recommendation) in ALL_PRODUCTS.items():
    _ings = get_ingredients(key, category=category)
    _classified = [
        {'name': i['name'], 'classification': _classify(i['name'])}
        for i in _ings
        if i.get('name') and i['name'].lower() != 'standard ingredients'
    ]
    _grade = calculate_grade(_classified) if _classified else _score_to_grade(score)
    SAMPLE_PRODUCTS[key] = {
        "id": key,
        "name": name,
        "brand": brand,
        "category": category,
        "image_url": PRODUCT_IMAGES.get(key),
        "awareness_score": score,
        "grade": _grade,
        "summary": f"{name} - {verdict}. This information is for general awareness based on publicly available regulatory data. It is not a health assessment or medical advice.",
        "fssai_note": "FSSAI approved product with standard ingredients.",
        "verdict": verdict,
        "recommendation": recommendation,
        "ingredients": [
            {"name": "Standard Ingredients", "classification": "generally_recognised", "one_line_note": "Full ingredient list available in database", "regulatory_note": "Load database for complete details"}
        ]
    }

# Pre-built search index — computed once at startup, never rebuilt per-request
SEARCH_INDEX = [
    {
        "name": p["name"],
        "brand": p["brand"],
        "category": p["category"],
        "name_lower": p["name"].lower(),
        "brand_lower": p["brand"].lower(),
    }
    for p in SAMPLE_PRODUCTS.values()
]


def normalize_name(name: str) -> str:
    """Normalize product name for matching"""
    return re.sub(r'[^a-z0-9]', '', name.lower())


@router.get("/search")
async def search_product(name: str = Query(..., description="Product name to search", min_length=1, max_length=120)):
    """
    DATABASE-ONLY SEARCH - NO AI (with sample data until you load real database)
    """
    print(f"[DATABASE ONLY] Searching for: {name}")
    
    # Normalize search term
    normalized_search = normalize_name(name)
    
    # Search in sample products
    for key, product_data in SAMPLE_PRODUCTS.items():
        if (normalized_search in normalize_name(key) or
            normalized_search in normalize_name(product_data["name"]) or
            normalized_search in normalize_name(product_data["brand"])):

            print(f"[DATABASE ONLY] Found: {product_data['name']}")

            # Check Supabase for an admin-approved ingredient correction first
            approved_ingredients = None
            approved_raw = None
            try:
                override = supabase.from_("ai_extracted_products") \
                    .select("ingredients_raw") \
                    .ilike("name", product_data["name"]) \
                    .limit(1) \
                    .execute()
                if override.data and override.data[0].get("ingredients_raw"):
                    approved_raw = override.data[0]["ingredients_raw"]
                    raw_names = _parse_raw(approved_raw)
                    approved_ingredients = [_build_ingredient_item(n) for n in raw_names if n]
                    print(f"[SUPABASE OVERRIDE] Using approved ingredients for {product_data['name']}")
            except Exception as e:
                print(f"[SUPABASE OVERRIDE ERROR] {e}")

            # Always get static ingredients (skip placeholder "Standard Ingredients")
            full_ingredients = get_ingredients(key, category=product_data["category"])
            static_items = []
            for ing in full_ingredients:
                if ing["name"].lower() == "standard ingredients":
                    continue
                static_items.append(IngredientItem(
                    name=ing["name"],
                    aliases="",
                    classification=ing["classification"],
                    one_line_note=ing["one_line_note"],
                    regulatory_note=ing["regulatory_note"]
                ))

            if approved_ingredients is not None:
                # Merge: static first, then add approved ones not already present
                static_names_lower = {i.name.lower() for i in static_items}
                extra = [i for i in approved_ingredients if i.name.lower() not in static_names_lower]
                ingredients = static_items + extra
                if not ingredients:
                    ingredients = approved_ingredients
            else:
                ingredients = static_items if static_items else [IngredientItem(
                    name="Standard Ingredients",
                    aliases="",
                    classification="generally_recognised",
                    one_line_note="Full ingredient list available in database",
                    regulatory_note=""
                )]

            grade = calculate_grade([i.dict() for i in ingredients])
            return ProductResponse(
                id=product_data["id"],
                name=product_data["name"],
                brand=product_data["brand"],
                category=product_data["category"],
                image_url=product_data["image_url"],
                grade=grade,
                awareness_score=grade_to_legacy_score(grade),
                summary=product_data["summary"],
                fssai_note=product_data["fssai_note"],
                verdict=product_data["verdict"],
                recommendation=product_data["recommendation"],
                ingredients=ingredients,
                ingredients_raw=approved_raw,
                search_count=1,
                data_source="database_verified",
                confidence="high",
                is_complete=True
            )
    
    # Check Supabase ai_extracted_products for community-submitted products
    try:
        db_result = supabase.from_("ai_extracted_products") \
            .select("*") \
            .ilike("name", f"%{name}%") \
            .order("created_at", desc=True) \
            .limit(1) \
            .execute()

        if db_result.data:
            p = db_result.data[0]
            # Always prefer ingredients_raw — identical logic to _grade_from_raw and browse
            # Dict ingredients may be stale AI-extracted data; raw text is the authoritative source
            if p.get("ingredients_raw"):
                raw_ingredients = _parse_raw(p["ingredients_raw"])
            else:
                raw_ingredients = p.get("ingredients") or []

            ingredients = [_build_ingredient_item(ing) for ing in raw_ingredients if ing]
            print(f"[SUPABASE] Found AI-extracted product: {p['name']} | {len(ingredients)} ingredients")
            raw_images = p.get("images") or []
            if not raw_images and p.get("image_url"):
                raw_images = [p["image_url"]]
            grade = calculate_grade([i.dict() for i in ingredients])
            return ProductResponse(
                id=str(p.get("id", "")),
                name=p["name"],
                brand=p.get("brand") or "Unknown",
                category=p.get("category") or "General",
                image_url=p.get("image_url"),
                images=raw_images if raw_images else None,
                grade=grade,
                awareness_score=grade_to_legacy_score(grade),
                summary=p.get("summary") or "",
                fssai_note=p.get("fssai_note") or "",
                verdict=p.get("verdict") or "",
                recommendation=p.get("recommendation") or "",
                ingredients=ingredients,
                ingredients_raw=p.get("ingredients_raw") or None,
                search_count=1,
                data_source="community_verified",
                confidence="medium",
                is_complete=True,
            )
    except Exception as e:
        print(f"[SUPABASE SEARCH ERROR] {e}")

    # Product not found anywhere
    available_products = list(SAMPLE_PRODUCTS.keys())
    raise HTTPException(
        status_code=404,
        detail=f"Product '{name}' not found in database. Available sample products: {', '.join(available_products[:20])}... ({len(available_products)} total products). Load full database with detailed ingredients using the SQL files."
    )


@router.get("/browse")
async def browse_products(
    category: str = Query(None, description="Filter by category"),
    brand: str = Query(None, description="Filter by brand"),
    q: str = Query(None, description="Search within results"),
    page: int = Query(1, ge=1),
    limit: int = Query(24, ge=1, le=100),
    sort: str = Query("score", description="sort: score | name | brand"),
):
    """Browse all products with category/brand filters and pagination."""
    # Build static items as a mutable dict keyed by normalised name so Supabase
    # corrections can update the grade in-place without creating duplicates.
    _norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
    items_by_name: dict = {}
    for p in SAMPLE_PRODUCTS.values():
        items_by_name[_norm(p["name"])] = dict(p)

    # Merge community products from Supabase
    try:
        community = supabase.from_("ai_extracted_products") \
            .select("id, name, brand, category, image_url, verdict, ingredients, ingredients_raw") \
            .order("created_at", desc=True) \
            .limit(500) \
            .execute()
        for p in (community.data or []):
            nn = _norm(p.get("name") or "")
            raw = p.get("ingredients_raw") or ""
            ings = p.get("ingredients") or []
            has_content = bool(raw) or bool(ings)

            if nn in items_by_name:
                if raw:
                    # Admin-approved correction exists — recompute grade with merged ingredients
                    # (matches what the detail page returns: static base + approved additions)
                    static_key = next(
                        (k for k, sp in SAMPLE_PRODUCTS.items()
                         if _norm(sp["name"]) == nn), None
                    )
                    if static_key:
                        approved_names = _parse_raw(raw)
                        full_ings = get_ingredients(static_key, category=items_by_name[nn].get("category", ""))
                        static_classified = [
                            {"name": i["name"], "classification": _classify(i["name"])}
                            for i in full_ings
                            if i.get("name") and i["name"].lower() != "standard ingredients"
                        ]
                        static_lower = {c["name"].lower() for c in static_classified}
                        extra = [
                            {"name": n, "classification": _classify(n)}
                            for n in approved_names if n.lower() not in static_lower
                        ]
                        merged = calculate_grade(static_classified + extra)
                        items_by_name[nn]["grade"] = merged
                # If no content (empty duplicate) — keep static entry unchanged, skip
            else:
                # Genuinely new product not in static data
                grade = _grade_from_raw(raw, ings)
                items_by_name[nn] = {
                    "id":        str(p.get("id", "")),
                    "name":      p.get("name", ""),
                    "brand":     p.get("brand") or "Unknown",
                    "category":  p.get("category") or "General",
                    "image_url": p.get("image_url"),
                    "grade":     grade,
                    "verdict":   p.get("verdict") or "",
                }
    except Exception as e:
        print(f"[BROWSE SUPABASE ERROR] {e}")

    items = list(items_by_name.values())

    # Filter
    if category and category != "All":
        items = [p for p in items if p["category"] == category]
    if brand and brand != "All":
        items = [p for p in items if p["brand"] == brand]
    if q:
        q_lower = q.lower()
        items = [
            p for p in items
            if q_lower in p["name"].lower() or q_lower in p["brand"].lower()
        ]

    # Sort
    _grade_order = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    if sort == "name":
        items.sort(key=lambda p: p["name"].lower())
    elif sort == "brand":
        items.sort(key=lambda p: (p["brand"].lower(), p["name"].lower()))
    else:
        items.sort(key=lambda p: _grade_order.get(p.get("grade", "C"), 2))

    total = len(items)

    # Paginate
    start = (page - 1) * limit
    page_items = items[start: start + limit]

    # Categories and brands from all items (static + community)
    all_items = list(SAMPLE_PRODUCTS.values())
    try:
        all_cats   = sorted({p["category"] for p in all_items} | {p["category"] for p in (community.data or []) if p.get("category")})
        base_brand = {p["brand"] for p in all_items}
        comm_brand = {p.get("brand") for p in (community.data or []) if p.get("brand")}
        if category and category != "All":
            avail_brands = sorted(
                {p["brand"] for p in all_items if p["category"] == category} |
                {p.get("brand") for p in (community.data or []) if p.get("category") == category and p.get("brand")}
            )
        else:
            avail_brands = sorted(base_brand | comm_brand)
    except Exception:
        all_cats     = sorted({p["category"] for p in all_items})
        avail_brands = sorted({p["brand"] for p in all_items})

    return {
        "products": [
            {
                "id":        p["id"],
                "name":      p["name"],
                "brand":     p["brand"],
                "category":  p["category"],
                "image_url": p["image_url"],
                "grade":     p.get("grade", "C"),
                "verdict":   p.get("verdict", ""),
            }
            for p in page_items
        ],
        "total": total,
        "page": page,
        "pages": max(1, -(-total // limit)),
        "categories": all_cats,
        "brands": avail_brands,
    }


@router.get("/suggestions")
async def get_search_suggestions(q: str = Query(..., description="Search query for suggestions", min_length=1, max_length=80)):
    if len(q) < 1:
        return {"suggestions": []}

    q_lower = q.lower()
    prefix = []
    substring = []

    # Static products
    for p in SEARCH_INDEX:
        name_match = q_lower in p["name_lower"]
        brand_match = q_lower in p["brand_lower"]
        if not name_match and not brand_match:
            continue
        entry = {"name": p["name"], "brand": p["brand"], "category": p["category"]}
        if p["name_lower"].startswith(q_lower):
            prefix.append(entry)
        else:
            substring.append(entry)

    # Community-submitted products from Supabase
    try:
        community = supabase.from_("ai_extracted_products") \
            .select("name, brand, category") \
            .ilike("name", f"%{q}%") \
            .limit(5) \
            .execute()
        for p in (community.data or []):
            if not p.get("name"):
                continue
            entry = {
                "name": p["name"],
                "brand": p.get("brand") or "",
                "category": p.get("category") or "General",
            }
            if p["name"].lower().startswith(q_lower):
                prefix.insert(0, entry)   # community prefix match gets top priority
            else:
                substring.insert(0, entry)
    except Exception as e:
        print(f"[SUGGESTIONS SUPABASE ERROR] {e}")

    suggestions = (prefix + substring)[:8]
    return {"suggestions": suggestions}
