"""
Insert Plum Goodness Clinical Database products
100% vegan and cruelty-free skincare with active botanical concentrations
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['salicylic acid', 'glycolic acid', 'lactic acid', 'sodium lauryl sulfate']
_WORTH = ['niacinamide', 'hyaluronic acid', 'vitamin c', 'caffeine', 'peptide', 'botanical extract']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'salicylic' in n: return 'BHA exfoliant; can irritate sensitive skin'
        if 'glycolic' in n or 'lactic' in n: return 'AHA exfoliant; can irritate sensitive skin'
        if 'sulfate' in n: return 'Sulfate surfactant; may strip natural oils'
    if cls == 'worth_knowing':
        if 'niacinamide' in n: return 'Vitamin B3; pore-minimizing and balancing'
        if 'hyaluronic' in n: return 'Humectant; deep hydration'
        if 'vitamin c' in n or 'ascorbic' in n: return 'Antioxidant; brightening and firming'
        if 'caffeine' in n: return 'Stimulant; improves circulation'
        if 'peptide' in n: return 'Amino acid chain; anti-aging'
        if 'extract' in n: return 'Botanical extract; clinically active'
    return 'Natural vegan ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Active ingredient; professional use recommended'
    if cls == 'worth_knowing': return 'Permitted cosmetic active; clinically proven efficacy'
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
        elif ing['classification'] == 'worth_knowing': score -= 1
    return max(0, min(100, score))

PRODUCTS = [
    {"name": "Plum Green Tea Pore Cleansing Face Wash", "brand": "Plum", "category": "Personal Care",
     "raw": "Aqua (Water), Camellia Sinensis (Green Tea) Leaf Extract, Glycolic Acid, Cellulose Beads, Sodium Laureth Sulfate, Cocamidopropyl Betaine, Glycerin, Ethoxylated Lanolin, Fragrance, Phenoxyethanol, Ethylhexylglycerin."},
    {"name": "Plum 10% Niacinamide Serum with Rice Water", "brand": "Plum", "category": "Personal Care",
     "raw": "Aqua, Niacinamide (10%), Oryza Sativa (Rice) Bran Water, Propanediol, Glycerin, Ethoxydiglycol, Caffeine, Squalane, Phenoxyethanol, Ethylhexylglycerin, Sodium Hyaluronate."},
    {"name": "Plum 15% Vitamin C Face Serum with Mandarin", "brand": "Plum", "category": "Personal Care",
     "raw": "Aqua, Ethyl Ascorbic Acid (15%), Propanediol, Ethoxydiglycol, Mandarin Orange Peel Extract, Kakadu Plum Fruit Extract, Betaine, Sodium Hyaluronate, Phenoxyethanol."},
    {"name": "Plum Green Tea Renewed Clarity Night Gel", "brand": "Plum", "category": "Personal Care",
     "raw": "Aqua, Aloe Barbadensis Leaf Juice, Green Tea Leaf Extract, Glycyrrhiza Glabra (Licorice) Root Extract, Lycium Barbarum (Goji) Fruit Extract, Ginkgo Biloba Leaf Extract, Argania Spinosa (Argan) Kernel Oil."},
    {"name": "Plum Cica & Hyaluronic Acid Aqua Repair Face Mask", "brand": "Plum", "category": "Personal Care",
     "raw": "Aqua, Centella Asiatica (Cica) Extract, Sodium Hyaluronate, Glycerin, Niacinamide, Panthenol, Allantoin, Aloe Barbadensis Leaf Juice, Kaolin, Bentonite."},
    {"name": "Plum 2% Salicylic Acid Face Serum", "brand": "Plum", "category": "Personal Care",
     "raw": "Aqua, Salicylic Acid (2%), Ethoxydiglycol, Chlorophyll Extract, Glycerin, Xanthan Gum, Phenoxyethanol, Triethanolamine."},
    {"name": "Plum Bulgarian Violet Luminizing Face Scrub", "brand": "Plum", "category": "Personal Care",
     "raw": "Aqua, Cellulose Acetate, Bulgarian Violet Extract, Glycerin, Sunflower Seed Oil, Cetearyl Alcohol, Glyceryl Stearate, Vitamin E."},
    {"name": "Plum Olive & Macadamia Healthy Hydration Shampoo", "brand": "Plum", "category": "Personal Care",
     "raw": "Aqua, Sodium Laureth Sulfate, Cocamidopropyl Betaine, Olive Oil PEG-7 Esters, Macadamia Integrifolia Seed Oil, Hydrolyzed Corn Protein, Hydrolyzed Wheat Protein, Hydrolyzed Soy Protein."},
    {"name": "Plum Coconut Milk & Peptides Strength & Shine Conditioner", "brand": "Plum", "category": "Personal Care",
     "raw": "Aqua, Cetearyl Alcohol, Coconut Milk Extract, Pea Peptide, Hydrolyzed Soy Protein, Coconut Oil, Panthenol, Phenoxyethanol."},
    {"name": "Plum Ginseng Anti-Hair Fall Root Serum", "brand": "Plum", "category": "Personal Care",
     "raw": "Aqua, Ginseng Root Extract, Watercress Extract, Indian Cress Extract, Panthenol, Glycerin, Biotinoyl Tripeptide-1, Phenoxyethanol."},
    {"name": "Plum Vanilla Vibes Body Oil", "brand": "Plum", "category": "Personal Care",
     "raw": "Helianthus Annuus (Sunflower) Seed Oil, Caprylic/Capric Triglyceride, Fragrance, Vanilla Planifolia Fruit Extract, Persea Gratissima (Avocado) Oil, Vitamin E."},
    {"name": "Plum Hawaiian Beach Body Wash", "brand": "Plum", "category": "Personal Care",
     "raw": "Aqua, Sodium Laureth Sulfate, Cocamidopropyl Betaine, Glycerin, Seaweed Extract, Fragrance, CI 42090."},
    {"name": "Plum Coffee Wake-up Scrub", "brand": "Plum", "category": "Personal Care",
     "raw": "Coffea Arabica (Coffee) Seed Powder, Sugar, Cocos Nucifera (Coconut) Oil, Shea Butter, Vitamin E."},
    {"name": "Plum Green Tea Daylight Sunscreen SPF 35 PA+++", "brand": "Plum", "category": "Personal Care",
     "raw": "Aqua, Ethylhexyl Methoxycinnamate, Benzophenone-3, Butyl Methoxydibenzoylmethane, Green Tea Leaf Extract, Calendula Officinalis Flower Extract, Aloe Barbadensis Leaf Juice."},
    {"name": "Plum 2% Niacinamide & Rice Water Hybrid Sunscreen SPF 50", "brand": "Plum", "category": "Personal Care",
     "raw": "Aqua, Zinc Oxide, Titanium Dioxide, Niacinamide, Rice Water, Diethylamino Hydroxybenzoyl Hexyl Benzoate, Bis-Ethylhexyloxyphenol Methoxyphenyl Triazine."},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Vegan skincare with clinical actives. Score: {score}/100. Cruelty-free formulation.",
            'fssai_note': '100% vegan and cruelty-free; clean label cosmetic.',
            'verdict': 'Premium vegan skincare' if score >= 90 else 'Clinical vegan formulation',
            'recommendation': 'Suitable for all skin types. Contains active ingredients; patch test recommended.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Plum Goodness products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
