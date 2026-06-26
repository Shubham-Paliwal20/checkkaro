"""
Insert expanded Foxtale & Dot & Key clinical skincare products from Foxtale_DotKey_Clinical_Database PDF
Advanced active ingredients including vitamin C, retinol, ceramides, cica, and probiotics
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = [
    'retinol', 'salicylic acid', 'azelaic acid', 'benzoyl peroxide',
]
_WORTH = [
    'phenoxyethanol', 'ethylhexylglycerin', 'carbomer', 'methylisothiazolinone',
    'butyl methoxydibenzoylmethane', 'ethylhexyl methoxycinnamate', 'benzophenone',
]

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
        if 'retinol' in n: return 'Vitamin A derivative; potent; may cause irritation and photosensitivity'
        if 'salicylic acid' in n: return 'Beta-hydroxy acid; exfoliant; can irritate sensitive skin'
        if 'azelaic acid' in n: return 'Anti-inflammatory acid; generally safe but may irritate'
        if 'benzoyl peroxide' in n: return 'Acne treatment; may cause dryness and sensitivity'
        return 'Active ingredient; requires careful use'
    if cls == 'worth_knowing':
        if 'phenoxyethanol' in n: return 'Preservative; safe at regulated levels'
        if 'ethylhexylglycerin' in n: return 'Humectant preservative; safe'
        if 'carbomer' in n: return 'Thickening agent; safe'
        if 'methoxycinnamate' in n or 'methoxydibenzoylmethane' in n: return 'UV filter; safe sunscreen ingredient'
        if 'benzophenone' in n: return 'UV filter; chemical sunscreen'
        return 'Moderate concern; safe in regulated amounts'
    # generally_recognised
    if 'vitamin c' in n or 'ascorbic acid' in n: return 'Antioxidant; brightening and protective'
    if 'hyaluronic acid' in n: return 'Humectant; hydrating and plumping'
    if 'niacinamide' in n or 'vitamin b3' in n: return 'Vitamin B3; skin-balancing and strengthening'
    if 'ceramide' in n: return 'Lipid barrier; protective and restoring'
    if 'centella asiatica' in n or 'cica' in n: return 'Soothing and protective botanical'
    if 'panthenol' in n or 'pro-vitamin b5' in n: return 'Moisturizing and soothing'
    if 'glycerin' in n: return 'Humectant; hydrating'
    if 'aloe vera' in n: return 'Soothing and hydrating botanical'
    if 'cucumber' in n: return 'Soothing and cooling botanical'
    if 'ferulic acid' in n: return 'Antioxidant; enhances vitamin C'
    if 'vitamin e' in n or 'tocopherol' in n: return 'Antioxidant protection'
    if 'tea tree oil' in n: return 'Antibacterial botanical oil'
    if 'peptide' in n: return 'Protein fragment; firming properties'
    if 'caffeine' in n: return 'Stimulating; anti-puffiness'
    if 'probiotics' in n or 'lactobacillus' in n: return 'Beneficial bacteria; barrier support'
    if 'marula oil' in n: return 'Nourishing botanical oil'
    if 'pomegranate' in n: return 'Antioxidant-rich botanical'
    if 'rice water' in n or 'rice bran' in n: return 'Soothing botanical; brightening'
    if 'shea butter' in n: return 'Nourishing natural butter'
    if 'olive oil' in n: return 'Rich natural oil; antioxidant'
    if 'blood orange' in n: return 'Natural botanical; antioxidant'
    if 'alpha arbutin' in n: return 'Brightening ingredient; safe alternative to hydroquinone'
    if 'tranexamic acid' in n: return 'Skin-brightening ingredient'
    if 'licorice' in n or 'licorice root' in n: return 'Soothing and brightening botanical'
    if 'kombucha' in n: return 'Fermented botanical; probiotic'
    if 'kakadu plum' in n: return 'Antioxidant-rich botanical; vitamin C source'
    return 'Cosmetic ingredient; safe for topical use'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Active ingredient; use as directed; not for sensitive skin'
    if cls == 'worth_knowing': return 'Permitted ingredient; safe at regulated levels'
    return 'Approved cosmetic ingredient'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    items = [i.strip() for i in raw.split(',')]
    return [i for i in items if len(i) > 2]

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
        elif cls == 'worth_knowing': score -= 2
    return max(0, min(100, score))

PRODUCTS = [
    # FOXTALE ACTIVE RANGE
    {"name": "Foxtale C For Yourself Vitamin C Serum", "brand": "Foxtale", "category": "Personal Care",
     "raw": "L-Ascorbic Acid (15%), Dicaprylyl Carbonate, C12-15 Alkyl Benzoate, Vitamin E (Tocopherol), Ferulic Acid, Ethoxydiglycol, Phenoxyethanol."},

    {"name": "Foxtale Keep Calm Hydrating Serum", "brand": "Foxtale", "category": "Personal Care",
     "raw": "Aqua, Sodium Hyaluronate (6 types), Panthenol (Pro-Vitamin B5), Glycerin, Red Algae Extract, Betaine, Xylitylglucoside, Ethylhexylglycerin."},

    {"name": "Foxtale The Daily Duet Cleanser", "brand": "Foxtale", "category": "Personal Care",
     "raw": "Aqua, Sodium Lauroyl Sarcosinate, Cocamidopropyl Betaine, Glycerin, Red Algae Extract, Sodium PCA, Panthenol, Citric Acid, Phenoxyethanol."},

    {"name": "Foxtale CoverUp Dewy Sunscreen SPF 50", "brand": "Foxtale", "category": "Personal Care",
     "raw": "Aqua, Ethylhexyl Methoxycinnamate, Butyl Methoxydibenzoylmethane, Benzophenone-3, Niacinamide, Vitamin E, Phospholipids, Glycerin."},

    {"name": "Foxtale Retinol Night Serum", "brand": "Foxtale", "category": "Personal Care",
     "raw": "Aqua, Caprylic/Capric Triglyceride, Retinol (0.15%), Betaine, Sodium Hyaluronate, Allantoin, Vitamin E, Palmitoyl Tripeptide-1, Phenoxyethanol."},

    {"name": "Foxtale Ceramide Supercream", "brand": "Foxtale", "category": "Personal Care",
     "raw": "Aqua, Ceramide NP, Ceramide AP, Ceramide EOP, Phytosphingosine, Cholesterol, Sodium Lauroyl Lactylate, Glycerin, Shea Butter, Olive Oil."},

    {"name": "Foxtale One Eve Eye Gel", "brand": "Foxtale", "category": "Personal Care",
     "raw": "Aqua, Caffeine, Niacinamide, Hyaluronic Acid, Peptide Complex, Cucumber Extract, Aloe Vera Gel, Phenoxyethanol."},

    # DOT & KEY ACTIVE RANGE
    {"name": "Dot & Key 20% Vitamin C + Cica Serum", "brand": "Dot & Key", "category": "Personal Care",
     "raw": "Aqua, Ethyl Ascorbic Acid (20%), Centella Asiatica (Cica) Extract, Glycerin, Propanediol, Sodium Hyaluronate, Blood Orange Extract, Ferulic Acid."},

    {"name": "Dot & Key Watermelon Cooling Sunscreen SPF 50", "brand": "Dot & Key", "category": "Personal Care",
     "raw": "Aqua, Ethylhexyl Methoxycinnamate, Watermelon Fruit Extract, Hyaluronic Acid, Menthyl Lactate, Diethylamino Hydroxybenzoyl Hexyl Benzoate, Titanium Dioxide."},

    {"name": "Dot & Key Cica + Niacinamide Oil-Free Face Gel", "brand": "Dot & Key", "category": "Personal Care",
     "raw": "Aqua, Niacinamide (5%), Centella Asiatica Extract, Tea Tree Oil, Aloe Vera Juice, Salicylic Acid, Carbomer, Phenoxyethanol."},

    {"name": "Dot & Key 72 HR Hydrating Gel + Probiotics", "brand": "Dot & Key", "category": "Personal Care",
     "raw": "Aqua, Rice Water, Lactobacillus Ferment Lysate (Probiotics), Hyaluronic Acid, Kombucha Extract, Glycerin, Saccharide Isomerate."},

    {"name": "Dot & Key Alpha Arbutin + Azelaic Blemish Serum", "brand": "Dot & Key", "category": "Personal Care",
     "raw": "Aqua, Alpha Arbutin (2%), Azelaic Acid, Niacinamide, Licorice Root Extract, Hyaluronic Acid, Tranexamic Acid, Propanediol."},

    {"name": "Dot & Key Retinol + Ceramide Sleep Mask", "brand": "Dot & Key", "category": "Personal Care",
     "raw": "Aqua, Ceramide NP, Retinol, Hyaluronic Acid, Marula Oil, Pomegranate Extract, Cetearyl Alcohol, Glycerin, Stearic Acid."},

    {"name": "Dot & Key Barrier Repair + Face Cream with Ceramides", "brand": "Dot & Key", "category": "Personal Care",
     "raw": "Aqua, Ceramide 1, Ceramide 3, Ceramide 6 II, Phytosphingosine, Cholesterol, Rice Bran Oil, Probiotics, Hyaluronic Acid."},

    {"name": "Dot & Key Skin Plumping Water Beans", "brand": "Dot & Key", "category": "Personal Care",
     "raw": "Aqua, Sodium Hyaluronate, Kakadu Plum Extract, Vitamin B5, Cucumber Extract, Polysorbate 20, Phenoxyethanol, Ethylhexylglycerin."},
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
                f"{name} by {p['brand']}. Clinical active skincare. "
                f"Awareness score: {score}/100. Not a medical recommendation."
            ),
            'fssai_note':      'Clinical cosmetic formulation; approved for topical use.',
            'verdict':         'High-efficacy formulation' if score >= 85 else 'Active ingredient blend' if score >= 70 else 'Professional use',
            'recommendation':  'Suitable for all skin types.' if score >= 85 else 'Patch test recommended for sensitive skin.' if score >= 70 else 'Consult dermatologist before use.',
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
    print(f"Inserting {len(PRODUCTS)} Foxtale & Dot & Key clinical products...")
    inserted = 0
    for p in PRODUCTS:
        if insert(p):
            inserted += 1
        time.sleep(0.1)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
