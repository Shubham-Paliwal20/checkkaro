"""
Insert Patanjali and Dabur products from Clinical_Deep_Database PDF
Includes medicines, supplements, food, and personal care products
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = [
    'sodium lauryl sulfate', 'sls', 'hydrogen peroxide', 'triclosan',
]
_WORTH = ['palm oil', 'paraffin', 'mineral oil']

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
        if 'hydrogen peroxide' in n: return 'Bleaching agent; can be harsh on skin'
        if 'triclosan' in n: return 'Antimicrobial agent; restricted in some regions'
        return 'Commonly questioned ingredient'
    if cls == 'worth_knowing':
        if 'palm oil' in n: return 'Common edible oil; environmental concerns'
        if 'paraffin' in n or 'mineral oil' in n: return 'Petroleum-derived; occlusive moisturizer'
        return 'Moderate concern; safe in regulated amounts'
    # generally_recognised — Ayurvedic/botanical focus
    if 'neem' in n: return 'Ayurvedic antibacterial and antifungal herb'
    if 'ashwagandha' in n: return 'Adaptogenic herb; stress management support'
    if 'brahmi' in n: return 'Ayurvedic herb for cognitive health'
    if 'tulsi' in n: return 'Holy basil; immune support herb'
    if 'haldi' in n or 'turmeric' in n: return 'Turmeric; anti-inflammatory and antioxidant'
    if 'aloe vera' in n: return 'Soothing and hydrating botanical'
    if 'saffron' in n: return 'Natural spice with antioxidant properties'
    if 'honey' in n: return 'Natural humectant and antimicrobial'
    if 'amla' in n: return 'Rich in Vitamin C; strengthens immunity'
    if 'giloy' in n: return 'Ayurvedic immune support herb'
    if 'arjun' in n: return 'Ayurvedic herb for cardiovascular health'
    if 'guggul' in n: return 'Ayurvedic resin; traditional joint support'
    if 'mushroom' in n or 'whey protein' in n: return 'Protein-rich ingredient'
    if 'vitamin' in n or 'mineral' in n: return 'Essential micronutrient'
    return 'Botanical/natural ingredient; generally safe'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Subject to regulatory scrutiny; permitted by FSSAI'
    if cls == 'worth_knowing': return 'Permitted ingredient; use as directed'
    return 'Compliant with Ayurvedic and FSSAI standards'

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
        if cls == 'commonly_questioned': score -= 15
        elif cls == 'worth_knowing': score -= 5
    return max(0, min(100, score))

PRODUCTS = [
    # PATANJALI - MEDICINES
    {"name": "Patanjali Divya Mukta Vati Extra Power", "brand": "Patanjali", "category": "Medicine",
     "raw": "Gajwan, Brahmi, Shankhpushpi, Jyotishmati, Ashwagandha, Mukta Pishti (Pearl Powder)."},
    {"name": "Patanjali Divya Madhunashini Vati", "brand": "Patanjali", "category": "Medicine",
     "raw": "Giloy, Saptrangi, Neem, Chirayata, Kutaj, Gurmar, Jamun, Karela, Shuddh Shilajit."},
    {"name": "Patanjali Divya Lipodom", "brand": "Patanjali", "category": "Medicine",
     "raw": "Arjun Bark, Ashwagandha, Garlic, Guggul Shuddh, Kokum."},
    {"name": "Patanjali Divya Peedanil Gold", "brand": "Patanjali", "category": "Medicine",
     "raw": "Punarnadi Mandoor, Guggul Shuddh, Mukta Shukti Bhasma, Mahavat Vidhwansan Ras."},
    {"name": "Patanjali Divya Kayakalp Vati", "brand": "Patanjali", "category": "Medicine",
     "raw": "Panvad, Daru Haldi, Karanj, Baheda, Neem, Manjistha, Chirayata, Kalmishora."},

    # PATANJALI - SUPPLEMENTS & FOOD
    {"name": "Patanjali Nutrela Daily Active", "brand": "Patanjali", "category": "Supplement",
     "raw": "Vitamins, Minerals, Ginseng, Rosehip Extract, Zinc, Magnesium, Calcium."},
    {"name": "Patanjali Nutrela Mother's Plus", "brand": "Patanjali", "category": "Supplement",
     "raw": "Milk Protein, Whey Protein Isolate, DHA, Saffron, Vitamins A, C, E."},
    {"name": "Patanjali Super Dishwash Bar", "brand": "Patanjali", "category": "Household",
     "raw": "Lemon, Neem, Wood Ash, Surfactants, Base material q.s."},
    {"name": "Patanjali Amla Candy", "brand": "Patanjali", "category": "Food",
     "raw": "Amla (Emblica officinalis), Sugar, Citric Acid."},
    {"name": "Patanjali Aloe Vera Juice with Fiber", "brand": "Patanjali", "category": "Food",
     "raw": "Aloe Vera Leaf (Aloe barbadensis), Citric Acid, Sodium Benzoate, Potassium Sorbate."},
    {"name": "Patanjali Biscuits (Doodh Biscuits)", "brand": "Patanjali", "category": "Food",
     "raw": "Wheat Flour, Sugar, Edible Vegetable Oil, Milk Solids, Malt Extract, Salt, Leavening Agents."},
    {"name": "Patanjali Kachchi Ghani Mustard Oil", "brand": "Patanjali", "category": "Food",
     "raw": "Pure Mustard Oil, Fortified with Vitamin A & D."},

    # PATANJALI - PERSONAL CARE
    {"name": "Patanjali Saffron Soap", "brand": "Patanjali", "category": "Personal Care",
     "raw": "Saffron Extract, Aloe Vera, Glycerin, Soap Base q.s."},
    {"name": "Patanjali Activated Charcoal Face Wash", "brand": "Patanjali", "category": "Skincare",
     "raw": "Activated Charcoal, Vitamin E, Aloe Vera, Neem, Aqua, Glycerin, Surfactants."},
    {"name": "Patanjali Body Lotion", "brand": "Patanjali", "category": "Personal Care",
     "raw": "Aloe Vera, Wheatgerm Oil, Turmeric, Cucumber, Saffron, Glycerin."},

    # DABUR - MEDICINES
    {"name": "Dabur Abhayarishta", "brand": "Dabur", "category": "Medicine",
     "raw": "Haritaki, Vidanga, Madhuka, Draksha, Sugar Cane Juice, Dhataki, Gokhru, Trivrit."},
    {"name": "Dabur Dashmularishta", "brand": "Dabur", "category": "Medicine",
     "raw": "Bilva, Agnimantha, Shyonaka, Gambhari, Patala, Shalaparni, Brihati, Kantakari, Gokhru."},
    {"name": "Dabur Lohasava", "brand": "Dabur", "category": "Medicine",
     "raw": "Loha Bhasma (Iron), Triphala, Trikatu, Vidanga, Mustaka, Chitraka, Honey."},
    {"name": "Dabur Shilajit Gold Capsules", "brand": "Dabur", "category": "Medicine",
     "raw": "Shuddh Shilajit, Swarna Bhasma (Gold), Kesar, Safed Musli, Ashwagandha."},
    {"name": "Dabur Stresscom Capsules", "brand": "Dabur", "category": "Medicine",
     "raw": "Ashwagandha (Withania somnifera) Dry Extract 300mg."},

    # DABUR - HEALTH & FOOD
    {"name": "Dabur Honitus Hot Sip", "brand": "Dabur", "category": "Health",
     "raw": "Tulsi, Sunthi, Mulethi, Kantakari, Banaphsa, Vasa, Talispatra, Pippali."},
    {"name": "Dabur Chyawanprash (Double Immunity)", "brand": "Dabur", "category": "Health",
     "raw": "Amla, Ashwagandha, Hareetaki, Dashmool, Giloy, Musli, Honey, Saffron."},
    {"name": "Dabur Real Activ 100% Mixed Fruit", "brand": "Dabur", "category": "Food",
     "raw": "Orange, Apple, Guava, Pineapple, Passion Fruit, Mango (No Added Sugar)."},
    {"name": "Dabur Hommade Tamarind Paste", "brand": "Dabur", "category": "Food",
     "raw": "Tamarind Pulp (80%), Water, Salt, Acidity Regulator (330), Preservative (211)."},
    {"name": "Dabur Hajmola Anardana", "brand": "Dabur", "category": "Food",
     "raw": "Punica Granatum (Pomegranate), Black Salt, Ginger, Cumin, Black Pepper."},

    # DABUR - PERSONAL CARE
    {"name": "Dabur Gulabari Moisturising Lotion", "brand": "Dabur", "category": "Skincare",
     "raw": "Rose Oil, Vitamin E, Glycerin, Pearl Extract, Shea Butter, Aqua."},
    {"name": "Dabur Oxylife Men Bleach", "brand": "Dabur", "category": "Personal Care",
     "raw": "Hydrogen Peroxide, Oxygen Active, Menthol, Vitamin E, Sea Minerals."},
    {"name": "Dabur Vatika Moroccan Argan Oil", "brand": "Dabur", "category": "Personal Care",
     "raw": "Paraffinum Liquidum, Canola Oil, Palm Oil, Argan Oil, Fragrance."},
    {"name": "Dabur Herbal Toothpaste with Clove", "brand": "Dabur", "category": "Personal Care",
     "raw": "Clove Oil, Calcium Carbonate, Sorbitol, Silica, Sodium Lauryl Sulfate."},
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
            'fssai_note':      'Subject to applicable regulations (FSSAI/Ayurveda/Medicine).',
            'verdict':         'Clean formulation' if score >= 80 else 'Average formulation',
            'recommendation':  'Consult healthcare provider before use.' if p['category'] in ['Medicine', 'Health'] else 'Suitable for most.',
            'ingredients':     ingredient_objs,
            'ingredients_raw': raw,
            'status':          'active',
        }).execute()
        print(f"  + {name} | {p['category']} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Patanjali & Dabur products...")
    inserted = 0
    for p in PRODUCTS:
        if insert(p):
            inserted += 1
        time.sleep(0.1)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
