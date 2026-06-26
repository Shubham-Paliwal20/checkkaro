"""
Add 20 Ohria Ayurveda products to ai_extracted_products.
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

BASE = "https://www.ohriaayurveda.com/cdn/shop/files/"

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
        return f"{name} by {brand} scores Grade A. All {total} ingredients are generally recognised as safe — 100% natural, no synthetic additives."
    elif grade == "B":
        return f"{name} by {brand} scores Grade B. {total} ingredients analysed; {w} worth knowing about (traditional Ayurvedic ingredients), no restricted additives."
    elif grade == "C":
        return f"{name} by {brand} scores Grade C. Contains {w} worth-knowing ingredients (>30% of total). Use with awareness."
    else:
        return f"{name} by {brand} scores Grade D. Contains {q} commonly questioned ingredient(s) flagged in some countries."

FSSAI_MAP = {
    "Face Care": "Cosmetics regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
    "Hair Care": "Hair care products regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
    "Body Care": "Cosmetics regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
}

# ── catalogue ─────────────────────────────────────────────────────────────────

PRODUCTS = [
    # ── FACE CARE ──
    (
        "Ohria Kumkumadi Skin Brightening Elixir",
        "Ohria Ayurveda", "Face Care",
        "Sesamum Indicum Seed Oil, Capra Aegagrus Hircus (Goat Milk), Crocus Sativus (Saffron), "
        "Pterocarpus Santalinus (Red Sandalwood), Rubia Cordifolia (Manjistha), "
        "Glycyrrhiza Glabra (Licorice), Laccifera Lacca (Lac), "
        "Ficus Benghalensis (Banyan), Ficus Religiosa (Pakar), "
        "Desmodium Gangeticum, Nelumbo Nucifera (Lotus), "
        "Berberis Aristata (Daruhaldi), Vetiveria Zizanioides (Vetiver), "
        "Prunus Cerasoides (Padmaka), Dashmool",
        BASE + "face_page-03.jpg?v=1760519263",
    ),
    (
        "Ohria Shata Dhauta Ghrita Harshringar Ghee Cream",
        "Ohria Ayurveda", "Face Care",
        "A2 Clarified Cow Butter (Ghee), "
        "Nyctanthes Arbortristis Flower Distillate (Harshringar), "
        "Nyctanthes Arbortristis Flower Oil",
        BASE + "WhatsApp_Image_2026-06-19_at_11.33.25_AM.jpg?v=1781849481",
    ),
    (
        "Ohria Papaya and Yoghurt Facial Cleanser",
        "Ohria Ayurveda", "Face Care",
        "Carica Papaya (Papaya), Lactobacillus Acidophilus (Yoghurt), "
        "Glycine Soja (Soya Extract), Glycerin, Helianthus Annuus Seed Oil, "
        "Rosa Sinensis (Rose Water), Floral Water, "
        "Cocos Nucifera Derivatives, Xanthan Gum, "
        "Rosa Sinensis Flower Extract, Prunus Armeniaca (Apricot Oil)",
        BASE + "Untitled-3-19.jpg?v=1762244852",
    ),
    (
        "Ohria Neem and Tulsi Face Wash",
        "Ohria Ayurveda", "Face Care",
        "Azadirachta Indica Seed Oil (Neem), Ocimum Tenuiflorum (Tulsi), "
        "Cocos Nucifera Derivatives, Aloe Barbadensis Leaf Gel, "
        "Triticum Sativum (Wheat Extract), Cyamopsis Tetragonoloba Gum (Guar Gum), "
        "Azadirachta Indica (Neem Water), Aloe Barbadensis Leaf Juice, "
        "Mentha Sp. (Peppermint Oil), Hemidesmus Indicus (Anantmool), "
        "Camellia Sinensis (Green Tea Extract), Rosa Sinensis Extract",
        BASE + "WhatsApp_Image_2026-01-23_at_11.06.40_1.jpg?v=1774086597",
    ),
    (
        "Ohria Tej Vardak Skin Glow Ubtan Powder",
        "Ohria Ayurveda", "Face Care",
        "Curcuma Longa (Turmeric), Rosa Sinensis Flower Powder, "
        "Musa Sapientum (Banana Powder), Lactobacillus Acidophilus (Yoghurt Powder), "
        "Carica Papaya (Papaya Powder), Azadirachta Indica (Neem Powder), "
        "Cicer Arietinum (Gram Flour), Capra Aegagrus Hircus (Goat Milk Powder), "
        "Citrus Sinensis Peel Powder, Lens Culinaris (Masoor Dal), "
        "Cocos Nucifera (Coconut Powder), Calcium Bentonite (Multani Mitti), "
        "Oryza Sativa (Navara Rice Powder), Hordeum Vulgare (Barley Flour), "
        "Santalum Album (Sandalwood Powder)",
        "",
    ),
    (
        "Ohria Rose and Pomegranate Cream",
        "Ohria Ayurveda", "Face Care",
        "Punica Granatum (Pomegranate Extract), Triticum Sativum Germ Oil, "
        "Cocos Nucifera Derivatives, Triticum Sativum Germ Extract, "
        "Rosa Damascena (Rose Water), Prunus Armeniaca (Apricot Oil), "
        "Prunus Amygdalus (Sweet Almond Oil), Withania Somnifera (Ashwagandha Oil), "
        "Rosa Damascena Flower Extract, Xanthan Gum, Glycerin",
        BASE + "Artboard1copy26.png?v=1751961898",
    ),
    (
        "Ohria Turmeric and Saffron Moisturizing Lotion",
        "Ohria Ayurveda", "Face Care",
        "Aloe Barbadensis Leaf Gel, Aloe Barbadensis Leaf Juice, "
        "Garcinia Indica (Kokum), Curcuma Longa (Turmeric), Glycerin, "
        "Glycine Soja (Soya Extract), Rosa Damascena Extract, Floral Water, "
        "Curcumin Extract, Cocos Nucifera Derivatives, Sesamum Indicum Seed Oil, "
        "Triphala, Santalum Album (Sandalwood), Crocus Sativus Water (Saffron), "
        "Rubia Cordifolia (Manjistha), Yashad Bhasma (Zinc Calx), "
        "Alpinia Galanga (Kulanjana)",
        BASE + "face_page-06_5ac8f1b3-c431-4b85-9606-1309ddc98efe.jpg?v=1762330385",
    ),
    (
        "Ohria Himalayan Clay Masque",
        "Ohria Ayurveda", "Face Care",
        "Himalayan Clay, Azadirachta Indica (Neem Extract), "
        "Cinnamomum Camphora (Camphor), Calendula Officinalis Extract, "
        "Glycerin, Kaolin, Bamboo Charcoal, "
        "Melaleuca Leucadendron Leaf Oil (Tea Tree)",
        "",
    ),
    (
        "Ohria Avbhasini Herbal Face Pack Powder",
        "Ohria Ayurveda", "Face Care",
        "Crocus Sativus (Saffron), Rosa Damascena Flower Powder, "
        "Curcuma Longa (Turmeric), Inula Racemosa (Pushkar Mool), "
        "Prunus Armeniaca Kernel Powder (Apricot), "
        "Capra Aegagrus Hircus (Goat Milk Powder), Santalum Album (Sandalwood), "
        "Citrus Sinensis Peel Powder, Lens Culinaris (Masoor Dal), "
        "Prunus Amygdalus (Almond Powder), Buchanania Lanzan (Chironji)",
        "",
    ),
    (
        "Ohria Rose and Pomegranate Jaggery Lip Balm",
        "Ohria Ayurveda", "Face Care",
        "Rosa Damascena Flower Extract, Punica Granatum (Pomegranate Extract), "
        "Cera Alba (Beeswax), Prunus Amygdalus (Almond Oil), "
        "Prunus Armeniaca (Apricot Oil), Juglans Regia (Walnut Oil), "
        "Saccharum Officinarum (Jaggery), Goghrta (Clarified Cow Butter), "
        "Garcinia Indica (Kokum Butter), Prunus Persica (Peach Oil), "
        "Sesamum Indicum Seed Oil, Triticum Aestivum Germ Oil (Vitamin E)",
        BASE + "Artboard1_5a8f5153-40ca-4ea8-9c76-9fbb147b5430.png?v=1751962992",
    ),
    # ── HAIR CARE ──
    (
        "Ohria Japa Pushpa Thailam Anti Hair Fall Oil",
        "Ohria Ayurveda", "Hair Care",
        "Sesamum Indicum Seed Oil (Til Taila), Indigofera Tinctoria (Neeli / Indigo), "
        "Eclipta Prostrata (Bhringraj), Cardiospermum Halicacabum (Balloon Vine), "
        "Phyllanthus Emblica (Amla), Glycyrrhiza Glabra (Licorice), "
        "Abrus Precatorius Root Extract (Gunja), "
        "Capra Aegagrus Hircus (Goat Milk), Bubalus Bubalis (Buffalo Milk), "
        "Bos Taurus (Cow Milk), Cocos Nucifera (Coconut Milk), "
        "Berberis Aristata (Daruhaldi), Hibiscus Rosa-Sinensis (Hibiscus)",
        BASE + "HAIR-03.jpg?v=1760008370",
    ),
    (
        "Ohria Banyan Root Hair Tonic",
        "Ohria Ayurveda", "Hair Care",
        "Ficus Benghalensis (Banyan Root), Hibiscus Rosa-Sinensis Leaf Extract, "
        "Azadirachta Indica (Neem Extract), Trigonella Foenum-Graecum (Fenugreek), "
        "Emblica Officinalis (Amla), Aloe Barbadensis Leaf Extract, "
        "Centella Asiatica (Brahmi), Triticum Sativum Germ Extract, "
        "Tocopherol (Vitamin E), Panthenol (Vitamin B5)",
        BASE + "Artboard1copy22.png?v=1751967609",
    ),
    (
        "Ohria Japa Hair Cleanser Shampoo",
        "Ohria Ayurveda", "Hair Care",
        "Hibiscus Rosa-Sinensis Leaf Extract, Cocos Nucifera Derivatives, "
        "Apis Indica (Honey), Cocos Nucifera (Coconut Milk), "
        "Aloe Barbadensis Leaf Gel, Glycerin, "
        "Emblica Officinalis (Amla), Acacia Concinna (Shikakai), "
        "Sapindus Mukorossi (Reetha), Prunus Armeniaca (Apricot Oil), "
        "Juglans Regia (Walnut Extract), Cyamopsis Tetragonoloba Gum, "
        "Triticum Sativum Germ Extract",
        BASE + "WhatsApp_Image_2026-03-20_at_11.52.35_AM.jpg?v=1773988037",
    ),
    (
        "Ohria Keshya Hair Vitalizer Rosemary",
        "Ohria Ayurveda", "Hair Care",
        "Lepidium Sativum (Halim / Garden Cress Seeds), "
        "Ziziphus Mauritiana (Ber / Indian Jujube), "
        "Trigonella Foenum-Graecum (Fenugreek), "
        "Hibiscus Rosa-Sinensis (Hibiscus), "
        "Linum Usitatissimum (Flaxseed), "
        "Rosmarinus Officinalis Leaf Oil, "
        "Lavandula Stoechas (Lavender Oil), "
        "Melaleuca Leucadendron Leaf Oil (Tea Tree), Glycerin",
        BASE + "Artboard1copy19.png?v=1751962204",
    ),
    (
        "Ohria Keshya Anti Frizz Hair Oil",
        "Ohria Ayurveda", "Hair Care",
        "Sesamum Indicum Seed Oil, Ziziphus Mauritiana (Jujube Leaves), "
        "Ricinus Communis (Castor Oil), Brassica Juncea (Mustard Oil), "
        "Emblica Officinalis (Amla Extract), Vitis Vinifera (Grapeseed Oil), "
        "Hibiscus Rosa-Sinensis Flower, Nigella Sativa (Kalonji), "
        "Trigonella Foenum-Graecum (Fenugreek), Azadirachta Indica (Neem)",
        "",
    ),
    (
        "Ohria Moringa and Ylang Ylang Hair Serum",
        "Ohria Ayurveda", "Hair Care",
        "Argania Spinosa Kernel Oil (Argan), Moringa Oleifera Seed Oil, "
        "Juglans Regia (Walnut Oil), Linum Usitatissimum (Flaxseed Oil), "
        "Vitis Vinifera (Grapeseed Oil), Sesamum Indicum Seed Oil, "
        "Triticum Sativum Germ Oil (Vitamin E), "
        "Cananga Odorata Flower Oil (Ylang Ylang)",
        BASE + "HAIR-11.jpg?v=1759999480",
    ),
    (
        "Ohria Nimba Karanj Thailam Anti Dandruff Hair Oil",
        "Ohria Ayurveda", "Hair Care",
        "Sesamum Indicum Seed Oil, Millettia Pinnata Seed Oil (Karanj), "
        "Azadirachta Indica (Neem Extract), Triphala, "
        "Cyperus Scariosus (Nagarmotha), Trigonella Foenum-Graecum (Fenugreek), "
        "Rubia Cordifolia (Manjistha), Hemidesmus Indicus (Sariva), "
        "Acacia Catechu (Khadira), Psoralea Corylifolia Seed Oil (Bakuchi), "
        "Cinnamomum Camphora (Camphor), Murraya Koenigii (Curry Leaves), "
        "Millettia Pinnata Extract (Karanja)",
        "",
    ),
    # ── BODY CARE ──
    (
        "Ohria Rose and Pomegranate Shower Oil",
        "Ohria Ayurveda", "Body Care",
        "Prunus Armeniaca (Apricot Oil), Vitis Vinifera (Grapeseed Oil), "
        "Juglans Regia (Walnut Oil), Tocopherol (Vitamin E), "
        "Rosa Damascena Flower Oil, Punica Granatum (Pomegranate Extract), "
        "Prunus Amygdalus (Sweet Almond Oil), Butyrospermum Parkii (Shea Butter)",
        BASE + "body-01_bcfc70b9-ee9e-42cf-8090-19da2e1c1ac2.jpg?v=1775297272",
    ),
    (
        "Ohria Amrit Ras Shower Wash",
        "Ohria Ayurveda", "Body Care",
        "Ocimum Sanctum (Tulsi), Cocos Nucifera Derivatives, "
        "Apis Indica (Honey), Goghrta (Clarified Cow Butter), "
        "Rosa Damascena Flower Extract, Musa Sapientum (Banana Extract), "
        "Glycerin",
        "",
    ),
    (
        "Ohria Amrit Ras Foot Balm",
        "Ohria Ayurveda", "Body Care",
        "Sesamum Indicum Seed Oil, Brassica Juncea (Mustard Oil), "
        "Ricinus Communis (Castor Oil), Cera Alba (Beeswax), "
        "Prunus Amygdalus (Sweet Almond Oil), Garcinia Indica (Kokum Butter), "
        "Goghrta (Clarified Cow Butter), Saccharum Officinarum (Cane Sugar), "
        "Apis Indica (Honey), Triticum Aestivum Germ Oil (Vitamin E), "
        "Boswellia Carterii (Frankincense Oil), Cedrus Deodara (Cedarwood Oil)",
        BASE + "Artboard1copy4.png?v=1751962952",
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
               "All ingredients are 100% natural — no synthetic additives detected.")
    recommendation = ("Avoid or use sparingly — contains commonly questioned ingredients." if q else
                      "Use with awareness — contains traditional Ayurvedic ingredients worth knowing." if w else
                      "Safe to use — 100% natural formula with no concerning additives.")
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
    print(f"Inserting {len(PRODUCTS)} Ohria Ayurveda products...\n")
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
