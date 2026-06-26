"""
Insert Typsy Beauty and Colorbar USA cosmetic products
Value and mid-tier makeup formulations
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['propylparaben', 'bha', 'talc', 'lanolin oil']
_WORTH = ['film-formers', 'cyclopentasiloxane', 'dimethicone', 'phenoxyethanol', 'propylene glycol']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'paraben' in n: return 'Preservative; endocrine disruptor concerns'
        if 'bha' in n: return 'Beta-hydroxy acid; exfoliant'
        if 'talc' in n: return 'Powder; inhalation concerns'
        if 'lanolin' in n: return 'Wool derivative; potential allergen'
    if cls == 'worth_knowing':
        if 'film-former' in n: return 'Polymer; texture and durability'
        if 'cyclopentasiloxane' in n or 'dimethicone' in n: return 'Silicone; conditioning'
        if 'phenoxyethanol' in n: return 'Preservative; safe at regulated levels'
    return 'Cosmetic ingredient; standard formulation'

def _reg_note(cls: str) -> str:
    return 'Cosmetic ingredient' if cls != 'commonly_questioned' else 'Subject to regulatory review'

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
    # TYPSY BEAUTY
    {"name": "Typsy Beauty Drink Up Lip Oil", "brand": "Typsy Beauty", "category": "Personal Care",
     "raw": "Hydrogenated Polyisobutene, Polyisobutene, Ethylhexyl Palmitate, Caprylic/Capric Triglyceride, Ethylene/Propylene/Styrene Copolymer, Silica Dimethyl Silylate, Tocopheryl Acetate, Jojoba Seed Oil."},
    {"name": "Typsy Beauty Cha Ching Highlighter", "brand": "Typsy Beauty", "category": "Personal Care",
     "raw": "Mica, Ethylhexyl Palmitate, Magnesium Stearate, Caprylic/Capric Triglyceride, Zea Mays (Corn) Starch, Polyethylene, Silica, Dimethicone, Phenoxyethanol."},
    {"name": "Typsy Beauty Enchanted Garden Rose Blush", "brand": "Typsy Beauty", "category": "Personal Care",
     "raw": "Talc, Mica, Magnesium Stearate, Polyethylene, Paraffinum Liquidum, Ethylhexyl Palmitate, Silica, Dimethicone, Tridecyl Trimellitate, Phenoxyethanol."},
    {"name": "Typsy Beauty Line Up Eyeliner", "brand": "Typsy Beauty", "category": "Personal Care",
     "raw": "Aqua, Acrylates/Ethylhexyl Acrylate Copolymer, Butylene Glycol, Styrene/Acrylates Copolymer, Phenoxyethanol, Ammonium Acrylates Copolymer, Sodium Dehydroacetate."},
    # COLORBAR
    {"name": "Colorbar Perfect Match Primer", "brand": "Colorbar", "category": "Personal Care",
     "raw": "Cyclopentasiloxane, Dimethicone Crosspolymer, Tocopheryl Acetate, Isododecane, Neopentyl Glycol Diheptanoate, Propylparaben."},
    {"name": "Colorbar 24Hrs Weightless Liquid Foundation", "brand": "Colorbar", "category": "Personal Care",
     "raw": "Aqua, Isododecane, Cyclopentasiloxane, Ethylhexyl Methoxycinnamate, Propylene Glycol, Potassium Cetyl Phosphate, PEG-10 Dimethicone, Magnesium Sulfate, Phenoxyethanol."},
    {"name": "Colorbar Velvet Matte Lipstick", "brand": "Colorbar", "category": "Personal Care",
     "raw": "Castor Seed Oil, Isopropyl Myristate, Candelilla Wax, Carnauba Wax, Ozokerite Wax, Lanolin Oil, Propylparaben, BHA, Tocopheryl Acetate."},
    {"name": "Colorbar Luxe Nail Lacquer", "brand": "Colorbar", "category": "Personal Care",
     "raw": "Butyl Acetate, Ethyl Acetate, Nitrocellulose, Adipic Acid/Neopentyl Glycol/Trimellitic Anhydride Copolymer, Acetyl Tributyl Citrate, Isopropyl Alcohol."},
    {"name": "Colorbar Hydrating Foam Cleanser", "brand": "Colorbar", "category": "Personal Care",
     "raw": "Aqua, Glycerin, Stearic Acid, Myristic Acid, Potassium Hydroxide, Lauric Acid, PEG-8, Glyceryl Stearate, Glycol Distearate, Sodium Methyl Cocoyl Taurate."},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Makeup and cosmetics. Score: {score}/100. Patch test for sensitive skin.",
            'fssai_note': 'Cosmetic formulation; standard makeup product.',
            'verdict': 'Standard cosmetic formulation',
            'recommendation': 'Patch test recommended for sensitive skin.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Typsy Beauty & Colorbar products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
