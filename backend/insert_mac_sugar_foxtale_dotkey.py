"""
Insert MAC, SUGAR, Foxtale, and Dot & Key products from Clinical_Cosmetic_Compilation PDF
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = [
    'sodium lauryl sulfate', 'sls', 'sodium laureth sulfate', 'sles',
    'phthalate', 'propylene glycol', 'phenoxyethanol', 'titanium dioxide',
    'alcohol', 'methylparaben', 'propylparaben',
]
_WORTH = ['mineral oil', 'silicone', 'cyclopentasiloxane', 'dimethicone', 'paraffin']

def _classify(name: str) -> str:
    n = name.lower()
    for q in _QUESTIONED:
        if q in n: return 'commonly_questioned'
    for w in _WORTH:
        if w in n: return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'sodium lauryl sulfate' in n or 'sls' in n: return 'Anionic surfactant; can be harsh on skin'
        if 'propylene glycol' in n: return 'Humectant; can cause irritation in sensitive individuals'
        if 'phenoxyethanol' in n: return 'Preservative; safe at regulated concentrations'
        if 'titanium dioxide' in n: return 'Physical UV filter; generally safe'
        return 'Commonly questioned ingredient'
    if cls == 'worth_knowing':
        if 'silicone' in n or 'cyclopentasiloxane' in n or 'dimethicone' in n:
            return 'Silicone conditioning agent; lightweight but non-biodegradable'
        if 'mineral oil' in n: return 'Occlusive moisturizer; derived from petroleum'
        return 'Moderate concern; safe in regulated amounts'
    # generally_recognised
    if 'argan oil' in n: return 'Rich in antioxidants and fatty acids'
    if 'almond oil' in n: return 'Nourishing oil; rich in Vitamin E'
    if 'aloe vera' in n: return 'Soothing and hydrating'
    if 'green tea' in n: return 'Antioxidant-rich botanical'
    if 'hyaluronic acid' in n: return 'Hydrating humectant; draws moisture to skin'
    if 'glycerin' in n: return 'Humectant; draws moisture to skin'
    if 'vitamin e' in n: return 'Antioxidant protection'
    if 'carnauba wax' in n: return 'Natural wax; protective and emollient'
    return 'Generally recognised as safe'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Permitted additive; check local regulations'
    if cls == 'worth_knowing': return 'Permitted ingredient; use as directed'
    return 'Approved under standard cosmetic regulations'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    items = [i.strip() for i in raw.split(',')]
    return [i for i in items if len(i) > 1]

def _build_obj(name: str) -> dict:
    cls = _classify(name)
    return {
        'name': name,
        'aliases': '',
        'classification': cls,
        'one_line_note': _note(name, cls),
        'regulatory_note': _reg_note(cls),
    }

def _score(ingredient_objs: list) -> int:
    score = 100
    for ing in ingredient_objs:
        cls = ing['classification']
        if cls == 'commonly_questioned': score -= 10
        elif cls == 'worth_knowing': score -= 5
    return max(0, min(100, score))

PRODUCTS = [
    # MAC PORTFOLIO
    {"name": "MAC Studio Fix Fluid SPF 15", "brand": "MAC", "category": "Makeup",
     "raw": "Water, Cyclopentasiloxane, PEG-10 Dimethicone, Butylene Glycol, Trimethylsiloxysilicate, Ethylhexyl Methoxycinnamate, Dimethicone, Magnesium Sulfate, Titanium Dioxide, Algae Extract, Tocopheryl Acetate, Sodium Hyaluronate."},
    {"name": "MAC Prep + Prime Fix+", "brand": "MAC", "category": "Makeup",
     "raw": "Water, Glycerin, Butylene Glycol, Cucumber Fruit Extract, Chamomilla Recutita Extract, Camellia Sinensis Leaf Extract, Caffeine, Panthenol, Arginine."},
    {"name": "MAC Strobe Cream", "brand": "MAC", "category": "Skincare",
     "raw": "Water, Cyclopentasiloxane, Glycerin, Pelargonium Graveolens Oil, Green Tea Extract, Grape Fruit Extract, Scutellaria Baicalensis Root Extract, Mulberry Root Extract, Sodium Hyaluronate."},
    {"name": "MAC Matte Lipstick Standard", "brand": "MAC", "category": "Makeup",
     "raw": "Octyldodecanol, Ricinus Communis Seed Oil, Silica, Tricaprylyl Citrate, Ozokerite, Isononyl Isononanoate, Paraffin, Phenyl Trimethicone, Microcrystalline Wax, Carnauba Wax."},

    # SUGAR PORTFOLIO
    {"name": "SUGAR Ace Of Face Foundation Stick", "brand": "SUGAR", "category": "Makeup",
     "raw": "Ethylhexyl Palmitate, Silica, Aluminum Starch Octenylsuccinate, Polyethylene, Phenyl Trimethicone, Caprylic/Capric Triglyceride, Candelilla Wax, Isododecane, Trimethylsiloxysilicate."},
    {"name": "SUGAR Smudge Me Not Liquid Lipstick", "brand": "SUGAR", "category": "Makeup",
     "raw": "Isododecane, Trimethylsiloxysilicate, Cyclopentasiloxane, Mica, Quaternium-18 Bentonite, Hydrogenated Polyisobutene, Vitamin E, Propylene Carbonate."},
    {"name": "SUGAR Aquaholic Priming Moisturizer", "brand": "SUGAR", "category": "Skincare",
     "raw": "Aqua, Cyclopentasiloxane, Dimethicone, Glycerin, Sea Water Extract, Sodium Hyaluronate, Malachite Extract, Aloe Vera Leaf Juice, Phenoxyethanol."},
    {"name": "SUGAR Arch Arrival Brow Definer", "brand": "SUGAR", "category": "Makeup",
     "raw": "Iron Oxides, Hydrogenated Soybean Oil, Hydrogenated Coco-Glycerides, Hydrogenated Vegetable Oil, Zinc Stearate, Carnauba Wax, Stearic Acid."},

    # FOXTALE PORTFOLIO
    {"name": "Foxtale 15% Vitamin C Serum (C For Yourself)", "brand": "Foxtale", "category": "Skincare",
     "raw": "L-Ascorbic Acid (15%), Dicaprylyl Carbonate, C12-15 Alkyl Benzoate, Tocopherol, Ferulic Acid, Ethoxydiglycol, Phenoxyethanol."},
    {"name": "Foxtale Keep Calm Hydrating Serum", "brand": "Foxtale", "category": "Skincare",
     "raw": "Aqua, Sodium Hyaluronate, Panthenol, Glycerin, Red Algae Extract, Betaine, Xylitylglucoside, Ethylhexylglycerin."},
    {"name": "Foxtale Daily Duet Cleanser", "brand": "Foxtale", "category": "Skincare",
     "raw": "Aqua, Sodium Lauroyl Sarcosinate, Cocamidopropyl Betaine, Glycerin, Red Algae Extract, Sodium PCA, Panthenol, Citric Acid."},

    # DOT & KEY PORTFOLIO
    {"name": "Dot & Key Watermelon Cooling Sunscreen SPF 50", "brand": "Dot & Key", "category": "Skincare",
     "raw": "Aqua, Ethylhexyl Methoxycinnamate, Watermelon Fruit Extract, Hyaluronic Acid, Menthyl Lactate, Diethylamino Hydroxybenzoyl Hexyl Benzoate, Titanium Dioxide."},
    {"name": "Dot & Key 72 HR Hydrating Gel + Probiotics", "brand": "Dot & Key", "category": "Skincare",
     "raw": "Aqua, Rice Water, Lactobacillus Ferment Lysate, Hyaluronic Acid, Kombucha Extract, Glycerin, Saccharide Isomerate."},
    {"name": "Dot & Key Cica + Niacinamide Oil-Free Face Gel", "brand": "Dot & Key", "category": "Skincare",
     "raw": "Aqua, Niacinamide, Centella Asiatica Extract, Tea Tree Oil, Aloe Vera Juice, Salicylic Acid, Carbomer."},
]

def insert(p: dict) -> bool:
    name = p['name']
    raw = p['raw']
    parsed = _parse(raw)
    ingredient_objs = [_build_obj(i) for i in parsed]
    score = _score(ingredient_objs)

    try:
        existing = supabase.from_('ai_extracted_products') \
            .select('id').ilike('name', name).limit(1).execute()
        if existing.data:
            print(f"  skip (exists): {name}")
            return False

        supabase.from_('ai_extracted_products').insert({
            'name':            name,
            'brand':           p['brand'],
            'category':        p['category'],
            'image_url':       None,
            'images':          [],
            'awareness_score': score,
            'summary': (
                f"{name} by {p['brand']}. Awareness score: {score}/100. "
                "Not a health assessment or medical advice."
            ),
            'fssai_note':      'Subject to applicable cosmetic regulations.',
            'verdict':         'Clean formulation' if score >= 80 else 'Average formulation',
            'recommendation':  'Suitable for most.' if score >= 80 else 'Review before use.',
            'ingredients':     ingredient_objs,
            'ingredients_raw': raw,
            'status':          'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} MAC, SUGAR, Foxtale, Dot & Key products...")
    inserted = 0
    for p in PRODUCTS:
        if insert(p):
            inserted += 1
        time.sleep(0.1)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
