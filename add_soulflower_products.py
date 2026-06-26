"""
Add 30 Soulflower products to ai_extracted_products.
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

CDN = "https://www.soulflower.in/cdn/shop/files/"

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
    "Haircare":     "Hair care products regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
    "Skincare":     "Cosmetics regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
    "Soap":         "Soaps regulated under Cosmetics Rules 2020 in India.",
    "Essential Oil":"Essential oils sold as cosmetics regulated under Cosmetics Rules 2020. Must be diluted before skin use.",
    "Carrier Oil":  "Carrier oils regulated under Cosmetics Rules 2020. For external use only.",
    "Face Mask":    "Cosmetic face mask regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
}

# ── catalogue ─────────────────────────────────────────────────────────────────

PRODUCTS = [
    # ── CARRIER OILS ──
    (
        "Soulflower 100% Pure Castor Oil",
        "Soulflower", "Carrier Oil",
        "Ricinus Communis Seed Oil",
        CDN + "Castor-oil.webp?v=1775568186",
    ),
    (
        "Soulflower 100% Pure Olive Oil",
        "Soulflower", "Carrier Oil",
        "Olea Europaea Fruit Oil",
        CDN + "bcnrlvbbgbgnpkg8wnve.webp?v=1775631822",
    ),
    (
        "Soulflower 100% Pure Moroccan Argan Oil",
        "Soulflower", "Carrier Oil",
        "Argania Spinosa Kernel Oil",
        CDN + "Argan-09.webp?v=1780126446",
    ),
    (
        "Soulflower Jojoba Oil",
        "Soulflower", "Carrier Oil",
        "Simmondsia Chinensis Seed Oil",
        CDN + "Jojoba-09.webp?v=1780126446",
    ),
    (
        "Soulflower Rosehip Oil",
        "Soulflower", "Carrier Oil",
        "Rosa Canina Seed Oil",
        CDN + "Rosehip-7.webp?v=1775568448",
    ),
    (
        "Soulflower 100% Pure Sesame Oil",
        "Soulflower", "Carrier Oil",
        "Sesamum Indicum Seed Oil",
        CDN + "aqcd68omrsdqbzhucyvd.webp?v=1773135416",
    ),
    (
        "Soulflower Pure Avocado Oil",
        "Soulflower", "Carrier Oil",
        "Persea Gratissima Oil",
        CDN + "Avocado_Oil_For_Hair_Skin_8.webp?v=1780126446",
    ),
    (
        "Soulflower Grapeseed Oil",
        "Soulflower", "Carrier Oil",
        "Vitis Vinifera Seed Oil",
        CDN + "Grapeseesd-8.webp?v=1775568374",
    ),
    # ── HAIR OIL BLENDS ──
    (
        "Soulflower Bhringraj Hair Growth Oil",
        "Soulflower", "Haircare",
        "Cocos Nucifera Oil, Eclipta Prostrata Extract, Sesamum Indicum Oil, "
        "Phyllanthus Emblica Extract, Azadirachta Indica Extract, "
        "Bacopa Monnieri Extract, Murraya Koenigii Extract",
        CDN + "bhringraj-hair-oil-main.webp?v=1780126387",
    ),
    (
        "Soulflower Tea Tree Anti Dandruff Scalp Oil",
        "Soulflower", "Haircare",
        "Oryza Sativa Bran Oil, Ricinus Communis Seed Oil, Sesamum Indicum Oil, "
        "Olea Europaea Fruit Oil, Melaleuca Alternifolia Leaf Oil, "
        "Simmondsia Chinensis Seed Oil, Tocopherol",
        CDN + "Tea-tree-oil-3_03e36bfd-3a80-4402-abfe-a8498aa0eaea.webp?v=1775569066",
    ),
    (
        "Soulflower Rosemary Mint Light Hair Growth Oil",
        "Soulflower", "Haircare",
        "Oryza Sativa Bran Oil, Helianthus Annuus Seed Oil, Rosmarinus Officinalis Oil, "
        "Nigella Sativa Seed Oil, Phyllanthus Emblica Oil, Ricinus Communis Seed Oil, "
        "Vitis Vinifera Seed Oil, Argania Spinosa Kernel Oil, Persea Gratissima Oil, "
        "Mentha Piperita Oil, Mentha Spicata Oil, Hibiscus Rosa-Sinensis Oil, Tocopherol",
        CDN + "Rosemary-mint-2.webp?v=1776517273",
    ),
    (
        "Soulflower Rosemary Lavender Baby Hair Growth Oil",
        "Soulflower", "Haircare",
        "Cocos Nucifera Oil, Olea Europaea Fruit Oil, Sesamum Indicum Oil, "
        "Oryza Sativa Bran Oil, Prunus Dulcis Oil, Ricinus Communis Seed Oil, "
        "Rosmarinus Officinalis Oil, Phyllanthus Emblica Oil, "
        "Simmondsia Chinensis Seed Oil, Persea Gratissima Oil, "
        "Argania Spinosa Kernel Oil, Lavandula Angustifolia Oil",
        CDN + "Baby-hair-oil_3_9b9dbe5b-f880-4f06-a7e9-7aa68d863d2a.jpg?v=1773127742",
    ),
    (
        "Soulflower Onion Amla Hair Growth Oil",
        "Soulflower", "Haircare",
        "Cocos Nucifera Oil, Sesamum Indicum Oil, Olea Europaea Oil, "
        "Ricinus Communis Oil, Allium Cepa Oil, Vetiveria Zizanioides Root Oil, "
        "Vitis Vinifera Seed Oil, Citrus Sinensis Peel Oil, Santalum Album Oil, "
        "Alkanna Tinctoria Extract, Argania Spinosa Kernel Oil, Prunus Dulcis Oil, "
        "Azadirachta Indica Oil, Phyllanthus Emblica Oil, Bacopa Monnieri Oil, "
        "Hibiscus Rosa-Sinensis Oil, Moringa Oleifera Seed Oil, "
        "Calophyllum Inophyllum Seed Oil, Pelargonium Graveolens Oil, "
        "Lawsonia Inermis Oil, Withania Somnifera Oil, "
        "Gaultheria Procumbens Oil, Cedrus Deodara Oil, "
        "Mentha Piperita Oil, Tocopherol",
        CDN + "onion-hair-oil-12ml.webp?v=1780126386",
    ),
    # ── HAIR SERUM & SPRAY ──
    (
        "Soulflower Rosemary Redensyl Hair Serum",
        "Soulflower", "Haircare",
        "Aqua, Pisum Sativum Sprout Extract, Phenoxyethanol, Sodium Benzoate, "
        "Glycerin, Sodium Metabisulfite, Larix Europaea Wood Extract, "
        "Glycine, Zinc Chloride, Camellia Sinensis Leaf Extract, "
        "Oryza Sativa Water Extract, Xylitylglucoside, Anhydroxylitol, "
        "Maltitol, Xylitol, Pelvetia Canaliculata Extract, "
        "PEG-40 Hydrogenated Castor Oil, Salvia Hispanica Seed Extract, "
        "Citrus Reticulata Extract, Acetyl Tyrosine, Pentylene Glycol, "
        "Gluconolactone, Rosmarinus Officinalis Oil, Euxyl K 712, "
        "Xanthan Gum, Propanediol, Caffeine, Hydrolysed Keratin, "
        "Sodium Gluconate, Biotin, Allantoin, Melaleuca Alternifolia Oil",
        CDN + "Redesyl-serum_1fd40ad2-0f14-467b-9304-b96cd09b88e2.webp?v=1775654405",
    ),
    (
        "Soulflower Rosemary Hair Spray Strength Boost",
        "Soulflower", "Haircare",
        "Rosmarinus Officinalis Hydrosol, Niacinamide, Rosmarinus Officinalis Oil, "
        "Panthenol, Heptyl Glucoside, Betaine, Phenoxyethanol, Sodium Benzoate, "
        "Mentha Piperita Oil, Allantoin, Disodium EDTA, Sodium Gluconate",
        CDN + "200ml_Rosemary_water_1_97933dec-1647-4ee3-a9c3-7dab10f597ce.webp?v=1775810856",
    ),
    # ── SHAMPOO ──
    (
        "Soulflower Rosemary Tea Tree Shampoo",
        "Soulflower", "Haircare",
        "Aqua, Sodium Cocoyl Isethionate, Phyllanthus Emblica Extract, "
        "Lauryl Glucoside, Cocoyl Glucoside, Aloe Barbadensis Extract, "
        "Vegetable Glycerin, Salicylic Acid, Hibiscus Rosa-Sinensis Extract, "
        "Sapindus Mukorossi Extract, Ethylene Glycol Distearate, "
        "Salix Alba Extract, Polyquaternium-37, Ginkgo Biloba Extract, "
        "Cocos Nucifera Milk, Niacinamide, Panthenol, Hydrolysed Soya Protein, "
        "Sodium Benzoate, Potassium Sorbate, Fragrance, "
        "Rosmarinus Officinalis Oil, Hyaluronic Acid, "
        "Melaleuca Alternifolia Oil, Guar Hydroxypropyl Trimonium Chloride, "
        "Tocopherol",
        CDN + "Rosemary-tea-tree-shampoo-2.webp?v=1775810434",
    ),
    # ── ESSENTIAL OILS ──
    (
        "Soulflower 100% Pure Rosemary Essential Oil",
        "Soulflower", "Essential Oil",
        "Rosmarinus Officinalis Essential Oil",
        CDN + "Essential-oil-pack-1_5c2093b6-2913-4fad-9c7e-9ed64788cede.webp?v=1780565448",
    ),
    (
        "Soulflower Lavender Essential Oil",
        "Soulflower", "Essential Oil",
        "Lavandula Angustifolia Essential Oil",
        CDN + "LavenderEssentialOil.webp?v=1780126446",
    ),
    (
        "Soulflower Peppermint Essential Oil",
        "Soulflower", "Essential Oil",
        "Mentha Piperita Essential Oil",
        CDN + "Peppermint.webp?v=1780126446",
    ),
    (
        "Soulflower Tea Tree Essential Oil",
        "Soulflower", "Essential Oil",
        "Melaleuca Alternifolia Essential Oil",
        CDN + "Tea-tree-oil-10_4edf7708-26ed-4709-adbe-11e8a978af00.webp?v=1775569066",
    ),
    (
        "Soulflower Eucalyptus Essential Oil",
        "Soulflower", "Essential Oil",
        "Eucalyptus Globulus Leaf Oil",
        CDN + "Eucalyptus15ml_8.webp?v=1780126445",
    ),
    (
        "Soulflower Frankincense Essential Oil",
        "Soulflower", "Essential Oil",
        "Boswellia Carterii Essential Oil",
        CDN + "Frankincense.webp?v=1780126445",
    ),
    # ── SKINCARE ──
    (
        "Soulflower Pure Kumkumadi Oil",
        "Soulflower", "Skincare",
        "Prunus Amygdalus Dulcis Seed Oil, Pterocarpus Santalinus Heartwood Extract, "
        "Rubia Cordifolia Stem Extract, Glycyrrhiza Glabra Root Extract, "
        "Berberis Aristata Stem Bark Extract, Vetiveria Zizanioides Root Extract, "
        "Prunus Cerasus Fruit Extract, Nymphaea Caerulea Flower Extract, "
        "Ficus Benghalensis Root Extract, Ficus Lacor Stem Bark Extract, "
        "Nelumbo Nucifera Flower Extract, Aegle Marmelos Fruit Extract, "
        "Clerodendrum Phlomidis Root Extract, Calendula Officinalis Flower Extract, "
        "Gmelina Arborea Root Extract, Chamomilla Recutita Flower Extract, "
        "Desmodium Gangeticum Root Extract, Althaea Officinalis Root Extract, "
        "Tribulus Terrestris Fruit Extract, Solanum Nigrum Root Extract, "
        "Solanum Xanthocarpum Root Extract, Madhuca Longifolia Seed Extract, "
        "Crocus Sativus Stigma Extract, Crocus Sativus Oil, "
        "Sesamum Indicum Seed Oil, Caprae Lac",
        CDN + "kumkumadi_30ml-08.webp?v=1780126386",
    ),
    (
        "Soulflower Deep Pores Cleansing Brightening Ubtan Face Mask",
        "Soulflower", "Face Mask",
        "Solum Fullonum, Citrus Aurantium Peel Powder, Santalum Album Powder, "
        "Carica Papaya Fruit Powder, Ascorbic Acid, Rubia Cordifolia Powder, "
        "Punica Granatum Peel Powder, Glycyrrhiza Glabra Root Powder, "
        "Curcuma Amada Powder, Citrus Aurantium Essential Oil",
        CDN + "UbtanFaceMaskforCleansing_Brightening.webp?v=1780126266",
    ),
    # ── SOAPS ──
    (
        "Soulflower Glycolic Acid Exfoliating Acne Zits Soap",
        "Soulflower", "Soap",
        "Aqua, Cocos Nucifera Oil, Sodium Palmate, Ricinus Communis Seed Oil, "
        "Kaolin, Olea Europaea Fruit Oil, Salicylic Acid, "
        "Ocimum Basilicum Leaf Extract, Melaleuca Alternifolia Leaf Oil, "
        "Glycolic Acid, Niacinamide, Tocopherol",
        CDN + "Acne-soap.webp?v=1780667116",
    ),
    (
        "Soulflower Niacinamide Mango Matcha Vitamin C Soap",
        "Soulflower", "Soap",
        "Elaeis Guineensis Oil, Sodium Palmate, Cocos Nucifera Oil, "
        "Mangifera Indica Extract, Aqua, Sodium Hydroxide, "
        "Ricinus Communis Oil, Olea Europaea Oil, Mangifera Indica Butter, "
        "Fragrance, Niacinamide, Ascorbic Acid, Camellia Sinensis Leaf Powder, "
        "Tocopherol, CI 15510, CI 61565, Curcuma Longa Powder",
        CDN + "Mango_Matcha_Soap_Ingredients.webp?v=1780224247",
    ),
    (
        "Soulflower Kojic Acid Anti Pigmentation Kumkumadi Soap",
        "Soulflower", "Soap",
        "Crocus Sativus Extract, Curcuma Longa, Kojic Acid, Glutathione, "
        "Niacinamide, Elaeis Guineensis Oil, Aqua, Cocos Nucifera Oil, "
        "Sodium Palmate, Sodium Hydroxide, Ricinus Communis Oil, Kaolin, "
        "Fragrance, Olea Europaea Oil, Prunus Dulcis Oil, Tocopherol",
        CDN + "3_9360188f-5475-4294-9100-c1830773ce14.webp?v=1775121684",
    ),
    (
        "Soulflower Niacinamide Rice Water Soap",
        "Soulflower", "Soap",
        "Elaeis Guineensis Oil, Cocos Nucifera Oil, Sodium Palmate, Aqua, "
        "Sodium Hydroxide, Oryza Sativa Water, Ricinus Communis Oil, "
        "Kaolin, Fragrance, Olea Europaea Oil, Alpha Arbutin, "
        "Niacinamide, Argania Spinosa Kernel Oil, Tocopherol",
        CDN + "4_89fd827c-a40e-4cf2-9349-9f6c380cb7f4.webp?v=1775132681",
    ),
    (
        "Soulflower Gentle Calming Moisturizing Lavender Soap",
        "Soulflower", "Soap",
        "Elaeis Guineensis Oil, Cocos Nucifera Oil, Sodium Palmate, "
        "Sodium Hydroxide, Ricinus Communis Oil, Olea Europaea Oil, "
        "Lavandula Angustifolia Essential Oil, Lavandula Angustifolia Herb, "
        "CI 61565, Tocopherol",
        CDN + "Gentle-Calming-Moisturizing-Lavender-Soap.webp?v=1780126085",
    ),
    (
        "Soulflower Activated Charcoal Soap for Pollution Protection",
        "Soulflower", "Soap",
        "Elaeis Guineensis Oil, Cocos Nucifera Oil, Sodium Palmate, "
        "Sodium Hydroxide, Ricinus Communis Oil, Brassica Napus Root Extract, "
        "Olea Europaea Oil, Mentha Piperita Essential Oil, "
        "Melaleuca Alternifolia Leaf Oil, Styrax Benzoin Oil, "
        "Activated Charcoal, Tocopherol",
        CDN + "Activated-Charcoal-Soap-for-clogged-pores.webp?v=1780126085",
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
    print(f"Inserting {len(PRODUCTS)} Soulflower products...\n")
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
