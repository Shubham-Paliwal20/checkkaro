"""
Insert Indian Soap Industry Registry
BIS-graded toilet soaps, beauty bars, and syndet formulations
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['triclocarban', 'chloroxylenol', 'mineral oil', 'paraben', 'palm kernel', 'sodium palmate']
_WORTH = ['neem', 'turmeric', 'sandalwood', 'herbal', 'glycerin', 'aloe vera', 'silk protein', 'herbal extract']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'triclocarban' in n: return 'Antimicrobial; potential endocrine disruptor'
        if 'chloroxylenol' in n: return 'Phenolic antimicrobial; antiseptic formulation'
        if 'mineral oil' in n: return 'Mineral oil; occlusive ingredient'
        if 'paraben' in n: return 'Preservative; endocrine concerns'
        if 'palm' in n: return 'Palm-derived fatty acid base'
    if cls == 'worth_knowing':
        if 'neem' in n: return 'Neem; antibacterial and traditional remedy'
        if 'turmeric' in n: return 'Turmeric; anti-inflammatory spice'
        if 'sandalwood' in n: return 'Sandalwood; aromatic and soothing'
        if 'herbal' in n or 'extract' in n: return 'Plant-based ingredients'
        if 'silk' in n: return 'Silk protein; skin conditioning'
        if 'glycerin' in n: return 'Glycerin; moisturizing humectant'
        if 'aloe' in n: return 'Aloe vera; soothing botanical'
    return 'Traditional soap ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Contains antimicrobial or traditional preservatives'
    if cls == 'worth_knowing': return 'Natural or traditional botanical ingredients'
    return 'BIS-certified soap ingredient'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    return [i.strip() for i in raw.split(',') if len(i.strip()) > 2]

def _build_obj(name: str) -> dict:
    cls = _classify(name)
    return {'name': name, 'aliases': '', 'classification': cls, 'one_line_note': _note(name, cls), 'regulatory_note': _reg_note(cls)}

def _score(ingredient_objs: list) -> int:
    score = 100
    for ing in ingredient_objs:
        if ing['classification'] == 'commonly_questioned': score -= 5
        elif ing['classification'] == 'worth_knowing': score -= 1
    return max(0, min(100, score))

PRODUCTS = [
    {"name": "Lifebuoy Total 10", "brand": "Hindustan Unilever", "category": "Personal Care",
     "raw": "Sodium Palmate, Water, Sodium Palm Kernelate, Glycerin, Perfume, Sodium Chloride, Lauric Acid, Terpineol, Thymol, Silver Oxide."},
    {"name": "Dettol Original", "brand": "Reckitt Benckiser", "category": "Personal Care",
     "raw": "Sodium Palmate, Sodium Palm Kernelate, Cymbopogon Flexuosus Oil, Chloroxylenol, Glycerin, Tetrasodium EDTA, Etidronic Acid."},
    {"name": "Dove Cream Beauty Bar", "brand": "Hindustan Unilever", "category": "Personal Care",
     "raw": "Sodium Lauroyl Isethionate, Stearic Acid, Lauric Acid, Sodium Palmate, Water, Sodium Isethionate, Sodium Stearate, Cocamidopropyl Betaine, Moisturizing Cream."},
    {"name": "Lux International", "brand": "Hindustan Unilever", "category": "Personal Care",
     "raw": "Sodium Palmate, Sodium Palm Kernelate, Water, Glycerin, Perfume, Sodium Chloride, Titanium Dioxide, Tetrasodium Etidronate, Silk Protein."},
    {"name": "Santoor Sandal & Turmeric", "brand": "Wipro Consumer Care", "category": "Personal Care",
     "raw": "Sodium Palmate, Sodium Palm Kernelate, Water, Sandalwood Extract, Turmeric Extract, Hydrated Magnesium Silicate, Glycerin."},
    {"name": "Pears Pure & Gentle", "brand": "Hindustan Unilever", "category": "Personal Care",
     "raw": "Sorbitol, Water, Sodium Palm Kernelate, Sodium Palmate, Propylene Glycol, Sodium Lauryl Sulfate, PEG-4, Glycerin, Perfume."},
    {"name": "Medimix Ayurvedic", "brand": "Cholayil", "category": "Personal Care",
     "raw": "Stearic Acid, Sodium Laureth Sulfate, Glycerin, Propylene Glycol, 18-Herb Extract (Chitraka, Vanardraka, Sariba, Chopchini, Guggulu)."},
    {"name": "Cinthol Original", "brand": "Godrej Consumer Products", "category": "Personal Care",
     "raw": "Sodium Palmate, Sodium Palm Kernelate, Water, Perfume, Triclocarban, Sodium Chloride, Titanium Dioxide."},
    {"name": "Himalaya Herbals Neem & Turmeric", "brand": "Himalaya Wellness", "category": "Personal Care",
     "raw": "Sodium Palmate, Sodium Palm Kernelate, Neem Seed Oil, Turmeric Root Oil, Lemon Peel Oil."},
    {"name": "Godrej No. 1 Sandal & Turmeric", "brand": "Godrej Consumer Products", "category": "Personal Care",
     "raw": "Sodium Palmate, Sodium Palm Kernelate, Water, Perfume, Sodium Chloride, Glycerin, Sandalwood Extract, Turmeric Extract."},
    {"name": "Fiama Di Wills Gel Bar", "brand": "ITC Limited", "category": "Personal Care",
     "raw": "Sodium Salts of Fatty Acids, Aqua, Propylene Glycol, Sodium Laureth Sulfate, Sorbitol, Glycerin, Peach Extract, Avocado Extract."},
    {"name": "Mysore Sandal Soap", "brand": "Karnataka Soaps & Detergents", "category": "Personal Care",
     "raw": "Sodium Palmate, Sodium Palm Kernelate, Water, Sodium Chloride, Glycerin, Pure Sandalwood Oil, Titanium Dioxide."},
    {"name": "Chandrika Ayurvedic", "brand": "Wipro Consumer Care", "category": "Personal Care",
     "raw": "Coconut Oil, Wild Ginger Oil, Lime Peel Oil, Hydnocarpus Oil, Orange Oil, Sandalwood Oil."},
    {"name": "Margo Neem", "brand": "Jyothy Labs", "category": "Personal Care",
     "raw": "Sodium Palmate, Sodium Palm Kernelate, Neem Oil (100% Original), Vitamin E, Perfume."},
    {"name": "Rexona with Coconut Oil", "brand": "Hindustan Unilever", "category": "Personal Care",
     "raw": "Sodium Palmate, Sodium Palm Kernelate, Water, Perfume, Sodium Chloride, Glycerin, Coconut Oil."},
    {"name": "Wild Stone Ultra Sensual", "brand": "McNROE", "category": "Personal Care",
     "raw": "Sodium Palmate, Sodium Palm Kernelate, Perfume, Glycerin, Kokum Butter."},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. BIS-graded toilet soap. Score: {score}/100. Traditional formulation.",
            'fssai_note': 'Toilet soap product; BIS-graded for Total Fatty Matter content.',
            'verdict': 'Standard soap formulation' if score >= 70 else 'Contains antimicrobial or traditional additives',
            'recommendation': 'Use daily for personal hygiene. Suitable for all skin types.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Indian Soap Registry products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
