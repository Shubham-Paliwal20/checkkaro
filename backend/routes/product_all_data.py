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

    # HONEY & SPREADS
    "dabur-honey": ("Dabur Honey", "Dabur", "Food", 92, "Pure natural honey", "Pure honey with no additives."),
    "patanjali-honey": ("Patanjali Honey", "Patanjali", "Food", 90, "Pure natural honey", "Pure honey."),
    "kissan-jam": ("Kissan Mixed Fruit Jam", "Kissan", "Food", 52, "Contains preservatives", "Contains sodium benzoate preservative."),
    "nutella": ("Nutella Hazelnut Spread", "Nutella", "Food", 45, "High sugar and palm oil", "High sugar with palm oil."),

    # COOKING OILS
    "fortune-sunflower-oil": ("Fortune Sunflower Oil", "Fortune", "Cooking Oil", 88, "Refined sunflower oil", "Pure refined sunflower oil."),
    "saffola-gold": ("Saffola Gold Oil", "Saffola", "Cooking Oil", 85, "Blended healthy oil", "Rice bran and sunflower oil blend."),
    "dhara-mustard-oil": ("Dhara Mustard Oil", "Dhara", "Cooking Oil", 86, "Pure mustard oil", "Pure refined mustard oil."),
    "fortune-rice-bran": ("Fortune Rice Bran Oil", "Fortune", "Cooking Oil", 84, "Rice bran oil", "Refined rice bran oil."),
    "saffola-tasty": ("Saffola Tasty Oil", "Saffola", "Cooking Oil", 83, "Blended oil", "Corn and soybean oil blend."),
    "patanjali-mustard-oil": ("Patanjali Mustard Oil", "Patanjali", "Cooking Oil", 85, "Pure mustard oil", "Pure mustard oil."),

    # SPICES & MASALAS
    "mdh-chana-masala": ("MDH Chana Masala", "MDH", "Spices", 88, "Natural spice blend", "All natural spices, no additives."),
    "mdh-garam-masala": ("MDH Garam Masala", "MDH", "Spices", 90, "Natural spice blend", "Pure spice blend."),
    "everest-garam-masala": ("Everest Garam Masala", "Everest", "Spices", 90, "Natural spice blend", "Pure spice blend."),
    "everest-chana-masala": ("Everest Chana Masala", "Everest", "Spices", 88, "Natural spice blend", "All natural spices."),
    "catch-turmeric": ("Catch Turmeric Powder", "Catch", "Spices", 95, "Pure turmeric", "100% pure turmeric."),
    "mdh-rajma-masala": ("MDH Rajma Masala", "MDH", "Spices", 88, "Natural spice blend", "All natural spices."),
    "everest-kitchen-king": ("Everest Kitchen King Masala", "Everest", "Spices", 88, "Natural spice blend", "All natural spices."),
    "patanjali-haldi": ("Patanjali Haldi Powder", "Patanjali", "Spices", 95, "Pure turmeric", "100% pure turmeric."),

    # READY TO EAT
    "mtr-paneer-butter-masala": ("MTR Ready to Eat Paneer Butter Masala", "MTR", "Ready to Eat", 62, "Contains preservatives", "Convenient meal with citric acid."),
    "mtr-dal-makhani": ("MTR Ready to Eat Dal Makhani", "MTR", "Ready to Eat", 65, "Contains preservatives", "Lentil dish with preservatives."),
    "mtr-palak-paneer": ("MTR Ready to Eat Palak Paneer", "MTR", "Ready to Eat", 64, "Contains preservatives", "Spinach and paneer dish."),
    "haldiram-ready-to-eat": ("Haldirams Ready to Eat Pav Bhaji", "Haldiram", "Ready to Eat", 60, "Contains preservatives", "Ready meal with preservatives."),

    # FLOUR & GRAINS
    "aashirvaad-atta": ("ITC Aashirvaad Atta", "ITC", "Food", 90, "Whole wheat flour", "100% whole wheat flour."),
    "pillsbury-atta": ("Pillsbury Chakki Fresh Atta", "Pillsbury", "Food", 90, "Whole wheat flour", "100% whole wheat flour."),
    "patanjali-atta": ("Patanjali Atta", "Patanjali", "Food", 90, "Whole wheat flour", "100% whole wheat flour."),
    "aashirvaad-multigrain": ("Aashirvaad Multigrain Atta", "ITC", "Food", 88, "Multigrain flour", "Wheat with multiple grains."),

    # CONDIMENTS & SAUCES
    "maggi-ketchup": ("Maggi Tomato Ketchup", "Maggi", "Condiments", 58, "Contains preservatives", "Contains sodium benzoate."),
    "kissan-ketchup": ("Kissan Fresh Tomato Ketchup", "Kissan", "Condiments", 60, "Contains preservatives", "Contains sodium benzoate."),
    "veeba-mayo": ("Veeba Mayonnaise", "Veeba", "Condiments", 55, "Contains preservatives", "Contains EDTA and potassium sorbate."),
    "dr-oetker-mayo": ("Dr. Oetker FunFoods Mayonnaise", "Dr. Oetker", "Condiments", 55, "Contains preservatives", "Contains EDTA."),
    "maggi-hot-sweet": ("Maggi Hot & Sweet Sauce", "Maggi", "Condiments", 55, "Contains preservatives", "Contains sodium benzoate."),

    # BREAKFAST CEREALS
    "kelloggs-corn-flakes": ("Kelloggs Corn Flakes", "Kelloggs", "Breakfast Cereal", 72, "Fortified cereal", "Corn-based with vitamins."),
    "kelloggs-chocos": ("Kelloggs Chocos", "Kelloggs", "Breakfast Cereal", 58, "Contains sugar", "Chocolate-flavored with high sugar."),
    "kelloggs-muesli": ("Kelloggs Muesli Fruit & Nut", "Kelloggs", "Breakfast Cereal", 75, "Whole grain cereal", "Oats with fruits and nuts."),
    "quaker-oats": ("Quaker Oats", "Quaker", "Breakfast Cereal", 92, "Pure oats", "100% whole grain oats."),
    "bagrry-corn-flakes": ("Bagrry's Corn Flakes", "Bagrry's", "Breakfast Cereal", 72, "Fortified cereal", "Corn-based with vitamins."),
    "saffola-oats": ("Saffola Oats", "Saffola", "Breakfast Cereal", 90, "Pure oats", "100% whole grain oats."),

    # JUICES & DRINKS
    "real-mango": ("Real Fruit Juice Mango", "Real", "Beverages", 55, "Juice from concentrate", "Contains citric acid and pectin."),
    "real-apple": ("Real Fruit Juice Apple", "Real", "Beverages", 58, "Juice from concentrate", "Apple juice with preservatives."),
    "tropicana-orange": ("Tropicana 100% Orange Juice", "Tropicana", "Beverages", 78, "100% juice", "Pure orange juice."),
    "paper-boat-aamras": ("Paper Boat Aamras", "Paper Boat", "Beverages", 72, "Mango pulp drink", "Mango pulp with minimal additives."),
    "paper-boat-jaljeera": ("Paper Boat Jaljeera", "Paper Boat", "Beverages", 75, "Traditional drink", "Traditional spiced drink."),
    "b-natural-mango": ("B Natural Mango Juice", "B Natural", "Beverages", 68, "Fruit juice", "Mango juice with no added color."),

    # ICE CREAMS
    "amul-vanilla": ("Amul Vanilla Ice Cream", "Amul", "Dessert", 65, "Contains stabilizers", "Contains carrageenan and guar gum."),
    "amul-chocolate": ("Amul Chocolate Ice Cream", "Amul", "Dessert", 62, "Contains stabilizers", "Chocolate ice cream with stabilizers."),
    "kwality-walls-cornetto": ("Kwality Walls Cornetto", "Kwality Walls", "Dessert", 55, "Contains stabilizers", "Contains multiple stabilizers."),
    "mother-dairy-kulfi": ("Mother Dairy Kulfi", "Mother Dairy", "Dessert", 72, "Traditional kulfi", "Milk-based with cardamom."),
    "havmor-ice-cream": ("Havmor Vanilla Ice Cream", "Havmor", "Dessert", 65, "Contains stabilizers", "Contains stabilizers."),

    # PICKLES
    "priya-mango-pickle": ("Priya Mango Pickle", "Priya", "Pickles", 72, "Traditional pickle", "Mango with spices and oil."),
    "mothers-recipe-pickle": ("Mother's Recipe Mixed Pickle", "Mother's Recipe", "Pickles", 70, "Traditional pickle", "Mixed vegetables with spices."),
    "patanjali-mango-pickle": ("Patanjali Mango Pickle", "Patanjali", "Pickles", 74, "Natural pickle", "Mango with natural spices."),

    # BAKERY
    "britannia-bread": ("Britannia Bread", "Britannia", "Bakery", 58, "Contains preservatives", "Contains DATEM emulsifier."),
    "modern-bread": ("Modern Bread", "Modern", "Bakery", 56, "Contains preservatives", "Contains calcium propionate."),
    "harvest-gold-bread": ("Harvest Gold Bread", "Harvest Gold", "Bakery", 58, "Contains preservatives", "Contains preservatives."),
    "britannia-whole-wheat-bread": ("Britannia 100% Whole Wheat Bread", "Britannia", "Bakery", 68, "Whole wheat bread", "Whole wheat with fewer additives."),

    # TEA & COFFEE
    "tata-tea-gold": ("Tata Tea Gold", "Tata", "Beverages", 92, "Pure black tea", "100% black tea."),
    "tata-tea-premium": ("Tata Tea Premium", "Tata", "Beverages", 92, "Pure black tea", "100% black tea."),
    "red-label-tea": ("Red Label Natural Care Tea", "Red Label", "Beverages", 90, "Tea with herbs", "Black tea with tulsi and ginger."),
    "nescafe-classic": ("Nescafe Classic Coffee", "Nescafe", "Beverages", 88, "Pure coffee", "100% coffee."),
    "bru-coffee": ("Bru Instant Coffee", "Bru", "Beverages", 85, "Instant coffee", "Coffee with chicory."),
    "tata-coffee": ("Tata Coffee Grand", "Tata", "Beverages", 88, "Pure coffee", "100% coffee."),
    "green-tea-lipton": ("Lipton Green Tea", "Lipton", "Beverages", 92, "Pure green tea", "100% green tea."),

    # FACE WASH & SKINCARE
    "himalaya-face-wash": ("Himalaya Neem Face Wash", "Himalaya", "Personal Care", 68, "Herbal face wash", "Contains neem and turmeric."),
    "garnier-men-face-wash": ("Garnier Men Face Wash", "Garnier", "Personal Care", 62, "Contains SLS", "Contains sodium laureth sulfate."),
    "neutrogena-face-wash": ("Neutrogena Deep Clean Face Wash", "Neutrogena", "Personal Care", 65, "Salicylic acid formula", "Contains salicylic acid."),
    "cetaphil-face-wash": ("Cetaphil Gentle Skin Cleanser", "Cetaphil", "Personal Care", 72, "Gentle cleanser", "Mild formula for sensitive skin."),
    "ponds-face-wash": ("Ponds Pure White Face Wash", "Ponds", "Personal Care", 60, "Contains SLS", "Contains sodium laureth sulfate."),
    "lakme-face-wash": ("Lakme Blush & Glow Face Wash", "Lakme", "Personal Care", 62, "Fruit-based face wash", "Contains fruit extracts."),

    # MOISTURIZERS & CREAMS
    "nivea-cream": ("Nivea Soft Moisturising Cream", "Nivea", "Personal Care", 68, "Standard moisturizer", "Contains mineral oil."),
    "vaseline-lotion": ("Vaseline Intensive Care Lotion", "Vaseline", "Personal Care", 65, "Petroleum-based", "Contains petroleum jelly."),
    "himalaya-moisturizer": ("Himalaya Nourishing Skin Cream", "Himalaya", "Personal Care", 72, "Herbal moisturizer", "Contains aloe vera and winter cherry."),
    "ponds-cold-cream": ("Ponds Cold Cream", "Ponds", "Personal Care", 65, "Classic cold cream", "Traditional cold cream formula."),
    "lakme-sunscreen": ("Lakme Sun Expert SPF 50", "Lakme", "Personal Care", 62, "Sunscreen", "Contains chemical UV filters."),

    # DETERGENTS & HOUSEHOLD
    "surf-excel-matic": ("Surf Excel Matic Detergent", "Surf Excel", "Household", 55, "Contains surfactants", "Anionic surfactants with enzymes."),
    "ariel-matic": ("Ariel Matic Detergent", "Ariel", "Household", 55, "Contains surfactants", "Surfactants with optical brightener."),
    "tide-plus": ("Tide Plus Detergent", "Tide", "Household", 52, "Contains surfactants", "Surfactants with sodium carbonate."),
    "rin-detergent": ("Rin Advanced Detergent", "Rin", "Household", 55, "Contains surfactants", "Standard detergent formula."),
    "wheel-detergent": ("Wheel Active Detergent", "Wheel", "Household", 58, "Contains surfactants", "Budget detergent."),

    # BABY PRODUCTS
    "johnsons-baby-shampoo": ("Johnson's Baby Shampoo", "Johnson's", "Baby Care", 72, "Mild baby formula", "Tear-free formula."),
    "johnsons-baby-lotion": ("Johnson's Baby Lotion", "Johnson's", "Baby Care", 70, "Baby moisturizer", "Gentle formula for babies."),
    "himalaya-baby-soap": ("Himalaya Baby Soap", "Himalaya", "Baby Care", 78, "Gentle herbal soap", "Mild herbal formula for babies."),

    # PROTEIN & NUTRITION
    "ensure-nutrition": ("Ensure Complete Nutrition", "Ensure", "Health Drink", 68, "Complete nutrition", "Fortified nutrition supplement."),
    "whey-protein-muscleblaze": ("MuscleBlaze Whey Protein", "MuscleBlaze", "Nutrition", 72, "Whey protein supplement", "Protein supplement with sweeteners."),
    "sattu-patanjali": ("Patanjali Sattu", "Patanjali", "Food", 92, "Pure roasted gram flour", "100% natural sattu."),

    # SKINCARE - FACE SERUMS & TREATMENTS (Most searched on Nykaa)
    "minimalist-niacinamide": ("Minimalist 10% Niacinamide Face Serum", "Minimalist", "Skincare", 78, "Niacinamide-based serum", "Well-formulated serum with niacinamide and zinc."),
    "minimalist-aha-bha": ("Minimalist AHA 25% + BHA 2% Exfoliant", "Minimalist", "Skincare", 62, "Chemical exfoliant", "Strong acid exfoliant — not for daily use or sensitive skin."),
    "minimalist-vitamin-c": ("Minimalist Vitamin C 10% Face Serum", "Minimalist", "Skincare", 76, "Vitamin C serum", "Stable vitamin C derivative with good efficacy."),
    "minimalist-retinol": ("Minimalist Granactive Retinoid 2%", "Minimalist", "Skincare", 68, "Retinoid serum", "Retinoid — avoid during pregnancy; use SPF."),
    "minimalist-hyaluronic-acid": ("Minimalist Hyaluronic Acid 2% + PGA", "Minimalist", "Skincare", 85, "Hydrating serum", "Excellent hydrator with no concerning ingredients."),
    "wow-vitamin-c": ("Wow Skin Science Vitamin C Serum", "Wow Skin Science", "Skincare", 74, "Vitamin C serum", "Contains vitamin C with hyaluronic acid."),
    "mamaearth-vitamin-c-serum": ("Mamaearth Vitamin C Face Serum", "Mamaearth", "Skincare", 72, "Vitamin C with turmeric", "Contains vitamin C and turmeric extract."),
    "dot-key-vitamin-c": ("Dot & Key Vitamin C + E Serum", "Dot & Key", "Skincare", 74, "Brightening serum", "Vitamin C and E antioxidant serum."),
    "plum-vitamin-c": ("Plum 15% Vitamin C Face Serum", "Plum", "Skincare", 76, "Vitamin C serum", "Stable vitamin C with ferulic acid."),
    "neutrogena-retinol": ("Neutrogena Rapid Wrinkle Repair Retinol Serum", "Neutrogena", "Skincare", 65, "Retinol serum", "Contains retinol — use sunscreen; avoid in pregnancy."),
    "lakme-absolute-serum": ("Lakme Absolute Perfect Radiance Serum", "Lakme", "Skincare", 60, "Brightening serum", "Contains kojic acid and niacinamide."),
    "olay-regenerist-serum": ("Olay Regenerist Micro-Sculpting Serum", "Olay", "Skincare", 65, "Anti-ageing serum", "Contains niacinamide and amino-peptides."),
    "garnier-serum": ("Garnier Bright Complete Vitamin C Booster Serum", "Garnier", "Skincare", 68, "Vitamin C serum", "Contains stable vitamin C derivative."),
    "forest-essentials-serum": ("Forest Essentials Tejus Facial Serum", "Forest Essentials", "Skincare", 80, "Ayurvedic serum", "Contains saffron, sandalwood and rose."),

    # SKINCARE - MOISTURISERS
    "cetaphil-moisturizer": ("Cetaphil Moisturising Cream", "Cetaphil", "Skincare", 75, "Gentle daily moisturizer", "Dermatologist-recommended gentle formula."),
    "neutrogena-water-gel": ("Neutrogena Hydro Boost Water Gel", "Neutrogena", "Skincare", 78, "Hyaluronic acid moisturizer", "Lightweight gel with hyaluronic acid."),
    "olay-total-effects": ("Olay Total Effects 7-in-1 Day Cream", "Olay", "Skincare", 65, "Multi-benefit moisturizer", "Contains niacinamide and vitamin B5."),
    "ponds-age-miracle": ("Pond's Age Miracle Day Cream", "Pond's", "Skincare", 58, "Anti-ageing cream", "Contains retinol — caution during pregnancy."),
    "lakme-peach-milk": ("Lakme Peach Milk Moisturizer", "Lakme", "Skincare", 68, "Lightweight moisturizer", "Peach-based with SPF 24."),
    "mamaearth-ubtan-moisturizer": ("Mamaearth Ubtan Moisturizer", "Mamaearth", "Skincare", 74, "Natural moisturizer", "Contains turmeric and saffron."),
    "himalaya-aloe-vera-gel": ("Himalaya Aloe Vera Gel", "Himalaya", "Skincare", 82, "Aloe vera gel", "Pure aloe vera with minimal additives."),
    "wow-aloe-vera-gel": ("Wow Skin Science Aloe Vera Gel", "Wow Skin Science", "Skincare", 80, "Aloe vera gel", "99% pure aloe vera gel."),
    "plum-e-luminence-moisturizer": ("Plum E-Luminence Simply Supple Moisturizer", "Plum", "Skincare", 76, "Vitamin E moisturizer", "Contains vitamin E and hyaluronic acid."),
    "biotique-morning-nectar": ("Biotique Morning Nectar Moisturizer", "Biotique", "Skincare", 74, "Ayurvedic moisturizer", "Contains honey, neem and basil."),
    "kama-ayurveda-kumkumadi": ("Kama Ayurveda Kumkumadi Miraculous Beauty Fluid", "Kama Ayurveda", "Skincare", 82, "Ayurvedic face oil", "Saffron-based traditional Ayurvedic formulation."),

    # SKINCARE - SUNSCREENS
    "lakme-sun-expert-spf50": ("Lakme Sun Expert SPF 50 PA+++ Sunscreen", "Lakme", "Skincare", 62, "Chemical sunscreen", "Contains avobenzone and octinoxate UV filters."),
    "neutrogena-sunscreen": ("Neutrogena Ultra Sheer Dry Touch SPF 50+", "Neutrogena", "Skincare", 65, "Sunscreen", "Contains homosalate and octisalate."),
    "minimalist-spf50-sunscreen": ("Minimalist SPF 50 PA++++ Sunscreen", "Minimalist", "Skincare", 72, "Broad spectrum sunscreen", "Lightweight mineral-chemical hybrid sunscreen."),
    "dot-key-sunscreen": ("Dot & Key Waterlight SPF 50 Sunscreen", "Dot & Key", "Skincare", 70, "Hybrid sunscreen", "Lightweight with zinc oxide and chemical filters."),
    "re-equil-sunscreen": ("Re'equil Ultra Matte Sunscreen SPF 50", "Re'equil", "Skincare", 72, "Matte sunscreen", "Broad spectrum with zinc oxide."),
    "mamaearth-spf-moisturizer": ("Mamaearth SPF 20 Daily Moisturizer", "Mamaearth", "Skincare", 70, "Moisturizer with SPF", "Contains SPF 20 with aloe vera."),
    "lotus-sunscreen": ("Lotus Herbals Safe Sun SPF 50", "Lotus Herbals", "Skincare", 68, "Herbal sunscreen", "Contains UV filters with herbal extracts."),
    "banana-boat-sunscreen": ("Banana Boat SPF 50 Sunscreen", "Banana Boat", "Skincare", 62, "Chemical sunscreen", "Contains oxybenzone — potential hormone disruptor."),

    # SKINCARE - FACE MASKS & TREATMENTS
    "mamaearth-ubtan-face-mask": ("Mamaearth Ubtan Face Mask", "Mamaearth", "Skincare", 76, "Natural face mask", "Contains turmeric, saffron and kaolin clay."),
    "multani-mitti-vicco": ("Vicco Turmeric Cream", "Vicco", "Skincare", 78, "Ayurvedic turmeric cream", "Contains turmeric extract in a mild base."),
    "plum-clay-mask": ("Plum Green Tea Pore Cleansing Face Mask", "Plum", "Skincare", 74, "Clay mask", "Kaolin clay with green tea antioxidants."),
    "forest-essentials-face-mask": ("Forest Essentials Sandalwood Face Mask", "Forest Essentials", "Skincare", 80, "Ayurvedic face mask", "Contains sandalwood, rosewater and multani mitti."),

    # SKINCARE - TONERS
    "minimalist-pgf-toner": ("Minimalist PGA 3% Pore Minimising Toner", "Minimalist", "Skincare", 76, "Pore-minimising toner", "Contains polyglutamic acid for hydration."),
    "plum-toner": ("Plum Green Tea Alcohol-Free Toner", "Plum", "Skincare", 78, "Alcohol-free toner", "Green tea toner with no alcohol."),
    "mamaearth-toner": ("Mamaearth Skin Illuminate Face Toner", "Mamaearth", "Skincare", 72, "Brightening toner", "Contains vitamin C and turmeric."),
    "biotique-rose-water-toner": ("Biotique Bio Rose Water Toner", "Biotique", "Skincare", 76, "Rose water toner", "Pure rose water with Ayurvedic extracts."),

    # HAIRCARE - CONDITIONERS
    "tresemme-conditioner": ("Tresemme Smooth & Shine Conditioner", "Tresemme", "Hair Care", 62, "Conditioner with silicones", "Contains dimethicone — builds up over time."),
    "loreal-conditioner": ("Loreal Paris Total Repair 5 Conditioner", "Loreal", "Hair Care", 64, "Repair conditioner", "Contains ceramide and arginine."),
    "dove-conditioner": ("Dove Intense Repair Conditioner", "Dove", "Hair Care", 68, "Protein-based conditioner", "Contains keratin actives."),
    "pantene-conditioner": ("Pantene Pro-V Smooth & Silky Conditioner", "Pantene", "Hair Care", 62, "Silicone conditioner", "Contains cyclopentasiloxane — avoid if scalp-sensitive."),
    "himalaya-conditioner": ("Himalaya Anti-Breakage Hair Conditioner", "Himalaya", "Hair Care", 70, "Herbal conditioner", "Contains bhringraj and chickpea."),
    "mamaearth-conditioner": ("Mamaearth Onion Conditioner for Hair Fall", "Mamaearth", "Hair Care", 72, "Onion-based conditioner", "Contains onion extract and plant keratin."),
    "biotique-conditioner": ("Biotique Bio Kelp Fresh Growth Conditioner", "Biotique", "Hair Care", 72, "Ayurvedic conditioner", "Contains seaweed and bhringraj."),
    "wow-onion-conditioner": ("Wow Skin Science Onion & Black Seed Oil Conditioner", "Wow Skin Science", "Hair Care", 74, "Natural conditioner", "Contains onion and black seed oil."),

    # HAIRCARE - HAIR OILS
    "dabur-amla-hair-oil": ("Dabur Amla Hair Oil", "Dabur", "Hair Care", 85, "Amla-based hair oil", "Contains amla (Indian gooseberry) in mineral oil base."),
    "parachute-coconut-oil": ("Parachute Advanced Coconut Hair Oil", "Parachute", "Hair Care", 88, "Pure coconut oil", "100% refined coconut oil."),
    "bajaj-almond-drops": ("Bajaj Almond Drops Hair Oil", "Bajaj", "Hair Care", 80, "Almond hair oil", "Contains almond oil in a light base."),
    "indulekha-hair-oil": ("Indulekha Bringha Hair Oil", "Indulekha", "Hair Care", 82, "Ayurvedic hair oil", "Contains bhringha, amla and neem."),
    "keo-karpin-hair-oil": ("Keo Karpin Hair Oil", "Keo Karpin", "Hair Care", 72, "Blended hair oil", "Contains mineral oil with herbal extracts."),
    "vatika-coconut-hair-oil": ("Vatika Coconut Hair Oil", "Vatika", "Hair Care", 82, "Enriched coconut oil", "Coconut oil with henna and amla."),
    "mamaearth-onion-hair-oil": ("Mamaearth Onion Hair Oil", "Mamaearth", "Hair Care", 78, "Onion-based hair oil", "Contains onion, bhringraj and redensyl."),
    "wow-castor-oil": ("Wow Skin Science Castor Oil", "Wow Skin Science", "Hair Care", 86, "Pure castor oil", "100% pure cold-pressed castor oil."),
    "forest-essentials-hair-oil": ("Forest Essentials Japakusum Hair Oil", "Forest Essentials", "Hair Care", 84, "Ayurvedic hair oil", "Contains hibiscus, brahmi and jasmine."),
    "khadi-hair-oil": ("Khadi Natural Amla & Bhringraj Hair Oil", "Khadi Natural", "Hair Care", 84, "Natural hair oil", "Contains amla, bhringraj in sesame oil base."),

    # HAIRCARE - HAIR MASKS & TREATMENTS
    "mamaearth-hair-mask": ("Mamaearth Argan Hair Mask", "Mamaearth", "Hair Care", 74, "Deep conditioning mask", "Contains argan oil and egg protein."),
    "loreal-hair-mask": ("Loreal Paris Total Repair 5 Hair Mask", "Loreal", "Hair Care", 65, "Repair hair mask", "Contains ceramide and arginine."),
    "wow-hair-mask": ("Wow Skin Science Revitalizing Hair Mask", "Wow Skin Science", "Hair Care", 72, "Protein hair mask", "Contains egg protein and argan oil."),
    "biotique-hair-mask": ("Biotique Bio Bhringraj Therapeutic Hair Pack", "Biotique", "Hair Care", 76, "Ayurvedic hair pack", "Contains bhringraj, amla and brahmi."),

    # COSMETICS - FOUNDATIONS & BB CREAMS
    "lakme-perfecting-bb-cream": ("Lakme 9 to 5 Naturale BB Cream SPF 20", "Lakme", "Cosmetics", 62, "BB cream with SPF", "Contains UV filters and skin-tone pigments."),
    "maybelline-fit-me-foundation": ("Maybelline Fit Me Foundation", "Maybelline", "Cosmetics", 60, "Liquid foundation", "Contains dimethicone and titanium dioxide."),
    "loreal-infallible-foundation": ("Loreal Paris Infallible Foundation", "Loreal", "Cosmetics", 58, "Long-wear foundation", "Contains isododecane and talc."),
    "colorbar-bb-cream": ("Colorbar Radiant White BB Cream", "Colorbar", "Cosmetics", 60, "BB cream with SPF", "Contains titanium dioxide and zinc oxide."),
    "mac-studio-fix": ("MAC Studio Fix Fluid Foundation", "MAC", "Cosmetics", 58, "Full coverage foundation", "Contains talc and synthetic polymers."),
    "nykaa-bb-cream": ("Nykaa Skin Loves Vitamin C BB Cream", "Nykaa Cosmetics", "Cosmetics", 65, "Vitamin C BB cream", "Contains vitamin C and SPF."),

    # COSMETICS - LIP PRODUCTS
    "lakme-lip-color": ("Lakme Enrich Matte Lipstick", "Lakme", "Cosmetics", 62, "Matte lipstick", "Contains castor oil, wax and pigments."),
    "maybelline-lipstick": ("Maybelline Color Sensational Lipstick", "Maybelline", "Cosmetics", 60, "Satin lipstick", "Contains beeswax, castor oil and pigments."),
    "nykaa-lip-gloss": ("Nykaa Matte To Last Lip Gloss", "Nykaa Cosmetics", "Cosmetics", 62, "Matte lip gloss", "Contains vitamin E and castor oil."),
    "mac-lipstick": ("MAC Matte Lipstick", "MAC", "Cosmetics", 60, "Classic matte lipstick", "Contains beeswax and synthetic dyes."),
    "loreal-rouge-signature": ("Loreal Paris Rouge Signature Matte Lip Ink", "Loreal", "Cosmetics", 64, "Matte liquid lipstick", "Contains isododecane and film-forming polymer."),
    "sugar-lip-balm": ("Sugar Cosmetics Tipsy Lips Moisturizing Balm", "Sugar Cosmetics", "Cosmetics", 70, "Tinted lip balm", "Contains shea butter and vitamin E."),

    # COSMETICS - EYE PRODUCTS
    "lakme-kajal": ("Lakme Eyeconic Kajal", "Lakme", "Cosmetics", 60, "Kajal eyeliner", "Contains carbon black and mineral oil."),
    "maybelline-kajal": ("Maybelline Colossal Kajal", "Maybelline", "Cosmetics", 62, "Kajal eyeliner", "Contains carbon black and wax."),
    "loreal-kajal": ("Loreal Paris Kajal Magique", "Loreal", "Cosmetics", 60, "Kajal eyeliner", "Contains mineral pigments and waxes."),
    "lakme-mascara": ("Lakme Absolute Eye Artist Mascara", "Lakme", "Cosmetics", 62, "Volume mascara", "Contains beeswax, iron oxides and silica."),
    "maybelline-colossal-mascara": ("Maybelline Colossal Volume Express Mascara", "Maybelline", "Cosmetics", 60, "Volumizing mascara", "Contains beeswax and coloring agents."),
    "colorbar-kajal": ("Colorbar Soft Touch Kajal", "Colorbar", "Cosmetics", 62, "Soft kajal", "Contains beeswax and pigments."),

    # COSMETICS - FACE POWDER & BLUSH
    "lakme-compact-powder": ("Lakme Radiance Complexion Compact", "Lakme", "Cosmetics", 60, "Compact powder", "Contains talc, mica and titanium dioxide."),
    "maybelline-fit-me-powder": ("Maybelline Fit Me Matte + Poreless Powder", "Maybelline", "Cosmetics", 60, "Setting powder", "Contains talc and silica."),
    "nykaa-blush": ("Nykaa Cosmetix Sky High Blush Palette", "Nykaa Cosmetics", "Cosmetics", 64, "Blush palette", "Contains mica, talc and cosmetic pigments."),
    "loreal-true-match-powder": ("Loreal Paris True Match Powder", "Loreal", "Cosmetics", 62, "Translucent powder", "Contains talc, mica and nylon."),
    "sugar-face-powder": ("Sugar Cosmetics Face Fwd Loose Powder", "Sugar Cosmetics", "Cosmetics", 64, "Setting powder", "Contains tapioca starch and silica."),

    # COSMETICS - NAIL CARE
    "opi-nail-polish": ("OPI Nail Lacquer", "OPI", "Cosmetics", 55, "Nail polish", "Contains formaldehyde resin and dibutyl phthalate."),
    "lakme-nail-polish": ("Lakme Color Crush Nailart", "Lakme", "Cosmetics", 60, "Nail polish", "Standard nail polish formula."),
    "sugar-nail-polish": ("Sugar Cosmetics Nail Polish", "Sugar Cosmetics", "Cosmetics", 62, "Nail polish", "5-free formula without harmful chemicals."),
    "colorbar-nail-polish": ("Colorbar Nail Lacquer", "Colorbar", "Cosmetics", 60, "Nail polish", "Standard nail polish formula."),

    # PERSONAL CARE - DEODORANTS & BODY SPRAYS
    "fogg-deo": ("Fogg Body Spray", "Fogg", "Personal Care", 60, "Body spray", "Contains alcohol and synthetic fragrance."),
    "axe-deo": ("Axe Dark Temptation Deo", "Axe", "Personal Care", 58, "Deodorant", "Contains aluminum salts and synthetic fragrance."),
    "dove-deo": ("Dove Original Antiperspirant Deodorant", "Dove", "Personal Care", 62, "Antiperspirant", "Contains aluminum zirconium tetrachlorohydrex."),
    "fa-deo": ("Fa Fresh Morning Deodorant", "Fa", "Personal Care", 60, "Deodorant", "Contains alcohol and fragrance."),
    "nivea-deo": ("Nivea Men Fresh Active Deo", "Nivea", "Personal Care", 62, "Deodorant", "Contains aluminum chlorohydrate and fragrance."),
    "engage-deo": ("Engage W1 Perfume Body Spray", "Engage", "Personal Care", 62, "Perfume spray", "Contains alcohol, water and fragrance blend."),
    "wild-stone-deo": ("Wild Stone Classic Marble Deo", "Wild Stone", "Personal Care", 60, "Deodorant", "Contains alcohol and synthetic fragrance."),

    # PERSONAL CARE - BODY WASHES
    "dove-body-wash": ("Dove Deeply Nourishing Body Wash", "Dove", "Personal Care", 70, "Mild body wash", "Contains mild surfactants and 1/4 moisturising cream."),
    "fiama-body-wash": ("Fiama Lemongrass Body Wash", "Fiama", "Personal Care", 68, "Gel body wash", "Contains lemongrass extract and moisturisers."),
    "pears-body-wash": ("Pears Pure & Gentle Shower Gel", "Pears", "Personal Care", 72, "Glycerin body wash", "Contains glycerin and no parabens."),
    "himalaya-body-wash": ("Himalaya Soothing Body Wash", "Himalaya", "Personal Care", 72, "Herbal body wash", "Contains aloe vera and milk protein."),
    "johnsons-body-wash": ("Johnson's Vita-Rich Softening Body Wash", "Johnson's", "Personal Care", 72, "Gentle body wash", "Contains natural butter extracts."),
    "mamaearth-body-wash": ("Mamaearth Ubtan Natural Body Wash", "Mamaearth", "Personal Care", 74, "Natural body wash", "Contains turmeric and saffron."),
    "wow-body-wash": ("Wow Skin Science Apple Cider Vinegar Body Wash", "Wow Skin Science", "Personal Care", 72, "ACV body wash", "Contains apple cider vinegar and aloe vera."),

    # PERSONAL CARE - LIP BALMS
    "vaseline-lip-balm": ("Vaseline Lip Therapy Rosy Lips", "Vaseline", "Personal Care", 72, "Petroleum-based lip balm", "Contains petrolatum, shea butter and fragrance."),
    "himalaya-lip-balm": ("Himalaya Herbals Lip Balm Strawberry", "Himalaya", "Personal Care", 76, "Herbal lip balm", "Contains strawberry extract and aloe vera."),
    "biotique-lip-balm": ("Biotique Bio Berry Lip Balm", "Biotique", "Personal Care", 78, "Ayurvedic lip balm", "Contains wheat germ and aloe vera."),
    "mamaearth-lip-balm": ("Mamaearth Vitamin C Lip Balm", "Mamaearth", "Personal Care", 76, "Vitamin C lip balm", "Contains vitamin C, shea butter and beeswax."),
    "plum-lip-balm": ("Plum Chamomile & White Tea Lip Balm", "Plum", "Personal Care", 78, "Natural lip balm", "100% vegan with chamomile and white tea."),
    "carmex-lip-balm": ("Carmex Classic Lip Balm", "Carmex", "Personal Care", 68, "Medicated lip balm", "Contains salicylic acid and camphor."),

    # FOOD - HEALTHY SNACKS & NUTS
    "mccain-fries": ("McCain Smiles Potato Snacks", "McCain", "Snacks", 62, "Processed potato snack", "Contains potato, oil and seasonings."),
    "tata-sampann-poha": ("Tata Sampann Thick Poha", "Tata", "Food", 88, "Whole grain flattened rice", "100% whole grain flattened rice."),
    "happydent-gum": ("Happydent White Xylitol Gum", "Happydent", "Confectionery", 58, "Chewing gum", "Contains xylitol and artificial sweeteners."),
    "milkybar-choclairs": ("Milky Bar Choc Lairs", "Nestle", "Confectionery", 52, "White chocolate toffee", "Contains hydrogenated fat and white chocolate."),
    "sunbites-whole-grain": ("Sunbites Whole Grain Multigrain Crackers", "Sunbites", "Snacks", 72, "Whole grain crackers", "Contains whole wheat and multi-grains."),
    "tiger-biscuits": ("Tiger Kreams Chocolate Biscuits", "Britannia", "Biscuits", 50, "Chocolate sandwich biscuit", "Contains artificial flavors."),

    # FOOD - PACKAGED PULSES & GRAINS
    "tata-dal": ("Tata Sampann Chana Dal", "Tata", "Food", 94, "Pure chana dal", "100% pure Bengal gram split."),
    "tata-moong-dal": ("Tata Sampann Moong Dal", "Tata", "Food", 94, "Pure moong dal", "100% pure green gram split."),
    "fortune-basmati-rice": ("Fortune Biryani Special Basmati Rice", "Fortune", "Food", 92, "Aged basmati rice", "100% aged basmati rice."),
    "india-gate-basmati": ("India Gate Classic Basmati Rice", "India Gate", "Food", 92, "Pure basmati rice", "100% aged basmati rice."),
    "daawat-basmati": ("Daawat Extra Long Basmati Rice", "Daawat", "Food", 92, "Pure basmati rice", "100% extra long grain basmati."),
    "patanjali-besan": ("Patanjali Besan", "Patanjali", "Food", 94, "Pure gram flour", "100% pure chickpea flour."),

    # FOOD - DAIRY ALTERNATIVES
    "silk-soy-milk": ("Silk Soy Milk Unsweetened", "Silk", "Beverages", 82, "Soy-based milk", "Contains soy protein with minimal additives."),
    "epigamia-greek-yogurt": ("Epigamia Greek Yogurt Mango", "Epigamia", "Dairy", 78, "Greek yogurt", "High protein yogurt with fruit."),
    "id-idli-batter": ("iD Fresh Food Idli Batter", "iD Fresh Food", "Food", 88, "Natural idli batter", "Rice and urad dal with no preservatives."),
    "id-dosa-batter": ("iD Fresh Food Dosa Batter", "iD Fresh Food", "Food", 88, "Natural dosa batter", "Rice and urad dal batter."),

    # FOOD - INSTANT MIXES
    "gits-gulab-jamun": ("Gits Gulab Jamun Mix", "Gits", "Food", 65, "Dessert mix", "Contains milk solids, sugar and refined flour."),
    "mtr-rava-idli-mix": ("MTR Rava Idli Mix", "MTR", "Food", 72, "Instant breakfast mix", "Contains semolina and spices."),
    "mtr-upma-mix": ("MTR Upma Mix", "MTR", "Food", 70, "Instant upma mix", "Contains semolina with spices."),
    "mtr-kheer-mix": ("MTR Gulab Jamun Mix", "MTR", "Food", 62, "Dessert mix", "Contains milk solids and refined flour."),
    "eastern-fish-curry-masala": ("Eastern Fish Curry Masala", "Eastern", "Spices", 85, "Fish curry spice blend", "All natural Kerala spices."),
    "catch-red-chilli-powder": ("Catch Red Chilli Powder", "Catch", "Spices", 92, "Pure chilli powder", "100% pure red chilli."),

    # FOOD - SPREADS & BREAKFAST
    "amul-peanut-butter": ("Amul Peanut Butter Crunchy", "Amul", "Food", 82, "Natural peanut butter", "Contains peanuts, sugar and salt only."),
    "sundrop-peanut-butter": ("Sundrop Peanut Butter Creamy", "Sundrop", "Food", 80, "Peanut butter", "Contains peanuts, sugar, hydrogenated vegetable oil and salt."),
    "dr-oetker-peanut-butter": ("Dr. Oetker FunFoods Peanut Butter", "Dr. Oetker", "Food", 78, "Peanut butter", "Contains peanuts, sugar and palm oil."),
    "myfitness-peanut-butter": ("My Fitness Peanut Butter Original Crunchy", "My Fitness", "Food", 88, "Natural peanut butter", "Contains peanuts only — no added sugar or oil."),
    "sleepy-owl-granola": ("Sleepy Owl Granola Honey & Oat", "Sleepy Owl", "Food", 78, "Granola cereal", "Contains oats, honey and nuts."),

    # FOOD - PROTEIN BARS & HEALTH SNACKS
    "rite-bite-protein-bar": ("RiteBite Max Protein Bar", "RiteBite", "Nutrition", 72, "Protein bar", "Contains soy protein, oats and dark chocolate."),
    "onelife-protein-bar": ("Onelife Protein Bar Choco Almond", "Onelife", "Nutrition", 70, "Protein bar", "Contains whey protein and almonds."),
    "yoga-bar-protein": ("Yoga Bar Protein Bar Chocolate Fudge", "Yoga Bar", "Nutrition", 74, "Protein bar", "Contains whey protein, oats and dark chocolate."),
    "true-elements-seeds": ("True Elements Roasted Pumpkin Seeds", "True Elements", "Food", 92, "Roasted seeds snack", "100% natural pumpkin seeds."),
    "farmley-almonds": ("Farmley Premium Almonds", "Farmley", "Food", 96, "Natural almonds", "100% whole almonds, no additives."),
    "happilo-cashews": ("Happilo Premium Whole Cashews", "Happilo", "Food", 96, "Natural cashews", "100% whole cashews."),

    # BEVERAGES - ENERGY DRINKS
    "red-bull": ("Red Bull Energy Drink", "Red Bull", "Energy Drink", 32, "High caffeine energy drink", "High caffeine (80mg/can) with taurine and B-vitamins. Not suitable for children."),
    "monster-energy": ("Monster Energy Original", "Monster", "Energy Drink", 28, "High caffeine energy drink", "Very high caffeine (160mg/can) with B-vitamins and taurine."),
    "sting-energy": ("Sting Energy Drink", "Sting", "Energy Drink", 35, "Caffeine energy drink", "Contains caffeine, taurine and B-vitamins."),
    "hell-energy": ("Hell Energy Drink", "Hell", "Energy Drink", 32, "Caffeine energy drink", "Contains high caffeine and synthetic B-vitamins."),

    # BEVERAGES - HEALTH DRINKS & TEAS
    "tetley-green-tea": ("Tetley Long Leaf Green Tea", "Tetley", "Beverages", 92, "Pure green tea", "100% green tea leaves."),
    "tulsi-green-tea": ("Organic India Tulsi Green Tea", "Organic India", "Beverages", 92, "Tulsi & green tea blend", "Organic tulsi and green tea."),
    "patanjali-honey-lemon-tea": ("Patanjali Honey Lemon Green Tea", "Patanjali", "Beverages", 88, "Herbal green tea", "Green tea with honey and lemon extracts."),
    "vahdam-tea": ("Vahdam Himalayan Green Tea", "Vahdam", "Beverages", 95, "Single-origin green tea", "100% pure first-flush Himalayan green tea."),
    "chaayos-masala-chai": ("Chaayos Instant Masala Chai Mix", "Chaayos", "Beverages", 80, "Masala chai mix", "Contains tea, spices and milk powder."),

    # AYURVEDIC & HEALTH SUPPLEMENTS
    "dabur-chyawanprash": ("Dabur Chyawanprash", "Dabur", "Health Supplement", 82, "Ayurvedic immunity supplement", "Contains amla, ashwagandha and 40+ Ayurvedic herbs."),
    "himalaya-ashwagandha": ("Himalaya Ashwagandha Tablets", "Himalaya", "Health Supplement", 85, "Ayurvedic supplement", "Pure ashwagandha root extract."),
    "patanjali-giloy-juice": ("Patanjali Giloy Juice", "Patanjali", "Health Supplement", 84, "Ayurvedic juice", "Pure giloy extract for immunity."),
    "kapiva-aloe-juice": ("Kapiva Aloe Vera Juice", "Kapiva", "Health Supplement", 82, "Aloe vera juice", "Contains fresh aloe vera pulp."),
    "dabur-amla-juice": ("Dabur Amla Juice", "Dabur", "Health Supplement", 85, "Amla extract juice", "Pure Indian gooseberry extract."),
    "vestige-noni-juice": ("Vestige Noni Juice", "Vestige", "Health Supplement", 78, "Noni fruit juice", "Contains noni fruit extract with natural flavors."),

    # BEVERAGES — CARBONATED & FRUIT DRINKS
    "7up": ("7UP Lemon Lime", "PepsiCo", "Soft Drink", 40, "High sugar, preservative", "High sugar; contains sodium benzoate preservative."),
    "mountain-dew": ("Mountain Dew", "PepsiCo", "Soft Drink", 30, "High sugar, caffeine, artificial color", "Contains tartrazine (E102) — linked to hyperactivity in children. Also has caffeine."),
    "appy-fizz": ("Appy Fizz Apple Drink", "Parle Agro", "Fruit Drink", 42, "Low fruit content, preservatives", "Only 3% apple juice concentrate; contains caramel colour (E150d) and sodium benzoate."),
    "slice-mango": ("Slice Mango Drink", "PepsiCo", "Fruit Drink", 38, "Low fruit content, artificial color", "Only 13% mango pulp; contains sunset yellow (E110) and sodium benzoate."),
    "nimbooz": ("Nimbooz Lemon Drink", "PepsiCo", "Fruit Drink", 45, "Low fruit content", "Only 1.5% lemon juice concentrate; rest is sugar and water with sodium benzoate."),
    "minute-maid-pulpy-orange": ("Minute Maid Pulpy Orange", "Coca-Cola India", "Fruit Drink", 52, "Juice from concentrate with additives", "12% orange juice from concentrate with colour (E160a) and stabilizers."),
    "glucon-d-original": ("Glucon-D Original Energy Drink", "Heinz India", "Health Drink", 48, "High glucose, artificial color", "97.5% dextrose; contains sunset yellow (E110) artificial colour and added vitamins."),
    "nestea-iced-tea-lemon": ("Nestea Lemon Iced Tea", "Nestle", "Beverages", 44, "High sugar, preservative", "Low tea content with sodium benzoate preservative."),
    "gatorade-lemon": ("Gatorade Lemon Electrolyte Drink", "PepsiCo", "Sports Drink", 60, "Electrolyte drink with artificial color", "Contains sodium, potassium electrolytes; tartrazine (E102) artificial colour."),

    # DAIRY — MILK & FRESH
    "amul-gold-full-cream-milk": ("Amul Gold Full Cream Milk", "Amul", "Dairy", 95, "Pure full cream milk", "Standardised to min 6% fat, 9% SNF. Nothing added."),
    "amul-taaza-toned-milk": ("Amul Taaza Toned Milk", "Amul", "Dairy", 95, "Pure toned milk", "Standardised to 3% fat, 8.5% SNF. Nothing added."),
    "amul-kool-chocolate-milk": ("Amul Kool Chocolate Flavoured Milk", "Amul", "Dairy", 62, "Flavoured milk with additives", "Contains carrageenan stabilizer and artificial chocolate flavour."),
    "amul-masti-dahi": ("Amul Masti Dahi", "Amul", "Dairy", 90, "Natural set curd", "Just toned milk and live lactic acid bacteria cultures. No preservatives."),
    "mother-dairy-full-cream-milk": ("Mother Dairy Full Cream Milk", "Mother Dairy", "Dairy", 95, "Pure full cream milk", "Standardised full cream milk. Nothing added."),
    "go-cheese-spread": ("Go Processed Cheese Spread", "Britannia", "Dairy", 62, "Processed cheese with emulsifiers", "Contains sodium citrate emulsifier and nisin preservative."),

    # BISCUITS — ADDITIONAL
    "mcvities-digestive": ("McVitie's Digestive Biscuits", "McVitie's", "Biscuits", 65, "Whole wheat with palm oil", "25% wholemeal wheat; no artificial colours or preservatives."),
    "britannia-jim-jam": ("Britannia Jim Jam Biscuits", "Britannia", "Biscuits", 48, "Contains artificial colour in filling", "Strawberry filling contains azorubine (E122) colour and potassium sorbate."),
    "parle-cheeselings": ("Parle Cheeselings Snack", "Parle", "Biscuits", 52, "Contains artificial flavour and colour", "Artificial cheese flavour; annatto colour (E160b)."),
    "sunfeast-bounce-chocolate": ("Sunfeast Bounce Chocolate Crème", "Sunfeast", "Biscuits", 50, "Contains artificial flavours", "Chocolate cream sandwich biscuit with artificial flavours."),
    "farmlite-oats-digestive": ("Sunfeast Farmlite Oats & Raisin Biscuits", "Sunfeast", "Biscuits", 68, "Oats with natural raisins", "Contains 12% oats and real raisins; no artificial colours."),
    "britannia-little-hearts": ("Britannia Little Hearts Biscuits", "Britannia", "Biscuits", 52, "High sugar, artificial flavour", "Heart-shaped biscuit with high sugar and artificial vanilla flavour."),

    # CHOCOLATES & CONFECTIONERY — ADDITIONAL
    "bounty-bar": ("Bounty Coconut Chocolate Bar", "Mars", "Chocolate", 50, "High sugar, palm oil", "Desiccated coconut in milk chocolate; contains palm oil emulsifiers (E442, E476)."),
    "twix-bar": ("Twix Caramel Cookie Bar", "Mars", "Chocolate", 48, "High sugar, multiple emulsifiers", "Caramel + biscuit in milk chocolate; contains palm oil and emulsifiers E442, E476."),
    "toblerone-milk-chocolate": ("Toblerone Milk Chocolate with Honey & Almond", "Mondelez", "Chocolate", 60, "Milk chocolate with honey", "Contains 3.6% honey and 3% almonds. Soy lecithin emulsifier."),
    "halls-mentho-lyptus": ("Halls Mentho-Lyptus Candy", "Mondelez", "Confectionery", 55, "Sugar candy with eucalyptus", "Contains eucalyptus oil and menthol. High sugar base."),
    "pulse-raw-mango-candy": ("Pass Pass Pulse Raw Mango Candy", "DS Group", "Confectionery", 38, "Artificial colour, high sugar", "Contains tartrazine (E102) and brilliant blue (E133) artificial colours."),
    "center-fresh-spearmint-gum": ("Center Fresh Spearmint Gum", "Perfetti Van Melle", "Confectionery", 42, "Artificial sweeteners, colour", "Contains aspartame (E951), acesulfame K (E950) and tartrazine (E102)."),
    "alpenliebe-caramel-candy": ("Alpenliebe Caramel Candy", "Perfetti Van Melle", "Confectionery", 45, "High sugar, palm oil", "Caramel candy with condensed skim milk and palm oil."),
    "mango-bite-candy": ("Mango Bite Candy", "Perfetti Van Melle", "Confectionery", 40, "Artificial flavour and colour", "Contains artificial mango flavour and sunset yellow (E110)."),

    # HANDWASH & SANITIZERS
    "dettol-original-handwash": ("Dettol Original Antibacterial Handwash", "Reckitt", "Personal Care", 60, "Antibacterial with PCMX", "Contains chloroxylenol (PCMX); MIT/MCIT preservatives linked to contact dermatitis."),
    "lifebuoy-total-handwash": ("Lifebuoy Total 10 Handwash", "HUL", "Personal Care", 55, "Contains triclosan", "Contains triclosan (0.3%) — hormone disruptor, banned in EU wash-off products."),
    "himalaya-purifying-handwash": ("Himalaya Purifying Neem Handwash", "Himalaya", "Personal Care", 65, "Herbal handwash with SLS", "Contains neem and turmeric; uses SLS and paraben preservatives."),
    "savlon-moisturising-handwash": ("Savlon Moisturizing Germ Protection Handwash", "ITC", "Personal Care", 62, "Antibacterial with chlorhexidine", "Contains chlorhexidine gluconate 0.3%; MIT/MCIT preservatives."),

    # ORAL CARE — ADDITIONAL
    "colgate-maxfresh-blue": ("Colgate MaxFresh Blue Gel Toothpaste", "Colgate", "Oral Care", 58, "Gel formula with SLS and cooling crystals", "Contains SLS, sodium fluoride and Blue 1 artificial colour. Cooling crystals are polyethylene microplastics."),
    "colgate-strong-teeth": ("Colgate Strong Teeth Toothpaste", "Colgate", "Oral Care", 60, "Standard fluoride toothpaste", "Contains sodium monofluorophosphate (0.76%); SLS and saccharin sweetener."),
    "dabur-meswak": ("Dabur Meswak Complete Oral Care Toothpaste", "Dabur", "Oral Care", 72, "Herbal toothpaste with Miswak", "Contains Salvadora persica (Miswak) extract; low fluoride formula (1000 ppm)."),

    # SKINCARE — ADDITIONAL
    "glow-and-lovely-face-cream": ("Glow & Lovely Advanced Multivitamin Face Cream", "HUL", "Skincare", 58, "Contains parabens and mineral oil", "Contains methylparaben, propylparaben and liquid paraffin (mineral oil); niacinamide 2%."),
    "ponds-white-beauty-spf15": ("Pond's White Beauty SPF 15 Day Cream", "HUL", "Skincare", 56, "Chemical sunscreen with parabens", "Contains octyl methoxycinnamate UV filter; methylparaben and propylparaben preservatives."),
    "dabur-gulabari-rose-water": ("Dabur Gulabari Premium Rose Water", "Dabur", "Skincare", 82, "Pure rose water toner", "99.5% Rosa damascena flower water. Minimal preservatives (phenoxyethanol, methylparaben)."),
    "the-derma-co-spf50-sunscreen": ("The Derma Co 1% Hyaluronic Sunscreen SPF 50", "The Derma Co", "Skincare", 70, "Hybrid sunscreen with hyaluronic acid", "Contains 1% sodium hyaluronate; avobenzone and zinc oxide UV filters."),
    "lotus-white-glow-cream": ("Lotus Herbals White Glow Skin Whitening Gel Cream SPF 25", "Lotus Herbals", "Skincare", 62, "Whitening cream with chemical UV filters", "Contains kojic acid and mulberry extract; avobenzone UV filter with paraben preservatives."),
    "biotique-coconut-whitening-cream": ("Biotique Bio Coconut Whitening & Brightening Cream", "Biotique", "Skincare", 68, "Ayurvedic brightening cream", "Contains coconut oil, turmeric and saffron. Minimal additives."),
    "pilgrim-vitamin-c-serum": ("Pilgrim 20% Vitamin C Brightening Serum", "Pilgrim", "Skincare", 74, "High-strength Vitamin C serum", "Contains 20% ascorbic acid with ferulic acid stabiliser. Free of parabens and sulphates."),

    # HAIR CARE — ADDITIONAL
    "streax-pro-serum": ("Streax Professional Vitariche Gloss Hair Serum", "Streax", "Hair Care", 65, "Silicone-based hair serum", "Contains cyclopentasiloxane (volatile silicone) and argan oil. Light non-greasy serum."),
    "parachute-advansed-body-lotion": ("Parachute Advansed Deep Nourish Body Lotion", "Marico", "Personal Care", 68, "Coconut oil-based lotion", "Contains coconut oil, glycerin and vitamin E. Paraben preservatives present."),
    "loreal-elvive-extraordinary-oil": ("Loreal Paris Elvive Extraordinary Oil Serum", "Loreal", "Hair Care", 64, "Multi-oil hair serum", "Contains blend of 6 rare flower oils in cyclopentasiloxane base. Dimethicone present."),
    "indulekha-bringha-shampoo": ("Indulekha Bringha Anti Hair Fall Shampoo", "HUL", "Hair Care", 70, "Ayurvedic anti-hairfall shampoo", "Contains bhringraj and light liquid paraffin; free of parabens."),

    # FOOD — SALT, OATS & INSTANT
    "tata-salt-iodized": ("Tata Salt Iodised", "Tata Consumer Products", "Food", 96, "Pure iodized salt", "Sodium chloride with potassium iodate (iodine). Anti-caking agent (E535 - sodium ferrocyanide, max 10 ppm)."),
    "captain-cook-salt": ("Captain Cook Free Flow Iodised Salt", "Tata", "Food", 95, "Iodized salt with anti-caking agent", "Sodium chloride with potassium iodate and silicon dioxide anti-caking agent."),
    "saffola-masala-oats-tomato": ("Saffola Masala Oats Peppy Tomato", "Marico", "Breakfast Cereal", 68, "Oats with flavour enhancer", "62% oats with dried vegetables; contains disodium ribonucleotide (E635) flavour enhancer."),
    "nissin-cup-noodles-masala": ("Nissin Cup Noodles Masala", "Nissin Foods", "Instant Noodles", 38, "Very high sodium, MSG", "Contains MSG (E621), disodium guanylate (E627) and disodium inosinate (E631). Very high salt."),
    "maggi-pazzta-masala": ("Maggi Pazzta Masala Twist Pasta", "Nestle", "Instant Noodles", 45, "Semolina pasta with flavour enhancers", "Contains disodium guanylate (E627) and disodium inosinate (E631); relatively lower sodium than noodles."),
    "aashirvaad-sambhar-masala": ("Aashirvaad Sambhar Masala", "ITC", "Spices", 86, "Natural spice blend", "All natural spices: coriander, cumin, chilli, turmeric, pepper, curry leaves. No artificial additives."),
    "mdh-dal-makhani-masala": ("MDH Dal Makhani Masala", "MDH", "Spices", 88, "Natural spice blend", "Pure blend of natural spices. No artificial colours, flavours or preservatives."),
    "heinz-tomato-ketchup": ("Heinz Tomato Ketchup", "Heinz", "Condiments", 58, "Contains sodium benzoate", "60% tomatoes but also contains sodium benzoate (E211) preservative and high sugar."),
    "amul-mithai-mate": ("Amul Mithai Mate Condensed Milk", "Amul", "Dairy", 55, "Very high sugar", "Condensed whole milk with 45% added sugar. High glycaemic."),
    "britannia-whole-wheat-bread": ("Britannia 100% Whole Wheat Bread", "Britannia", "Bakery", 70, "Whole wheat with preservatives", "100% whole wheat flour; calcium propionate (E282) preservative."),

    # HEALTH SUPPLEMENTS — ADDITIONAL
    "revital-h-multivitamin": ("Revital H Multivitamin & Multimineral Capsules", "Sun Pharma", "Health Supplement", 78, "Ginseng + multivitamin complex", "Contains ginseng extract 42.5 mg with 17 vitamins and minerals. Generally safe for adults."),
    "baidyanath-chyawanprash": ("Baidyanath Special Chyawanprash", "Baidyanath", "Health Supplement", 82, "Traditional Ayurvedic formulation", "Amla 3.6g per 10g serving; 40+ classical herbs with ghee, honey and sesame oil base."),
    "himalaya-triphala": ("Himalaya Triphala Tablets", "Himalaya", "Health Supplement", 88, "Three-fruit Ayurvedic supplement", "Equal parts amla, haritaki and bibhitaki. No synthetic additives."),
    "patanjali-ashwagandha-churna": ("Patanjali Ashwagandha Churna", "Patanjali", "Health Supplement", 90, "Pure ashwagandha root powder", "100% Withania somnifera root powder. No fillers or additives."),
    "himalaya-liv52-syrup": ("Himalaya Liv.52 Syrup", "Himalaya", "Health Supplement", 80, "Liver protective herbal syrup", "Contains caper bush (himsra), chicory, black nightshade, arjuna. Sucrose base."),

    # BABY CARE — ADDITIONAL
    "johnsons-baby-powder": ("Johnson's Baby Powder", "Johnson's", "Baby Care", 55, "Talc-based powder", "Primary ingredient is talc — FDA has raised cancer concerns for talc near genital area."),
    "himalaya-gentle-baby-powder": ("Himalaya Gentle Baby Powder", "Himalaya", "Baby Care", 72, "Herbal baby powder", "Talc base with khus khus and lodhra herbal extracts. Gentler than standard talc powders."),
    "mamaearth-baby-massage-oil": ("Mamaearth Daily Moisturizing Baby Massage Oil", "Mamaearth", "Baby Care", 82, "Natural oil blend for babies", "Blend of sesame, almond, jojoba and chamomile oils. Free of mineral oil and parabens."),
    "himalaya-baby-lotion": ("Himalaya Baby Lotion", "Himalaya", "Baby Care", 75, "Gentle herbal baby lotion", "Contains aloe vera and almond oil. Free of parabens; mild formula for sensitive baby skin."),

    # SNACKS — ADDITIONAL POPULAR
    "haldiram-navrattan-mixture": ("Haldirams Navrattan Mixture", "Haldiram", "Snacks", 68, "Mixed namkeen with natural spices", "Nine-ingredient traditional namkeen with natural spices. Fried in palmolein oil."),
    "bikaji-bhujia": ("Bikaji Bhujia", "Bikaji", "Snacks", 70, "Traditional moth dal bhujia", "Moth bean flour, spices and palmolein oil. No artificial preservatives."),
    "too-yumm-multigrain": ("Too Yumm Multigrain Chilli Chips", "Too Yumm", "Snacks", 72, "Baked multigrain chips", "Lower fat baked chips; contains corn, rice and wheat with natural spices."),
    "mccain-aloo-tikki": ("McCain Aloo Tikki", "McCain", "Snacks", 58, "Processed potato product", "Contains reconstituted potato, starch, onion powder and flavour enhancers."),
    "britannia-cheese-croissant": ("Britannia Cheese Croissant", "Britannia", "Bakery", 48, "Cheese-filled pastry with trans fat risk", "Contains hydrogenated vegetable fat — potential trans fat source. Artificial cheese flavour."),
}


print(f"Total products loaded: {len(ALL_PRODUCTS)}")

