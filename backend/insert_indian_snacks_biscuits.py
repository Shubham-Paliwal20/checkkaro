"""
Insert Indian Snacks & Biscuits Registry
100 products spanning biscuits, cookies, chips, and savory snacks
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['palm oil', 'vegetable fat', 'sugar', 'sodium', 'artificial', 'emulsifier', 'color', 'e322', 'e471']
_WORTH = ['coconut', 'nut', 'oat', 'wheat bran', 'cocoa', 'fruit', 'cashew', 'almond', 'whole grain']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'palm' in n: return 'Palm oil; saturated fat base'
        if 'vegetable fat' in n or 'vegetable oil' in n: return 'Vegetable fat; typical in baked products'
        if 'sugar' in n: return 'Sugar content; sweetening base'
        if 'sodium' in n or 'salt' in n: return 'Sodium/salt content; preservative'
        if 'artificial' in n or 'color' in n or 'e' in n: return 'Artificial color/additive; permitted'
        if 'emulsifier' in n or 'e322' in n or 'e471' in n: return 'Emulsifier; texture modifier'
    if cls == 'worth_knowing':
        if 'coconut' in n: return 'Coconut; natural ingredient'
        if 'nut' in n or 'cashew' in n or 'almond' in n: return 'Nuts; protein and healthy fats'
        if 'oat' in n or 'bran' in n: return 'Oats/bran; dietary fiber'
        if 'cocoa' in n: return 'Cocoa; antioxidant-rich'
        if 'fruit' in n: return 'Fruit inclusions; natural flavor'
        if 'whole' in n or 'wheat' in n: return 'Whole grain; nutritional benefit'
    return 'Biscuit/snack ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Processed snack/biscuit with additives; FSSAI approved'
    if cls == 'worth_knowing': return 'Natural inclusions; permitted ingredients'
    return 'Standard snack/biscuit ingredient'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    return [i.strip() for i in raw.split(',') if len(i.strip()) > 2]

def _build_obj(name: str) -> dict:
    cls = _classify(name)
    return {'name': name, 'aliases': '', 'classification': cls, 'one_line_note': _note(name, cls), 'regulatory_note': _reg_note(cls)}

def _score(ingredient_objs: list) -> int:
    score = 100
    for ing in ingredient_objs:
        if ing['classification'] == 'commonly_questioned': score -= 3
        elif ing['classification'] == 'worth_knowing': score -= 1
    return max(0, min(100, score))

PRODUCTS = [
    # BISCUITS & COOKIES
    {"name": "Parle-G", "brand": "Parle", "category": "Biscuit",
     "raw": "Refined Wheat Flour (Maida), Sugar, Edible Vegetable Oil (Palm Oil), Invert Sugar Syrup, Raising Agents [503 (ii), 500 (ii)], Iodized Salt, Milk Solids, Emulsifier [322] and Dough Conditioner [223]."},
    {"name": "Hide & Seek Chocolate Chip", "brand": "Parle", "category": "Cookie",
     "raw": "Wheat Flour, Chocolate Chips (Sugar, Cocoa Mass, Cocoa Butter, Dextrose, Emulsifier (E322), Edible Vegetable Oil, Sugar, Invert Sugar Syrup, Cocoa Solids, Raising Agents (503(ii), 500(ii)), Salt, Emulsifier (E322)."},
    {"name": "KrackJack", "brand": "Parle", "category": "Cracker",
     "raw": "Wheat Flour, Edible Vegetable Oil, Sugar, Raising Agents (503(ii), 500(ii)), Invert Sugar Syrup, Iodized Salt, Yeast, Emulsifier (E322, E471), Dough Conditioner (E223), Lactic Acid."},
    {"name": "Monaco Classic", "brand": "Parle", "category": "Cracker",
     "raw": "Wheat Flour, Edible Vegetable Oil, Sugar, Raising Agents (503(ii), 500(ii)), Invert Sugar Syrup, Iodized Salt (3.1%), Yeast, Emulsifiers (322, 471), Dough Conditioner (223)."},
    {"name": "Magix Orange", "brand": "Parle", "category": "Cookie",
     "raw": "Wheat Flour, Sugar, Edible Vegetable Oil, Invert Sugar Syrup, Raising Agents, Iodized Salt, Emulsifier, Acidity Regulator, Added Flavours (Orange)."},
    {"name": "Marie Gold", "brand": "Britannia", "category": "Biscuit",
     "raw": "Refined Wheat Flour (Maida), Sugar, Refined Palm Oil, Invert Sugar Syrup, Raising Agents [503(ii), 500(ii)], Milk Solids, Iodized Salt, Emulsifiers [322(i), 471, 472e], Flour Treatment Agents [223, 1101(i)]."},
    {"name": "Good Day Cashew", "brand": "Britannia", "category": "Cookie",
     "raw": "Refined Wheat Flour, Sugar, Edible Vegetable Oil, Cashew Nuts (4.5%), Milk Solids, Butter, Iodized Salt, Raising Agents (503(ii), 500(ii)), Emulsifiers (322, 471, 472e)."},
    {"name": "Bourbon", "brand": "Britannia", "category": "Cookie",
     "raw": "Refined Wheat Flour, Sugar (36%), Edible Vegetable Oil, Starch, Cocoa Solids (2.6%), Milk Solids, Raising Agents (503(ii), 500(ii)), Iodized Salt, Emulsifier (322)."},
    {"name": "50-50 Maska Chaska", "brand": "Britannia", "category": "Savory Cracker",
     "raw": "Refined Wheat Flour, Edible Vegetable Oil, Sugar, Raising Agents (503(ii), 500(ii), 450(i)), Invert Sugar Syrup, Butter (1.2%), Iodized Salt, Black Salt, Milk Solids, Dough Conditioner (223)."},
    {"name": "Little Hearts", "brand": "Britannia", "category": "Cookie",
     "raw": "Refined Wheat Flour, Sugar (24%), Edible Vegetable Oil (Palm), Raising Agents (503(ii), 500(ii)), Iodized Salt, Milk Solids, Yeast, Emulsifier (322)."},
    {"name": "Jim Jam", "brand": "Britannia", "category": "Cookie",
     "raw": "Refined Wheat Flour, Sugar (30%), Edible Vegetable Oil, Invert Sugar Syrup, Mixed Fruit Jam (7%) [Sugar, Mixed Fruit Pulp, Thickener (440), Acidity Regulator (330)], Milk Solids, Starch, Iodized Salt, Raising Agents, Emulsifiers."},
    {"name": "NutriChoice Digestive", "brand": "Britannia", "category": "Biscuit",
     "raw": "Refined Wheat Flour (33%), Wheat Bran (16%), Edible Vegetable Oil, Sugar, Whole Wheat Flour (10%), Raising Agents, Iodized Salt, Malt Extract, Emulsifier (322)."},
    {"name": "Nice Time", "brand": "Britannia", "category": "Cookie",
     "raw": "Refined Wheat Flour, Sugar, Edible Vegetable Oil (Palm), Coconut (6%), Raising Agents, Iodized Salt, Emulsifiers."},
    {"name": "Pure Magic Chocolush", "brand": "Britannia", "category": "Cookie",
     "raw": "Wheat Flour, Choco Filling (35%) [Sugar, Edible Vegetable Oil, Cocoa Solids, Cocoa Butter, Emulsifier (322)], Sugar, Edible Vegetable Oil, Cocoa Solids, Raising Agents, Iodized Salt, Emulsifier."},
    {"name": "Tiger Glucose", "brand": "Britannia", "category": "Biscuit",
     "raw": "Refined Wheat Flour, Sugar, Edible Vegetable Oil, Invert Sugar Syrup, Liquid Glucose (1%), Raising Agents, Iodized Salt, Milk Solids, Emulsifiers, Vitamins, Minerals."},
    {"name": "Dark Fantasy Choco Fills", "brand": "Sunfeast", "category": "Cookie",
     "raw": "Choco Filling (35%) [Sugar, Edible Vegetable Oil, Cocoa Solids, Cocoa Butter, Emulsifier (E322), Artificial Flavour (Vanillin)], Wheat Flour, Hydrogenated Vegetable Oil, Sugar, Invert Sugar Syrup, Liquid Glucose, Cocoa Solids, Raising Agents (E503(ii), E500(ii)), Iodized Salt, Emulsifier (E322)."},
    {"name": "Mom's Magic Cashew & Almond", "brand": "Sunfeast", "category": "Cookie",
     "raw": "Wheat Flour, Sugar, Edible Vegetable Oil, Nuts (5%) [Cashew, Almond], Milk Solids, Invert Sugar Syrup, Raising Agents, Iodized Salt, Emulsifiers."},
    {"name": "Bounce Orange Cream", "brand": "Sunfeast", "category": "Cookie",
     "raw": "Wheat Flour, Sugar (35%), Edible Vegetable Oil, Invert Sugar Syrup, Raising Agents, Iodized Salt, Starch, Emulsifiers, Acidity Regulator (330)."},
    {"name": "Marie Light", "brand": "Sunfeast", "category": "Biscuit",
     "raw": "Wheat Flour, Sugar, Edible Vegetable Oil, Invert Sugar Syrup, Raising Agents, Iodized Salt, Milk Solids, Wheat Fiber (0.5%), Flour Treatment Agent (223)."},
    {"name": "Cream Biscuits - Pineapple", "brand": "Sunfeast", "category": "Cookie",
     "raw": "Wheat Flour, Sugar, Edible Vegetable Oil, Starch, Raising Agents, Iodized Salt, Emulsifier, Acidity Regulator."},
    {"name": "Digestive Biscuits", "brand": "McVitie's", "category": "Biscuit",
     "raw": "Wheat Flour (44%), Edible Vegetable Oil (Palm), Whole Wheat Flour (14%), Sugar, Wheat Bran (4%), Invert Sugar Syrup, Raising Agents [500(ii), 503(ii), 450(i)], Iodized Salt, Malt Extract."},
    {"name": "Chocolate Creme", "brand": "Oreo", "category": "Cookie",
     "raw": "Refined Wheat Flour, Sugar, Edible Vegetable Fat, Cocoa Solids (3.3%), Invert Sugar, Raising Agents (500(ii), 503(ii)), Iodized Salt, Emulsifier (322)."},
    {"name": "Vanilla Creme", "brand": "Oreo", "category": "Cookie",
     "raw": "Refined Wheat Flour, Sugar, Edible Vegetable Fat, Invert Sugar, Cocoa Solids, Raising Agents (500(ii), 503(ii)), Iodized Salt, Emulsifier (322)."},
    {"name": "Chocobakes Choco-filled Cookies", "brand": "Cadbury", "category": "Cookie",
     "raw": "Choco Filling (38%) [Sugar, Edible Vegetable Oil, Cocoa Solids, Cocoa Butter, Emulsifier (442, 476)], Wheat Flour, Sugar, Edible Vegetable Fat, Cocoa Solids, Invert Sugar, Raising Agents, Iodized Salt, Emulsifier."},
    {"name": "Fruit & Nut Cookies", "brand": "UniBic", "category": "Cookie",
     "raw": "Wheat Flour, Sugar, Edible Vegetable Oil (Palm), Fruits (10%) [Papaya, Cranberry, Blackcurrant], Nuts (5%) [Cashew, Almond], Liquid Glucose, Raising Agents, Emulsifier (322)."},
    {"name": "Oatmeal Cookies", "brand": "UniBic", "category": "Cookie",
     "raw": "Wheat Flour, Oatmeal (20%), Sugar, Edible Vegetable Oil, Liquid Glucose, Raising Agents, Iodized Salt."},
    {"name": "Dream Lite", "brand": "Anmol", "category": "Biscuit",
     "raw": "Wheat Flour, Edible Vegetable Oil, Sugar, Raising Agents, Iodized Salt, Invert Sugar Syrup, Emulsifier, Dough Conditioner."},
    {"name": "Butter Delite", "brand": "Priyagold", "category": "Biscuit",
     "raw": "Wheat Flour, Sugar, Edible Vegetable Oil, Butter (2%), Milk Solids, Raising Agents, Iodized Salt, Emulsifier."},
    {"name": "Golden Bytes", "brand": "Bector's Cremica", "category": "Cookie",
     "raw": "Wheat Flour, Sugar, Edible Vegetable Oil, Cashew Bits, Milk Solids, Raising Agents, Iodized Salt, Emulsifier."},
    {"name": "Digestive", "brand": "Bector's Cremica", "category": "Biscuit",
     "raw": "Wheat Flour, Whole Wheat Flour, Edible Vegetable Oil, Sugar, Wheat Bran, Raising Agents, Iodized Salt."},
    {"name": "Doodh Biscuit", "brand": "Patanjali", "category": "Biscuit",
     "raw": "Wheat Flour, Sugar, Edible Vegetable Oil, Milk Solids, Iodized Salt, Raising Agents."},
    {"name": "Nariyal Biscuit", "brand": "Patanjali", "category": "Cookie",
     "raw": "Wheat Flour, Sugar, Edible Vegetable Oil, Coconut Powder (10%), Raising Agents, Iodized Salt."},
    {"name": "Biscuits (Horlicks)", "brand": "Horlicks", "category": "Biscuit",
     "raw": "Wheat Flour, Sugar, Edible Vegetable Oil, Malt Extract (2.5%), Milk Solids, Raising Agents, Iodized Salt, Emulsifier, Vitamins, Minerals."},
    {"name": "Biscuits (Bournvita)", "brand": "Bournvita", "category": "Biscuit",
     "raw": "Wheat Flour, Sugar, Edible Vegetable Fat, Malt Extract, Cocoa Solids, Milk Solids, Raising Agents, Iodized Salt, Emulsifier, Vitamins, Minerals."},
    # CHIPS & SAVORY SNACKS
    {"name": "Classic Salted", "brand": "Lay's", "category": "Potato Chips",
     "raw": "Potato, Edible Vegetable Oil (Palmolein, Rice Bran Oil), Iodized Salt."},
    {"name": "Magic Masala", "brand": "Lay's", "category": "Potato Chips",
     "raw": "Potato, Edible Vegetable Oil, Spices & Condiments (Onion Powder, Chilli Powder, Dry Mango Powder, Coriander Powder, Ginger Powder, Garlic Powder, Black Pepper Powder, Turmeric Powder, Cumin Powder), Iodized Salt, Black Salt, Sugar."},
    {"name": "American Style Cream & Onion", "brand": "Lay's", "category": "Potato Chips",
     "raw": "Potato, Edible Vegetable Oil, Sugar, Iodized Salt, Milk Solids, Spices & Condiments (Onion Powder, Parsley), Cheese Powder, Citric Acid (330)."},
    {"name": "Spanish Tomato Tango", "brand": "Lay's", "category": "Potato Chips",
     "raw": "Potato, Edible Vegetable Oil, Sugar, Iodized Salt, Spices & Condiments (Onion Powder, Chilli Powder, Garlic Powder, Clove Powder, Cinnamon Powder), Tomato Powder (0.5%), Acidity Regulators (330, 296)."},
    {"name": "West Indies Hot 'n' Sweet Chilli", "brand": "Lay's", "category": "Potato Chips",
     "raw": "Potato, Edible Vegetable Oil, Sugar, Iodized Salt, Spices & Condiments (Chilli Powder, Garlic Powder), Acidity Regulators."},
    {"name": "India's Magic Masala Maxx", "brand": "Lay's", "category": "Potato Chips",
     "raw": "Potato, Edible Vegetable Oil, Spices & Condiments, Iodized Salt, Sugar, Acidity Regulators."},
    {"name": "Masala Munch", "brand": "Kurkure", "category": "Savory Snacks",
     "raw": "Rice Meal, Edible Vegetable Oil (Palmolein Oil), Corn Meal, Gram Meal, Spices and Condiments (Onion Powder, Chilli Powder, Amchur Powder, Coriander Powder, Garlic Powder, Ginger Powder, Black Pepper Powder, Turmeric Powder, Fenugreek Powder), Iodized Salt, Sugar."},
    {"name": "Green Chutney Style", "brand": "Kurkure", "category": "Savory Snacks",
     "raw": "Rice Meal, Edible Vegetable Oil, Corn Meal, Gram Meal, Spices and Condiments (Chilli Powder, Onion Powder, Coriander Powder, Garlic Powder), Iodized Salt, Sugar, Citric Acid."},
    {"name": "Chilli Chatka", "brand": "Kurkure", "category": "Savory Snacks",
     "raw": "Rice Meal, Edible Vegetable Oil, Corn Meal, Gram Meal, Spices and Condiments, Iodized Salt, Sugar, Acidity Regulators."},
    {"name": "Solid Masti Twisteez", "brand": "Kurkure", "category": "Savory Snacks",
     "raw": "Rice Meal, Edible Vegetable Oil, Corn Meal, Gram Meal, Spices, Iodized Salt, Sugar."},
    {"name": "Mad Angles Achaari Masti", "brand": "Bingo!", "category": "Savory Snacks",
     "raw": "Rice Grits, Edible Vegetable Oil (Palmolein), Corn Grits, Gram Grits, Wheat Flour, Sugar, Iodized Salt, Spices & Condiments (Mango Powder, Chilli Powder, Onion Powder, Garlic Powder, Cumin Powder), Acidity Regulators (330, 296, 334)."},
    {"name": "Potato Chips Salted", "brand": "Bingo!", "category": "Potato Chips",
     "raw": "Potato, Edible Vegetable Oil, Iodized Salt."},
    {"name": "Tedhe Medhe Masala Tadka", "brand": "Bingo!", "category": "Savory Snacks",
     "raw": "Rice Grits, Edible Vegetable Oil, Corn Grits, Gram Grits, Spices & Condiments (Chilli Powder, Onion Powder, Garlic Powder, Coriander Powder, Cumin Powder, Amchur, Ginger Powder, Fenugreek, Black Pepper, Turmeric), Iodized Salt."},
    {"name": "Mad Angles Tomato Madness", "brand": "Bingo!", "category": "Savory Snacks",
     "raw": "Rice Grits, Edible Vegetable Oil, Corn Grits, Gram Grits, Sugar, Iodized Salt, Tomato Powder, Spices & Condiments, Acidity Regulators."},
    {"name": "Aloo Bhujia", "brand": "Haldiram's", "category": "Namkeen",
     "raw": "Potatoes (44%), Edible Vegetable Oil (Palmolein), Gram Pulse Flour (13%), Tepary Beans Flour (5%), Iodized Salt, Spices & Condiments (Chilli Powder, Onion Powder, Garlic Powder, Coriander Powder, Cumin Powder, Amchur, Ginger Powder, Mace, Nutmeg, Cardamom)."},
    {"name": "Bhikari", "brand": "Haldiram's", "category": "Namkeen",
     "raw": "Gram Pulse Flour, Edible Vegetable Oil, Tepary Beans Flour, Iodized Salt, Spices & Condiments."},
    {"name": "Moong Dal", "brand": "Haldiram's", "category": "Namkeen",
     "raw": "Moong Pulse (75%), Edible Vegetable Oil (Palmolein), Iodized Salt."},
    {"name": "Khatta Meetha", "brand": "Haldiram's", "category": "Mixture",
     "raw": "Chickpeas Flour, Edible Vegetable Oil, Rice Flakes, Sugar, Green Peas, Peanuts, Sago, Lentils, Iodized Salt, Spices & Condiments, Citric Acid."},
    {"name": "Navratan Mixture", "brand": "Haldiram's", "category": "Mixture",
     "raw": "Chickpeas Flour, Edible Vegetable Oil, Green Peas, Peanuts, Lentils, Potatoes, Sago, Rice Flakes, Iodized Salt, Spices & Condiments."},
    {"name": "Spicy Treat", "brand": "Uncle Chipps", "category": "Potato Chips",
     "raw": "Potato, Edible Vegetable Oil, Spices & Condiments (Chilli Powder, Onion Powder, Coriander Powder, Garlic Powder, Cumin Powder, Amchur, Turmeric Powder), Iodized Salt."},
    {"name": "Veggie Stix - Cheese Herbs", "brand": "Too Yumm!", "category": "Savory Snacks",
     "raw": "Corn Flour, Rice Flour, Edible Vegetable Oil, Potato Powder, Seasoning (Sugar, Salt, Milk Solids, Cheese Powder, Herbs, Spices)."},
    {"name": "Multigrain Chips", "brand": "Too Yumm!", "category": "Chips",
     "raw": "Corn Flour, Wheat Flour, Rice Flour, Oats Flour, Edible Vegetable Oil, Spices, Iodized Salt."},
    {"name": "Original", "brand": "Pringles", "category": "Potato Chips",
     "raw": "Dried Potatoes, Edible Vegetable Oil (Palm Oil), Corn Flour, Wheat Starch, Emulsifier (E471), Maltodextrin, Iodized Salt, Acidity Regulator (E330)."},
    {"name": "Nacho Cheese", "brand": "Doritos", "category": "Corn Chips",
     "raw": "Corn (70%), Edible Vegetable Oil (Palmolein), Milk Solids, Iodized Salt, Spices & Condiments (Onion Powder, Chilli Powder, Garlic Powder), Cheese Powder (0.5%), Citric Acid."},
    {"name": "Sizzlin' Hot", "brand": "Doritos", "category": "Corn Chips",
     "raw": "Corn, Edible Vegetable Oil, Spices & Condiments, Iodized Salt, Sugar, Acidity Regulators."},
    {"name": "Cheese Puffs", "brand": "Cheetos", "category": "Corn Puffs",
     "raw": "Corn Meal (65%), Edible Vegetable Oil, Cheese Powder, Milk Solids, Iodized Salt, Spices & Condiments."},
    {"name": "Lite Chiwda", "brand": "Haldiram's", "category": "Snack Mix",
     "raw": "Rice Flakes (65%), Edible Vegetable Oil, Gram Flour Flour, Peanuts, Iodized Salt, Spices & Condiments, Turmeric."},
    {"name": "Simply Salted", "brand": "Balaji Wafers", "category": "Potato Chips",
     "raw": "Potato, Edible Vegetable Oil, Iodized Salt."},
    {"name": "Masala Masti", "brand": "Balaji Wafers", "category": "Potato Chips",
     "raw": "Potato, Edible Vegetable Oil, Spices & Condiments, Iodized Salt."},
    {"name": "Chaat Chaska", "brand": "Balaji Wafers", "category": "Potato Chips",
     "raw": "Potato, Edible Vegetable Oil, Spices & Condiments, Iodized Salt, Black Salt, Sugar, Mango Powder."},
    {"name": "Potato Chips Salted", "brand": "Prataap Snacks", "category": "Potato Chips",
     "raw": "Potato, Edible Vegetable Oil, Iodized Salt."},
    {"name": "Curls Masala Munch", "brand": "Yellow Diamond", "category": "Corn Snacks",
     "raw": "Corn Grits, Edible Vegetable Oil, Spices & Condiments, Iodized Salt, Sugar."},
    {"name": "Nacho Crisps Cheese & Herbs", "brand": "Cornitos", "category": "Corn Chips",
     "raw": "Corn (70%), Edible Vegetable Oil (Corn Oil), Milk Solids, Iodized Salt, Cheese Powder, Herbs (Parsley, Oregano), Citric Acid."},
    {"name": "Nacho Crisps Sizzlin Jalapeno", "brand": "Cornitos", "category": "Corn Chips",
     "raw": "Corn, Edible Vegetable Oil, Spices & Condiments (Jalapeno, Onion, Garlic), Iodized Salt, Sugar."},
    {"name": "Nut-Cracker", "brand": "Haldiram's", "category": "Nuts & Legumes",
     "raw": "Peanuts (65%), Chickpeas Flour, Starch, Edible Vegetable Oil, Iodized Salt, Spices & Condiments."},
    {"name": "Murukku", "brand": "Haldiram's", "category": "Savory Snacks",
     "raw": "Rice Flour, Edible Vegetable Oil, Black Gram Flour, Iodized Salt, Sesame Seeds, Spices."},
    {"name": "Chatkeens Namkeen Mix", "brand": "Parle", "category": "Mixture",
     "raw": "Chickpeas Flour, Edible Vegetable Oil, Rice Flakes, Peanuts, Lentils, Iodized Salt, Spices."},
    {"name": "Bikaneri Bhujia", "brand": "Bikaji", "category": "Namkeen",
     "raw": "Dew Bean Flour (Moth Flour), Gram Flour Flour, Edible Vegetable Oil, Iodized Salt, Spices & Condiments."},
    {"name": "Tana Bana", "brand": "Bikaji", "category": "Mixture",
     "raw": "Chickpeas Flour, Edible Vegetable Oil, Peanuts, Rice Flakes, Lentils, Spices, Iodized Salt."},
    {"name": "Papad (Punjabi Masala)", "brand": "Lijjat", "category": "Papad",
     "raw": "Urad Dal Flour, Black Pepper, Iodized Salt, Edible Vegetable Oil, Sodium Bicarbonate, Asafoetida (Hing)."},
    {"name": "Karare - Masala Munch", "brand": "Too Yumm!", "category": "Savory Snacks",
     "raw": "Rice Flour, Corn Flour, Edible Vegetable Oil, Spices & Condiments, Iodized Salt."},
    {"name": "Starters Masti Masala", "brand": "Bingo!", "category": "Savory Snacks",
     "raw": "Rice Grits, Corn Grits, Edible Vegetable Oil, Spices & Condiments, Iodized Salt."},
    {"name": "Butter Popcorn (Instant)", "brand": "Act II", "category": "Popcorn",
     "raw": "Popping Corn, Edible Vegetable Fat, Iodized Salt, Beta Carotene (Colour)."},
    {"name": "Golden Sizzle Popcorn", "brand": "Act II", "category": "Popcorn",
     "raw": "Popping Corn, Edible Vegetable Oil, Iodized Salt."},
    {"name": "Maxx Macho Chilli", "brand": "Lay's", "category": "Potato Chips",
     "raw": "Potato, Edible Vegetable Oil, Sugar, Iodized Salt, Spices & Condiments, Acidity Regulator."},
    {"name": "Puffcorn Yummy Cheese", "brand": "Kurkure", "category": "Corn Puffs",
     "raw": "Corn Meal, Edible Vegetable Oil, Cheese Powder, Milk Solids, Iodized Salt."},
    {"name": "Cream & Onion", "brand": "Balaji Wafers", "category": "Potato Chips",
     "raw": "Potato, Edible Vegetable Oil, Sugar, Iodized Salt, Milk Solids, Onion Powder, Herbs."},
    {"name": "Potato Chips Tomato", "brand": "Bingo!", "category": "Potato Chips",
     "raw": "Potato, Edible Vegetable Oil, Sugar, Tomato Powder, Spices, Iodized Salt."},
    {"name": "Rings Masala", "brand": "Prataap Snacks", "category": "Corn Rings",
     "raw": "Corn Grits, Edible Vegetable Oil, Spices & Condiments, Iodized Salt."},
    {"name": "Plain Boondi", "brand": "Haldiram's", "category": "Savory Snacks",
     "raw": "Chickpeas Flour, Edible Vegetable Oil, Iodized Salt."},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Snack/biscuit product. Score: {score}/100.",
            'fssai_note': 'Processed snack/biscuit; FSSAI approved for commercial sale.',
            'verdict': 'Standard snack product' if score >= 70 else 'Contains refined ingredients and food additives',
            'recommendation': 'Enjoy in moderation as part of a balanced diet.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Indian Snacks & Biscuits products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
