"""
Insert YogaBar full product registry from YogaBar_Full_Product_Registry PDF
Nutrition-first ingredients and formulation guide
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
        if 'rosemary extract' in n: return 'Natural antioxidant preservative'
        if 'prebiotic' in n or 'fructooligosaccharides' in n: return 'Prebiotic fiber; digestive support'
        return 'Natural additive; safe ingredient'
    # generally_recognised
    if 'rolled oats' in n or 'oats' in n: return 'Whole grain; nutritious and satiating'
    if 'brown rice' in n: return 'Whole grain; balanced nutrients'
    if 'ragi' in n or 'millet' in n: return 'Ancient grain; mineral-rich'
    if 'bajra' in n: return 'Millet grain; nutritious'
    if 'dark chocolate' in n or 'cocoa' in n: return 'Rich cocoa; antioxidant-rich'
    if 'cranberries' in n: return 'Antioxidant berry'
    if 'almonds' in n: return 'Tree nut; protein and healthy fats'
    if 'cashews' in n: return 'Tree nut; mineral-rich'
    if 'apricots' in n: return 'Stone fruit; vitamin A rich'
    if 'dates' in n: return 'Natural sweetener; minerals and fiber'
    if 'honey' in n: return 'Natural sweetener; antioxidant'
    if 'pumpkin seeds' in n: return 'Nutritious seed; magnesium-rich'
    if 'chia seed' in n: return 'Superfood seed; omega-3 and fiber'
    if 'sunflower seed' in n or 'flax' in n: return 'Nutritious seed; healthy fats'
    if 'turmeric' in n: return 'Spice; anti-inflammatory'
    if 'ginger' in n: return 'Spice; warming and digestive'
    if 'black pepper' in n or 'pepper' in n: return 'Spice; flavor and bioavailability'
    if 'cinnamon' in n: return 'Spice; warming properties'
    if 'jaggery' in n: return 'Unrefined sweetener; minerals'
    if 'watermelon seed' in n: return 'Nutritious seed; hydrating'
    if 'moong dal' in n or 'lentil' in n: return 'Legume; protein-rich'
    if 'cumin' in n: return 'Spice; digestive aid'
    if 'curry leaves' in n: return 'Botanical; traditional ingredient'
    if 'peanuts' in n or 'peanut' in n: return 'Legume; protein and fats'
    if 'pea protein' in n: return 'Plant-based protein; complete amino acids'
    if 'cocoa powder' in n: return 'Cocoa component; antioxidants'
    if 'cocoa butter' in n: return 'Natural fat; smooth texture'
    if 'whey protein' in n: return 'Dairy protein; amino acid profile'
    if 'milk protein' in n: return 'Dairy protein; complete amino acids'
    if 'hazelnuts' in n: return 'Tree nut; rich and creamy'
    if 'sea salt' in n: return 'Mineral seasoning; pure salt'
    if 'sunflower oil' in n: return 'Plant oil; vitamin E rich'
    if 'rice bran oil' in n: return 'Plant oil; nutritious'
    if 'dehydrated' in n: return 'Preserved vegetable; concentrated nutrients'
    if 'vegetable' in n: return 'Whole vegetable ingredient'
    if 'spice' in n: return 'Botanical spice; traditional'
    return 'Natural whole food ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'worth_knowing': return 'Natural additive; safe and permitted'
    return 'Clean label ingredient; natural whole food'

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
    # BREAKFAST MUESLI
    {"name": "YogaBar Dark Chocolate + Cranberry Muesli", "brand": "YogaBar", "category": "Food",
     "raw": "Whole Grains (50%) [Rolled Oats, Brown Rice, Ragi], Dried Cranberries, Dark Chocolate (10%) [Sugar, Cocoa Butter, Cocoa Solids], Almonds, Pumpkin Seeds, Chia Seeds, Honey, Date Syrup, Rice Bran Oil."},

    {"name": "YogaBar Turmeric + Ginger Muesli", "brand": "YogaBar", "category": "Food",
     "raw": "Whole Grains [Oats, Brown Rice], Turmeric Powder, Ginger Powder, Almonds, Watermelon Seeds, Dates, Honey, Jaggery, Cinnamon, Black Pepper."},

    # ENERGY BARS
    {"name": "YogaBar Multigrain Energy Bar - Chocolate", "brand": "YogaBar", "category": "Food",
     "raw": "Whole Grains (40%) [Oats, Ragi, Bajra], Seeds (15%) [Sunflower, Pumpkin, Flax], Dates, Honey, Dark Chocolate, Almonds, Peanut Butter, Cocoa Powder."},

    {"name": "YogaBar Nutty Apricot Energy Bar", "brand": "YogaBar", "category": "Food",
     "raw": "Apricots (20%), Dates, Almonds (15%), Cashews, Whole Grains [Oats, Brown Rice], Honey, Seeds [Flax, Sunflower], Cinnamon."},

    # OATS
    {"name": "YogaBar Veggie Masala Oats", "brand": "YogaBar", "category": "Food",
     "raw": "Rolled Oats (75%), Dehydrated Vegetables (10%) [Carrot, Green Peas, Onion], Spices and Condiments [Turmeric, Cumin, Pepper, Chili], Salt, Rice Bran Oil."},

    {"name": "YogaBar Dal Khichdi Oats", "brand": "YogaBar", "category": "Food",
     "raw": "Rolled Oats, Moong Dal (Yellow Lentil), Spices [Cumin, Ginger, Turmeric], Curry Leaves, Salt, Dehydrated Carrots."},

    # PEANUT BUTTER
    {"name": "YogaBar Crunchy Peanut Butter (Pure)", "brand": "YogaBar", "category": "Food",
     "raw": "100% Roasted Peanuts. (No Added Sugar, No Added Salt, No Hydrogenated Oils)."},

    {"name": "YogaBar Dark Chocolate Peanut Butter", "brand": "YogaBar", "category": "Food",
     "raw": "Roasted Peanuts (80%), Dark Chocolate, Cocoa Powder, Organic Jaggery, Sea Salt."},

    # PROTEIN BARS
    {"name": "YogaBar Chocolate Cranberry (20g Protein)", "brand": "YogaBar", "category": "Food",
     "raw": "Whey Protein Isolate, Milk Protein, Almonds, Cashews, Dates, Cranberries (10%), Cocoa Powder, Honey, Prebiotic Fiber (Fructooligosaccharides), Sunflower Oil, Rosemary Extract."},

    {"name": "YogaBar Hazelnut Toffee (20g Protein)", "brand": "YogaBar", "category": "Food",
     "raw": "Whey Protein Isolate, Milk Protein, Hazelnuts (12%), Dates, Honey, Cocoa Powder, Sea Salt, Prebiotic Fiber, Sunflower Oil, Natural Flavors."},
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
                f"{name} by {p['brand']}. Nutrition-first formulation. "
                f"Awareness score: {score}/100. No artificial additives."
            ),
            'fssai_note':      'Clean label formulation; whole food focus.',
            'verdict':         'Excellent formulation' if score >= 98 else 'Clean nutrition product',
            'recommendation':  'Perfect daily nutritious choice; wholesome ingredients.',
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
    print(f"Inserting {len(PRODUCTS)} YogaBar registry products...")
    inserted = 0
    for p in PRODUCTS:
        if insert(p):
            inserted += 1
        time.sleep(0.1)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
