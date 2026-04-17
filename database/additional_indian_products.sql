-- Additional Popular Indian Products
-- Add more products to expand the database

-- HONEY & SPREADS
INSERT INTO products_catalog (name, brand, category, ingredients_text, ingredients_list, data_source, is_verified) VALUES
('Dabur Honey', 'Dabur', 'Food', 'Pure Honey', 
ARRAY['Pure Honey'], 'manual', true),

('Kissan Mixed Fruit Jam', 'Kissan', 'Food', 'Sugar, Mixed Fruit Pulp (Apple, Banana, Papaya, Pineapple, Mango, Grape), Acidity Regulator (E330), Gelling Agent (E440), Preservative (E211)', 
ARRAY['Sugar', 'Apple Pulp', 'Banana Pulp', 'Papaya Pulp', 'Pineapple Pulp', 'Mango Pulp', 'Grape Pulp', 'Citric Acid', 'Pectin', 'Sodium Benzoate'], 'manual', true),

('Nutella Hazelnut Spread', 'Nutella', 'Food', 'Sugar, Palm Oil, Hazelnuts (13%), Skimmed Milk Powder (8.7%), Fat-Reduced Cocoa (7.4%), Emulsifier (Soy Lecithin), Vanillin', 
ARRAY['Sugar', 'Palm Oil', 'Hazelnuts', 'Skimmed Milk Powder', 'Cocoa Powder', 'Soy Lecithin', 'Vanillin'], 'manual', true);

-- COOKING OILS
INSERT INTO products_catalog (name, brand, category, ingredients_text, ingredients_list, data_source, is_verified) VALUES
('Fortune Sunflower Oil', 'Fortune', 'Cooking Oil', 'Refined Sunflower Oil', 
ARRAY['Refined Sunflower Oil'], 'manual', true),

('Saffola Gold Oil', 'Saffola', 'Cooking Oil', 'Refined Rice Bran Oil, Refined Sunflower Oil', 
ARRAY['Refined Rice Bran Oil', 'Refined Sunflower Oil'], 'manual', true),

('Dhara Mustard Oil', 'Dhara', 'Cooking Oil', 'Refined Mustard Oil', 
ARRAY['Refined Mustard Oil'], 'manual', true);

-- SPICES & MASALAS
INSERT INTO products_catalog (name, brand, category, ingredients_text, ingredients_list, data_source, is_verified) VALUES
('MDH Chana Masala', 'MDH', 'Spices', 'Coriander, Cumin, Dry Mango, Black Pepper, Red Chilli, Iodised Salt, Black Salt, Dry Ginger, Pomegranate Seeds, Mint Leaves, Carom Seeds, Cloves, Nutmeg, Mace, Green Cardamom, Bay Leaves, Asafoetida', 
ARRAY['Coriander', 'Cumin', 'Dry Mango', 'Black Pepper', 'Red Chilli', 'Iodised Salt', 'Black Salt', 'Dry Ginger', 'Pomegranate Seeds', 'Mint Leaves', 'Carom Seeds', 'Cloves', 'Nutmeg', 'Mace', 'Green Cardamom', 'Bay Leaves', 'Asafoetida'], 'manual', true),

('Everest Garam Masala', 'Everest', 'Spices', 'Coriander, Cumin, Black Pepper, Cassia, Cloves, Cardamom, Mace, Nutmeg, Bay Leaves', 
ARRAY['Coriander', 'Cumin', 'Black Pepper', 'Cassia', 'Cloves', 'Cardamom', 'Mace', 'Nutmeg', 'Bay Leaves'], 'manual', true),

('Catch Turmeric Powder', 'Catch', 'Spices', 'Turmeric', 
ARRAY['Turmeric'], 'manual', true);

-- READY TO EAT
INSERT INTO products_catalog (name, brand, category, ingredients_text, ingredients_list, data_source, is_verified) VALUES
('MTR Ready to Eat Paneer Butter Masala', 'MTR', 'Ready to Eat', 'Water, Paneer (Milk) (15%), Tomato Paste, Onion, Butter (3%), Cashew Paste, Cream (Milk), Sugar, Refined Sunflower Oil, Ginger, Garlic, Salt, Spices, Kasuri Methi, Acidity Regulator (E330)', 
ARRAY['Water', 'Paneer', 'Tomato Paste', 'Onion', 'Butter', 'Cashew Paste', 'Cream', 'Sugar', 'Refined Sunflower Oil', 'Ginger', 'Garlic', 'Salt', 'Spices', 'Kasuri Methi', 'Citric Acid'], 'manual', true),

('ITC Aashirvaad Atta', 'ITC', 'Food', 'Whole Wheat Flour', 
ARRAY['Whole Wheat Flour'], 'manual', true),

('Pillsbury Chakki Fresh Atta', 'Pillsbury', 'Food', 'Whole Wheat Flour', 
ARRAY['Whole Wheat Flour'], 'manual', true);

-- SAUCES & CONDIMENTS
INSERT INTO products_catalog (name, brand, category, ingredients_text, ingredients_list, data_source, is_verified) VALUES
('Maggi Tomato Ketchup', 'Maggi', 'Condiments', 'Tomato Paste, Sugar, Water, Iodised Salt, Acidity Regulator (E260), Spices, Thickener (E1442), Preservative (E211)', 
ARRAY['Tomato Paste', 'Sugar', 'Water', 'Iodised Salt', 'Acetic Acid', 'Spices', 'Modified Starch', 'Sodium Benzoate'], 'manual', true),

('Kissan Fresh Tomato Ketchup', 'Kissan', 'Condiments', 'Tomatoes, Sugar, Salt, Spices, Acidity Regulator (E260), Preservative (E211)', 
ARRAY['Tomatoes', 'Sugar', 'Salt', 'Spices', 'Acetic Acid', 'Sodium Benzoate'], 'manual', true),

('Veeba Mayonnaise', 'Veeba', 'Condiments', 'Refined Soybean Oil, Water, Sugar, Egg Yolk, Iodised Salt, Acidity Regulators (E260, E330), Thickener (E415), Preservative (E202), Antioxidant (E385)', 
ARRAY['Refined Soybean Oil', 'Water', 'Sugar', 'Egg Yolk', 'Iodised Salt', 'Acetic Acid', 'Citric Acid', 'Xanthan Gum', 'Potassium Sorbate', 'Calcium Disodium EDTA'], 'manual', true);

-- BREAKFAST CEREALS
INSERT INTO products_catalog (name, brand, category, ingredients_text, ingredients_list, data_source, is_verified) VALUES
('Kelloggs Corn Flakes', 'Kelloggs', 'Breakfast Cereal', 'Milled Corn, Sugar, Malt Flavouring, Iodised Salt, Vitamins, Minerals', 
ARRAY['Milled Corn', 'Sugar', 'Malt Flavouring', 'Iodised Salt', 'Vitamins', 'Minerals'], 'manual', true),

('Kelloggs Chocos', 'Kelloggs', 'Breakfast Cereal', 'Wheat Flour, Sugar, Cocoa Solids, Edible Vegetable Oil, Iodised Salt, Minerals, Vitamins, Emulsifier (E322)', 
ARRAY['Wheat Flour', 'Sugar', 'Cocoa Solids', 'Edible Vegetable Oil', 'Iodised Salt', 'Minerals', 'Vitamins', 'Soy Lecithin'], 'manual', true),

('Bagrry\'s Corn Flakes', 'Bagrry\'s', 'Breakfast Cereal', 'Corn, Sugar, Malt Extract, Salt', 
ARRAY['Corn', 'Sugar', 'Malt Extract', 'Salt'], 'manual', true);

-- JUICES & DRINKS
INSERT INTO products_catalog (name, brand, category, ingredients_text, ingredients_list, data_source, is_verified) VALUES
('Real Fruit Juice Mango', 'Real', 'Beverages', 'Water, Mango Pulp (20%), Sugar, Acidity Regulator (E330), Antioxidant (E300), Stabilizer (E440), Natural Flavour', 
ARRAY['Water', 'Mango Pulp', 'Sugar', 'Citric Acid', 'Ascorbic Acid', 'Pectin', 'Natural Flavour'], 'manual', true),

('Tropicana 100% Orange Juice', 'Tropicana', 'Beverages', 'Orange Juice (100%)', 
ARRAY['Orange Juice'], 'manual', true),

('Frooti Mango Drink', 'Frooti', 'Beverages', 'Water, Mango Pulp (10%), Sugar, Acidity Regulator (E330), Antioxidant (E300), Stabilizer (E440), Natural Flavour, Colour (E160a)', 
ARRAY['Water', 'Mango Pulp', 'Sugar', 'Citric Acid', 'Ascorbic Acid', 'Pectin', 'Natural Flavour', 'Beta Carotene'], 'manual', true);

-- ICE CREAMS
INSERT INTO products_catalog (name, brand, category, ingredients_text, ingredients_list, data_source, is_verified) VALUES
('Amul Vanilla Ice Cream', 'Amul', 'Dessert', 'Milk, Sugar, Milk Solids, Edible Vegetable Oil, Emulsifier (E471), Stabilizers (E412, E410, E407), Natural Vanilla Flavour', 
ARRAY['Milk', 'Sugar', 'Milk Solids', 'Edible Vegetable Oil', 'Mono and Diglycerides', 'Guar Gum', 'Locust Bean Gum', 'Carrageenan', 'Natural Vanilla Flavour'], 'manual', true),

('Kwality Walls Cornetto', 'Kwality Walls', 'Dessert', 'Milk Solids, Sugar, Edible Vegetable Oil, Glucose Syrup, Cocoa Solids, Emulsifiers (E471, E322), Stabilizers (E412, E410, E407), Flavours', 
ARRAY['Milk Solids', 'Sugar', 'Edible Vegetable Oil', 'Glucose Syrup', 'Cocoa Solids', 'Mono and Diglycerides', 'Soy Lecithin', 'Guar Gum', 'Locust Bean Gum', 'Carrageenan', 'Flavours'], 'manual', true),

('Mother Dairy Kulfi', 'Mother Dairy', 'Dessert', 'Milk, Sugar, Milk Solids, Cardamom, Saffron, Stabilizers (E412, E410)', 
ARRAY['Milk', 'Sugar', 'Milk Solids', 'Cardamom', 'Saffron', 'Guar Gum', 'Locust Bean Gum'], 'manual', true);

-- PICKLES & CHUTNEYS
INSERT INTO products_catalog (name, brand, category, ingredients_text, ingredients_list, data_source, is_verified) VALUES
('Priya Mango Pickle', 'Priya', 'Pickles', 'Mango, Refined Rice Bran Oil, Salt, Red Chilli Powder, Mustard, Fenugreek, Turmeric, Asafoetida, Acidity Regulator (E260)', 
ARRAY['Mango', 'Refined Rice Bran Oil', 'Salt', 'Red Chilli Powder', 'Mustard', 'Fenugreek', 'Turmeric', 'Asafoetida', 'Acetic Acid'], 'manual', true),

('Mother\'s Recipe Mixed Pickle', 'Mother\'s Recipe', 'Pickles', 'Mixed Vegetables (Mango, Lime, Carrot, Chilli), Refined Sunflower Oil, Salt, Spices, Acidity Regulator (E260)', 
ARRAY['Mango', 'Lime', 'Carrot', 'Chilli', 'Refined Sunflower Oil', 'Salt', 'Spices', 'Acetic Acid'], 'manual', true);

-- BAKERY PRODUCTS
INSERT INTO products_catalog (name, brand, category, ingredients_text, ingredients_list, data_source, is_verified) VALUES
('Britannia Bread', 'Britannia', 'Bakery', 'Refined Wheat Flour (Maida), Water, Sugar, Edible Vegetable Oil (Palmolein), Yeast, Iodised Salt, Gluten, Emulsifiers (E471, E472e), Flour Treatment Agent (E300)', 
ARRAY['Refined Wheat Flour', 'Water', 'Sugar', 'Palmolein Oil', 'Yeast', 'Iodised Salt', 'Gluten', 'Mono and Diglycerides', 'DATEM', 'Ascorbic Acid'], 'manual', true),

('Modern Bread', 'Modern', 'Bakery', 'Refined Wheat Flour, Water, Sugar, Edible Vegetable Fat, Yeast, Iodised Salt, Gluten, Emulsifier (E471), Preservative (E282)', 
ARRAY['Refined Wheat Flour', 'Water', 'Sugar', 'Edible Vegetable Fat', 'Yeast', 'Iodised Salt', 'Gluten', 'Mono and Diglycerides', 'Calcium Propionate'], 'manual', true);

-- TEA & COFFEE
INSERT INTO products_catalog (name, brand, category, ingredients_text, ingredients_list, data_source, is_verified) VALUES
('Tata Tea Gold', 'Tata', 'Beverages', 'Black Tea', 
ARRAY['Black Tea'], 'manual', true),

('Nescafe Classic Coffee', 'Nescafe', 'Beverages', 'Coffee', 
ARRAY['Coffee'], 'manual', true),

('Red Label Natural Care Tea', 'Red Label', 'Beverages', 'Black Tea, Tulsi, Ginger, Cardamom, Ashwagandha, Mulethi', 
ARRAY['Black Tea', 'Tulsi', 'Ginger', 'Cardamom', 'Ashwagandha', 'Mulethi'], 'manual', true);

-- PERSONAL CARE - FACE WASH
INSERT INTO products_catalog (name, brand, category, ingredients_text, ingredients_list, data_source, is_verified) VALUES
('Himalaya Neem Face Wash', 'Himalaya', 'Personal Care', 'Water, Sodium Laureth Sulfate, Glycerin, Neem Extract, Turmeric Extract, Cocamidopropyl Betaine, Acrylates Copolymer, Sodium Chloride, Fragrance, Citric Acid, Sodium Benzoate', 
ARRAY['Water', 'Sodium Laureth Sulfate', 'Glycerin', 'Neem Extract', 'Turmeric Extract', 'Cocamidopropyl Betaine', 'Acrylates Copolymer', 'Sodium Chloride', 'Fragrance', 'Citric Acid', 'Sodium Benzoate'], 'manual', true),

('Garnier Men Face Wash', 'Garnier', 'Personal Care', 'Water, Glycerin, Sodium Laureth Sulfate, Coco-Betaine, Sodium Chloride, Charcoal Powder, Salicylic Acid, Citric Acid, Sodium Benzoate, Fragrance', 
ARRAY['Water', 'Glycerin', 'Sodium Laureth Sulfate', 'Coco-Betaine', 'Sodium Chloride', 'Charcoal Powder', 'Salicylic Acid', 'Citric Acid', 'Sodium Benzoate', 'Fragrance'], 'manual', true);

-- DETERGENTS
INSERT INTO products_catalog (name, brand, category, ingredients_text, ingredients_list, data_source, is_verified) VALUES
('Surf Excel Matic Detergent', 'Surf Excel', 'Household', 'Anionic Surfactants, Non-Ionic Surfactants, Soap, Enzymes, Optical Brightener, Perfume, Water', 
ARRAY['Anionic Surfactants', 'Non-Ionic Surfactants', 'Soap', 'Enzymes', 'Optical Brightener', 'Perfume', 'Water'], 'manual', true),

('Ariel Matic Detergent', 'Ariel', 'Household', 'Anionic Surfactants, Non-Ionic Surfactants, Enzymes, Optical Brightener, Perfume, Sodium Carbonate', 
ARRAY['Anionic Surfactants', 'Non-Ionic Surfactants', 'Enzymes', 'Optical Brightener', 'Perfume', 'Sodium Carbonate'], 'manual', true),

('Tide Plus Detergent', 'Tide', 'Household', 'Anionic Surfactants, Non-Ionic Surfactants, Soap, Enzymes, Optical Brightener, Perfume, Sodium Carbonate, Sodium Sulfate', 
ARRAY['Anionic Surfactants', 'Non-Ionic Surfactants', 'Soap', 'Enzymes', 'Optical Brightener', 'Perfume', 'Sodium Carbonate', 'Sodium Sulfate'], 'manual', true);

-- Update search counts
UPDATE products_catalog SET search_count = 80 WHERE name LIKE '%Dabur%' OR name LIKE '%Kissan%' OR name LIKE '%Fortune%';
UPDATE products_catalog SET search_count = 60 WHERE name LIKE '%MDH%' OR name LIKE '%MTR%' OR name LIKE '%Real%';
UPDATE products_catalog SET search_count = 40 WHERE name LIKE '%Kelloggs%' OR name LIKE '%Surf%' OR name LIKE '%Himalaya%';
