"""
Insert Loreal Paris Clinical Skincare Products
Advanced dermatological formulations and actives
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['glycolic acid', 'salicylic acid', 'bht', 'alcohol']
_WORTH = ['sodium hyaluronate', 'vitamin c', 'niacinamide', 'castor oil', 'rye seed extract']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'glycolic' in n: return 'AHA exfoliant; chemical peel'
        if 'salicylic' in n: return 'BHA exfoliant; can irritate sensitive skin'
        if 'bht' in n: return 'Antioxidant; potential allergen'
        if 'alcohol' in n: return 'Denatured alcohol; preservative'
    if cls == 'worth_knowing':
        if 'sodium hyaluronate' in n: return 'Humectant; hydrating'
        if 'vitamin c' in n: return 'Antioxidant; brightening'
        if 'niacinamide' in n: return 'Vitamin B3; balancing'
        if 'castor' in n: return 'Natural oil; emollient'
        if 'rye seed' in n: return 'Plant extract; beneficial'
    return 'Clinical skincare ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Active ingredient; professional-grade'
    if cls == 'worth_knowing': return 'Clinical skincare ingredient'
    return 'Dermatological cosmetic'

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
        elif ing['classification'] == 'worth_knowing': score -= 1
    return max(0, min(100, score))

PRODUCTS = [
    {"name": "L'Oreal Paris Revitalift 1.5% Hyaluronic Acid Serum", "brand": "L'Oreal Paris", "category": "Personal Care",
     "raw": "Aqua, Glycerin, Hydroxyethylpiperazine Ethane Sulfonic Acid, Sodium Hyaluronate, Peg-60 Hydrogenated Castor Oil, Rye Seed Extract, Calcium Pantothenate, Ascorbyl Glucoside, Phenoxyethanol."},
    {"name": "L'Oreal Paris Glycolic Bright Instant Glowing Serum", "brand": "L'Oreal Paris", "category": "Personal Care",
     "raw": "Aqua, Glycerin, Alcohol, Glycolic Acid, Ethoxydiglycol, Sodium Hyaluronate, Salicylic Acid, Adenosine, Ammonium Polyacryloyldimethyl Taurate, Phenoxyethanol."},
    {"name": "L'Oreal Paris Revitalift Crystal Micro-Essence", "brand": "L'Oreal Paris", "category": "Personal Care",
     "raw": "Aqua, Butylene Glycol, Alcohol, Hydroxyethylpiperazine Ethane Sulfonic Acid, Propanediol, Salicylic Acid, Sodium Hyaluronate, Centella Asiatica Extract."},
    {"name": "L'Oreal Paris Revitalift Hyaluronic Acid Plumping Day Cream", "brand": "L'Oreal Paris", "category": "Personal Care",
     "raw": "Aqua, Glycerin, Dimethicone, Silica, Pentylene Glycol, Adenosine, Sodium Hyaluronate, Capryloyl Salicylic Acid, Citric Acid."},
    {"name": "L'Oreal Paris Glycolic Bright Glowing Day Cream SPF 17", "brand": "L'Oreal Paris", "category": "Personal Care",
     "raw": "Aqua, Ethylhexyl Methoxycinnamate, Glycerin, Isohexadecane, Glycolic Acid, Titanium Dioxide, BHT, Vitamin C Glocoside."},
    {"name": "L'Oreal Paris Glycolic Bright Glowing Night Cream", "brand": "L'Oreal Paris", "category": "Personal Care",
     "raw": "Aqua, Glycerin, Niacinamide, Glycolic Acid, Ammonium Polyacryloyldimethyl Taurate, Ascorbyl Glucoside, Sodium Hyaluronate."},
    {"name": "L'Oreal Paris Revitalift Night Cream", "brand": "L'Oreal Paris", "category": "Personal Care",
     "raw": "Aqua, Glycerin, Prunus Armeniaca Kernel Oil, Stearic Acid, Palmitic Acid, Retinyl Palmitate, Hydrolyzed Soy Protein, Acetyl Trifluoromethylphenyl Valylglycine."},
    {"name": "L'Oreal Paris Extraordinary Oil Serum", "brand": "L'Oreal Paris", "category": "Personal Care",
     "raw": "Cyclopentasiloxane, Dimethiconol, Chamomilla Recutita Flower Extract, Cocos Nucifera Oil, Helianthus Annuus Seed Oil, Nelumbo Nucifera Flower Extract."},
    {"name": "L'Oreal Paris Hyaluron Moisture 72H Hydrating Shampoo", "brand": "L'Oreal Paris", "category": "Personal Care",
     "raw": "Aqua, Sodium Laureth Sulfate, Glycol Distearate, Sodium Hyaluronate, Cocamidopropyl Betaine, Dimethicone, Guar Hydroxypropyltrimonium Chloride, Salicylic Acid."},
    {"name": "L'Oreal Paris Hyaluron Moisture 72H Hydrating Conditioner", "brand": "L'Oreal Paris", "category": "Personal Care",
     "raw": "Aqua, Cetearyl Alcohol, Dimethicone, Glycerin, Behentrimonium Chloride, Sodium Hyaluronate, Lactic Acid, Amodimethicone."},
    {"name": "L'Oreal Paris Total Repair 5 Shampoo", "brand": "L'Oreal Paris", "category": "Personal Care",
     "raw": "Aqua, Sodium Laureth Sulfate, Coco-Betaine, Dimethicone, Glycol Distearate, Sodium Chloride, Salicylic Acid, Ceramide, Arginine."},
    {"name": "L'Oreal Paris Total Repair 5 Conditioner", "brand": "L'Oreal Paris", "category": "Personal Care",
     "raw": "Aqua, Cetearyl Alcohol, Behentrimonium Chloride, Cetyl Esters, Lactic Acid, Trideceth-6, Chlorhexidine Digluconate."},
    {"name": "L'Oreal Paris 6 Oil Nourish Shampoo", "brand": "L'Oreal Paris", "category": "Personal Care",
     "raw": "Aqua, Sodium Laureth Sulfate, Argania Spinosa Kernel Oil, Cocos Nucifera Oil, Helianthus Annuus Seed Oil, Salicylic Acid."},
    {"name": "L'Oreal Paris 6 Oil Nourish Conditioner", "brand": "L'Oreal Paris", "category": "Personal Care",
     "raw": "Aqua, Cetearyl Alcohol, Behentrimonium Chloride, Amodimethicone, Trideceth-6, Argania Spinosa Kernel Oil."},
    {"name": "L'Oreal Paris Dream Lengths Restoring Shampoo", "brand": "L'Oreal Paris", "category": "Personal Care",
     "raw": "Aqua, Sodium Laureth Sulfate, Sodium Chloride, Ricinus Communis Seed Oil (Castor Oil), Niacinamide, Panthenol, Hydrolyzed Wheat Protein."},
    {"name": "L'Oreal Paris Dream Lengths No Haircut Cream", "brand": "L'Oreal Paris", "category": "Personal Care",
     "raw": "Aqua, Cyclopentasiloxane, Propylene Glycol, Niacinamide, Panthenol, Hydrolyzed Corn Protein, Hydrolyzed Soy Protein."},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Clinical skincare. Score: {score}/100. Dermatologically tested formulation.",
            'fssai_note': 'Advanced skincare with clinical-grade actives.',
            'verdict': 'Clinical skincare product' if score >= 85 else 'Active formulation',
            'recommendation': 'Contains active ingredients. Introduce gradually. Use sunscreen during day. Patch test recommended.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} L'Oreal Paris products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
