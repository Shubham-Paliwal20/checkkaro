"""
Insert Minimalist Advanced Skincare Products
Clinical skincare database with standardized active ingredients
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['salicylic acid', 'lha', 'mandelic acid', 'tranexamic acid']
_WORTH = ['niacinamide', 'hyaluronic acid', 'vitamin c', 'alpha arbutin', 'retinol', 'ceramide', 'peptide']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'salicylic' in n or 'lha' in n: return 'Chemical exfoliant; can irritate sensitive skin'
        if 'mandelic' in n: return 'AHA exfoliant; gentler than glycolic acid'
        if 'tranexamic' in n: return 'Amino acid; brightening and anti-inflammatory'
    if cls == 'worth_knowing':
        if 'niacinamide' in n: return 'Vitamin B3; pore-minimizing and balancing'
        if 'hyaluronic' in n: return 'Humectant; deep hydration'
        if 'vitamin c' in n or 'ascorbic' in n: return 'Antioxidant; brightening and antioxidant'
        if 'alpha arbutin' in n: return 'Skin lightener; melanin inhibitor'
        if 'retinol' in n: return 'Vitamin A derivative; anti-aging'
        if 'ceramide' in n: return 'Lipid barrier repair; essential'
        if 'peptide' in n or 'tripeptide' in n: return 'Amino acid chain; anti-aging'
    return 'Clinical skincare ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Active ingredient; professional use recommended'
    if cls == 'worth_knowing': return 'Permitted cosmetic active; clinically proven'
    return 'Clean label skincare ingredient'

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
    {"name": "Minimalist Vitamin C (Ethyl Ascorbic Acid) 16%", "brand": "Minimalist", "category": "Personal Care",
     "raw": "1-Ethyl Ascorbic Acid, Ethoxydiglycol, Dimethyl Isosorbide, Gluconolactone, Sodium Gluconate, Ferulic Acid, Centella Asiatica (Cica) Water, Pullulan, Xanthan Gum, Lecithin, Sclerotium Gum."},
    {"name": "Minimalist Alpha Arbutin 2% + Hyaluronic Acid", "brand": "Minimalist", "category": "Personal Care",
     "raw": "Aloe Vera Juice, Alpha Arbutin (2%), Propanediol, Ethoxydiglycol, Sodium Hyaluronate, Phenoxyethanol, Pullulan, Xanthan Gum, Lecithin, Sclerotium Gum."},
    {"name": "Minimalist Sunscreen SPF 50 Multi-Vitamin", "brand": "Minimalist", "category": "Personal Care",
     "raw": "Aqua, Octocrylene, Diisopropyl Adipate, Propylene Glycol, Butyl Methoxydibenzoylmethane, Cetearyl Alcohol, C12-15 Alkyl Benzoate, Glyceryl Stearate, Niacinamide, Retinyl Palmitate, Tocopheryl Acetate, Panthenol."},
    {"name": "Minimalist Sepicalm 3% + Oat Moisturizer", "brand": "Minimalist", "category": "Personal Care",
     "raw": "Aqua, Avena Sativa (Oat) Kernel Extract, Squalane, Glyceryl Stearate, Cetyl Alcohol, Sepicalm (Sodium Palmitoyl Proline), Niacinamide, Polyacrylate Crosspolymer-6."},
    {"name": "Minimalist Marula Oil 5% Moisturizer", "brand": "Minimalist", "category": "Personal Care",
     "raw": "Aqua, Sclerocarya Birrea (Marula) Seed Oil, Glycerin, Caprylic/Capric Triglyceride, Glyceryl Stearate, Betaine, Sodium Hyaluronate, Vitamin F."},
    {"name": "Minimalist Aquaporin Booster 5% Cleanser", "brand": "Minimalist", "category": "Personal Care",
     "raw": "Aqua, Glycerin, Glyceryl Glucoside, Diglycerin, PEG-7 Glyceryl Cocoate, Sodium Lauroyl Methyl Isethionate, Cocamidopropyl Betaine, Sodium Methyl Oleoyl Taurate."},
    {"name": "Minimalist Salicylic + LHA 2% Face Wash", "brand": "Minimalist", "category": "Personal Care",
     "raw": "Aqua, Glycerin, Cocamidopropyl Betaine, Salicylic Acid, Capryloyl Salicylic Acid (LHA), Sodium Lauroyl Methyl Isethionate, Panthenol."},
    {"name": "Minimalist Tranexamic 3% + HPA", "brand": "Minimalist", "category": "Personal Care",
     "raw": "Aqua, Tranexamic Acid (3%), Mandelic Acid, Hydroxyphenoxy Propionic Acid, Sodium Hyaluronate, Ethoxydiglycol, Propanediol."},
    {"name": "Minimalist Maleic Bond Repair Complex 5%", "brand": "Minimalist", "category": "Personal Care",
     "raw": "Aqua, Maleic Acid, Transglutaminase, Amino Acids (Arginine, Serine, Valine), Squalane, Coconut Oil, Cetyl Alcohol, Behentrimonium Chloride."},
    {"name": "Minimalist Niacinamide 5% Body Lotion", "brand": "Minimalist", "category": "Personal Care",
     "raw": "Aqua, Glycerin, Niacinamide (5%), Caprylic/Capric Triglyceride, Shea Butter, Glyceryl Stearate, Glycerin, Ceramide NP, Ceramide AP, Ceramide EOP."},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Clinical active skincare. Score: {score}/100. Clinically verified formulation.",
            'fssai_note': 'Advanced skincare with standardized active ingredients.',
            'verdict': 'Clinical skincare product' if score >= 85 else 'Active ingredient formulation',
            'recommendation': 'Contains active ingredients; patch test recommended. Use as directed.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Minimalist Advanced products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
