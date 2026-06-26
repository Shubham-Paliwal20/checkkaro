"""
Insert fragrance and deodorant products from Detailed_Ingredient_List_100_Fragrances PDF
Brands: Fogg, Wild Stone, Axe, Park Avenue, Engage, Nivea, Denver, Envy, Beardo, The Man Company
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_BANNED = ['triclosan']
_QUESTIONED = [
    'diethyl phthalate', 'phthalate', 'alcohol', 'propylene glycol',
    'benzophenone', 'menthol',
]
_WORTH = [
    'propellant', 'butane', 'isobutane', 'ethyl alcohol', 'fragrance',
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
    if cls == 'banned':
        if 'triclosan' in n: return 'Antimicrobial; banned in several countries'
        return 'Banned ingredient'
    if cls == 'commonly_questioned':
        if 'diethyl phthalate' in n or 'phthalate' in n: return 'Phthalate; plasticizer; hormone disruptor concerns'
        if 'alcohol' in n: return 'Denatured alcohol; flammable'
        if 'propylene glycol' in n: return 'Humectant; skin penetrant'
        if 'benzophenone' in n: return 'UV filter; potential endocrine disruptor'
        if 'menthol' in n: return 'Cooling agent; can irritate sensitive skin'
        return 'Commonly questioned ingredient'
    if cls == 'worth_knowing':
        if 'propellant' in n or 'butane' in n or 'isobutane' in n: return 'Flammable propellant gas; handle carefully'
        if 'ethyl alcohol' in n: return 'Alcohol base; flammable'
        if 'fragrance' in n: return 'Perfume compound; undisclosed fragrance ingredients'
        return 'Moderate concern; safe when used as directed'
    # generally_recognised
    if 'water' in n or 'aqua' in n: return 'Base solvent; hydrating'
    if 'glycerin' in n: return 'Humectant; hydrating'
    if 'panthenol' in n: return 'Provitamin B5; conditioning'
    if 'glycerin' in n: return 'Natural humectant'
    return 'Generally recognised as safe'

def _reg_note(cls: str) -> str:
    if cls == 'banned': return 'Banned in multiple countries'
    if cls == 'commonly_questioned': return 'Subject to regulatory scrutiny; permitted by FSSAI'
    if cls == 'worth_knowing': return 'Safe when used as directed; flammable'
    return 'Approved for fragrance use'

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
        elif cls == 'commonly_questioned': score -= 12
        elif cls == 'worth_knowing': score -= 3
    return max(0, min(100, score))

PRODUCTS = [
    # FOGG COLLECTION (15)
    {"name": "Fogg Marco", "brand": "Fogg", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate (1.0% w/w), Propylene Glycol, Triclosan (0.1% w/w)."},
    {"name": "Fogg Royal", "brand": "Fogg", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate (1.0% w/w), Propylene Glycol, Triclosan (0.1% w/w)."},
    {"name": "Fogg Napoleon", "brand": "Fogg", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Propylene Glycol, Triclosan."},
    {"name": "Fogg Master Pine", "brand": "Fogg", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Propylene Glycol, Triclosan."},
    {"name": "Fogg Master Oak", "brand": "Fogg", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Propylene Glycol, Triclosan."},
    {"name": "Fogg Dynamic", "brand": "Fogg", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Propylene Glycol, Triclosan."},
    {"name": "Fogg Impressio", "brand": "Fogg", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Propylene Glycol, Aqua."},
    {"name": "Fogg Intensio", "brand": "Fogg", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Propylene Glycol, Aqua."},
    {"name": "Fogg Paradise", "brand": "Fogg", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Propylene Glycol, Triclosan."},
    {"name": "Fogg Radiant", "brand": "Fogg", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Propylene Glycol, Triclosan."},
    {"name": "Fogg Essence", "brand": "Fogg", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Propylene Glycol, Triclosan."},
    {"name": "Fogg Make My Day", "brand": "Fogg", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Propylene Glycol."},
    {"name": "Fogg I Am Queen", "brand": "Fogg", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Propylene Glycol."},
    {"name": "Fogg 1000 Sprays Black", "brand": "Fogg", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Propylene Glycol."},
    {"name": "Fogg 1000 Sprays White", "brand": "Fogg", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Propylene Glycol."},

    # WILD STONE COLLECTION (15)
    {"name": "Wild Stone Ultra Sensual", "brand": "Wild Stone", "category": "Personal Care",
     "raw": "Ethyl Alcohol (95% v/v), Fragrance, Diethyl Phthalate (1.0% w/w), Propylene Glycol, Triclosan (0.1% w/w)."},
    {"name": "Wild Stone Red", "brand": "Wild Stone", "category": "Personal Care",
     "raw": "Ethyl Alcohol (95% v/v), Fragrance, Diethyl Phthalate, Propylene Glycol, Triclosan."},
    {"name": "Wild Stone Code Steel", "brand": "Wild Stone", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Fragrance, Diethyl Phthalate, Propylene Glycol."},
    {"name": "Wild Stone Code Titanium", "brand": "Wild Stone", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Fragrance, Diethyl Phthalate, Propylene Glycol."},
    {"name": "Wild Stone Code Gold", "brand": "Wild Stone", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Fragrance, Diethyl Phthalate, Propylene Glycol."},
    {"name": "Wild Stone Code Copper", "brand": "Wild Stone", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Fragrance, Diethyl Phthalate, Propylene Glycol."},
    {"name": "Wild Stone Forest Spice", "brand": "Wild Stone", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Fragrance, Diethyl Phthalate, Triclosan."},
    {"name": "Wild Stone Hydra Blue", "brand": "Wild Stone", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Fragrance, Diethyl Phthalate, Triclosan."},
    {"name": "Wild Stone Night Rider", "brand": "Wild Stone", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Fragrance, Diethyl Phthalate, Triclosan."},
    {"name": "Wild Stone Edge", "brand": "Wild Stone", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Fragrance, Diethyl Phthalate."},
    {"name": "Wild Stone Iridium", "brand": "Wild Stone", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Fragrance, Diethyl Phthalate."},
    {"name": "Wild Stone Aura", "brand": "Wild Stone", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Fragrance, Diethyl Phthalate."},
    {"name": "Wild Stone Bronze", "brand": "Wild Stone", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Fragrance, Diethyl Phthalate, Triclosan."},
    {"name": "Wild Stone Iron", "brand": "Wild Stone", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Fragrance, Diethyl Phthalate, Triclosan."},
    {"name": "Wild Stone Soap", "brand": "Wild Stone", "category": "Personal Care",
     "raw": "Sodium Palmitate, Sodium Palm Kernelate, Fragrance, Glycerin."},

    # AXE COLLECTION (12)
    {"name": "Axe Dark Temptation", "brand": "Axe", "category": "Personal Care",
     "raw": "Alcohol Denat., Butane, Isobutane, Propane, Perfume, Neodecanoic Acid, Zinc Neodecanoate."},
    {"name": "Axe Signature Gold", "brand": "Axe", "category": "Personal Care",
     "raw": "Alcohol Denat., Perfume, Ethylhexylglycerin, Benzyl Alcohol, Citral."},
    {"name": "Axe Apollo", "brand": "Axe", "category": "Personal Care",
     "raw": "Alcohol Denat., Butane, Isobutane, Propane, Perfume, Alpha-Isomethyl Ionone."},
    {"name": "Axe Marine", "brand": "Axe", "category": "Personal Care",
     "raw": "Alcohol Denat., Butane, Isobutane, Propane, Perfume, Limonene."},
    {"name": "Axe Ice Breaker", "brand": "Axe", "category": "Personal Care",
     "raw": "Alcohol Denat., Butane, Isobutane, Propane, Perfume, Menthol."},
    {"name": "Axe Pulse", "brand": "Axe", "category": "Personal Care",
     "raw": "Alcohol Denat., Butane, Isobutane, Propane, Perfume, Citronellol."},
    {"name": "Axe Copper", "brand": "Axe", "category": "Personal Care",
     "raw": "Alcohol Denat., Perfume, Water, Coumarin."},
    {"name": "Axe Black", "brand": "Axe", "category": "Personal Care",
     "raw": "Alcohol Denat., Butane, Isobutane, Propane, Perfume, Linalool."},
    {"name": "Axe Ticket Dark Temptation", "brand": "Axe", "category": "Personal Care",
     "raw": "Alcohol Denat., Perfume, Ethylhexylglycerin."},
    {"name": "Axe Ticket Intense", "brand": "Axe", "category": "Personal Care",
     "raw": "Alcohol Denat., Perfume, Alpha-Isomethyl Ionone."},
    {"name": "Axe Anarchy For Him", "brand": "Axe", "category": "Personal Care",
     "raw": "Alcohol Denat., Butane, Isobutane, Propane, Perfume."},
    {"name": "Axe Excite", "brand": "Axe", "category": "Personal Care",
     "raw": "Alcohol Denat., Butane, Isobutane, Propane, Perfume."},

    # PARK AVENUE COLLECTION (10)
    {"name": "Park Avenue Good Morning", "brand": "Park Avenue", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Propellant (LPG), Perfume, Triclosan, Diethyl Phthalate, Aqua."},
    {"name": "Park Avenue Cool Blue", "brand": "Park Avenue", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Propellant, Perfume, Triclosan, Diethyl Phthalate."},
    {"name": "Park Avenue Storm", "brand": "Park Avenue", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Propellant, Perfume, Triclosan, Diethyl Phthalate."},
    {"name": "Park Avenue Trance", "brand": "Park Avenue", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Propellant, Perfume, Triclosan, Diethyl Phthalate."},
    {"name": "Park Avenue Euphoria", "brand": "Park Avenue", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Propylene Glycol, Aqua, Diethyl Phthalate."},
    {"name": "Park Avenue Conquer", "brand": "Park Avenue", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Propylene Glycol, Diethyl Phthalate."},
    {"name": "Park Avenue Voyage", "brand": "Park Avenue", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Propellant, Perfume, Diethyl Phthalate."},
    {"name": "Park Avenue Signature", "brand": "Park Avenue", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate."},
    {"name": "Park Avenue Neo", "brand": "Park Avenue", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Propellant, Perfume."},
    {"name": "Park Avenue Zing", "brand": "Park Avenue", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Propellant, Perfume."},

    # ENGAGE COLLECTION (12)
    {"name": "Engage M1", "brand": "Engage", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Propellant, Perfume, Diethyl Phthalate, Tertiary Butyl Alcohol."},
    {"name": "Engage W1", "brand": "Engage", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Propellant, Perfume, Diethyl Phthalate, Tertiary Butyl Alcohol."},
    {"name": "Engage W2", "brand": "Engage", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Propellant, Perfume, Diethyl Phthalate."},
    {"name": "Engage On On Pocket Perfume Men", "brand": "Engage", "category": "Personal Care",
     "raw": "Alcohol Denat., Perfume, Butylated Hydroxytoluene."},
    {"name": "Engage On On Pocket Perfume Women", "brand": "Engage", "category": "Personal Care",
     "raw": "Alcohol Denat., Perfume, Butylated Hydroxytoluene."},
    {"name": "Engage L'Amante Men", "brand": "Engage", "category": "Personal Care",
     "raw": "Alcohol Denat., Perfume, Benzophenone-3."},
    {"name": "Engage L'Amante Women", "brand": "Engage", "category": "Personal Care",
     "raw": "Alcohol Denat., Perfume, Benzophenone-3."},
    {"name": "Engage Yang", "brand": "Engage", "category": "Personal Care",
     "raw": "Alcohol Content, Propellant, Perfume, Diethyl Phthalate."},
    {"name": "Engage Yin", "brand": "Engage", "category": "Personal Care",
     "raw": "Alcohol Content, Propellant, Perfume, Diethyl Phthalate."},
    {"name": "Engage Drizzle", "brand": "Engage", "category": "Personal Care",
     "raw": "Alcohol Content, Propellant, Perfume."},
    {"name": "Engage Tease", "brand": "Engage", "category": "Personal Care",
     "raw": "Alcohol Content, Propellant, Perfume."},
    {"name": "Engage Spell", "brand": "Engage", "category": "Personal Care",
     "raw": "Alcohol Content, Propellant, Perfume."},

    # NIVEA COLLECTION (10)
    {"name": "Nivea Fresh Active", "brand": "Nivea", "category": "Personal Care",
     "raw": "Butane, Alcohol Denat., Isobutane, Propane, Perfume, Maris Limus Extract, Ostrea Shell Extract."},
    {"name": "Nivea Deep Impact", "brand": "Nivea", "category": "Personal Care",
     "raw": "Butane, Alcohol Denat., Perfume, Charcoal Powder, Persea Gratissima Oil."},
    {"name": "Nivea Pearl & Beauty", "brand": "Nivea", "category": "Personal Care",
     "raw": "Butane, Alcohol Denat., Perfume, Hydrolyzed Pearl, Persea Gratissima Oil."},
    {"name": "Nivea Whitening Smooth Skin", "brand": "Nivea", "category": "Personal Care",
     "raw": "Butane, Alcohol Denat., Licorice Extracts, Witch Hazel Extract."},
    {"name": "Nivea Fresh Flower", "brand": "Nivea", "category": "Personal Care",
     "raw": "Butane, Alcohol Denat., Perfume, Citronellol, Linalool."},
    {"name": "Nivea Protect & Care", "brand": "Nivea", "category": "Personal Care",
     "raw": "Butane, Alcohol Denat., Glycerin, Panthenol, Aqua."},
    {"name": "Nivea Cool Kick", "brand": "Nivea", "category": "Personal Care",
     "raw": "Butane, Alcohol Denat., Menthol, Persea Gratissima Oil."},
    {"name": "Nivea Dry Comfort", "brand": "Nivea", "category": "Personal Care",
     "raw": "Butane, Alcohol Denat., Aluminum Chlorohydrate, Magnesium Aluminum Silicate."},
    {"name": "Nivea Silver Protect", "brand": "Nivea", "category": "Personal Care",
     "raw": "Butane, Alcohol Denat., Silver Citrate, Citric Acid."},
    {"name": "Nivea Fresh Natural", "brand": "Nivea", "category": "Personal Care",
     "raw": "Butane, Alcohol Denat., Marine Extracts, Ostrea Shell Extract."},

    # DENVER COLLECTION (10)
    {"name": "Denver Hamilton", "brand": "Denver", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Propylene Glycol, Triclosan."},
    {"name": "Denver Black Code", "brand": "Denver", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Propylene Glycol, Triclosan."},
    {"name": "Denver Imperial", "brand": "Denver", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Propylene Glycol, Triclosan."},
    {"name": "Denver Pride", "brand": "Denver", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Triclosan."},
    {"name": "Denver Honour", "brand": "Denver", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Triclosan."},
    {"name": "Denver Caliber", "brand": "Denver", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Triclosan."},
    {"name": "Denver Zenith", "brand": "Denver", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Triclosan."},
    {"name": "Denver Goal", "brand": "Denver", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Triclosan."},
    {"name": "Denver Knight", "brand": "Denver", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Triclosan."},
    {"name": "Denver Sporting Club Victor", "brand": "Denver", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Triclosan."},

    # ENVY COLLECTION (6)
    {"name": "Envy Dark", "brand": "Envy", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Propylene Glycol."},
    {"name": "Envy Magnetic", "brand": "Envy", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Propylene Glycol."},
    {"name": "Envy Speed", "brand": "Envy", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Propylene Glycol."},
    {"name": "Envy Nitro", "brand": "Envy", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Propylene Glycol."},
    {"name": "Envy Fiery", "brand": "Envy", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Propylene Glycol."},
    {"name": "Envy Rush", "brand": "Envy", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate."},

    # BEARDO COLLECTION (5)
    {"name": "Beardo Whisky Smoke", "brand": "Beardo", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Aqua, Denatonium Benzoate."},
    {"name": "Beardo Dark Side", "brand": "Beardo", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Aqua."},
    {"name": "Beardo Godfather", "brand": "Beardo", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Aqua."},
    {"name": "Beardo Black Musk", "brand": "Beardo", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Aqua."},
    {"name": "Beardo Mariner", "brand": "Beardo", "category": "Personal Care",
     "raw": "Ethyl Alcohol, Perfume, Diethyl Phthalate, Aqua."},

    # THE MAN COMPANY COLLECTION (5)
    {"name": "The Man Company Blanc", "brand": "The Man Company", "category": "Personal Care",
     "raw": "Ethyl Alcohol (95% v/v), Perfume, Diethyl Phthalate, Propylene Glycol."},
    {"name": "The Man Company Bleu", "brand": "The Man Company", "category": "Personal Care",
     "raw": "Ethyl Alcohol (95% v/v), Perfume, Diethyl Phthalate, Propylene Glycol."},
    {"name": "The Man Company Noir", "brand": "The Man Company", "category": "Personal Care",
     "raw": "Ethyl Alcohol (95% v/v), Perfume, Diethyl Phthalate, Propylene Glycol."},
    {"name": "The Man Company Rouge", "brand": "The Man Company", "category": "Personal Care",
     "raw": "Ethyl Alcohol (95% v/v), Perfume, Diethyl Phthalate, Propylene Glycol."},
    {"name": "The Man Company Fire", "brand": "The Man Company", "category": "Personal Care",
     "raw": "Ethyl Alcohol (95% v/v), Perfume, Diethyl Phthalate, Propylene Glycol."},
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
                f"{name} by {p['brand']}. Fragrance/deodorant. "
                f"Awareness score: {score}/100. Not for medical use."
            ),
            'fssai_note':      'Fragrance product; not for ingestion.',
            'verdict':         'Standard formulation' if score >= 60 else 'Review before use',
            'recommendation':  'Use as directed; avoid contact with eyes.' if score >= 60 else 'May contain concerning ingredients.',
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
    print(f"Inserting {len(PRODUCTS)} fragrance and deodorant products...")
    inserted = 0
    for p in PRODUCTS:
        if insert(p):
            inserted += 1
        time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
