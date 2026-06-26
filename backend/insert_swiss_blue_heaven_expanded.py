"""
Insert Swiss Beauty and Blue Heaven expanded phase 2 registry
Value-segment cosmetics with clinical formulation analysis
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['talc', 'propylparaben', 'bha', 'mineral oil']
_WORTH = ['dimethicone', 'phenoxyethanol', 'cyclopentasiloxane', 'film-formers', 'propylene glycol']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'talc' in n: return 'Talc powder; inhalation concerns'
        if 'paraben' in n: return 'Preservative; endocrine disruptor concerns'
        if 'bha' in n: return 'Beta-hydroxy acid; exfoliant'
        if 'mineral oil' in n: return 'Occlusive mineral oil; may clog pores'
    if cls == 'worth_knowing':
        if 'dimethicone' in n or 'cyclopentasiloxane' in n: return 'Silicone; texture and wear'
        if 'phenoxyethanol' in n: return 'Preservative; safe at levels'
        if 'film-former' in n: return 'Polymer for texture and durability'
        return 'Moderate concern ingredient'
    return 'Natural or safe cosmetic ingredient'

def _reg_note(cls: str) -> str:
    return 'Cosmetic ingredient; permitted ingredient' if cls != 'commonly_questioned' else 'Subject to regulatory review'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    return [i.strip() for i in raw.split(',') if len(i.strip()) > 2]

def _build_obj(name: str) -> dict:
    cls = _classify(name)
    return {'name': name, 'aliases': '', 'classification': cls, 'one_line_note': _note(name, cls), 'regulatory_note': _reg_note(cls)}

def _score(ingredient_objs: list) -> int:
    score = 100
    for ing in ingredient_objs:
        if ing['classification'] == 'commonly_questioned': score -= 8
        elif ing['classification'] == 'worth_knowing': score -= 2
    return max(0, min(100, score))

PRODUCTS = [
    # SWISS BEAUTY
    {"name": "Swiss Beauty Highlighter Liquid (Drop & Glow)", "brand": "Swiss Beauty", "category": "Personal Care",
     "raw": "Aqua, Mica, Titanium Dioxide, Isododecane, Glycerin, Cyclopentasiloxane, Ethylhexyl Palmitate, PEG-10 Dimethicone, Magnesium Sulfate, Phenoxyethanol."},
    {"name": "Swiss Beauty Airbrush Finish Full Coverage Foundation", "brand": "Swiss Beauty", "category": "Personal Care",
     "raw": "Aqua, Dimethicone, Isononyl Isononanoate, Silica, Glycerin, Butylene Glycol, Trimethylsiloxysilicate, Polyglyceryl-4 Isostearate, Sodium Hyaluronate, Vitamin E."},
    {"name": "Swiss Beauty Metallic Liquid Eyeshadow", "brand": "Swiss Beauty", "category": "Personal Care",
     "raw": "Water, Polyvinyl Alcohol, Propylene Glycol, Glycerin, Mica, Carbomer, Triethanolamine, Phenoxyethanol."},
    {"name": "Swiss Beauty HD Matte Lipstick", "brand": "Swiss Beauty", "category": "Personal Care",
     "raw": "Octyldodecanol, Ricinus Communis Seed Oil, Silica, Microcrystalline Wax, Ozokerite, Polyethylene, Isopropyl Myristate, Vitamin E."},
    {"name": "Swiss Beauty Lip Primer & Matte Lipstick (2-in-1)", "brand": "Swiss Beauty", "category": "Personal Care",
     "raw": "Lipstick: Candelilla Wax, Carnauba Wax, Synthetic Wax, Isopropyl Myristate, Vit E. Primer: Dimethicone Crosspolymer, Silica, Cyclopentasiloxane."},
    {"name": "Swiss Beauty Pearl Illuminator Makeup Base", "brand": "Swiss Beauty", "category": "Personal Care",
     "raw": "Water, Glycerin, Mica, Propylene Glycol, Caprylic/Capric Triglyceride, Niacinamide, Squalane, Sodium Hyaluronate."},
    # BLUE HEAVEN
    {"name": "Blue Heaven Oil Control Compact Powder", "brand": "Blue Heaven", "category": "Personal Care",
     "raw": "Talc, Kaolin, Zinc Stearate, Magnesium Carbonate, Titanium Dioxide, Silica, Perfume, Iron Oxides."},
    {"name": "Blue Heaven Lash Twist Mascara", "brand": "Blue Heaven", "category": "Personal Care",
     "raw": "Water, Styrene/Acrylates/Ammonium Methacrylate Copolymer, Beeswax, Paraffin, Stearic Acid, Glyceryl Stearate, Polyisobutene, Carbon Black."},
    {"name": "Blue Heaven Primer (Studio Perfection)", "brand": "Blue Heaven", "category": "Personal Care",
     "raw": "Cyclopentasiloxane, Dimethicone Crosspolymer, Vitamin E, Propylparaben, Silicones."},
    {"name": "Blue Heaven Elegance Matte Lip Color", "brand": "Blue Heaven", "category": "Personal Care",
     "raw": "Isododecane, Trimethylsiloxysilicate, Disteardimonium Hectorite, Propylene Carbonate, Vitamin E, Approved Colors."},
    {"name": "Blue Heaven Candy Lip Balm", "brand": "Blue Heaven", "category": "Personal Care",
     "raw": "Mineral Oil, Paraffin Wax, Shea Butter, Cocoa Butter, Vitamin E, Flavor."},
    {"name": "Blue Heaven Shimmer Matte Blush", "brand": "Blue Heaven", "category": "Personal Care",
     "raw": "Talc, Mica, Magnesium Stearate, Aluminum Starch Octenylsuccinate, Silica, Vitamin E, Phenoxyethanol."},
]

def insert(p: dict) -> bool:
    name = p['name']
    raw = p['raw']
    parsed = _parse(raw)
    ingredient_objs = [_build_obj(i) for i in parsed]
    score = _score(ingredient_objs)
    try:
        existing = supabase.from_('ai_extracted_products').select('id').ilike('name', name).limit(1).execute()
        if existing.data:
            print(f"  skip (exists): {name}")
            return False
        supabase.from_('ai_extracted_products').insert({
            'name': name, 'brand': p['brand'], 'category': p['category'], 'image_url': None, 'images': [],
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Value cosmetics. Score: {score}/100. Patch test for sensitive skin.",
            'fssai_note': 'Value-tier cosmetic; standard formulation.', 'verdict': 'Standard formulation' if score >= 80 else 'Contains additives',
            'recommendation': 'Patch test recommended.', 'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Swiss Beauty & Blue Heaven expanded products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    time.sleep(0.1)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
