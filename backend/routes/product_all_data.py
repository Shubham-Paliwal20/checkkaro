"""
Complete product database with all 118+ Indian products
This file contains all product data to keep product_new.py clean
"""

# Minimal product data - full ingredients will be loaded from database later
ALL_PRODUCTS = {
    # Format: "key": (name, brand, category, score, verdict, recommendation)
    
    # BISCUITS & COOKIES (15)
    "parle-g": ("Parle-G Gold Biscuits", "Parle", "Biscuits", 55, "Contains preservatives with usage restrictions", "Contains sulphite allergen. High sugar and refined carbs."),
    "britannia-good-day": ("Britannia Good Day Butter Cookies", "Britannia", "Biscuits", 60, "Contains artificial flavors and preservatives", "Contains artificial flavors with usage limits."),
    "britannia-marie": ("Britannia Marie Gold", "Britannia", "Biscuits", 62, "Contains preservatives", "Standard biscuit with preservatives."),
    "parle-monaco": ("Parle Monaco Salted Biscuits", "Parle", "Biscuits", 58, "Contains preservatives", "Salted biscuit with standard ingredients."),
    "britannia-bourbon": ("Britannia Bourbon Chocolate Cream Biscuits", "Britannia", "Biscuits", 52, "Contains artificial flavors", "Chocolate biscuit with artificial flavors."),
    "sunfeast-dark-fantasy": ("Sunfeast Dark Fantasy Choco Fills", "Sunfeast", "Biscuits", 48, "Contains sulphite allergen", "Contains allergen (223). High sugar content."),
    "oreo": ("Oreo Original Cookies", "Oreo", "Biscuits", 50, "Contains artificial flavors", "Popular cookie with artificial flavoring."),
    "parle-hide-seek": ("Parle Hide & Seek Chocolate Chip Cookies", "Parle", "Biscuits", 54, "Contains artificial flavors", "Chocolate chip cookie with artificial flavors."),
    "britannia-nutrichoice": ("Britannia NutriChoice Digestive Biscuits", "Britannia", "Biscuits", 68, "Whole wheat with preservatives", "Better option with whole wheat flour."),
    "sunfeast-moms-magic": ("Sunfeast Mom's Magic Rich Butter Cookies", "Sunfeast", "Biscuits", 58, "Contains artificial flavors", "Butter cookie with artificial flavoring."),
    "parle-krackjack": ("Parle Krackjack Sweet & Salty Biscuits", "Parle", "Biscuits", 60, "Standard ingredients", "Sweet and salty biscuit."),
    "britannia-50-50": ("Britannia 50-50 Maska Chaska", "Britannia", "Biscuits", 56, "Contains artificial flavors", "Popular biscuit with artificial flavors."),
    "sunfeast-glucose": ("Sunfeast Glucose Biscuits", "Sunfeast", "Biscuits", 62, "Standard ingredients", "Basic glucose biscuit."),
    "parle-20-20": ("Parle 20-20 Cookies", "Parle", "Biscuits", 58, "Contains artificial flavors", "Cookie with artificial butter and vanilla flavors."),
    "britannia-treat": ("Britannia Treat Croissant", "Britannia", "Biscuits", 50, "Contains artificial flavors", "Chocolate croissant with artificial flavors."),
    
    # SNACKS & CHIPS (20)
    "lays-classic": ("Lays Classic Salted Chips", "Lays", "Snacks", 85, "Minimal ingredients", "Simple ingredient list with no major concerns."),
    "lays-cream-onion": ("Lays American Style Cream & Onion", "Lays", "Snacks", 65, "Contains flavor enhancers", "Contains MSG-like flavor enhancers."),
    "lays-magic-masala": ("Lays Magic Masala", "Lays", "Snacks", 62, "Contains flavor enhancers", "Contains flavor enhancers and anticaking agent."),
    "kurkure-masala": ("Kurkure Masala Munch", "Kurkure", "Snacks", 50, "Contains flavor enhancers", "Contains MSG-like enhancers."),
    "kurkure-solid": ("Kurkure Solid Masti", "Kurkure", "Snacks", 52, "Contains flavor enhancers", "Contains flavor enhancers."),
    "bingo-mad-angles": ("Bingo Mad Angles", "Bingo", "Snacks", 55, "Contains flavor enhancers", "Contains flavor enhancers."),
    "haldiram-bhujia": ("Haldirams Aloo Bhujia", "Haldiram", "Snacks", 68, "Traditional ingredients", "Traditional namkeen with natural spices."),
    "haldiram-moong-dal": ("Haldirams Moong Dal", "Haldiram", "Snacks", 72, "Natural ingredients", "Simple dal snack with natural spices."),
    "haldiram-sev": ("Haldirams Sev Bhujia", "Haldiram", "Snacks", 70, "Traditional ingredients", "Traditional sev with natural spices."),
    "bikano-bhujia": ("Bikano Bhujia", "Bikano", "Snacks", 68, "Traditional ingredients", "Traditional bhujia with natural spices."),
    "bikano-aloo-lachha": ("Bikano Aloo Lachha", "Bikano", "Snacks", 66, "Traditional ingredients", "Potato-based namkeen."),
    "uncle-chipps": ("Uncle Chipps Spicy Treat", "Uncle Chipps", "Snacks", 60, "Contains flavor enhancers", "Contains flavor enhancers."),
    "pringles": ("Pringles Original", "Pringles", "Snacks", 58, "Processed potato product", "Made from dried potatoes with multiple oils."),
    "balaji-wafers": ("Balaji Wafers Masala Masti", "Balaji", "Snacks", 62, "Contains flavor enhancers", "Contains flavor enhancers."),
    "too-yumm": ("Too Yumm Veggie Stix", "Too Yumm", "Snacks", 75, "Vegetable-based snack", "Healthier snack with vegetable powders."),
    "act-ii-popcorn": ("Act II Popcorn Butter", "Act II", "Snacks", 70, "Popcorn with butter flavor", "Popcorn with artificial butter flavor."),
    "cornitos": ("Cornitos Nacho Crisps", "Cornitos", "Snacks", 78, "Simple ingredients", "Corn-based with minimal ingredients."),
    "doritos": ("Doritos Nacho Cheese", "Doritos", "Snacks", 58, "Contains flavor enhancers", "Cheese-flavored with enhancers."),
    "cheetos": ("Cheetos Flamin Hot", "Cheetos", "Snacks", 45, "Contains artificial color", "Contains Allura Red (E129) artificial color."),
    "bingo-salted": ("Bingo Original Style Salted", "Bingo", "Snacks", 82, "Simple ingredients", "Basic salted chips."),
    
    # INSTANT NOODLES (8)
    "maggi-masala": ("Maggi 2-Minute Masala Noodles", "Maggi", "Instant Noodles", 45, "Contains flavor enhancers", "High sodium with MSG-like enhancers."),
    "maggi-atta": ("Maggi Atta Noodles", "Maggi", "Instant Noodles", 55, "Whole wheat with enhancers", "Better than regular but still has enhancers."),
    "top-ramen": ("Top Ramen Curry Noodles", "Top Ramen", "Instant Noodles", 48, "Contains flavor enhancers", "Contains flavor enhancers."),
    "yippee": ("Yippee Noodles Magic Masala", "Yippee", "Instant Noodles", 50, "Contains flavor enhancers", "Contains flavor enhancers."),
    "sunfeast-yippee-atta": ("Sunfeast YiPPee! Power Up Atta Noodles", "Sunfeast", "Instant Noodles", 58, "Whole wheat option", "Whole wheat noodles."),
    "knorr-soupy": ("Knorr Soupy Noodles", "Knorr", "Instant Noodles", 52, "Contains flavor enhancers", "Soup-based noodles with enhancers."),
    "wai-wai": ("Wai Wai Noodles", "Wai Wai", "Instant Noodles", 48, "Contains flavor enhancers", "Contains flavor enhancers."),
    "patanjali-atta-noodles": ("Patanjali Atta Noodles", "Patanjali", "Instant Noodles", 65, "Whole wheat, fewer additives", "Cleaner ingredient list."),
    
    # CHOCOLATES & CONFECTIONERY (15)
    "cadbury-dairy-milk": ("Cadbury Dairy Milk Chocolate", "Cadbury", "Chocolate", 55, "High sugar content", "Milk chocolate with high sugar."),
    "cadbury-silk": ("Cadbury Dairy Milk Silk", "Cadbury", "Chocolate", 52, "High sugar content", "Premium milk chocolate with high sugar."),
    "kitkat": ("Nestle KitKat", "Nestle", "Chocolate", 54, "Wafer chocolate", "Chocolate-coated wafer."),
    "nestle-munch": ("Nestle Munch", "Nestle", "Chocolate", 56, "Peanut chocolate", "Chocolate with peanuts."),
    "amul-dark-chocolate": ("Amul Dark Chocolate", "Amul", "Chocolate", 72, "Higher cocoa content", "Dark chocolate with 45% cocoa."),
    "amul-milk-chocolate": ("Amul Milk Chocolate", "Amul", "Chocolate", 65, "Milk chocolate", "Standard milk chocolate."),
    "5-star": ("5 Star Chocolate", "5 Star", "Chocolate", 50, "Chocolate with caramel", "Chocolate bar with caramel and peanuts."),
    "perk": ("Perk Chocolate", "Perk", "Chocolate", 52, "Wafer chocolate", "Chocolate-coated wafer."),
    "snickers": ("Snickers Chocolate Bar", "Snickers", "Chocolate", 48, "High sugar and calories", "Chocolate bar with peanuts and caramel."),
    "mars": ("Mars Chocolate Bar", "Mars", "Chocolate", 50, "High sugar content", "Chocolate bar with caramel."),
    "ferrero-rocher": ("Ferrero Rocher", "Ferrero", "Chocolate", 58, "Premium chocolate", "Hazelnut chocolate."),
    "cadbury-bournville": ("Cadbury Bournville Dark Chocolate", "Cadbury", "Chocolate", 75, "Dark chocolate", "Dark chocolate with 50% cocoa."),
    "nestle-milkybar": ("Nestle Milkybar", "Nestle", "Chocolate", 54, "White chocolate", "White chocolate with high sugar."),
    "cadbury-gems": ("Cadbury Gems", "Cadbury", "Chocolate", 42, "Contains artificial colors", "Contains multiple artificial colors."),
    "cadbury-eclairs": ("Cadbury Eclairs", "Cadbury", "Confectionery", 48, "Toffee with chocolate", "Chocolate-flavored toffee."),
    
    # HEALTH DRINKS (10)
    "bournvita": ("Bournvita Health Drink", "Cadbury", "Health Drink", 60, "Fortified with sugar", "Contains sugar as major ingredient."),
    "horlicks": ("Horlicks Original", "Horlicks", "Health Drink", 58, "Fortified malt drink", "Contains sugar with fortification."),
    "complan": ("Complan Nutrition Drink", "Complan", "Health Drink", 62, "Nutrition supplement", "Fortified nutrition drink."),
    "boost": ("Boost Health Drink", "Boost", "Health Drink", 58, "Malt-based drink", "Malt drink with fortification."),
    "pediasure": ("Pediasure Vanilla", "Pediasure", "Health Drink", 68, "Pediatric nutrition", "Specialized nutrition for children."),
    "protinex": ("Protinex Original", "Protinex", "Health Drink", 70, "High protein drink", "Protein-focused nutrition drink."),
    "milo": ("Milo Chocolate Drink", "Milo", "Health Drink", 60, "Chocolate malt drink", "Chocolate-flavored malt drink."),
    "patanjali-nutrela": ("Patanjali Nutrela Badam", "Patanjali", "Health Drink", 75, "Almond-based drink", "Natural almond powder drink."),
    "nestle-ceregrow": ("Nestle Ceregrow", "Nestle", "Health Drink", 65, "Cereal-based nutrition", "Wheat and milk-based drink."),
    "junior-horlicks": ("Junior Horlicks", "Horlicks", "Health Drink", 62, "For children", "Fortified drink for children."),
    
    # BEVERAGES (10)
    "coca-cola": ("Coca Cola", "Coca Cola", "Soft Drink", 35, "High sugar and caffeine", "High sugar content with caffeine."),
    "pepsi": ("Pepsi", "Pepsi", "Soft Drink", 35, "High sugar and caffeine", "High sugar content with caffeine."),
    "thums-up": ("Thums Up", "Thums Up", "Soft Drink", 38, "High sugar and caffeine", "High sugar content with caffeine."),
    "sprite": ("Sprite", "Sprite", "Soft Drink", 42, "High sugar, no caffeine", "Lemon-lime soda with high sugar."),
    "fanta": ("Fanta Orange", "Fanta", "Soft Drink", 38, "Contains artificial color", "Contains Sunset Yellow (E110)."),
    "limca": ("Limca", "Limca", "Soft Drink", 40, "High sugar content", "Lemon-flavored soda."),
    "maaza": ("Maaza Mango Drink", "Maaza", "Fruit Drink", 45, "Low fruit content", "Only 15% mango pulp with artificial color."),
    "frooti": ("Frooti Mango Drink", "Frooti", "Fruit Drink", 48, "Low fruit content", "Only 12% mango pulp."),
    "real-juice": ("Real Fruit Juice Orange", "Real", "Fruit Juice", 55, "Juice from concentrate", "10% juice concentrate with sugar."),
    "tropicana": ("Tropicana 100% Orange Juice", "Tropicana", "Fruit Juice", 75, "100% juice", "Pure orange juice, no added sugar."),
    
    # DAIRY (10)
    "amul-butter": ("Amul Butter", "Amul", "Dairy", 78, "Minimal ingredients", "Just milk fat and salt."),
    "amul-cheese-slices": ("Amul Cheese Slices", "Amul", "Dairy", 68, "Processed cheese", "Contains emulsifiers and preservatives."),
    "amul-cheese-spread": ("Amul Cheese Spread", "Amul", "Dairy", 65, "Processed cheese spread", "Contains emulsifiers."),
    "mother-dairy-dahi": ("Mother Dairy Dahi", "Mother Dairy", "Dairy", 88, "Natural yogurt", "Just milk and culture."),
    "amul-lassi": ("Amul Lassi", "Amul", "Dairy", 75, "Yogurt drink", "Milk, sugar, and culture."),
    "britannia-cheese": ("Britannia Cheese Slices", "Britannia", "Dairy", 68, "Processed cheese", "Contains emulsifiers and preservatives."),
    "nestle-milkmaid": ("Nestle Milkmaid Condensed Milk", "Nestle", "Dairy", 52, "High sugar content", "Milk with high sugar."),
    "amul-paneer": ("Amul Paneer", "Amul", "Dairy", 85, "Fresh cheese", "Just milk and citric acid."),
    "mother-dairy-paneer": ("Mother Dairy Paneer", "Mother Dairy", "Dairy", 85, "Fresh cheese", "Just milk and citric acid."),
    "amul-shrikhand": ("Amul Shrikhand", "Amul", "Dairy", 70, "Sweetened yogurt", "Yogurt with sugar and spices."),
    
    # SOAPS (12)
    "dove-soap": ("Dove Beauty Bar", "Dove", "Personal Care", 65, "Mild surfactant system", "Gentler than traditional soap."),
    "pears-soap": ("Pears Transparent Soap", "Pears", "Personal Care", 72, "Glycerin-based soap", "Transparent soap with glycerin."),
    "lifebuoy-soap": ("Lifebuoy Total 10 Soap", "Lifebuoy", "Personal Care", 68, "Antibacterial soap", "Contains thymol for antibacterial action."),
    "dettol-soap": ("Dettol Original Soap", "Dettol", "Personal Care", 70, "Antibacterial soap", "Contains chloroxylenol."),
    "lux-soap": ("Lux Soft Touch Soap", "Lux", "Personal Care", 66, "Fragrant soap", "Standard soap with fragrance."),
    "santoor-soap": ("Santoor Sandal & Turmeric Soap", "Santoor", "Personal Care", 75, "Herbal soap", "Contains sandalwood and turmeric."),
    "patanjali-neem-soap": ("Patanjali Neem Kanti Soap", "Patanjali", "Personal Care", 78, "Ayurvedic soap", "Natural ingredients with neem."),
    "patanjali-haldi-soap": ("Patanjali Haldi Chandan Soap", "Patanjali", "Personal Care", 76, "Ayurvedic soap", "Turmeric and sandalwood soap."),
    "himalaya-neem-soap": ("Himalaya Neem & Turmeric Soap", "Himalaya", "Personal Care", 74, "Herbal soap", "Neem and turmeric extracts."),
    "medimix-soap": ("Medimix Ayurvedic Soap", "Medimix", "Personal Care", 76, "18 herbs soap", "Traditional Ayurvedic soap."),
    "cinthol-soap": ("Cinthol Original Soap", "Cinthol", "Personal Care", 68, "Refreshing soap", "Standard soap with fragrance."),
    "fiama-gel-bar": ("Fiama Di Wills Gel Bar", "Fiama", "Personal Care", 64, "Gel-based cleanser", "Liquid soap in bar form."),
    
    # SHAMPOOS (10)
    "clinic-plus": ("Clinic Plus Strong & Long Shampoo", "Clinic Plus", "Hair Care", 58, "Contains SLS", "Contains strong surfactants."),
    "pantene-shampoo": ("Pantene Pro-V Shampoo", "Pantene", "Hair Care", 56, "Contains SLS and silicones", "Contains SLS and MIT preservative."),
    "head-shoulders": ("Head & Shoulders Anti-Dandruff Shampoo", "Head & Shoulders", "Hair Care", 62, "Anti-dandruff formula", "Contains zinc pyrithione."),
    "sunsilk": ("Sunsilk Black Shine Shampoo", "Sunsilk", "Hair Care", 58, "Contains SLS", "Contains strong surfactants."),
    "dove-shampoo": ("Dove Hair Fall Rescue Shampoo", "Dove", "Hair Care", 64, "Mild formula", "Milder than most shampoos."),
    "himalaya-shampoo": ("Himalaya Anti-Dandruff Shampoo", "Himalaya", "Hair Care", 68, "Herbal anti-dandruff", "Contains tea tree oil."),
    "patanjali-shampoo": ("Patanjali Kesh Kanti Natural Shampoo", "Patanjali", "Hair Care", 72, "Ayurvedic shampoo", "Contains herbal extracts."),
    "tresemme": ("Tresemme Keratin Smooth Shampoo", "Tresemme", "Hair Care", 60, "Salon-quality formula", "Contains keratin."),
    "loreal-shampoo": ("Loreal Paris Total Repair 5 Shampoo", "Loreal", "Hair Care", 62, "Repair formula", "Contains ceramide."),
    "garnier-shampoo": ("Garnier Fructis Shampoo", "Garnier", "Hair Care", 60, "Fruit-enriched", "Contains fruit extracts."),
    
    # TOOTHPASTE (8)
    "colgate-total": ("Colgate Total Advanced Health", "Colgate", "Oral Care", 55, "Contains triclosan", "Contains triclosan (antibacterial)."),
    "pepsodent": ("Pepsodent Germicheck", "Pepsodent", "Oral Care", 58, "Standard toothpaste", "Contains fluoride."),
    "colgate-visible-white": ("Colgate Visible White", "Colgate", "Oral Care", 56, "Whitening toothpaste", "Contains fluoride."),
    "sensodyne": ("Sensodyne Sensitive Toothpaste", "Sensodyne", "Oral Care", 72, "For sensitive teeth", "Contains potassium nitrate."),
    "patanjali-dant-kanti": ("Patanjali Dant Kanti", "Patanjali", "Oral Care", 75, "Ayurvedic toothpaste", "Contains herbal extracts."),
    "dabur-red": ("Dabur Red Toothpaste", "Dabur", "Oral Care", 74, "Ayurvedic toothpaste", "Contains clove oil."),
    "himalaya-toothpaste": ("Himalaya Complete Care Toothpaste", "Himalaya", "Oral Care", 76, "Herbal toothpaste", "Contains neem and pomegranate."),
    "close-up": ("Close Up Red Hot Toothpaste", "Close Up", "Oral Care", 54, "Gel toothpaste", "Gel formula with artificial color."),
}

print(f"Total products loaded: {len(ALL_PRODUCTS)}")
