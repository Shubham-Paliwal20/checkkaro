"""
Insert Havmor Ice Cream Master Registry
Complete Product Portfolio with Approved Emulsifiers & Stabilizers
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['emulsifier', 'stabilizer', 'sucralose', 'vegetable oil', 'palm oil']
_WORTH = ['milk solids', 'natural', 'mango', 'saffron', 'cardamom', 'fruit', 'nuts', 'cocoa']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'emulsifier' in n or 'e471' in n or 'e476' in n: return 'FSSAI approved emulsifier; safe food additive'
        if 'stabilizer' in n or 'e412' in n or 'e407' in n or 'e410' in n: return 'FSSAI approved stabilizer; improves texture'
        if 'sucralose' in n: return 'Artificial sweetener; approved sugar substitute'
        if 'palm' in n or 'vegetable oil' in n: return 'Vegetable oil base; permitted ingredient'
    if cls == 'worth_knowing':
        if 'milk' in n or 'cream' in n: return 'Milk solids; primary dairy ingredient'
        if 'mango' in n or 'alphonso' in n: return 'Alphonso mango; premium Indian fruit'
        if 'saffron' in n or 'kesar' in n: return 'Saffron; precious spice'
        if 'cardamom' in n: return 'Cardamom; traditional Indian spice'
        if 'kulfi' in n: return 'Traditional Indian frozen dessert'
        if 'nuts' in n or 'pistachio' in n or 'cashew' in n: return 'Premium roasted nuts'
    return 'Havmor ice cream ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'FSSAI approved additives; BIS graded ice cream'
    if cls == 'worth_knowing': return 'Made from pure milk fat; traditional flavors'
    return 'BIS-graded ice cream product'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    return [i.strip() for i in raw.split(',') if len(i.strip()) > 2]

def _build_obj(name: str) -> dict:
    cls = _classify(name)
    return {'name': name, 'aliases': '', 'classification': cls, 'one_line_note': _note(name, cls), 'regulatory_note': _reg_note(cls)}

def _score(ingredient_objs: list) -> int:
    score = 100
    for ing in ingredient_objs:
        if ing['classification'] == 'commonly_questioned': score -= 2
        elif ing['classification'] == 'worth_knowing': score -= 1
    return max(0, min(100, score))

PRODUCTS = [
    # CLASSICS RANGE
    {"name": "Havmor Vanilla", "brand": "Havmor", "category": "Ice Cream",
     "raw": "Milk Solids, Sugar, Permitted Emulsifier (E471), Stabilizers (E412, E407, E410), Natural Vanilla Flavour.",
     "range": "Classics"},
    {"name": "Havmor Strawberry", "brand": "Havmor", "category": "Ice Cream",
     "raw": "Milk Solids, Sugar, Strawberry Fruit Preparation, Emulsifier (E471), Stabilizers (E412, E407, E410).",
     "range": "Classics"},
    {"name": "Havmor Chocolate", "brand": "Havmor", "category": "Ice Cream",
     "raw": "Milk Solids, Sugar, Cocoa Solids, Emulsifier (E471), Stabilizers (E412, E407).",
     "range": "Classics"},
    {"name": "Havmor Butterscotch", "brand": "Havmor", "category": "Ice Cream",
     "raw": "Milk Solids, Sugar, Butterscotch Nuties, Emulsifier (E471), Stabilizers.",
     "range": "Classics"},
    # CONES RANGE
    {"name": "Havmor Turbo Cone - Chocolate", "brand": "Havmor", "category": "Ice Cream",
     "raw": "Ice Cream: Milk Solids, Cocoa. Cone: Wheat Flour, Sugar. Spray: Chocolate compound. Top: Cashew nuts.",
     "range": "Cones", "format": "Cone"},
    {"name": "Havmor Turbo Cone - Butterscotch", "brand": "Havmor", "category": "Ice Cream",
     "raw": "Ice Cream: Milk Solids, Butterscotch granules. Cone: Wheat Flour. Top: Praline nuts.",
     "range": "Cones", "format": "Cone"},
    # EXOTIC RANGE
    {"name": "Havmor Red Velvet Tub", "brand": "Havmor", "category": "Ice Cream",
     "raw": "Milk Solids, Sugar, Red Velvet Cake pieces, Cream Cheese flavour, Emulsifier (E471), Stabilizers.",
     "range": "Exotic"},
    {"name": "Havmor Lotte Choco Pie Ice Cream", "brand": "Havmor", "category": "Ice Cream",
     "raw": "Milk Solids, Sugar, Lotte Choco Pie pieces, Marshmallows, Chocolate sauce.",
     "range": "Exotic"},
    # FRUIT RANGE
    {"name": "Havmor Alphonso Mango Tub", "brand": "Havmor", "category": "Ice Cream",
     "raw": "Milk Solids, Sugar, Alphonso Mango Pulp, Stabilizers, Natural Color (E160b).",
     "range": "Fruit"},
    {"name": "Havmor Tender Coconut", "brand": "Havmor", "category": "Ice Cream",
     "raw": "Milk Solids, Sugar, Tender Coconut bits, Coconut Milk, Stabilizers.",
     "range": "Fruit"},
    # HEALTH RANGE
    {"name": "Havmor Sugar Free Vanilla", "brand": "Havmor", "category": "Ice Cream",
     "raw": "Milk Solids, Fructo-Oligosaccharide, Sucralose, Emulsifiers, Stabilizers.",
     "range": "Health"},
    # INDULGENCE RANGE
    {"name": "Havmor Zulubar (Choco Bar)", "brand": "Havmor", "category": "Ice Cream",
     "raw": "Ice Cream: Milk Solids, Sugar, Emulsifier (E471). Coating: Edible Vegetable Oil, Sugar, Cocoa Solids, Emulsifier (E322, E476).",
     "range": "Indulgence", "format": "Bar"},
    {"name": "Havmor American Nuts", "brand": "Havmor", "category": "Ice Cream",
     "raw": "Milk Solids, Sugar, Mixed Fruit Jelly, Roasted Almonds, Roasted Cashews, Emulsifier (E471), Stabilizers.",
     "range": "Indulgence"},
    {"name": "Havmor Cookie N Cream", "brand": "Havmor", "category": "Ice Cream",
     "raw": "Milk Solids, Sugar, Chocolate Cookies, Emulsifier (E471), Stabilizers (E412, E407).",
     "range": "Indulgence"},
    # KULFI RANGE
    {"name": "Havmor Roll Cut Malai Kulfi", "brand": "Havmor", "category": "Ice Cream",
     "raw": "Concentrated Milk Solids, Sugar, Cardamom, Emulsifiers, Stabilizers.",
     "range": "Kulfi", "format": "Stick"},
    {"name": "Havmor Kesar Pista Kulfi", "brand": "Havmor", "category": "Ice Cream",
     "raw": "Concentrated Milk Solids, Sugar, Roasted Pistachio bits, Saffron, Cardamom.",
     "range": "Kulfi", "format": "Stick"},
    {"name": "Havmor Shahi Gulkand Kulfi", "brand": "Havmor", "category": "Ice Cream",
     "raw": "Milk Solids, Sugar, Gulkand, Fennel, Cardamom.",
     "range": "Kulfi", "format": "Stick"},
    # NOVELTY RANGE
    {"name": "Havmor Ice Cream Sandwich", "brand": "Havmor", "category": "Ice Cream",
     "raw": "Ice Cream: Milk Solids, Sugar. Biscuit: Wheat Flour, Sugar, Cocoa Solids, Palm Oil, Leavening Agents.",
     "range": "Novelty", "format": "Sandwich"},
    # PREMIUM RANGE
    {"name": "Havmor Rajbhog", "brand": "Havmor", "category": "Ice Cream",
     "raw": "Milk Solids, Sugar, Roasted Cashews, Almonds, Pistachios, Cardamom, Saffron, Honey, Emulsifier (E471).",
     "range": "Premium"},
    {"name": "Havmor Taj Mahal", "brand": "Havmor", "category": "Ice Cream",
     "raw": "Milk Solids, Sugar, Cashew, Almond, Pistachio, Saffron, Rose Petals, Cardamom.",
     "range": "Premium"},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. {p.get('range', 'Ice Cream')} range. Made from pure milk fat. Score: {score}/100.",
            'fssai_note': 'BIS-graded ice cream made from pure milk fat. FSSAI approved emulsifiers and stabilizers.',
            'verdict': 'Premium formulation with traditional Indian flavors' if 'Kulfi' in name or 'Rajbhog' in name or 'Taj Mahal' in name else 'Quality ice cream with approved food additives',
            'recommendation': 'Store at -18°C or below. Consume within 3 months of opening.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Havmor Ice Cream Products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
