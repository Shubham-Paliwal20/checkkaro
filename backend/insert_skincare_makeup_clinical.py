"""
Insert Skincare and Makeup Clinical Registry products
Active ingredients and clinical formulations from multiple brands
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['salicylic acid', 'retinol', 'glycolic acid', 'paraben']
_WORTH = ['niacinamide', 'hyaluronic acid', 'ceramide', 'propylene glycol', 'cyclopentasiloxane', 'dimethicone', 'phenoxyethanol']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'salicylic acid' in n: return 'BHA exfoliant; can irritate sensitive skin'
        if 'retinol' in n: return 'Vitamin A derivative; may cause retinization'
        if 'glycolic acid' in n: return 'AHA exfoliant; can irritate sensitive skin'
        if 'paraben' in n: return 'Preservative; endocrine disruptor concerns'
    if cls == 'worth_knowing':
        if 'niacinamide' in n: return 'Vitamin B3; skin-balancing and pore-minimizing'
        if 'hyaluronic acid' in n: return 'Humectant; hydrating and plumping'
        if 'ceramide' in n: return 'Lipid barrier repair; essential for skin health'
        if 'propylene glycol' in n: return 'Humectant; skin conditioning'
        if 'cyclopentasiloxane' in n or 'dimethicone' in n: return 'Silicone; texture and wear'
        if 'phenoxyethanol' in n: return 'Preservative; safe at regulated levels'
    return 'Natural botanical or recognized cosmetic ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Active ingredient; use with caution'
    if cls == 'worth_knowing': return 'Permitted cosmetic ingredient; safe'
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
        if ing['classification'] == 'commonly_questioned': score -= 10
        elif ing['classification'] == 'worth_knowing': score -= 2
    return max(0, min(100, score))

PRODUCTS = [
    # CETAPHIL
    {"name": "Cetaphil Gentle Skin Cleanser", "brand": "Cetaphil", "category": "Personal Care",
     "raw": "Aqua, Cetyl Alcohol, Propylene Glycol, Sodium Lauryl Sulfate, Stearyl Alcohol, Methylparaben, Propylparaben, Butylparaben."},
    {"name": "Cetaphil Moisturising Cream", "brand": "Cetaphil", "category": "Personal Care",
     "raw": "Aqua, Glycerin, Petrolatum, Dicaprylyl Ether, Dimethicone, Glyceryl Stearate, Cetyl Alcohol, Helianthus Annuus Seed Oil, PEG-30 Stearate, Tocopheryl Acetate."},
    {"name": "Cetaphil Oily Skin Cleanser", "brand": "Cetaphil", "category": "Personal Care",
     "raw": "Aqua, Cetyl Alcohol, PEG-7 Glyceryl Cocoate, Sodium Laureth Sulfate, Panthenol, Glycerin, Methylparaben, Propylparaben."},
    # MINIMALIST
    {"name": "Minimalist Niacinamide 10% + Zinc", "brand": "Minimalist", "category": "Personal Care",
     "raw": "Aloe Vera Juice, Niacinamide (10%), Propylene Glycol, Dimethyl Isosorbide, Zinc PCA, Ethoxydiglycol, Phenoxyethanol, Sodium Hyaluronate, Pullulan."},
    {"name": "Minimalist Salicylic Acid 2%", "brand": "Minimalist", "category": "Personal Care",
     "raw": "Aloe Vera Juice, Ethoxydiglycol, Salicylic Acid (2%), Dimethyl Isosorbide, Propylene Glycol, Sodium Hyaluronate, Phenoxyethanol."},
    {"name": "Minimalist Retinol 0.3% + Q10", "brand": "Minimalist", "category": "Personal Care",
     "raw": "Caprylic/Capric Triglyceride, Isododecane, Squalane, Retinol (0.3%), Coenzyme Q10, Tocopheryl Acetate."},
    # AQUALOGICA
    {"name": "Aqualogica Radiance+ Dewy Sunscreen", "brand": "Aqualogica", "category": "Personal Care",
     "raw": "Aqua, Suncat MTA, Niacinamide, Watermelon Fruit Extract, Hyaluronic Acid, Glycerin, Aloe Vera Juice, Zinc Oxide."},
    {"name": "Aqualogica Hydrate+ Jello Gel", "brand": "Aqualogica", "category": "Personal Care",
     "raw": "Aqua, Coconut Water, Hyaluronic Acid, Glycerin, Glyceryl Glucoside, Ammonium Acryloyldimethyltaurate/VP Copolymer."},
    # DERMA TOUCH
    {"name": "Derma Touch Bye Bye Pigmentation Cream", "brand": "Derma Touch", "category": "Personal Care",
     "raw": "Aqua, Kojic Acid Dipalmitate, Niacinamide, Alpha Arbutin, Glycolic Acid, Vitamin E, Glycerin, Mulberry Extract."},
    {"name": "Derma Touch Ceramide Complex Intensive Moisturizer", "brand": "Derma Touch", "category": "Personal Care",
     "raw": "Aqua, Ceramide NP, Ceramide AP, Ceramide EOP, Phytosphingosine, Cholesterol, Glycerin."},
    # TYPSY BEAUTY
    {"name": "Typsy Beauty Face-First Serum Foundation", "brand": "Typsy Beauty", "category": "Personal Care",
     "raw": "Aqua, Dimethicone, Isononyl Isononanoate, Glycerin, Niacinamide, Sodium Hyaluronate, Tocopheryl Acetate."},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Clinical skincare formulation. Score: {score}/100. Patch test recommended for sensitive skin.",
            'fssai_note': 'Cosmetic formulation; clinical actives present.',
            'verdict': 'Clinical formulation' if score >= 80 else 'Contains active ingredients',
            'recommendation': 'Patch test recommended, especially with actives.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Skincare & Makeup Clinical products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
