"""
Add 16 Aravi Organic products to ai_extracted_products.
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

BASE = "https://araviorganic.com/cdn/shop/files/"

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
        return f"{name} by {brand} scores Grade A. All {total} ingredients are generally recognised as safe — clean, natural formula with no synthetic additives."
    elif grade == "B":
        return f"{name} by {brand} scores Grade B. {total} ingredients analysed; {w} worth knowing about, no restricted additives."
    elif grade == "C":
        return f"{name} by {brand} scores Grade C. Contains {w} worth-knowing ingredients (>30% of total). Use with awareness."
    else:
        return f"{name} by {brand} scores Grade D. Contains {q} commonly questioned ingredient(s) flagged by regulatory bodies."

FSSAI_MAP = {
    "Hair Care": "Hair care products regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
    "Body Care": "Cosmetics regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
    "Sun Care":  "Sunscreen products regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
    "Lip Care":  "Lip care products regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
}

# ── catalogue ─────────────────────────────────────────────────────────────────

PRODUCTS = [
    # ── HAIR CARE ──
    (
        "Aravi Organic Rosemary Anti Hair Fall Shampoo",
        "Aravi Organic", "Hair Care",
        "Aqua, Lauryl Glucoside, Cocoyl Glucoside, Sodium Lauroyl Sarcosinate, "
        "Cocamidopropyl Betaine, Guar Hydroxypropyltrimonium Chloride, Polyquaternium-10, "
        "Caffeine Extract, Rosmarinus Officinalis Leaf Oil, "
        "Aloe Barbadensis Leaf Extract, Murraya Koenigii Leaf Extract, "
        "Camellia Sinensis Leaf Extract, Phyllanthus Emblica Fruit Extract, "
        "Trigonella Foenum-Graecum Seed Extract, Zingiber Officinale Root Extract, "
        "Hibiscus Sabdariffa Flower Extract, Sapindus Mukorossi Fruit Extract, "
        "Ocimum Basilicum Leaf Oil, Azadirachta Indica Seed Oil, "
        "Sodium Gluconate, Phenoxyethanol, Ethylhexylglycerin",
        BASE + "RS_200ml.jpg?v=1769589827",
    ),
    (
        "Aravi Organic Rosemary Conditioner",
        "Aravi Organic", "Hair Care",
        "Aqua, Behentrimonium Methosulfate, Guar Hydroxypropyltrimonium Chloride, "
        "Stearamidopropyl Dimethylamine, Cetrimonium Chloride, "
        "Prunus Amygdalus Dulcis Oil, Cetostearyl Alcohol, Cetyl Alcohol, "
        "Glycerine, DL-Panthenol, Propylene Glycol, Dimethicone, "
        "Cyclopentasiloxane, Phyllanthus Emblica Fruit Extract, "
        "Aloe Barbadensis Leaf Extract, Rosmarinus Officinalis Leaf Extract, "
        "Jasminum Officinale Flower Extract, Disodium EDTA, "
        "Phenoxyethanol, Ethylhexyl Glycerine",
        "https://cdn.shopify.com/s/files/1/0675/5732/7164/files/Rosemary_sampoo_edb3cd14-851b-4e3a-8a59-ff27ceb2bf78.jpg?v=1753191078",
    ),
    (
        "Aravi Organic Multi-Peptide Shampoo",
        "Aravi Organic", "Hair Care",
        "Aqua, Sodium Cocoyl Isethionate, Decyl Glucoside, Sodium Cocoyl Glycinate, "
        "Sodium Lauroyl Sarcosinate, Cocamidopropyl Betaine, "
        "Sodium C14-16 Olefin Sulfonate, Peg-7 Glyceryl Cocoate, "
        "Acetyl Tripeptide-3, Copper Tripeptide-1, Palmitoyl Oligopeptide, Oligopeptide-2, "
        "Pilocarpus Jaborandi Leaf Extract, Arnica Montana Flower Extract, "
        "Bacopa Monnieri Leaf Extract, Ginkgo Biloba Leaf Extract, "
        "Hydrolyzed Wheat Protein, Hydrolyzed Soy Protein, Hydrolyzed Corn Protein, "
        "Amodimethicone (and) Trideceth-12 (and) Cetrimonium Chloride, "
        "Propylene Glycol, Lactic Acid, Sodium Gluconate, "
        "Phenoxyethanol, Ethylhexyl Glycerine",
        BASE + "Multi-Peptide_Shampoo.jpg?v=1739959635",
    ),
    (
        "Aravi Organic Multi-Peptide Conditioner",
        "Aravi Organic", "Hair Care",
        "Aqua, Behentrimonium Methosulfate, Guar Hydroxypropyltrimonium Chloride, "
        "Stearamidopropyl Dimethylamine, Cetrimonium Chloride, "
        "Butyrospermum Parkii Butter, Astrocaryum Murumuru Seed Butter, "
        "Prunus Amygdalus Dulcis Oil, Cetostearyl Alcohol, Cetyl Alcohol, "
        "Glycerine, DL-Panthenol, Quaternium-18, "
        "Acetyl Tripeptide-3, Copper Tripeptide-1, Palmitoyl Oligopeptide, Oligopeptide-2, "
        "Hydrolyzed Wheat Protein, Hydrolyzed Soy Protein, Hydrolyzed Corn Protein, "
        "Dimethicone, Cyclopentasiloxane, "
        "Phyllanthus Emblica Fruit Extract, Rosmarinus Officinalis Leaf Extract, "
        "Aloe Barbadensis Leaf Extract, Jasminum Officinale Flower Extract, "
        "Disodium EDTA, Phenoxyethanol, Ethylhexyl Glycerine",
        BASE + "Multi-peptide_conditioner.jpg?v=1749874680",
    ),
    (
        "Aravi Organic Advanced Hair Growth Serum",
        "Aravi Organic", "Hair Care",
        "Aqua, Aloe Barbadensis Leaf Extract, Phyllanthus Emblica Fruit Extract, "
        "Redensyl (Dihydroquercetin-Glucoside, EGCG2), "
        "Anagain (Pisum Sativum Shoot Extract), "
        "Procapil (Biotinyl-GHK, Apigenin, Oleanolic Acid), "
        "Caffeine, Biotin, Coffea Arabica Seed Extract, "
        "Eclipta Prostrata Leaf Extract, Onion Extract, "
        "Acacia Concinna Pod Extract, Hydrolyzed Collagen Peptide, "
        "DL-Panthenol, Hydroxyethyl Cellulose, Polyquaternium-39, "
        "Refined Glycerine, Polysorbate 20, "
        "Sodium Benzoate, Potassium Sorbate, Sodium Gluconate",
        BASE + "Artboard_5.png?v=1753196802",
    ),
    (
        "Aravi Organic Rosemary Water Hair Spray",
        "Aravi Organic", "Hair Care",
        "Aqua, Rosmarinus Officinalis Leaf Extract, Rosmarinus Officinalis Flower Oil, "
        "1,3-Propanediol, Glycerin, DL-Panthenol, "
        "Aloe Barbadensis Leaf Extract, Oryza Sativa (Rice Water)",
        BASE + "Rosemary_water_spry.jpg?v=1739959404",
    ),
    (
        "Aravi Organic Batana Hair Oil",
        "Aravi Organic", "Hair Care",
        "Elaeis Oleifera Fruit Oil (Batana Oil), Nigella Sativa Seed Oil, "
        "Cucurbita Pepo Seed Oil, Simmondsia Chinensis Seed Oil, "
        "Sesamum Indicum Seed Oil, Cocos Nucifera Oil, "
        "Prunus Amygdalus Dulcis Oil, Olea Europaea Fruit Oil, "
        "Ricinus Communis Seed Oil",
        BASE + "Batana_1x1_cc2dbbbb-8029-4386-be49-0254e87fdc32.jpg?v=1753176901",
    ),
    (
        "Aravi Organic Rosemary Hair Growth Oil with Lavender",
        "Aravi Organic", "Hair Care",
        "Rosmarinus Officinalis Leaf Oil, Lavandula Angustifolia Flower Oil, "
        "Melaleuca Alternifolia Leaf Oil, Cocos Nucifera Oil, "
        "Prunus Amygdalus Dulcis Oil, Nigella Sativa Seed Oil, "
        "Sesamum Indicum Seed Oil, Ricinus Communis Seed Oil, "
        "Helianthus Annuus Seed Oil, Glycine Max Seed Oil, "
        "Olea Europaea Fruit Oil, Simmondsia Chinensis Seed Oil, "
        "Argania Spinosa Kernel Oil, Cinnamomum Camphora Bark Oil, "
        "Eucalyptus Globulus Leaf Oil, Ocimum Basilicum Leaf Oil",
        BASE + "Artboard_28.jpg?v=1753162263",
    ),
    (
        "Aravi Organic Pure Cold-Pressed Castor Hair Oil",
        "Aravi Organic", "Hair Care",
        "Ricinus Communis (Cold-Pressed Castor Oil) 100%",
        BASE + "Artboard_26.jpg?v=1753161218",
    ),
    # ── SUN CARE ──
    (
        "Aravi Organic Oil-Free Sunscreen Body Lotion SPF 50 PA++++",
        "Aravi Organic", "Sun Care",
        "Aqua, Ethylhexyl Methoxycinnamate, Butyl Methoxydibenzoylmethane, "
        "Zinc Oxide, Titanium Dioxide, Sodium Hyaluronate, Niacinamide, "
        "Ceramide NP, Copper Tripeptide-1, Carica Papaya Fruit Extract, "
        "Glycyrrhiza Glabra Root Extract, Curcuma Longa Root Extract, "
        "Rosmarinus Officinalis Leaf Extract, Allantoin, Squalene, Glycerine, "
        "Cetostearyl Alcohol, Stearic Acid, Caprylic/Capric Triglyceride, "
        "Polyacrylamide, Isopropyl Myristate, Carbomer, Triethanolamine, "
        "Tocopheryl Acetate, Disodium EDTA, "
        "Phenoxyethanol, Ethylhexylglycerin",
        BASE + "Sunscreen_2ce055da-9f43-4cca-ad4d-2d31841bd3ea.jpg?v=1739959611",
    ),
    (
        "Aravi Organic Classic Sunscreen Body Lotion SPF 50",
        "Aravi Organic", "Sun Care",
        "Aqua, Titanium Dioxide, Ethylhexyl Methoxycinnamate, "
        "Butyl Methoxydibenzoylmethane, Benzophenone-3, "
        "Niacinamide, Camellia Sinensis Leaf Extract, Pyrus Malus Fruit Extract, "
        "Cetostearyl Alcohol, Stearic Acid, Glyceryl Monostearate, "
        "Cyclopentasiloxane, Dimethicone, Isopropyl Myristate, "
        "BHT, Glycerine, Prunus Amygdalus Dulcis Oil, Tocopherol, "
        "Carbomer, Triethanolamine, Disodium EDTA, "
        "Phenoxyethanol, Ethylhexyl Glycerine",
        BASE + "Sunscreen_2ce055da-9f43-4cca-ad4d-2d31841bd3ea.jpg?v=1739959611",
    ),
    # ── BODY CARE ──
    (
        "Aravi Organic 10% AHA 1% BHA Exfoliating Body Lotion",
        "Aravi Organic", "Body Care",
        "Aqua, Sodium Gluconate, Glycerin, Salicylic Acid, "
        "Glycolic Acid, Lactic Acid, Niacinamide, Ceramide NP, "
        "Vaccinium Angustifolium Fruit Extract, Carica Papaya Fruit Extract, "
        "Ananas Sativus Fruit Extract, Butyrospermum Parkii Butter, "
        "Simmondsia Chinensis Seed Oil, Caprylic/Capric Triglyceride, "
        "Tocopherol, Cetostearyl Alcohol, Stearic Acid, Glyceryl Monostearate, "
        "PEG-100 Stearate, BHT, Isopropyl Myristate, Carbomer, "
        "Triethanolamine, Parfum, Disodium EDTA, "
        "Phenoxyethanol, Ethylhexylglycerin",
        BASE + "AHA_-_BHA.jpg?v=1739959243",
    ),
    (
        "Aravi Organic Advanced Barrier Repair Moisturiser",
        "Aravi Organic", "Body Care",
        "Aqua, Cocos Nucifera Oil, Prunus Amygdalus Dulcis Oil, Squalane, "
        "Coffea Arabica Seed Oil, Butyrospermum Parkii Butter, "
        "DL-Panthenol, Niacinamide, Ceramide-1, Ceramide-2, Ceramide-3, Ceramide-6, "
        "Copper Tripeptide-1, Glyceryl Glucoside, "
        "Oryza Sativa Bran Extract, Avena Sativa Kernel Extract, "
        "Centella Asiatica Extract, Glycyrrhiza Glabra Root Extract, "
        "Arctostaphylos Uva Ursi Leaf Extract, "
        "Cucumis Sativus Fruit Extract, Citrus Sinensis Peel Extract, "
        "Allantoin, Glycerine, Cetostearyl Alcohol, Stearic Acid, "
        "Caprylic/Capric Triglyceride, Cyclopentasiloxane, Dimethicone, "
        "Polysorbate 20, Carbomer, Triethanolamine, Disodium EDTA, "
        "Phenoxyethanol",
        BASE + "Artboard_5.png?v=1753196802",
    ),
    # ── LIP CARE ──
    (
        "Aravi Organic Beetroot Tinted Lip Balm SPF 50 PA+++",
        "Aravi Organic", "Lip Care",
        "Ricinus Communis Seed Oil, Butyrospermum Parkii Butter, "
        "Ceramide NP, Palmitoyl Oligopeptide, Kojic Acid, Tocopherol, "
        "Caprylic/Capric Triglyceride, Paraffin, Cera Alba, Ozokerite, "
        "Carnauba Wax, Microcrystalline Wax, Candelilla Wax, Polyisobutene, "
        "Octocrylene, Butyl Methoxydibenzoylmethane, Zinc Oxide, "
        "Helianthus Annuus Seed Oil, Beta Vulgaris Root Extract",
        BASE + "TLB.jpg?v=1773990037",
    ),
    (
        "Aravi Organic Lip Glowy Balm SPF 50 PA+++",
        "Aravi Organic", "Lip Care",
        "Ricinus Communis Seed Oil, Helianthus Annuus Seed Oil, "
        "Butyrospermum Parkii Butter, Caprylic/Capric Triglyceride, "
        "Ozokerite, Microcrystalline Wax, Carnauba Wax, Candelilla Wax, "
        "Polyisobutene, Ethylhexyl Methoxycinnamate, Octocrylene, "
        "Butyl Methoxydibenzoylmethane, Zinc Oxide, "
        "Kojic Acid, Palmitoyl Oligopeptide, Ceramide NP, Tocopherol",
        BASE + "NonTeented.jpg?v=1739959216",
    ),
    (
        "Aravi Organic Beetroot Lip Scrub",
        "Aravi Organic", "Lip Care",
        "Cocos Nucifera Oil, Saccharum Officinarum (Brown Sugar), "
        "Beta Vulgaris Root Oil, Tocopheryl Acetate, Helianthus Annuus Seed Oil, "
        "Persea Gratissima Oil, Butyrospermum Parkii Butter, Cera Alba, "
        "Theobroma Cacao Seed Butter, Simmondsia Chinensis Seed Oil, "
        "Olea Europaea Fruit Oil, Prunus Amygdalus Dulcis Oil, "
        "Isopropyl Myristate, Argania Spinosa Kernel Oil",
        BASE + "Beetroot_Lip_Scrub.jpg?v=1741322453",
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
               "All ingredients are generally recognised as safe — clean formula.")
    recommendation = ("Avoid or use sparingly — contains commonly questioned ingredients." if q else
                      "Use with awareness — contains synthetic ingredients worth knowing about." if w else
                      "Safe to use — clean formula with no concerning additives.")
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
    print(f"Inserting {len(PRODUCTS)} Aravi Organic products...\n")
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
