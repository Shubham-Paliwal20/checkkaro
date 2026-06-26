"""
Add 13 Kama Ayurveda products to ai_extracted_products.
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

FSSAI_MAP = {
    "Face Care": "Cosmetics regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
    "Hair Care": "Hair care products regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
}

# ── catalogue ─────────────────────────────────────────────────────────────────

PRODUCTS = [
    # ── FACE CARE ──
    (
        "Kama Ayurveda Kumkumadi Facial Oil",
        "Kama Ayurveda", "Face Care",
        "Caprae Lac, Sesamum Indicum Seed Oil, Crocus Sativus Stigma Extract, "
        "Caesalpinia Sappan Bark Extract, Glycyrrhiza Glabra Root Powder, "
        "Rubia Cordifolia Root Powder, Shellac, Ficus Benghalensis Bark Extract, "
        "Eichhornia Crassipes Extract, Nelumbo Nucifera Flower Powder, "
        "Prunus Cerasus Extract, Vetiveria Zizanoides Root Powder, "
        "Pelargonium Graveolens Oil, Vetiveria Zizanoides Root Oil, "
        "Citrus Reticulata Peel Oil, Rosa Damascena Flower Oil, "
        "Citronellol, Geraniol, Linalool",
        INCI + "/36bb8986-11ad-4cb6-90ce-1a14266281b5/products/"
               "kama-ayurveda-kumkumadi-facial-oil/"
               "kama-ayurveda-kumkumadi-facial-oil_front_photo_original.jpeg",
    ),
    (
        "Kama Ayurveda Kumkumadi Miraculous Beauty Fluid Ayurvedic Night Serum",
        "Kama Ayurveda", "Face Care",
        "Caprae Lac, Sesamum Indicum Seed Oil, Caesalpinia Sappan Bark Extract, "
        "Crocus Sativus Flower Extract, Glycyrrhiza Glabra Root Powder, "
        "Rubia Cordifolia Root Powder, Shellac, Ficus Indica Bark, "
        "Eichhornia Crassipes Extract, Nelumbo Nucifera Flower Powder, "
        "Prunus Cerasus Extract, Vetiveria Zizanoides Root Powder",
        INCI + "/6a7ebbbb-26d5-4c13-8a3c-32d6173cf0f3/products/"
               "kama-ayurveda-kumkumadi-miraculous-beauty-fluid-ayurvedic-night-serum/"
               "kama-ayurveda-kumkumadi-miraculous-beauty-fluid-ayurvedic-night-serum_front_photo_original.jpeg",
    ),
    (
        "Kama Ayurveda Eladi Hydrating Face Cream",
        "Kama Ayurveda", "Face Care",
        "Aqua, Stearic Acid, Cetyl Alcohol, Cocos Nucifera Fruit Extract, "
        "Cetearyl Olivate, Sorbitan Olivate, Rose Essential Oil, Jasmine Essential Oil, "
        "Vetiveria Zizanoides Extract, Shorea Robusta Leaf Extract, "
        "Sesamum Indicum Seed Oil, Myristica Fragrans Extract, "
        "Mesua Ferrea Flower Extract, Cinnamomum Zeylanicum Bark Extract, "
        "Cedrus Deodara Wood Extract, Elettaria Cardamomum Seed Powder, "
        "Panthenol, Allantoin, Xanthan Gum, Aloe Barbadensis Leaf Juice, "
        "Phenoxyethanol, Disodium EDTA",
        INCI + "/db778955-9843-4fd8-87b5-b397c24eddcb/ingredients/"
               "kama-ayurveda-eladi-hydrating-face-cream/"
               "kama-ayurveda-eladi-hydrating-face-cream_original.jpeg",
    ),
    (
        "Kama Ayurveda Anti Acne Cleansing Foam with Neem Tulsi Tea Tree",
        "Kama Ayurveda", "Face Care",
        "Aqua, Sodium Cocoyl Glutamate, Disodium Cocoyl Glutamate, "
        "Sodium Cocoamphoacetate, Sodium Lauroyl Glutamate, Dimethyl Isosorbide, "
        "Phragmites Communis Extract, Poria Cocos Extract, Salicylic Acid, "
        "Aloe Barbadensis Leaf Juice, Sodium Benzoate, Potassium Sorbate, "
        "Azadirachta Indica Seed Oil, Ocimum Sanctum Leaf Oil, "
        "Melaleuca Alternifolia Leaf Oil, Calendula Officinalis Flower Extract, "
        "Allantoin, Xanthan Gum",
        INCI + "/dc5f9ce2-ea16-4108-a422-a622ccdd11b7/products/"
               "kama-ayurveda-anti-acne-cleansing-foam-with-neem-tulsi-tea-tree/"
               "kama-ayurveda-anti-acne-cleansing-foam-with-neem-tulsi-tea-tree_front_photo_original.jpeg",
    ),
    (
        "Kama Ayurveda Kumkumadi Clarifying and Brightening Cleansing Oil",
        "Kama Ayurveda", "Face Care",
        "Caprylic/Capric Triglyceride, Caprae Lac, Helianthus Annuus Seed Oil, "
        "Simmondsia Chinensis Seed Oil, Laureth-4, Mipa-Laureth Sulfate, "
        "Sesamum Indicum Seed Oil, Cocamide DEA, Tocopheryl Acetate, "
        "Glycyrrhiza Glabra Root Powder, Rubia Cordifolia Root Powder, Shellac, "
        "Citrus Medica Fruit Juice Extract, Caesalpinia Sappan Stem Powder, "
        "Crocus Sativus Stigma Extract, Ficus Benghalensis Bark Extract, "
        "Monochoria Hastata Oil, Nelumbo Nucifera Flower Extract, "
        "Prunus Cerasus Flower Extract, Vetiveria Zizanoides Extract, "
        "Emblica Officinalis Fruit Extract, Glycine Soja Oil, "
        "Centella Asiatica Extract, Beta-Carotene, Daucus Carota Sativa Root Extract",
        INCI + "/6dfda6f3-9b22-4bea-8df0-e9f22261b99a/products/"
               "kama-ayurveda-kumkumadi-clarifying-and-brightening-cleaning-oil/"
               "kama-ayurveda-kumkumadi-clarifying-and-brightening-cleaning-oil_front_photo_original.jpeg",
    ),
    (
        "Kama Ayurveda Foaming Face Wash",
        "Kama Ayurveda", "Face Care",
        "Aqua, Aloe Barbadensis Leaf Juice, Sodium Lauroyl Sarcosinate, Glycerine, "
        "Cyamopsis Tetragonoloba Gum, Vetiveria Zizanoides Root Extract, "
        "Ocimum Sanctum Leaf Extract, Glycyrrhiza Glabra Root Extract, "
        "Cuminum Cyminum Seed Extract, Cassia Alata Leaf Extract, "
        "Potassium Sorbate, Polianthes Tuberosa Flower Oil, "
        "Simmondsia Chinensis Seed Oil, Salicylic Acid, "
        "Rose Essential Oil, Jasmine Essential Oil",
        INCI + "/469907fb-a073-4199-8e37-0445f6c7548c/products/"
               "foaming-face-wash-kama-ayurveda/"
               "foaming-face-wash-kama-ayurveda_front_photo_original.jpeg",
    ),
    (
        "Kama Ayurveda Kumkumadi Brightening Ayurvedic Face Scrub",
        "Kama Ayurveda", "Face Care",
        "Aqua, Helianthus Annuus Seed Oil, Glyceryl Stearate, "
        "Juglans Regia Shell Powder, Stearic Acid, Glycerine, Cetyl Alcohol, "
        "Phenoxyethanol, Prunus Amygdalus Dulcis Seed Extract, "
        "Crocus Sativus Flower Extract, BHT, Vetiveria Zizanoides Extract, "
        "Sesamum Indicum Seed Oil, Rubia Cordifolia Root Powder, "
        "Prunus Cerasoides Extract, Nelumbo Nucifera Flower Powder, "
        "Monochoria Vaginalis Extract, Laciferra Lacca, "
        "Glycyrrhiza Glabra Root Powder, Ficus Benghalensis Bark Powder, "
        "Caprae Lac, Caesalpinia Sappan Stem Powder",
        INCI + "/916c4fd6-0b08-4f04-806a-1e96554e7d35/products/"
               "kama-ayurveda-kumkumadi-brightening-ayurvedic-face-scrub/"
               "kama-ayurveda-kumkumadi-brightening-ayurvedic-face-scrub_front_photo_original.jpeg",
    ),
    (
        "Kama Ayurveda Rose and Jasmine Face Cleanser",
        "Kama Ayurveda", "Face Care",
        "Aqua, Aloe Barbadensis Leaf Juice, Sodium Lauroyl Sarcosinate, Glycerine, "
        "Cyamopsis Tetragonoloba Gum, Vetiveria Zizanoides Root Extract, "
        "Ocimum Sanctum Leaf Extract, Glycyrrhiza Glabra Root Extract, "
        "Cuminum Cyminum Seed Extract, Cassia Alata Leaf Extract, "
        "Potassium Sorbate, Polianthes Tuberosa Flower Oil, "
        "Simmondsia Chinensis Seed Oil, Salicylic Acid, "
        "Rosa Damascena Flower Oil, Jasminum Officinale Oil",
        INCI + "/03cbc08f-2012-4b10-88c6-38f245461c9d/products/"
               "kama-ayurveda-rose-and-jasmine-cleanser/"
               "kama-ayurveda-rose-and-jasmine-cleanser_front_photo_original.jpeg",
    ),
    (
        "Kama Ayurveda Soap Free Face Cleanser Powder",
        "Kama Ayurveda", "Face Care",
        "Avena Sativa (Colloidal Oatmeal), Vigna Radiata Seed Extract, "
        "Azadirachta Indica Leaf Extract, Cicer Arietinum Seed Powder, "
        "Foeniculum Vulgare Fruit Powder, Prunus Amygdalus Dulcis Seedcoat Powder, "
        "Rosa Damascena Flower Powder, Curcuma Longa Root Powder, "
        "Santalum Album, Cinnamomum Camphora",
        INCI + "/b126d4c6-48a0-4e96-93f5-f1740c6c68b6/products/"
               "kama-ayurveda-face-cleanser/"
               "kama-ayurveda-face-cleanser_front_photo_original.jpeg",
    ),
    (
        "Kama Ayurveda Brightening Night Cream",
        "Kama Ayurveda", "Face Care",
        "Aqua, Stearic Acid, Cetyl Alcohol, Cetearyl Olivate, Sorbitan Olivate, "
        "Cyclopentasiloxane, Dimethicone, Dimethicone Crosspolymer, Phenyltrimethicone, "
        "D-Panthenol, Xanthan Gum, Allantoin, Disodium EDTA, "
        "Vetiveria Zizanoides Extract, Symplocos Racemosa Extract, "
        "Shorea Robusta Leaf Extract, Sesamum Indicum Seed Oil, "
        "Crocus Sativus Flower Extract, Myristica Fragrans Extract, "
        "Mesua Ferrea Flower Extract, Nelumbo Nucifera Flower Powder, "
        "Glycyrrhiza Glabra Root Powder, Cocos Nucifera Fruit Extract, "
        "Cinnamomum Zeylanicum Bark Extract, Cedrus Deodara Wood Extract, "
        "Elettaria Cardamomum Seed Powder, Caprae Lac, "
        "Caesalpinia Sappan Stem Powder, Aloe Barbadensis Leaf Juice, "
        "Callicarpa Macrophylla Flower Extract, Phenoxyethanol",
        INCI + "/ef272af2-0bd9-4a82-918a-9bc64940a0e3/products/"
               "kama-ayurveda-brightening-night-cream/"
               "kama-ayurveda-brightening-night-cream_front_photo_original.jpeg",
    ),
    # ── HAIR CARE ──
    (
        "Kama Ayurveda Bringadi Intensive Hair Treatment Oil",
        "Kama Ayurveda", "Hair Care",
        "Indigofera Tinctoria Leaf Extract, Cardiospermum Halicacabum Leaf Extract, "
        "Eclipta Prostrata Leaf Extract, Phyllanthus Emblica Fruit Juice, "
        "Sesamum Indicum Seed Oil, Lac, Cocos Nucifera Fruit Extract, "
        "Glycyrrhiza Glabra Root Powder, Rosmarinus Officinalis Leaf Oil, "
        "Lavandula Hybrida Oil",
        INCI + "/dc14c8fa-953e-42f6-89a0-8fbcc995c4bf/products/"
               "kama-ayurveda-bringadi-hair-treatment/"
               "kama-ayurveda-bringadi-hair-treatment_front_photo_original.jpeg",
    ),
    (
        "Kama Ayurveda Bringadi Hair Cleanser Shampoo",
        "Kama Ayurveda", "Hair Care",
        "Aqua, Lauryl Glucoside, Disodium Cocoyl Glutamate, "
        "Sodium Cocoamphoacetate, Glycerine, Betaine, Citric Acid, "
        "Sodium PCA, PCA Glyceryl Oleate, Hydrolyzed Soy Protein, "
        "Hydrolyzed Vegetable Protein, Sodium Benzoate, Potassium Sorbate, "
        "Lavandula Hybrida Oil, Rosmarinus Officinalis Leaf Oil, "
        "Xanthan Gum, D-Panthenol, Emblica Officinalis Fruit Extract, "
        "Indigofera Tinctoria Leaf Extract, Glycyrrhiza Glabra Root Extract, "
        "Eclipta Alba Leaf Extract",
        INCI + "/166c00f1-77dc-4c46-9d37-2af2ecf11c08/products/"
               "kama-ayurveda-bringadi-hair-cleanser/"
               "kama-ayurveda-bringadi-hair-cleanser_front_photo_original.jpeg",
    ),
    (
        "Kama Ayurveda Hair Conditioner",
        "Kama Ayurveda", "Hair Care",
        "Aqua, Cetearyl Alcohol, Lecithin, Sodium Cetearyl Sulfate, Vegetable Oil, "
        "Arachidyl Alcohol, Behenyl Alcohol, Arachidyl Glucoside, "
        "Coco-Caprylate/Caprate, Hydrolyzed Vegetable Protein, "
        "Sodium Benzoate, Potassium Sorbate, Lac, Tocopheryl Acetate, "
        "Linalool, Rosmarinus Officinalis Leaf Extract, Lavandula Hybrida Oil, "
        "Lavandula Angustifolia Oil, Salvia Sclarea Oil, Limonene, Geraniol, "
        "Coumarin, Eugenol, Citronellol, Eclipta Prostrata Leaf Extract, "
        "Citric Acid, Sesamum Indicum Seed Oil, Sodium Gluconate, "
        "Indigofera Tinctoria Leaf Extract, Emblica Officinalis Fruit Extract, "
        "Cocos Nucifera Fruit Juice, Cardiospermum Halicacabum Leaf Extract, "
        "Glycyrrhiza Glabra Root Powder, Abrus Precatorius Root Extract, "
        "Cinnamomum Camphora, Banksia Serrata Flower Extract",
        INCI + "/4b476cb9-18e3-4c8a-bed3-744435169327/products/"
               "kama-ayurveda-hair-conditioner/"
               "kama-ayurveda-hair-conditioner_front_photo_original.jpeg",
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
    print(f"Inserting {len(PRODUCTS)} Kama Ayurveda products...\n")
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
