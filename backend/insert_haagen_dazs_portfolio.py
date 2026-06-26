"""
Insert Haagen-Dazs Premium Ice Cream Portfolio
Ultra-Premium Luxury Formulation with Clean Label Approach
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['soy lecithin', 'emulsifier', 'artificial flavor']
_WORTH = ['fresh cream', 'egg yolk', 'natural flavor', 'real fruit', 'nuts', 'chocolate', 'vanilla']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'soy lecithin' in n: return 'Soy lecithin; natural emulsifier'
    if cls == 'worth_knowing':
        if 'cream' in n or 'fresh' in n: return 'High fresh cream content; ultra-premium formulation'
        if 'egg' in n or 'yolk' in n: return 'Egg yolk; natural emulsifier for creaminess'
        if 'fruit' in n or 'strawberry' in n or 'mango' in n: return 'Real fruit puree; natural flavor'
        if 'nut' in n or 'almond' in n or 'macadamia' in n: return 'Premium roasted nuts; artisanal ingredient'
        if 'chocolate' in n: return 'Belgian chocolate; premium cacao sourcing'
    return 'Ultra-premium ice cream ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Natural emulsifier; clean label formulation'
    if cls == 'worth_knowing': return 'Premium natural ingredients; minimal additives; ultra-premium density'
    return 'Haagen-Dazs ultra-premium product'

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
        elif ing['classification'] == 'worth_knowing': score -= 0
    return max(0, min(100, score))

PRODUCTS = [
    # CHOCOLATE & NUTTY
    {"name": "Haagen-Dazs Pralines & Cream", "brand": "Haagen-Dazs", "category": "Ice Cream",
     "raw": "Fresh Cream, Condensed Skimmed Milk, Sugar, Caramel Swirl, Praline Pecans, Egg Yolk.",
     "type": "Ultra-Premium Ice Cream", "format": "Pint"},
    {"name": "Haagen-Dazs Dulce de Leche", "brand": "Haagen-Dazs", "category": "Ice Cream",
     "raw": "Fresh Cream, Condensed Skimmed Milk, Sugar, Dulce de Leche Swirl, Egg Yolk.",
     "type": "Ultra-Premium Ice Cream", "format": "Pint"},
    # CLASSIC FLAVOURS
    {"name": "Haagen-Dazs Vanilla", "brand": "Haagen-Dazs", "category": "Ice Cream",
     "raw": "Fresh Cream, Condensed Skimmed Milk, Sugar, Water, Egg Yolk, Natural Vanilla Flavouring.",
     "type": "Ultra-Premium Ice Cream", "format": "Pint", "clean_label": True},
    {"name": "Haagen-Dazs Belgian Chocolate", "brand": "Haagen-Dazs", "category": "Ice Cream",
     "raw": "Fresh Cream, Condensed Skimmed Milk, Sugar, Water, Belgian Chocolate, Chocolate Chunks, Egg Yolk, Cocoa Powder.",
     "type": "Ultra-Premium Ice Cream", "format": "Pint"},
    {"name": "Haagen-Dazs Strawberry", "brand": "Haagen-Dazs", "category": "Ice Cream",
     "raw": "Fresh Cream, Condensed Skimmed Milk, Strawberries, Sugar, Egg Yolk.",
     "type": "Ultra-Premium Ice Cream", "format": "Pint"},
    {"name": "Haagen-Dazs Macadamia Nut Brittle", "brand": "Haagen-Dazs", "category": "Ice Cream",
     "raw": "Fresh Cream, Condensed Skimmed Milk, Sugar, Water, Macadamia Nut Brittle, Egg Yolk, Natural Vanilla Flavouring.",
     "type": "Ultra-Premium Ice Cream", "format": "Pint"},
    {"name": "Haagen-Dazs Cookies & Cream", "brand": "Haagen-Dazs", "category": "Ice Cream",
     "raw": "Fresh Cream, Condensed Skimmed Milk, Sugar, Water, Cookie Pieces, Egg Yolk, Natural Vanilla Flavouring.",
     "type": "Ultra-Premium Ice Cream", "format": "Pint"},
    {"name": "Haagen-Dazs Caramel Biscuit & Cream", "brand": "Haagen-Dazs", "category": "Ice Cream",
     "raw": "Fresh Cream, Condensed Skimmed Milk, Sugar, Water, Caramel Biscuit, Speculoos Paste, Egg Yolk, Salt.",
     "type": "Ultra-Premium Ice Cream", "format": "Pint"},
    # EXOTIC & FRUIT
    {"name": "Haagen-Dazs Mango & Raspberry", "brand": "Haagen-Dazs", "category": "Ice Cream",
     "raw": "Fresh Cream, Condensed Skimmed Milk, Mango Puree, Raspberry Ripple, Sugar, Water, Egg Yolk, Orange Juice Concentrate, Lemon Juice Concentrate.",
     "type": "Ultra-Premium Ice Cream", "format": "Pint"},
    {"name": "Haagen-Dazs Blueberries & Cream", "brand": "Haagen-Dazs", "category": "Ice Cream",
     "raw": "Fresh Cream, Condensed Skimmed Milk, Sugar, Blueberry Preparation, Egg Yolk.",
     "type": "Ultra-Premium Ice Cream", "format": "Pint"},
    # STICKS & BARS
    {"name": "Haagen-Dazs Vanilla Caramel Almond Stick", "brand": "Haagen-Dazs", "category": "Ice Cream",
     "raw": "Vanilla Ice Cream, Belgian Milk Chocolate, Roasted Almonds, Caramel Swirl.",
     "type": "Ultra-Premium Stick", "format": "Bar"},
    {"name": "Haagen-Dazs Salted Caramel Stick", "brand": "Haagen-Dazs", "category": "Ice Cream",
     "raw": "Caramel Ice Cream, Belgian Milk Chocolate, Salted Caramel Pieces.",
     "type": "Ultra-Premium Stick", "format": "Bar"},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. {p['type']}. {p.get('format', '')}. Clean label ultra-premium formulation. Score: {score}/100.",
            'fssai_note': 'Ultra-premium ice cream with minimal air (overrun). No synthetic emulsifiers or vegetable fats. Clean label approach.',
            'verdict': 'Ultra-premium luxury formulation with real cream, egg yolks, and premium ingredients' if score >= 95 else 'Premium ice cream with high-quality natural ingredients',
            'recommendation': 'Serve at -15°C for optimal texture and flavor. Part of Haagen-Dazs ultra-premium selection.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Haagen-Dazs Ultra-Premium Products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
