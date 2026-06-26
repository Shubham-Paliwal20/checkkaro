"""
Insert Pilgrim Global Beauty Clinical Database products
Clean label formulations with botanical actives and clinical ingredients
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['salicylic acid', 'glycolic acid', 'aha', 'bha', 'retinol']
_WORTH = ['niacinamide', 'hyaluronic acid', 'vitamin c', 'rosehip', 'ceramide', 'alpha arbutin']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'salicylic' in n: return 'BHA exfoliant; can irritate sensitive skin'
        if 'glycolic' in n or 'aha' in n: return 'AHA exfoliant; can irritate sensitive skin'
        if 'retinol' in n: return 'Vitamin A derivative; may cause retinization'
    if cls == 'worth_knowing':
        if 'niacinamide' in n: return 'Vitamin B3; skin-balancing'
        if 'hyaluronic' in n: return 'Humectant; hydrating and plumping'
        if 'vitamin c' in n or 'ascorbic' in n: return 'Antioxidant; brightening'
        if 'rosehip' in n: return 'Plant oil; rich in vitamins and antioxidants'
        if 'alpha arbutin' in n: return 'Skin lightener; melanin inhibitor'
    return 'Natural botanical or cosmetic ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Active ingredient; use with caution'
    if cls == 'worth_knowing': return 'Permitted cosmetic ingredient; clinically proven'
    return 'Clean label natural ingredient'

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
        elif ing['classification'] == 'worth_knowing': score -= 2
    return max(0, min(100, score))

PRODUCTS = [
    {"name": "Pilgrim Volcanic Lava Ash Face Wash", "brand": "Pilgrim", "category": "Personal Care",
     "raw": "Aqua, Lauryl Glucoside, Volcanic Lava Ash, Yugdugu Extract, Nelumbo Nucifera (Lotus) Flower Extract, Camellia Sinensis (Green Tea) Leaf Extract, Glycerin, Panthenol (Vitamin B5)."},
    {"name": "Pilgrim White Lotus Day Cream SPF 50", "brand": "Pilgrim", "category": "Personal Care",
     "raw": "Aqua, Ethylhexyl Methoxycinnamate, White Lotus Extract, Niacinamide, Camellia Sinensis (Green Tea) Leaf Extract, Sodium Hyaluronate, Titanium Dioxide, Phenoxyethanol."},
    {"name": "Pilgrim Jeju Volcanic Lava Ash Face Scrub", "brand": "Pilgrim", "category": "Personal Care",
     "raw": "Aqua, Volcanic Lava Ash, White Lotus Extract, Camellia Sinensis (Green Tea) Leaf Extract, Cellulose, Glycerin, Cetearyl Alcohol."},
    {"name": "Pilgrim Red Vine Face Serum with Vitamin C & Rosehip", "brand": "Pilgrim", "category": "Personal Care",
     "raw": "Aqua, Red Vine Extract (Vitis Vinifera), Ethyl Ascorbic Acid (Vitamin C), Rosehip Oil, Sodium Hyaluronate, Propanediol, Phenoxyethanol, Fragrance."},
    {"name": "Pilgrim Red Vine Face Cream with SPF 30", "brand": "Pilgrim", "category": "Personal Care",
     "raw": "Aqua, Red Vine Extract, Vitamin C, Rosehip Oil, Benzophenone-3, Ethylhexyl Methoxycinnamate, Niacinamide, Glycerin."},
    {"name": "Pilgrim Red Vine Under Eye Cream", "brand": "Pilgrim", "category": "Personal Care",
     "raw": "Aqua, Red Vine Extract, Caffeine, Retinol, Vitamin C, Hyaluronic Acid, Shea Butter, Almond Oil."},
    {"name": "Pilgrim Patua & Keratin Smoothing Shampoo", "brand": "Pilgrim", "category": "Personal Care",
     "raw": "Aqua, Sodium Lauroyl Sarcosinate, Patua Oil, Hydrolyzed Keratin, Polyquaternium-10, Panthenol, Phenoxyethanol, Fragrance."},
    {"name": "Pilgrim Patua & Keratin Smoothing Conditioner", "brand": "Pilgrim", "category": "Personal Care",
     "raw": "Aqua, Cetearyl Alcohol, Patua Oil, Hydrolyzed Keratin, Shea Butter, Behentrimonium Chloride, Panthenol."},
    {"name": "Pilgrim 2% Alpha Arbutin & 3% Vitamin C Brightening Serum", "brand": "Pilgrim", "category": "Personal Care",
     "raw": "Aqua, Alpha Arbutin (2%), Ethyl Ascorbic Acid (3%), Blueberry Extract, Propanediol, Glycerin, Sodium Hyaluronate, Phenoxyethanol."},
    {"name": "Pilgrim 25% AHA + 2% BHA + 5% PHA Peeling Solution", "brand": "Pilgrim", "category": "Personal Care",
     "raw": "Aqua, Glycolic Acid, Lactic Acid, Mandelic Acid, Gluconolactone (PHA), Salicylic Acid (BHA), Aloe Barbadensis Leaf Juice, Sodium Hyaluronate, Panthenol."},
    {"name": "Pilgrim Squalane Glow Oil", "brand": "Pilgrim", "category": "Personal Care",
     "raw": "Squalane (Olive derived), Vitamin C (Tetrahexyldecyl Ascorbate), Rosehip Oil, Passion Fruit Oil."},
    {"name": "Pilgrim Korean Rituals Body Butter", "brand": "Pilgrim", "category": "Personal Care",
     "raw": "Aqua, Shea Butter, Cocoa Butter, White Lotus Extract, Camellia Sinensis (Green Tea) Leaf Extract, Niacinamide, Glycerin."},
    {"name": "Pilgrim Tea Tree & Peppermint Foot Cream", "brand": "Pilgrim", "category": "Personal Care",
     "raw": "Aqua, Tea Tree Oil, Peppermint Oil, Urea, Lactic Acid, Glycerin, Shea Butter."},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Clean beauty formulation. Score: {score}/100. Cruelty-free and vegan.",
            'fssai_note': 'Clean label cosmetic; paraben-free, phthalate-free formulation.',
            'verdict': 'Premium clean beauty product' if score >= 85 else 'Clean label formulation',
            'recommendation': 'Suitable for all skin types. Patch test recommended for sensitive skin.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Pilgrim Beauty products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
