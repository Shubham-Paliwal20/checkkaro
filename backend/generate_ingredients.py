"""
Script to generate complete ingredient database from SQL file
"""

import re

# Read the SQL file
with open('../database/indian_products_extended.sql', 'r', encoding='utf-8') as f:
    sql_content = f.read()

# Extract all product entries
pattern = r"\('([^']+)',\s*'([^']+)',\s*'([^']+)',\s*'[^']*',\s*ARRAY\[([^\]]+)\]"
matches = re.findall(pattern, sql_content)

print(f"Found {len(matches)} products")

# Map product names to keys (from product_all_data.py)
name_to_key = {
    "Parle-G Gold Biscuits": "parle-g",
    "Britannia Good Day Butter Cookies": "britannia-good-day",
    "Britannia Marie Gold": "britannia-marie",
    "Parle Monaco Salted Biscuits": "parle-monaco",
    "Britannia Bourbon Chocolate Cream Biscuits": "britannia-bourbon",
    "Sunfeast Dark Fantasy Choco Fills": "sunfeast-dark-fantasy",
    "Oreo Original Cookies": "oreo",
    "Lays Classic Salted Chips": "lays-classic",
    "Lays American Style Cream & Onion": "lays-cream-onion",
    "Lays Magic Masala": "lays-magic-masala",
    "Kurkure Masala Munch": "kurkure-masala",
    "Kurkure Solid Masti": "kurkure-solid",
    "Bingo Mad Angles": "bingo-mad-angles",
    "Haldirams Aloo Bhujia": "haldiram-bhujia",
    "Haldirams Moong Dal": "haldiram-moong-dal",
    "Pringles Original": "pringles",
    "Cheetos Flamin Hot": "cheetos",
    "Maggi 2-Minute Masala Noodles": "maggi-masala",
    "Maggi Atta Noodles": "maggi-atta",
    "Top Ramen Curry Noodles": "top-ramen",
    "Yippee Noodles Magic Masala": "yippee",
    "Cadbury Dairy Milk Chocolate": "cadbury-dairy-milk",
    "Cadbury Dairy Milk Silk": "cadbury-silk",
    "Nestle KitKat": "nestle-kitkat",
    "Cadbury Gems": "cadbury-gems",
    "Bournvita Health Drink": "bournvita",
    "Horlicks Original": "horlicks",
    "Complan Nutrition Drink": "complan",
    "Boost Health Drink": "boost",
    "Milo Chocolate Drink": "milo",
    "Protinex Original": "protinex",
    "Pediasure Vanilla": "pediasure",
    "Coca Cola": "coca-cola",
    "Pepsi": "pepsi",
    "Thums Up": "thums-up",
    "Sprite": "sprite",
    "Fanta Orange": "fanta-orange",
    "Limca": "limca",
    "Maaza Mango Drink": "maaza",
    "Frooti Mango Drink": "frooti",
    "Real Fruit Juice Orange": "real-juice",
    "Tropicana 100% Orange Juice": "tropicana",
    "Amul Butter": "amul-butter",
    "Amul Cheese Slices": "amul-cheese-slices",
    "Mother Dairy Dahi": "mother-dairy-dahi",
    "Nestle Milkmaid Condensed Milk": "nestle-milkmaid",
    "Amul Paneer": "amul-paneer",
    "Dove Beauty Bar": "dove-soap",
    "Pears Transparent Soap": "pears-soap",
    "Lifebuoy Total 10 Soap": "lifebuoy-soap",
    "Dettol Original Soap": "dettol-soap",
    "Lux Soft Touch Soap": "lux-soap",
    "Santoor Sandal & Turmeric Soap": "santoor-soap",
    "Patanjali Neem Kanti Soap": "patanjali-neem-soap",
    "Himalaya Neem & Turmeric Soap": "himalaya-soap",
    "Clinic Plus Strong & Long Shampoo": "clinic-plus",
    "Pantene Pro-V Shampoo": "pantene",
    "Head & Shoulders Anti-Dandruff Shampoo": "head-shoulders",
    "Sunsilk Black Shine Shampoo": "sunsilk",
    "Dove Hair Fall Rescue Shampoo": "dove-shampoo",
    "Colgate Total Advanced Health": "colgate-total",
    "Pepsodent Germicheck": "pepsodent",
    "Colgate Visible White": "colgate-visible-white",
    "Sensodyne Sensitive Toothpaste": "sensodyne",
    "Patanjali Dant Kanti": "patanjali-dant-kanti",
}

# Generate Python code
output = []
for name, brand, category, ingredients_str in matches:
    if name in name_to_key:
        key = name_to_key[name]
        # Parse ingredients
        ingredients = [ing.strip().strip("'") for ing in ingredients_str.split("',")]
        
        output.append(f'    "{key}": [')
        for ing in ingredients:
            if ing:
                output.append(f'        create_ingredient_item("{ing}"),')
        output.append('    ],')
        output.append('')

print("\n".join(output[:50]))  # Print first 50 lines as sample
print(f"\nTotal products processed: {len([m for m in matches if m[0] in name_to_key])}")
