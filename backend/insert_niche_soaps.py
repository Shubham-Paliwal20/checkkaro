"""
Insert Niche and Artisanal Soap Brands
Handcrafted and herbal soap registry
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['sodium lauryl sulfate', 'parabens', 'synthetic fragrance']
_WORTH = ['shea butter', 'coconut oil', 'olive oil', 'neem', 'turmeric', 'honey', 'charcoal', 'herbal extract']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'sodium lauryl sulfate' in n: return 'SLS surfactant; can strip natural oils'
        if 'parabens' in n: return 'Preservative; endocrine concerns'
        if 'synthetic fragrance' in n: return 'Synthetic scent; potential irritant'
    if cls == 'worth_knowing':
        if 'shea butter' in n: return 'Natural moisturizer; rich in fatty acids'
        if 'coconut oil' in n: return 'Natural oil; antimicrobial properties'
        if 'olive oil' in n: return 'Natural oil; emollient and nourishing'
        if 'neem' in n: return 'Antibacterial; traditional remedy'
        if 'turmeric' in n: return 'Anti-inflammatory; Ayurvedic spice'
        if 'honey' in n: return 'Natural humectant; antibacterial'
        if 'charcoal' in n: return 'Detoxifying; purifying ingredient'
        if 'herbal' in n or 'extract' in n: return 'Plant-based ingredient'
    return 'Natural soap ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Contains additives; artisanal formulation'
    if cls == 'worth_knowing': return 'Natural and herbal ingredients'
    return 'Handcrafted natural soap'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    return [i.strip() for i in raw.split(',') if len(i.strip()) > 2]

def _build_obj(name: str) -> dict:
    cls = _classify(name)
    return {'name': name, 'aliases': '', 'classification': cls, 'one_line_note': _note(name, cls), 'regulatory_note': _reg_note(cls)}

def _score(ingredient_objs: list) -> int:
    score = 100
    for ing in ingredient_objs:
        if ing['classification'] == 'commonly_questioned': score -= 10
        elif ing['classification'] == 'worth_knowing': score -= 0
    return max(0, min(100, score))

PRODUCTS = [
    {"name": "Tedibar Turmeric & Honey Soap", "brand": "Tedibar", "category": "Personal Care",
     "raw": "Coconut Oil, Palm Oil, Turmeric Extract, Honey, Shea Butter, Neem Oil, Natural Fragrance."},
    {"name": "Rustic Art Activated Charcoal Soap", "brand": "Rustic Art", "category": "Personal Care",
     "raw": "Activated Charcoal, Coconut Oil, Olive Oil, Shea Butter, Tea Tree Oil, Eucalyptus Essential Oil."},
    {"name": "Seamed Goat Milk & Oat Soap", "brand": "Seamed", "category": "Personal Care",
     "raw": "Goat Milk, Oat Flour, Coconut Oil, Shea Butter, Olive Oil, Almond Oil, Lavender Essential Oil."},
    {"name": "Juicy Chemistry Neem & Tulsi Soap", "brand": "Juicy Chemistry", "category": "Personal Care",
     "raw": "Neem Oil, Tulsi Extract, Coconut Oil, Olive Oil, Shea Butter, Tea Tree Oil, Natural Fragrance."},
    {"name": "Neev Herbal Multani Mitti Soap", "brand": "Neev Herbal", "category": "Personal Care",
     "raw": "Multani Mitti Clay, Coconut Oil, Olive Oil, Shea Butter, Turmeric Extract, Aloe Vera, Honey."},
    {"name": "Ancient Living Ubtan Soap", "brand": "Ancient Living", "category": "Personal Care",
     "raw": "Turmeric, Sandalwood, Rose Petal, Coconut Oil, Olive Oil, Shea Butter, Neem Extract, Honey."},
    {"name": "Ethiglo Ayurvedic Herbal Soap", "brand": "Ethiglo", "category": "Personal Care",
     "raw": "Ayurvedic Herb Extract, Neem, Turmeric, Coconut Oil, Olive Oil, Shea Butter, Aloe Vera, Honey."},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Natural artisanal soap. Score: {score}/100. Handcrafted herbal formula.",
            'fssai_note': 'Artisanal herbal soap with natural ingredients.',
            'verdict': 'Natural herbal soap' if score >= 90 else 'Handcrafted natural formulation',
            'recommendation': 'Gentle on skin. Suitable for regular use. Patch test for sensitivities.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} niche and artisanal soaps...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
