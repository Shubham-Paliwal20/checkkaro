"""
Insert missing 4 Beardo products from Extended Registry PDF
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = [
    'sodium laureth sulfate','sls','phthalate','diethyl phthalate',
    'p-phenylenediamine','resorcinol','sodium sulfite','phenoxyethanol',
]
_WORTH = ['mineral oil','beeswax','carnauba wax','silicone','cyclopentasiloxane']

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
        if 'p-phenylenediamine' in n: return 'Hair dye intermediate; potential allergic reactions'
        if 'resorcinol' in n: return 'Hair dye coupler; skin irritant potential'
        if 'sodium sulfite' in n: return 'Reducing agent; oxidising allergen'
        if 'phenoxyethanol' in n: return 'Preservative; safe at low concentrations'
        return 'Commonly questioned ingredient'
    if cls == 'worth_knowing':
        if 'cyclopentasiloxane' in n: return 'Silicone; lightweight conditioning agent'
        return 'Moderate concern; safe in regulated amounts'
    # generally_recognised
    if 'argan oil' in n: return 'Rich in antioxidants and fatty acids'
    if 'walnut' in n: return 'Natural exfoliant and scrub'
    if 'coffee' in n: return 'Exfoliating and stimulating agent'
    if 'turmeric' in n: return 'Natural brightening and soothing'
    if 'aloe vera' in n: return 'Soothing and hydrating'
    if 'vitamin e' in n: return 'Antioxidant protection'
    if 'menthol' in n: return 'Cooling and refreshing'
    if 'dimethiconol' in n: return 'Silicone conditioning agent'
    if 'glycerin' in n: return 'Humectant; draws moisture to skin'
    return 'Generally recognised as safe'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Permitted for temporary use; check local regulations'
    if cls == 'worth_knowing': return 'Permitted additive; use as directed'
    return 'Approved under standard regulations'

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
        if cls == 'commonly_questioned': score -= 15
        elif cls == 'worth_knowing': score -= 5
    return max(0, min(100, score))

PRODUCTS = [
    {"name": "Beardo Argan Oil Hair Serum", "raw": "Cyclopentasiloxane, Dimethiconol, Argan Oil, Almond Oil, Vitamin E, Fragrance."},
    {"name": "Beardo De-Tan Face Scrub", "raw": "Aqua, Stearic Acid, Walnut Shell Powder, Glycerin, Coffee Powder, Aloe Vera Extract, Vitamin E."},
    {"name": "Beardo Beard Color (Natural Black)", "raw": "Aqua, Cetearyl Alcohol, p-Phenylenediamine, Resorcinol, Sodium Sulfite, Erythorbic Acid, Aloe Vera Extract."},
    {"name": "Beardo Ice Blast Body Wash", "raw": "Aqua, Sodium Laureth Sulfate, Cocamidopropyl Betaine, Menthol, Peppermint Oil, Glycerin, Aloe Vera Extract."},
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
            'brand':           'Beardo',
            'category':        'Personal Care',
            'image_url':       None,
            'images':          [],
            'awareness_score': score,
            'summary': (
                f"{name} by Beardo. Awareness score: {score}/100. "
                "Not a health assessment or medical advice."
            ),
            'fssai_note':      'Subject to applicable cosmetic regulations.',
            'verdict':         'Average formulation' if score < 80 else 'Clean formulation',
            'recommendation':  'Suitable for most. Check for personal allergies.' if score >= 80 else 'Review before regular use.',
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
    print(f"Inserting {len(PRODUCTS)} missing Beardo products...")
    inserted = 0
    for p in PRODUCTS:
        if insert(p):
            inserted += 1
        time.sleep(0.1)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
