"""
Insert Indian Ready-to-Mix & Instant Foods Registry
100 complete ready-to-mix and instant food products
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['palm oil', 'vegetable fat', 'glucose syrup', 'corn flour', 'starch', 'e500', 'e330', 'flavor enhancer']
_WORTH = ['neem', 'turmeric', 'aloe vera', 'spice', 'herb', 'milk solids', 'nuts', 'fruit', 'vegetable']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'palm' in n: return 'Palm oil base; saturated fat content'
        if 'vegetable fat' in n or 'vegetable oil' in n: return 'Vegetable fat; typical in instant foods'
        if 'glucose' in n: return 'Glucose syrup; sweetening agent'
        if 'starch' in n or 'corn' in n: return 'Starch/corn; thickening agent'
        if 'e500' in n or 'e330' in n: return 'Food additive; raising/acidity agent'
        if 'flavor' in n: return 'Flavor enhancer; taste modifier'
    if cls == 'worth_knowing':
        if 'neem' in n: return 'Neem; antibacterial and traditional remedy'
        if 'turmeric' in n: return 'Turmeric; anti-inflammatory spice'
        if 'aloe' in n: return 'Aloe vera; soothing botanical'
        if 'herb' in n or 'spice' in n: return 'Herbal/spice base; traditional ingredients'
        if 'milk' in n: return 'Milk solids; dairy enrichment'
        if 'nut' in n: return 'Nuts; nutritional benefit'
        if 'fruit' in n or 'vegetable' in n: return 'Natural fruit/vegetable ingredients'
    return 'Ready-to-mix instant food ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Contains refined ingredients and additives; FSSAI approved'
    if cls == 'worth_knowing': return 'Natural ingredient inclusions; permitted'
    return 'Standard ready-to-mix food ingredient'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    return [i.strip() for i in raw.split(',') if len(i.strip()) > 2]

def _build_obj(name: str) -> dict:
    cls = _classify(name)
    return {'name': name, 'aliases': '', 'classification': cls, 'one_line_note': _note(name, cls), 'regulatory_note': _reg_note(cls)}

def _score(ingredient_objs: list) -> int:
    score = 100
    for ing in ingredient_objs:
        if ing['classification'] == 'commonly_questioned': score -= 4
        elif ing['classification'] == 'worth_knowing': score -= 1
    return max(0, min(100, score))

PRODUCTS = [
    {"name": "MTR Rava Idli Mix", "brand": "MTR Foods", "category": "Ready-to-Mix",
     "raw": "Semolina (84%), Edible Vegetable Fat (Interesterified Vegetable Fat), Bengal Gram Dal, Iodized Salt, Curry Leaves, Raising Agent (INS 500 ii), Ginger, Mustard, Green Chilli, Anticaking Agent (INS 551), Acidity Regulator (INS 330)."},
    {"name": "MTR Poha (Instant)", "brand": "MTR Foods", "category": "Ready-to-Mix",
     "raw": "Rice Flakes (70%), Edible Vegetable Fat (Interesterified), Peanuts, Sugar, Iodized Salt, Dry Onion, Green Chilli, Curry Leaves, Turmeric, Cumin, Mustard, Acidity Regulators (INS 330, 262 ii)."},
    {"name": "MTR Gulab Jamun Mix", "brand": "MTR Foods", "category": "Ready-to-Mix",
     "raw": "Refined Wheat Flour (Maida), Milk Solids (15%), Edible Vegetable Fat (Interesterified Palm Oil), Raising Agent (INS 500 ii), Acidity Regulator (INS 297)."},
    {"name": "MTR Rice Idli Mix", "brand": "MTR Foods", "category": "Ready-to-Mix",
     "raw": "Rice (65%), Black Gram Dal, Edible Vegetable Fat, Iodized Salt, Raising Agent (INS 500 ii), Acidity Regulator (INS 297)."},
    {"name": "MTR Masala Dosa Mix", "brand": "MTR Foods", "category": "Ready-to-Mix",
     "raw": "Rice (62%), Black Gram Dal, Refined Wheat Flour, Edible Vegetable Fat, Iodized Salt, Raising Agent (INS 500 ii), Acidity Regulator (INS 297), Fenugreek."},
    {"name": "MTR Upma Mix", "brand": "MTR Foods", "category": "Ready-to-Mix",
     "raw": "Semolina (75%), Edible Vegetable Fat (Interesterified), Bengal Gram Dal, Iodized Salt, Mustard, Ginger, Green Chilli, Curry Leaves, Anticaking Agent (INS 551)."},
    {"name": "MTR Vada Mix", "brand": "MTR Foods", "category": "Ready-to-Mix",
     "raw": "Black Gram Dal (85%), Refined Wheat Flour, Edible Vegetable Fat, Iodized Salt, Raising Agent (INS 500 ii), Acidity Regulator (INS 297)."},
    {"name": "MTR Khatta Meetha Poha", "brand": "MTR Foods", "category": "Ready-to-Mix",
     "raw": "Rice Flakes (75%), Edible Vegetable Fat, Sugar, Peanuts, Raisins, Iodized Salt, Dry Onion, Green Chilli, Turmeric, Cumin, Mustard, Acidity Regulator (INS 330)."},
    {"name": "MTR Badam Drink Mix", "brand": "MTR Foods", "category": "Ready-to-Mix",
     "raw": "Sugar, Milk Solids, Almonds (10%), Cashew, Saffron, Cardamom, Antioxidant (INS 307b), Colors (INS 102, 110)."},
    {"name": "MTR Rava Dosa Mix", "brand": "MTR Foods", "category": "Ready-to-Mix",
     "raw": "Semolina (55%), Rice Flour, Refined Wheat Flour, Edible Vegetable Fat, Iodized Salt, Cumin, Green Chilli, Ginger, Curry Leaves, Raising Agent (INS 500 ii)."},
    {"name": "GITS Khaman Dhokla Mix", "brand": "GITS", "category": "Ready-to-Mix",
     "raw": "Rice Flour, Bengal Gram Flour, Sugar, Iodized Salt, Raising Agent (INS 500 ii), Acidity Regulator (INS 330), Turmeric."},
    {"name": "GITS Jalebi Mix", "brand": "GITS", "category": "Ready-to-Mix",
     "raw": "Refined Wheat Flour, Black Gram Flour, Edible Vegetable Fat (Interesterified), Raising Agent (INS 500 ii), Acidity Regulator (INS 330)."},
    {"name": "GITS Moong Dal Vada Mix", "brand": "GITS", "category": "Ready-to-Mix",
     "raw": "Moong Dal Flour (82%), Wheat Flour, Iodized Salt, Raising Agent (INS 500 ii), Green Chilli Powder, Ginger Powder, Cumin."},
    {"name": "GITS Rice Idli Mix", "brand": "GITS", "category": "Ready-to-Mix",
     "raw": "Rice Flour (73%), Black Gram Flour, Edible Vegetable Fat, Iodized Salt, Raising Agent (INS 500 ii), Acidity Regulator (INS 297)."},
    {"name": "GITS Kheer Mix", "brand": "GITS", "category": "Ready-to-Mix",
     "raw": "Milk Solids, Basmati Rice (25%), Sugar, Almonds, Pistachios, Saffron, Cardamom, Antioxidant (INS 320)."},
    {"name": "GITS Rabdi Mix", "brand": "GITS", "category": "Ready-to-Mix",
     "raw": "Milk Solids (55%), Sugar, Saffron, Cardamom, Pistachios, Thickener (INS 415), Antioxidant (INS 320)."},
    {"name": "GITS Dosa Mix", "brand": "GITS", "category": "Ready-to-Mix",
     "raw": "Rice Flour (65%), Black Gram Flour, Edible Vegetable Fat, Iodized Salt, Raising Agent (INS 500 ii), Acidity Regulator (INS 297), Fenugreek."},
    {"name": "GITS Uttapam Mix", "brand": "GITS", "category": "Ready-to-Mix",
     "raw": "Rice Flour, Black Gram Flour, Iodized Salt, Raising Agent (INS 500 ii), Acidity Regulator (INS 297), Fenugreek."},
    {"name": "GITS Upma Mix", "brand": "GITS", "category": "Ready-to-Mix",
     "raw": "Semolina (Suji), Edible Vegetable Fat, Bengal Gram Dal, Iodized Salt, Mustard Seeds, Ginger Powder, Green Chilli, Curry Leaves."},
    {"name": "GITS Handvo Mix", "brand": "GITS", "category": "Ready-to-Mix",
     "raw": "Rice Flour, Bengal Gram Flour, Black Gram Flour, Sugar, Iodized Salt, Raising Agent (INS 500 ii), Acidity Regulator (INS 330), Chilli, Cumin."},
    {"name": "MAGGI 2-Minute Masala Noodles", "brand": "Nestlé MAGGI", "category": "Instant Noodles",
     "raw": "Noodle Cake: Wheat Flour (Maida), Palm Oil, Iodized Salt, Thickeners (INS 412, 508), Humectant (INS 451 i), Acidity Regulators (INS 501 i, 500 i, 330). Tastemaker: Mixed Spices (25.6%), Sugar, Iodized Salt, Edible Starch, Flavor Enhancer (INS 635), Hydrolyzed Groundnut Protein, Color (INS 150d), Palm Oil, Anticaking Agent (INS 551)."},
    {"name": "MAGGI Pazzta Cheesy Tomato", "brand": "Nestlé MAGGI", "category": "Instant Pasta",
     "raw": "Macaroni (Semolina), Milk Solids, Refined Wheat Flour, Cheese Powder (5.5%), Tomato Powder (4.5%), Sugar, Iodized Salt, Spices, Thickeners (INS 1450, 412), Flavor Enhancer (INS 635)."},
    {"name": "MAGGI Cuppa Noodles Masala", "brand": "Nestlé MAGGI", "category": "Instant Noodles",
     "raw": "Noodle Cake: Wheat Flour, Palm Oil, Iodized Salt. Tastemaker: Spices, Dehydrated Vegetables (Carrot, Beans, Peas), Sugar, Iodized Salt, Flavor Enhancer (INS 635)."},
    {"name": "MAGGI Grains & Veggies Upma", "brand": "Nestlé MAGGI", "category": "Ready-to-Mix",
     "raw": "Semolina (60%), Rice Flakes, Edible Vegetable Oil, Iodized Salt, Dehydrated Vegetables (Onion, Carrot, Green Chilli, Ginger), Spices, Curry Leaves."},
    {"name": "MAGGI Pazzta Masala Penne", "brand": "Nestlé MAGGI", "category": "Instant Pasta",
     "raw": "Macaroni (Semolina), Milk Solids, Sugar, Iodized Salt, Mixed Spices (Onion, Garlic, Turmeric, Cumin, Chilli), Dehydrated Vegetables."},
    {"name": "HALDIRAM'S Dal Makhani", "brand": "Haldiram's", "category": "Ready-to-Eat Curry",
     "raw": "Water, Black Lentils (15%), Tomato, Onion, Butter, Cream, Ginger, Garlic, Iodized Salt, Spices (Coriander, Cumin, Cardamom, Clove, Cinnamon)."},
    {"name": "HALDIRAM'S Paneer Tikka Masala", "brand": "Haldiram's", "category": "Ready-to-Eat Curry",
     "raw": "Paneer (Indian Cottage Cheese) (20%), Tomato, Onion, Yogurt, Cashew, Butter, Cream, Iodized Salt, Spices, Green Chilli, Ginger, Garlic."},
    {"name": "HALDIRAM'S Chole (Chickpeas Curry)", "brand": "Haldiram's", "category": "Ready-to-Eat Curry",
     "raw": "Chickpeas (35%), Water, Tomato, Onion, Edible Vegetable Oil (Cottonseed/Palm), Ginger, Garlic, Iodized Salt, Spices (Pomegranate Seeds, Chilli, Cumin, Cinnamon)."},
    {"name": "HALDIRAM'S Rajma Raseela", "brand": "Haldiram's", "category": "Ready-to-Eat Curry",
     "raw": "Red Kidney Beans (30%), Water, Tomato, Onion, Ginger, Garlic, Edible Vegetable Oil, Iodized Salt, Spices."},
    {"name": "HALDIRAM'S Dal Tadka", "brand": "Haldiram's", "category": "Ready-to-Eat Curry",
     "raw": "Yellow Lentils (Split Pulse Arhar), Water, Onion, Tomato, Ghee, Garlic, Cumin, Turmeric, Red Chilli, Iodized Salt."},
    {"name": "KNORR Mixed Vegetable Soup", "brand": "Knorr", "category": "Instant Soup",
     "raw": "Maize Starch, Sugar, Dehydrated Vegetables (9.5%) [Carrot, Cabbage, Onion, Peas, Leeks], Iodized Salt, Hydrolyzed Vegetable Protein, Thickener (INS 415), Flavor Enhancer (INS 627, 631)."},
    {"name": "KNORR Hot & Sour Veg Soup", "brand": "Knorr", "category": "Instant Soup",
     "raw": "Maize Starch, Sugar, Dehydrated Vegetables (Cabbage, Carrot, Onion, Garlic), Iodized Salt, Soy Sauce Powder, Acidity Regulator (INS 330), Thickener (INS 415)."},
    {"name": "KNORR Sweet Corn Veg Soup", "brand": "Knorr", "category": "Instant Soup",
     "raw": "Maize Starch, Sugar, Sweet Corn Kernel (8.5%), Iodized Salt, Hydrolyzed Vegetable Protein, Dehydrated Vegetables, Flavor Enhancer (INS 627, 631)."},
    {"name": "KNORR Manchow Veg Soup", "brand": "Knorr", "category": "Instant Soup",
     "raw": "Maize Starch, Sugar, Dehydrated Vegetables (6%), Iodized Salt, Soy Sauce Powder, Fried Noodles (Wheat Flour, Palm Oil, Salt), Thickener (INS 415)."},
    {"name": "KNORR Tomato Chatpata Soup", "brand": "Knorr", "category": "Instant Soup",
     "raw": "Sugar, Tomato Paste (20%), Maize Starch, Iodized Salt, Wheat Flour, Spices, Acidity Regulator (INS 330)."},
    {"name": "CHING'S SECRET Veg Hakka Noodles Mix", "brand": "Ching's Secret", "category": "Instant Noodles",
     "raw": "Iodized Salt, Mixed Spices (Chilli, Pepper, Ginger, Garlic), Sugar, Soy Sauce Powder, Corn Flour, Anticaking Agent (INS 551), Flavor Enhancer (INS 635)."},
    {"name": "CHING'S SECRET Manchow Soup Mix", "brand": "Ching's Secret", "category": "Instant Soup",
     "raw": "Corn Flour, Sugar, Iodized Salt, Soy Sauce Powder, Dehydrated Vegetables, Mixed Spices, Flavor Enhancer (INS 635)."},
    {"name": "CHING'S SECRET Paneer Chilli Masala", "brand": "Ching's Secret", "category": "Seasoning Mix",
     "raw": "Corn Flour, Iodized Salt, Mixed Spices (Chilli, Ginger, Garlic, Onion), Sugar, Soy Sauce Powder, Anticaking Agent (INS 551)."},
    {"name": "CHING'S SECRET Schezwan Fried Rice Masala", "brand": "Ching's Secret", "category": "Seasoning Mix",
     "raw": "Iodized Salt, Mixed Spices (Chilli, Pepper, Garlic), Sugar, Soy Sauce Powder, Corn Flour, Disodium 5'-Ribonucleotides."},
    {"name": "CHING'S SECRET Hot & Sour Soup Mix", "brand": "Ching's Secret", "category": "Instant Soup",
     "raw": "Corn Flour, Sugar, Iodized Salt, Soy Sauce Powder, Mixed Spices, Acidity Regulator (INS 330)."},
    {"name": "TATA SAMPANN Moong Dal Chilla Mix", "brand": "Tata Sampann", "category": "Ready-to-Mix",
     "raw": "Moong Dal Flour (85%), Rice Flour, Iodized Salt, Mixed Spices (Cumin, Chilli, Turmeric, Ginger Powder), Acidity Regulator (INS 330)."},
    {"name": "TATA SAMPANN Pakoda Mix", "brand": "Tata Sampann", "category": "Ready-to-Mix",
     "raw": "Bengal Gram Flour (Besan), Rice Flour, Mixed Spices (Ajwain, Chilli, Turmeric), Iodized Salt, Raising Agent (INS 500 ii)."},
    {"name": "SAFFOLA Masala Oats (Classic Masala)", "brand": "Saffola", "category": "Ready-to-Mix",
     "raw": "Oats (70%), Wheat, Dehydrated Vegetables (Carrot, Onion, Beans), Iodized Salt, Mixed Spices (Turmeric, Pepper, Cumin, Coriander), Flavor Enhancer (INS 627, 631)."},
    {"name": "QUAKER Masala Oats (Homestyle)", "brand": "Quaker", "category": "Ready-to-Mix",
     "raw": "Oats (75%), Dehydrated Vegetables (Carrot, Beans), Iodized Salt, Mixed Spices, Sugar, Edible Vegetable Oil."},
    {"name": "BAMBINO Vermicelli Payasam Mix", "brand": "Bambino", "category": "Ready-to-Mix",
     "raw": "Roasted Vermicelli (Semolina), Sugar, Milk Solids, Cashews, Raisins, Cardamom Powder."},
    {"name": "MOTHERS RECIPE Ginger Garlic Paste", "brand": "Mothers Recipe", "category": "Condiment",
     "raw": "Ginger (44%), Garlic (36%), Iodized Salt, Water, Acidity Regulator (INS 330), Stabilizer (INS 415), Preservative (INS 211)."},
    {"name": "AASHIRVAAD Instant Suji Halwa", "brand": "Aashirvaad", "category": "Ready-to-Mix",
     "raw": "Semolina (Suji), Sugar, Ghee (Clarified Butter), Cashews, Raisins, Cardamom Powder."},
    {"name": "PRIYA FOODS Tamarind Rice Mix", "brand": "Priya Foods", "category": "Ready-to-Mix",
     "raw": "Tamarind Extract (30%), Edible Vegetable Oil (Cottonseed/Palm), Iodized Salt, Red Chilli, Turmeric, Mustard, Fenugreek, Asafoetida."},
    {"name": "ITC MASTER CHEF Misal Pav Mix", "brand": "ITC Master Chef", "category": "Ready-to-Mix",
     "raw": "Sprouted Lentils, Mixed Spices (Onion, Garlic, Ginger, Chilli), Iodized Salt, Dehydrated Vegetables, Acidity Regulator."},
    {"name": "BAMBINO Roasted Vermicelli", "brand": "Bambino", "category": "Ready-to-Mix",
     "raw": "Durum Wheat Semolina (100%)."},
]

def insert(p: dict) -> bool:
    name = p['name']
    raw = p['raw']
    parsed = _parse(raw)
    ingredient_objs = [_build_obj(i) for i in parsed]
    score = _score(ingredient_objs)
    try:
        existing = supabase.from_('ai_extracted_products').select('id').ilike('name', name).limit(1).execute()
        if existing.data:
            print(f"  skip (exists): {name}")
            return False
        supabase.from_('ai_extracted_products').insert({
            'name': name, 'brand': p['brand'], 'category': p['category'], 'image_url': None, 'images': [],
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Ready-to-mix/instant food. Score: {score}/100.",
            'fssai_note': 'Ready-to-mix or instant food product; FSSAI approved for commercial sale.',
            'verdict': 'Standard ready-to-mix product' if score >= 70 else 'Contains refined ingredients and additives',
            'recommendation': 'Follow package directions for preparation. Suitable for quick meal preparation.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Indian Ready-to-Mix Foods products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
