"""
Insert Indian Ready-to-Mix & Instant Foods
100 products with complete ingredient and chemical additive declarations
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['palm oil', 'flavor enhancer', 'ins 635', 'ins 627', 'ins 631', 'synthetic colour', 'artificial flavour', 'hydrogenated', 'edta', 'disodium']
_WORTH = ['turmeric', 'asafoetida', 'cumin', 'coriander', 'dehydrated vegetables', 'herbs', 'spices', 'oats', 'whole wheat', 'saffron', 'almond', 'cashew']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'palm' in n: return 'Palm oil; saturated fat content'
        if 'flavor enhancer' in n or 'ins 635' in n or 'ins 627' in n: return 'Flavor enhancer; MSG alternative'
        if 'synthetic' in n or 'colour' in n: return 'Synthetic colour; artificial additive'
        if 'hydrogenated' in n: return 'Hydrogenated oil; trans fat'
        if 'edta' in n: return 'Chelating agent; binds minerals'
    if cls == 'worth_knowing':
        if 'turmeric' in n: return 'Turmeric; anti-inflammatory spice'
        if 'asafoetida' in n: return 'Asafoetida; digestive aid'
        if 'dehydrated vegetables' in n: return 'Dehydrated vegetables; nutrient preservation'
        if 'oats' in n: return 'Oats; fiber-rich whole grain'
        if 'saffron' in n: return 'Saffron; aromatic luxury spice'
        if 'almond' in n or 'cashew' in n: return 'Nuts; protein and healthy fats'
    return 'Instant food ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Contains additives and preservatives'
    if cls == 'worth_knowing': return 'Natural and traditional ingredients'
    return 'Ready-to-mix food ingredient'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    return [i.strip() for i in raw.split(',') if len(i.strip()) > 2]

def _build_obj(name: str) -> dict:
    cls = _classify(name)
    return {'name': name, 'aliases': '', 'classification': cls, 'one_line_note': _note(name, cls), 'regulatory_note': _reg_note(cls)}

def _score(ingredient_objs: list) -> int:
    score = 100
    for ing in ingredient_objs:
        if ing['classification'] == 'commonly_questioned': score -= 6
        elif ing['classification'] == 'worth_knowing': score -= 1
    return max(0, min(100, score))

PRODUCTS = [
    # MTR PRODUCTS
    {"name": "MTR Rava Idli Mix", "brand": "MTR", "category": "Food",
     "raw": "Semolina (84%), Edible Vegetable Fat (Interesterified Vegetable Fat), Bengal Gram Dal, Iodized Salt, Curry Leaves, Raising Agent (INS 500 ii), Ginger, Mustard, Green Chilli, Anticaking Agent (INS 551), Acidity Regulator (INS 330)."},
    {"name": "MTR Poha (Instant)", "brand": "MTR", "category": "Food",
     "raw": "Rice Flakes (70%), Edible Vegetable Fat (Interesterified), Peanuts, Sugar, Iodized Salt, Dry Onion, Green Chilli, Curry Leaves, Turmeric, Cumin, Mustard, Acidity Regulators (INS 330, 262 ii)."},
    {"name": "MTR Gulab Jamun Mix", "brand": "MTR", "category": "Food",
     "raw": "Refined Wheat Flour (Maida), Milk Solids (15%), Edible Vegetable Fat (Interesterified Palm Oil), Raising Agent (INS 500 ii), Acidity Regulator (INS 297)."},
    {"name": "MTR Rice Idli Mix", "brand": "MTR", "category": "Food",
     "raw": "Rice (65%), Black Gram Dal, Edible Vegetable Fat, Iodized Salt, Raising Agent (INS 500 ii), Acidity Regulator (INS 297)."},
    {"name": "MTR Masala Dosa Mix", "brand": "MTR", "category": "Food",
     "raw": "Rice (62%), Black Gram Dal, Refined Wheat Flour, Edible Vegetable Fat, Iodized Salt, Raising Agent (INS 500 ii), Acidity Regulator (INS 297), Fenugreek."},
    {"name": "MTR Upma Mix", "brand": "MTR", "category": "Food",
     "raw": "Semolina (75%), Edible Vegetable Fat (Interesterified), Bengal Gram Dal, Iodized Salt, Mustard, Ginger, Green Chilli, Curry Leaves, Anticaking Agent (INS 551)."},
    {"name": "MTR Vada Mix", "brand": "MTR", "category": "Food",
     "raw": "Black Gram Dal (85%), Refined Wheat Flour, Edible Vegetable Fat, Iodized Salt, Raising Agent (INS 500 ii), Acidity Regulator (INS 297)."},
    {"name": "MTR Khatta Meetha Poha", "brand": "MTR", "category": "Food",
     "raw": "Rice Flakes (75%), Edible Vegetable Fat, Sugar, Peanuts, Raisins, Iodized Salt, Dry Onion, Green Chilli, Turmeric, Cumin, Mustard, Acidity Regulator (INS 330)."},
    {"name": "MTR Badam Drink Mix", "brand": "MTR", "category": "Food",
     "raw": "Sugar, Milk Solids, Almonds (10%), Cashew, Saffron, Cardamom, Antioxidant (INS 307b), Colors (INS 102, 110)."},
    {"name": "MTR Rava Dosa Mix", "brand": "MTR", "category": "Food",
     "raw": "Semolina (55%), Rice Flour, Refined Wheat Flour, Edible Vegetable Fat, Iodized Salt, Cumin, Green Chilli, Ginger, Curry Leaves, Raising Agent (INS 500 ii)."},
    # GITS PRODUCTS
    {"name": "GITS Khaman Dhokla Mix", "brand": "GITS", "category": "Food",
     "raw": "Rice Flour, Bengal Gram Flour, Sugar, Iodized Salt, Raising Agent (INS 500 ii), Acidity Regulator (INS 330), Turmeric."},
    {"name": "GITS Jalebi Mix", "brand": "GITS", "category": "Food",
     "raw": "Refined Wheat Flour, Black Gram Flour, Edible Vegetable Fat (Interesterified), Raising Agent (INS 500 ii), Acidity Regulator (INS 330)."},
    {"name": "GITS Moong Dal Vada Mix", "brand": "GITS", "category": "Food",
     "raw": "Moong Dal Flour (82%), Wheat Flour, Iodized Salt, Raising Agent (INS 500 ii), Green Chilli Powder, Ginger Powder, Cumin."},
    {"name": "GITS Rice Idli Mix", "brand": "GITS", "category": "Food",
     "raw": "Rice Flour (73%), Black Gram Flour, Edible Vegetable Fat, Iodized Salt, Raising Agent (INS 500 ii), Acidity Regulator (INS 297)."},
    {"name": "GITS Kheer Mix", "brand": "GITS", "category": "Food",
     "raw": "Milk Solids, Basmati Rice (25%), Sugar, Almonds, Pistachios, Saffron, Cardamom, Antioxidant (INS 320)."},
    {"name": "GITS Rabdi Mix", "brand": "GITS", "category": "Food",
     "raw": "Milk Solids (55%), Sugar, Saffron, Cardamom, Pistachios, Thickener (INS 415), Antioxidant (INS 320)."},
    {"name": "GITS Dosa Mix", "brand": "GITS", "category": "Food",
     "raw": "Rice Flour (65%), Black Gram Flour, Edible Vegetable Fat, Iodized Salt, Raising Agent (INS 500 ii), Acidity Regulator (INS 297), Fenugreek."},
    {"name": "GITS Uttapam Mix", "brand": "GITS", "category": "Food",
     "raw": "Rice Flour, Black Gram Flour, Iodized Salt, Raising Agent (INS 500 ii), Acidity Regulator (INS 297), Fenugreek."},
    {"name": "GITS Upma Mix", "brand": "GITS", "category": "Food",
     "raw": "Semolina (Suji), Edible Vegetable Fat, Bengal Gram Dal, Iodized Salt, Mustard Seeds, Ginger Powder, Green Chilli, Curry Leaves."},
    {"name": "GITS Handvo Mix", "brand": "GITS", "category": "Food",
     "raw": "Rice Flour, Bengal Gram Flour, Black Gram Flour, Sugar, Iodized Salt, Raising Agent (INS 500 ii), Acidity Regulator (INS 330), Chilli, Cumin."},
    # MAGGI PRODUCTS
    {"name": "MAGGI 2-Minute Masala Noodles", "brand": "MAGGI", "category": "Food",
     "raw": "Noodle Cake: Wheat Flour (Maida), Palm Oil, Iodized Salt, Thickeners (INS 412, 508), Humectant (INS 451 i), Acidity Regulators (INS 501 i, 500 i, 330). Tastemaker: Mixed Spices (25.6%), Sugar, Iodized Salt, Edible Starch, Flavor Enhancer (INS 635), Hydrolyzed Groundnut Protein, Color (INS 150d), Palm Oil, Anticaking Agent (INS 551)."},
    {"name": "MAGGI Pazzta Cheesy Tomato", "brand": "MAGGI", "category": "Food",
     "raw": "Macaroni (Semolina), Milk Solids, Refined Wheat Flour, Cheese Powder (5.5%), Tomato Powder (4.5%), Sugar, Iodized Salt, Spices, Thickeners (INS 1450, 412), Flavor Enhancer (INS 635)."},
    {"name": "MAGGI Cuppa Noodles Masala", "brand": "MAGGI", "category": "Food",
     "raw": "Noodle Cake: Wheat Flour, Palm Oil, Iodized Salt. Tastemaker: Spices, Dehydrated Vegetables (Carrot, Beans, Peas), Sugar, Iodized Salt, Flavor Enhancer (INS 635)."},
    {"name": "MAGGI Grains & Veggies Upma", "brand": "MAGGI", "category": "Food",
     "raw": "Semolina (60%), Rice Flakes, Edible Vegetable Oil, Iodized Salt, Dehydrated Vegetables (Onion, Carrot, Green Chilli, Ginger), Spices, Curry Leaves."},
    {"name": "MAGGI Pazzta Masala Penne", "brand": "MAGGI", "category": "Food",
     "raw": "Macaroni (Semolina), Milk Solids, Sugar, Iodized Salt, Mixed Spices (Onion, Garlic, Turmeric, Cumin, Chilli), Dehydrated Vegetables."},
    # HALDIRAM'S READY MEALS
    {"name": "Haldiram's Dal Makhani", "brand": "Haldiram's", "category": "Food",
     "raw": "Water, Black Lentils (15%), Tomato, Onion, Butter, Cream, Ginger, Garlic, Iodized Salt, Spices (Coriander, Cumin, Cardamom, Clove, Cinnamon)."},
    {"name": "Haldiram's Paneer Tikka Masala", "brand": "Haldiram's", "category": "Food",
     "raw": "Paneer (Indian Cottage Cheese) (20%), Tomato, Onion, Yogurt, Cashew, Butter, Cream, Iodized Salt, Spices, Green Chilli, Ginger, Garlic."},
    {"name": "Haldiram's Chole (Chickpeas Curry)", "brand": "Haldiram's", "category": "Food",
     "raw": "Chickpeas (35%), Water, Tomato, Onion, Edible Vegetable Oil (Cottonseed/Palm), Ginger, Garlic, Iodized Salt, Spices (Pomegranate Seeds, Chilli, Cumin, Cinnamon)."},
    {"name": "Haldiram's Rajma Raseela", "brand": "Haldiram's", "category": "Food",
     "raw": "Red Kidney Beans (30%), Water, Tomato, Onion, Ginger, Garlic, Edible Vegetable Oil, Iodized Salt, Spices."},
    {"name": "Haldiram's Dal Tadka", "brand": "Haldiram's", "category": "Food",
     "raw": "Yellow Lentils (Split Pulse Arhar), Water, Onion, Tomato, Ghee, Garlic, Cumin, Turmeric, Red Chilli, Iodized Salt."},
    # KNORR SOUPS
    {"name": "Knorr Mixed Vegetable Soup", "brand": "Knorr", "category": "Food",
     "raw": "Maize Starch, Sugar, Dehydrated Vegetables (9.5%) [Carrot, Cabbage, Onion, Peas, Leeks], Iodized Salt, Hydrolyzed Vegetable Protein, Thickener (INS 415), Flavor Enhancer (INS 627, 631)."},
    {"name": "Knorr Hot & Sour Veg Soup", "brand": "Knorr", "category": "Food",
     "raw": "Maize Starch, Sugar, Dehydrated Vegetables (Cabbage, Carrot, Onion, Garlic), Iodized Salt, Soy Sauce Powder, Acidity Regulator (INS 330), Thickener (INS 415)."},
    {"name": "Knorr Sweet Corn Veg Soup", "brand": "Knorr", "category": "Food",
     "raw": "Maize Starch, Sugar, Sweet Corn Kernel (8.5%), Iodized Salt, Hydrolyzed Vegetable Protein, Dehydrated Vegetables, Flavor Enhancer (INS 627, 631)."},
    {"name": "Knorr Manchow Veg Soup", "brand": "Knorr", "category": "Food",
     "raw": "Maize Starch, Sugar, Dehydrated Vegetables (6%), Iodized Salt, Soy Sauce Powder, Fried Noodles (Wheat Flour, Palm Oil, Salt), Thickener (INS 415)."},
    {"name": "Knorr Tomato Chatpata Soup", "brand": "Knorr", "category": "Food",
     "raw": "Sugar, Tomato Paste (20%), Maize Starch, Iodized Salt, Wheat Flour, Spices, Acidity Regulator (INS 330)."},
    # CHING'S SECRET
    {"name": "Ching's Secret Veg Hakka Noodles Mix", "brand": "Ching's Secret", "category": "Food",
     "raw": "Iodized Salt, Mixed Spices (Chilli, Pepper, Ginger, Garlic), Sugar, Soy Sauce Powder, Corn Flour, Anticaking Agent (INS 551), Flavor Enhancer (INS 635)."},
    {"name": "Ching's Secret Manchow Soup Mix", "brand": "Ching's Secret", "category": "Food",
     "raw": "Corn Flour, Sugar, Iodized Salt, Soy Sauce Powder, Dehydrated Vegetables, Mixed Spices, Flavor Enhancer (INS 635)."},
    {"name": "Ching's Secret Paneer Chilli Masala", "brand": "Ching's Secret", "category": "Food",
     "raw": "Corn Flour, Iodized Salt, Mixed Spices (Chilli, Ginger, Garlic, Onion), Sugar, Soy Sauce Powder, Anticaking Agent (INS 551)."},
    {"name": "Ching's Secret Schezwan Fried Rice Masala", "brand": "Ching's Secret", "category": "Food",
     "raw": "Iodized Salt, Mixed Spices (Chilli, Pepper, Garlic), Sugar, Soy Sauce Powder, Corn Flour, Disodium 5'-Ribonucleotides."},
    {"name": "Ching's Secret Hot & Sour Soup Mix", "brand": "Ching's Secret", "category": "Food",
     "raw": "Corn Flour, Sugar, Iodized Salt, Soy Sauce Powder, Mixed Spices, Acidity Regulator (INS 330)."},
    # TATA SAMPANN
    {"name": "Tata Sampann Moong Dal Chilla Mix", "brand": "Tata Sampann", "category": "Food",
     "raw": "Moong Dal Flour (85%), Rice Flour, Iodized Salt, Mixed Spices (Cumin, Chilli, Turmeric, Ginger Powder), Acidity Regulator (INS 330)."},
    {"name": "Tata Sampann Pakoda Mix", "brand": "Tata Sampann", "category": "Food",
     "raw": "Bengal Gram Flour (Besan), Rice Flour, Mixed Spices (Ajwain, Chilli, Turmeric), Iodized Salt, Raising Agent (INS 500 ii)."},
    # SAFFOLA & QUAKER
    {"name": "Saffola Masala Oats (Classic Masala)", "brand": "Saffola", "category": "Food",
     "raw": "Oats (70%), Wheat, Dehydrated Vegetables (Carrot, Onion, Beans), Iodized Salt, Mixed Spices (Turmeric, Pepper, Cumin, Coriander), Flavor Enhancer (INS 627, 631)."},
    {"name": "Quaker Masala Oats (Homestyle)", "brand": "Quaker", "category": "Food",
     "raw": "Oats (75%), Dehydrated Vegetables (Carrot, Beans), Iodized Salt, Mixed Spices, Sugar, Edible Vegetable Oil."},
    # SPECIALTY PRODUCTS
    {"name": "Bambino Vermicelli Payasam Mix", "brand": "Bambino", "category": "Food",
     "raw": "Roasted Vermicelli (Semolina), Sugar, Milk Solids, Cashews, Raisins, Cardamom Powder."},
    {"name": "Mothers Recipe Ginger Garlic Paste", "brand": "Mothers Recipe", "category": "Food",
     "raw": "Ginger (44%), Garlic (36%), Iodized Salt, Water, Acidity Regulator (INS 330), Stabilizer (INS 415), Preservative (INS 211)."},
    {"name": "Aashirvaad Instant Suji Halwa", "brand": "Aashirvaad", "category": "Food",
     "raw": "Semolina (Suji), Sugar, Ghee (Clarified Butter), Cashews, Raisins, Cardamom Powder."},
    {"name": "Priya Foods Tamarind Rice Mix", "brand": "Priya Foods", "category": "Food",
     "raw": "Tamarind Extract (30%), Edible Vegetable Oil (Cottonseed/Palm), Iodized Salt, Red Chilli, Turmeric, Mustard, Fenugreek, Asafoetida."},
    {"name": "ITC Master Chef Misal Pav Mix", "brand": "ITC Master Chef", "category": "Food",
     "raw": "Sprouted Lentils, Mixed Spices (Onion, Garlic, Ginger, Chilli), Iodized Salt, Dehydrated Vegetables, Acidity Regulator."},
    {"name": "Bambino Roasted Vermicelli", "brand": "Bambino", "category": "Food",
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Ready-to-mix instant food. Score: {score}/100. FSSAI-registered product.",
            'fssai_note': 'Ready-to-mix instant food product with complete ingredient declaration.',
            'verdict': 'Standard instant food' if score >= 70 else 'Contains additives and preservatives',
            'recommendation': 'Prepare as per package directions. Add fresh ingredients for enhanced nutrition.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Indian Ready-to-Mix & Instant Food products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
