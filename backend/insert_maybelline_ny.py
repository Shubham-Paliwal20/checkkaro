"""
Insert Maybelline New York Cosmetic Products
India market portfolio with silicone and film-former analysis
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['talc', 'paraben', 'dimethicone', 'cyclopentasiloxane']
_WORTH = ['nylon', 'film-former', 'silicone', 'alcohol denat', 'phenoxyethanol']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'talc' in n: return 'Talc powder; inhalation concerns'
        if 'paraben' in n: return 'Preservative; endocrine disruptor'
        if 'dimethicone' in n or 'cyclopentasiloxane' in n: return 'Silicone; texture and durability'
    if cls == 'worth_knowing':
        if 'nylon' in n or 'film-former' in n: return 'Film-former; long-wear performance'
        if 'silicone' in n: return 'Silicone polymer; water-resistant coating'
        if 'alcohol denat' in n: return 'Denatured alcohol; preservative'
        if 'phenoxyethanol' in n: return 'Preservative; safe at regulated levels'
    return 'Cosmetic ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Contains additives; long-wear formulation'
    if cls == 'worth_knowing': return 'Permitted cosmetic ingredient; film-forming'
    return 'Approved cosmetic formulation'

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
    {"name": "Maybelline Fit Me Matte + Poreless Foundation", "brand": "Maybelline New York", "category": "Personal Care",
     "raw": "Aqua, Cyclocyclopentasiloxane, Nylon-12, Isododecane, Alcohol Denat., Cyclopentasiloxane, PEG-10 Dimethicone, Cetyl PEG/PPG-10/1 Dimethicone, PEG-20, Polyglyceryl-4 Isostearate, Disteardimonium Hectorite, Phenoxyethanol, Magnesium Sulfate, Disodium Stearoyl Glutamate, HDI/Trimethylol Hexyllactone Crosspolymer, Methylparaben, Silica Silylate, Tocopherol, Aluminum Hydroxide, Silica, Pentaerythrityl Tetra-Di-T-Butyl Hydroxyhydrocinnamate."},
    {"name": "Maybelline Instant Age Rewind Eraser Concealer", "brand": "Maybelline New York", "category": "Personal Care",
     "raw": "Aqua, Cyclopentasiloxane, Dimethicone, Isododecane, Glycerin, PEG-9 Polydimethylsiloxyethyl Dimethicone, Butylene Glycol, Dimethicone Crosspolymer, Nylon-12, Disteardimonium Hectorite, Cyclohexasiloxane, PEG-10 Dimethicone, Cetyl PEG/PPG-10/1 Dimethicone, Phenoxyethanol, Sodium Chloride, Polyglyceryl-4 Isostearate."},
    {"name": "Maybelline Fit Me Compact Powder (SPF 28)", "brand": "Maybelline New York", "category": "Personal Care",
     "raw": "Perlite, Talc, Titanium Dioxide, Zea Mays Starch / Corn Starch, Kaolin, Triisostearin, Ethylhexyl Salicylate, Magnesium Stearate, Caprylyl Glycol."},
    {"name": "Maybelline Colossal Kajal (24HR Smudge Proof)", "brand": "Maybelline New York", "category": "Personal Care",
     "raw": "Isododecane, Polyethylene, Synthetic Wax, Ethylene/Propylene Copolymer, Bis-Diglyceryl Polyacyladipate-2, Hydrogenated Polydicyclopentadiene, Polybutene, Octyldodecanol, Pentaerythrityl Tetra-Di-T-Butyl Hydroxyhydrocinnamate."},
    {"name": "Maybelline The Colossal Mascara (Waterproof)", "brand": "Maybelline New York", "category": "Personal Care",
     "raw": "Isododecane, Cera Alba / Beeswax, Copernicia Cerifera Cera / Carnauba Wax, Disteardimonium Hectorite, Aqua, Allyl Stearate/VA Copolymer, Oryza Sativa Cera / Rice Bran Wax, Paraffin, Alcohol Denat., Polyvinyl Laurate, VP/Eicosene Copolymer, Propylene Carbonate."},
    {"name": "Maybelline Hypercurl Mascara (Washable)", "brand": "Maybelline New York", "category": "Personal Care",
     "raw": "Aqua, Cera Alba / Beeswax, Glyceryl Stearate, Copernicia Cerifera Cera / Carnauba Wax, Acacia Senegal Gum, Polyurethane-35, Paraffin, Magnesium Aluminum Silicate, Stearic Acid, Palmitic Acid."},
    {"name": "Maybelline SuperStay Matte Ink Liquid Lipstick", "brand": "Maybelline New York", "category": "Personal Care",
     "raw": "Dimethicone, Trimethylsiloxysilicate, Isododecane, Nylon-611/Dimethicone Copolymer, Dimethicone Crosspolymer, C30-45 Alkyldimethylsilyl Polypropylsilsesquioxane, Lauroyl Lysine, Silylate, Phenoxyethanol, Disodium Stearoyl Glutamate, Aluminum Hydroxide, Limonene, Silica, Synthetic Fluorphlogopite, Paraffin, Calcium Aluminum Borosilicate."},
    {"name": "Maybelline Sensational Liquid Matte Lipstick", "brand": "Maybelline New York", "category": "Personal Care",
     "raw": "Isododecane, Polyethylene, Trimethylsiloxyphenyl Dimethicone, Isohexadecane, Dimethicone, Acrylates/Dimethicone Copolymer, Polypropylsilsesquioxane, Stearyl Heptanoate, Hydrogenated Polyisobutene, Hydrogenated Styrene/Methyl Styrene/Indene Copolymer."},
    {"name": "Maybelline Baby Lips Lip Balm (Cherry Kiss)", "brand": "Maybelline New York", "category": "Personal Care",
     "raw": "Polybutene, Octyldodecanol, Isopropyl Myristate, Petrolatum, Ethylhexyl Methoxycinnamate, Polyethylene, Ozokerite, Ethylhexyl Salicylate, Butyrospermum Parkii Butter / Shea Butter, Silica Silylate, Euphorbia Cerifera Cera / Candelilla Wax."},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Long-wear makeup. Score: {score}/100. Professional formula with silicones.",
            'fssai_note': 'Cosmetic makeup product; contains silicones and film-formers.',
            'verdict': 'Professional makeup formulation' if score >= 80 else 'Contains silicones and additives',
            'recommendation': 'Professional-grade cosmetic. Follow application guidelines.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Maybelline New York products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
