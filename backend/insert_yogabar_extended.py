"""
Insert YogaBar extended portfolio from YogaBar_Extended_Portfolio PDF
Phase II specialized nutrition and clean label expansion
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = []
_WORTH = [
    'rosemary extract', 'prebiotic fiber', 'fructooligosaccharides',
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
        if 'rosemary extract' in n: return 'Natural antioxidant; preservative'
        if 'prebiotic' in n or 'fructooligosaccharides' in n: return 'Prebiotic fiber; digestive health'
        return 'Natural additive; safe ingredient'
    # generally_recognised
    if 'rolled oats' in n or 'oats' in n: return 'Whole grain; nutritious and filling'
    if 'dried apples' in n or 'apple' in n: return 'Natural fruit; vitamin C rich'
    if 'blueberr' in n: return 'Antioxidant-rich berry'
    if 'dates' in n: return 'Natural sweetener; fiber and minerals'
    if 'almonds' in n or 'almond' in n: return 'Tree nut; protein and healthy fats'
    if 'cashews' in n or 'cashew' in n: return 'Tree nut; mineral-rich'
    if 'honey' in n: return 'Natural sweetener; antioxidant'
    if 'cinnamon' in n: return 'Spice; warming and flavor'
    if 'dark chocolate' in n or 'cocoa' in n: return 'Rich cocoa; antioxidant-rich'
    if 'cocoa butter' in n: return 'Natural fat; smooth texture'
    if 'sunflower oil' in n: return 'Plant oil; vitamin E rich'
    if 'rice bran oil' in n: return 'Plant oil; nutritious'
    if 'flax' in n or 'flaxseed' in n: return 'Seed; omega-3 and fiber'
    if 'chia' in n or 'chia seed' in n: return 'Seed; protein and fiber'
    if 'seed' in n: return 'Nutritious seed'
    if 'vanilla' in n: return 'Natural flavor; aromatic'
    if 'bacillus coagulans' in n: return 'Probiotic strain; gut health'
    if 'pumpkin seed' in n: return 'Nutritious seed; minerals'
    if 'cranberries' in n or 'cranberry' in n: return 'Antioxidant berry; tart flavor'
    if 'strawberr' in n: return 'Antioxidant berry; vitamin C'
    if 'brown rice' in n or 'rice' in n: return 'Whole grain; nutritious'
    if 'muesli' in n: return 'Mixed grain cereal; balanced nutrition'
    if 'whole grain' in n or 'whole grains' in n: return 'Nutritious grain blend'
    if 'chocolate filling' in n: return 'Chocolate component; cocoa-based'
    if 'pea protein' in n: return 'Plant-based protein; complete amino acids'
    if 'cocoa solids' in n: return 'Cocoa component; antioxidants'
    if 'salt' in n: return 'Mineral seasoning'
    if 'apple cider vinegar' in n: return 'Fermented vinegar; digestive aid'
    if 'raw' in n and 'unfiltered' in n: return 'Raw and unfiltered; living enzymes'
    if '100% roasted' in n: return 'Pure roasted nut butter; no additives'
    if 'roasted almonds' in n: return 'Roasted for flavor; protein-rich'
    if 'roasted cashews' in n: return 'Roasted for flavor; mineral-rich'
    return 'Natural whole food ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'worth_knowing': return 'Natural additive; safe and permitted'
    return 'Clean label ingredient; natural and whole food'

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
        if cls == 'worth_knowing': score -= 1
    return max(0, min(100, score))

PRODUCTS = [
    # BREAKFAST BARS
    {"name": "YogaBar Apple Cinnamon Oats Bar", "brand": "YogaBar", "category": "Food",
     "raw": "Rolled Oats (42%), Dried Apples (12%), Dates, Almonds, Honey, Cinnamon, Rice Bran Oil, Rosemary Extract."},

    {"name": "YogaBar Blueberry Pie Oats Bar", "brand": "YogaBar", "category": "Food",
     "raw": "Rolled Oats, Dried Blueberries (10%), Dates, Cashews, Honey, Seeds (Flax, Chia), Natural Blueberry Flavor."},

    # DESSERT BARS
    {"name": "YogaBar Chocolate Brownie Energy Bar", "brand": "YogaBar", "category": "Food",
     "raw": "Whole Grains (Oats, Brown Rice), Dates, Cashews, Almonds, Dark Chocolate (Cocoa Solids, Sugar, Cocoa Butter), Cocoa Powder, Honey, Sunflower Oil."},

    {"name": "YogaBar Vanilla Almond Energy Bar", "brand": "YogaBar", "category": "Food",
     "raw": "Whole Grains (Oats, Brown Rice), Almonds (18%), Dates, Honey, Vanilla Extract, Seeds (Sunflower, Pumpkin), Rice Bran Oil."},

    # HEALTHY SNACKS
    {"name": "YogaBar Probiotic Muesli - Berry Mix", "brand": "YogaBar", "category": "Food",
     "raw": "Whole Grains (Oats, Ragi, Bajra), Dried Berries (Cranberries, Strawberries), Probiotic Culture (Bacillus Coagulans), Honey, Almonds, Pumpkin Seeds."},

    {"name": "YogaBar High Fiber Choco-Fills (Cereal)", "brand": "YogaBar", "category": "Food",
     "raw": "Multigrain Flour (Oats, Rice, Ragi), Chocolate Filling (Sugar, Edible Vegetable Oil, Cocoa Solids), Pea Protein, Cocoa Powder, Salt."},

    # JUICES & DRINKS
    {"name": "YogaBar Apple Cider Vinegar (with Mother)", "brand": "YogaBar", "category": "Food",
     "raw": "100% Natural Apple Cider Vinegar (Raw, Unfiltered, Unpasteurized)."},

    # NUT BUTTERS
    {"name": "YogaBar Almond Butter (Pure Roasted)", "brand": "YogaBar", "category": "Food",
     "raw": "100% Roasted Almonds. (No added oils, sugars, or preservatives)."},

    {"name": "YogaBar Cashew Butter", "brand": "YogaBar", "category": "Food",
     "raw": "100% Roasted Cashews."},
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
                f"{name} by {p['brand']}. Clean label nutrition product. "
                f"Awareness score: {score}/100. No artificial additives."
            ),
            'fssai_note':      'Clean label formulation; whole food ingredients.',
            'verdict':         'Excellent formulation' if score >= 98 else 'Clean nutrition bar',
            'recommendation':  'Perfect for daily consumption; nutritious and natural.',
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
    print(f"Inserting {len(PRODUCTS)} YogaBar extended portfolio products...")
    inserted = 0
    for p in PRODUCTS:
        if insert(p):
            inserted += 1
        time.sleep(0.1)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
