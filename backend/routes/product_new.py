from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List, Dict
from models.schemas import ProductResponse, IngredientItem
import re
from db.supabase_client import supabase
from grading import calculate_grade, grade_to_legacy_score

router = APIRouter()

# ── Ingredient classification ─────────────────────────────────────────────────
# Single source of truth — used for every grade computation across browse,
# search/detail, and suggestions. ingredient_database.classify_ingredient()
# is intentionally NOT used here (it diverges on salt, sodium bicarbonate, etc.)

_BANNED = [
    'triclosan','formaldehyde','hydroquinone','mercury','lead',
    'e128','e216','e217','e240','sudan red','para red',
    'methylparaben','propylparaben','butylparaben','ethylparaben',
    'sodium nitrite','sodium nitrate','potassium bromate',
    'azodicarbonamide','brominated vegetable oil','olestra',
    'asbestos','benzene','vinyl chloride','aflatoxin',
]
_QUESTIONED = [
    'sodium lauryl sulfate','sls','sodium laureth sulfate','sles',
    'ammonium laureth sulfate','cocamidopropyl betaine',
    'tartrazine','sunset yellow','carmoisine','allura red','brilliant blue',
    'ponceau','erythrosine','quinoline yellow','brown ht','patent blue','azorubine',
    'e102','e110','e122','e124','e129','e131','e132','e133','e104','e127','e155',
    'monosodium glutamate','msg','disodium guanylate','disodium inosinate',
    'e621','e627','e631',
    'sodium benzoate','sodium metabisulphite','sulfur dioxide','sodium nitrite','sodium nitrate',
    'e211','e220','e223','e250','e251',
    'bha','bht','tbhq','butylated hydroxyanisole','butylated hydroxytoluene','tert-butylhydroquinone',
    'methylchloroisothiazolinone','methylisothiazolinone','dmdm hydantoin',
    'imidazolidinyl urea','diazolidinyl urea','quaternium-15',
    'aspartame','acesulfame','sucralose','saccharin','e951','e950','e955','e954',
    'tetrasodium edta','disodium edta','tetrasodium etidronate',
    'propylene glycol','polyethylene glycol','peg-',
    'titanium dioxide','e171',
    'carrageenan','e407',
    'phthalate','diethyl phthalate','dibutyl phthalate',
    'caramel colour','caramel color','e150',
    'phosphoric acid','e338',
    'partially hydrogenated','trans fat',
    'mono and diglycerides',
    'benzyl alcohol',
    'cyclomethicone','cyclopentasiloxane','cyclohexasiloxane',
    'mineral oil','petrolatum','paraffinum liquidum','paraffin wax',
    'retinol','retinyl palmitate','tretinoin','retinal','hydroxypinacolone retinoate',
    'beta carotene',
    'fragrance','parfum','perfume',
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
        if 'stabilizer' in n or 'stabiliser' in n or 'e466' in n or 'e412' in n or 'e410' in n:
            return 'Texture stabilizer; generally recognised as safe'
        if 'e322' in n: return 'Lecithin emulsifier; generally safe'
        if 'vegetable' in n: return 'Processed vegetable fat; quality varies by source'
        if 'palm oil' in n: return 'Common edible oil; environmental concerns'
        if 'nature identical' in n or 'natural flavour' in n or 'artificial flavour' in n:
            return 'Synthetic flavour compound'
        return 'Permitted additive; safe in regulated amounts'
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
    cleaned = []
    for item in items:
        item = re.sub(r'^[A-Za-z\s]+:\s*', '', item).strip()
        if len(item) > 1:
            cleaned.append(item)
    return cleaned

def _build_ingredient_item(ing) -> IngredientItem:
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

def _grade_from_raw(raw: str, ingredients: list) -> str:
    """Compute grade from ingredients_raw text (preferred) or dict list (fallback)."""
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

def _score_to_grade(score: int) -> str:
    if score >= 85: return 'A'
    if score >= 70: return 'B'
    if score >= 50: return 'C'
    return 'D'

def normalize_name(name: str) -> str:
    return re.sub(r'[^a-z0-9]', '', name.lower())

def _word_pattern(term: str) -> str:
    """'dove soap' → '%dove%soap%'  |  'parle g' → '%parle%g%'"""
    words = [w for w in term.strip().split() if w]
    return "%" + "%".join(words) + "%"

def _search_query(term: str):
    """Multi-strategy search — most specific first, broadest last."""
    normalized = normalize_name(term)

    def _run(col, op, val, prefer_static=True):
        try:
            q = supabase.from_("ai_extracted_products").select("*")
            if op == "eq":
                q = q.eq(col, val)
            else:
                q = q.ilike(col, val)
            if prefer_static:
                q = q.order("static_key", nullsfirst=False)
            return (q.limit(1).execute().data or [None])[0]
        except Exception:
            return None

    # 1a. Exact static_key — normalized (spaces stripped)
    r = _run("static_key", "eq", normalized, prefer_static=False)
    if r: return r

    # 1b. static_key with spaces replaced by hyphens: "dove soap" → "dove-soap"
    hyphenated = re.sub(r'\s+', '-', term.lower().strip())
    hyphenated = re.sub(r'[^a-z0-9-]', '', hyphenated)
    if hyphenated != normalized:
        r = _run("static_key", "eq", hyphenated, prefer_static=False)
        if r: return r

    # 2. Exact name (ilike for case-insensitivity)
    r = _run("name", "ilike", term)
    if r: return r

    # 3. Prefix: "Parle" → "Parle%"
    r = _run("name", "ilike", f"{term}%")
    if r: return r

    # 4. Word-by-word: "parle g" → "%parle%g%"
    #    Handles hyphens, spaces, punctuation differences between query and stored name
    word_pat = _word_pattern(term)
    r = _run("name", "ilike", word_pat)
    if r: return r

    # 5. Substring: "%term%"
    r = _run("name", "ilike", f"%{term}%")
    if r: return r

    # 6. Word-by-word on cleaned term (strip non-alphanum)
    clean_words = re.sub(r'[^a-z0-9 ]', ' ', term.lower()).split()
    clean_words = [w for w in clean_words if len(w) > 1]
    if clean_words:
        clean_pat = "%" + "%".join(clean_words) + "%"
        r = _run("name", "ilike", clean_pat)
        if r: return r

    return None


# ── Search / Detail ───────────────────────────────────────────────────────────

@router.get("/search")
async def search_product(name: str = Query(..., description="Product name to search", min_length=1, max_length=120)):
    print(f"[SEARCH] Querying: {name}")

    p = _search_query(name)
    if not p:
        raise HTTPException(status_code=404, detail=f"Product '{name}' not found.")

    print(f"[SEARCH] Found: {p['name']} (static_key={p.get('static_key')})")

    raw = p.get("ingredients_raw") or ""
    if raw:
        raw_names = _parse_raw(raw)
        ingredients = [_build_ingredient_item(n) for n in raw_names if n]
        # Compute grade live from actual ingredients
        grade = calculate_grade([i.dict() for i in ingredients])
        # Sync stored grade if it differs (keeps browse consistent with detail)
        if grade != p.get("grade"):
            try:
                supabase.from_("ai_extracted_products") \
                    .update({"grade": grade}).eq("id", p["id"]).execute()
            except Exception:
                pass
    else:
        ingredients = [IngredientItem(
            name="Standard Ingredients",
            aliases="",
            classification="generally_recognised",
            one_line_note="Full ingredient list not yet available",
            regulatory_note="FSSAI approved"
        )]
        # No ingredients to compute from — use whatever grade backfill stored.
        # Defaulting to "C" matches browse page so both pages agree.
        grade = p.get("grade") or "C"

    raw_images = p.get("images") or []
    if not raw_images and p.get("image_url"):
        raw_images = [p["image_url"]]

    return ProductResponse(
        id=str(p.get("id", "")),
        name=p["name"],
        brand=p.get("brand") or "Unknown",
        category=p.get("category") or "General",
        image_url=p.get("image_url"),
        images=raw_images if raw_images else None,
        grade=grade,
        awareness_score=grade_to_legacy_score(grade),
        summary=p.get("summary") or f"{p['name']} — product information.",
        fssai_note=p.get("fssai_note") or "FSSAI approved product.",
        verdict=p.get("verdict") or "",
        recommendation=p.get("recommendation") or "",
        ingredients=ingredients,
        ingredients_raw=raw or None,
        search_count=1,
        data_source="database_verified" if p.get("static_key") else "community_verified",
        confidence="high" if p.get("static_key") else "medium",
        is_complete=True,
    )


# ── Browse ────────────────────────────────────────────────────────────────────

@router.get("/browse")
async def browse_products(
    category: str = Query(None),
    brand: str = Query(None),
    q: str = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(24, ge=1, le=100),
    sort: str = Query("score"),
):
    # Use stored grade — no ingredients_raw fetch needed (fast)
    _grade_order = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

    try:
        def _base_query():
            q_ = supabase.from_("ai_extracted_products") \
                .select("id, name, brand, category, image_url, verdict, grade, static_key")
            if category and category != "All":
                q_ = q_.eq("category", category)
            if brand and brand != "All":
                q_ = q_.eq("brand", brand)
            if q:
                # Search across name, brand, and category so "soap" finds
                # products in the Soap category, "amul" finds all Amul products, etc.
                q_ = q_.or_(f"name.ilike.%{q}%,brand.ilike.%{q}%,category.ilike.%{q}%")
            return q_

        # Batch-fetch all matching rows (Supabase caps at 1000 per request)
        all_rows = []
        offset = 0
        while True:
            batch = _base_query().range(offset, offset + 999).execute()
            rows = batch.data or []
            all_rows.extend(rows)
            if len(rows) < 1000:
                break
            offset += 1000
    except Exception as e:
        print(f"[BROWSE ERROR] {e}")
        return {"products": [], "total": 0, "page": 1, "pages": 1, "categories": [], "brands": []}

    # Deduplicate by normalised name — static (has static_key) beats community
    _norm = lambda s: re.sub(r'[^a-z0-9]', '', (s or "").lower())
    seen: dict = {}
    for p in all_rows:
        nn = _norm(p.get("name") or "")
        if not nn:
            continue
        existing = seen.get(nn)
        if existing is None or (p.get("static_key") and not existing.get("static_key")):
            seen[nn] = p

    items = []
    for p in seen.values():
        items.append({
            "id":        str(p.get("id", "")),
            "name":      p.get("name", ""),
            "brand":     p.get("brand") or "Unknown",
            "category":  p.get("category") or "General",
            "image_url": p.get("image_url"),
            "grade":     p.get("grade") or "C",
            "verdict":   p.get("verdict") or "",
        })

    if sort == "name":
        items.sort(key=lambda p: p["name"].lower())
    elif sort == "brand":
        items.sort(key=lambda p: (p["brand"].lower(), p["name"].lower()))
    else:
        items.sort(key=lambda p: _grade_order.get(p.get("grade", "C"), 2))

    total = len(items)
    start = (page - 1) * limit
    page_items = items[start: start + limit]

    all_cats = sorted({p["category"] for p in all_rows if p.get("category")})
    all_brands = sorted({p["brand"] for p in all_rows if p.get("brand")})
    if category and category != "All":
        all_brands = sorted({p["brand"] for p in all_rows if p.get("brand") and p.get("category") == category})

    return {
        "products": page_items,
        "total": total,
        "page": page,
        "pages": max(1, -(-total // limit)),
        "categories": all_cats,
        "brands": all_brands,
    }


# ── Suggestions ───────────────────────────────────────────────────────────────

@router.get("/suggestions")
async def get_search_suggestions(q: str = Query(..., min_length=1, max_length=80)):
    try:
        result = supabase.from_("ai_extracted_products") \
            .select("name, brand, category, static_key") \
            .ilike("name", f"%{q}%") \
            .order("static_key", nullsfirst=False) \
            .limit(12) \
            .execute()

        seen_names = set()
        suggestions = []
        for p in (result.data or []):
            if not p.get("name"):
                continue
            nn = normalize_name(p["name"])
            if nn in seen_names:
                continue
            seen_names.add(nn)
            suggestions.append({
                "name":     p["name"],
                "brand":    p.get("brand") or "",
                "category": p.get("category") or "General",
            })
            if len(suggestions) >= 8:
                break
    except Exception as e:
        print(f"[SUGGESTIONS ERROR] {e}")
        suggestions = []

    return {"suggestions": suggestions}
