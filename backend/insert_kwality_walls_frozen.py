"""
Insert Kwality Walls Frozen Dessert Products
Complete range of ice cream and frozen dessert registry
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['palm oil', 'vegetable fat', 'synthetic colour', 'glucose syrup', 'e122', 'e471']
_WORTH = ['cocoa solids', 'almond', 'cashew', 'nuts', 'fruit', 'cream cheese', 'cocoa butter']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'palm' in n: return 'Palm oil; saturated fat content'
        if 'vegetable fat' in n or 'vegetable oil' in n: return 'Vegetable fat base; typical in frozen desserts'
        if 'synthetic' in n or 'e122' in n or 'colour' in n: return 'Synthetic colour; permitted additive'
        if 'glucose' in n: return 'Glucose syrup; sweetening agent'
        if 'e471' in n: return 'Emulsifier; texture modifier'
    if cls == 'worth_knowing':
        if 'cocoa' in n: return 'Cocoa solids; antioxidant rich'
        if 'almond' in n: return 'Roasted almonds; protein and healthy fats'
        if 'cashew' in n: return 'Cashew nuts; mineral-rich addition'
        if 'fruit' in n or 'berry' in n or 'raspberry' in n or 'orange' in n: return 'Natural fruit ingredients'
        if 'cream cheese' in n: return 'Cream cheese; dairy-based richness'
        if 'nut' in n: return 'Nut inclusion; nutritional benefit'
    return 'Frozen dessert ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Frozen dessert with vegetable fat base; FSSAI classified'
    if cls == 'worth_knowing': return 'Natural ingredient inclusion; permitted'
    return 'Standard frozen dessert ingredient'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    return [i.strip() for i in raw.split(',') if len(i.strip()) > 2]

def _build_obj(name: str) -> dict:
    cls = _classify(name)
    return {'name': name, 'aliases': '', 'classification': cls, 'one_line_note': _note(name, cls), 'regulatory_note': _reg_note(cls)}

def _score(ingredient_objs: list) -> int:
    score = 100
    for ing in ingredient_objs:
        if ing['classification'] == 'commonly_questioned': score -= 5
        elif ing['classification'] == 'worth_knowing': score -= 1
    return max(0, min(100, score))

PRODUCTS = [
    # CORNETTO SERIES
    {"name": "Cornetto Double Chocolate", "brand": "Kwality Walls", "category": "Frozen Dessert",
     "raw": "Water, Wafer Cone (16%) [Wheat Flour, Sugar, Palm Oil, Cocoa Powder, Salt], Coating (15%) [Vegetable Fat, Sugar, Cocoa Solids, Lecithin], Sugar, Edible Vegetable Oil (Palm), Milk Solids, Glucose Syrup, Cocoa Solids, Emulsifier (E471), Stabilizers (E410, E412, E407)."},
    {"name": "Cornetto Butterscotch", "brand": "Kwality Walls", "category": "Frozen Dessert",
     "raw": "Water, Wafer Cone, Butterscotch Confectionery (12%), Sugar, Edible Vegetable Oil, Milk Solids, Butterscotch Pieces (3%), Emulsifier (E471), Stabilizers (E410, E412, E407)."},
    {"name": "Cornetto Oreo", "brand": "Kwality Walls", "category": "Frozen Dessert",
     "raw": "Water, Wafer Cone, Oreo Cookie Crumbles (10%), Sugar, Edible Vegetable Oil, Milk Solids, Glucose, Emulsifiers, Stabilizers."},
    # FEAST SERIES
    {"name": "Feast Choco Bar", "brand": "Kwality Walls", "category": "Frozen Dessert",
     "raw": "Water, Chocolate Coating (30%) [Vegetable Oil, Sugar, Cocoa Solids, E322], Sugar, Edible Vegetable Oil, Milk Solids, Wheat Crispies (3%), Emulsifier (E471), Stabilizers."},
    {"name": "Feast Cadbury Crackle", "brand": "Kwality Walls", "category": "Frozen Dessert",
     "raw": "Water, Cadbury Milk Chocolate Coating, Sugar, Vegetable Fat, Milk Solids, Rice Crispies."},
    # KULFI SERIES
    {"name": "Kulfi Pista Stick", "brand": "Kwality Walls", "category": "Frozen Dessert",
     "raw": "Water, Sugar, Milk Solids, Vegetable Oil, Pista bits, Cardamom, Emulsifiers, Stabilizers."},
    # MAGNUM SERIES
    {"name": "Magnum Classic", "brand": "Kwality Walls", "category": "Frozen Dessert",
     "raw": "Ice Cream Layer (65%): Water, Sugar, Edible Vegetable Oil, Milk Solids, Glucose Syrup, Emulsifier (E471), Stabilizers (E410, E412). Coating (35%): Milk Chocolate [Sugar, Cocoa Butter, Cocoa Solids, Milk Solids, Lecithin (E322), E476]."},
    {"name": "Magnum Almond", "brand": "Kwality Walls", "category": "Frozen Dessert",
     "raw": "Ice Cream Layer: Water, Sugar, Milk Solids, Vegetable Oil. Coating: Milk Chocolate, Roasted Almond Pieces (5%), Cocoa Butter, Cocoa Solids, Emulsifiers."},
    {"name": "Magnum Brownie", "brand": "Kwality Walls", "category": "Frozen Dessert",
     "raw": "Ice Cream Layer: Water, Sugar, Cocoa Solids. Coating: Belgian Chocolate, Brownie pieces, Cocoa Butter."},
    # PADDLE POP SERIES
    {"name": "Paddle Pop Raspberry Dolly", "brand": "Kwality Walls", "category": "Frozen Dessert",
     "raw": "Water, Sugar, Raspberry Puree (2%), Citric Acid, Stabilizers (E410, E412), Permitted Synthetic Colour (E122)."},
    {"name": "Paddle Pop Orange Bar", "brand": "Kwality Walls", "category": "Frozen Dessert",
     "raw": "Water, Sugar, Orange Juice Concentrate, Citric Acid, Stabilizers, Natural Colour (E160a)."},
    # STICKS SERIES
    {"name": "Choco Bar (Classic)", "brand": "Kwality Walls", "category": "Frozen Dessert",
     "raw": "Water, Chocolate Coating (Vegetable Fat based), Sugar, Edible Vegetable Oil, Milk Solids, Emulsifiers, Stabilizers."},
    # TUBS SERIES
    {"name": "Vanilla (Frozen Dessert)", "brand": "Kwality Walls", "category": "Frozen Dessert",
     "raw": "Water, Sugar, Edible Vegetable Oil, Milk Solids, Liquid Glucose, Emulsifier (E471), Stabilizers (E410, E412, E407). Contains Added Flavour (Nature Identical Vanilla)."},
    {"name": "Chocolate (Frozen Dessert)", "brand": "Kwality Walls", "category": "Frozen Dessert",
     "raw": "Water, Sugar, Edible Vegetable Oil, Cocoa Solids, Milk Solids, Emulsifier (E471), Stabilizers."},
    {"name": "Fruit 'n' Nut", "brand": "Kwality Walls", "category": "Frozen Dessert",
     "raw": "Water, Sugar, Edible Vegetable Oil, Milk Solids, Cashew Nuts, Raisins, Mixed Fruit bits, Emulsifier (E471), Stabilizers."},
    {"name": "Trixy Cheesecake Cup", "brand": "Kwality Walls", "category": "Frozen Dessert",
     "raw": "Water, Cheesecake Layer [Milk Solids, Cream Cheese], Cookie Crumbs, Strawberry Ripple, Sugar, Vegetable Fat."},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Frozen dessert product. Score: {score}/100. FSSAI classified frozen dessert.",
            'fssai_note': 'Frozen dessert product; uses vegetable fat base instead of milk fat per FSSAI classification.',
            'verdict': 'Standard frozen dessert' if score >= 70 else 'Contains vegetable fat and additives',
            'recommendation': 'Freeze and consume as per package directions. Enjoy in moderation.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Kwality Walls Frozen Dessert products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
