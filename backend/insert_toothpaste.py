"""
Insert toothpaste products from Common Toothpaste Products Registry PDF
Includes Colgate, Sensodyne, Pepsodent, Dabur, Patanjali, Close-Up, Oral-B, Vicco, Himalaya
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_BANNED = ['triclosan']
_QUESTIONED = [
    'sodium lauryl sulfate', 'sls', 'sodium saccharin', 'artificial color', 'ci 16035', 'ci 17200',
]
_WORTH = ['calcium carbonate', 'titanium dioxide', 'sorbitol', 'xanthan gum']

def _classify(name: str) -> str:
    n = name.lower()
    for b in _BANNED:
        if b in n: return 'banned'
    for q in _QUESTIONED:
        if q in n: return 'commonly_questioned'
    for w in _WORTH:
        if w in n: return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'banned':
        if 'triclosan' in n: return 'Antimicrobial; banned in several countries'
        return 'Banned or restricted ingredient'
    if cls == 'commonly_questioned':
        if 'sodium lauryl sulfate' in n or 'sls' in n: return 'Harsh surfactant; can irritate gums'
        if 'sodium saccharin' in n: return 'Artificial sweetener; debated safety'
        if 'ci 16035' in n or 'ci 17200' in n: return 'Artificial colour; azo dye'
        return 'Commonly questioned ingredient'
    if cls == 'worth_knowing':
        if 'calcium carbonate' in n: return 'Abrasive and whitening agent; mild'
        if 'sorbitol' in n: return 'Sugar alcohol; sweetening agent'
        if 'titanium dioxide' in n: return 'Whitening agent; safe'
        return 'Moderate concern; safe in regulated amounts'
    # generally_recognised
    if 'fluoride' in n: return 'Cavity protection; FDA-approved'
    if 'potassium nitrate' in n: return 'Desensitizing agent for sensitive teeth'
    if 'neem' in n: return 'Ayurvedic antibacterial herb'
    if 'clove' in n: return 'Natural antiseptic and analgesic'
    if 'mint' in n or 'peppermint' in n: return 'Cooling and freshening agent'
    if 'aloe vera' in n: return 'Soothing botanical'
    if 'glycerin' in n: return 'Humectant and sweetener'
    if 'peppali' in n or 'pipali' in n: return 'Ayurvedic warming spice'
    if 'ajwain' in n or 'akarkara' in n: return 'Ayurvedic herbs for oral health'
    if 'babool' in n: return 'Ayurvedic herb; gum strengthening'
    if 'tomar' in n: return 'Ayurvedic herb; oral care'
    if 'herb' in n: return 'Natural herbal ingredient'
    return 'Generally recognised as safe'

def _reg_note(cls: str) -> str:
    if cls == 'banned': return 'Banned in multiple countries'
    if cls == 'commonly_questioned': return 'Subject to regulatory scrutiny; permitted by FSSAI'
    if cls == 'worth_knowing': return 'Permitted ingredient; safe at regulated levels'
    return 'Approved for oral care use'

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
        if cls == 'banned': score -= 50
        elif cls == 'commonly_questioned': score -= 10
        elif cls == 'worth_knowing': score -= 3
    return max(0, min(100, score))

PRODUCTS = [
    # COLGATE
    {"name": "Colgate Strong Teeth Toothpaste", "brand": "Colgate", "category": "Personal Care",
     "raw": "Calcium Carbonate, Sorbitol, Sodium Lauryl Sulfate, Silica, Titanium Dioxide, Sodium Silicate, Carrageenan, Sodium Monofluorophosphate (Source of Fluoride), Sodium Saccharin, Flavor, Water."},
    {"name": "Colgate Visible White", "brand": "Colgate", "category": "Personal Care",
     "raw": "Silica, Sorbitol, Glycerin, Polyethylene Glycol, Tetrapotassium Pyrophosphate, Tetrasodium Pyrophosphate, Sodium Lauryl Sulfate, Flavor, Cocamidopropyl Betaine, Sodium Saccharin, Sodium Fluoride."},

    # SENSODYNE
    {"name": "Sensodyne Fresh Gel Sensitivity Relief", "brand": "Sensodyne", "category": "Personal Care",
     "raw": "Water, Sorbitol, Hydrated Silica, Glycerin, Potassium Nitrate (Desensitizing agent), Cocamidopropyl Betaine, Flavor, Xanthan Gum, CI 42090, Sodium Fluoride (0.221% w/w), Sodium Saccharin."},

    # PEPSODENT
    {"name": "Pepsodent Germicheck 2-in-1", "brand": "Pepsodent", "category": "Personal Care",
     "raw": "Calcium Carbonate, Water, Sorbitol, Hydrated Silica, Sodium Lauryl Sulfate, Flavor, Cellulose Gum, Sodium Silicate, Benzyl Alcohol, Sodium Saccharin, Sodium Monofluorophosphate, Triclosan."},

    # DABUR
    {"name": "Dabur Red Toothpaste", "brand": "Dabur", "category": "Personal Care",
     "raw": "Calcium Carbonate, Sorbitol, Water, Silica, Sodium Lauryl Sulfate, Herbal Extract (Clove, Mint, Tomar, Ginger, Pippali), Red Ochre (Geru), Flavor, Sodium Silicate, Xanthan Gum, Sodium Saccharin."},

    # PATANJALI
    {"name": "Patanjali Dant Kanti", "brand": "Patanjali", "category": "Personal Care",
     "raw": "Calcium Carbonate, Sorbitol, Aqua, Glycerin, Hydrated Silica, Sodium Lauryl Sulfate, Herbal Extracts (Akarkara, Neem, Babool, Tomar, Pudina, Cloves, Pippali, Vajradanti, Meswak, Majuphal), Flavor."},

    # CLOSE-UP
    {"name": "Close-Up Everfresh Red Hot Gel", "brand": "Close-Up", "category": "Personal Care",
     "raw": "Sorbitol, Water, Hydrated Silica, Sodium Lauryl Sulfate, PEG-32, Flavor, Cellulose Gum, Sodium Fluoride, Sodium Saccharin, Zinc Sulfate, CI 16035, CI 17200."},

    # ORAL-B
    {"name": "Oral-B Pro-Expert Healthy White", "brand": "Oral-B", "category": "Personal Care",
     "raw": "Glycerin, Hydrated Silica, Sodium Hexametaphosphate, Propylene Glycol, PEG-6, Water, Zinc Lactate, Sodium Lauryl Sulfate, Flavor, Sodium Gluconate, Stannous Fluoride, Carrageenan, Sodium Saccharin."},

    # VICCO
    {"name": "Vicco Vajradanti Paste", "brand": "Vicco", "category": "Personal Care",
     "raw": "Water, Calcium Carbonate, Sorbitol, 18 Ayurvedic Herbs (Bakul, Babool, Akrod, Dalchini, Patang, Vajradanti, Lavang, Manjistha), Gum Tragacanth."},

    # HIMALAYA
    {"name": "Himalaya Complete Care Toothpaste", "brand": "Himalaya", "category": "Personal Care",
     "raw": "Sorbitol, Water, Hydrated Silica, Glycerin, Silica, Sodium Lauryl Sulfate, Flavor, Gums (Meswak, Neem, Pomegranate Peel), Sodium Saccharin, Calcium Fluoride (500 ppm F)."},
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
                f"{name} by {p['brand']}. Awareness score: {score}/100. "
                "Not a health assessment or medical advice."
            ),
            'fssai_note':      'Subject to applicable oral care regulations.',
            'verdict':         'Clean formulation' if score >= 80 else 'Average formulation' if score >= 60 else 'Review before use',
            'recommendation':  'Suitable for daily use.' if score >= 80 else 'Test for sensitivity.' if score >= 60 else 'Consult dentist.',
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
    print(f"Inserting {len(PRODUCTS)} toothpaste products...")
    inserted = 0
    for p in PRODUCTS:
        if insert(p):
            inserted += 1
        time.sleep(0.1)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
