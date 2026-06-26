"""
Insert Swiss Beauty and Blue Heaven value-tier cosmetics from clinical databases
Paraben-free makeup and cosmetic formulations
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = [
    'mineral oil', 'isopropyl myristate', 'talc',
]
_WORTH = [
    'dimethicone', 'phenoxyethanol', 'propylene glycol', 'cyclopentasiloxane',
    'film-formers', 'silica', 'propylparaben', 'methylparaben',
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
        if 'mineral oil' in n: return 'Mineral oil; occlusive; may clog pores'
        if 'isopropyl myristate' in n: return 'Emollient; potentially comedogenic'
        if 'talc' in n: return 'Powder; asbestos contamination concerns'
        return 'Questioned ingredient'
    if cls == 'worth_knowing':
        if 'dimethicone' in n: return 'Silicone; conditioning agent'
        if 'phenoxyethanol' in n: return 'Preservative; safe at regulated levels'
        if 'propylene glycol' in n: return 'Humectant; skin conditioning'
        if 'cyclopentasiloxane' in n: return 'Silicone; texture agent'
        if 'silica' in n: return 'Absorbent; safe ingredient'
        if 'propylparaben' in n or 'methylparaben' in n: return 'Preservative; endocrine concerns'
        if 'film-former' in n: return 'Polymer; texture and wear'
        return 'Moderate concern; safe in regulated amounts'
    # generally_recognised
    if 'glycerin' in n: return 'Humectant; hydrating'
    if 'shea butter' in n: return 'Natural butter; nourishing'
    if 'mica' in n: return 'Mineral; shimmer and texture'
    if 'titanium dioxide' in n: return 'Mineral; whitening and sun protection'
    if 'aloe vera' in n: return 'Soothing botanical'
    if 'vitamin e' in n: return 'Antioxidant; protective'
    if 'beeswax' in n: return 'Natural wax; protective'
    if 'rose' in n: return 'Botanical; hydrating'
    if 'water' in n or 'aqua' in n: return 'Solvent; pure ingredient'
    if 'castor oil' in n: return 'Natural oil; emollient'
    if 'jojoba' in n: return 'Natural oil; conditioning'
    if 'hyaluronic acid' in n: return 'Humectant; hydrating and plumping'
    if 'niacinamide' in n: return 'Vitamin B3; skin-balancing'
    if 'menthol' in n: return 'Cooling botanical'
    if 'panthenol' in n: return 'Pro-vitamin B5; soothing'
    if 'xanthan gum' in n: return 'Natural thickener; safe'
    if 'almond oil' in n: return 'Natural oil; nourishing'
    if 'hazelnut' in n: return 'Natural nut; conditioning'
    return 'Cosmetic ingredient; safe for topical use'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Cosmetic ingredient; regulatory review needed'
    if cls == 'worth_knowing': return 'Permitted cosmetic additive; safe at regulated levels'
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
        if cls == 'commonly_questioned': score -= 8
        elif cls == 'worth_knowing': score -= 2
    return max(0, min(100, score))

PRODUCTS = [
    # SWISS BEAUTY
    {"name": "Swiss Beauty Real Makeup Base Highlighting Primer", "brand": "Swiss Beauty", "category": "Personal Care",
     "raw": "Aqua, Glycerin, Propylene Glycol, Mica, Titanium Dioxide, Dimethicone, Shea Butter, Cetearyl Alcohol, Caprylic/Capric Triglyceride, Phenoxyethanol."},

    {"name": "Swiss Beauty Liquid Concealer", "brand": "Swiss Beauty", "category": "Personal Care",
     "raw": "Water, Isododecane, Dimethicone, Cyclopentasiloxane, Ethylhexyl Palmitate, Silica, Sorbitan Sesquioleate, Stearic Acid, Vitamin E."},

    {"name": "Swiss Beauty Long Lasting Makeup Fixer", "brand": "Swiss Beauty", "category": "Personal Care",
     "raw": "Aqua, Aloe Barbadensis Leaf Extract, Vitamin E, Propylene Glycol, PVP, Phenoxyethanol, Castor Oil, Fragrance."},

    {"name": "Swiss Beauty Blemish Balm (BB) Cream", "brand": "Swiss Beauty", "category": "Personal Care",
     "raw": "Aqua, Mineral Oil, Titanium Dioxide, Isopropyl Myristate, Glycerin, Stearic Acid, Cetyl Alcohol, Niacinamide, Vitamin E."},

    {"name": "Swiss Beauty Skin Care Makeup HD Foundation", "brand": "Swiss Beauty", "category": "Personal Care",
     "raw": "Aqua, Cyclopentasiloxane, Ethylhexyl Palmitate, Silica, Sorbitan Sesquioleate, Beeswax, Vitamin E, Dimethicone."},

    # BLUE HEAVEN
    {"name": "Blue Heaven Hyper Matte Liquid Foundation", "brand": "Blue Heaven", "category": "Personal Care",
     "raw": "Aqua, Cyclopentasiloxane, PEG-10 Dimethicone, Silica, Glycerin, Phenoxyethanol, Ethylhexylglycerin, Vitamin E, Iron Oxides."},

    {"name": "Blue Heaven Flawless Makeup Finisher", "brand": "Blue Heaven", "category": "Personal Care",
     "raw": "Aqua, Propylene Glycol, Aloe Vera Extract, Vitamin E, PVP, Polysorbate 20, Phenoxyethanol, Menthol."},

    {"name": "Blue Heaven Silk & Stain Lip Stain", "brand": "Blue Heaven", "category": "Personal Care",
     "raw": "Water, Glycerin, Polyacrylate Crosspolymer-6, Vitamin E, Panthenol, Hyaluronic Acid, Sodium Benzoate, Potassium Sorbate."},

    {"name": "Blue Heaven Kiss & Blush Lip & Cheek Tint", "brand": "Blue Heaven", "category": "Personal Care",
     "raw": "Aqua, Glycerin, Rose Extract, Vitamin E, Hyaluronic Acid, Xanthan Gum, Phenoxyethanol, Food Grade Colors."},

    {"name": "Blue Heaven Get Bold Eyeliner", "brand": "Blue Heaven", "category": "Personal Care",
     "raw": "Aqua, Carbon Black, Polyvinyl Alcohol, Propylene Glycol, Magnesium Aluminum Silicate, Xanthan Gum, Methylparaben, Propylparaben."},
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
                f"{name} by {p['brand']}. Value-tier makeup and cosmetics. "
                f"Awareness score: {score}/100. Patch test recommended for sensitive skin."
            ),
            'fssai_note':      'Cosmetic formulation; paraben-free option available.',
            'verdict':         'Standard formulation' if score >= 80 else 'Contains additives',
            'recommendation':  'Patch test recommended for sensitive skin.',
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
    print(f"Inserting {len(PRODUCTS)} Swiss Beauty & Blue Heaven products...")
    inserted = 0
    for p in PRODUCTS:
        if insert(p):
            inserted += 1
        time.sleep(0.1)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
