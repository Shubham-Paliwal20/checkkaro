"""
Insert Indian Soap Portfolio - Volume II
Premium and specialty soap products
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['sodium palmate', 'palm kernel', 'detergent', 'pcmx', 'triclocarban', 'edta']
_WORTH = ['neem', 'turmeric', 'sandalwood', 'aloe vera', 'tulsi', 'tea tree', 'herbal', 'natural oil']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'palmate' in n or 'palm' in n: return 'Palm-derived fatty acid base'
        if 'edta' in n or 'tetrasodium' in n: return 'Chelating agent; helps lather formation'
        if 'pcmx' in n: return 'PCMX antiseptic; antimicrobial agent'
        if 'detergent' in n: return 'Synthetic detergent base'
    if cls == 'worth_knowing':
        if 'neem' in n: return 'Neem oil; antibacterial and traditional remedy'
        if 'turmeric' in n: return 'Turmeric; anti-inflammatory spice'
        if 'sandalwood' in n: return 'Sandalwood; aromatic and soothing'
        if 'aloe' in n: return 'Aloe vera; soothing botanical'
        if 'tulsi' in n: return 'Tulsi/Holy Basil; traditional herb'
        if 'tea tree' in n: return 'Tea tree oil; antimicrobial properties'
        if 'herbal' in n or 'oil' in n: return 'Natural/herbal ingredients'
        if 'glycerin' in n: return 'Glycerin; moisturizing humectant'
    return 'Traditional soap ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Contains synthetic detergent base; BIS-approved toilet soap'
    if cls == 'worth_knowing': return 'Contains natural/herbal ingredients; permitted'
    return 'BIS-graded toilet soap ingredient'

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
        elif ing['classification'] == 'worth_knowing': score -= 2
    return max(0, min(100, score))

PRODUCTS = [
    {"name": "Liril Lemon & Tea Tree", "brand": "Hindustan Unilever", "category": "Personal Care",
     "raw": "Sodium Palmate, Water, Sodium Palm Kernelate, Glycerin, Perfume, Sodium Chloride, Lemon Peel Extract, Tea Tree Oil, Tetrasodium EDTA.",
     "grade": "Grade 2", "note": "Freshness Soap"},
    {"name": "Hamam Neem, Tulsi & Aloe Vera", "brand": "Hindustan Unilever", "category": "Personal Care",
     "raw": "Sodium Palmate, Sodium Palm Kernelate, Neem Oil, Tulsi Extract, Aloe Vera Extract, Camphor, Tetrasodium EDTA.",
     "grade": "Grade 3", "note": "Protection Soap"},
    {"name": "Santoor Aloe Fresh", "brand": "Wipro Consumer Care", "category": "Personal Care",
     "raw": "Sodium Palmate, Sodium Palm Kernelate, Water, Aloe Vera Extract, Lime Peel Extract, Hydrated Magnesium Silicate.",
     "grade": "Grade 2", "note": "Moisturizing Soap"},
    {"name": "Park Avenue Cool Blue", "brand": "Raymond Consumer Care", "category": "Personal Care",
     "raw": "Sodium Palmate, Sodium Palm Kernelate, Menthol, Multi-mineral salts, Fragrance, Glycerin.",
     "grade": "Grade 1", "note": "Fragrance Soap"},
    {"name": "Khadi Natural Sandalwood", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Sandalwood Oil, Glycerin, Vegetable Oils, Aloe Vera Extract, Reetha, Purified Water.",
     "grade": "Handmade", "note": "Handmade Soap"},
    {"name": "Vivel Aloe Vera", "brand": "ITC Limited", "category": "Personal Care",
     "raw": "Sodium Palmate, Sodium Palm Kernelate, Water, Vitamin E, Aloe Vera Extract, Milk Cream.",
     "grade": "Grade 2", "note": "Softness Soap"},
    {"name": "Savlon Glycerin Soap", "brand": "ITC Limited", "category": "Personal Care",
     "raw": "Sodium Palmate, Sodium Palm Kernelate, Glycerin, PCMX (Antiseptic), Fragrance.",
     "grade": "Glycerin-based", "note": "Germ Protection"},
    {"name": "Lifebuoy Neem & Aloe Vera", "brand": "Hindustan Unilever", "category": "Personal Care",
     "raw": "Sodium Palmate, Water, Sodium Palm Kernelate, Neem Extract, Aloe Vera Extract, Silver Oxide.",
     "grade": "Grade 3", "note": "Hygiene Soap"},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. {p['note']}. {p['grade']}. Score: {score}/100.",
            'fssai_note': f"BIS-certified toilet soap ({p['grade']}). {p['note']} formulation.",
            'verdict': 'Premium toilet soap formulation' if score >= 75 else 'Standard soap with traditional additives',
            'recommendation': 'Use daily for personal hygiene. Suitable for all skin types. Follow package directions.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Indian Soap Portfolio products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
