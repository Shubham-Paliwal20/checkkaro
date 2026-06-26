"""
Insert Vadilal Ice Cream Full Registry products
Comprehensive portfolio across candy, classic, cones, family tubs, sticks, and traditional ranges
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['synthetic food colour', 'e122', 'e100', 'hydrogenated']
_WORTH = ['emulsifier', 'stabilizer', 'e471', 'e412', 'e407', 'e410', 'e401', 'e440', 'e433', 'e322', 'e476']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'synthetic' in n or 'colour' in n or 'e122' in n: return 'Synthetic food colour; permitted but additive-based'
        if 'hydrogenated' in n: return 'Hydrogenated oil; trans fat concerns'
    if cls == 'worth_knowing':
        if 'emulsifier' in n or 'e471' in n or 'e322' in n or 'e476' in n: return 'Emulsifier; texture and stability'
        if 'stabilizer' in n or 'e412' in n or 'e407' in n or 'e410' in n or 'e401' in n or 'e440' in n or 'e433' in n: return 'Stabilizer; prevents separation'
    return 'Natural or permitted food ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Contains additives; permitted in regulated amounts'
    if cls == 'worth_knowing': return 'Permitted food additive; standard ice cream formulation'
    return 'Natural food ingredient'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    items = [i.strip() for i in raw.split(',')]
    return [i for i in items if len(i) > 2]

def _build_obj(name: str) -> dict:
    cls = _classify(name)
    return {'name': name, 'aliases': '', 'classification': cls, 'one_line_note': _note(name, cls), 'regulatory_note': _reg_note(cls)}

def _score(ingredient_objs: list) -> int:
    score = 100
    for ing in ingredient_objs:
        if ing['classification'] == 'commonly_questioned': score -= 8
        elif ing['classification'] == 'worth_knowing': score -= 1
    return max(0, min(100, score))

PRODUCTS = [
    # CANDY & NOVELTIES RANGE
    {"name": "Vadilal Jolly Jelly (Raspberry)", "brand": "Vadilal", "category": "Food",
     "raw": "Water, Sugar, Fruit Pulp (5%), Acidity Regulator (E330), Stabilizers (E401, E440), Permitted Synthetic Food Colour (E122)."},
    # CLASSIC RANGE
    {"name": "Vadilal Vanilla Cup", "brand": "Vadilal", "category": "Food",
     "raw": "Milk Solids, Sugar, Permitted Emulsifier (E471) and Stabilizers (E412, E407, E410), Vanilla Flavour (Nature Identical)."},
    # CONES RANGE
    {"name": "Vadilal Badabite Select Belgian Chocolate", "brand": "Vadilal", "category": "Food",
     "raw": "Ice Cream (65%): Milk Solids, Sugar, Belgian Chocolate (5%), Cocoa Solids. Cone (15%): Wheat Flour, Sugar, Edible Vegetable Oil. Coating (20%): Dark Chocolate, Edible Vegetable Oil."},
    {"name": "Vadilal Disc Cookie 'n' Cream", "brand": "Vadilal", "category": "Food",
     "raw": "Milk Solids, Sugar, Chocolate Cookies (10%), Wheat Flour, Cocoa Solids, Emulsifier (E471), Stabilizers (E412, E407)."},
    # FAMILY TUBS RANGE
    {"name": "Vadilal Gourmet Natural Tender Coconut", "brand": "Vadilal", "category": "Food",
     "raw": "Milk Solids, Sugar, Tender Coconut Pieces (15%), Coconut Milk, Permitted Emulsifier (E471) and Stabilizers (E412, E433, E407, E401, E410)."},
    {"name": "Vadilal Gourmet Natural Kesar Pista", "brand": "Vadilal", "category": "Food",
     "raw": "Milk Solids, Sugar, Pistachio Nuts (4%), Saffron, Permitted Emulsifier (E471) and Stabilizers (E412, E407, E410), Saffron Flavour, Permitted Natural Colours (E100, E160b)."},
    {"name": "Vadilal Funtasia Chocolate Brownie", "brand": "Vadilal", "category": "Food",
     "raw": "Milk Solids, Sugar, Brownie Pieces (8%) [Wheat Flour, Cocoa Solids, Butter], Cocoa Solids, Emulsifier (E471), Stabilizers (E412, E407)."},
    # STICKS & BARS RANGE
    {"name": "Vadilal Gourmet Ice Cream Bar - Roasted Almond", "brand": "Vadilal", "category": "Food",
     "raw": "Ice Cream: Milk Solids, Sugar. Coating: Milk Chocolate, Roasted Almonds (6%), Cocoa Butter, Cocoa Solids, Emulsifier (E322, E476)."},
    {"name": "Vadilal Mega Bar Alphonso Mango", "brand": "Vadilal", "category": "Food",
     "raw": "Mango Ice Cream: Milk Solids, Sugar, Alphonso Mango Pulp (15%). Coating: Mango Fruit Layer, White Chocolate."},
    # TRADITIONAL RANGE
    {"name": "Vadilal Matka Kulfi", "brand": "Vadilal", "category": "Food",
     "raw": "Milk Solids (Condensed Milk), Sugar, Saffron, Cardamom, Almond bits, Pistachio bits, Permitted Stabilizers."},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Premium ice cream. Score: {score}/100. Contains dairy and common allergens.",
            'fssai_note': 'Frozen dessert; contains milk solids and emulsifiers.',
            'verdict': 'Premium ice cream formulation' if score >= 90 else 'Standard ice cream product',
            'recommendation': 'Contains dairy and nuts; check for allergies. Best served fresh.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Vadilal Ice Cream products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
