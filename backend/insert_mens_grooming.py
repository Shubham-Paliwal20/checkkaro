"""
Insert mens grooming products from 4 PDFs:
- Beardo (7 products from main registry + 4 extended = 11 total)
- Bombay Shaving Co (6 products)
- Biotique Extended Vol 2 (12 products)
- BSC Advanced Grooming (6 products)
Total: 35 products
"""
import os, re, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_BANNED = ['triclosan','formaldehyde','methylparaben','propylparaben','butylparaben']
_QUESTIONED = [
    'sodium lauryl sulfate','sls','sodium laureth sulfate','sles',
    'phthalate','diethyl phthalate','titanium dioxide','sodium benzoate',
    'potassium sorbate','propylene glycol','polyethylene glycol','sucralose',
    'fragrance','parfum','phenoxyethanol','dimethicone','cyclopentasiloxane',
]
_WORTH = [
    'mineral oil','vegetable oil','palm oil','beeswax','carnauba wax',
    'silicone','dimethiconol','sodium lauryl sulfate','butane','propane',
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
    if cls == 'commonly_questioned':
        if 'phthalate' in n: return 'Phthalate plasticizer; restricted in EU cosmetics'
        if 'phenoxyethanol' in n: return 'Preservative; generally safe at low concentrations'
        if 'sodium laureth' in n or 'sles' in n: return 'Mild sulfate surfactant; gentler than SLS'
        if 'dimethicone' in n or 'cyclopentasiloxane' in n: return 'Silicone conditioning agent'
        return 'Commonly questioned ingredient'
    if cls == 'worth_knowing':
        if 'mineral oil' in n: return 'Petroleum-derived occlusive; non-comedogenic'
        if 'beeswax' in n or 'carnauba wax' in n: return 'Natural wax; not vegan'
        if 'propane' in n or 'butane' in n: return 'Propellant gas; flammable'
        if 'palm oil' in n: return 'Common oil; environmental concerns'
        return 'Moderate concern; safe in regulated amounts'
    # generally_recognised
    if 'almond oil' in n: return 'Almond oil; rich in Vitamin E and omega fatty acids'
    if 'coconut oil' in n: return 'Coconut oil; moisturising and antimicrobial'
    if 'argan oil' in n: return 'Argan oil; rich in antioxidants and fatty acids'
    if 'jojoba oil' in n: return 'Jojoba oil; similar to skin sebum, non-comedogenic'
    if 'hemp seed' in n: return 'Hemp seed oil; rich in omega-3 and omega-6'
    if 'aloe vera' in n: return 'Aloe vera; soothing and hydrating'
    if 'glycerin' in n: return 'Humectant; draws moisture into skin'
    if 'vitamin e' in n: return 'Antioxidant; protects against free radicals'
    if 'neem' in n: return 'Ayurvedic antibacterial herb'
    if 'turmeric' in n or 'haldi' in n: return 'Natural anti-inflammatory and brightening'
    if 'charcoal' in n or 'activated charcoal' in n: return 'Porous carbon; detoxifying and absorbent'
    if 'menthol' in n: return 'Cooling and soothing mint derivative'
    if 'caffeine' in n: return 'Stimulant; improves blood circulation'
    if 'biotin' in n: return 'B-vitamin; supports hair and nail health'
    if 'sandalwood' in n: return 'Aromatic oil; soothing and antimicrobial'
    if 'witch hazel' in n: return 'Astringent plant extract; soothes skin'
    if 'allantoin' in n: return 'Natural compound; promotes skin healing'
    if 'shea butter' in n: return 'Rich emollient; deeply moisturising'
    if 'green tea' in n: return 'Antioxidant-rich; protects and soothes skin'
    if 'salicylic acid' in n: return 'Beta-hydroxy acid; gentle exfoliant for acne'
    if 'niacinamide' in n: return 'Vitamin B3; strengthens skin barrier'
    if 'hyaluronic acid' in n: return 'Humectant polymer; holds up to 1000x water'
    if 'keratin' in n: return 'Protein; strengthens hair structure'
    if 'panthenol' in n: return 'Pro-Vitamin B5; moisturising and soothing'
    if 'ascorbic acid' in n or 'vitamin c' in n: return 'Antioxidant; brightens and protects'
    return 'Generally recognised as safe'

def _reg_note(cls: str) -> str:
    if cls == 'banned': return 'Banned in EU and multiple countries'
    if cls == 'commonly_questioned': return 'Subject to regulatory scrutiny'
    if cls == 'worth_knowing': return 'Permitted additive; use as directed'
    return 'Approved under standard cosmetic regulations'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    items = [i.strip() for i in raw.split(',')]
    return [i for i in items if len(i) > 1 and 'q.s.' not in i.lower()]

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
    if score >= 80: return 'Generally suitable. Check for personal allergies.'
    if score >= 60: return 'Suitable for most. Some ingredients may warrant attention.'
    if score >= 40: return 'Review before regular use, especially for sensitive skin.'
    return 'Consider checking with a professional before use.'

PRODUCTS = [
    # ──── BEARDO (11 total) ────
    {"name": "Beardo Beard Activator", "brand": "Beardo", "category": "Personal Care",
     "raw": "High-grade metal (0.5 mm needles), ABS Plastic (Handle). Note: This is a mechanical device (derma roller)."},
    {"name": "Beardo Godfather Beard Oil", "brand": "Beardo", "category": "Personal Care",
     "raw": "Mineral Oil, Almond Oil, Fragrance, Vitamin E, Aloe Vera Extract, Olive Oil."},
    {"name": "Beardo Hemp Styling Hair Wax", "brand": "Beardo", "category": "Hair Care",
     "raw": "Beeswax, Hemp Seed Oil, Aloe Vera Extract, Carnauba Wax, Vitamin E, Fragrance."},
    {"name": "Beardo Ultraglow Face Cream SPF 30", "brand": "Beardo", "category": "Skincare",
     "raw": "Aqua, Ethylhexyl Methoxycinnamate, Niacinamide, Mulberry Extract, Licorice Extract, Glycerin, Titanium Dioxide."},
    {"name": "Beardo Activated Charcoal Face Wash", "brand": "Beardo", "category": "Skincare",
     "raw": "Aqua, Activated Charcoal Powder, Glycerin, Myristic Acid, Stearic Acid, Potassium Hydroxide, Menthol, Aloe Vera Extract."},
    {"name": "Beardo Dark Side Perfume EDP", "brand": "Beardo", "category": "Personal Care",
     "raw": "Ethyl Alcohol (95% v/v), Fragrance, Aqua, Diethyl Phthalate, Propylene Glycol."},
    {"name": "Beardo Hair Fall Control Shampoo", "brand": "Beardo", "category": "Hair Care",
     "raw": "Aqua, Sodium Laureth Sulfate, Cocamidopropyl Betaine, Saw Palmetto Extract, Caffeine, Rosemary Oil, Biotin, Amla Extract."},
    {"name": "Beardo Hair Wax Strong Hold", "brand": "Beardo", "category": "Hair Care",
     "raw": "Aqua, Ceteareth-25, PEG-7 Glyceryl Cocoate, Glycerin, PVP, Fragrance, Phenoxyethanol."},
    {"name": "Beardo Beard Growth Oil", "brand": "Beardo", "category": "Personal Care",
     "raw": "Coconut Oil, Sesame Oil, Vetiver Oil, Jojoba Oil, Brahmi Extract, Amla Extract, Hibiscus Extract."},
    {"name": "Beardo Ultraglow Face Wash", "brand": "Beardo", "category": "Skincare",
     "raw": "Aqua, Sodium Laureth Sulfate, Cocamidopropyl Betaine, Glycerin, Niacinamide, Licorice Extract, Mulberry Extract, Aloe Vera Extract, Menthol."},
    {"name": "Beardo Beard Softener", "brand": "Beardo", "category": "Personal Care",
     "raw": "Aqua, Cetyl Alcohol, Shea Butter, Cocoa Butter, Argan Oil, Almond Oil, Glycerin, Guar Hydroxypropyltrimonium Chloride."},

    # ──── BOMBAY SHAVING CO (6 products) ────
    {"name": "Bombay Shaving Co Precision Safety Razor", "brand": "Bombay Shaving Co", "category": "Personal Care",
     "raw": "Zinc Alloy (Chrome Plated), Stainless Steel (Feather Blades). Mechanical device."},
    {"name": "Bombay Shaving Co Charcoal Shaving Foam", "brand": "Bombay Shaving Co", "category": "Personal Care",
     "raw": "Aqua, Stearic Acid, Triethanolamine, Butane/Propane (Propellant), Glycerin, Charcoal Powder, Menthol, Aloe Vera Extract."},
    {"name": "Bombay Shaving Co Post-Shave Balm Witch Hazel", "brand": "Bombay Shaving Co", "category": "Personal Care",
     "raw": "Aqua, Witch Hazel Extract, Aloe Vera Juice, Vitamin E, Menthol, Panthenol, Allantoin, Caprylic/Capric Triglyceride."},
    {"name": "Bombay Shaving Co Charcoal Face Wash", "brand": "Bombay Shaving Co", "category": "Skincare",
     "raw": "Aqua, Activated Charcoal, Glycerin, Sodium Lauroyl Sarcosinate, Lauryl Glucoside, Papaya Extract, Turmeric Extract."},
    {"name": "Bombay Shaving Co Beard Growth Oil Exotic", "brand": "Bombay Shaving Co", "category": "Personal Care",
     "raw": "Coconut Oil, Almond Oil, Argan Oil, Jojoba Oil, Vetiver Essential Oil, Lemon Essential Oil, Vitamin E."},
    {"name": "Bombay Shaving Co Onion Hair Oil", "brand": "Bombay Shaving Co", "category": "Hair Care",
     "raw": "Onion Seed Oil, Black Seed Oil, Almond Oil, Castor Oil, Jojoba Oil, Olive Oil, Coconut Oil."},

    # ──── BIOTIQUE EXTENDED VOL 2 (12 products) ────
    {"name": "Biotique Bio Winter Cherry Rejuvenating Body Nourisher", "brand": "Biotique", "category": "Personal Care",
     "raw": "Surajmukhi Tail, Dhamasa Plant, Kasani Seed, Ashwagandha Root, Gajari Seed, Winter Cherry, Purified Water q.s."},
    {"name": "Biotique Bio Costus Stress Relief Foot Cream", "brand": "Biotique", "category": "Skincare",
     "raw": "Costus Root, Cobbler's Leather, Pudina Leaf, Datura Leaf, Rai Oil, Bees Wax, Purified Water q.s."},
    {"name": "Biotique Bio Clove Purifying Anti-Blemish Face Pack", "brand": "Biotique", "category": "Skincare",
     "raw": "Lavang (Clove), Peppermint Oil, Gandhak (Sulphur), Neem Bark, Yashad Bhasma (Zinc Oxide), Multani Mitti (Fuller's Earth)."},
    {"name": "Biotique Bio Pistachio Ageless Nourishing Face Pack", "brand": "Biotique", "category": "Skincare",
     "raw": "Pista (Pistachio), Jaiphal (Nutmeg), Badam (Almond), Haldi (Turmeric), Kesar (Saffron), Musli, Base q.s."},
    {"name": "Biotique Bio Walnut Purifying & Polishing Face Scrub", "brand": "Biotique", "category": "Skincare",
     "raw": "Akhrot Shell (Walnut), Neem Bark, Nagkesar Flower, Pudina Leaf, Vitamin E, Purified Water q.s."},
    {"name": "Biotique Bio Saffron Dew Ageless Day Cream", "brand": "Biotique", "category": "Skincare",
     "raw": "Kesar (Saffron), Pistachio Oil, Haldi (Turmeric), Badam Oil, Mulethi Root, Himalayan Water q.s."},
    {"name": "Biotique Bio Vera Ultra Soothing Body Lotion", "brand": "Biotique", "category": "Personal Care",
     "raw": "Aloe Vera Gel, Surajmukhi Tail (Sunflower Oil), Kusumbhi Tail, Gehun Oil, Purified Water q.s."},
    {"name": "Biotique Bio BXL Cellular Whitening Cream", "brand": "Biotique", "category": "Skincare",
     "raw": "BXL Complex (Blackberry, Saffron, Mulberry, Aloe Vera), Coconut Water, Vitamin E, Base q.s."},
    {"name": "Biotique Bio Flame of the Forest Fresh Shine-Expert Hair Oil", "brand": "Biotique", "category": "Hair Care",
     "raw": "Tesu Flower (Flame of the Forest), Japa Flower (Hibiscus), Amla Fruit, Shikakai, Coconut Oil Base."},
    {"name": "Biotique Bio Sea Kelp Fresh-Growth Revitalizing Body Wash", "brand": "Biotique", "category": "Personal Care",
     "raw": "Sea Kelp, Neem Bark, Bhringraj Plant, Ritha Fruit, Sajjikshar, Purified Water q.s."},
    {"name": "Biotique Bio Henna Fresh Powder Hair Color", "brand": "Biotique", "category": "Hair Care",
     "raw": "Mehendi Leaf, Neem Bark, Babul Bark, Gambhari, Amla Fruit, Arjun Bark."},
    {"name": "Biotique Bio Mountain Ebony Vitalizing Serum for Falling Hair", "brand": "Biotique", "category": "Hair Care",
     "raw": "Kachnar (Mountain Ebony), Pudina (Peppermint), Kusumbhi (Safflower), Neem Bark, Pipali, Mulethi, Purified Water q.s."},

    # ──── BSC ADVANCED GROOMING (6 products) ────
    {"name": "BSC Vitamin C Face Serum", "brand": "Bombay Shaving Co", "category": "Skincare",
     "raw": "Aqua, 10% Ethyl Ascorbic Acid (Vitamin C), Glycerin, Ferulic Acid, Hyaluronic Acid, Aloe Vera Extract, Phenoxyethanol."},
    {"name": "BSC Sandalwood & Turmeric Bath Soap", "brand": "Bombay Shaving Co", "category": "Personal Care",
     "raw": "Sodium Palmate, Sodium Palm Kernelate, Sandalwood Oil, Turmeric Extract, Glycerin, Shea Butter, Walnut Scrub Particles."},
    {"name": "BSC Coffee Hair Mask", "brand": "Bombay Shaving Co", "category": "Hair Care",
     "raw": "Aqua, Coffee Bean Extract, Keratin, Argan Oil, Shea Butter, Panthenol (Pro-Vitamin B5), Cetostearyl Alcohol, Fragrance."},
    {"name": "BSC Pre-Shave Scrub", "brand": "Bombay Shaving Co", "category": "Personal Care",
     "raw": "Aqua, Black Sand, Activated Charcoal, Vitamin E, Lemon Oil, Aloe Vera, Stearic Acid, Walnut Shell Powder."},
    {"name": "BSC Red Onion Hair Mask", "brand": "Bombay Shaving Co", "category": "Hair Care",
     "raw": "Onion Seed Oil, Black Seed Oil, Shea Butter, Wheat Germ Oil, Sweet Almond Oil, Vitamin E, Behentrimonium Chloride."},
    {"name": "BSC Oil Control Face Moisturizer", "brand": "Bombay Shaving Co", "category": "Skincare",
     "raw": "Aqua, Salicylic Acid, Green Tea Extract, Aloe Vera, Vitamin C, Niacinamide, Glycerin, Dimethicone."},
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
                f"{name} by {p['brand']}. "
                f"Awareness score: {score}/100. "
                "Not a health assessment or medical advice."
            ),
            'fssai_note':      'Subject to applicable cosmetic regulations.',
            'verdict':         _verdict(score),
            'recommendation':  _recommendation(score),
            'ingredients':     ingredient_objs,
            'ingredients_raw': raw,
            'status':          'active',
        }).execute()
        print(f"  + {name} | {p['category']} | score {score}")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} mens grooming products...")
    inserted = 0
    for p in PRODUCTS:
        if insert(p):
            inserted += 1
        time.sleep(0.1)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
