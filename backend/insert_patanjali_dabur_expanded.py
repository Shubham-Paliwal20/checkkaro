"""
Insert expanded Patanjali & Dabur products from Expanded_Patanjali_Dabur_Database PDF (v2)
Comprehensive Ayurvedic health and wellness products with detailed ingredient declarations
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = [
    'sodium lauryl sulfate', 'sls', 'hydrogen peroxide', 'artificial flavor', 'artificial flavour',
]
_WORTH = [
    'sorbitol', 'sodium benzoate', 'potassium sorbate', 'citric acid', 'dimethicone',
    'carbomer', 'xanthan gum', 'hydrolyzed veg protein',
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
    if cls == 'commonly_questioned':
        if 'sodium lauryl sulfate' in n or 'sls' in n: return 'Anionic surfactant; can be harsh on skin'
        if 'hydrogen peroxide' in n: return 'Oxidizing agent; bleaching compound'
        return 'Commonly questioned ingredient'
    if cls == 'worth_knowing':
        if 'sorbitol' in n: return 'Sugar alcohol; sweetening agent'
        if 'sodium benzoate' in n or 'potassium sorbate' in n: return 'Preservative; safe at regulated levels'
        if 'citric acid' in n: return 'Acidity regulator; natural preservative'
        if 'dimethicone' in n: return 'Silicone; conditioning agent'
        if 'carbomer' in n: return 'Thickening agent; safe'
        if 'xanthan gum' in n: return 'Natural thickener; safe'
        return 'Moderate concern; safe in regulated amounts'
    # generally_recognised
    if 'akarkara' in n: return 'Ayurvedic herb for oral health'
    if 'neem' in n: return 'Ayurvedic antibacterial herb'
    if 'babool' in n: return 'Ayurvedic herb; gum strengthening'
    if 'tomar' in n: return 'Ayurvedic herb; oral care'
    if 'pudina' in n or 'peppermint' in n: return 'Cooling and freshening agent'
    if 'clove' in n or 'cloves' in n: return 'Natural antiseptic and analgesic'
    if 'turmeric' in n: return 'Anti-inflammatory and antioxidant'
    if 'ginger' in n or 'shunthi' in n: return 'Warming spice; digestive aid'
    if 'honey' in n: return 'Natural humectant and antioxidant'
    if 'ghee' in n: return 'Ayurvedic butter; deeply nourishing'
    if 'aloe vera' in n: return 'Soothing and healing botanical'
    if 'amla' in n: return 'Indian gooseberry; vitamin C rich'
    if 'ashwagandha' in n: return 'Adaptogenic herb; stress relief'
    if 'brahmi' in n: return 'Ayurvedic herb; cooling and calming'
    if 'bhringraj' in n: return 'Ayurvedic herb; hair strengthening'
    if 'henna' in n or 'mehandi' in n: return 'Traditional botanical; conditioning'
    if 'reetha' in n or 'soapnut' in n: return 'Natural cleanser; gentle'
    if 'shikakai' in n: return 'Natural cleanser; conditioning properties'
    if 'mint' in n: return 'Cooling and soothing botanical'
    if 'basil' in n or 'tulsi' in n: return 'Ayurvedic purifying herb'
    if 'giloy' in n: return 'Ayurvedic immune herb'
    if 'mulethi' in n or 'licorice' in n: return 'Soothing botanical; anti-inflammatory'
    if 'lauki' in n: return 'Bottle gourd; cooling and detoxifying'
    if 'isabgol' in n or 'ispaghula' in n: return 'Fiber supplement; digestive aid'
    if 'tamarind' in n: return 'Traditional digestive; tangy botanical'
    if 'cumin' in n: return 'Warming spice; digestive'
    if 'fennel' in n: return 'Cooling botanical; digestive aid'
    if 'menthol' in n: return 'Cooling compound; soothing'
    if 'sesame oil' in n: return 'Traditional oil; warming and nourishing'
    if 'coconut oil' in n: return 'Natural moisturizing oil; sustainable'
    if 'olive oil' in n: return 'Rich natural oil; antioxidant-rich'
    if 'vitamin e' in n: return 'Antioxidant protection'
    if 'saffron' in n: return 'Premium botanical; antioxidant and brightening'
    return 'Natural botanical ingredient; safe'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Subject to regulatory scrutiny; permitted by FSSAI'
    if cls == 'worth_knowing': return 'Permitted ingredient; safe at regulated levels'
    return 'Approved Ayurvedic formulation'

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
    # PATANJALI ORAL CARE
    {"name": "Patanjali Dant Kanti Regular", "brand": "Patanjali", "category": "Personal Care",
     "raw": "Akarkara, Neem, Babool, Tomar, Pudina, Cloves, Pippali, Vajradanti, Meswak, Majuphal, Vidang, Calcium Carbonate base, Sorbitol, Silica, Sodium Lauryl Sulfate."},

    {"name": "Patanjali Dant Kanti Advanced", "brand": "Patanjali", "category": "Personal Care",
     "raw": "Clove, Tomar, Akarkara, Babool, Neem, Meswak, Guggul, Khair, Apamarg, Kantkari, Tulsi, Cinnamon, Mulethi."},

    {"name": "Patanjali Dant Kanti Fresh Active Gel", "brand": "Patanjali", "category": "Personal Care",
     "raw": "Aloe Vera, Clove oil, Ginger, Mint, Basil, Fennel, Menthol, Sorbitol, Hydrated Silica, PEG, Sodium Benzoate."},

    # PATANJALI HEALTH
    {"name": "Patanjali Lauki-Ghanvati", "brand": "Patanjali", "category": "Health",
     "raw": "Lauki (Bottle Gourd) extract, Base material q.s."},

    {"name": "Patanjali Ashwagandha Capsules", "brand": "Patanjali", "category": "Health",
     "raw": "Pure extract of Ashwagandha (Withania somnifera) 390mg, Powder of Ashwagandha 60mg."},

    {"name": "Patanjali Aloe Vera Juice (Fiber)", "brand": "Patanjali", "category": "Health",
     "raw": "Aloe Vera Leaf Juice 9.47ml, Citric Acid, Sodium Benzoate, Potassium Sorbate."},

    {"name": "Patanjali Giloy Ghanvati", "brand": "Patanjali", "category": "Health",
     "raw": "Giloy (Tinospora cordifolia) stem extract 500mg."},

    {"name": "Patanjali Tulsi Ghanvati", "brand": "Patanjali", "category": "Health",
     "raw": "Tulsi (Ocimum sanctum) extract 500mg."},

    # PATANJALI PERSONAL CARE
    {"name": "Patanjali Saundarya Neem-Tulsi Face Wash", "brand": "Patanjali", "category": "Personal Care",
     "raw": "Aqua, Neem, Tulsi, Aloe Vera, Vitamin E, Vitamin B5, Honey, SLES, Carbomer."},

    {"name": "Patanjali Saundarya Aloe Vera Gel (Kesar Chandan)", "brand": "Patanjali", "category": "Personal Care",
     "raw": "Aloe Vera Gel, Kesar (Saffron), Chandan (Sandalwood) extract, Vitamin E, Permitted color and fragrance."},

    {"name": "Patanjali Kesh Kanti Hair Oil", "brand": "Patanjali", "category": "Personal Care",
     "raw": "Brahmi, Amla, Bhringraj, Mehandi, Neem Leaf, Yashti-Madhu, Ghrit Kumari, Jatamansi, Sesame Oil, Coconut Oil."},

    {"name": "Patanjali Kesh Kanti Reetha Hair Cleanser", "brand": "Patanjali", "category": "Personal Care",
     "raw": "Reetha, Shikakai, Amla, Bakuchi, Neem, Mehandi, SLES, Dimethicone, Aqua."},

    # PATANJALI FOOD
    {"name": "Patanjali Mixed Fruit Jam", "brand": "Patanjali", "category": "Food",
     "raw": "Sugar, Fruit Pulp (45%), Pectin, Citric Acid, Sodium Benzoate."},

    {"name": "Patanjali Honey", "brand": "Patanjali", "category": "Food",
     "raw": "100% Pure Natural Honey."},

    {"name": "Patanjali Atta Noodles (Classic)", "brand": "Patanjali", "category": "Food",
     "raw": "Wheat Flour (Atta) 80%, Refined Sunflower Oil, Salt, Wheat Gluten. Masala: Spices, Sugar, Garlic, Onion, Hydrolyzed Veg Protein."},

    # DABUR HEALTH
    {"name": "Dabur Chyawanprash Awaleha", "brand": "Dabur", "category": "Health",
     "raw": "Amla, Sugar, Honey, Ghee, Pippali, Ashwagandha, Shatavari, Giloy, Mulethi, Dashmool, Cinnamon, Saffron."},

    {"name": "Dabur Lavanbhaskar Churna", "brand": "Dabur", "category": "Health",
     "raw": "Samudra Lavana, Souvarchala Lavana, Vida Lavana, Saindhava Lavana, Dhanyaka, Pippali, Shweta Jiraka, Nagkesar, Talispatra."},

    {"name": "Dabur Honitus Herbal Lozenges", "brand": "Dabur", "category": "Health",
     "raw": "Shunthi, Mulethi, Tulsi, Haritaki, Menthol, Sugar Base."},

    {"name": "Dabur Janma Ghunti", "brand": "Dabur", "category": "Health",
     "raw": "Aniseed, Ajwain, Amaltas, Sanai, Vacha, Palasbeej, Honey."},

    {"name": "Dabur Nature Care Regular (Isabgol)", "brand": "Dabur", "category": "Health",
     "raw": "Isabgol (Ispaghula) Husk, Sarjika Kshara, Citric Acid."},

    # DABUR ORAL CARE
    {"name": "Dabur Red Gel", "brand": "Dabur", "category": "Personal Care",
     "raw": "Laung (Clove), Tomar, Pudina (Mint), Gairic Powder, Sorbitol, Silica, Sodium Benzoate."},

    {"name": "Dabur Babool Toothpaste", "brand": "Dabur", "category": "Personal Care",
     "raw": "Babool (Acacia Arabica) extract, Calcium Carbonate, Sorbitol, Silica, Sodium Lauryl Sulfate, Flavor."},

    # DABUR PERSONAL CARE
    {"name": "Dabur Vatika Enriched Coconut Hair Oil", "brand": "Dabur", "category": "Personal Care",
     "raw": "Coconut Oil, Brahmi, Amla, Bahera, Kapurkachri, Henna, Lemon oil."},

    {"name": "Dabur Fem Fairness Naturals Saffron Bleach", "brand": "Dabur", "category": "Personal Care",
     "raw": "Aqua, Hydrogen Peroxide, Stearic Acid, Saffron extract, Vitamin E, Propylene Glycol."},

    {"name": "Dabur DermoViva Soap", "brand": "Dabur", "category": "Personal Care",
     "raw": "Sodium Palmate, Sodium Palm Kernelate, Olive oil, Black Seed oil, Garlic extract, Fragrance."},

    # DABUR FOOD
    {"name": "Dabur Real Fruit Power Guava", "brand": "Dabur", "category": "Food",
     "raw": "Water, Guava Pulp (25%), Sugar, Citric Acid, Stabilizer (INS 440), Antioxidant (INS 300)."},

    {"name": "Dabur Hommade Ginger Garlic Paste", "brand": "Dabur", "category": "Food",
     "raw": "Ginger (44%), Garlic (36%), Water, Salt, Acidity Regulator (INS 330, 260), Stabilizer (INS 415)."},

    {"name": "Dabur Hajmola Imli", "brand": "Dabur", "category": "Food",
     "raw": "Imli (Tamarind) extract, Black Salt, Rock Salt, Cumin, Black Pepper, Ginger, Long Pepper."},
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
                f"{name} by {p['brand']}. Ayurvedic wellness product. "
                f"Awareness score: {score}/100. Not a health assessment or medical advice."
            ),
            'fssai_note':      'Traditional Ayurvedic formulation; permitted by FSSAI.',
            'verdict':         'Pure botanical blend' if score >= 95 else 'Clean formulation' if score >= 85 else 'Ayurvedic blend',
            'recommendation':  'Suitable for daily use.' if score >= 85 else 'Use as directed.',
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
    print(f"Inserting {len(PRODUCTS)} Patanjali & Dabur expanded products...")
    inserted = 0
    for p in PRODUCTS:
        if insert(p):
            inserted += 1
        time.sleep(0.1)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
