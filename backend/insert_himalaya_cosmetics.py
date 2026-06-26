"""
Insert Himalaya Wellness Ayurvedic Personal Care & Pharmaceutical
Traditional herbs and natural wellness products
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['talc', 'sodium laureth sulfate', 'ammonium lauryl sulfate', 'zinc pyrithione']
_WORTH = ['neem', 'turmeric', 'aloe vera', 'honey', 'walnut', 'tea tree oil', 'niacinamide']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'talc' in n: return 'Talc powder; inhalation concerns'
        if 'sodium laureth' in n or 'ammonium lauryl' in n: return 'Surfactant; can strip oils'
        if 'zinc pyrithione' in n: return 'Antifungal; may cause irritation'
    if cls == 'worth_knowing':
        if 'neem' in n: return 'Antibacterial; traditional remedy'
        if 'turmeric' in n: return 'Anti-inflammatory; Ayurvedic spice'
        if 'aloe' in n: return 'Soothing; hydrating gel'
        if 'honey' in n: return 'Natural humectant; antibacterial'
        if 'walnut' in n: return 'Natural exfoliant; gentle scrub'
        if 'tea tree' in n: return 'Antifungal; antibacterial oil'
        if 'niacinamide' in n: return 'Vitamin B3; balancing'
    return 'Ayurvedic natural ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Contains additives; Ayurvedic formulation'
    if cls == 'worth_knowing': return 'Traditional herbal ingredient'
    return 'Ayurvedic wellness product'

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
    {"name": "Himalaya Purifying Neem Face Wash", "brand": "Himalaya", "category": "Personal Care",
     "raw": "Aqua, Ammonium Lauryl Sulfate, Melia Azadirachta (Neem) Leaf Extract, Cocamidopropyl Betaine, Sodium Cocoyl Glycinate, Glycerin, Turmeric Extract."},
    {"name": "Himalaya Aloe Vera Face Wash", "brand": "Himalaya", "category": "Personal Care",
     "raw": "Aqua, Ammonium Lauryl Sulfate, Aloe Barbadensis Leaf Extract, Cocamidopropyl Betaine, Glycerin, Sodium Cocoyl Glycinate."},
    {"name": "Himalaya Tan Removal Orange Face Wash", "brand": "Himalaya", "category": "Personal Care",
     "raw": "Aqua, Orange Peel Extract, Papain, Honey, Glycerin, Ammonium Lauryl Sulfate."},
    {"name": "Himalaya Oil Clear Lemon Face Wash", "brand": "Himalaya", "category": "Personal Care",
     "raw": "Aqua, Lemon Peel Extract, Honey, Ammonium Lauryl Sulfate, Cocamidopropyl Betaine, Glycerin."},
    {"name": "Himalaya Gentle Exfoliating Walnut Scrub", "brand": "Himalaya", "category": "Personal Care",
     "raw": "Aqua, Walnut Shell Powder, Apple Fruit Extract, Wheat Germ Oil, Glycerin, Stearic Acid."},
    {"name": "Himalaya Anti-Hair Fall Shampoo", "brand": "Himalaya", "category": "Personal Care",
     "raw": "Aqua, Sodium Laureth Sulfate, Butea Monosperma Flower Extract, Eclipta Prostrata Extract, Bhringaraja, Palasha flower extract."},
    {"name": "Himalaya Anti-Dandruff Tea Tree Shampoo", "brand": "Himalaya", "category": "Personal Care",
     "raw": "Aqua, Tea Tree Oil, Rosemary Leaf Oil, Zinc Pyrithione, Grape Seed Extract, Aloe Vera."},
    {"name": "Himalaya Complete Care Toothpaste", "brand": "Himalaya", "category": "Personal Care",
     "raw": "Sorbitol, Hydrated Silica, Pomegranate Pericarp Extract, Neem Bark Extract, Acacia Arabica Extract, Terminalia Chebula."},
    {"name": "Himalaya Sparkly White Toothpaste", "brand": "Himalaya", "category": "Personal Care",
     "raw": "Sorbitol, Silica, Papain, Bromelain, Miswak Extract, Clove Oil."},
    {"name": "Himalaya Baby Powder", "brand": "Himalaya", "category": "Personal Care",
     "raw": "Talc, Zinc Oxide, Olive Oil, Sweet Almond Oil, Vetiver Root Extract."},
    {"name": "Himalaya Baby Gentle Wash", "brand": "Himalaya", "category": "Personal Care",
     "raw": "Aqua, Green Gram Extract, Chickpea Extract, Fenugreek Extract, Sodium Coco-Sulfate."},
    {"name": "Himalaya Clear Complexion Whitening Day Cream", "brand": "Himalaya", "category": "Personal Care",
     "raw": "Aqua, Licorice Extract, White Dammar Extract, Spiked Ginger Lily, Greater Galangal."},
    {"name": "Himalaya Anti-Wrinkle Cream", "brand": "Himalaya", "category": "Personal Care",
     "raw": "Aqua, Aloe Vera, Grapes, Poppy Seeds, Lemon, Sandalwood Tree Extract."},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Ayurvedic personal care. Score: {score}/100. Traditional herbal formulation.",
            'fssai_note': 'Ayurvedic wellness product with natural herbs.',
            'verdict': 'Traditional herbal product' if score >= 92 else 'Ayurvedic formulation',
            'recommendation': 'Suitable for daily use. Gentle formula. Patch test recommended.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Himalaya Wellness cosmetic products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
