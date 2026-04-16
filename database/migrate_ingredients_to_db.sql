-- Migration Script: Populate ingredient_rules table from hardcoded patterns
-- This script converts the hardcoded ingredient patterns to database entries

-- Clear existing data
TRUNCATE TABLE ingredient_rules CASCADE;

-- COMMONLY QUESTIONED INGREDIENTS (RED CATEGORY)
INSERT INTO ingredient_rules (name, aliases, classification, what_it_is, commonly_found_in, one_line_note, countries_restricted, fssai_position, applies_to) VALUES

-- Preservatives with serious concerns
('Triclosan', ARRAY['5-chloro-2-(2,4-dichlorophenoxy)phenol'], 'commonly_questioned', 'Antibacterial agent banned in EU cosmetics', 'Antibacterial soaps, toothpaste, cosmetics', 'Hormone disruption, antibiotic resistance, thyroid problems', ARRAY['EU (cosmetics)', 'USA (consumer soaps)'], 'Restricted in cosmetics, banned in consumer soaps', 'both'),

('Sodium Benzoate', ARRAY['E211', 'Benzoate of Soda'], 'commonly_questioned', 'Preservative E211', 'Soft drinks, pickles, dried fruits, processed foods', 'Forms benzene (carcinogen) with vitamin C, linked to hyperactivity in children', ARRAY[]::text[], 'Permitted up to 150 ppm with mandatory labeling', 'food'),

('Sodium Metabisulphite', ARRAY['E223', 'Sodium Metabisulfite'], 'commonly_questioned', 'Sulfite preservative E223', 'Wine, dried fruits, processed foods', 'Severe allergic reactions, asthma attacks, can cause anaphylaxis', ARRAY[]::text[], 'Permitted with mandatory allergen labeling', 'food'),

('Sodium Nitrite', ARRAY['E250', 'Nitrous Acid Sodium Salt'], 'commonly_questioned', 'Meat preservative E250', 'Bacon, ham, hot dogs, cured meats', 'Forms nitrosamines (cancer-causing) when cooked at high heat', ARRAY[]::text[], 'Permitted up to 200 ppm in meat products', 'food'),

('Sodium Nitrate', ARRAY['E251', 'Chile Saltpeter'], 'commonly_questioned', 'Meat preservative E251', 'Cured meats, some cheeses', 'Converts to nitrite in body, linked to colorectal cancer', ARRAY[]::text[], 'Permitted in meat products with concentration limits', 'food'),

('Sulfur Dioxide', ARRAY['E220', 'SO2'], 'commonly_questioned', 'Preservative E220', 'Dried fruits, wine, processed potatoes', 'Destroys vitamin B1, triggers severe asthma, allergic reactions', ARRAY[]::text[], 'Permitted with mandatory labeling, restricted in thiamine-rich foods', 'food'),

('Methylparaben', ARRAY['E218', 'Methyl p-hydroxybenzoate'], 'commonly_questioned', 'Paraben preservative E218', 'Cosmetics, pharmaceuticals, some foods', 'Mimics estrogen, hormone disruption, accumulates in breast tissue', ARRAY['Denmark (children products)', 'EU (restricted)'], 'Permitted in foods up to 250 ppm, under review', 'both'),

('Propylparaben', ARRAY['E216', 'Propyl p-hydroxybenzoate'], 'commonly_questioned', 'Paraben preservative E216', 'Cosmetics, baked goods, soft drinks', 'Endocrine disruptor, linked to reduced sperm count, reproductive harm', ARRAY['EU (children products)', 'Denmark'], 'Permitted up to 250 ppm, under regulatory review', 'both'),

('Butylparaben', ARRAY['E214', 'Butyl p-hydroxybenzoate'], 'commonly_questioned', 'Paraben preservative E214', 'Personal care products, some processed foods', 'Strongest hormone disruptor, bioaccumulation, reproductive toxicity', ARRAY['EU (restricted)', 'Japan (restricted)'], 'Not commonly used in foods, restricted in cosmetics', 'both'),

-- Artificial colors with serious concerns
('Tartrazine', ARRAY['E102', 'Yellow 5', 'FD&C Yellow No. 5'], 'commonly_questioned', 'Yellow artificial color E102', 'Candies, soft drinks, desserts, processed foods', 'Hyperactivity & ADHD in children, asthma attacks, requires EU warning label', ARRAY[]::text[], 'Permitted with mandatory warning label about hyperactivity', 'food'),

('Sunset Yellow', ARRAY['E110', 'Yellow 6', 'Orange Yellow S'], 'commonly_questioned', 'Orange artificial color E110', 'Candies, soft drinks, desserts, processed foods', 'Hyperactivity in children, allergic reactions, banned in Norway & Finland', ARRAY['Norway', 'Finland'], 'Permitted with mandatory warning label', 'food'),

('Allura Red', ARRAY['E129', 'Red 40', 'FD&C Red No. 40'], 'commonly_questioned', 'Red artificial color E129', 'Candies, soft drinks, desserts, processed foods', 'Hyperactivity, immune system tumors in mice, allergic reactions', ARRAY[]::text[], 'Permitted with mandatory warning label about hyperactivity', 'food'),

('Ponceau 4R', ARRAY['E124', 'Cochineal Red A'], 'commonly_questioned', 'Red artificial color E124', 'Candies, desserts, processed foods', 'Banned in USA/Norway/Finland - cancer concerns, hyperactivity', ARRAY['USA', 'Norway', 'Finland'], 'Permitted with warning label, under review', 'food'),

('Carmoisine', ARRAY['E122', 'Azorubine'], 'commonly_questioned', 'Red artificial color E122', 'Candies, desserts, processed foods', 'Banned in USA/Canada/Japan - hyperactivity, asthma, allergic reactions', ARRAY['USA', 'Canada', 'Japan'], 'Permitted with mandatory warning label', 'food'),

('Brilliant Blue', ARRAY['E133', 'FD&C Blue No. 1'], 'commonly_questioned', 'Blue artificial color E133', 'Candies, soft drinks, desserts', 'Crosses blood-brain barrier, neurotoxicity, chromosomal damage', ARRAY[]::text[], 'Permitted with concentration limits', 'food'),

('Indigo Carmine', ARRAY['E132', 'FD&C Blue No. 2'], 'commonly_questioned', 'Blue artificial color E132', 'Candies, desserts, processed foods', 'Brain tumors in animal studies, banned in Norway', ARRAY['Norway'], 'Permitted with concentration limits', 'food'),

('Erythrosine', ARRAY['E127', 'FD&C Red No. 3'], 'commonly_questioned', 'Red artificial color E127', 'Candies, desserts, processed foods', 'Thyroid tumors in rats, interferes with thyroid function', ARRAY[]::text[], 'Permitted with concentration limits, under review', 'food'),

('Quinoline Yellow', ARRAY['E104'], 'commonly_questioned', 'Yellow artificial color E104', 'Candies, desserts, processed foods', 'Banned in USA/Canada/Japan/Australia - hyperactivity, dermatitis', ARRAY['USA', 'Canada', 'Japan', 'Australia'], 'Permitted with mandatory warning label', 'food'),

('Brown HT', ARRAY['E155'], 'commonly_questioned', 'Brown artificial color E155', 'Chocolate products, desserts', 'Banned in USA/Canada/Australia - hyperactivity, asthma', ARRAY['USA', 'Canada', 'Australia'], 'Permitted with warning label', 'food'),

-- Flavor enhancers
('Disodium Guanylate', ARRAY['E627'], 'commonly_questioned', 'Flavor enhancer E627', 'Chips, instant noodles, savory snacks, processed foods', 'MSG-like effects: headaches, numbness, flushing, neurotoxicity concerns', ARRAY[]::text[], 'Permitted with concentration limits', 'food'),

('Disodium Inosinate', ARRAY['E631'], 'commonly_questioned', 'Flavor enhancer E631', 'Chips, instant noodles, savory snacks, processed foods', 'MSG-like effects: headaches, sweating, chest pain, avoid if MSG-sensitive', ARRAY[]::text[], 'Permitted with concentration limits', 'food'),

('Monosodium Glutamate', ARRAY['MSG', 'E621'], 'commonly_questioned', 'Flavor enhancer MSG', 'Chips, instant noodles, savory snacks, processed foods', 'Headaches, nausea, chest pain, neurotoxicity at high doses', ARRAY[]::text[], 'Permitted with mandatory labeling', 'food'),

-- Acids with concerns
('Phosphoric Acid', ARRAY['E338'], 'commonly_questioned', 'Acidulant E338', 'Soft drinks, processed foods', 'Erodes tooth enamel, reduces bone density, kidney stones, calcium depletion', ARRAY[]::text[], 'Permitted with concentration limits', 'food'),

('Caramel Colour', ARRAY['E150', 'Caramel Color'], 'commonly_questioned', 'Color additive E150', 'Soft drinks, sauces, processed foods', 'Contains 4-MEI (potential carcinogen), linked to cancer in animal studies', ARRAY[]::text[], 'Permitted with limits on 4-MEI content', 'food'),

-- Personal care preservatives
('Methylchloroisothiazolinone', ARRAY['MIT', 'Kathon CG'], 'commonly_questioned', 'Preservative MIT', 'Shampoos, body washes, cleansers', 'Severe contact dermatitis, skin allergies, EU restricted, neurotoxic', ARRAY['EU (restricted concentrations)'], 'Restricted in cosmetics, concentration limits', 'cosmetic'),

('Methylisothiazolinone', ARRAY['MIT'], 'commonly_questioned', 'Preservative MIT', 'Shampoos, body washes, cleansers', 'Strong allergen, contact dermatitis, banned in leave-on products in EU', ARRAY['EU (leave-on products)'], 'Banned in leave-on cosmetics, restricted in rinse-off', 'cosmetic'),

-- Fragrances
('Fragrance', ARRAY['Parfum', 'Perfume'], 'commonly_questioned', 'Undisclosed fragrance mixture', 'Cosmetics, personal care products', 'May contain phthalates (hormone disruptors), allergens, no disclosure required', ARRAY[]::text[], 'Permitted but allergens must be listed if >0.01%', 'cosmetic'),

-- WORTH KNOWING INGREDIENTS (YELLOW CATEGORY)

-- Sugars and sweeteners
('Sugar', ARRAY['Sucrose', 'Table Sugar'], 'worth_knowing', 'Sweetener', 'Beverages, desserts, baked goods, processed foods', 'Excess causes obesity, type 2 diabetes, tooth decay, energy crashes, inflammation', ARRAY[]::text[], 'No specific restrictions, dietary guidelines recommend limits', 'food'),

('High Fructose Corn Syrup', ARRAY['HFCS', 'Corn Syrup'], 'worth_knowing', 'Sweetener', 'Soft drinks, processed foods, baked goods', 'Linked to obesity, fatty liver disease, insulin resistance, metabolic syndrome', ARRAY[]::text[], 'Permitted, dietary guidelines recommend limiting added sugars', 'food'),

('Glucose Syrup', ARRAY['Corn Syrup', 'Liquid Glucose'], 'worth_knowing', 'Sweetener', 'Candies, baked goods, processed foods', 'Rapid blood sugar spikes, weight gain, diabetes risk with regular consumption', ARRAY[]::text[], 'Permitted, no specific restrictions', 'food'),

('Invert Sugar', ARRAY['Inverted Sugar Syrup'], 'worth_knowing', 'Sweetener', 'Candies, baked goods, processed foods', 'High calorie, tooth decay, blood sugar spikes, similar concerns as regular sugar', ARRAY[]::text[], 'Permitted, no specific restrictions', 'food'),

('Maltodextrin', ARRAY['Maltodextrose'], 'worth_knowing', 'Carbohydrate additive', 'Sports drinks, processed foods, supplements', 'Very high glycemic index, blood sugar spikes, may harm gut bacteria', ARRAY[]::text[], 'Permitted, no specific restrictions', 'food'),

-- Oils and fats
('Palm Oil', ARRAY['Elaeis Guineensis Oil'], 'worth_knowing', 'Vegetable oil', 'Fried foods, baked goods, processed snacks', 'High saturated fat (50%), raises LDL cholesterol, heart disease risk', ARRAY[]::text[], 'Permitted, no specific restrictions', 'food'),

('Palmolein', ARRAY['Refined Palm Oil'], 'worth_knowing', 'Refined palm oil', 'Cooking oil, fried foods, processed foods', 'High saturated fat, may increase cardiovascular disease risk', ARRAY[]::text[], 'Permitted, no specific restrictions', 'food'),

('Hydrogenated Oil', ARRAY['Hydrogenated Fat'], 'worth_knowing', 'Modified fat', 'Margarine, baked goods, processed foods', 'May contain trans fats, increases heart disease risk, raises bad cholesterol', ARRAY[]::text[], 'Permitted with trans fat labeling requirements', 'food'),

('Partially Hydrogenated Oil', ARRAY['PHO'], 'commonly_questioned', 'Modified fat', 'Margarine, baked goods, fried foods', 'Contains trans fats - avoid! Banned in many countries, heart disease', ARRAY['USA (phased out)', 'EU (restricted)'], 'Being phased out, trans fat limits apply', 'food'),

-- Emulsifiers and stabilizers
('Soy Lecithin', ARRAY['E322', 'Lecithin'], 'worth_knowing', 'Emulsifier E322', 'Chocolates, baked goods, margarine, processed foods', 'Generally safe but soy allergen, may cause digestive issues in sensitive people', ARRAY[]::text[], 'Permitted, must declare soy allergen', 'food'),

('Mono and Diglycerides', ARRAY['E471'], 'worth_knowing', 'Emulsifier E471', 'Baked goods, margarine, processed foods', 'May contain trans fats, digestive issues, source often unclear', ARRAY[]::text[], 'Permitted, no specific restrictions', 'food'),

('Polyglycerol Polyricinoleate', ARRAY['E476', 'PGPR'], 'worth_knowing', 'Emulsifier E476', 'Chocolate, confectionery', 'Synthetic, may cause digestive upset, liver enlargement in animal studies', ARRAY[]::text[], 'Permitted with concentration limits', 'food'),

('Ammonium Phosphatides', ARRAY['E442'], 'worth_knowing', 'Emulsifier E442', 'Chocolate, confectionery', 'Synthetic, limited safety data, may affect mineral absorption', ARRAY[]::text[], 'Permitted with concentration limits', 'food'),

('Carrageenan', ARRAY['E407'], 'worth_knowing', 'Thickener E407', 'Dairy products, plant-based milks, processed foods', 'Digestive inflammation, may trigger IBS, linked to colon issues in studies', ARRAY[]::text[], 'Permitted, under ongoing safety review', 'food'),

-- Personal care surfactants
('Sodium Laureth Sulfate', ARRAY['SLES'], 'worth_knowing', 'Surfactant cleanser', 'Shampoos, body washes, cleansers, soaps', 'Strips natural oils, causes dryness, scalp irritation, eye irritation', ARRAY[]::text[], 'Permitted in cosmetics with concentration limits', 'cosmetic'),

('Sodium Lauryl Sulfate', ARRAY['SLS'], 'worth_knowing', 'Surfactant cleanser', 'Shampoos, body washes, cleansers, soaps', 'Harsh, causes skin dryness, irritation, may damage hair protein', ARRAY[]::text[], 'Permitted in cosmetics with concentration limits', 'cosmetic'),

('Cocamidopropyl Betaine', ARRAY['CAPB'], 'worth_knowing', 'Surfactant', 'Shampoos, body washes, cleansers', 'Can cause allergic reactions, contact dermatitis, eye irritation', ARRAY[]::text[], 'Permitted in cosmetics', 'cosmetic'),

-- Silicones
('Dimethiconol', ARRAY['Dimethicone Copolyol'], 'worth_knowing', 'Silicone', 'Hair care products, cosmetics', 'Builds up on hair/skin, clogs pores, environmental persistence, hard to remove', ARRAY[]::text[], 'Permitted in cosmetics', 'cosmetic'),

('Dimethicone', ARRAY['Polydimethylsiloxane'], 'worth_knowing', 'Silicone', 'Hair care products, cosmetics, skincare', 'Can trap dirt/bacteria, may cause breakouts, environmental concerns', ARRAY[]::text[], 'Permitted in cosmetics', 'cosmetic'),

-- GENERALLY RECOGNISED INGREDIENTS (GREEN CATEGORY)

-- Natural preservatives
('Ascorbic Acid', ARRAY['E300', 'Vitamin C'], 'generally_recognised', 'Vitamin C, antioxidant E300', 'Fruit juices, processed foods, supplements', 'Generally safe, essential vitamin, antioxidant properties', ARRAY[]::text[], 'Permitted, no restrictions', 'both'),

('Tocopherol', ARRAY['E306', 'Vitamin E'], 'generally_recognised', 'Vitamin E, antioxidant E306', 'Oils, processed foods, cosmetics', 'Essential vitamin, antioxidant, generally safe', ARRAY[]::text[], 'Permitted, no restrictions', 'both'),

('Citric Acid', ARRAY['E330'], 'generally_recognised', 'Natural acid E330', 'Soft drinks, candies, processed foods', 'Natural preservative and flavor enhancer, generally safe', ARRAY[]::text[], 'Permitted, no restrictions', 'food'),

-- Natural thickeners
('Guar Gum', ARRAY['E412'], 'generally_recognised', 'Natural thickener E412', 'Ice cream, sauces, gluten-free products', 'Natural fiber, generally safe, may cause digestive issues in large amounts', ARRAY[]::text[], 'Permitted, no restrictions', 'food'),

('Xanthan Gum', ARRAY['E415'], 'generally_recognised', 'Natural thickener E415', 'Sauces, dressings, gluten-free products', 'Natural polysaccharide, generally safe, excellent thickening properties', ARRAY[]::text[], 'Permitted, no restrictions', 'food'),

-- Natural colors
('Beta Carotene', ARRAY['E160a'], 'generally_recognised', 'Natural orange color E160a', 'Margarine, cheese, processed foods', 'Vitamin A precursor, natural color, generally safe', ARRAY[]::text[], 'Permitted, no restrictions', 'food'),

('Annatto', ARRAY['E160b'], 'generally_recognised', 'Natural yellow/orange color E160b', 'Cheese, butter, processed foods', 'Natural color from annatto seeds, generally safe', ARRAY[]::text[], 'Permitted, no restrictions', 'food'),

-- Basic ingredients
('Water', ARRAY['Aqua', 'H2O'], 'generally_recognised', 'Universal solvent', 'All food and cosmetic products', 'Essential for life, completely safe', ARRAY[]::text[], 'No restrictions', 'both'),

('Salt', ARRAY['Sodium Chloride', 'NaCl'], 'generally_recognised', 'Sodium chloride', 'Most processed foods', 'Essential mineral, safe in normal amounts', ARRAY[]::text[], 'No restrictions, dietary guidelines recommend limits', 'food'),

('Glycerin', ARRAY['Glycerol', 'E422'], 'generally_recognised', 'Humectant', 'Cosmetics, food products', 'Natural humectant, generally safe, moisturizing properties', ARRAY[]::text[], 'Permitted, no restrictions', 'both');

-- Create indexes for fast searching
CREATE INDEX IF NOT EXISTS idx_ingredient_rules_name_search ON ingredient_rules USING gin(to_tsvector('english', name));
CREATE INDEX IF NOT EXISTS idx_ingredient_rules_aliases_search ON ingredient_rules USING gin(aliases);
CREATE INDEX IF NOT EXISTS idx_ingredient_rules_name_lower ON ingredient_rules(lower(name));

-- Create function for ingredient search with suggestions
CREATE OR REPLACE FUNCTION search_ingredients_with_suggestions(search_term TEXT, limit_count INTEGER DEFAULT 10)
RETURNS TABLE(
    id UUID,
    name TEXT,
    aliases TEXT[],
    classification TEXT,
    what_it_is TEXT,
    commonly_found_in TEXT,
    one_line_note TEXT,
    similarity_score REAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ir.id,
        ir.name,
        ir.aliases,
        ir.classification,
        ir.what_it_is,
        ir.commonly_found_in,
        ir.one_line_note,
        GREATEST(
            similarity(lower(ir.name), lower(search_term)),
            COALESCE(
                (SELECT MAX(similarity(lower(alias), lower(search_term))) 
                 FROM unnest(ir.aliases) AS alias), 
                0
            )
        ) as similarity_score
    FROM ingredient_rules ir
    WHERE 
        lower(ir.name) LIKE lower(search_term || '%')
        OR lower(ir.name) LIKE lower('%' || search_term || '%')
        OR EXISTS (
            SELECT 1 FROM unnest(ir.aliases) AS alias 
            WHERE lower(alias) LIKE lower(search_term || '%')
        )
        OR to_tsvector('english', ir.name) @@ plainto_tsquery('english', search_term)
    ORDER BY 
        CASE 
            WHEN lower(ir.name) LIKE lower(search_term || '%') THEN 1
            WHEN lower(ir.name) LIKE lower('%' || search_term || '%') THEN 2
            ELSE 3
        END,
        similarity_score DESC,
        ir.name
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql;

-- Enable pg_trgm extension for similarity search
CREATE EXTENSION IF NOT EXISTS pg_trgm;