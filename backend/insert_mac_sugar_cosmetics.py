"""
Insert M·A·C and SUGAR Cosmetics Professional Artistry Products
Pro-artistry & high-wear registry for professional makeup
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['cyclopentasiloxane', 'dimethicone', 'talc', 'paraffin', 'isododecane']
_WORTH = ['sodium hyaluronate', 'tocopheryl acetate', 'green tea extract', 'caffeine', 'glycerin']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'cyclopentasiloxane' in n or 'dimethicone' in n: return 'Silicone; long-wear texture'
        if 'talc' in n: return 'Talc powder; inhalation concerns'
        if 'paraffin' in n or 'isododecane' in n: return 'Mineral oil derivative; occlusive'
    if cls == 'worth_knowing':
        if 'sodium hyaluronate' in n: return 'Humectant; hydrating'
        if 'tocopheryl acetate' in n: return 'Vitamin E; antioxidant'
        if 'green tea' in n: return 'Antioxidant; skin-soothing'
        if 'caffeine' in n: return 'Stimulant; energizing'
        if 'glycerin' in n: return 'Humectant; hydrating'
    return 'Professional makeup ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Professional-grade formulation; long-wear'
    if cls == 'worth_knowing': return 'Contains beneficial actives'
    return 'Professional artistry cosmetic'

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
    {"name": "M.A.C Studio Fix Fluid SPF 15", "brand": "M.A.C", "category": "Personal Care",
     "raw": "Water, Cyclopentasiloxane, PEG-10 Dimethicone, Butylene Glycol, Trimethylsiloxysilicate, Ethylhexyl Methoxycinnamate, Dimethicone, Magnesium Sulfate, Titanium Dioxide, Algae Extract, Tocopheryl Acetate, Sodium Hyaluronate, Lecithin, Hydrogenated Lecithin."},
    {"name": "M.A.C Prep + Prime Fix+", "brand": "M.A.C", "category": "Personal Care",
     "raw": "Water, Glycerin, Butylene Glycol, Cucumber Fruit Extract, Chamomilla Recutita Extract, Green Tea Leaf Extract, Caffeine, Panthenol, Arginine, PEG-40 Hydrogenated Castor Oil, Phenoxyethanol."},
    {"name": "M.A.C Strobe Cream", "brand": "M.A.C", "category": "Personal Care",
     "raw": "Water, Cyclopentasiloxane, Glycerin, Geranium Oil, Green Tea Extract, Grape Fruit Extract, Scutellaria Baicalensis Root Extract, Mulberry Root Extract, Sodium Hyaluronate, Panthenol, Tocopheryl Acetate."},
    {"name": "M.A.C Matte Lipstick (Ruby Woo)", "brand": "M.A.C", "category": "Personal Care",
     "raw": "Octyldodecanol, Ricinus Communis Seed Oil, Silica, Tricaprylyl Citrate, Ozokerite, Isononyl Isononanoate, Paraffin, Phenyl Trimethicone, Microcrystalline Wax, Ethylhexyl Palmitate, Carnauba Wax."},
    {"name": "M.A.C Retro Matte Liquid Lipcolour", "brand": "M.A.C", "category": "Personal Care",
     "raw": "Isododecane, Dimethicone, Trimethylsiloxysilicate, Polybutene, Petrolatum, Cyclohexasiloxane, Kaolin, Disteardimonium Hectorite, Beeswax, Silica Dimethyl Silylate, Tocopherol, Avocado Oil."},
    {"name": "M.A.C Studio Fix 24-Hour Smooth Wear Concealer", "brand": "M.A.C", "category": "Personal Care",
     "raw": "Water, Cyclopentasiloxane, Trimethylsiloxysilicate, Phenyl Trimethicone, Butylene Glycol, Boron Nitride, Sorbitan Sesquioleate, PEG/PPG-18/18 Dimethicone, Algae Extract, Tocopheryl Acetate, Sodium Hyaluronate."},
    {"name": "M.A.C Pro Longwear Paint Pot", "brand": "M.A.C", "category": "Personal Care",
     "raw": "Isododecane, Calcium Sodium Borosilicate, Dimethicone, Polyethylene, Hydrogenated Polyisobutene, Quaternium-90 Bentonite, Silica, Retinyl Palmitate, Tocopheryl Acetate, Lecithin."},
    {"name": "M.A.C Mineralize Skinfinish", "brand": "M.A.C", "category": "Personal Care",
     "raw": "Mica, Talc, Nylon-12, Dimethicone, Isopropyl Palmitate, Polysorbate 20, Magnesium Aluminum Silicate, Tocopheryl Acetate, Simmondsia Chinensis Seed Oil, Yeast Extract."},
    {"name": "M.A.C Stack Mascara", "brand": "M.A.C", "category": "Personal Care",
     "raw": "Water, Silica, Stearic Acid, Glyceryl Stearate, Synthetic Beeswax, Paraffin, Acacia Senegal Gum, Butylene Glycol, Acrylates/Ethylhexyl Acrylate Copolymer, Aminomethyl Propanediol, Copernicia Cerifera Wax, VP/Eicosene Copolymer."},
    {"name": "M.A.C Technakohl Liner", "brand": "M.A.C", "category": "Personal Care",
     "raw": "Cyclopentasiloxane, Polyethylene, Polybutene, Silica Silylate, Euphorbia Cerifera Wax, Hydrogenated Jojoba Oil, Octyldodecanol, Microcrystalline Wax, Sucrose Tetrastearate Triacetate."},
    {"name": "SUGAR Ace Of Face Foundation Stick", "brand": "SUGAR", "category": "Personal Care",
     "raw": "Ethylhexyl Palmitate, Silica, Aluminum Starch Octenylsuccinate, Polyethylene, Phenyl Trimethicone, Caprylic/Capric Triglyceride, Candelilla Wax, Isododecane, Trimethylsiloxysilicate, Phenoxyethanol."},
    {"name": "SUGAR Smudge Me Not Liquid Lipstick", "brand": "SUGAR", "category": "Personal Care",
     "raw": "Isododecane, Trimethylsiloxysilicate, Cyclopentasiloxane, Mica, Quaternium-18 Bentonite, Hydrogenated Polyisobutene, Vitamin E, Propylene Carbonate, Fragrance."},
    {"name": "SUGAR Aquaholic Priming Moisturizer", "brand": "SUGAR", "category": "Personal Care",
     "raw": "Aqua, Cyclopentasiloxane, Dimethicone, Glycerin, Sea Water Extract, Sodium Hyaluronate, Malachite Extract, Aloe Vera Leaf Juice, Phenoxyethanol, Ethylhexylglycerin."},
    {"name": "SUGAR Arch Arrival Brow Definer", "brand": "SUGAR", "category": "Personal Care",
     "raw": "Iron Oxides, Hydrogenated Soybean Oil, Hydrogenated Coco-Glycerides, Hydrogenated Vegetable Oil, Zinc Stearate, Carnauba Wax, Stearic Acid, Polyglyceryl-2 Triisostearate."},
    {"name": "SUGAR Contour De Force Face Palette", "brand": "SUGAR", "category": "Personal Care",
     "raw": "Talc, Mica, Magnesium Stearate, Dimethicone, Isopropyl Myristate, Ethylhexyl Palmitate, Silica, Phenoxyethanol, Ethylhexylglycerin, Iron Oxides."},
    {"name": "SUGAR Kohl Of Honour Intense Kajal", "brand": "SUGAR", "category": "Personal Care",
     "raw": "Cyclopentasiloxane, Trimethylsiloxysilicate, Polyethylene, Candelilla Wax, Silica, Hydrogenated Cottonseed Oil, Tocopherol, Ascorbyl Palmitate."},
    {"name": "SUGAR Matte As Hell Crayon Lipstick", "brand": "SUGAR", "category": "Personal Care",
     "raw": "Isododecane, Diisostearyl Malate, Synthetic Wax, Dimethicone, Caprylyl Methicone, Polybutene, Vinyl Dimethicone/Methicone Silsesquioxane Crosspolymer, Glyceryl Caprylate."},
    {"name": "SUGAR Bling Leader Illuminating Sunscreen", "brand": "SUGAR", "category": "Personal Care",
     "raw": "Aqua, Ethylhexyl Methoxycinnamate, Butyl Methoxydibenzoylmethane, Glycerin, Niacinamide, Shea Butter, Sodium Hyaluronate, Mica, Titanium Dioxide, Phenoxyethanol."},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Professional artistry makeup. Score: {score}/100. Dermatologist tested formulation.",
            'fssai_note': 'Professional makeup product with silicones and long-wear actives.',
            'verdict': 'Professional artistry makeup' if score >= 80 else 'Long-wear makeup formulation',
            'recommendation': 'Professional-grade formula. Double cleanse required. Patch test for sensitivities.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} M.A.C & SUGAR products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
