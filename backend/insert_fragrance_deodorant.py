"""
Insert Fragrance and Deodorant Registry products
Personal hygiene and fragrance formulations with phthalate analysis
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['diethyl phthalate', 'triclosan', 'denatonium benzoate']
_WORTH = ['ethyl alcohol', 'propylene glycol', 'fragrance', 'perfume']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'phthalate' in n or 'dep' in n: return 'Phthalate plasticizer; endocrine disruptor concerns'
        if 'triclosan' in n: return 'Antimicrobial; banned in several countries'
        if 'denatonium' in n: return 'Denaturant; bitter agent for denatured alcohol'
    if cls == 'worth_knowing':
        if 'ethyl alcohol' in n or 'alcohol denat' in n: return 'Denaturated alcohol; antimicrobial and preservative'
        if 'propylene glycol' in n: return 'Humectant; skin conditioning'
        if 'fragrance' in n or 'perfume' in n: return 'Fragrance compound; may contain allergens'
    return 'Personal hygiene ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Contains controlled substances; regulatory scrutiny'
    if cls == 'worth_knowing': return 'Permitted fragrance/deodorant additive'
    return 'Approved personal hygiene ingredient'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    return [i.strip() for i in raw.split(',') if len(i.strip()) > 2]

def _build_obj(name: str) -> dict:
    cls = _classify(name)
    return {'name': name, 'aliases': '', 'classification': cls, 'one_line_note': _note(name, cls), 'regulatory_note': _reg_note(cls)}

def _score(ingredient_objs: list) -> int:
    score = 100
    for ing in ingredient_objs:
        if ing['classification'] == 'commonly_questioned': score -= 12
        elif ing['classification'] == 'worth_knowing': score -= 3
    return max(0, min(100, score))

PRODUCTS = [
    {"name": "Fogg Marco Body Spray", "brand": "Fogg", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, DEP (Diethyl Phthalate), Propylene Glycol, Triclosan."},
    {"name": "Wild Stone Code Steel Body Perfume", "brand": "Wild Stone", "category": "Personal Care",
     "raw": "Ethyl Alcohol (95% v/v), Fragrance, Propylene Glycol, Diethyl Phthalate (1% w/w)."},
    {"name": "Nivea Fresh Active Deodorant (Men)", "brand": "Nivea", "category": "Personal Care",
     "raw": "Alcohol Denat., Butane, Isobutane, Propane, Perfume, Maris Limus Extract, Ostrea Shell Extract, Persea Gratissima Oil, Octyldodecanol, Aqua, Propylene Glycol."},
    {"name": "Axe Signature Dark Temptation", "brand": "Axe", "category": "Personal Care",
     "raw": "Alcohol Denat. (95% v/v), Perfume, Diethyl Phthalate, Denatonium Benzoate."},
    {"name": "Park Avenue Good Morning Body Spray", "brand": "Park Avenue", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Propellant, Perfume, Aqua, Isopropyl Myristate, Cyclomethicone, Diethyl Phthalate, Triclosan."},
    {"name": "Engage W1 Perfume Spray (Women)", "brand": "Engage", "category": "Personal Care",
     "raw": "Ethyl Alcohol (95% v/v), Perfume, Diethyl Phthalate, Denatonium Benzoate."},
    {"name": "Yardley London English Lavender Deodorant", "brand": "Yardley London", "category": "Personal Care",
     "raw": "Alcohol Denat., Butane, Isobutane, Propane, Perfume, Isopropyl Myristate, Diethyl Phthalate, Triclosan."},
    {"name": "Old Spice After Shave Lotion (Original)", "brand": "Old Spice", "category": "Personal Care",
     "raw": "Alcohol Denat., Water, Propylene Glycol, Fragrance, Benzyl Alcohol, Limonene, Linalool, Eugenol, Geraniol, Citronellol."},
    {"name": "Denver Hamilton Deodorant", "brand": "Denver", "category": "Personal Care",
     "raw": "Ethyl Alcohol Denatured, Fragrance, Aqua, Propylene Glycol, Diethyl Phthalate, Triclosan."},
    {"name": "Envy Dark Deodorant", "brand": "Envy", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, DEP, Propylene Glycol, Triclosan."},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Fragrance/deodorant product. Score: {score}/100. Contains ethanol and fragrance compounds.",
            'fssai_note': 'Personal hygiene product; contains alcohol and fragrance ingredients.',
            'verdict': 'Standard fragrance formulation' if score >= 70 else 'Contains phthalates and antimicrobials',
            'recommendation': 'Use in well-ventilated areas. Avoid prolonged skin contact.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Fragrance & Deodorant products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
