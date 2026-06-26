"""
Add 6 Herbal Essences products to ai_extracted_products.
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

INCI = "https://incidecoder-content.storage.googleapis.com"

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
        return f"{name} by {brand} scores Grade A. All {total} ingredients are generally recognised as safe."
    elif grade == "B":
        return f"{name} by {brand} scores Grade B. {total} ingredients analysed; {w} worth knowing about, no restricted additives."
    elif grade == "C":
        return f"{name} by {brand} scores Grade C. Contains {w} worth-knowing ingredients (>30% of total). Use with awareness."
    else:
        return f"{name} by {brand} scores Grade D. Contains {q} commonly questioned ingredient(s) flagged in some countries."

FSSAI_NOTE = "Hair care products regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020."

# ── catalogue ─────────────────────────────────────────────────────────────────

PRODUCTS = [
    # ── ARGAN OIL CLASSIC LINE ──
    (
        "Herbal Essences Argan Oil of Morocco Shampoo",
        "Herbal Essences", "Haircare",
        "Water, Sodium Lauryl Sulfate, Sodium Laureth Sulfate, "
        "Cocamidopropyl Betaine, Glycol Distearate, Dimethicone, Parfum, "
        "Argania Spinosa Kernel Oil, Histidine, Aloe Barbadensis Leaf Juice, "
        "Ecklonia Radiata Extract, Sodium Citrate, Cocamide MEA, "
        "Sodium Xylenesulfonate, Citric Acid, Sodium Benzoate, Sodium Chloride, "
        "Guar Hydroxypropyltrimonium Chloride, Tetrasodium EDTA, Polyquaternium-6, "
        "Methylchloroisothiazolinone, Methylisothiazolinone",
        INCI + "/9df6ebd3-9086-4e12-a847-22c93382624f/products/"
               "herbal-essences-argan-oil-of-morocco-shampoo/"
               "herbal-essences-argan-oil-of-morocco-shampoo_front_photo_original.jpeg",
    ),
    (
        "Herbal Essences Argan Oil of Morocco Conditioner",
        "Herbal Essences", "Haircare",
        "Water, Stearyl Alcohol, Behentrimonium Methosulfate, "
        "Bis-Aminopropyl Dimethicone, Argania Spinosa Kernel Oil, Histidine, "
        "Aloe Barbadensis Leaf Juice, Ecklonia Radiata Extract, Parfum, "
        "Cetyl Alcohol, Benzyl Alcohol, Dicetyldimonium Chloride, "
        "Disodium EDTA, Citric Acid, "
        "Methylchloroisothiazolinone, Methylisothiazolinone",
        INCI + "/1baf58ff-7a72-4fd3-a497-5746f1bc663a/products/"
               "herbal-essences-argan-oil-of-morocco-conditioner/"
               "herbal-essences-argan-oil-of-morocco-conditioner_front_photo_original.jpeg",
    ),
    # ── BIO:RENEW LINE ──
    (
        "Herbal Essences Bio:Renew Coconut Milk Shampoo",
        "Herbal Essences", "Haircare",
        "Water, Sodium Laureth Sulfate, Cocamidopropyl Betaine, "
        "Sodium Lauryl Sulfate, Sodium Citrate, Sodium Xylenesulfonate, "
        "Sodium Chloride, Parfum, Cocos Nucifera Fruit Extract, Histidine, "
        "Aloe Barbadensis Leaf Juice, Ecklonia Radiata Extract, "
        "Zea Mays Silk Extract, Orchis Mascula Flower Extract, "
        "Stearyl Alcohol, Cetyl Alcohol, Glycol Distearate, Glycerin, "
        "Dimethiconol, Citric Acid, Sodium Benzoate, Dimethicone, "
        "Guar Hydroxypropyltrimonium Chloride, Tetrasodium EDTA, Polyquaternium-6, "
        "Trihydroxystearin, Trideceth-10, "
        "Methylchloroisothiazolinone, Methylisothiazolinone",
        INCI + "/69ab1631-3a3a-40f4-849e-2d1b077866da/ingredients/"
               "herbal-essences-coconut-milk-shampoo/"
               "herbal-essences-coconut-milk-shampoo_original.jpeg",
    ),
    (
        "Herbal Essences Bio:Renew Sulfate Free Shampoo Potent Aloe + Mango",
        "Herbal Essences", "Haircare",
        "Aqua, Lauramidopropyl Betaine, Sodium Cocoyl Isethionate, "
        "Sodium Lauroyl Sarcosinate, Sodium Citrate, Citric Acid, Parfum, "
        "Sodium Benzoate, Sodium Salicylate, Polyquaternium-10, Tetrasodium EDTA, "
        "Limonene, Propylene Glycol, Hexyl Cinnamal, Linalool, "
        "Aloe Barbadensis Leaf Juice, Butylene Glycol, Histidine, "
        "Rubus Fruticosus Fruit Extract, Persea Gratissima Fruit Extract, "
        "Mangifera Indica Fruit Extract, Alcohol Denatured, Ecklonia Radiata Extract",
        INCI + "/d02f8bba-629a-4ccc-bff4-b5d2444ceff7/products/"
               "herbal-essences-bio-renew-sulfate-free-shampoo-with-potent-aloe-mango/"
               "herbal-essences-bio-renew-sulfate-free-shampoo-with-potent-aloe-mango_front_photo_original.jpeg",
    ),
    (
        "Herbal Essences Bio:Renew Potent Aloe + Honey Shampoo",
        "Herbal Essences", "Haircare",
        "Water, Lauramidopropyl Betaine, Sodium Cocoyl Isethionate, "
        "Sodium Lauroyl Sarcosinate, Sodium Citrate, Citric Acid, Parfum, "
        "Sodium Benzoate, Sodium Salicylate, Polyquaternium-10, Tetrasodium EDTA, "
        "Aloe Barbadensis Leaf Juice, Butylene Glycol, Histidine, Honey Extract, "
        "Alcohol Denatured, Ecklonia Radiata Extract, T-Butyl Alcohol",
        INCI + "/6f810efe-dfae-4047-8ce9-ba3f85fc2e29/products/"
               "herbal-essences-bio-renew-potent-aloe-honey-shampoo/"
               "herbal-essences-bio-renew-potent-aloe-honey-shampoo_front_photo_original.jpeg",
    ),
    (
        "Herbal Essences Bio:Renew Avocado & Pequi Shampoo",
        "Herbal Essences", "Haircare",
        "Aqua, Lauramidopropyl Betaine, Sodium Cocoyl Isethionate, "
        "Sodium Lauroyl Sarcosinate, Sodium Citrate, Citric Acid, Parfum, "
        "Sodium Benzoate, Sodium Salicylate, Polyquaternium-10, Tetrasodium EDTA, "
        "Limonene, Aloe Barbadensis Leaf Juice, Butylene Glycol, Histidine, "
        "Persea Gratissima Oil, Alcohol Denatured, Ecklonia Radiata Extract",
        INCI + "/6eb33b55-14dc-47d2-84fc-35f430ba7a9b/products/"
               "herbal-essences-avocado-and-pequi-bio-renew-shampoo/"
               "herbal-essences-avocado-and-pequi-bio-renew-shampoo_front_photo_original.jpeg",
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

    verdict = (f"Contains {q} restricted/flagged ingredient(s)." if q else
               f"Contains {w} ingredient(s) worth monitoring." if w else
               "All ingredients are generally safe.")
    recommendation = ("Avoid or use sparingly — contains commonly questioned ingredients." if q else
                      "Use with awareness — some additives worth monitoring." if w else
                      "Safe to use — no concerning ingredients detected.")
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
        "fssai_note":      FSSAI_NOTE,
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
    print(f"Inserting {len(PRODUCTS)} Herbal Essences products...\n")
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
