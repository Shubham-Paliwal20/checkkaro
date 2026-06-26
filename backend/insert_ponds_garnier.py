"""
Insert Pond's and Garnier Product Registry
Comprehensive ingredient and formulation breakdown from both registries
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['mineral oil', 'paraben', 'bht', 'disodium edta', 'salicylic acid', 'p-phenylenediamine']
_WORTH = ['niacinamide', 'hyaluronic acid', 'vitamin c', 'propylene glycol', 'dimethicone', 'glycolic acid']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'mineral oil' in n: return 'Mineral oil; occlusive and pore-clogging'
        if 'paraben' in n: return 'Preservative; endocrine disruptor concerns'
        if 'bht' in n: return 'Antioxidant; potential allergen'
        if 'edta' in n: return 'Chelating agent; environmental concerns'
        if 'salicylic' in n: return 'BHA exfoliant; can irritate sensitive skin'
        if 'phenylenediamine' in n: return 'Hair dye chemical; oxidative dye'
    if cls == 'worth_knowing':
        if 'niacinamide' in n: return 'Vitamin B3; pore-minimizing'
        if 'hyaluronic' in n: return 'Humectant; hydrating'
        if 'vitamin c' in n: return 'Antioxidant; brightening'
        if 'propylene glycol' in n: return 'Humectant; skin conditioning'
        if 'dimethicone' in n: return 'Silicone; texture and protection'
        if 'glycolic' in n: return 'AHA exfoliant; chemical peel'
    return 'Cosmetic or personal care ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Contains additives; regulatory concern'
    if cls == 'worth_knowing': return 'Permitted cosmetic ingredient'
    return 'Approved cosmetic ingredient'

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
        elif ing['classification'] == 'worth_knowing': score -= 2
    return max(0, min(100, score))

PRODUCTS = [
    # POND'S PRODUCTS
    {"name": "Pond's Light Moisturiser", "brand": "Pond's", "category": "Personal Care",
     "raw": "Aqua, Isopropyl Myristate, Niacinamide (Vitamin B3), Stearic Acid, Glyceryl Stearate, Mineral Oil, Ethylhexyl Methoxycinnamate, Glycerin, Cetyl Alcohol, Dimethicone, Phenoxyethanol, Potassium Hydroxide, Methylparaben, Propylparaben, Disodium EDTA, BHT."},
    {"name": "Pond's Pure Detox Face Wash", "brand": "Pond's", "category": "Personal Care",
     "raw": "Aqua, Myristic Acid, Glycerin, Stearic Acid, Potassium Hydroxide, Lauric Acid, Glycol Distearate, Decyl Glucoside, Activated Charcoal Powder, Niacinamide, Polyquaternium-7, Phenoxyethanol, Parfum."},
    {"name": "Pond's Bright Beauty Cream", "brand": "Pond's", "category": "Personal Care",
     "raw": "Aqua, Palmitic Acid, Stearic Acid, Niacinamide, Isopropyl Myristate, Ethylhexyl Methoxycinnamate, Butyl Methoxydibenzoylmethane, Sodium Ascorbyl Phosphate, Tocopheryl Acetate, Titanium Dioxide, Dimethicone."},
    {"name": "Pond's Age Miracle Eye Cream", "brand": "Pond's", "category": "Personal Care",
     "raw": "Aqua, Cyclopentasiloxane, Dimethicone Crosspolymer, Glycerin, Ethylhexyl Methoxycinnamate, Niacinamide, Retinyl Propionate (Retinol), Bisabolol, Allantoin, Tocopheryl Acetate, Palmitic Acid, Stearic Acid."},
    {"name": "Pond's Bright Beauty Serum Facial Foam", "brand": "Pond's", "category": "Personal Care",
     "raw": "Aqua, Myristic Acid, Glycerin, Stearic Acid, Potassium Hydroxide, Lauric Acid, Glycol Distearate, Niacinamide, Rosa Canina Fruit Oil, Sodium Ascorbyl Phosphate, Phenoxyethanol, Parfum."},
    {"name": "Pond's Juliet Rose Body Lotion", "brand": "Pond's", "category": "Personal Care",
     "raw": "Aqua, Isopropyl Myristate, Stearic Acid, Glyceryl Stearate, Mineral Oil, Ethylhexyl Methoxycinnamate, Niacinamide, Glycerin, Triethanolamine, Phenoxyethanol, Dimethicone, Carbomer, Parfum."},
    # GARNIER PRODUCTS
    {"name": "Garnier Bright Complete Vitamin C Serum", "brand": "Garnier", "category": "Personal Care",
     "raw": "Aqua, Glycerin, Alcohol, Dipropylene Glycol, Niacinamide, Butylene Glycol, PEG/PPG/Polybutylene Glycol-8/5/3 Glycerin, 3-O-Ethyl Ascorbic Acid (Vitamin C), Isononyl Isononanoate, Phenoxyethanol, Citrus Limon Fruit Extract."},
    {"name": "Garnier Micellar Cleansing Water", "brand": "Garnier", "category": "Personal Care",
     "raw": "Aqua, Hexylene Glycol, Glycerin, Disodium Cocoamphodiacetate, Disodium EDTA, Poloxamer 184, Polyaminopropyl Biguanide."},
    {"name": "Garnier Bright Complete Face Wash", "brand": "Garnier", "category": "Personal Care",
     "raw": "Aqua, Sorbitol, Lauric Acid, Stearic Acid, Myristic Acid, Potassium Hydroxide, Glycol Distearate, Palmitic Acid, Kaolin, Citrus Limon Fruit Extract, Salicylic Acid, Phenoxyethanol, Parfum."},
    {"name": "Garnier Fructis Long & Strong Shampoo", "brand": "Garnier", "category": "Personal Care",
     "raw": "Aqua, Sodium Laureth Sulfate, Cocamidopropyl Betaine, Sodium Lauryl Sulfate, Glycol Distearate, Sodium Chloride, Niacinamide, Saccharum Officinarum Extract, Lemon Peel Extract, Camellia Sinensis Leaf Extract, Pyridoxine HCl."},
    {"name": "Garnier Bright Complete Vitamin C Water-Gel", "brand": "Garnier", "category": "Personal Care",
     "raw": "Aqua, Glycerin, Niacinamide, Dimethicone, 3-O-Ethyl Ascorbic Acid (Vitamin C), Citrus Limon Fruit Extract, Panthenol, Adenosine, Capryloyl Salicylic Acid, Sodium Hyaluronate, Phenoxyethanol."},
    {"name": "Garnier Color Naturals (Cream Hair Color)", "brand": "Garnier", "category": "Personal Care",
     "raw": "Aqua, Cetearyl Alcohol, Ethanolamine, Ceteareth-25, Mineral Oil, p-Phenylenediamine, Resorcinol, 2,4-Diaminophenoxyethanol HCl, m-Aminophenol, Olive Fruit Oil, Avocado Oil, Shea Butter."},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Cosmetic formulation. Score: {score}/100.",
            'fssai_note': 'Personal care product with varied formulation approach.',
            'verdict': 'Standard formulation' if score >= 75 else 'Contains additives and preservatives',
            'recommendation': 'Suitable for general use. Patch test for sensitive skin.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Pond's & Garnier products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
