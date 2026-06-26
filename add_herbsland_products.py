"""
Add 12 HerbsLand herbal powder products to ai_extracted_products.
"""
import sys, os, re
sys.path.insert(0, 'backend')
from dotenv import load_dotenv
load_dotenv('backend/.env')
from supabase import create_client
from routes.ingredient_database import classify_ingredient, INGREDIENT_DESCRIPTIONS

SUPABASE_URL = os.environ['SUPABASE_URL']
SERVICE_KEY  = os.environ['SUPABASE_SERVICE_ROLE_KEY']
sb = create_client(SUPABASE_URL, SERVICE_KEY)

FK = "https://rukminim2.flixcart.com/image/612/612/xif0q"

# ── helpers ───────────────────────────────────────────────────────────────────

def parse_ingredients(raw: str):
    parts, depth, cur = [], 0, ""
    for ch in raw:
        if ch == '(': depth += 1; cur += ch
        elif ch == ')': depth -= 1; cur += ch
        elif ch == ',' and depth == 0:
            p = cur.strip().rstrip('.')
            if p: parts.append(p)
            cur = ""
        else: cur += ch
    if cur.strip(): parts.append(cur.strip().rstrip('.'))
    return parts

def classify_one(name: str) -> dict:
    try:
        cls = classify_ingredient(name)
        if not isinstance(cls, str):
            cls = cls.get('classification', 'generally_recognised')
    except Exception:
        cls = 'generally_recognised'
    key = name.lower().strip()
    raw_desc = (INGREDIENT_DESCRIPTIONS.get(key) or
                INGREDIENT_DESCRIPTIONS.get(re.sub(r'\s*\(.*?\)', '', key).strip()))
    desc = raw_desc if isinstance(raw_desc, dict) else {}
    return {
        "name": name, "aliases": desc.get('aliases', ''), "classification": cls,
        "one_line_note": desc.get('one_line_note', ''), "regulatory_note": desc.get('regulatory_note', ''),
        "commonly_found_in": desc.get('commonly_found_in'), "health_effects": desc.get('health_effects'),
        "countries_restricted": desc.get('countries_restricted', []),
        "fssai_position": desc.get('fssai_position'), "recommendation": desc.get('recommendation'),
    }

def compute_grade(classified):
    if not classified: return "B"
    total = len(classified)
    q = sum(1 for i in classified if i['classification'] == 'commonly_questioned')
    w = sum(1 for i in classified if i['classification'] == 'worth_knowing')
    if q > 0: return "D"
    if w == 0: return "A"
    return "B" if w / total <= 0.30 else "C"

def make_static_key(name: str) -> str:
    return re.sub(r'[^a-z0-9]', '', name.lower())

def make_summary(name, brand, grade, q, w, total):
    if grade == "A":
        return f"{name} by {brand} scores Grade A. All {total} ingredients are 100% pure herbal powders — natural, chemical-free, and generally recognised as safe."
    elif grade == "B":
        return f"{name} by {brand} scores Grade B. {total} ingredients analysed; {w} worth knowing about, no restricted additives."
    elif grade == "C":
        return f"{name} by {brand} scores Grade C. Contains {w} worth-knowing ingredients (>30% of total). Use with awareness."
    else:
        return f"{name} by {brand} scores Grade D. Contains {q} commonly questioned ingredient(s) flagged in some countries."

FSSAI_MAP = {
    "Haircare": "Hair care products regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
    "Skincare": "Cosmetics regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
}

# ── catalogue ─────────────────────────────────────────────────────────────────

PRODUCTS = [
    # ── HAIR CARE ──
    (
        "HerbsLand Organic Amla Powder (Indian Gooseberry)",
        "HerbsLand", "Haircare",
        "Phyllanthus Emblica Fruit Powder",
        FK + "/hair-treatment/f/b/9/300-organic-amla-powder-indian-gooseberry-powder-for-hair-and-original-imahghgynckvyzyr.jpeg",
    ),
    (
        "HerbsLand Organic Bhringraj Leaf Powder",
        "HerbsLand", "Haircare",
        "Eclipta Alba Leaf Powder",
        FK + "/hair-treatment/f/l/q/300-organic-100-natural-bhringraj-leaf-powder-for-hair-herbsland-original-imahghgyygxqkyk7.jpeg",
    ),
    (
        "HerbsLand Amla Reetha Shikakai Powder 3-in-1",
        "HerbsLand", "Haircare",
        "Phyllanthus Emblica Fruit Powder, Sapindus Mukorossi Fruit Powder, Acacia Concinna Pod Powder",
        FK + "/shopsy-hair-treatment/r/x/6/210-organic-amla-reetha-shikakai-powder-for-hair-natural-hair-original-imahhc9ynyamne8z.jpeg",
    ),
    (
        "HerbsLand Amla Reetha Shikakai Hibiscus Bhringraj Powder 5-in-1",
        "HerbsLand", "Haircare",
        "Phyllanthus Emblica Fruit Powder, Sapindus Mukorossi Fruit Powder, Acacia Concinna Pod Powder, "
        "Hibiscus Rosa-Sinensis Flower Powder, Eclipta Alba Leaf Powder",
        FK + "/hair-treatment/5/u/h/250-combo-of-amla-reetha-shikakai-hibiscus-bhringraj-powder-for-original-imahhcbdtbth9qhf.jpeg",
    ),
    (
        "HerbsLand Amla Reetha Shikakai Hibiscus Bhringraj Henna Neem Powder 7-in-1",
        "HerbsLand", "Haircare",
        "Phyllanthus Emblica Fruit Powder, Sapindus Mukorossi Fruit Powder, Acacia Concinna Pod Powder, "
        "Hibiscus Rosa-Sinensis Flower Powder, Eclipta Alba Leaf Powder, "
        "Lawsonia Inermis Leaf Powder, Azadirachta Indica Leaf Powder",
        FK + "/hair-treatment/u/d/m/450-amla-ritha-shikakai-bhringraj-hibiscus-powder-for-natural-original-imahhcb9eddjppav.jpeg",
    ),
    # ── SKIN / FACE CARE ──
    (
        "HerbsLand Multani Mitti & Sandalwood Powder",
        "HerbsLand", "Skincare",
        "Calcium Bentonite, Santalum Album Wood Powder",
        FK + "/face-pack/c/b/4/200-multani-mitti-fuller-s-earth-sandalwood-powder-chandan-for-original-imahgkh7zqwprrx3.jpeg",
    ),
    (
        "HerbsLand Orange Peel & Mulethi Powder",
        "HerbsLand", "Skincare",
        "Citrus Sinensis Peel Powder, Glycyrrhiza Glabra Root Powder",
        FK + "/face-pack/q/i/v/200-100-organic-natural-orange-peel-powder-and-mulethi-powder-original-imahgkh76gssjbnj.jpeg",
    ),
    (
        "HerbsLand Rose Petal Sandalwood Neem Leaf Multani Mitti Face Pack 4-in-1",
        "HerbsLand", "Skincare",
        "Rosa Centifolia Flower Powder, Santalum Album Wood Powder, "
        "Azadirachta Indica Leaf Powder, Calcium Bentonite",
        FK + "/face-pack/x/u/t/400-combo-of-rose-petal-sandalwood-chandan-neem-leaf-multani-original-imahgkh7j47revw9.jpeg",
    ),
    (
        "HerbsLand Multani Mitti Orange Peel Sandalwood Powder 3-in-1",
        "HerbsLand", "Skincare",
        "Calcium Bentonite, Citrus Sinensis Peel Powder, Santalum Album Wood Powder",
        FK + "/face-pack/1/d/y/300-100-bio-organic-multani-mitti-fuller-s-earth-orange-peel-original-imahgkh7szhgt3tp.jpeg",
    ),
    (
        "HerbsLand Multani Mitti Sandalwood Orange Peel Neem Rose Petals 5-in-1",
        "HerbsLand", "Skincare",
        "Calcium Bentonite, Santalum Album Wood Powder, Citrus Sinensis Peel Powder, "
        "Azadirachta Indica Leaf Powder, Rosa Centifolia Flower Powder",
        FK + "/face-pack/q/y/z/250-100-bio-multani-mitti-sandalwood-chandan-orange-peel-neem-original-imahgkh78h3n4xbx.jpeg",
    ),
    (
        "HerbsLand Wild Kasturi Turmeric Orange Peel Rose Petal Lemon Peel 4-in-1",
        "HerbsLand", "Skincare",
        "Curcuma Aromatica Rhizome Powder, Citrus Sinensis Peel Powder, "
        "Rosa Centifolia Flower Powder, Citrus Limon Peel Powder",
        FK + "/face-pack/4/u/o/400-100-pure-organic-wild-kasturi-turmeric-orange-peel-rose-original-imahgkh77hhdpg7a.jpeg",
    ),
    (
        "HerbsLand Organic Mulethi (Licorice Root) Powder",
        "HerbsLand", "Skincare",
        "Glycyrrhiza Glabra Root Powder",
        FK + "/face-pack/p/r/h/300-organic-mulethi-powder-for-skin-and-face-100-g-powder-original-imahgkh7uf3sf8uz.jpeg",
    ),
]

# ── insertion ─────────────────────────────────────────────────────────────────

def already_exists(name: str) -> bool:
    res = sb.table('ai_extracted_products').select('id').ilike('name', name).limit(1).execute()
    return bool(res.data)

def insert_product(name, brand, category, ingredients_raw, image_url):
    print(f"\n[{name}]")
    if already_exists(name):
        print("  SKIP — already in database")
        return False

    ing_names  = parse_ingredients(ingredients_raw)
    classified = [classify_one(n) for n in ing_names]
    grade      = compute_grade(classified)
    q = sum(1 for i in classified if i['classification'] == 'commonly_questioned')
    w = sum(1 for i in classified if i['classification'] == 'worth_knowing')
    total = len(classified)
    print(f"  Grade={grade}  questioned={q}  worth={w}  total={total}")

    fssai_note = FSSAI_MAP.get(category, "Regulated under Cosmetics Rules 2020.")
    verdict = (f"Contains {q} restricted/flagged ingredient(s)." if q else
               f"Contains {w} ingredient(s) worth monitoring." if w else
               "All ingredients are 100% pure herbal powders — no chemicals, no additives.")
    recommendation = ("Avoid or use sparingly — contains commonly questioned ingredients." if q else
                      "Use with awareness — some additives worth monitoring." if w else
                      "Safe to use — 100% natural herbal powder with no concerning additives.")
    awareness_score = max(0, 100 - (q * 25) - (w * 8))

    record = {
        "name":            name,
        "brand":           brand,
        "category":        category,
        "grade":           grade,
        "ingredients_raw": ingredients_raw,
        "ingredients":     classified,
        "image_url":       image_url,
        "static_key":      make_static_key(name),
        "summary":         make_summary(name, brand, grade, q, w, total),
        "fssai_note":      fssai_note,
        "verdict":         verdict,
        "recommendation":  recommendation,
        "awareness_score": awareness_score,
        "status":          "approved",
    }
    try:
        res = sb.table('ai_extracted_products').insert(record).execute()
        print(f"  INSERTED (id: {res.data[0]['id'][:8]}...)")
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return None

def main():
    print(f"Inserting {len(PRODUCTS)} HerbsLand products...\n")
    added = skipped = failed = 0
    for p in PRODUCTS:
        r = insert_product(*p)
        if r is True:    added += 1
        elif r is False: skipped += 1
        else:            failed += 1
    print(f"\n{'='*60}")
    print(f"Done.  Added: {added}  |  Skipped: {skipped}  |  Failed: {failed}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
