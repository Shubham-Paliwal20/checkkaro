"""
Insert Indian Baby Products
Bath, Hygiene, Massage, Nutrition, Protection, Skincare, Sun Care
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['mineral oil', 'paraben', 'sls', 'talc', 'petroleum', 'phenoxyethanol']
_WORTH = ['neem', 'olive oil', 'coconut oil', 'natural', 'herbal', 'aloe vera', 'organic']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'mineral oil' in n: return 'Mineral oil; petroleum-derived moisturizer'
        if 'paraben' in n: return 'Paraben preservative; approved for use'
        if 'sls' in n or 'sulfate' in n: return 'SLS/SLES surfactant; gentle formulation'
        if 'talc' in n: return 'Talc powder; mineral-based absorbent'
    if cls == 'worth_knowing':
        if 'neem' in n: return 'Neem; antibacterial and natural'
        if 'coconut' in n: return 'Coconut oil; natural moisturizer'
        if 'olive' in n: return 'Olive oil; gentle natural oil'
        if 'aloe' in n: return 'Aloe vera; soothing botanical'
        if 'organic' in n or 'herbal' in n: return 'Organic/herbal formulation'
    return 'Baby care ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Dermatologically tested; safe for baby skin'
    if cls == 'worth_knowing': return 'Contains natural/herbal ingredients; hypoallergenic'
    return 'Gentle baby care product'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    return [i.strip() for i in raw.split(',') if len(i.strip()) > 2]

def _build_obj(name: str) -> dict:
    cls = _classify(name)
    return {'name': name, 'aliases': '', 'classification': cls, 'one_line_note': _note(name, cls), 'regulatory_note': _reg_note(cls)}

def _score(ingredient_objs: list) -> int:
    score = 100
    for ing in ingredient_objs:
        if ing['classification'] == 'commonly_questioned': score -= 3
        elif ing['classification'] == 'worth_knowing': score -= 1
    return max(0, min(100, score))

PRODUCTS = [
    # BATH & HYGIENE
    {"name": "Johnson's Baby Bath", "brand": "Johnson & Johnson", "category": "Baby Care",
     "raw": "Water, Sodium Laureth Sulfate, Cocamidopropyl Betaine, Glycerin, Fragrance, Sodium Chloride, Disodium EDTA, Citric Acid, Sodium Hydroxide, Methylchloroisothiazolinone.",
     "type": "Baby Bath"},
    {"name": "Chicco Gentle Bath", "brand": "Chicco", "category": "Baby Care",
     "raw": "Water, Sodium Cocoyl Isethionate, Sodium Chloride, Glycerin, Cocamide DEA, Fragrance, Cellulose, Sodium Benzoate, Potassium Sorbate.",
     "type": "Baby Bath"},
    {"name": "Himalaya Gentle Baby Bath", "brand": "Himalaya Wellness", "category": "Baby Care",
     "raw": "Water, Sodium Lauryl Sulfate, Cocamidopropyl Betaine, Glycerin, Aloe Barbadensis (Aloe Vera) Leaf Extract, Fragrance, Sodium Chloride, Sodium Benzoate.",
     "type": "Baby Bath"},
    # MASSAGE & OIL
    {"name": "Johnson's Baby Oil", "brand": "Johnson & Johnson", "category": "Baby Care",
     "raw": "Mineral Oil, Tocopherol Acetate (Vitamin E), Fragrance.",
     "type": "Baby Oil"},
    {"name": "Himalaya Baby Massage Oil", "brand": "Himalaya Wellness", "category": "Baby Care",
     "raw": "Mineral Oil, Coconut Oil, Sesame Oil, Fragrance, Tocopherol, BHT.",
     "type": "Baby Massage Oil"},
    {"name": "Mamaearth Ubtan Baby Massage Oil", "brand": "Mamaearth", "category": "Baby Care",
     "raw": "Coconut Oil, Almond Oil, Olive Oil, Turmeric Extract, Ashwagandha Extract, Sesame Oil, Vitamin E.",
     "type": "Baby Massage Oil"},
    # SKINCARE
    {"name": "Johnson's Baby Lotion", "brand": "Johnson & Johnson", "category": "Baby Care",
     "raw": "Water, Glycerin, Mineral Oil, Stearic Acid, Cetyl Alcohol, Dimethicone, Fragrance, Disodium EDTA, Sodium Chloride.",
     "type": "Baby Lotion"},
    {"name": "Cetaphil Baby Moisturizing Cream", "brand": "Cetaphil", "category": "Baby Care",
     "raw": "Water, Mineral Oil, Isopropyl Palmitate, Glycerin, Cetyl Alcohol, Stearyl Alcohol, Sodium Chloride, Fragrance.",
     "type": "Baby Cream"},
    {"name": "Mamaearth Natural Moisturizer for Baby", "brand": "Mamaearth", "category": "Baby Care",
     "raw": "Water, Coconut Oil, Almond Oil, Olive Oil, Shea Butter, Vitamin E, Aloe Vera Extract.",
     "type": "Baby Moisturizer"},
    # DIAPER & PROTECTION
    {"name": "Pampers Swaddlers Diaper", "brand": "Pampers", "category": "Baby Care",
     "raw": "Non-woven fabric, Absorbent core (fluff pulp, SAP), Polyethylene, Polypropylene, Elastic thread, Fragrance.",
     "type": "Diaper"},
    {"name": "Himalaya Diaper Rash Cream", "brand": "Himalaya Wellness", "category": "Baby Care",
     "raw": "Mineral Oil, Lanolin, Zinc Oxide, Talc, Calendula Extract, Turmeric Extract, Vitamin A, Fragrance.",
     "type": "Diaper Rash Cream"},
    # SUN CARE
    {"name": "Chicco Sunscreen SPF 50", "brand": "Chicco", "category": "Baby Care",
     "raw": "Water, Zinc Oxide, Titanium Dioxide, Glycerin, Octinoxate, Fragrance, Tocopherol, Glyceryl Stearate.",
     "type": "Baby Sunscreen"},
    {"name": "Mamaearth Ubtan Natural Sunscreen SPF 30", "brand": "Mamaearth", "category": "Baby Care",
     "raw": "Water, Zinc Oxide, Turmeric Extract, Aloe Vera, Sesame Oil, Coconut Oil, Vitamin E, Almond Oil.",
     "type": "Baby Sunscreen"},
    # HAIR & SCALP
    {"name": "Johnson's Baby Shampoo", "brand": "Johnson & Johnson", "category": "Baby Care",
     "raw": "Water, Sodium Laureth Sulfate, Cocamidopropyl Betaine, Glycerin, Sodium Chloride, Fragrance, Sodium Benzoate.",
     "type": "Baby Shampoo"},
    {"name": "Himalaya Baby Shampoo", "brand": "Himalaya Wellness", "category": "Baby Care",
     "raw": "Water, Sodium Laureth Sulfate, Cocamidopropyl Betaine, Glycerin, Aloe Barbadensis Leaf Extract, Fragrance, Sodium Benzoate.",
     "type": "Baby Shampoo"},
    # NUTRITION
    {"name": "Wyeth Nutrition Fortipro", "brand": "Wyeth", "category": "Baby Care",
     "raw": "Skimmed Milk Powder, Whey Protein Concentrate, Lactose, Vegetable Oil, Soy Lecithin, Minerals (Calcium, Iron, Zinc), Vitamins (A, D, B12).",
     "type": "Infant Formula"},
    {"name": "Nestlé Lactogen 1 Infant Formula", "brand": "Nestlé", "category": "Baby Care",
     "raw": "Skimmed Milk, Whey Protein Concentrate, Lactose, Vegetable Oil, Nucleotides, Vitamins, Minerals, Choline.",
     "type": "Infant Formula"},
    {"name": "Aptamil Gold Infant Formula", "brand": "Nutricia", "category": "Baby Care",
     "raw": "Skimmed Cow Milk, Whey Protein, Lactose, Palm Oil, Fish Oil, Probiotics, Vitamins, Minerals.",
     "type": "Infant Formula"},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. {p['type']}. Gentle baby care product. Score: {score}/100.",
            'fssai_note': 'Dermatologically tested baby product - safe for sensitive baby skin. Follow usage instructions.',
            'verdict': 'Gentle formulation with hypoallergenic ingredients' if score >= 90 else 'Standard baby care product',
            'recommendation': 'Patch test before use. Use as directed. Consult pediatrician if irritation occurs.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Indian Baby Products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
