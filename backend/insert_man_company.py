"""
Insert The Man Company premium grooming and skincare products
Master registry and extended volume II
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['diethyl phthalate', 'triclosan', 'salicylic acid', 'glycolic acid']
_WORTH = ['ethyl alcohol', 'fragrance', 'propylene glycol', 'redensyl']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'phthalate' in n: return 'Phthalate plasticizer; endocrine disruptor concerns'
        if 'triclosan' in n: return 'Antimicrobial; banned in several countries'
        if 'salicylic acid' in n: return 'BHA exfoliant; can irritate sensitive skin'
        if 'glycolic acid' in n: return 'AHA exfoliant; can irritate sensitive skin'
    if cls == 'worth_knowing':
        if 'ethyl alcohol' in n: return 'Preservative/denaturant; controlled concentration'
        if 'fragrance' in n: return 'Fragrance compound; may contain allergens'
        if 'propylene glycol' in n: return 'Humectant; skin conditioning'
        if 'redensyl' in n: return 'Hair growth promoter; research-backed'
    return 'Natural botanical or safe ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Active ingredient; regulatory scrutiny'
    if cls == 'worth_knowing': return 'Permitted grooming ingredient'
    return 'Approved grooming formulation'

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
    # MASTER REGISTRY
    {"name": "The Man Company Charcoal Face Wash with Ylang Ylang", "brand": "The Man Company", "category": "Personal Care",
     "raw": "Aqua, Activated Charcoal, Ylang Ylang Oil, Argan Oil, Vitamin E, Aloe Vera Extract, Sodium Lauroyl Sarcosinate."},
    {"name": "The Man Company Beard Oil (Argan & Geranium)", "brand": "The Man Company", "category": "Personal Care",
     "raw": "Argan Oil, Geranium Oil, Almond Oil, Hazelnut Oil, Jojoba Oil, Vitamin E."},
    {"name": "The Man Company Anti-Dandruff Shampoo (Apple Cider Vinegar)", "brand": "The Man Company", "category": "Personal Care",
     "raw": "Aqua, Apple Cider Vinegar, Rosemary Oil, Tea Tree Oil, Aloe Vera Extract, Sodium Cocoyl Isethionate."},
    {"name": "The Man Company Daily Moisturising Cream (Shea Butter)", "brand": "The Man Company", "category": "Personal Care",
     "raw": "Aqua, Shea Butter, Vitamin E, Almond Oil, Glycerin, Glyceryl Stearate, Aloe Vera Extract."},
    {"name": "The Man Company Blanc Body Parfum", "brand": "The Man Company", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Fragrance, Aqua, Diethyl Phthalate, Propylene Glycol."},
    {"name": "The Man Company Fire EDP (Woody & Spicy)", "brand": "The Man Company", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Triclosan, Propylene Glycol."},
    {"name": "The Man Company Beard Wax (Lemon & Mint)", "brand": "The Man Company", "category": "Personal Care",
     "raw": "Beeswax, Shea Butter, Cocoa Butter, Coconut Oil, Lemon Essential Oil, Mint Essential Oil."},
    {"name": "The Man Company Lightening Lip Balm", "brand": "The Man Company", "category": "Personal Care",
     "raw": "Shea Butter, Cocoa Butter, Vitamin E, Licorice Extract, Almond Oil, Beeswax."},
    # EXTENDED REGISTRY VOL II
    {"name": "The Man Company Sunscreen Lotion (SPF 50) PA+++", "brand": "The Man Company", "category": "Personal Care",
     "raw": "Aqua, Octyl Methoxycinnamate, Avobenzone, Benzophenone-3, Zinc Oxide, Sea Buckthorn Oil, Allantoin, Glycerin."},
    {"name": "The Man Company Vitamin C Face Cream", "brand": "The Man Company", "category": "Personal Care",
     "raw": "Aqua, Vitamin C (Ethyl Ascorbic Acid), Shea Butter, Cocoa Butter, Hyaluronic Acid, Niacinamide, Vitamin E."},
    {"name": "The Man Company Under Eye Gel (Coffee Bean)", "brand": "The Man Company", "category": "Personal Care",
     "raw": "Aqua, Coffee Bean Extract, Aloe Vera, Cucumber Extract, Hyaluronic Acid, Vitamin E, Caffeine."},
    {"name": "The Man Company Charcoal Soap Bar", "brand": "The Man Company", "category": "Personal Care",
     "raw": "Soap Base, Activated Charcoal, Glycerin, Mahua Oil, Coconut Oil, Castor Oil, Patchouli Oil."},
    {"name": "The Man Company Blemish Relief Spot Gel", "brand": "The Man Company", "category": "Personal Care",
     "raw": "Aqua, Salicylic Acid, Tea Tree Oil, Aloe Vera Extract, Neem Extract, Glycolic Acid, Niacinamide."},
    {"name": "The Man Company Hair Growth Tonic (Follicle Therapy)", "brand": "The Man Company", "category": "Personal Care",
     "raw": "Aqua, Redensyl, Saw Palmetto Extract, Biotin, Rosemary Oil, Jojoba Oil, Wheat Germ Oil."},
    {"name": "The Man Company Sky EDP (Fresh & Marine)", "brand": "The Man Company", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Fragrance, Aqua, Diethyl Phthalate, Propylene Glycol."},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Premium grooming. Score: {score}/100.",
            'fssai_note': 'Premium grooming formulation; natural and botanical focus.',
            'verdict': 'Premium formulation' if score >= 85 else 'Standard grooming product',
            'recommendation': 'Suitable for daily grooming use.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} The Man Company products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
