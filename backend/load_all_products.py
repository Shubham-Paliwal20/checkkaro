"""
Script to generate all 118+ products for the sample database
Run this to update product_new.py with all products
"""

# All 118 products from the database
ALL_PRODUCTS_DATA = {
    # BISCUITS (15)
    "parle-g": ("Parle-G Gold Biscuits", "Parle", "Biscuits", 55),
    "britannia-good-day": ("Britannia Good Day Butter Cookies", "Britannia", "Biscuits", 60),
    "britannia-marie": ("Britannia Marie Gold", "Britannia", "Biscuits", 62),
    "parle-monaco": ("Parle Monaco Salted Biscuits", "Parle", "Biscuits", 58),
    "britannia-bourbon": ("Britannia Bourbon Chocolate Cream Biscuits", "Britannia", "Biscuits", 52),
    "sunfeast-dark-fantasy": ("Sunfeast Dark Fantasy Choco Fills", "Sunfeast", "Biscuits", 48),
    "oreo": ("Oreo Original Cookies", "Oreo", "Biscuits", 50),
    "parle-hide-seek": ("Parle Hide & Seek Chocolate Chip Cookies", "Parle", "Biscuits", 54),
    "britannia-nutrichoice": ("Britannia NutriChoice Digestive Biscuits", "Britannia", "Biscuits", 68),
    "sunfeast-moms-magic": ("Sunfeast Mom's Magic Rich Butter Cookies", "Sunfeast", "Biscuits", 58),
    "parle-krackjack": ("Parle Krackjack Sweet & Salty Biscuits", "Parle", "Biscuits", 60),
    "britannia-50-50": ("Britannia 50-50 Maska Chaska", "Britannia", "Biscuits", 56),
    "sunfeast-glucose": ("Sunfeast Glucose Biscuits", "Sunfeast", "Biscuits", 62),
    "parle-20-20": ("Parle 20-20 Cookies", "Parle", "Biscuits", 58),
    "britannia-treat": ("Britannia Treat Croissant", "Britannia", "Biscuits", 50),
    
    # SNACKS (20)
    "lays-classic": ("Lays Classic Salted Chips", "Lays", "Snacks", 85),
    "lays-cream-onion": ("Lays American Style Cream & Onion", "Lays", "Snacks", 65),
    "lays-magic-masala": ("Lays Magic Masala", "Lays", "Snacks", 62),
    "kurkure-masala": ("Kurkure Masala Munch", "Kurkure", "Snacks", 50),
    "kurkure-solid": ("Kurkure Solid Masti", "Kurkure", "Snacks", 52),
    "bingo-mad-angles": ("Bingo Mad Angles", "Bingo", "Snacks", 55),
    "haldiram-bhujia": ("Haldirams Aloo Bhujia", "Haldiram", "Snacks", 68),
    "haldiram-moong-dal": ("Haldirams Moong Dal", "Haldiram", "Snacks", 72),
    "haldiram-sev": ("Haldirams Sev Bhujia", "Haldiram", "Snacks", 70),
    "bikano-bhujia": ("Bikano Bhujia", "Bikano", "Snacks", 68),
    "bikano-aloo-lachha": ("Bikano Aloo Lachha", "Bikano", "Snacks", 66),
    "uncle-chipps": ("Uncle Chipps Spicy Treat", "Uncle Chipps", "Snacks", 60),
    "pringles": ("Pringles Original", "Pringles", "Snacks", 58),
    "balaji-wafers": ("Balaji Wafers Masala Masti", "Balaji", "Snacks", 62),
    "too-yumm": ("Too Yumm Veggie Stix", "Too Yumm", "Snacks", 75),
    "act-ii-popcorn": ("Act II Popcorn Butter", "Act II", "Snacks", 70),
    "cornitos": ("Cornitos Nacho Crisps", "Cornitos", "Snacks", 78),
    "doritos": ("Doritos Nacho Cheese", "Doritos", "Snacks", 58),
    "cheetos": ("Cheetos Flamin Hot", "Cheetos", "Snacks", 45),
    "bingo-salted": ("Bingo Original Style Salted", "Bingo", "Snacks", 82),
    
    # NOODLES (8)
    "maggi-masala": ("Maggi 2-Minute Masala Noodles", "Maggi", "Instant Noodles", 45),
    "maggi-atta": ("Maggi Atta Noodles", "Maggi", "Instant Noodles", 55),
    "top-ramen": ("Top Ramen Curry Noodles", "Top Ramen", "Instant Noodles", 48),
    "yippee": ("Yippee Noodles Magic Masala", "Yippee", "Instant Noodles", 50),
    "sunfeast-yippee-atta": ("Sunfeast YiPPee! Power Up Atta Noodles", "Sunfeast", "Instant Noodles", 58),
    "knorr-soupy": ("Knorr Soupy Noodles", "Knorr", "Instant Noodles", 52),
    "wai-wai": ("Wai Wai Noodles", "Wai Wai", "Instant Noodles", 48),
    "patanjali-atta-noodles": ("Patanjali Atta Noodles", "Patanjali", "Instant Noodles", 65),
    
    # CHOCOLATES (15)
    "cadbury-dairy-milk": ("Cadbury Dairy Milk Chocolate", "Cadbury", "Chocolate", 55),
    "cadbury-silk": ("Cadbury Dairy Milk Silk", "Cadbury", "Chocolate", 52),
    "kitkat": ("Nestle KitKat", "Nestle", "Chocolate", 54),
    "nestle-munch": ("Nestle Munch", "Nestle", "Chocolate", 56),
    "amul-dark-chocolate": ("Amul Dark Chocolate", "Amul", "Chocolate", 72),
    "amul-milk-chocolate": ("Amul Milk Chocolate", "Amul", "Chocolate", 65),
    "5-star": ("5 Star Chocolate", "5 Star", "Chocolate", 50),
    "perk": ("Perk Chocolate", "Perk", "Chocolate", 52),
    "snickers": ("Snickers Chocolate Bar", "Snickers", "Chocolate", 48),
    "mars": ("Mars Chocolate Bar", "Mars", "Chocolate", 50),
    "ferrero-rocher": ("Ferrero Rocher", "Ferrero", "Chocolate", 58),
    "cadbury-bournville": ("Cadbury Bournville Dark Chocolate", "Cadbury", "Chocolate", 75),
    "nestle-milkybar": ("Nestle Milkybar", "Nestle", "Chocolate", 54),
    "cadbury-gems": ("Cadbury Gems", "Cadbury", "Chocolate", 42),
    "cadbury-eclairs": ("Cadbury Eclairs", "Cadbury", "Confectionery", 48),
    
    # HEALTH DRINKS (10)
    "bournvita": ("Bournvita Health Drink", "Cadbury", "Health Drink", 60),
    "horlicks": ("Horlicks Original", "Horlicks", "Health Drink", 58),
    "complan": ("Complan Nutrition Drink", "Complan", "Health Drink", 62),
    "boost": ("Boost Health Drink", "Boost", "Health Drink", 58),
    "pediasure": ("Pediasure Vanilla", "Pediasure", "Health Drink", 68),
    "protinex": ("Protinex Original", "Protinex", "Health Drink", 70),
    "milo": ("Milo Chocolate Drink", "Milo", "Health Drink", 60),
    "patanjali-nutrela": ("Patanjali Nutrela Badam", "Patanjali", "Health Drink", 75),
    "nestle-ceregrow": ("Nestle Ceregrow", "Nestle", "Health Drink", 65),
    "junior-horlicks": ("Junior Horlicks", "Horlicks", "Health Drink", 62),
    
    # BEVERAGES (10)
    "coca-cola": ("Coca Cola", "Coca Cola", "Soft Drink", 35),
    "pepsi": ("Pepsi", "Pepsi", "Soft Drink", 35),
    "thums-up": ("Thums Up", "Thums Up", "Soft Drink", 38),
    "sprite": ("Sprite", "Sprite", "Soft Drink", 42),
    "fanta": ("Fanta Orange", "Fanta", "Soft Drink", 38),
    "limca": ("Limca", "Limca", "Soft Drink", 40),
    "maaza": ("Maaza Mango Drink", "Maaza", "Fruit Drink", 45),
    "frooti": ("Frooti Mango Drink", "Frooti", "Fruit Drink", 48),
    "real-juice": ("Real Fruit Juice Orange", "Real", "Fruit Juice", 55),
    "tropicana": ("Tropicana 100% Orange Juice", "Tropicana", "Fruit Juice", 75),
    
    # DAIRY (10)
    "amul-butter": ("Amul Butter", "Amul", "Dairy", 78),
    "amul-cheese-slices": ("Amul Cheese Slices", "Amul", "Dairy", 68),
    "amul-cheese-spread": ("Amul Cheese Spread", "Amul", "Dairy", 65),
    "mother-dairy-dahi": ("Mother Dairy Dahi", "Mother Dairy", "Dairy", 88),
    "amul-lassi": ("Amul Lassi", "Amul", "Dairy", 75),
    "britannia-cheese": ("Britannia Cheese Slices", "Britannia", "Dairy", 68),
    "nestle-milkmaid": ("Nestle Milkmaid Condensed Milk", "Nestle", "Dairy", 52),
    "amul-paneer": ("Amul Paneer", "Amul", "Dairy", 85),
    "mother-dairy-paneer": ("Mother Dairy Paneer", "Mother Dairy", "Dairy", 85),
    "amul-shrikhand": ("Amul Shrikhand", "Amul", "Dairy", 70),
    
    # SOAPS (12)
    "dove-soap": ("Dove Beauty Bar", "Dove", "Personal Care", 65),
    "pears-soap": ("Pears Transparent Soap", "Pears", "Personal Care", 72),
    "lifebuoy-soap": ("Lifebuoy Total 10 Soap", "Lifebuoy", "Personal Care", 68),
    "dettol-soap": ("Dettol Original Soap", "Dettol", "Personal Care", 70),
    "lux-soap": ("Lux Soft Touch Soap", "Lux", "Personal Care", 66),
    "santoor-soap": ("Santoor Sandal & Turmeric Soap", "Santoor", "Personal Care", 75),
    "patanjali-neem-soap": ("Patanjali Neem Kanti Soap", "Patanjali", "Personal Care", 78),
    "patanjali-haldi-soap": ("Patanjali Haldi Chandan Soap", "Patanjali", "Personal Care", 76),
    "himalaya-neem-soap": ("Himalaya Neem & Turmeric Soap", "Himalaya", "Personal Care", 74),
    "medimix-soap": ("Medimix Ayurvedic Soap", "Medimix", "Personal Care", 76),
    "cinthol-soap": ("Cinthol Original Soap", "Cinthol", "Personal Care", 68),
    "fiama-gel-bar": ("Fiama Di Wills Gel Bar", "Fiama", "Personal Care", 64),
    
    # SHAMPOOS (10)
    "clinic-plus": ("Clinic Plus Strong & Long Shampoo", "Clinic Plus", "Hair Care", 58),
    "pantene-shampoo": ("Pantene Pro-V Shampoo", "Pantene", "Hair Care", 56),
    "head-shoulders": ("Head & Shoulders Anti-Dandruff Shampoo", "Head & Shoulders", "Hair Care", 62),
    "sunsilk": ("Sunsilk Black Shine Shampoo", "Sunsilk", "Hair Care", 58),
    "dove-shampoo": ("Dove Hair Fall Rescue Shampoo", "Dove", "Hair Care", 64),
    "himalaya-shampoo": ("Himalaya Anti-Dandruff Shampoo", "Himalaya", "Hair Care", 68),
    "patanjali-shampoo": ("Patanjali Kesh Kanti Natural Shampoo", "Patanjali", "Hair Care", 72),
    "tresemme": ("Tresemme Keratin Smooth Shampoo", "Tresemme", "Hair Care", 60),
    "loreal-shampoo": ("Loreal Paris Total Repair 5 Shampoo", "Loreal", "Hair Care", 62),
    "garnier-shampoo": ("Garnier Fructis Shampoo", "Garnier", "Hair Care", 60),
    
    # TOOTHPASTE (8)
    "colgate-total": ("Colgate Total Advanced Health", "Colgate", "Oral Care", 55),
    "pepsodent": ("Pepsodent Germicheck", "Pepsodent", "Oral Care", 58),
    "colgate-visible-white": ("Colgate Visible White", "Colgate", "Oral Care", 56),
    "sensodyne": ("Sensodyne Sensitive Toothpaste", "Sensodyne", "Oral Care", 72),
    "patanjali-dant-kanti": ("Patanjali Dant Kanti", "Patanjali", "Oral Care", 75),
    "dabur-red": ("Dabur Red Toothpaste", "Dabur", "Oral Care", 74),
    "himalaya-toothpaste": ("Himalaya Complete Care Toothpaste", "Himalaya", "Oral Care", 76),
    "close-up": ("Close Up Red Hot Toothpaste", "Close Up", "Oral Care", 54),
}

print(f"Total products: {len(ALL_PRODUCTS_DATA)}")
print("\nProduct keys:")
for key in sorted(ALL_PRODUCTS_DATA.keys()):
    name, brand, category, score = ALL_PRODUCTS_DATA[key]
    print(f"  {key}: {name} ({brand}) - Score: {score}")
