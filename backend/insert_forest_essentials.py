"""
Insert Forest Essentials luxury Ayurvedic products from Forest_Essentials_Ingredient_Registry PDF
Premium skincare with traditional Indian ingredients and cold-pressed oils
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = []
_WORTH = [
    'hydrogen peroxide', 'propylene glycol', 'stearic acid',
]

def _classify(name: str) -> str:
    n = name.lower()
    for q in _QUESTIONED:
        if q in n: return 'commonly_questioned'
    for w in _WORTH:
        if w in n: return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'worth_knowing':
        if 'hydrogen peroxide' in n: return 'Oxidizing agent; bleaching compound'
        if 'propylene glycol' in n: return 'Humectant; may cause irritation in sensitive skin'
        if 'stearic acid' in n: return 'Fatty acid; thickening agent'
        return 'Ingredient used in regulated amounts'
    # generally_recognised
    if 'gold' in n or 'bhasma' in n: return 'Gold dust; traditional luxury ingredient'
    if 'saffron' in n: return 'Premium botanical; antioxidant and brightening'
    if 'sandalwood' in n or 'chandan' in n: return 'Cooling botanical; soothing properties'
    if 'turmeric' in n: return 'Anti-inflammatory and antioxidant botanical'
    if 'neem' in n: return 'Ayurvedic antibacterial herb'
    if 'aloe vera' in n: return 'Soothing and hydrating botanical'
    if 'honey' in n: return 'Natural humectant and antioxidant'
    if 'rose' in n: return 'Traditional botanical; hydrating and soothing'
    if 'jasmine' in n: return 'Aromatic botanical; fragrant and calming'
    if 'marigold' in n: return 'Traditional botanical; soothing properties'
    if 'almond oil' in n: return 'Cold-pressed oil; nourishing and rich'
    if 'sesame oil' in n: return 'Traditional oil; warming and nourishing'
    if 'mustard oil' in n: return 'Traditional Indian oil; stimulating properties'
    if 'ghee' in n or 'clarified butter' in n: return 'Ayurvedic butter; deeply nourishing'
    if 'wheat germ oil' in n: return 'Rich oil; vitamin E source'
    if 'coconut oil' in n: return 'Natural moisturizing oil; sustainable'
    if 'shea butter' in n: return 'Nourishing natural butter; rich in fatty acids'
    if 'cocoa butter' in n: return 'Natural moisturizer; protective'
    if 'kokum butter' in n: return 'Traditional butter; deeply moisturizing'
    if 'henna' in n: return 'Traditional botanical; conditioning properties'
    if 'bhringraj' in n: return 'Ayurvedic herb; hair strengthening'
    if 'shikakai' in n: return 'Natural cleanser; gentle on hair'
    if 'vitamin e' in n: return 'Antioxidant protection'
    if 'beeswax' in n: return 'Natural wax; protective and conditioning'
    if 'royal jelly' in n: return 'Bee product; nourishing and antioxidant'
    if 'tomato juice' in n: return 'Natural botanical; brightening properties'
    if 'multani mitti' in n or 'fullers earth' in n: return 'Clay mineral; oil-absorbing and detoxifying'
    if 'peepal' in n: return 'Ayurvedic tree bark; traditional ingredient'
    return 'Natural botanical ingredient; traditionally used'

def _reg_note(cls: str) -> str:
    if cls == 'worth_knowing': return 'Permitted ingredient; safe at regulated levels'
    return 'Approved traditional ingredient; Ayurvedic formulation'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    items = [i.strip() for i in raw.split(',')]
    return [i for i in items if len(i) > 2]

def _build_obj(name: str) -> dict:
    cls = _classify(name)
    return {
        'name': name,
        'aliases': '',
        'classification': cls,
        'one_line_note': _note(name, cls),
        'regulatory_note': _reg_note(cls),
    }

def _score(ingredient_objs: list) -> int:
    score = 100
    for ing in ingredient_objs:
        cls = ing['classification']
        if cls == 'commonly_questioned': score -= 8
        elif cls == 'worth_knowing': score -= 2
    return max(0, min(100, score))

PRODUCTS = [
    # FACE CARE
    {"name": "Forest Essentials Soundarya Radiance Cream With 24K Gold & SPF 25", "brand": "Forest Essentials", "category": "Personal Care",
     "raw": "24 Karat Gold Bhasma, Saffron Extract, Shea Butter, Sweet Almond Oil, Cow's Milk, Cold Pressed Sesame Oil, Licorice Root Extract, Turmeric Extract."},

    {"name": "Forest Essentials Advanced Eternal Youth Formula Date & Litchi", "brand": "Forest Essentials", "category": "Personal Care",
     "raw": "Date Extract, Litchi Extract, Fenugreek Seed Extract, Sweet Almond Oil, Cold Pressed Organic Mustard Oil, Pure Ghee, Vitamin E."},

    # FACIAL CLEANSERS
    {"name": "Forest Essentials Mashobra Honey, Lemon & Rosewater Cleanser", "brand": "Forest Essentials", "category": "Personal Care",
     "raw": "Raw Honey, Lemon Essential Oil, Steam Distilled Rose Water, Royal Jelly, Vitamin E, Soya Protein, Glycerin."},

    # HAIR CARE
    {"name": "Forest Essentials Bhringraj & Shikakai Hair Cleanser", "brand": "Forest Essentials", "category": "Personal Care",
     "raw": "Bhringraj Extract, Shikakai Fruit Extract, Reetha Soapnut Extract, Coconut Oil Derivatives, Henna Leaf Extract, Herbal Infusion."},

    # BODY CARE
    {"name": "Forest Essentials Velvet Silk Body Cream Indian Rose Absolute", "brand": "Forest Essentials", "category": "Personal Care",
     "raw": "Indian Rose Essential Oil, Wheat Germ Oil, Kokum Butter, Organic Beeswax, Sweet Almond Oil, Aloe Vera Juice, Vitamin E."},

    # FACIAL TONERS
    {"name": "Forest Essentials Panchpushp Facial Tonic Mist", "brand": "Forest Essentials", "category": "Personal Care",
     "raw": "Pure Steam Distilled Waters of Rose, Marigold, Jasmine, Kewda, and Saffron."},

    # FACE MASKS
    {"name": "Forest Essentials Tejasvi Brightening Facial Ubtan", "brand": "Forest Essentials", "category": "Personal Care",
     "raw": "Fresh Tomato Juice, Sandalwood Powder, Turmeric, Neem Leaf, Multani Mitti, Peepal Bark Extract."},
]

def insert(p: dict) -> bool:
    name = p['name']
    raw = p['raw']
    parsed = _parse(raw)
    ingredient_objs = [_build_obj(i) for i in parsed]
    score = _score(ingredient_objs)

    try:
        existing = supabase.from_('ai_extracted_products') \
            .select('id').ilike('name', name).limit(1).execute()
        if existing.data:
            print(f"  skip (exists): {name}")
            return False

        supabase.from_('ai_extracted_products').insert({
            'name':            name,
            'brand':           p['brand'],
            'category':        p['category'],
            'image_url':       None,
            'images':          [],
            'awareness_score': score,
            'summary': (
                f"{name} by {p['brand']}. Luxury Ayurvedic skincare. "
                f"Awareness score: {score}/100. Not a health assessment."
            ),
            'fssai_note':      'Traditional Ayurvedic formulation; premium ingredients.',
            'verdict':         'Clean luxury formulation' if score >= 95 else 'Clean formulation' if score >= 85 else 'Pure botanical blend',
            'recommendation':  'Premium daily use.' if score >= 95 else 'Suitable for regular use.',
            'ingredients':     ingredient_objs,
            'ingredients_raw': raw,
            'status':          'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Forest Essentials products...")
    inserted = 0
    for p in PRODUCTS:
        if insert(p):
            inserted += 1
        time.sleep(0.1)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
