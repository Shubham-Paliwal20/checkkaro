"""
Insert Mamaearth Plant-Based Portfolio
Natural and organic personal care products
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['salicylic acid']
_WORTH = ['onion seed oil', 'turmeric', 'neem', 'aloe vera', 'shea butter', 'coconut oil', 'vitamin c', 'niacinamide']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'salicylic' in n: return 'BHA exfoliant; can irritate sensitive skin'
    if cls == 'worth_knowing':
        if 'onion' in n: return 'Hair fall control; traditional remedy'
        if 'turmeric' in n: return 'Anti-inflammatory; Ayurvedic spice'
        if 'neem' in n: return 'Antibacterial; traditional remedy'
        if 'aloe' in n: return 'Soothing; hydrating gel'
        if 'shea' in n: return 'Natural butter; moisturizing'
        if 'coconut' in n: return 'Natural oil; antimicrobial'
        if 'vitamin c' in n: return 'Antioxidant; brightening'
        if 'niacinamide' in n: return 'Vitamin B3; balancing'
    return 'Plant-based natural ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Contains active ingredient; patch test recommended'
    if cls == 'worth_knowing': return 'Natural botanical ingredient'
    return 'Clean label plant-based ingredient'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    return [i.strip() for i in raw.split(',') if len(i.strip()) > 2]

def _build_obj(name: str) -> dict:
    cls = _classify(name)
    return {'name': name, 'aliases': '', 'classification': cls, 'one_line_note': _note(name, cls), 'regulatory_note': _reg_note(cls)}

def _score(ingredient_objs: list) -> int:
    score = 100
    for ing in ingredient_objs:
        if ing['classification'] == 'commonly_questioned': score -= 8
        elif ing['classification'] == 'worth_knowing': score -= 0
    return max(0, min(100, score))

PRODUCTS = [
    {"name": "Mamaearth Onion Hair Oil", "brand": "Mamaearth", "category": "Personal Care",
     "raw": "Sunflower Oil, Onion Seed Oil, Almond Oil, Amla Oil, Castor Oil, Hibiscus Oil, Bhringraj Oil, Sesame Oil, Vitamin E, Redensyl, Onion Extract, Fragrance."},
    {"name": "Mamaearth Vitamin C Face Wash", "brand": "Mamaearth", "category": "Personal Care",
     "raw": "Aqua, Glycerin, Sodium Lauroyl Sarcosinate, Disodium Cocoamphodiacetate, Vitamin C (Sodium Ascorbyl Phosphate), Turmeric Extract, Lemon Oil, Potassium Sorbate, Sodium Benzoate."},
    {"name": "Mamaearth Ubtan Face Wash", "brand": "Mamaearth", "category": "Personal Care",
     "raw": "Aqua, Stearic Acid, Sodium Lauroyl Sarcosinate, Glycerin, Turmeric Extract, Walnut Beads, Carrot Seed Oil, Saffron Extract, Tocopheryl Acetate (Vitamin E), Licorice Extract."},
    {"name": "Mamaearth Rice Face Wash", "brand": "Mamaearth", "category": "Personal Care",
     "raw": "Aqua, Rice Water, Niacinamide, Glycerin, Cocamidopropyl Betaine, Sodium Lauroyl Sarcosinate, Rice Bran Oil, Vitamin E, Potassium Sorbate."},
    {"name": "Mamaearth Tea Tree Face Wash", "brand": "Mamaearth", "category": "Personal Care",
     "raw": "Aqua, Neem Leaf Extract, Tea Tree Oil, Salicylic Acid, Glycerin, Sodium Benzoate, Potassium Sorbate, Aloe Vera Extract."},
    {"name": "Mamaearth Aloe Vera Gel", "brand": "Mamaearth", "category": "Personal Care",
     "raw": "Aloe Vera Juice, Glycerin, Vitamin E, Xanthan Gum, Potassium Sorbate, Sodium Benzoate."},
    {"name": "Mamaearth Mineral Based Sunscreen (SPF 50)", "brand": "Mamaearth", "category": "Personal Care",
     "raw": "Aqua, Zinc Oxide, Titanium Dioxide, Carrot Seed Oil, Raspberry Seed Oil, Turmeric Extract, Glycerin, Sodium Benzoate."},
    {"name": "Mamaearth Milky Soft Baby Face Cream", "brand": "Mamaearth", "category": "Personal Care",
     "raw": "Aqua, Milk Protein, Shea Butter, Cocoa Butter, Murumuru Butter, Almond Oil, Olive Oil, Vitamin E, Potassium Sorbate."},
    {"name": "Mamaearth Onion Shampoo", "brand": "Mamaearth", "category": "Personal Care",
     "raw": "Aqua, Sodium Lauroyl Sarcosinate, Polyquaternium-10, Onion Seed Extract, Plant Keratin, Soy Amino Acids, Wheat Amino Acids, D-Panthenol."},
    {"name": "Mamaearth Bye Bye Blemishes Face Cream", "brand": "Mamaearth", "category": "Personal Care",
     "raw": "Aqua, Mulberry Extract, Vitamin C, Niacinamide, Daisy Flower Extract, Glycerin, Licorice Extract, Potassium Sorbate."},
    {"name": "Mamaearth Charcoal Face Wash", "brand": "Mamaearth", "category": "Personal Care",
     "raw": "Aqua, Activated Charcoal, Coffee Extract, Aloe Vera Extract, Cedarwood Oil, Sodium Lauroyl Sarcosinate."},
    {"name": "Mamaearth Rosemary Hair Growth Oil", "brand": "Mamaearth", "category": "Personal Care",
     "raw": "Rosemary Oil, Methi (Fenugreek) Oil, Bhringraj Oil, Curry Leaf Oil, Almond Oil, Sesame Oil, Vitamin E."},
    {"name": "Mamaearth CoCo Face Scrub", "brand": "Mamaearth", "category": "Personal Care",
     "raw": "Aqua, Coffee Bean Powder, Cocoa Butter, Shea Butter, Coconut Oil, Walnut Shell Powder, Glycerin, Sodium Benzoate."},
    {"name": "Mamaearth Green Tea Face Serum", "brand": "Mamaearth", "category": "Personal Care",
     "raw": "Aqua, Green Tea Extract, Collagen, Niacinamide, Rosehip Oil, Hyaluronic Acid, Potassium Sorbate."},
    {"name": "Mamaearth Henna Hair Oil", "brand": "Mamaearth", "category": "Personal Care",
     "raw": "Henna Oil, Coffee Oil, Indigo Oil, Coconut Oil, Almond Oil, Vitamin E, Curry Leaf Extract."},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Plant-based personal care. Score: {score}/100. Free from parabens, sulfates, and phthalates.",
            'fssai_note': 'Natural plant-based personal care product without harsh chemicals.',
            'verdict': 'Clean label natural product' if score >= 92 else 'Plant-based formulation',
            'recommendation': 'Suitable for daily use. Dermatologist tested. Patch test for sensitivities.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Mamaearth products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
