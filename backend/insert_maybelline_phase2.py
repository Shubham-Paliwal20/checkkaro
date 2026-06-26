"""
Insert Maybelline New York Phase 2 Advanced Formulations
High-impact actives and advanced makeup technologies
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['talc', 'dimethicone', 'phenoxyethanol', 'alcohol denat']
_WORTH = ['glycerin', 'vitamin c', 'hyaluronic acid', 'niacinamide', 'panthenol']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'talc' in n: return 'Talc powder; inhalation concerns'
        if 'dimethicone' in n: return 'Silicone; long-wear texture'
        if 'phenoxyethanol' in n: return 'Preservative; safe at regulated levels'
        if 'alcohol' in n: return 'Denatured alcohol; preservative'
    if cls == 'worth_knowing':
        if 'glycerin' in n: return 'Humectant; hydrating'
        if 'vitamin c' in n: return 'Antioxidant; brightening'
        if 'hyaluronic' in n: return 'Humectant; deep hydration'
        if 'niacinamide' in n: return 'Vitamin B3; balancing'
        if 'panthenol' in n: return 'Pro-vitamin B5; soothing'
    return 'Advanced makeup ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Professional-grade formulation'
    if cls == 'worth_knowing': return 'Contains beneficial actives'
    return 'Advanced cosmetic formulation'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    return [i.strip() for i in raw.split(',') if len(i.strip()) > 2]

def _build_obj(name: str) -> dict:
    cls = _classify(name)
    return {'name': name, 'aliases': '', 'classification': cls, 'one_line_note': _note(name, cls), 'regulatory_note': _reg_note(cls)}

def _score(ingredient_objs: list) -> int:
    score = 100
    for ing in ingredient_objs:
        if ing['classification'] == 'commonly_questioned': score -= 6
        elif ing['classification'] == 'worth_knowing': score -= 1
    return max(0, min(100, score))

PRODUCTS = [
    {"name": "Maybelline Fit Me Fresh Tint (SPF 50 & Vitamin C)", "brand": "Maybelline New York", "category": "Personal Care",
     "raw": "Aqua, Homosalate, Dicaprylyl Ether, Glycerin, Silica, Alcohol Denat., Ethylhexyl Salicylate, Octocrylene, Polyglyceryl-4 Isostearate, Disteardimonium Hectorite, Tribehenin, PEG-30 Dipolyhydroxystearate, Sodium Chloride, Phenoxyethanol, Silica Silylate, Ascorbyl Glucoside (Vitamin C)."},
    {"name": "Maybelline Fit Me Loose Finishing Powder", "brand": "Maybelline New York", "category": "Personal Care",
     "raw": "Talc, Silica, Dimethicone, Magnesium Stearate, Phenoxyethanol, Ethylhexylglycerin, Iron Oxides, Titanium Dioxide."},
    {"name": "Maybelline Line Tattoo High Impact Liner", "brand": "Maybelline New York", "category": "Personal Care",
     "raw": "Aqua, Styrene/Acrylates Copolymer, Propylene Glycol, Laureth-21, Pentylene Glycol, PEG-40 Hydrogenated Castor Oil, Phenoxyethanol, Ammonium Acrylates Copolymer, Caprylyl Glycol, PPG-2-Deceth-30, Sodium Dehydroacetate."},
    {"name": "Maybelline Sky High Mascara (Waterproof)", "brand": "Maybelline New York", "category": "Personal Care",
     "raw": "Isododecane, Cera Alba / Beeswax, Copernicia Cerifera Cera / Carnauba Wax, Disteardimonium Hectorite, Aqua, Allyl Stearate/VA Copolymer, Oryza Sativa Cera / Rice Bran Wax, Paraffin, Polyvinyl Laurate, VP/Eicosene Copolymer, Propylene Carbonate, Talc, Bamboo Extract."},
    {"name": "Maybelline SuperStay Vinyl Ink Liquid Lipstick", "brand": "Maybelline New York", "category": "Personal Care",
     "raw": "Isododecane, Dimethicone, Trimethylsiloxysilicate, Polymethylsilsesquioxane/Trimethylsiloxysilicate, Polypropylsilsesquioxane, C30-45 Alkyldimethylsilyl Polypropylsilsesquioxane, Trimethylsiloxyphenyl Dimethicone, Isopropyl Lauroyl Sarcosinate."},
    {"name": "Maybelline Lifter Gloss with Hyaluronic Acid", "brand": "Maybelline New York", "category": "Personal Care",
     "raw": "C18-36 Acid Triglyceride, Bis-Diglyceryl Polyacyladipate-2, Polybutene, Pentaerythrityl Tetraisostearate, Tridecyl Trimellitate, Diisostearyl Malate, Silica Dimethyl Silylate, Sodium Hyaluronate."},
    {"name": "Maybelline Tattoo Studio Gel Pencil Liner", "brand": "Maybelline New York", "category": "Personal Care",
     "raw": "Trimethylsiloxysilicate, Hydrogenated Polyisobutene, Synthetic Wax, Isododecane, Polybutene, Ethylene/Propylene Copolymer, Silica Silylate, Pentaerythrityl Tetra-Di-T-Butyl Hydroxyhydrocinnamate."},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Advanced makeup formulation. Score: {score}/100. Professional-grade formula with actives.",
            'fssai_note': 'Professional makeup with silicones and advanced actives.',
            'verdict': 'Advanced makeup formula' if score >= 85 else 'Professional makeup formulation',
            'recommendation': 'Professional-grade product. Double cleanse required. Contains active ingredients.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Maybelline Phase 2 products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
