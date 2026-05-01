"""
Insert Amul Ice Cream Portfolio (44 products) into ai_extracted_products
Data extracted directly from Amul_IceCream_Full_Portfolio.pdf
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

PRODUCTS = [
    # CLASSIC RANGE
    {"name": "Amul Vanilla Magic Ice Cream", "sub": "Classic Range",
     "ingredients": "Milk Solids, Sugar, Permitted Emulsifier (E471) and Stabilizers (E407, E466, E412, E410), Nature Identical Vanilla Flavour.",
     "score": 72},
    {"name": "Amul Strawberry Hub Ice Cream", "sub": "Classic Range",
     "ingredients": "Milk Solids, Sugar, Strawberry Fruit Preparation (10%), Emulsifier (E471), Stabilizers (E407, E466, E412, E410), Permitted Natural Colour (E162).",
     "score": 70},
    {"name": "Amul Chocolate Brownie Ice Cream", "sub": "Classic Range",
     "ingredients": "Milk Solids, Sugar, Brownie Pieces (8%) [Wheat Flour, Cocoa Solids, Sugar, Butter], Cocoa Solids, Emulsifier (E471), Stabilizers (E407, E466, E412, E410).",
     "score": 65},
    {"name": "Amul Anjeer Fig Ice Cream", "sub": "Classic Range",
     "ingredients": "Milk Solids, Sugar, Fig Preparation (10%), Emulsifier (E471), Stabilizers.",
     "score": 74},
    {"name": "Amul Tutti Frutti Ice Cream", "sub": "Classic Range",
     "ingredients": "Milk Solids, Sugar, Candied Fruits (8%), Emulsifier (E471), Stabilizers.",
     "score": 68},
    {"name": "Amul Vanilla Cup Ice Cream", "sub": "Classic Range",
     "ingredients": "Milk Solids, Sugar, Emulsifiers, Stabilizers, Vanilla Flavour.",
     "score": 72},

    # CONE RANGE
    {"name": "Amul Tricone Butterscotch", "sub": "Cone Range",
     "ingredients": "Ice Cream: Milk Solids, Butterscotch Granules. Cone: Wheat Flour, Sugar, Vegetable Oil. Spray: Edible Vegetable Fat, Cocoa Solids, E322.",
     "score": 62},
    {"name": "Amul Tricone Chocolate", "sub": "Cone Range",
     "ingredients": "Ice Cream: Milk Solids, Cocoa Solids. Cone: Wheat Flour, Sugar. Spray: Chocolate Compound.",
     "score": 65},
    {"name": "Amul Tricone Cookie n Cream", "sub": "Cone Range",
     "ingredients": "Ice Cream: Milk Solids, Chocolate Cookies. Cone: Wheat Flour. Top: Chocolate disc with cookie bits.",
     "score": 63},
    {"name": "Amul Tricone Pista", "sub": "Cone Range",
     "ingredients": "Ice Cream: Milk Solids, Pista bits. Cone: Wheat Flour. Top: Cashew nuts.",
     "score": 74},

    # EPIC STICK RANGE
    {"name": "Amul Epic Choco Almond", "sub": "Epic Stick Range",
     "ingredients": "Ice Cream: Milk Solids, Sugar. Coating: Belgian Chocolate, Roasted Almonds (5%), Cocoa Butter, Cocoa Solids, Emulsifier (E322, E476).",
     "score": 68},
    {"name": "Amul Epic Choco Brownie", "sub": "Epic Stick Range",
     "ingredients": "Ice Cream: Milk Solids, Sugar, Cocoa. Coating: Dark Chocolate, Brownie Crumbles, Cocoa Butter, Emulsifier (E322).",
     "score": 66},
    {"name": "Amul Epic Strawberry Twist", "sub": "Epic Stick Range",
     "ingredients": "Ice Cream: Milk Solids, Strawberry Pulp. Coating: White Chocolate, Strawberry Flakes, Cocoa Butter, Emulsifier (E322).",
     "score": 67},
    {"name": "Amul Epic Pistachio", "sub": "Epic Stick Range",
     "ingredients": "Ice Cream: Milk Solids, Pista Paste. Coating: White Chocolate, Roasted Pistachio bits, Emulsifier (E322).",
     "score": 70},

    # FRUIT RANGE
    {"name": "Amul King Alphonso Mango Ice Cream", "sub": "Fruit Range",
     "ingredients": "Milk Solids, Sugar, Alphonso Mango Pulp (15%), Emulsifier (E471), Stabilizers (E407, E466, E412, E410), Natural Colour (E160b).",
     "score": 73},
    {"name": "Amul Black Currant Ice Cream", "sub": "Fruit Range",
     "ingredients": "Milk Solids, Sugar, Black Currant Fruit (10%), Emulsifier (E471), Stabilizers (E407, E466, E412, E410).",
     "score": 72},
    {"name": "Amul Litchi Ice Cream", "sub": "Fruit Range",
     "ingredients": "Milk Solids, Sugar, Litchi Fruit Pieces, Emulsifier (E471), Stabilizers.",
     "score": 73},

    # HEALTH RANGE
    {"name": "Amul Sugar Free Vanilla Ice Cream", "sub": "Health Range",
     "ingredients": "Milk Solids, Fructo-Oligosaccharide (FOS), Sucralose (No Sugar Added), Emulsifier (E471), Stabilizers.",
     "score": 74},
    {"name": "Amul Haldi Turmeric Ice Cream", "sub": "Health Range",
     "ingredients": "Milk Solids, Sugar, Turmeric, Honey, Pepper, Emulsifiers, Stabilizers.",
     "score": 78},
    {"name": "Amul Ashwagandha Ice Cream", "sub": "Health Range",
     "ingredients": "Milk Solids, Sugar, Ashwagandha Extract, Honey, Dry Fruits.",
     "score": 80},
    {"name": "Amul Protein Ice Cream", "sub": "Health Range",
     "ingredients": "Milk Solids, Whey Protein Isolate, Sugar, Emulsifiers, Stabilizers. (20g Protein per tub).",
     "score": 76},

    # INDULGENCE RANGE
    {"name": "Amul Caramel Popcorn Ice Cream Tub", "sub": "Indulgence Range",
     "ingredients": "Milk Solids, Sugar, Caramel Sauce, Buttered Popcorn pieces, Stabilizers.",
     "score": 63},
    {"name": "Amul Creme Rich Paan Ice Cream", "sub": "Indulgence Range",
     "ingredients": "Milk Solids, Sugar, Betel Leaves (Paan), Gulkand (Rose petal preserve), Fennel, Dates.",
     "score": 75},
    {"name": "Amul Creme Rich Italian Delight Ice Cream", "sub": "Indulgence Range",
     "ingredients": "Milk Solids, Sugar, Raisins, Cashews, Mixed Fruit bits, Emulsifiers.",
     "score": 72},
    {"name": "Amul Creme Rich Belgian Chocolate Ice Cream", "sub": "Indulgence Range",
     "ingredients": "Milk Solids, Sugar, Belgian Cocoa Powder, Cocoa Butter, Chocolate flakes.",
     "score": 70},

    # NOVELTY RANGE
    {"name": "Amul Isabcool Curd Ice Cream", "sub": "Novelty Range",
     "ingredients": "Curd (Yoghurt), Milk Solids, Sugar, Isabgol (Psyllium Husk), Emulsifier, Stabilizers.",
     "score": 76},
    {"name": "Amul Sandwich Ice Cream Vanilla Chocolate", "sub": "Novelty Range",
     "ingredients": "Milk Solids, Sugar. Biscuit: Wheat Flour, Cocoa Powder, Sugar.",
     "score": 66},

    # NUTTY RANGE
    {"name": "Amul Roasted Almond Ice Cream", "sub": "Nutty Range",
     "ingredients": "Milk Solids, Sugar, Roasted Almonds (6%), Emulsifier (E471), Stabilizers.",
     "score": 75},

    # PREMIUM RANGE
    {"name": "Amul Cassis Black Currant Ice Cream Tub", "sub": "Premium Range",
     "ingredients": "Milk Solids, Sugar, Black Currant Fruit preparation, Emulsifiers.",
     "score": 72},
    {"name": "Amul Almond Fudge Ice Cream Tub", "sub": "Premium Range",
     "ingredients": "Milk Solids, Sugar, Roasted Almonds, Caramel Fudge sauce.",
     "score": 70},
    {"name": "Amul Irish Coffee Ice Cream Tub", "sub": "Premium Range",
     "ingredients": "Milk Solids, Sugar, Coffee powder, Irish Coffee flavour (Non-alcoholic).",
     "score": 68},

    # ROYAL RANGE
    {"name": "Amul Kesar Pista Ice Cream", "sub": "Royal Range",
     "ingredients": "Milk Solids, Sugar, Pistachio Nuts (2%), Saffron (Kesar), Emulsifier (E471), Stabilizers (E407, E466, E412, E410).",
     "score": 76},
    {"name": "Amul Rajbhog Ice Cream", "sub": "Royal Range",
     "ingredients": "Milk Solids, Sugar, Cashew Nuts, Almonds, Pistachio, Honey, Saffron, Cardamom, Emulsifier (E471), Stabilizers.",
     "score": 78},
    {"name": "Amul Afghan Dry Fruit Ice Cream", "sub": "Royal Range",
     "ingredients": "Milk Solids, Sugar, Figs (Anjeer), Roasted Almonds, Cashews, Raisins, Emulsifier (E471), Stabilizers.",
     "score": 77},
    {"name": "Amul Shahi Anjir Ice Cream", "sub": "Royal Range",
     "ingredients": "Milk Solids, Sugar, Anjir (Fig), Honey, Cashew, Emulsifier (E471), Stabilizers.",
     "score": 76},
    {"name": "Amul Spanish Saffron Ice Cream", "sub": "Royal Range",
     "ingredients": "Milk Solids, Sugar, Spanish Saffron, Emulsifier (E471), Stabilizers.",
     "score": 77},

    # SPECIALTY RANGE
    {"name": "Amul Camel Milk Ice Cream", "sub": "Specialty Range",
     "ingredients": "Camel Milk, Milk Solids, Sugar, Emulsifiers, Stabilizers.",
     "score": 78},

    # STICK BAR RANGE
    {"name": "Amul Frostik Ice Cream Bar", "sub": "Stick Bar Range",
     "ingredients": "Milk Solids, Sugar, Chocolate Coating (Sugar, Edible Vegetable Fat, Cocoa Solids, Emulsifier E322), Emulsifier (E471), Stabilizers.",
     "score": 62},
    {"name": "Amul Choco Bar Ice Cream", "sub": "Stick Bar Range",
     "ingredients": "Milk Solids, Sugar, Chocolate Coating (Vegetable Fat, Cocoa Solids), Emulsifiers, Stabilizers.",
     "score": 63},
    {"name": "Amul Kulfi Stick", "sub": "Stick Bar Range",
     "ingredients": "Concentrated Milk Solids, Sugar, Cardamom, Almonds, Saffron.",
     "score": 82},
    {"name": "Amul Raspberry Dolly", "sub": "Stick Bar Range",
     "ingredients": "Milk Solids, Sugar. Outer Layer: Raspberry Water Ice (Sugar, Fruit Acid, Colour E122).",
     "score": 61},
    {"name": "Amul Mango Dolly", "sub": "Stick Bar Range",
     "ingredients": "Milk Solids, Sugar. Outer Layer: Mango Water Ice (Mango Pulp, Colour E110).",
     "score": 62},

    # TRADITIONAL RANGE
    {"name": "Amul Matka Kulfi", "sub": "Traditional Range",
     "ingredients": "Milk Solids (Condensed), Sugar, Saffron, Cardamom, Cashew, Pista bits.",
     "score": 83},
    {"name": "Amul Malai Kulfi Tub", "sub": "Traditional Range",
     "ingredients": "Full Cream Milk Solids, Sugar, Cardamom Flavour.",
     "score": 82},
]

def verdict(score):
    if score >= 80: return 'Clean formulation'
    if score >= 60: return 'Average formulation'
    if score >= 40: return 'Worth reviewing'
    return 'Review carefully'

def recommendation(score):
    if score >= 80: return 'Generally suitable for regular use. Check for personal allergies.'
    if score >= 60: return 'Suitable for most people. Some ingredients may warrant attention.'
    if score >= 40: return 'Review ingredient list before regular use, especially for sensitive individuals.'
    return 'Consider checking with a professional before regular use.'

def insert(p):
    name = p['name']
    score = p['score']
    ingredients_raw = p['ingredients']
    ingredients_list = [i.strip() for i in ingredients_raw.replace('. ', ', ').split(',') if i.strip()]

    try:
        existing = supabase.from_('ai_extracted_products') \
            .select('id').ilike('name', name).limit(1).execute()
        if existing.data:
            print(f"  skip: {name}")
            return False

        supabase.from_('ai_extracted_products').insert({
            'name':            name,
            'brand':           'Amul',
            'category':        'Dairy',
            'image_url':       None,
            'images':          [],
            'awareness_score': score,
            'summary': (
                f"{name} by Amul ({p['sub']}). Awareness score: {score}/100. "
                "Ingredients are based on FSSAI-compliant declarations. "
                "Not a health assessment or medical advice."
            ),
            'fssai_note':      'Subject to applicable FSSAI regulations.',
            'verdict':         verdict(score),
            'recommendation':  recommendation(score),
            'ingredients':     ingredients_list,
            'ingredients_raw': ingredients_raw,
            'status':          'active',
        }).execute()
        print(f"  + {name} | score {score}")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Amul Ice Cream products...")
    inserted = 0
    for p in PRODUCTS:
        if insert(p):
            inserted += 1
        time.sleep(0.1)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
