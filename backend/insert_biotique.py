"""
Insert Biotique Advanced Ayurveda products into ai_extracted_products.
Data extracted directly from Biotique_Clinical_Database.pdf
"""
import os, re, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_BANNED = [
    'triclosan','formaldehyde','hydroquinone','mercury','lead',
    'methylparaben','propylparaben','butylparaben','ethylparaben',
    'sodium nitrite','potassium bromate','azodicarbonamide',
]
_QUESTIONED = [
    'sodium lauryl sulfate','sls','sodium laureth sulfate','sles',
    'phthalate','artificial color','artificial colour','titanium dioxide',
    'sodium benzoate','potassium sorbate','tetrasodium edta',
    'propylene glycol','polyethylene glycol','sucralose','aspartame',
    'fragrance','parfum',
]
_WORTH = [
    'palm oil','palmolein','vegetable oil','edible vegetable fat',
    'mineral oil','paraffin','petroleum','silicone','dimethicone',
    'beeswax','cream base','soya oil',
]

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
    if cls == 'banned': return 'Banned or restricted ingredient'
    if cls == 'commonly_questioned': return 'Commonly questioned ingredient'
    if cls == 'worth_knowing':
        if 'beeswax' in n: return 'Natural wax; generally safe, not vegan'
        if 'cream base' in n: return 'Proprietary base; individual ingredients not disclosed'
        if 'soya' in n or 'soy' in n: return 'Soy-derived oil; common allergen for some'
        return 'Moderate concern; safe in regulated amounts'
    # generally_recognised — botanical-specific notes
    if 'neem' in n: return 'Ayurvedic antibacterial and antifungal herb'
    if 'bhringraj' in n: return 'Ayurvedic herb known for hair growth support'
    if 'amla' in n: return 'Rich in Vitamin C; strengthens hair and skin'
    if 'ritha' in n: return 'Natural saponin-based cleanser (soapnut)'
    if 'badam' in n or 'almond' in n: return 'Almond oil; rich in Vitamin E and fatty acids'
    if 'haldi' in n or 'turmeric' in n: return 'Turmeric; anti-inflammatory and antioxidant'
    if 'coconut' in n: return 'Coconut oil; moisturising and antimicrobial'
    if 'brahmi' in n: return 'Ayurvedic herb used for scalp and cognitive health'
    if 'shikakai' in n: return 'Natural hair cleanser with low pH'
    if 'manjistha' in n: return 'Ayurvedic herb used for skin brightening'
    if 'mulethi' in n or 'licorice' in n: return 'Licorice root; brightening and anti-inflammatory'
    if 'peppermint' in n: return 'Natural cooling and antiseptic essential oil'
    if 'honey' in n or 'madhu' in n: return 'Natural humectant and antimicrobial'
    if 'sunflower' in n or 'surajmukhi' in n: return 'Sunflower oil; rich in linoleic acid'
    if 'dandelion' in n: return 'Antioxidant-rich plant extract'
    if 'sea kelp' in n: return 'Marine algae; rich in minerals and iodine'
    if 'himalayan water' in n or 'purified water' in n: return 'Pure water base'
    if 'lavang' in n or 'clove' in n: return 'Clove oil; antiseptic and antimicrobial'
    if 'pineapple' in n: return 'Natural source of bromelain enzyme'
    if 'cucumber' in n: return 'Soothing and hydrating botanical'
    if 'apple' in n: return 'Natural fruit extract with antioxidants'
    if 'papaya' in n or 'papita' in n: return 'Contains papain enzyme; gentle exfoliant'
    if 'apricot' in n or 'khubani' in n: return 'Apricot kernel oil; nourishing emollient'
    if 'til' in n or 'sesame' in n: return 'Sesame oil; rich in antioxidants'
    if 'wheat' in n or 'gehun' in n: return 'Wheat germ; rich in Vitamin E'
    if 'ghritkumari' in n or 'kumari' in n or 'aloe' in n: return 'Aloe vera; soothing and hydrating'
    return 'Botanical/natural ingredient; generally safe'

def _reg_note(cls: str) -> str:
    if cls == 'banned': return 'Banned or restricted in EU and multiple countries'
    if cls == 'commonly_questioned': return 'Subject to regulatory scrutiny; check label'
    if cls == 'worth_knowing': return 'Permitted ingredient; use as directed'
    return 'Natural botanical; compliant with Ayurvedic product standards'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    # Remove "q.s." suffix items
    items = [i.strip().replace(' q.s.', '').strip() for i in raw.split(',')]
    return [i for i in items if len(i) > 1]

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
        elif cls == 'commonly_questioned': score -= 15
        elif cls == 'worth_knowing': score -= 5
    return max(0, min(100, score))

def _verdict(score: int) -> str:
    if score >= 80: return 'Clean formulation'
    if score >= 60: return 'Average formulation'
    if score >= 40: return 'Worth reviewing'
    return 'Review carefully'

def _recommendation(score: int) -> str:
    if score >= 80: return 'Botanical formulation. Generally suitable. Check for individual plant allergies.'
    if score >= 60: return 'Suitable for most. Some ingredients may warrant attention for sensitive skin.'
    if score >= 40: return 'Review before regular use, especially for sensitive individuals.'
    return 'Consider checking with a professional before use.'

PRODUCTS = [
    # FACE WASH / CLEANSER
    {"name": "Biotique Bio Papaya Visibly Flawless Gel Face Wash", "category": "Skincare",
     "raw": "Papita Juice, Akrot Shell Powder, Neem Bark, Banhaldi Root, Ritha Fruit, Kikar Gond, Purified Water q.s."},
    {"name": "Biotique Bio Honey Gel Refreshing Foaming Face Wash", "category": "Skincare",
     "raw": "Arjun Bark, Chhoti Dudhi Plant, Banhaldi Root, Ritha Fruit, Honey, Himalayan Water q.s."},
    {"name": "Biotique Bio Pineapple Oil-Control Foaming Face Cleanser", "category": "Skincare",
     "raw": "Gazar Seed, Haldi Root, Neem Bark, Lavang Oil, Pineapple Fruit, Himalayan Water q.s."},
    {"name": "Biotique Bio Almond Oil Soothing Face & Eye Makeup Cleanser", "category": "Skincare",
     "raw": "Kusumbhi Oil, Erandi Oil, Neem Oil, Soya Oil, Badam Oil, Beeswax."},

    # TONER
    {"name": "Biotique Bio Cucumber Pore Tightening Toner", "category": "Skincare",
     "raw": "Daruhaldi Root, Dhania Fruit, Majuphal Fruit, Peppermint Oil, Cucumber Juice, Himalayan Water q.s."},

    # LIP CARE
    {"name": "Biotique Bio Fruit Whitening Lip Balm", "category": "Skincare",
     "raw": "Angur Fruit, Vach Root, Mulethi Stem, Badam Oil, Surajmukhi Oil, Kusumbhi Oil, Erandi Oil, Til Oil, Beeswax."},

    # SHAMPOO / HAIR CARE
    {"name": "Biotique Bio Kelp Protein Shampoo", "category": "Hair Care",
     "raw": "Neem Bark, Tesu Flower, Daruhaldi Root, Bhringraj Plant, Ritha Fruit, Sajjikshar, Sea Kelp, Himalayan Water q.s."},
    {"name": "Biotique Bio Green Apple Fresh Daily Purifying Shampoo", "category": "Hair Care",
     "raw": "Chinai Ghas Plant, Mandukparni Plant, Shikakai Fruit, Ghritkumari Leaf juice, Apple Juice, Himalayan Water q.s."},
    {"name": "Biotique Bio Bhringraj Therapeutic Oil", "category": "Hair Care",
     "raw": "Bhringraj Plant, Amla Fruit, Tesu Flower, Mulethi Stem, Brahmi Plant, Cow Milk, Goat Milk, Coconut Oil."},

    # MOISTURISER / LOTION / CREAM
    {"name": "Biotique Bio Morning Nectar Visibly Flawless Skin Lotion", "category": "Skincare",
     "raw": "Gehun Seed, Kumari Leaf Pulp, Madhu, Badam Oil, Mungfali Oil, Kusumbhi Oil, Purified Water q.s."},
    {"name": "Biotique Bio Coconut Whitening & Brightening Cream", "category": "Skincare",
     "raw": "Nariyal Water, Dudhal Root, Dugdh, Manjistha Root, Nimbu Leaf juice, Badam Oil, Cream Base q.s."},
    {"name": "Biotique Bio Wheat Germ Youthful Nourishing Night Cream", "category": "Skincare",
     "raw": "Ankurit Gehun Seed, Gazar Seed, Badam Oil, Kulanjan Root, Khubani Oil, Sunflower Oil, Cream Base q.s."},
    {"name": "Biotique Bio Carrot Ultra Soothing Face Lotion SPF 40", "category": "Skincare",
     "raw": "Parijat Leaf, Lodhra Bark, Gazar Seed, Surajmukhi Oil, Lodhra Bark, Himalayan Water q.s."},

    # SERUM
    {"name": "Biotique Bio Dandelion Visibly Ageless Serum", "category": "Skincare",
     "raw": "Bihidana Seed, Haldi Root, Jaiphal Oil, Badam Oil, Surajmukhi Oil, Dandelion Plant, Beeswax, Himalayan Water q.s."},

    # BODY WASH
    {"name": "Biotique Bio Apricot Refreshing Body Wash", "category": "Personal Care",
     "raw": "Khubani Kernel Oil, Wild Turmeric Root, Kuda Bark, Ritha Fruit, Himalayan Water q.s."},
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
            'brand':           'Biotique',
            'category':        p['category'],
            'image_url':       None,
            'images':          [],
            'awareness_score': score,
            'summary': (
                f"{name} by Biotique. Botanical Ayurvedic formulation. "
                f"Awareness score: {score}/100. "
                "Ingredients are based on BOTANICAL COMPOSITION declarations. "
                "Not a health assessment or medical advice."
            ),
            'fssai_note':      'Subject to applicable cosmetic regulations (BIS/Drugs & Cosmetics Act).',
            'verdict':         _verdict(score),
            'recommendation':  _recommendation(score),
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
    print(f"Inserting {len(PRODUCTS)} Biotique products...")
    inserted = 0
    for p in PRODUCTS:
        if insert(p):
            inserted += 1
        time.sleep(0.1)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
