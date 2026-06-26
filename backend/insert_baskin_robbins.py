"""
Insert Baskin Robbins ice cream products from Baskin_Robbins_Full_Portfolio PDF
Premium ice cream flavours including chocolate, classic, fruit & exotic, and novelties
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = [
    'sugar', 'glucose', 'butter', 'artificial flavor', 'artificial flavour', 'nature identical',
]
_WORTH = [
    'emulsifier', 'stabilizer', 'stabiliser', 'e471', 'e322', 'e476', 'e407', 'e141',
    'edible vegetable fat', 'vegetable oil', 'cocoa solids',
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
        if 'butter' in n: return 'Dairy fat; high in saturated fat'
        if 'glucose' in n: return 'Simple sugar; rapid glucose spike'
        if 'nature identical' in n or 'artificial flavor' in n or 'artificial flavour' in n:
            return 'Synthetic replica of a natural flavour compound'
        return 'Commonly questioned ingredient'
    if cls == 'worth_knowing':
        if 'emulsifier' in n or 'e471' in n: return 'Emulsifier derived from fats, generally safe'
        if 'e322' in n: return 'Lecithin emulsifier, generally safe'
        if 'e476' in n: return 'Polyglycerol polyricinoleate; food emulsifier'
        if 'stabilizer' in n or 'stabiliser' in n: return 'Texture stabilizer, generally recognised as safe'
        if 'e407' in n: return 'Carrageenan – seaweed extract stabilizer'
        if 'e141' in n: return 'Chlorophyll; natural green colour'
        if 'vegetable' in n and 'fat' in n: return 'Processed vegetable fat; quality varies by source'
        return 'Moderate concern, safe in regulated amounts'
    # generally_recognised
    if 'milk solid' in n or 'milk solids' in n: return 'Dairy base, source of protein and calcium'
    if 'cocoa' in n or 'chocolate' in n: return 'Contains cocoa solids and cocoa butter; antioxidants'
    if 'almond' in n: return 'Roasted almond; rich in healthy fats and protein'
    if 'pecan' in n: return 'Pecan nut; nutrient-dense'
    if 'mango' in n or 'alphonso' in n: return 'Natural mango pulp; rich in vitamins'
    if 'strawberry' in n: return 'Natural strawberry; antioxidant-rich'
    if 'coffee' in n: return 'Coffee extract; natural flavouring'
    if 'mint' in n: return 'Mint extract; cooling and digestive'
    if 'currant' in n: return 'Black currant fruit; vitamin C rich'
    if 'fudge' in n: return 'Chocolate fudge component'
    if 'caramel' in n: return 'Caramel ribbon; flavour enhancement'
    if 'cookie dough' in n: return 'Contains wheat flour and chocolate chips'
    if 'wheat flour' in n: return 'Contains gluten; avoid if gluten intolerant'
    if 'cocoa butter' in n: return 'Natural fat from cocoa beans'
    return 'Generally recognised as safe'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Subject to regulatory scrutiny; permitted by FSSAI'
    if cls == 'worth_knowing': return 'Permitted additive under FSSAI/CODEX standards'
    return 'Approved under FSSAI ice cream standards'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    import re
    # Remove percentage info
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
    # CHOCOLATE & NUTTY
    {"name": "Baskin Robbins Roasted Californian Almond", "brand": "Baskin Robbins", "category": "Dairy",
     "raw": "Vanilla flavoured ice cream with roasted Californian almonds. Milk Solids, Sugar, Roasted Almonds (10%), Emulsifier (E471), Stabilizers."},

    {"name": "Baskin Robbins Bavarian Chocolate", "brand": "Baskin Robbins", "category": "Dairy",
     "raw": "Chocolate flavoured ice cream with chocolate chips and a cashew fudge ribbon. Milk Solids, Sugar, Chocolate Chips, Cashew Fudge Ribbon, Cocoa Solids, Emulsifier (E471), Stabilizers."},

    {"name": "Baskin Robbins World Class Chocolate", "brand": "Baskin Robbins", "category": "Dairy",
     "raw": "White chocolate flavoured ice cream swirled with milk chocolate flavoured ice cream. Milk Solids, Sugar, Cocoa Solids, Cocoa Butter, Emulsifier (E471), Stabilizers."},

    # CLASSIC FLAVOURS
    {"name": "Baskin Robbins Gold Medal Ribbon", "brand": "Baskin Robbins", "category": "Dairy",
     "raw": "Vanilla flavoured ice cream with chocolate flavoured chips and a caramel ribbon. Milk Solids, Sugar, Caramel Ribbon (15%) [Condensed Milk, Sugar, Glucose, Butter], Chocolate Chips (5%), Permitted Emulsifier (E471), Stabilizers (E412, E407)."},

    {"name": "Baskin Robbins Pralines 'n Cream", "brand": "Baskin Robbins", "category": "Dairy",
     "raw": "Vanilla flavoured ice cream with praline pecans and a caramel ribbon. Milk Solids, Sugar, Praline Pecans (10%) [Pecans, Sugar, Butter, Salt], Caramel Ribbon (10%), Emulsifier (E471), Stabilizers."},

    {"name": "Baskin Robbins Chocolate Chip Cookie Dough", "brand": "Baskin Robbins", "category": "Dairy",
     "raw": "Vanilla flavoured ice cream with cookie dough pieces and chocolate chips. Milk Solids, Sugar, Cookie Dough (12%) [Wheat Flour, Sugar, Butter, Chocolate Chips], Emulsifier (E471), Stabilizers."},

    {"name": "Baskin Robbins Mint Chocolate Chip", "brand": "Baskin Robbins", "category": "Dairy",
     "raw": "Mint flavoured ice cream with chocolate chips. Milk Solids, Sugar, Chocolate Chips (8%), Mint Extract, Emulsifier (E471), Stabilizers, Permitted Natural Colour (E141)."},

    {"name": "Baskin Robbins Very Berry Strawberry", "brand": "Baskin Robbins", "category": "Dairy",
     "raw": "Strawberry ice cream with strawberry pieces. Milk Solids, Sugar, Strawberry Fruit (15%), Strawberry Puree, Emulsifier (E471), Stabilizers."},

    {"name": "Baskin Robbins Jamoca Almond Fudge", "brand": "Baskin Robbins", "category": "Dairy",
     "raw": "Coffee flavoured ice cream with roasted almonds and a chocolate fudge ribbon. Milk Solids, Sugar, Roasted Almonds (8%), Chocolate Fudge Ribbon (10%), Coffee Extract, Emulsifier (E471), Stabilizers."},

    # FRUIT & EXOTIC
    {"name": "Baskin Robbins Mississippi Mud", "brand": "Baskin Robbins", "category": "Dairy",
     "raw": "Chocolate flavoured ice cream with chocolate cake pieces and a chocolate fudge ribbon. Milk Solids, Sugar, Chocolate Cake (8%), Cocoa Solids, Emulsifier (E471), Stabilizers."},

    {"name": "Baskin Robbins Alphonso Mango", "brand": "Baskin Robbins", "category": "Dairy",
     "raw": "Mango ice cream made with real Alphonso mango pulp. Milk Solids, Sugar, Alphonso Mango Pulp (20%), Emulsifier (E471), Stabilizers, Natural Colour (E160b)."},

    {"name": "Baskin Robbins Black Currant", "brand": "Baskin Robbins", "category": "Dairy",
     "raw": "Black currant flavoured ice cream with black currant fruit pieces. Milk Solids, Sugar, Black Currant Fruit (12%), Emulsifier (E471), Stabilizers."},

    # NOVELTIES & CAKES
    {"name": "Baskin Robbins Roll Cake Slice", "brand": "Baskin Robbins", "category": "Dairy",
     "raw": "Ice Cream: Milk Solids, Sugar, Emulsifiers. Cake: Wheat Flour, Sugar, Eggless Sponge, Cocoa Solids."},

    {"name": "Baskin Robbins Ice Cream Rocks", "brand": "Baskin Robbins", "category": "Dairy",
     "raw": "Bite-sized ice cream treats coated in chocolate. Milk Solids, Sugar, Chocolate Coating [Sugar, Vegetable Fat, Cocoa Solids, Emulsifier E322]."},
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
                f"{name} by {p['brand']}. Premium dairy ice cream. "
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
    print(f"Inserting {len(PRODUCTS)} Baskin Robbins ice cream products...")
    inserted = 0
    for p in PRODUCTS:
        if insert(p):
            inserted += 1
        time.sleep(0.1)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
