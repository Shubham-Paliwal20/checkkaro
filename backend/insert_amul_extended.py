"""
Insert Amul Ice Cream extended products from Amul_IceCream_Product_Registry PDF
Includes family packs, cones, and premium sticks
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = [
    'sugar', 'glucose', 'high fructose corn syrup',
    'artificial flavor', 'artificial flavour', 'nature identical',
]
_WORTH = [
    'emulsifier', 'stabilizer', 'stabiliser', 'e471', 'e407', 'e466', 'e412', 'e410',
    'hydrogenated vegetable fat', 'vegetable fat', 'edible vegetable oil',
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
        if 'sugar' in n: return 'Sweetener; high consumption linked to health concerns'
        if 'nature identical' in n or 'artificial flavor' in n or 'artificial flavour' in n:
            return 'Synthetic replica of a natural flavour compound'
        return 'Commonly questioned ingredient'
    if cls == 'worth_knowing':
        if 'emulsifier' in n or 'e471' in n: return 'Emulsifier derived from fats, generally safe'
        if 'stabilizer' in n or 'stabiliser' in n: return 'Texture stabilizer, generally recognised as safe'
        if 'e407' in n: return 'Carrageenan – seaweed extract stabilizer'
        if 'e466' in n: return 'Carboxymethyl cellulose – thickener'
        if 'e412' in n: return 'Guar gum – natural stabilizer'
        if 'e410' in n: return 'Locust bean gum – natural stabilizer'
        if 'vegetable' in n and 'fat' in n: return 'Processed vegetable fat; quality varies by source'
        if 'hydrogenated' in n: return 'Hydrogenated fat; trans fat concerns'
        return 'Moderate concern, safe in regulated amounts'
    # generally_recognised
    if 'milk solid' in n or 'milk solids' in n: return 'Dairy base, source of protein and calcium'
    if 'cocoa' in n: return 'Natural cocoa, source of antioxidants'
    if 'almond' in n or 'cashew' in n: return 'Natural nut, rich in healthy fats and protein'
    if 'mango' in n: return 'Natural fruit, rich in vitamins and antioxidants'
    if 'cocoa butter' in n: return 'Natural fat from cocoa beans'
    if 'chocolate' in n: return 'Contains cocoa solids and cocoa butter'
    return 'Generally recognised as safe'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Subject to regulatory scrutiny; permitted by FSSAI'
    if cls == 'worth_knowing': return 'Permitted additive under FSSAI/CODEX standards'
    return 'Approved under FSSAI ice cream standards'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    # Remove parenthetical info like percentages
    import re
    raw = re.sub(r'\s*\(\d+%\)', '', raw)

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
        elif cls == 'worth_knowing': score -= 3
    return max(0, min(100, score))

PRODUCTS = [
    # AMUL FAMILY PACK / TUB
    {"name": "Amul Vanilla Magic", "brand": "Amul", "category": "Dairy",
     "raw": "Milk Solids, Sugar, Permitted Emulsifier (E471) and Stabilizers (E407, E466, E412, E410), Vanilla Flavour (Nature Identical Flavouring Substances)."},

    {"name": "Amul Choco Chips", "brand": "Amul", "category": "Dairy",
     "raw": "Milk Solids, Sugar, Chocolate Chips (10%) [Sugar, Hydrogenated Vegetable Fat, Cocoa Solids, Emulsifier (E322)], Cocoa Solids, Permitted Emulsifier (E471) and Stabilizers (E407, E466, E412, E410)."},

    {"name": "Amul King Alphonso", "brand": "Amul", "category": "Dairy",
     "raw": "Milk Solids, Sugar, Mango Pulp (15%), Permitted Emulsifier (E471) and Stabilizers (E407, E466, E412, E410), Mango Flavour, Permitted Natural Colour (E160b)."},

    # AMUL CONE
    {"name": "Amul Tricone (Butterscotch)", "brand": "Amul", "category": "Dairy",
     "raw": "Ice Cream: Milk Solids, Sugar, Butterscotch Granules (12%), Emulsifiers, Stabilizers. Biscuit Cone: Wheat Flour, Sugar, Vegetable Oil, Emulsifier (E322). Spray: Edible Vegetable Fat, Cocoa Solids."},

    # AMUL PREMIUM STICK
    {"name": "Amul Epic (Choco Almond)", "brand": "Amul", "category": "Dairy",
     "raw": "Ice Cream: Milk Solids, Sugar, Permitted Emulsifiers, Stabilizers. Outer Coating: Belgian Chocolate, Roasted Almonds (5%), Edible Vegetable Oil, Cocoa Butter, Cocoa Solids, Emulsifier (E322, E476)."},

    # AMUL STICK
    {"name": "Amul Frostik", "brand": "Amul", "category": "Dairy",
     "raw": "Milk Solids, Sugar, Chocolate Coating (Sugar, Edible Vegetable Fat, Cocoa Solids, Emulsifier E322), Permitted Emulsifier (E471), Stabilizers (E407, E466, E412, E410)."},
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
                f"{name} by {p['brand']}. Dairy ice cream. "
                f"Awareness score: {score}/100. Not a health assessment or medical advice."
            ),
            'fssai_note':      'Subject to FSSAI ice cream standards.',
            'verdict':         'Clean formulation' if score >= 80 else 'Average formulation' if score >= 60 else 'High sugar content',
            'recommendation':  'Enjoy in moderation.' if score >= 60 else 'Limit consumption due to high sugar.',
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
    print(f"Inserting {len(PRODUCTS)} Amul ice cream products...")
    inserted = 0
    for p in PRODUCTS:
        if insert(p):
            inserted += 1
        time.sleep(0.1)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
