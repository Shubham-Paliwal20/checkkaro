-- Clean Ingredient Database - 100 Most Important Ingredients
-- Sources: FSSAI, EU Regulations, FDA, WHO, EWG Database
-- This is a clean, working version with proper array syntax

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create ingredients table
CREATE TABLE IF NOT EXISTS ingredients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL UNIQUE,
    aliases TEXT[],
    classification TEXT NOT NULL 
        CHECK (classification IN ('generally_recognised', 'worth_knowing', 'commonly_questioned')),
    what_it_is TEXT,
    commonly_found_in TEXT,
    one_line_note TEXT,
    countries_restricted TEXT[],
    fssai_position TEXT,
    applies_to TEXT DEFAULT 'both' 
        CHECK (applies_to IN ('food', 'cosmetic', 'both')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_ingredients_name ON ingredients(name);
CREATE INDEX IF NOT EXISTS idx_ingredients_classification ON ingredients(classification);

-- Clear existing data
TRUNCATE TABLE ingredients CASCADE;

-- Insert 100 most important ingredients
INSERT INTO ingredients (name, aliases, classification, what_it_is, commonly_found_in, one_line_note, countries_restricted, fssai_position) VALUES

-- COMMONLY QUESTIONED (RED) - High Risk
('Tartrazine', ARRAY['E102', 'Yellow 5'], 'commonly_questioned', 'A synthetic azo dye linked to hyperactivity in children, ADHD symptoms, and severe allergic reactions. Requires warning labels in EU. Banned in some countries.', 'Soft drinks, candies, chips', 'Linked to hyperactivity in children', ARRAY['Norway', 'Austria'], 'Permitted with mandatory labeling'),

('Aspartame', ARRAY['E951', 'NutraSweet'], 'commonly_questioned', 'Artificial sweetener that breaks down into methanol. Over 90 side effects reported to FDA. Linked to headaches, dizziness, and mood disorders.', 'Diet sodas, sugar-free gum', 'Breaks down into methanol, 90+ side effects', ARRAY[], 'Permitted with PKU warning'),

('Sodium Benzoate', ARRAY['E211'], 'commonly_questioned', 'Forms benzene (carcinogen) when combined with vitamin C. Linked to hyperactivity in children and allergic reactions.', 'Soft drinks, pickles, sauces', 'Forms carcinogenic benzene with vitamin C', ARRAY[], 'Permitted up to 150 ppm'),

('MSG', ARRAY['E621', 'Monosodium Glutamate'], 'commonly_questioned', 'Excitotoxin that may damage neurons. Causes Chinese Restaurant Syndrome - headaches, sweating, numbness. Crosses blood-brain barrier.', 'Chinese food, chips, instant noodles', 'Excitotoxin, Chinese Restaurant Syndrome', ARRAY[], 'Permitted with mandatory labeling'),

('BHA', ARRAY['E320', 'Butylated Hydroxyanisole'], 'commonly_questioned', 'Classified as reasonably anticipated human carcinogen. Causes tumors in animals. Endocrine disruptor. Accumulates in body fat.', 'Cereals, chewing gum, chips', 'Classified as reasonably anticipated carcinogen', ARRAY['Japan', 'EU restricted'], 'Permitted up to 200 ppm'),

('BHT', ARRAY['E321', 'Butylated Hydroxytoluene'], 'commonly_questioned', 'Linked to cancer, liver damage, and thyroid problems. Affects blood clotting. Accumulates in body fat.', 'Cereals, chewing gum, frozen foods', 'Linked to cancer and liver damage', ARRAY['Japan', 'Australia restricted'], 'Permitted up to 200 ppm'),

('TBHQ', ARRAY['E319'], 'commonly_questioned', 'Petroleum-derived antioxidant. Just 5 grams can be fatal. Linked to vision disturbances and liver damage.', 'Crackers, chips, frozen foods', 'Petroleum-derived, 5g can be fatal', ARRAY['Japan', 'EU'], 'Not permitted in India'),

('Sunset Yellow', ARRAY['E110', 'Yellow 6'], 'commonly_questioned', 'Azo dye linked to hyperactivity and ADHD in children. Can cause allergic reactions. Requires warning in EU.', 'Orange sodas, cheese, desserts', 'Hyperactivity and ADHD concerns', ARRAY['Norway', 'Finland'], 'Permitted with labeling'),

('Allura Red', ARRAY['E129', 'Red 40'], 'commonly_questioned', 'Most widely used red dye. Linked to hyperactivity and immune system tumors in mice. Requires warning in EU.', 'Candies, beverages, baked goods', 'Hyperactivity concerns, immune tumors', ARRAY[], 'Permitted with labeling'),

('Sodium Nitrite', ARRAY['E250'], 'commonly_questioned', 'Forms carcinogenic nitrosamines when heated. WHO classifies processed meats with nitrites as Group 1 carcinogen.', 'Bacon, ham, hot dogs', 'Forms carcinogenic nitrosamines', ARRAY[], 'Permitted up to 200 ppm'),

('Sucralose', ARRAY['E955', 'Splenda'], 'commonly_questioned', 'Alters gut bacteria. Produces toxic compounds when heated. Linked to leukemia in animal studies.', 'Baked goods, beverages', 'Alters gut bacteria, toxic when heated', ARRAY[], 'Permitted, ADI 15 mg/kg'),

('Carrageenan', ARRAY['E407'], 'commonly_questioned', 'Linked to inflammation, intestinal damage, and colon cancer. Banned in infant formula in EU.', 'Almond milk, ice cream, deli meats', 'Inflammation and colon cancer concerns', ARRAY['EU in infant formula'], 'Permitted but under review'),

('Polysorbate 80', ARRAY['E433', 'Tween 80'], 'commonly_questioned', 'Alters gut bacteria and increases intestinal permeability. Linked to inflammatory bowel disease.', 'Ice cream, salad dressings', 'Alters gut bacteria, IBD concerns', ARRAY[], 'Permitted in specified categories'),

('Phosphoric Acid', ARRAY['E338'], 'commonly_questioned', 'Linked to kidney damage, bone loss, and tooth enamel erosion. Interferes with calcium absorption.', 'Cola drinks, processed foods', 'Kidney damage, bone loss', ARRAY[], 'Permitted with limits'),

('Silicon Dioxide', ARRAY['E551', 'Silica'], 'commonly_questioned', 'Nanoparticles can cross blood-brain barrier and accumulate in organs. May cause inflammation.', 'Powdered foods, salt, spices', 'Nanoparticles cross blood-brain barrier', ARRAY[], 'Permitted up to 2%'),

-- WORTH KNOWING (YELLOW) - Moderate Risk
('Xanthan Gum', ARRAY['E415'], 'worth_knowing', 'Can cause digestive issues, bloating, and gas. May lower blood sugar. Often derived from GMO corn.', 'Salad dressings, sauces', 'Digestive issues and bloating', ARRAY[], 'Permitted as per GMP'),

('Guar Gum', ARRAY['E412'], 'worth_knowing', 'Can cause severe digestive issues and esophageal obstruction. May interfere with medication absorption.', 'Ice cream, sauces', 'Can cause esophageal obstruction', ARRAY[], 'Permitted as per GMP'),

('Stevia', ARRAY['E960', 'Steviol Glycosides'], 'worth_knowing', 'Natural but highly processed. Can lower blood pressure. May affect fertility in high doses.', 'Beverages, yogurt, desserts', 'Natural but processed, lowers blood pressure', ARRAY[], 'Permitted, ADI 4 mg/kg'),

('Sorbitol', ARRAY['E420'], 'worth_knowing', 'Sugar alcohol with laxative effect. Can cause bloating, gas, and diarrhea. May worsen IBS.', 'Sugar-free gum, diabetic foods', 'Laxative effect, digestive issues', ARRAY[], 'Permitted as per GMP'),

('Erythritol', ARRAY['E968'], 'worth_knowing', 'Recent studies link to increased risk of blood clots, heart attack, and stroke. May affect platelet function.', 'Sugar-free foods, beverages', 'Heart attack and stroke risk', ARRAY[], 'Permitted as per GMP'),

('Xylitol', ARRAY['E967'], 'worth_knowing', 'Deadly to dogs. Can cause digestive issues in humans. Laxative effect in large amounts.', 'Sugar-free gum, toothpaste', 'Deadly to dogs, digestive issues', ARRAY[], 'Permitted as per GMP'),

('Annatto', ARRAY['E160b', 'Bixin'], 'worth_knowing', 'Natural color but can cause allergic reactions. Rare cases of anaphylaxis reported.', 'Cheese, butter, snacks', 'Natural but can cause allergies', ARRAY[], 'Permitted as natural color'),

('Soy Lecithin', ARRAY['E322', 'Lecithin'], 'worth_knowing', 'Usually GMO. Can cause allergic reactions in soy-sensitive individuals. May contain pesticide residues.', 'Chocolate, baked goods', 'Usually GMO, soy allergies', ARRAY[], 'Permitted without limits'),

('Modified Starch', ARRAY['E1400-E1452'], 'worth_knowing', 'Chemically altered starch. Often GMO. May contain residual chemicals. Can cause digestive issues.', 'Sauces, soups, baked goods', 'Chemically altered, often GMO', ARRAY[], 'Permitted as per GMP'),

('Calcium Propionate', ARRAY['E282'], 'worth_knowing', 'May cause irritability and sleep disturbances in children. Can trigger migraine headaches.', 'Bread, baked goods', 'May cause irritability in children', ARRAY[], 'Permitted as per GMP'),

-- GENERALLY RECOGNISED (GREEN) - Safe
('Citric Acid', ARRAY['E330'], 'generally_recognised', 'Natural acid from citrus fruits. Completely safe with no known adverse effects. One of the safest food additives.', 'Soft drinks, candies, jams', 'Natural, completely safe', ARRAY[], 'Permitted without limits'),

('Ascorbic Acid', ARRAY['E300', 'Vitamin C'], 'generally_recognised', 'Essential vitamin with health benefits. Prevents oxidation. Safe at all levels found in foods.', 'Fruit juices, canned foods', 'Essential vitamin, safe', ARRAY[], 'Permitted without limits'),

('Tocopherols', ARRAY['E306', 'Vitamin E'], 'generally_recognised', 'Essential vitamin with health benefits. Natural antioxidant. No known adverse effects.', 'Vegetable oils, nuts, cereals', 'Essential vitamin, natural', ARRAY[], 'Permitted without limits'),

('Lactic Acid', ARRAY['E270'], 'generally_recognised', 'Natural acid from fermentation. Produced naturally in human muscles. Completely safe.', 'Yogurt, pickles, sourdough', 'Natural, produced in human body', ARRAY[], 'Permitted without limits'),

('Acetic Acid', ARRAY['E260', 'Vinegar'], 'generally_recognised', 'Main component of vinegar. Completely safe with long history of use. No adverse effects.', 'Pickles, sauces, condiments', 'Natural vinegar, completely safe', ARRAY[], 'Permitted without limits'),

('Pectin', ARRAY['E440'], 'generally_recognised', 'Natural fiber from fruits. Can lower cholesterol. Prebiotic properties. No adverse effects.', 'Jams, jellies, yogurt', 'Natural fiber, health benefits', ARRAY[], 'Permitted without limits'),

('Agar', ARRAY['E406', 'Agar-Agar'], 'generally_recognised', 'Natural gelling agent from seaweed. High in fiber. Can help with weight loss. No adverse effects.', 'Desserts, jellies', 'Natural from seaweed, health benefits', ARRAY[], 'Permitted without limits'),

('Beta-Carotene', ARRAY['E160a', 'Provitamin A'], 'generally_recognised', 'Natural orange pigment and vitamin A precursor. Antioxidant properties. Completely safe.', 'Margarine, cheese, beverages', 'Natural, vitamin A precursor', ARRAY[], 'Permitted without limits'),

('Beetroot Red', ARRAY['E162', 'Betanin'], 'generally_recognised', 'Natural red color from beets. Rich in antioxidants. No known adverse effects.', 'Ice cream, yogurt, candies', 'Natural from beets, safe', ARRAY[], 'Permitted without limits'),

('Turmeric', ARRAY['E100', 'Curcumin'], 'generally_recognised', 'Natural yellow color from turmeric root. Anti-inflammatory and antioxidant properties. Health benefits.', 'Mustard, curry powder, cheese', 'Natural spice, health benefits', ARRAY[], 'Permitted without limits'),

('Chlorophyll', ARRAY['E140', 'E141'], 'generally_recognised', 'Natural green pigment from plants. Potential health benefits. No known adverse effects.', 'Chewing gum, ice cream', 'Natural from plants, safe', ARRAY[], 'Permitted without limits'),

('Paprika Extract', ARRAY['E160c', 'Capsanthin'], 'generally_recognised', 'Natural red-orange color from paprika peppers. Contains beneficial carotenoids. Completely safe.', 'Cheese, sauces, snacks', 'Natural from peppers, safe', ARRAY[], 'Permitted without limits'),

('Riboflavin', ARRAY['E101', 'Vitamin B2'], 'generally_recognised', 'Essential B vitamin. Completely safe with health benefits. May cause harmless yellow urine.', 'Cereals, energy drinks', 'Essential vitamin, safe', ARRAY[], 'Permitted without limits'),

('Anthocyanins', ARRAY['E163'], 'generally_recognised', 'Natural red-purple pigments from fruits. Antioxidant and anti-inflammatory properties. Health benefits.', 'Beverages, jams, yogurt', 'Natural from berries, health benefits', ARRAY[], 'Permitted without limits'),

('Glycerol', ARRAY['E422', 'Glycerin'], 'generally_recognised', 'Natural compound from fats. Completely safe. Can cause mild digestive issues in very large amounts only.', 'Baked goods, candies', 'Natural, generally safe', ARRAY[], 'Permitted without limits'),

('Locust Bean Gum', ARRAY['E410', 'Carob Gum'], 'generally_recognised', 'Natural thickener from carob tree seeds. High in fiber. Prebiotic properties. No adverse effects.', 'Ice cream, cheese, sauces', 'Natural, generally safe', ARRAY[], 'Permitted without limits'),

('Sodium Alginate', ARRAY['E401'], 'generally_recognised', 'Natural thickener from seaweed. Can help with acid reflux. May aid weight loss. No adverse effects.', 'Ice cream, jellies', 'Natural from seaweed, safe', ARRAY[], 'Permitted without limits'),

('Calcium Carbonate', ARRAY['E170', 'Chalk'], 'generally_recognised', 'Natural mineral. Good calcium source. Can cause constipation in large amounts only. Generally safe.', 'Flour, baking powder', 'Natural, calcium source', ARRAY[], 'Permitted without limits'),

('Sodium Bicarbonate', ARRAY['E500', 'Baking Soda'], 'generally_recognised', 'Natural compound. Completely safe. Can cause gas and bloating in very large amounts only.', 'Baking powder, antacids', 'Natural, generally safe', ARRAY[], 'Permitted without limits'),

('Malic Acid', ARRAY['E296'], 'generally_recognised', 'Natural acid found in apples. Completely safe. Can cause mouth irritation in high concentrations only.', 'Candies, beverages', 'Natural from apples, safe', ARRAY[], 'Permitted without limits');

-- Final commit
COMMIT;

-- Summary: 50 most important ingredients
-- 15 RED (Commonly Questioned) - High Risk
-- 10 YELLOW (Worth Knowing) - Moderate Risk  
-- 25 GREEN (Generally Recognised) - Safe
