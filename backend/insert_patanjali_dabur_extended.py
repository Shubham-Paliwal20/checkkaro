"""
Insert Patanjali & Dabur Extended Product Range
Ayurvedic and heritage brand cosmetics and personal care database
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['hydrogen peroxide', 'sles', 'paraben', 'mineral oil']
_WORTH = ['ayurvedic', 'herbal extract', 'turmeric', 'neem', 'honey', 'essential oil']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'hydrogen peroxide' in n: return 'Bleaching agent; oxidative'
        if 'sles' in n: return 'Sulfate surfactant; may strip oils'
        if 'paraben' in n: return 'Preservative; endocrine concerns'
        if 'mineral oil' in n: return 'Occlusive mineral oil'
    if cls == 'worth_knowing':
        if 'turmeric' in n: return 'Ayurvedic spice; anti-inflammatory'
        if 'neem' in n: return 'Antibacterial; traditional remedy'
        if 'honey' in n: return 'Natural humectant; antibacterial'
        if 'herbal' in n or 'extract' in n: return 'Plant-based ingredient'
        if 'essential oil' in n: return 'Aromatic botanical extract'
    return 'Ayurvedic personal care ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Contains additives; heritage formula'
    if cls == 'worth_knowing': return 'Permitted Ayurvedic ingredient'
    return 'Traditional natural ingredient'

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
    # PATANJALI
    {"name": "Patanjali Saundarya Aloe Vera Gel", "brand": "Patanjali", "category": "Personal Care",
     "raw": "Aloe Vera (Aloe barbadensis), Vitamin E, Permitted Color, Fragrance, Base Material q.s."},
    {"name": "Patanjali Saundarya Face Wash (Orange Peel)", "brand": "Patanjali", "category": "Personal Care",
     "raw": "Orange Peel (Citrus reticulata), Neem (Azadirachta indica), Tulsi (Ocimum sanctum), Aloe Vera, Aqua, Vitamin E, Honey, Glycerin."},
    {"name": "Patanjali Aloe Vera Face Wash", "brand": "Patanjali", "category": "Personal Care",
     "raw": "Aloe Vera Leaf Juice, Aqua, SLES, Gel Base, Vitamin E, Fragrance."},
    {"name": "Patanjali Neem-Tulsi Face Wash", "brand": "Patanjali", "category": "Personal Care",
     "raw": "Extracts of Neem, Tulsi, Aloe Vera, Aqua, Vitamin E, Honey, CI 19140, CI 42090."},
    {"name": "Patanjali Kesh Kanti Hair Cleanser (Milk Protein)", "brand": "Patanjali", "category": "Personal Care",
     "raw": "Bhringraj, Mehandi, Neem, Tulsi, Ghritkumari (Aloe Vera), Reetha, Shikakai, Bakuchi, Turmeric, Milk Protein."},
    {"name": "Patanjali Kesh Kanti Anti-Dandruff Hair Cleanser", "brand": "Patanjali", "category": "Personal Care",
     "raw": "Rosemary Oil, Honey, Neem Oil, Tea Tree Oil, Nilgiri Oil, Amla, Shikakai, Reetha, Aqua, SLES."},
    {"name": "Patanjali Kesh Kanti Aloe Vera Hair Cleanser", "brand": "Patanjali", "category": "Personal Care",
     "raw": "Aloe Vera, Tulsi, Turmeric, Shikakai, Reetha, Amla, Aqua, Fragrance."},
    {"name": "Patanjali Tejus Anti-Wrinkle Cream", "brand": "Patanjali", "category": "Personal Care",
     "raw": "Aloe Vera, Wheat Germ Oil, Jojoba Oil, Cucumber, Papaya, Banana, Rhubarb, Manjistha, Sandalwood."},
    {"name": "Patanjali Sun Screen Cream (SPF 30)", "brand": "Patanjali", "category": "Personal Care",
     "raw": "Aloe Vera, Wheatgerm Oil, Coconut Oil, Cucumber, Fenugreek, Rubia cordifolia (Manjistha), Turmeric."},
    {"name": "Patanjali Body Ubtan", "brand": "Patanjali", "category": "Personal Care",
     "raw": "Chiraunji, Red Lentil, Black Gram, Barley, Mustard, Turmeric, Sandalwood, Rose, Camphor."},
    {"name": "Patanjali Saundarya Anti-Aging Cream", "brand": "Patanjali", "category": "Personal Care",
     "raw": "Aloe Vera, Wheat Germ Oil, Fruit Extracts (Papaya, Banana), Essential Oils, Aqua, Base material q.s."},
    {"name": "Patanjali Charcoal Face Wash", "brand": "Patanjali", "category": "Personal Care",
     "raw": "Activated Charcoal, Vitamin E, Aloe Vera, Neem, Honey, Aqua, Gel Base."},
    # DABUR
    {"name": "Dabur Gulabari Rose Water", "brand": "Dabur", "category": "Personal Care",
     "raw": "Aqua, Fragrance (Rooh Gulab), Rose Oil, Propylene Glycol, Propyl Paraben, Methyl Paraben."},
    {"name": "Dabur Gulabari Rose Glow Face Cleanser", "brand": "Dabur", "category": "Personal Care",
     "raw": "Aqua, Rose Oil, Glycerin, Propylene Glycol, Citric Acid, Fragrance."},
    {"name": "Dabur Gulabari Moisturising Cold Cream", "brand": "Dabur", "category": "Personal Care",
     "raw": "Rose Oil, Vitamin E, Glycerin, Liquid Paraffin, Cetyl Alcohol, Aqua."},
    {"name": "Dabur Vatika Enriched Coconut Hair Oil (Hibiscus)", "brand": "Dabur", "category": "Personal Care",
     "raw": "Coconut Oil, Hibiscus extract, Brahmi, Amla, Bahera, Kapurkachri, Henna, Lemon oil."},
    {"name": "Dabur Vatika Garlic Enriched Hair Oil", "brand": "Dabur", "category": "Personal Care",
     "raw": "Canola Oil, Palm Oil, Garlic Extract, Rosemary Oil, Tocopheryl Acetate."},
    {"name": "Dabur Vatika Olive Enriched Hair Oil", "brand": "Dabur", "category": "Personal Care",
     "raw": "Mineral Oil, Olive Oil, Cactus Extract, Almond Oil, Vitamin E, Fragrance."},
    {"name": "Dabur Vatika Black Seed Hair Oil", "brand": "Dabur", "category": "Personal Care",
     "raw": "Black Seed (Nigella sativa) extract, Canola Oil, Palm Oil, Fragrance."},
    {"name": "Dabur Fem Fairness Naturals Turmeric Bleach", "brand": "Dabur", "category": "Personal Care",
     "raw": "Aqua, Hydrogen Peroxide, Stearic Acid, Turmeric Extract, Milk Powder, Fragrance."},
    {"name": "Dabur Oxylife Salon Professional Bleach", "brand": "Dabur", "category": "Personal Care",
     "raw": "Hydrogen Peroxide, Oxygen Active, Sea Minerals, Aqua, Glycerin, Stearic Acid."},
    {"name": "Dabur Vatika Health Shampoo", "brand": "Dabur", "category": "Personal Care",
     "raw": "Henna, Shikakai, Olive, Almond, Hibiscus, Amla, SLES, Silicones, Fragrance."},
    {"name": "Dabur DermoViva Fairness Glow Soap", "brand": "Dabur", "category": "Personal Care",
     "raw": "Sodium Palmate, Sodium Palm Kernelate, Saffron, Sandalwood, Turmeric, Fragrance."},
    {"name": "Dabur DermoViva Moisturising Soap", "brand": "Dabur", "category": "Personal Care",
     "raw": "Sodium Palmate, Aloe Vera, Almond, Honey, Olive, Glycerin."},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Ayurvedic/heritage formulation. Score: {score}/100. Traditional recipe.",
            'fssai_note': 'Ayurvedic personal care product; traditional herbs.',
            'verdict': 'Heritage formula' if score >= 85 else 'Traditional formulation',
            'recommendation': 'Use as directed. Test for allergies with herbal ingredients.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Patanjali & Dabur products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
