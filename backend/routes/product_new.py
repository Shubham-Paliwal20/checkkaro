from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List, Dict
from models.schemas import ProductResponse, IngredientItem
import re
import time
from db.supabase_client import supabase, supabase_admin
from grading import calculate_grade, grade_to_legacy_score

router = APIRouter()

# ── Browse cache ──────────────────────────────────────────────────────────────
# Caches the full sorted+deduped product list per filter combo for 2 minutes.
# Pagination is served from cache — zero DB calls on subsequent pages.
_browse_cache: dict = {}
_BROWSE_TTL = 120   # seconds
_BROWSE_MAX = 80    # max distinct filter combos in memory

def _browse_cache_key(category, brand, q, sort):
    return f"{category or ''}|{brand or ''}|{q or ''}|{sort}"

def _prune_browse():
    if len(_browse_cache) <= _BROWSE_MAX:
        return
    now = time.monotonic()
    dead = [k for k, (ts, _) in _browse_cache.items() if now - ts > _BROWSE_TTL]
    for k in dead:
        del _browse_cache[k]
    if len(_browse_cache) > _BROWSE_MAX:
        for k, _ in sorted(_browse_cache.items(), key=lambda x: x[1][0])[:_BROWSE_MAX // 2]:
            del _browse_cache[k]

def invalidate_browse_cache():
    """Call after any product insert/delete so stale data isn't served."""
    _browse_cache.clear()

# ── Suggestions cache ─────────────────────────────────────────────────────────
_suggest_cache: dict = {}
_SUGGEST_TTL = 300  # 5 minutes
_SUGGEST_MAX = 200

def _prune_suggest():
    if len(_suggest_cache) <= _SUGGEST_MAX:
        return
    for k, _ in sorted(_suggest_cache.items(), key=lambda x: x[1][0])[:_SUGGEST_MAX // 2]:
        del _suggest_cache[k]

# ── Ingredient classification ─────────────────────────────────────────────────
# Single source of truth — used for every grade computation across browse,
# search/detail, and suggestions. ingredient_database.classify_ingredient()
# is intentionally NOT used here (it diverges on salt, sodium bicarbonate, etc.)

_BANNED = [
    'triclosan','formaldehyde','hydroquinone','mercury','lead',
    'e128','e240','sudan red','para red',
    'sodium nitrite','sodium nitrate','potassium bromate',
    'azodicarbonamide','brominated vegetable oil','olestra',
    'asbestos','benzene','vinyl chloride','aflatoxin',
]

# ── Commonly Questioned ───────────────────────────────────────────────────────
# Ingredients with regulatory bans, carcinogen links, or serious health concerns.
# RULE: full names only — short codes ('bha','bht','sls') cause false positives
# e.g. 'bha' matches 'bhasma', 'sls' could match 'soluble' — use full INCI names.
_QUESTIONED = [
    # Surfactants — irritants / 1,4-dioxane carcinogen contamination risk
    'sodium lauryl sulfate','sodium lauryl sulphate',
    'sodium laureth sulfate','sodium laureth sulphate','ammonium laureth sulfate',
    'cocamidopropyl betaine',
    # Synthetic dyes — EU/FDA bans, hyperactivity, cancer links
    'tartrazine','sunset yellow','carmoisine','allura red','brilliant blue',
    'ponceau','erythrosine','quinoline yellow','brown ht','patent blue','azorubine','red 40',
    'e102','e110','e122','e124','e129','e131','e132','e133','e104','e127','e155',
    'ci 47000','ci 19140','ci 15985','ci 16035','ci 42090',
    # Flavour enhancers — neurotoxicity, MSG-like side effects (not MSG itself — see _WORTH)
    'disodium guanylate','disodium inosinate','e627','e631',
    # Parabens — endocrine disruption at high doses; EU restricted concentrations
    'methylparaben','ethylparaben','propylparaben','butylparaben','isobutylparaben',
    'e214','e215','e216','e217','e218','e219',
    # Preservatives — benzene formation, sulfite allergies, nitrosamine risk
    'sodium benzoate','sodium metabisulphite','sulfur dioxide',
    'e211','e220','e223','e250','e251',
    # Antioxidant preservatives — IARC possible carcinogens, banned in Japan
    'butylated hydroxyanisole','butylated hydroxytoluene','tbhq','tert-butylhydroquinone',
    # Formaldehyde releasers / strong skin sensitisers
    'methylchloroisothiazolinone','methylisothiazolinone','dmdm hydantoin',
    'imidazolidinyl urea','diazolidinyl urea','quaternium-15',
    # Sweeteners — IARC 2B carcinogen (aspartame), bladder cancer risk (saccharin)
    'aspartame','acesulfame','saccharin','e951','e950','e954',
    # Chelating agents — strip minerals, penetration enhancers
    'tetrasodium edta','disodium edta','tetrasodium etidronate',
    # Humectant/solvent — neurotoxic at high systemic exposure
    'propylene glycol',
    # PEG compounds — 1,4-dioxane carcinogen contamination
    'polyethylene glycol','peg-',
    # EU-banned food additive (genotoxicity confirmed by EFSA 2021)
    'titanium dioxide','e171',
    # Banned in EU infant formula; gut inflammation in studies
    'carrageenan','e407',
    # Endocrine-disrupting phthalates
    'phthalate','diethyl phthalate','dibutyl phthalate',
    # Caramel Class III/IV — 4-MEI probable carcinogen (California Prop 65)
    'caramel colour','caramel color','e150',
    # Erodes tooth enamel, calcium depletion
    'phosphoric acid','e338',
    # Trans fats — banned USA/EU; cardiovascular risk
    'partially hydrogenated','trans fat','mono and diglycerides',
    # Toxic to neonates; fatal gasping syndrome
    'benzyl alcohol',
    # Cyclic silicones — EU banned in rinse-off; endocrine disruption; environmental persistence
    'cyclomethicone','cyclopentasiloxane','cyclohexasiloxane',
    # Petroleum-derived — PAH/MOAH carcinogens from refining contamination
    'mineral oil','petrolatum','paraffinum liquidum','paraffin wax',
    # Undisclosed colorants behind Q.S — exact dye identity hidden by brand
    'colour q.s','color q.s','colour q.s.','color q.s.',
    # Undisclosed chemical mixtures — may hide allergens, phthalates, synthetic musks
    'fragrance','parfum','perfume','artificial flavor','artificial flavour',
    # Retinoids — teratogenic (cause birth defects); photocarcinogenic in sunlight
    'retinol','retinyl palmitate','tretinoin','retinal','hydroxypinacolone retinoate',
    # Talc — asbestos contamination risk; IARC carcinogen (asbestos-contaminated form)
    'talc','talcum',
]

# ── Worth Knowing ─────────────────────────────────────────────────────────────
# Permitted ingredients with mild concerns or worth being aware of.
_WORTH = [
    # Vague / undisclosed ingredient descriptors — brand not fully disclosing composition
    'q.s','q.s.','quantum sufficit',
    # Vegetable oils — high saturated fat, palm = environmental concern
    'palm oil','palmolein','vegetable oil','edible vegetable fat',
    # Sugars and high-GI carbs
    'sugar','glucose syrup','high fructose corn syrup','invert sugar','maltodextrin',
    # Natural flavors (from natural sources) — generally safe; check for hidden allergens
    'natural flavor','natural flavour','nature identical',
    # Permitted food additives
    'citric acid','emulsifier','stabilizer','stabiliser','thickener',
    'lecithin','soy lecithin','potassium sorbate','e202',
    'polyglycerol','ammonium phosphatides',
    'e322','e471','e466','e412','e410','e476',
    # Cosmetic preservative — safe at EU-permitted levels (<1%)
    'phenoxyethanol',
    # Sweetener — alters gut microbiome; FDA GRAS; concern less severe than aspartame
    'sucralose','e955',
    # MSG — FDA GRAS; some individuals report sensitivity at high doses
    'monosodium glutamate','msg','e621',
    # Salt — excess linked to hypertension and cardiovascular disease
    'salt','sodium chloride',
    # Beta-carotene — natural pigment; safe at food levels; concern only at very high supplement doses in smokers
    'beta carotene',
    # Non-cyclic silicones — buildup on hair/skin; not banned; no endocrine disruption
    'dimethicone','dimethiconol','amodimethicone',
    # Denatured alcohols — drying; disrupts skin barrier with repeated use
    'alcohol denat','denatured alcohol','sd alcohol',
    # Natural allergens
    'lanolin','wool wax',
]

# Pre-compute compact (no-space, no-hyphen) forms of every keyword so
# "Methyl Paraben" → "methylparaben" matches correctly at classify-time.
_BANNED_C     = [re.sub(r'[\s\-/]', '', k) for k in _BANNED]
_QUESTIONED_C = [re.sub(r'[\s\-/]', '', k) for k in _QUESTIONED]
_WORTH_C      = [re.sub(r'[\s\-/]', '', k) for k in _WORTH]

# In cosmetic / topical products, salt and citric acid are safe pH/texture
# agents with zero health concern — their food-context warnings don't apply.
_COSMETIC_CATS = {'skincare', 'skin care', 'hair care', 'haircare',
                  'personal care', 'cosmetics', 'baby care', 'oral care', 'household'}
_COSMETIC_GR   = {'salt', 'sodium chloride', 'citric acid'}


# Known-safe ingredients that remain generally_recognised even when Q.S is appended.
# Checked before colour/perfume Q.S patterns so "Purified Water Q.S" isn't flagged.
_QS_SAFE = [
    'multani mitti', "fuller's earth", 'fullers earth',
]


def _classify(name: str, category: str = '') -> str:
    n   = name.lower()
    n_c = re.sub(r'[\s\-/]', '', n)   # compact: "Methyl Paraben" → "methylparaben"

    # Certified organic fragrance override — must run before 'fragrance' → commonly_questioned
    # e.g. "Fragrance *CO Certified Organic" is disclosed and certified; no undisclosed-mix concern
    if any(w in n for w in ('fragrance', 'parfum', 'perfume')) and 'certified organic' in n:
        return 'generally_recognised'

    # Safe Q.S override: "Purified Water Q.S" → generally_recognised despite 'q.s' in _WORTH
    if 'q.s' in n:
        for safe in _QS_SAFE:
            if safe in n:
                return 'generally_recognised'

    # Category-aware override: salt / citric acid are generally recognised
    # in topical products (no dietary hypertension / enamel-erosion risk)
    if category:
        cat = category.lower()
        if any(c in cat for c in _COSMETIC_CATS):
            for safe in _COSMETIC_GR:
                if safe in n or safe in n_c:
                    return 'generally_recognised'

    for kw, kw_c in zip(_BANNED, _BANNED_C):
        if kw in n or kw_c in n_c: return 'banned'
    for kw, kw_c in zip(_QUESTIONED, _QUESTIONED_C):
        if kw in n or kw_c in n_c: return 'commonly_questioned'
    for kw, kw_c in zip(_WORTH, _WORTH_C):
        if kw in n or kw_c in n_c: return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'banned': return 'Banned or restricted ingredient'
    if cls == 'commonly_questioned':
        if 'colour q.s' in n or 'color q.s' in n: return 'Brand is hiding the exact colorant — undisclosed dye or pigment; may include restricted synthetic azo dyes or heavy-metal-based pigments'
        if 'q.s' in n: return 'Brand has not disclosed the full ingredient — "quantum sufficit" means added in unspecified quantity; exact composition unknown'
        if 'sucralose' in n: return 'Artificial sweetener; long-term effects debated'
        if 'e110' in n: return 'Sunset Yellow – artificial colour, restricted in EU'
        if 'e122' in n: return 'Carmoisine – artificial colour, restricted in EU'
        if 'msg' in n or 'monosodium' in n: return 'Flavour enhancer; generally safe in normal amounts'
        if 'sodium benzoate' in n: return 'Preservative; may form benzene with ascorbic acid'
        return 'Commonly questioned ingredient'
    if cls == 'worth_knowing':
        if 'q.s' in n: return 'Brand has not disclosed the full ingredient — "quantum sufficit" means added in unspecified quantity; exact composition unknown'
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
    if 'gold bhasma' in n or 'swarna bhasma' in n or 'gold leaf' in n or 'pure gold' in n or '24 karat gold' in n or '24k gold' in n:
        return 'Traditional Ayurvedic Swarna Bhasma; used in premium skincare for centuries; generally recognised as safe'
    if 'bhasma' in n: return 'Traditional Ayurvedic calcined mineral preparation; generally recognised as safe'
    if 'neem' in n: return 'Natural Ayurvedic herb with antibacterial properties'
    if 'amla' in n or 'amalaki' in n: return 'Natural Indian gooseberry; rich in Vitamin C'
    if 'brahmi' in n: return 'Adaptogenic Ayurvedic herb'
    if 'rose water' in n or 'rose extract' in n: return 'Natural floral extract; soothing properties'
    if 'aloe vera' in n or 'aloe barbadensis' in n: return 'Natural plant extract; soothing and moisturising'
    if 'shea butter' in n: return 'Natural plant butter; moisturising'
    if 'jojoba' in n: return 'Natural plant wax; skin-conditioning'
    if 'argan oil' in n: return 'Natural plant oil; rich in fatty acids'
    if 'rosehip' in n: return 'Natural plant oil; rich in Vitamin C and antioxidants'
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

def _build_ingredient_item(ing, category: str = '') -> IngredientItem:
    name = ing if isinstance(ing, str) else ing.get('name', '')
    aliases = '' if isinstance(ing, str) else ing.get('aliases', '')
    cls = _classify(name, category)
    return IngredientItem(
        name=name,
        aliases=aliases,
        classification=cls,
        one_line_note=_note(name, cls),
        regulatory_note=_reg_note(cls),
    )

def _grade_from_raw(raw: str, ingredients: list, category: str = '') -> str:
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
    classified = [{'name': n, 'classification': _classify(n, category)} for n in names]
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
    cat = p.get("category") or ""
    if raw:
        raw_names = _parse_raw(raw)
        ingredients = [_build_ingredient_item(n, cat) for n in raw_names if n]
        # Compute grade live from actual ingredients
        grade = calculate_grade([i.dict() for i in ingredients])

        # Persist classified ingredients + grade so the Supabase fallback path
        # (used when this server is cold/slow) always shows correct classifications
        # instead of mapping everything to 'generally_recognised'.
        stored_ings = p.get("ingredients") or []
        grade_changed = grade != p.get("grade")
        ings_missing  = not stored_ings or len(stored_ings) == 0

        if grade_changed or ings_missing:
            try:
                update_payload: dict = {}
                if grade_changed:
                    update_payload["grade"] = grade
                if ings_missing:
                    update_payload["ingredients"] = [i.dict() for i in ingredients]
                supabase_admin.from_("ai_extracted_products") \
                    .update(update_payload).eq("id", p["id"]).execute()
                if grade_changed:
                    invalidate_browse_cache()
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
    _grade_order = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

    # ── Cache check ───────────────────────────────────────────────────────────
    cache_key = _browse_cache_key(category, brand, q, sort)
    now = time.monotonic()
    if cache_key in _browse_cache:
        ts, cached = _browse_cache[cache_key]
        if now - ts < _BROWSE_TTL:
            items = cached["items"]
            total = len(items)
            start = (page - 1) * limit
            return {
                "products": items[start: start + limit],
                "total":    total,
                "page":     page,
                "pages":    max(1, -(-total // limit)),
                "categories": cached["categories"],
                "brands":     cached["brands"],
            }

    # ── Fetch from Supabase ───────────────────────────────────────────────────
    try:
        def _base_query():
            q_ = supabase.from_("ai_extracted_products") \
                .select("id, name, brand, category, image_url, verdict, grade, static_key")
            if category and category != "All":
                q_ = q_.eq("category", category)
            if brand and brand != "All":
                q_ = q_.eq("brand", brand)
            if q:
                q_ = q_.or_(f"name.ilike.%{q}%,brand.ilike.%{q}%,category.ilike.%{q}%")
            return q_

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

    # ── Deduplicate by normalised name ────────────────────────────────────────
    _norm = lambda s: re.sub(r'[^a-z0-9]', '', (s or "").lower())
    seen: dict = {}
    for p in all_rows:
        nn = _norm(p.get("name") or "")
        if not nn:
            continue
        existing = seen.get(nn)
        if existing is None or (p.get("static_key") and not existing.get("static_key")):
            seen[nn] = p

    items = [
        {
            "id":        str(p.get("id", "")),
            "name":      p.get("name", ""),
            "brand":     p.get("brand") or "Unknown",
            "category":  p.get("category") or "General",
            "image_url": p.get("image_url"),
            "grade":     p.get("grade") or "C",
            "verdict":   p.get("verdict") or "",
        }
        for p in seen.values()
    ]

    if sort == "name":
        items.sort(key=lambda p: p["name"].lower())
    elif sort == "brand":
        items.sort(key=lambda p: (p["brand"].lower(), p["name"].lower()))
    else:
        items.sort(key=lambda p: _grade_order.get(p.get("grade", "C"), 2))

    all_cats   = sorted({p["category"] for p in all_rows if p.get("category")})
    all_brands = sorted({p["brand"]    for p in all_rows if p.get("brand")})

    # ── Store in cache ────────────────────────────────────────────────────────
    _browse_cache[cache_key] = (now, {"items": items, "categories": all_cats, "brands": all_brands})
    _prune_browse()

    total = len(items)
    start = (page - 1) * limit
    return {
        "products": items[start: start + limit],
        "total":    total,
        "page":     page,
        "pages":    max(1, -(-total // limit)),
        "categories": all_cats,
        "brands":     all_brands,
    }


# ── Suggestions ───────────────────────────────────────────────────────────────

@router.get("/suggestions")
async def get_search_suggestions(q: str = Query(..., min_length=1, max_length=80)):
    # ── Cache check ───────────────────────────────────────────────────────────
    ck = q.lower().strip()
    now = time.monotonic()
    if ck in _suggest_cache:
        ts, cached = _suggest_cache[ck]
        if now - ts < _SUGGEST_TTL:
            return {"suggestions": cached}

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

    _suggest_cache[ck] = (now, suggestions)
    _prune_suggest()
    return {"suggestions": suggestions}
