"""
Add 10 Arata products (full INCI only) to ai_extracted_products.
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

CDN = "https://www.arata.in/cdn/shop/files/"

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
    "Haircare":   "Hair care products are regulated under the Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020. Ingredient labelling is mandatory.",
    "Face Wash":  "Regulated under Cosmetics Rules 2020. Surfactant concentrations must meet BIS standards.",
    "Skincare":   "Cosmetics regulated under the Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020. Ingredient labelling is mandatory.",
    "Serums":     "Face serums regulated as cosmetics under Cosmetics Rules 2020. Active concentrations should match label claims.",
    "Sunscreen":  "Sunscreens classified as cosmetics under Drugs & Cosmetics Act. SPF values must be validated per ISO 24444.",
    "Body Care":  "Body care products regulated under Cosmetics Rules 2020. Ingredient labelling mandatory. Preservative limits must comply with Schedule Q.",
}

# ── catalogue (name, brand, category, variant, net_wt, ingredients_raw, image_url) ──

PRODUCTS = [
    (
        "Arata Damage Defence Super Shampoo", "Arata", "Haircare", "Damage Defence Super Shampoo", "200 ml",
        "Purified Water, Sodium Lauroyl Methyl Isethionate, Alpha Olefin Sulfonate, "
        "Sodium Cocoyl Isethionate, Cocamidopropyl Betaine, "
        "Divinyldimethicone/Dimethicone Copolymer, "
        "Acrylamidopropyltrimonium Chloride/Acrylamide Copolymer, Phenoxyethanol, "
        "Fragrance, Propylene Glycol, Sodium Chloride, Glycol Distearate, Panthenol, "
        "Dimethiconol, Apple Cider Vinegar, Alpha-Glucan Hydroxypropyltrimonium Chloride, "
        "Citric Acid, TEA-Dodecylbenzene Sulfonate, Guar Hydroxypropyltrimonium Chloride, "
        "Piroctone Olamine, Sodium Hyaluronate, Tocopheryl Acetate, C12-13 Alketh-23, "
        "C12-13 Alketh-3, Arginine, Hydrolyzed Pea Protein, Hydrolyzed Soy Protein, "
        "Laureth-23, Potassium Sorbate",
        CDN + "DamageDefenceSuperShampoo_200ml_466bc8bc-4df8-4f04-b590-833b003e9d40.webp",
    ),
    (
        "Arata Anti-Dandruff Shampoo", "Arata", "Haircare", "Anti-Dandruff Shampoo", "200 ml",
        "Aqua, Cocamidopropyl Betaine, Sodium Cocoyl Isethionate, Lauryl Glucoside, "
        "Polyquaternium-10, Glycerin, Polyquaternium-7, Ethylene Glycol Distearate, "
        "Octyldodecanol, Leptospermum Scoparium Branch/Leaf Oil, "
        "Piper Nigrum Seed Extract, Magnolia Officinalis Bark Extract, "
        "Phenoxyethanol, Ethylhexylglycerin, Piroctone Olamine, "
        "Trigonella Foenum-Graecum Seed Extract, Azadirachta Indica Leaf Extract, "
        "Melaleuca Alternifolia Leaf Extract, Hamamelis Virginiana Extract, "
        "Parfum, Disodium EDTA",
        CDN + "Anti_Dandruff_Shampoo_200_ml_1.webp?v=1780481666&width=1080",
    ),
    (
        "Arata Anti-Hair Fall Intensive Shampoo", "Arata", "Haircare", "Anti-Hair Fall Intensive Shampoo", "200 ml",
        "Purified Water, Alpha Olefin Sulfonate, Cocamidopropyl Betaine, Glycerin, "
        "Oryza Sativa Rice Extract, Sodium Chloride, Dimethiconol, Glycol Distearate, "
        "Phenoxyethanol, Rosmarinus Officinalis Leaf Extract, Fragrance, "
        "PEG-150 Distearate, Sodium Methyl Cocoyl Taurate, Polyquaternium 39, "
        "Polyquaternium 7, Sodium Cocoamphoacetate, Polyquaternium 10, Cocamide MEA, "
        "Guar Hydroxypropyltrimonium Chloride, Lauryl Glucoside, Carbomer, Propanediol, "
        "Caffeine, Disodium EDTA, Alpha-Glucan Hydroxypropyltrimonium Chloride, "
        "Propylene Glycol, Sodium Cocoyl Glutamate, Sodium Lauryl Glucose Carboxylate, "
        "Platycladus Orientalis Leaf Extract, Sodium Benzoate, "
        "Triethanolamine Dodecylbenzene Sulfonate, Citric Acid, "
        "Zingiber Officinale Root Extract, Biotin, Artemisia Argyi Leaf Extract, "
        "Trifolium Pratense Leaf Extract, Potassium Sorbate",
        CDN + "Anti-HairFallIntensiveShampoo200ml_8ca11048-13ab-4770-9b40-71c65169f7a4.webp",
    ),
    (
        "Arata Damage Defence Super Conditioner", "Arata", "Haircare", "Damage Defence Super Conditioner", "200 ml",
        "Demineralized Water, Bhringraj Extract, Rice Extract, Flaxseed Oil, "
        "Pumpkin Seed Butter, Glycerine, Guar Hydroxypropyltrimonium Chloride, "
        "Tetrasodium EDTA, Behentrimonium Chloride, Cetyl Alcohol, Emulsifying Wax, "
        "Behentrimonium Methosulfate, Cetrimonium Chloride, Quaternium-98, "
        "Polyquaternium-7, Cyclopentasiloxane, Hydrolyzed Wheat Protein, "
        "Hydrolyzed Soy Protein, Hydrolyzed Corn Protein, PCA Glyceryl Oleate, "
        "Pentylene Glycol, Lactic Acid, Sodium Lactate, Arginine, Sorbitol, "
        "Saccharide Isomerate, Citric Acid, Sodium Citrate, Safe Fragrance, "
        "Sodium Benzoate, Potassium Sorbate, Phenoxyethanol, Ethylhexylglycerine",
        CDN + "DamageDefenceSuperConditioner_200ml_1236bbc5-4951-4c4c-9bfc-0d88e012e896.webp",
    ),
    (
        "Arata Hair Growth Intensive Serum", "Arata", "Haircare", "Hair Growth Intensive Serum", "30 ml",
        "Aqua, Capixyl, Rice Water Extract, Aloe Vera Extract, Redensyl, Procapil, "
        "Glycerin, Xylitylglucoside, Anhydroxylitol, Xylitol, Maltitol, "
        "PEG-40 Hydrogenated Castor Oil, Gooseberry Extract, Turmeric Extract, "
        "Sodium Benzoate, Potassium Sorbate, Fragrance, Coffee Extract, "
        "Xanthan Gum, Propanediol, Onion Extract, Glycine, Sodium Gluconate, Allantoin",
        CDN + "HairGrowthIntensiveSerum_4ebb45eb-007e-489b-8a5d-b56643771f84.webp",
    ),
    (
        "Arata Damage Defence Super Serum", "Arata", "Haircare", "Damage Defence Super Serum", "30 ml",
        "Camellia Sinensis Oil, Nelumbo Nucifera Lotus Oil, Olea Europaea Olive Oil, "
        "Cyclopentasiloxane, Dimethiconol, Hydrogenated Polyisobutene, "
        "Simmondsia Chinensis Jojoba Seed Oil, Parfum",
        CDN + "DamageDefenceSuperSerum_30ml_1cd76dbc-fd1a-4228-8eb4-d94f46b0c22d.webp",
    ),
    (
        "Arata Strong Hold Styling Gel", "Arata", "Haircare", "Strong Hold Styling Gel", "100 ml",
        "Purified Water, Linum Usitatissimum Flaxseed Extract, Propanediol, "
        "Dehydroxanthan Gum, Caprylhydroxamic Acid, Caprylyl Glycol, Glycerin, "
        "Essential Oils, Parfum, Sodium Gluconate",
        CDN + "StrongHoldStylingGel_100ml_8164a1f2-cef2-4a99-9b38-c385be55420b.webp",
    ),
    (
        "Arata Texturising Styling Spray", "Arata", "Haircare", "Texturising Styling Spray", "50 ml",
        "Aqua, Butylene Glycol, Magnesium Sulfate, Phenoxyethanol, Triethylene Glycol, "
        "Dimethicone, Maris Sal, Sodium Aspartate, Perfume, Disodium EDTA, "
        "Niacinamide, Benzophenone-4, Panthenol, Biotin",
        CDN + "TexturisingStylingSpray50ml_e42d2273-32ea-439f-a4c5-931445f8a549.webp?v=1773663592",
    ),
    (
        "Arata 1% Salicylic Acid Body Wash", "Arata", "Body Care", "1% Salicylic Acid Body Wash", "300 ml",
        "Purified Water, Sodium Laureth Sulfate, Sodium Chloride, Cocamidopropyl Betaine, "
        "Fragrance, Cocamide Diethanolamide, Glycerine, Polyquaternium 7, Salicylic Acid, "
        "Ceteareth-25, Sodium Hydroxide, PEG-150 Distearate, Sodium Gluconate, "
        "Sodium Metabisulfite, Sodium Benzoate, Methylchloroisothiazolinone, "
        "Methylisothiazolinone, CI 17200, CI 14700",
        CDN + "1-salicylic-acid-body-wash-removes-bacne-i-treats-476.webp?v=1749897225&width=1000",
    ),
    (
        "Arata 6.5% AHA BHA Body Lotion", "Arata", "Body Care", "6.5% AHA BHA Exfoliating Body Lotion", "200 ml",
        "Purified Water, Glycolic Acid, Lactic Acid, Cetyl Alcohol, Cyclopentasiloxane, "
        "Glyceryl Monostearate, Propanediol, Stearic Acid, Ethyl Olivate, Sodium Hydroxide, "
        "Cetostearyl Alcohol, Emulsifying Wax, Glycerine, Niacinamide, Fragrance, "
        "Salicylic Acid, Phenoxyethanol, Olive Oil Methyl Ester, Sodium Benzoate, "
        "Potassium Sorbate, Sodium Acrylate/Sodium Acryloyldimethyl Taurate Copolymer, "
        "Polyacrylate-13, Isohexadecane, Oat Meal Extract, Citrus Grandis Fruit Extract, "
        "Sodium Gluconate, Vaccinium Angustifolium Blueberry Fruit Extract, Polyisobutene, "
        "Ethylhexylglycerin, Polysorbate 80, PEG-7 Glyceryl Cocoate, Polysorbate 20, "
        "Sorbitan Oleate, Sorbitan Isostearate, Sodium Hyaluronate, Ceramide NP",
        CDN + "6-5-aha-bha-body-lotion-for-rough-and-textured-skin-598.webp?v=1750945054&width=1000",
    ),
]

# ── insertion ─────────────────────────────────────────────────────────────────

def already_exists(name: str) -> bool:
    res = sb.table('ai_extracted_products').select('id').ilike('name', name).limit(1).execute()
    return bool(res.data)

def insert_product(name, brand, category, variant, net_wt, ingredients_raw, image_url):
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
    print(f"Inserting {len(PRODUCTS)} Arata products (full INCI only)...\n")
    added = skipped = failed = 0
    for p in PRODUCTS:
        r = insert_product(*p)
        if r is True:    added += 1
        elif r is False: skipped += 1
        else:            failed += 1
    print(f"\n{'='*55}")
    print(f"Done.  Added: {added}  |  Skipped: {skipped}  |  Failed: {failed}")
    print(f"{'='*55}")

if __name__ == "__main__":
    main()
