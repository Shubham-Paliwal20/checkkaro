"""
Insert verified Indian flagship products from Verified_Indian_Flagship_Products PDF
Major brands with authentic packaging data: Maggi, Amul, Horlicks, Coca-Cola, Cadbury, Himalaya, etc.
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = [
    'sugar', 'artificial flavor', 'artificial flavour', 'nature identical', 'sodium lauryl sulfate', 'sls',
    'artificial color', 'synthetic food colour', 'chloroxylenol', 'talc', 'methylparaben', 'propylparaben',
    'bht', 'caffeine', 'high fructose',
]
_WORTH = [
    'edible vegetable oil', 'palm oil', 'vegetable fat', 'emulsifier', 'stabilizer', 'stabiliser',
    'acidity regulator', 'flavor enhancer', 'preservative', 'citric acid', 'sodium benzoate',
    'potassium sorbate', 'color', 'dimethicone', 'paraffinum liquidum', 'petrolatum',
    'isopropyl myristate', 'zinc pyrithione', 'menthol', 'camphor', 'alcohol denat',
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
        if 'sugar' in n: return 'Sweetener; high consumption linked to health concerns'
        if 'artificial flavor' in n or 'artificial flavour' in n: return 'Synthetic replica of natural flavor'
        if 'nature identical' in n: return 'Synthetic flavor compound'
        if 'sodium lauryl sulfate' in n or 'sls' in n: return 'Harsh surfactant; can irritate skin'
        if 'artificial color' in n or 'synthetic food colour' in n: return 'Synthetic dye; regulatory scrutiny'
        if 'chloroxylenol' in n: return 'Antimicrobial; linked to concerns'
        if 'talc' in n: return 'Mineral powder; asbestos contamination concerns'
        if 'methylparaben' in n or 'propylparaben' in n: return 'Preservative; endocrine disruptor concerns'
        if 'bht' in n: return 'Antioxidant preservative; regulatory scrutiny'
        if 'caffeine' in n: return 'Stimulant; can cause dependence'
        return 'Commonly questioned ingredient'
    if cls == 'worth_knowing':
        if 'edible vegetable oil' in n or 'palm oil' in n: return 'Vegetable fat; environmental concerns'
        if 'emulsifier' in n: return 'Texture stabilizer; generally safe'
        if 'stabilizer' in n or 'stabiliser' in n: return 'Texture agent; safe in regulated amounts'
        if 'acidity regulator' in n or 'citric acid' in n: return 'pH control; safe preservative'
        if 'flavor enhancer' in n: return 'Taste enhancer; regulated ingredient'
        if 'preservative' in n or 'sodium benzoate' in n or 'potassium sorbate' in n: return 'Food preservative; safe at regulated levels'
        if 'color' in n: return 'Food coloring; regulated additive'
        if 'dimethicone' in n: return 'Silicone; conditioning agent'
        if 'paraffinum liquidum' in n or 'petrolatum' in n: return 'Mineral oil; inert moisturizer'
        if 'isopropyl myristate' in n: return 'Emollient; skin conditioning'
        if 'zinc pyrithione' in n: return 'Anti-dandruff agent; well-tolerated'
        if 'menthol' in n: return 'Cooling botanical; soothing'
        if 'camphor' in n: return 'Warming botanical; traditional use'
        if 'alcohol denat' in n or 'denatured alcohol' in n: return 'Denaturant; controlled concentration'
        return 'Moderate concern; safe in regulated amounts'
    # generally_recognised
    if 'honey' in n: return 'Natural sweetener; antioxidant properties'
    if 'milk' in n or 'milk solids' in n or 'milk fat' in n: return 'Dairy; protein and calcium source'
    if 'cocoa' in n or 'chocolate' in n: return 'Natural cocoa; antioxidant-rich'
    if 'butter' in n or 'ghee' in n: return 'Natural fat; traditional ingredient'
    if 'spices' in n or 'spice' in n: return 'Natural spice blend; traditional'
    if 'wheat' in n or 'flour' in n: return 'Grain base; carbohydrate source'
    if 'oat' in n: return 'Whole grain; nutritious'
    if 'salt' in n: return 'Iodized salt; mineral source'
    if 'water' in n: return 'Solvent; pure ingredient'
    if 'coconut oil' in n: return 'Natural oil; traditional ingredient'
    if 'almond' in n: return 'Tree nut; protein and fat rich'
    if 'neem' in n: return 'Ayurvedic herb; antibacterial'
    if 'turmeric' in n: return 'Spice; anti-inflammatory'
    if 'mint' in n or 'peppermint' in n: return 'Cooling botanical; freshening'
    if 'eucalyptus' in n: return 'Essential oil; decongestant'
    if 'rose' in n: return 'Botanical extract; soothing'
    if 'ginger' in n: return 'Spice; warming properties'
    if 'clove' in n: return 'Spice; antiseptic properties'
    if 'herbal' in n: return 'Botanical extract; traditional'
    if 'fruit' in n or 'pulp' in n: return 'Natural fruit; vitamin source'
    if 'tea' in n: return 'Natural leaf; antioxidants'
    if 'cereal' in n: return 'Grain extract; nutritious'
    if 'jelly' in n: return 'Petroleum jelly; protective barrier'
    if 'zinc oxide' in n: return 'Mineral; sun protection and skin barrier'
    if 'beeswax' in n: return 'Natural wax; protective and conditioning'
    if 'tocopherol' in n or 'vitamin e' in n: return 'Antioxidant; protective'
    return 'Food or cosmetic ingredient; safe for use'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Subject to regulatory scrutiny; permitted by FSSAI/Drugs & Cosmetics Act'
    if cls == 'worth_knowing': return 'Permitted additive; safe at regulated levels'
    return 'Approved ingredient under FSSAI/Drugs & Cosmetics regulations'

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
        elif cls == 'worth_knowing': score -= 3
    return max(0, min(100, score))

PRODUCTS = [
    # FOOD PRODUCTS
    {"name": "Maggi 2-Minute Noodles", "brand": "Nestle India", "category": "Food",
     "raw": "Refined Wheat Flour (Maida), Palm Oil, Iodized Salt, Wheat Gluten, Calcium Carbonate, Thickener (508), Acidity Regulators (501(i) & 500(i)), Humectant (451(i)). MASALA: Hydrolyzed Groundnut Protein, Mixed Spices (Onion Powder, Coriander, Chili Powder, Turmeric, Garlic Powder, Cumin, Aniseed, Ginger, Fenugreek, Black Pepper, Clove, Nutmeg, Cardamom), Sugar, Starch, Edible Vegetable Oil, Flavor Enhancer (635), Acidity Regulator (330), Color (150d), Salt."},

    {"name": "Amul Pasteurised Butter", "brand": "Amul", "category": "Food",
     "raw": "Butter (Milk Fat 80%), Common Salt, Permitted Natural Colour (Annatto - E160b)."},

    {"name": "Horlicks Classic Malt", "brand": "HUL", "category": "Food",
     "raw": "Wheat Flour (33%), Malted Barley (Extracted Solids) (27%), Milk Solids (14%), Sugar, Cereal Extract (8%), Wheat Gluten, Minerals, Soy Protein Isolate, Acidity Regulator (INS 501(ii), 500(ii)), Edible Iodized Salt, Vitamins, Nature Identical Flavouring Substances."},

    {"name": "Lay's Magic Masala", "brand": "PepsiCo", "category": "Food",
     "raw": "Potato, Edible Vegetable Oil (Palmolein, Rice Bran Oil), Spices & Condiments (Onion Powder, Chili Powder, Dry Mango Powder, Coriander Powder, Ginger Powder, Garlic Powder, Black Pepper Powder, Turmeric Powder, Cumin Powder), Salt, Black Salt, Sugar, Tomato Powder, Citric Acid (330), Tartaric Acid (334)."},

    {"name": "Coca-Cola Classic", "brand": "Coca-Cola", "category": "Food",
     "raw": "Carbonated Water, Sugar, Acidity Regulator (338), Caffeine, Permitted Natural Colour (150d), Added Flavours (Natural Flavouring Substances)."},

    {"name": "Kissan Mixed Fruit Jam", "brand": "HUL", "category": "Food",
     "raw": "Sugar, Mixed Fruit Pulp (46%), Thickener (440), Acidity Regulator (330), Preservative (211), Vitamin B3, Permitted Synthetic Food Colour (122), Added Flavours."},

    {"name": "Cadbury Dairy Milk", "brand": "Mondelez", "category": "Food",
     "raw": "Sugar, Milk Solids (22%), Cocoa Butter, Cocoa Solids, Emulsifiers (442, 476), Flavours (Natural, Nature Identical and Artificial (Ethyl Vanillin) Flavouring Substances)."},

    {"name": "Dabur Honey", "brand": "Dabur", "category": "Food",
     "raw": "100% Pure Honey."},

    {"name": "Mother Dairy Full Cream Milk", "brand": "Mother Dairy", "category": "Food",
     "raw": "Milk Fat (6.0% min), Milk Solids Not Fat (9.0% min), Vitamin A, Vitamin D."},

    {"name": "Parle-G Biscuits", "brand": "Parle", "category": "Food",
     "raw": "Wheat Flour, Sugar, Edible Vegetable Oil, Invert Sugar Syrup, Raising Agents [503 (ii), 500 (ii)], Salt, Milk Solids, Emulsifier [322], Dough Conditioner [223]."},

    {"name": "Britannia Marie Gold", "brand": "Britannia", "category": "Food",
     "raw": "Refined Wheat Flour (Maida), Sugar, Refined Palm Oil, Invert Sugar Syrup, Raising Agents [503(ii), 500(ii)], Milk Solids, Iodized Salt, Emulsifiers [322(i), 471, 472e], Flour Treatment Agents [223, 1101(i)]."},

    {"name": "Real Fruit Power Mango", "brand": "Dabur", "category": "Food",
     "raw": "Water, Mango Pulp (25%), Sugar, Acidity Regulator (330), Stabilizer (440), Antioxidant (300)."},

    {"name": "Red Label Tea", "brand": "HUL", "category": "Food",
     "raw": "Tea (CTC Leaf), Added Flavours."},

    {"name": "Bournvita Drink", "brand": "Mondelez", "category": "Food",
     "raw": "Cereal Extract (56%), Sugar, Cocoa Solids, Milk Solids, Liquid Glucose, Emulsifiers (322, 471), Raising Agent (500(ii)), Vitamins, Minerals, Edible Salt. Contains Permitted Natural Colour (150c)."},

    {"name": "Tata Salt", "brand": "Tata Consumer", "category": "Food",
     "raw": "Edible Common Salt, Iodine, Anticaking Agent (551), Potassium Iodate."},

    # COSMETIC/PERSONAL CARE PRODUCTS
    {"name": "Himalaya Neem Face Wash", "brand": "Himalaya", "category": "Personal Care",
     "raw": "Aqua, Ammonium Lauryl Sulfate, Melia Azadirachta Leaf Extract, Cocamidopropyl Betaine, Sodium Cocoyl Glycinate, Glycerin, Acrylates/C10-30 Alkyl Acrylate Crosspolymer, Phenoxyethanol, Fragrance, Curcuma Longa Root Extract, Methylchloroisothiazolinone, Methylisothiazolinone, Disodium EDTA, Citric Acid, CI 19140, CI 42090."},

    {"name": "Pond's Light Moisturiser", "brand": "HUL", "category": "Personal Care",
     "raw": "Water, Isopropyl Myristate, Niacinamide, Stearic Acid, Glyceryl Stearate, Mineral Oil, Ethylhexyl Methoxycinnamate, Glycerin, Cetyl Alcohol, Dimethicone, Phenoxyethanol, Potassium Hydroxide, Methylparaben, Propylparaben, Disodium EDTA, BHT."},

    {"name": "Dettol Antiseptic Liquid", "brand": "Reckitt", "category": "Personal Care",
     "raw": "Chloroxylenol (4.8% w/v), Terpineol, Alcohol (Denatured), Caramel, Pine Oil, Water, Castor Oil Soap."},

    {"name": "Dove Beauty Bar", "brand": "Unilever", "category": "Personal Care",
     "raw": "Sodium Lauroyl Isethionate, Stearic Acid, Lauric Acid, Sodium Palmate, Water, Sodium Isethionate, Sodium Stearate, Cocamidopropyl Betaine, Sodium Palm Kernelate, Glycerin, Perfume, Sodium Chloride, Zinc Oxide, Tetrasodium EDTA, CI 77891."},

    {"name": "Parachute Hair Oil", "brand": "Marico", "category": "Personal Care",
     "raw": "100% Pure Coconut Oil."},

    {"name": "Head & Shoulders Shampoo", "brand": "P&G", "category": "Personal Care",
     "raw": "Water, Sodium Laureth Sulfate, Sodium Lauryl Sulfate, Sodium Chloride, Sodium Xylenesulfonate, Glycol Distearate, Zinc Pyrithione, Dimethicone, Fragrance, Cetyl Alcohol, Guar Hydroxypropyltrimonium Chloride, Magnesium Carbonate Hydroxide, Methylchloroisothiazolinone."},

    {"name": "Glow & Lovely Cream", "brand": "HUL", "category": "Personal Care",
     "raw": "Water, Palmitic Acid, Stearic Acid, Niacinamide, Glycerin, Cetearyl Ethylhexanoate, Isopropyl Myristate, Ethylhexyl Methoxycinnamate, Butyl Methoxydibenzoylmethane, Sodium Ascorbyl Phosphate, Tocopheryl Acetate, Titanium Dioxide."},

    {"name": "Colgate Strong Teeth", "brand": "Colgate", "category": "Personal Care",
     "raw": "Calcium Carbonate, Sorbitol, Sodium Lauryl Sulfate, Silica, Titanium Dioxide, Sodium Silicate, Carrageenan, Sodium Monofluorophosphate, Sodium Saccharin, Flavor, Water."},

    {"name": "Vicks Vaporub", "brand": "P&G", "category": "Personal Care",
     "raw": "Menthol (2.82%), Camphor (5.25%), Eucalyptus Oil (1.35%), Ajwain Flower (0.10%), Turpentine Oil, Cedar Leaf Oil, Petrolatum q.s."},

    {"name": "Nivea Soft Cream", "brand": "Beiersdorf", "category": "Personal Care",
     "raw": "Aqua, Glycerin, Paraffinum Liquidum, Myristyl Alcohol, Butylene Glycol, Alcohol Denat., Stearic Acid, Myristyl Myristate, Cera Microcristallina, Glyceryl Stearate, Simmondsia Chinensis Seed Oil, Tocopheryl Acetate."},

    {"name": "Vaseline Jelly", "brand": "HUL", "category": "Personal Care",
     "raw": "White Petrolatum USP (100%)."},

    {"name": "Dabur Red Paste", "brand": "Dabur", "category": "Personal Care",
     "raw": "Calcium Carbonate, Sorbitol, Water, Silica, Sodium Lauryl Sulfate, Herbal Extract (Clove, Mint, Tomar, Ginger, Pippali), Red Ochre, Flavor, Sodium Silicate."},

    {"name": "Johnson's Baby Powder", "brand": "J&J", "category": "Personal Care",
     "raw": "Talc, Fragrance, Benzyl Benzoate, Citronellol, Coumarin, Geraniol, Linalool."},

    {"name": "Lakme Sun Expert", "brand": "HUL", "category": "Personal Care",
     "raw": "Water, Cyclopentasiloxane, Ethylhexyl Methoxycinnamate, Zinc Oxide, Phenylbenzimidazole Sulfonic Acid, Niacinamide, Triethanolamine, Glycerin, Phenoxyethanol, Methylparaben, Disodium EDTA."},

    {"name": "Sunsilk Black Shine", "brand": "HUL", "category": "Personal Care",
     "raw": "Water, Sodium Laureth Sulfate, Cocamidopropyl Betaine, Sodium Chloride, Fragrance, Dimethiconol, Carbomer, Mica, Titanium Dioxide, Citric Acid, Amla Extract."},
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
                f"{name} by {p['brand']}. Verified flagship product. "
                f"Awareness score: {score}/100. Not a health assessment."
            ),
            'fssai_note':      'Flagship brand; verified packaging data.',
            'verdict':         'Standard formulation' if score >= 70 else 'Contains additives',
            'recommendation':  'Popular choice; use as directed.' if score >= 70 else 'Review ingredients before use.',
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
    print(f"Inserting {len(PRODUCTS)} verified Indian flagship products...")
    inserted = 0
    for p in PRODUCTS:
        if insert(p):
            inserted += 1
        time.sleep(0.1)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
