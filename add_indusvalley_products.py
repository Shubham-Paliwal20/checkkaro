"""
Add 11 Indus Valley products to ai_extracted_products.
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

IV_CDN = "https://cdn.shopify.com/s/files/1/0593/5720/0560/files/"
IV_CDN2 = "https://www.buyindusvalley.in/cdn/shop/files/"
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

FSSAI_MAP = {
    "Hair Colour": "Hair colourants regulated under Schedule Q of Drugs and Cosmetics Act 1940. Patch test 48 hrs before use.",
    "Haircare":    "Hair care products regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
    "Skincare":    "Cosmetics regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
}

# ── catalogue ─────────────────────────────────────────────────────────────────

PRODUCTS = [
    # ── HAIR COLOUR ──
    (
        "Indus Valley Damage Free Natural Gel Hair Colour",
        "Indus Valley", "Hair Colour",
        "Aqua, Aloe Barbadensis Leaf Juice, Glycerin, "
        "Guar Hydroxypropyltrimonium Chloride, Helianthus Annuus Seed Oil, "
        "Carbomer, Alpha Olefin Sulfonate, Citrus Aurantium Dulcis Peel Oil, "
        "Triticum Vulgare Germ Oil, Simmondsia Chinensis Seed Oil, "
        "Sodium Picramate, Potassium Sorbate, Sodium Benzoate, Benzyl Alcohol, "
        "Sodium Perborate, Toluene-2,5-Diamine Sulfate, "
        "Phyllanthus Emblica Fruit Powder, Lawsonia Inermis Leaf Powder, "
        "Cellulose Gum, Sodium Chloride, Ocimum Basilicum Leaf Powder, "
        "Cocos Nucifera Oil, Citric Acid, 4-Chlororesorcinol, P-Aminophenol, "
        "M-Aminophenol, 2-Amino-6-Chloro-4-Nitrophenol, 4-Amino-2-Hydroxytoluene, "
        "1-Naphthol, Picramic Acid, 1,5-Naphthalenediol",
        INCI + "/28af8884-bd6a-41ec-9397-cbc7ae9763e7/products/"
               "indus-valley-hair-colour-gel/"
               "indus-valley-hair-colour-gel_front_photo_original.jpeg",
    ),
    # ── HAIR CARE ──
    (
        "Indus Valley Bio Organic Growout Hair Oil",
        "Indus Valley", "Haircare",
        "Helianthus Annuus Seed Oil, Hibiscus Rosa Sinensis Flower Extract, "
        "Allium Cepa Root Extract, Cyperus Scariosus Root Extract, "
        "Centella Asiatica Leaf Extract, Urtica Dioica Leaf Extract, "
        "Eclipta Alba Leaf Extract, Terminalia Chebula Fruit Extract, "
        "Syzygium Aromaticum Oil, Vitis Vinifera Seed Oil, "
        "Nardostachys Jatamansi Root Extract",
        IV_CDN + "growout-oil-100ml_9e675c90-e52a-4182-b41f-e25aa3b28550.jpg",
    ),
    (
        "Indus Valley Bio Organic Growout Hair Shampoo",
        "Indus Valley", "Haircare",
        "Himalayan Spring Purified Water, Triticum Vulgare Seed Extract, "
        "Centella Asiatica Leaf Extract, Eclipta Alba Leaf Extract, "
        "Cyperus Scariosus Root Extract, Terminalia Chebula Fruit Extract, "
        "Urtica Dioica Leaf Extract, Allium Cepa Root Extract, "
        "Nardostachys Jatamansi Root Extract, Hibiscus Rosa Sinensis Flower Extract, "
        "Persea Gratissima Oil, Cocos Nucifera Oil",
        IV_CDN + "Growout-Hair-Fall-Control-Shampoo.jpg?v=1757398645",
    ),
    (
        "Indus Valley Bio Organic Colour Protective Shampoo",
        "Indus Valley", "Haircare",
        "Himalayan Spring Purified Water, Coco Betaine, Cocamidopropyl Betaine, "
        "Aloe Barbadensis Leaf Juice, Phyllanthus Emblica Extract, "
        "Rubia Cordifolia Extract, Trigonella Foenum-Graecum Seed Extract, "
        "Withania Somnifera Extract, Lawsonia Inermis Extract, "
        "Soya Protein, Casein, Honey, Melaleuca Alternifolia Leaf Oil, "
        "Citrus Limon Peel Oil, Glycerin",
        IV_CDN2 + "colour-protective-shampoo-200ml_50740e49-8907-49a1-aedb-d388161b5717.jpg",
    ),
    (
        "Indus Valley Bio Organic Argan Oil Shampoo",
        "Indus Valley", "Haircare",
        "Himalayan Spring Purified Water, Wheat Protein Extract, Decyl Glucoside, "
        "C14-16 Olefin Sulfonate, Cocamidopropyl Betaine, "
        "Argania Spinosa Kernel Oil, Theobroma Cacao Seed Butter, Parfum, "
        "Cocos Nucifera Oil, Panthenol, Polyquaternium-11, Cetyl Alcohol, "
        "Hydrolyzed Soya Protein, Sodium Benzoate, Behentrimonium Chloride, "
        "Cetrimonium Chloride, Amodimethicone, Potassium Sorbate, Phenoxyethanol, "
        "Ascorbic Acid, Disodium EDTA, Cyclopentasiloxane, "
        "Hydroxypropyltrimonium Chloride",
        IV_CDN + "argan-oil-shampoo-200ml.jpg?v=1757398642",
    ),
    (
        "Indus Valley Anti Dandruff Shampoo",
        "Indus Valley", "Haircare",
        "Himalayan Spring Purified Water, Climbazole, Salicylic Acid, "
        "Rosmarinus Officinalis Extract, Aloe Barbadensis Leaf Juice, "
        "Glycerin, Hydrolyzed Soy Protein",
        IV_CDN2 + "anti-dandruff-shampoo-001.jpg?v=1757398639",
    ),
    (
        "Indus Valley Deep Nourishing Hair Ultima Spa",
        "Indus Valley", "Haircare",
        "Aqua, Cetyl Alcohol, Cyclopentasiloxane, Behentrimonium Chloride, "
        "Stearyl Alcohol, Phenyl Trimethicone, Triticum Vulgare Extract, "
        "Azadirachta Indica, Mentha Extract, Butylene Glycol, Cocos Nucifera Oil, "
        "Collagen, Trigonella Foenum-Graecum Seeds Extract, "
        "Lawsonia Inermis Extract, Panthenol, Hydrolyzed Wheat Protein, "
        "Citrus Limon Peel Oil, Glycol Stearate, Prunus Dulcis Oil, "
        "Rosmarinus Officinalis Oil, Camellia Sinensis Leaf Oil, "
        "Ocimum Basilicum Oil, Lavandula Angustifolia Oil, Casein, "
        "Polyquaternium-10, Sorbic Acid, Citric Acid, Phenoxyethanol, "
        "Sodium Benzoate",
        IV_CDN + "ultima-spa-175ml.webp?v=1777360468",
    ),
    # ── SKIN CARE ──
    (
        "Indus Valley Brightening Depigmentation Gel",
        "Indus Valley", "Skincare",
        "Melaleuca Alternifolia Leaf Oil, Lac Vaccinum, "
        "Citrus Grandis Seed Extract, Triticum Vulgare Germ Oil, Honey, "
        "Cellulose Gum, Cyamopsis Tetragonoloba Gum, "
        "Benzyl Alcohol, Phenoxyethanol, Potassium Sorbate",
        IV_CDN + "Depigmentation-gel-iv.jpg?v=1763988237",
    ),
    (
        "Indus Valley Soothing & Firming Light Day Cream",
        "Indus Valley", "Skincare",
        "Rosa Damascena Extract, Ocimum Basilicum Oil, "
        "Simmondsia Chinensis Seed Oil, Citrus Limon Fruit Extract, "
        "Triticum Vulgare Germ Oil, Potassium Hydroxide, Sodium Borate, "
        "Sesamum Indicum Seed Oil, Stearic Acid, Potassium Sorbate, "
        "Sodium Benzoate, Phenoxyethanol, Benzyl Alcohol",
        INCI + "/12b3332c-844c-4142-ab72-9cfe0c79e703/products/"
               "indus-valley-soothing-firming-light-day-cream/"
               "indus-valley-soothing-firming-light-day-cream_front_photo_original.jpeg",
    ),
    (
        "Indus Valley Bio Organic Aloe Vera Gel with Green Tea",
        "Indus Valley", "Skincare",
        "Aloe Barbadensis Leaf Juice, Rosa Damascena Water, "
        "Triticum Vulgare Extract, Camellia Sinensis Leaf Extract, Honey, "
        "Citrus Limon Peel Extract, Carbomer, Potassium Hydroxide, "
        "Sodium Benzoate, Benzyl Alcohol, Potassium Sorbate",
        INCI + "/c685d112-421f-4b61-9971-2c7746975e22/products/"
               "indus-valley-alovera-gel-with-green-tea-extract/"
               "indus-valley-alovera-gel-with-green-tea-extract_front_photo_original.jpeg",
    ),
    (
        "Indus Valley Saffron Water Toner",
        "Indus Valley", "Skincare",
        "Spring Water, Crocus Sativus Flower Extract, Aloe Barbadensis Leaf Extract, "
        "Mint Hydrosol, Rosa Damascena Extract, Vitis Vinifera Seed Extract, "
        "Glycerin, Levulinic Acid, PCA Ethyl Cocoyl Arginate",
        INCI + "/de234c9b-7691-4c07-82f7-48985697fc4e/products/"
               "indus-valley-saffron-water/"
               "indus-valley-saffron-water_front_photo_original.jpeg",
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
    print(f"Inserting {len(PRODUCTS)} Indus Valley products...\n")
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
