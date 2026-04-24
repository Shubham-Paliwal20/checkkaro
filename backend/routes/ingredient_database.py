"""
Comprehensive Ingredient Database - Single Source of Truth
This ensures consistency between product search and ingredient check pages
"""

COSMETIC_CATEGORIES = {
    "Skincare", "Hair Care", "Cosmetics", "Personal Care", "Baby Care", "Oral Care", "Household"
}

# Ingredients that are standard/safe in cosmetics but have dietary concerns in food
COSMETIC_SAFE_OVERRIDES = {
    'sodium chloride': ('Isotonic agent / texture ingredient', 'Standard cosmetic ingredient; the salt-intake concern applies only to food, not topical use'),
    'nacl': ('Isotonic agent / texture ingredient', 'Standard cosmetic ingredient used to adjust texture and tonicity'),
    'citric acid': ('pH adjuster (E330)', 'Used in cosmetics to balance pH; the tooth-enamel concern applies to ingestion, not skin application'),
    'glycerin': ('Humectant', 'Standard moisturising agent, one of the most widely used cosmetic ingredients globally'),
    'glycerine': ('Humectant', 'Standard moisturising agent, one of the most widely used cosmetic ingredients globally'),
    'glycerol': ('Humectant', 'Standard moisturising agent, widely used in cosmetics and pharmaceuticals'),
    'sorbitol': ('Humectant', 'Used as a moisture-retaining agent in cosmetics; laxative concern is only relevant to ingestion'),
    'ascorbic acid': ('Antioxidant / Vitamin C', 'Antioxidant preservative and skin-brightening agent; safe for topical use'),
    'sodium bicarbonate': ('pH adjuster', 'Used to adjust pH in cosmetic formulations; no dietary concerns apply topically'),
    'lactic acid': ('Alpha hydroxy acid (AHA)', 'Standard exfoliant and pH adjuster in skincare; gentle and widely used'),
    'tocopherol': ('Vitamin E antioxidant', 'Natural antioxidant preservative widely used in skincare products'),
    'tocopheryl acetate': ('Vitamin E ester', 'Stable form of Vitamin E, widely used antioxidant in cosmetics'),
    'salt': ('Isotonic / texture agent', 'Standard cosmetic ingredient; dietary salt concerns do not apply to topical use'),
}


def classify_ingredient(ingredient_name, category=None):
    """Classify ingredients based on regulatory and health concerns - SINGLE SOURCE OF TRUTH"""
    ingredient_lower = ingredient_name.lower()
    is_cosmetic = category in COSMETIC_CATEGORIES
    
    # COMMONLY QUESTIONED INGREDIENTS (RED) - Regulatory concerns, banned substances, health risks
    commonly_questioned_patterns = {
        # Preservatives with serious concerns
        'triclosan': ('Antibacterial agent banned in EU cosmetics', 'Hormone disruption, antibiotic resistance, thyroid problems'),
        'sodium benzoate': ('Preservative E211', 'Forms benzene (carcinogen) with vitamin C, linked to hyperactivity in children'),
        'sodium metabisulphite': ('Sulfite preservative E223', 'Severe allergic reactions, asthma attacks, can cause anaphylaxis'),
        'sodium nitrite': ('Meat preservative E250', 'Forms nitrosamines (cancer-causing) when cooked at high heat'),
        'sodium nitrate': ('Meat preservative E251', 'Converts to nitrite in body, linked to colorectal cancer'),
        'sulfur dioxide': ('Preservative E220', 'Destroys vitamin B1, triggers severe asthma, allergic reactions'),
        'methylparaben': ('Paraben preservative E218', 'Mimics estrogen, hormone disruption, accumulates in breast tissue'),
        'propylparaben': ('Paraben preservative E216', 'Endocrine disruptor, linked to reduced sperm count, reproductive harm'),
        'butylparaben': ('Paraben preservative E214', 'Strongest hormone disruptor, bioaccumulation, reproductive toxicity'),
        
        # Artificial colors with serious concerns
        'tartrazine': ('Yellow artificial color E102', 'Hyperactivity & ADHD in children, asthma attacks, requires EU warning label'),
        'sunset yellow': ('Orange artificial color E110', 'Hyperactivity in children, allergic reactions, banned in Norway & Finland'),
        'allura red': ('Red artificial color E129', 'Hyperactivity, immune system tumors in mice, allergic reactions'),
        'ponceau 4r': ('Red artificial color E124', 'Banned in USA/Norway/Finland - cancer concerns, hyperactivity'),
        'carmoisine': ('Red artificial color E122', 'Banned in USA/Canada/Japan - hyperactivity, asthma, allergic reactions'),
        'brilliant blue': ('Blue artificial color E133', 'Crosses blood-brain barrier, neurotoxicity, chromosomal damage'),
        'indigo carmine': ('Blue artificial color E132', 'Brain tumors in animal studies, banned in Norway'),
        'erythrosine': ('Red artificial color E127', 'Thyroid tumors in rats, interferes with thyroid function'),
        'quinoline yellow': ('Yellow artificial color E104', 'Banned in USA/Canada/Japan/Australia - hyperactivity, dermatitis'),
        'brown ht': ('Brown artificial color E155', 'Banned in USA/Canada/Australia - hyperactivity, asthma'),
        
        # Flavor enhancers
        'disodium guanylate': ('Flavor enhancer E627', 'MSG-like effects: headaches, numbness, flushing, neurotoxicity concerns'),
        'disodium inosinate': ('Flavor enhancer E631', 'MSG-like effects: headaches, sweating, chest pain, avoid if MSG-sensitive'),
        'monosodium glutamate': ('Flavor enhancer MSG', 'Headaches, nausea, chest pain, neurotoxicity at high doses'),
        
        # Acids with concerns
        'phosphoric acid': ('Acidulant E338', 'Erodes tooth enamel, reduces bone density, kidney stones, calcium depletion'),
        'caramel colour': ('Color additive E150', 'Contains 4-MEI (potential carcinogen), linked to cancer in animal studies'),
        'caramel color': ('Color additive E150', 'Contains 4-MEI (potential carcinogen), linked to cancer in animal studies'),
        
        # Preservatives in personal care
        'methylchloroisothiazolinone': ('Preservative MIT', 'Severe contact dermatitis, skin allergies, EU restricted, neurotoxic'),
        'methylisothiazolinone': ('Preservative MIT', 'Strong allergen, contact dermatitis, banned in leave-on products in EU'),
        
        # Fragrances
        'fragrance': ('Undisclosed fragrance mixture', 'May contain phthalates (hormone disruptors), allergens, no disclosure required'),
        'perfume': ('Undisclosed fragrance mixture', 'May contain hormone disruptors, allergens, respiratory irritants'),
        'parfum': ('Undisclosed fragrance mixture', 'May contain phthalates, allergens, linked to asthma and allergies'),
        
        # Artificial flavors
        'artificial': ('Synthetic flavoring', 'May contain allergens, some linked to behavioral issues in children'),
    }
    
    # WORTH KNOWING INGREDIENTS (YELLOW) - Generally safe but with considerations
    worth_knowing_patterns = {
        # Sugars and sweeteners
        'sugar': ('Sweetener', 'Excess causes obesity, type 2 diabetes, tooth decay, energy crashes, inflammation'),
        'high fructose corn syrup': ('Sweetener', 'Linked to obesity, fatty liver disease, insulin resistance, metabolic syndrome'),
        'glucose syrup': ('Sweetener', 'Rapid blood sugar spikes, weight gain, diabetes risk with regular consumption'),
        'invert sugar': ('Sweetener', 'High calorie, tooth decay, blood sugar spikes, similar concerns as regular sugar'),
        'maltodextrin': ('Carbohydrate additive', 'Very high glycemic index, blood sugar spikes, may harm gut bacteria'),
        
        # Oils and fats
        'palm oil': ('Vegetable oil', 'High saturated fat (50%), raises LDL cholesterol, heart disease risk'),
        'palmolein': ('Refined palm oil', 'High saturated fat, may increase cardiovascular disease risk'),
        'hydrogenated': ('Modified fat', 'May contain trans fats, increases heart disease risk, raises bad cholesterol'),
        'partially hydrogenated': ('Modified fat', 'Contains trans fats - avoid! Banned in many countries, heart disease'),
        
        # Emulsifiers and stabilizers
        'soy lecithin': ('Emulsifier E322', 'Generally safe but soy allergen, may cause digestive issues in sensitive people'),
        'mono and diglycerides': ('Emulsifier E471', 'May contain trans fats, digestive issues, source often unclear'),
        'polyglycerol polyricinoleate': ('Emulsifier E476', 'Synthetic, may cause digestive upset, liver enlargement in animal studies'),
        'ammonium phosphatides': ('Emulsifier E442', 'Synthetic, limited safety data, may affect mineral absorption'),
        'carrageenan': ('Thickener E407', 'Digestive inflammation, may trigger IBS, linked to colon issues in studies'),
        
        # Surfactants in personal care
        'sodium laureth sulfate': ('Surfactant cleanser', 'Strips natural oils, causes dryness, scalp irritation, eye irritation'),
        'sodium lauryl sulfate': ('Surfactant cleanser', 'Harsh, causes skin dryness, irritation, may damage hair protein'),
        'cocamidopropyl betaine': ('Surfactant', 'Can cause allergic reactions, contact dermatitis, eye irritation'),
        
        # Silicones
        'dimethiconol': ('Silicone', 'Builds up on hair/skin, clogs pores, environmental persistence, hard to remove'),
        'dimethicone': ('Silicone', 'Can trap dirt/bacteria, may cause breakouts, environmental concerns'),
        
        # Chelating agents
        'tetrasodium edta': ('Chelating agent', 'Binds essential minerals, environmental persistence, may enhance absorption of toxins'),
        'disodium edta': ('Chelating agent', 'Removes beneficial minerals, environmental pollutant, penetration enhancer'),
        'tetrasodium etidronate': ('Chelating agent', 'Binds minerals like calcium, may affect bone health with long-term use'),
        
        # Preservatives (milder)
        'sodium benzoate': ('Preservative E211', 'Can form benzene with vitamin C (carcinogen), asthma trigger in sensitive people'),
        'potassium sorbate': ('Preservative E202', 'Generally safe but may cause allergic reactions, skin irritation, migraines'),
        'citric acid': ('Preservative/acidulant E330', 'Tooth enamel erosion with frequent exposure, stomach upset in large amounts'),
        
        # Colorants (natural/mineral)
        'titanium dioxide': ('White pigment E171', 'Nanoparticles may penetrate skin, inhalation concerns, under EU review'),
        'beta carotene': ('Orange color E160a', 'Safe but high doses linked to lung cancer risk in smokers'),
        'caramel': ('Brown color', 'Natural but may contain trace amounts of carcinogenic compounds'),
        
        # Thickeners
        'guar gum': ('Thickener E412', 'Digestive issues, bloating, gas, may interfere with medication absorption'),
        'xanthan gum': ('Thickener E415', 'Digestive issues in large amounts, bloating, may cause allergic reactions'),
        
        # Humectants
        'propylene glycol': ('Humectant', 'Skin irritation, allergic reactions, neurotoxicity at high doses'),
        'glycerin': ('Humectant', 'Generally safe but may cause headaches, thirst, nausea in large amounts'),
        'sorbitol': ('Humectant/sweetener', 'Laxative effect, bloating, diarrhea, abdominal pain in moderate amounts'),
        
        # Caffeine
        'caffeine': ('Stimulant', 'Anxiety, jitters, insomnia, dependency, heart palpitations, dehydration'),
        
        # Alcohol
        'alcohol': ('Solvent', 'Drying, irritating, disrupts skin barrier, may cause sensitivity'),
        'ethanol': ('Solvent', 'Drying, can damage skin barrier, irritation with frequent use'),
        
        # Salts
        'salt': ('Sodium chloride', 'High intake causes high blood pressure, heart disease, stroke, kidney damage'),
        'sodium chloride': ('Salt', 'Excess linked to hypertension, cardiovascular disease, kidney stones'),
        
        # Acids (milder)
        'lactic acid': ('Acid E270', 'Skin irritation, sun sensitivity, stinging on broken skin'),
        'malic acid': ('Acid E296', 'Tooth enamel erosion, mouth irritation, digestive upset in large amounts'),
        
        # Vitamins and minerals (when added)
        'ascorbic acid': ('Vitamin C E300', 'Generally safe but high doses cause diarrhea, kidney stones, nausea'),
        'tocopherol': ('Vitamin E E306', 'Safe but very high doses may increase bleeding risk, interfere with medications'),
        'vitamin': ('Nutrient', 'Fortified - check if you need extra, excess can cause toxicity'),
        'mineral': ('Nutrient', 'Fortified - excess minerals can interfere with absorption of others'),
        
        # Proteins
        'whey': ('Milk protein', 'Dairy allergen, digestive issues in lactose intolerant, acne trigger for some'),
        'casein': ('Milk protein', 'Dairy allergen, digestive issues, may cause inflammation in sensitive people'),
        'lactose': ('Milk sugar', 'Causes bloating, gas, diarrhea in lactose intolerant (65% of adults)'),
        
        # Starches
        'starch': ('Carbohydrate', 'High glycemic, blood sugar spikes, weight gain with excess consumption'),
        'modified starch': ('Modified carbohydrate', 'Chemically altered, may cause digestive issues, blood sugar spikes'),
        
        # Raising agents
        'sodium bicarbonate': ('Baking soda E500', 'Excess causes gas, bloating, alkalosis, interferes with stomach acid'),
        'ammonium bicarbonate': ('Raising agent E503', 'Generally safe, breaks down during baking, may cause irritation'),
        'sodium carbonate': ('Raising agent E500', 'Skin/eye irritant, digestive upset if consumed in large amounts'),
        'potassium carbonate': ('Raising agent E501', 'Irritant, may cause digestive issues, interferes with medications'),
        
        # Anticaking agents
        'silicon dioxide': ('Anticaking agent E551', 'Nanoparticles under study, inhalation concerns, may affect gut health'),
        
        # Flavor enhancers (milder)
        'yeast extract': ('Flavor enhancer', 'Contains natural glutamates, may trigger MSG-like reactions in sensitive people'),
        'hydrolysed': ('Protein flavor enhancer', 'Contains free glutamates, headaches and reactions in MSG-sensitive people'),
        
        # Colorants (natural)
        'annatto': ('Natural yellow/orange color E160b', 'Rare but can cause allergic reactions, hives, IBS symptoms'),
        'paprika': ('Natural red color', 'Generally safe but may cause allergic reactions in sensitive individuals'),
        'beetroot': ('Natural red color', 'Generally safe but may cause red urine/stools (harmless but alarming)'),
        
        # Waxes and glazing agents
        'shellac': ('Glazing agent E904', 'Natural resin from insects, rare allergic reactions, digestive issues'),
        'beeswax': ('Glazing agent E901', 'Generally safe but rare allergic reactions, may cause digestive upset'),
        'carnauba wax': ('Glazing agent E903', 'Generally safe but indigestible, may cause digestive discomfort'),
    }
    
    # GENERALLY RECOGNISED - Natural/herbal/organic ingredients (check FIRST before worth_knowing)
    generally_recognised_patterns = {
        # Herbal extracts
        'neem': ('Herbal extract from neem tree', 'Traditional Ayurvedic ingredient, antibacterial, antifungal properties'),
        'neem extract': ('Herbal extract from neem tree', 'Traditional Ayurvedic ingredient with antibacterial properties'),
        'neem oil': ('Natural oil from neem tree', 'Ayurvedic ingredient with antibacterial and antifungal properties'),
        'tulsi': ('Holy basil extract', 'Adaptogenic herb, antioxidant, antimicrobial, widely used in Ayurveda'),
        'tulsi extract': ('Holy basil extract', 'Adaptogenic herb with antioxidant and antimicrobial properties'),
        'aloe vera': ('Aloe vera gel/extract', 'Soothing, moisturizing, anti-inflammatory, widely used in skincare'),
        'aloe': ('Aloe vera extract', 'Soothing and moisturizing natural ingredient'),
        'turmeric extract': ('Curcumin-rich herbal extract', 'Anti-inflammatory, antioxidant, traditional Ayurvedic ingredient'),
        'turmeric': ('Natural spice/colorant', 'Anti-inflammatory, antioxidant, safe at normal dietary levels'),
        'haldi': ('Turmeric extract', 'Traditional Indian spice with anti-inflammatory properties'),
        'neem leaves': ('Neem leaf extract', 'Antibacterial and antifungal herbal ingredient'),
        'ashwagandha': ('Adaptogenic herb', 'Traditional Ayurvedic herb, stress-reducing, generally safe'),
        'mulethi': ('Licorice root extract', 'Traditional herb, anti-inflammatory, soothing properties'),
        'ginger': ('Natural spice/extract', 'Anti-nausea, anti-inflammatory, digestive aid, safe at normal levels'),
        'ginger extract': ('Natural ginger extract', 'Anti-inflammatory and digestive properties'),
        'cardamom': ('Natural spice', 'Digestive aid, antioxidant, safe at normal dietary levels'),
        'cloves': ('Natural spice', 'Antimicrobial, antioxidant, safe at normal dietary levels'),
        'cinnamon': ('Natural spice', 'Antioxidant, anti-inflammatory, safe at normal dietary levels'),
        'cassia': ('Natural spice (cinnamon variety)', 'Antioxidant properties, safe at normal dietary levels'),
        'black pepper': ('Natural spice', 'Antioxidant, digestive aid, safe at normal dietary levels'),
        'cumin': ('Natural spice', 'Digestive aid, antioxidant, safe at normal dietary levels'),
        'coriander': ('Natural spice', 'Digestive aid, antioxidant, safe at normal dietary levels'),
        'fenugreek': ('Natural spice/herb', 'Blood sugar regulation, digestive aid, safe at normal levels'),
        'mustard': ('Natural spice', 'Antioxidant, digestive aid, safe at normal dietary levels'),
        'asafoetida': ('Natural spice (hing)', 'Digestive aid, anti-flatulent, safe at normal dietary levels'),
        'bay leaves': ('Natural herb', 'Antioxidant, digestive aid, safe at normal dietary levels'),
        'mace': ('Natural spice', 'Antioxidant, digestive aid, safe at normal dietary levels'),
        'nutmeg': ('Natural spice', 'Antioxidant, safe at normal dietary levels'),
        'saffron': ('Natural spice/colorant', 'Antioxidant, mood-enhancing, safe at normal dietary levels'),
        'mint': ('Natural herb', 'Digestive aid, cooling, antimicrobial, safe at normal levels'),
        'mint extract': ('Natural mint extract', 'Cooling and digestive properties'),
        'rosemary': ('Natural herb extract', 'Antioxidant, antimicrobial, safe at normal levels'),
        'rosemary extract': ('Natural rosemary extract', 'Natural antioxidant preservative'),
        'tea tree': ('Tea tree oil', 'Natural antimicrobial, antifungal, used in skincare'),
        'tea tree oil': ('Natural essential oil', 'Antimicrobial and antifungal properties'),
        'sandalwood': ('Natural wood extract', 'Soothing, anti-inflammatory, traditional skincare ingredient'),
        'pomegranate': ('Natural fruit extract', 'Antioxidant-rich, anti-inflammatory, safe'),
        'pomegranate seeds': ('Natural ingredient', 'Rich in antioxidants, safe at normal levels'),
        'winter cherry': ('Ashwagandha extract', 'Adaptogenic herb, stress-reducing, safe'),
        'indian pennywort': ('Centella asiatica extract', 'Wound healing, anti-inflammatory, safe'),
        'babool': ('Acacia extract', 'Traditional Ayurvedic ingredient for oral care'),
        'clove oil': ('Natural essential oil', 'Antimicrobial, analgesic, traditional oral care ingredient'),
        'olive oil': ('Natural plant oil', 'Rich in healthy fats, antioxidants, widely used in skincare'),
        'coconut oil': ('Natural plant oil', 'Antimicrobial, moisturizing, safe for skin and food'),
        'argan oil': ('Natural plant oil', 'Rich in vitamin E, moisturizing, safe for hair and skin'),
        'jojoba': ('Natural plant wax/oil', 'Moisturizing, non-comedogenic, safe for skin'),
        'shea butter': ('Natural plant butter', 'Moisturizing, anti-inflammatory, safe for skin'),
        'cocoa butter': ('Natural plant fat', 'Moisturizing, antioxidant, safe for skin and food'),
        'honey': ('Natural sweetener', 'Antimicrobial, antioxidant, safe at normal levels'),
        'pure honey': ('Natural honey', 'Natural sweetener with antimicrobial properties'),
        'beeswax': ('Natural wax', 'Protective, moisturizing, safe for skin'),
        'milk': ('Dairy ingredient', 'Natural protein and calcium source'),
        'milk solids': ('Dairy ingredient', 'Natural dairy component'),
        'paneer': ('Fresh Indian cheese', 'Natural dairy product, protein source'),
        'cream': ('Dairy ingredient', 'Natural dairy fat'),
        'butter': ('Dairy fat', 'Natural dairy ingredient'),
        'ghee': ('Clarified butter', 'Traditional Indian cooking fat, natural'),
        'whole wheat flour': ('Whole grain flour', 'Natural whole grain, good source of fiber'),
        'wheat flour': ('Grain flour', 'Natural grain ingredient'),
        'oats': ('Whole grain', 'Natural whole grain, high in fiber'),
        'rolled oats': ('Whole grain oats', 'Natural whole grain, high in fiber and beta-glucan'),
        'whole grain': ('Whole grain ingredient', 'Natural whole grain, good source of fiber'),
        'black tea': ('Natural tea', 'Rich in antioxidants, safe at normal consumption'),
        'green tea': ('Natural tea', 'Rich in antioxidants, catechins, safe at normal consumption'),
        'coffee': ('Natural coffee', 'Contains caffeine and antioxidants, safe at moderate levels'),
        'chicory': ('Natural root ingredient', 'Prebiotic fiber, digestive aid, safe'),
        'mango pulp': ('Natural fruit pulp', 'Natural fruit ingredient, vitamins and minerals'),
        'orange juice': ('Natural fruit juice', '100% natural fruit juice'),
        'apple juice': ('Natural fruit juice', 'Natural fruit ingredient'),
        'lemon': ('Natural citrus', 'Natural vitamin C source, safe'),
        'lime': ('Natural citrus', 'Natural vitamin C source, safe'),
        'tomato': ('Natural vegetable', 'Rich in lycopene, vitamins, safe'),
        'tomatoes': ('Natural vegetable', 'Rich in lycopene and vitamins'),
        'onion': ('Natural vegetable', 'Natural flavoring, antioxidant, safe'),
        'garlic': ('Natural vegetable', 'Antimicrobial, antioxidant, safe at normal levels'),
        'spinach': ('Natural vegetable', 'Rich in iron, vitamins, safe'),
        'potato': ('Natural vegetable', 'Natural starch source, safe'),
        'potatoes': ('Natural vegetable', 'Natural starch source, safe'),
        'cashew': ('Natural nut', 'Natural nut, healthy fats, protein'),
        'almond': ('Natural nut', 'Natural nut, healthy fats, vitamin E'),
        'hazelnut': ('Natural nut', 'Natural nut, healthy fats, antioxidants'),
        'raisin': ('Dried fruit', 'Natural dried fruit, safe'),
        'water': ('Water', 'Essential ingredient, no concerns'),
        'salt': ('Sodium chloride', 'Essential mineral, safe at normal dietary levels'),
        'iodised salt': ('Iodized salt', 'Essential mineral with added iodine for thyroid health'),
        'lactic acid culture': ('Probiotic culture', 'Beneficial bacteria, safe, promotes gut health'),
        'cheese culture': ('Probiotic culture', 'Beneficial bacteria used in cheese making'),
        'yeast': ('Natural leavening agent', 'Natural microorganism, safe, used in baking'),
        'malt': ('Natural grain extract', 'Natural grain ingredient, safe'),
        'malt extract': ('Natural grain extract', 'Natural grain ingredient, safe'),
        'malted barley': ('Natural grain', 'Natural grain ingredient, safe'),
        'roasted gram': ('Natural legume', 'Natural roasted chickpea flour, safe'),
        'gram flour': ('Natural legume flour', 'Natural chickpea flour, safe'),
        'spices': ('Natural spice blend', 'Natural spices, generally safe'),
        'natural flavour': ('Natural flavoring', 'Derived from natural sources, generally safe'),
        'natural flavor': ('Natural flavoring', 'Derived from natural sources, generally safe'),
        'vanilla': ('Natural flavoring', 'Natural vanilla extract, safe'),
        'charcoal powder': ('Activated charcoal', 'Natural detoxifying ingredient, safe in skincare'),
        'salicylic acid': ('Beta hydroxy acid', 'Natural acid from willow bark, effective for acne, safe at normal levels'),
        'panthenol': ('Provitamin B5', 'Natural vitamin precursor, moisturizing, safe'),
        'keratin': ('Natural protein', 'Natural hair protein, safe'),
        'ceramide': ('Natural lipid', 'Natural skin barrier component, safe'),
        'collagen': ('Natural protein', 'Natural skin protein, safe'),
        'hyaluronic acid': ('Natural polysaccharide', 'Natural skin hydrator, safe'),
        'vitamin c': ('Ascorbic acid', 'Essential vitamin, antioxidant, safe'),
        'vitamin e': ('Tocopherol', 'Essential vitamin, antioxidant, safe'),
        'zinc': ('Essential mineral', 'Essential mineral, safe at normal levels'),
        'iron': ('Essential mineral', 'Essential mineral, safe at normal levels'),
        'calcium': ('Essential mineral', 'Essential mineral for bones, safe'),
        'potassium': ('Essential mineral', 'Essential mineral, safe at normal levels'),
        'protein': ('Natural protein', 'Essential macronutrient, safe'),
        'whey protein': ('Milk-derived protein', 'Natural dairy protein, safe for most people'),
        'fruit extract': ('Natural fruit extract', 'Natural plant-derived ingredient, safe'),
        'plant extract': ('Natural plant extract', 'Natural plant-derived ingredient, safe'),
        'herbal extract': ('Natural herbal extract', 'Natural plant-derived ingredient, safe'),
        'botanical extract': ('Natural botanical extract', 'Natural plant-derived ingredient, safe'),
    }

    # For cosmetic/topical products, override food-context concerns with cosmetic-appropriate classification
    if is_cosmetic:
        for pattern, (what_it_is, note) in COSMETIC_SAFE_OVERRIDES.items():
            if pattern in ingredient_lower:
                return {
                    'classification': 'generally_recognised',
                    'what_it_is': what_it_is,
                    'one_line_note': note,
                    'regulatory_note': 'Standard cosmetic ingredient, no topical safety concerns'
                }

    # Check commonly questioned first (highest priority)
    for pattern, (what_it_is, note) in commonly_questioned_patterns.items():
        if pattern in ingredient_lower:
            return {
                'classification': 'commonly_questioned',
                'what_it_is': what_it_is,
                'one_line_note': note,
                'regulatory_note': 'Check usage guidelines and restrictions'
            }

    # Check generally recognised BEFORE worth_knowing (natural/herbal ingredients)
    for pattern, (what_it_is, note) in generally_recognised_patterns.items():
        if pattern in ingredient_lower:
            return {
                'classification': 'generally_recognised',
                'what_it_is': what_it_is,
                'one_line_note': note,
                'regulatory_note': 'No specific restrictions, widely used'
            }

    # Check worth knowing
    for pattern, (what_it_is, note) in worth_knowing_patterns.items():
        if pattern in ingredient_lower:
            return {
                'classification': 'worth_knowing',
                'what_it_is': what_it_is,
                'one_line_note': note,
                'regulatory_note': 'FSSAI approved with usage guidelines'
            }
    
    # Default to generally recognised
    return {
        'classification': 'generally_recognised',
        'what_it_is': 'Food or cosmetic ingredient',
        'one_line_note': 'Generally recognised as safe',
        'regulatory_note': 'No specific restrictions'
    }


def get_countries_restricted(ingredient_name):
    """Return list of countries where the ingredient is banned or restricted"""
    ingredient_lower = ingredient_name.lower()

    bans = {
        'triclosan': ['European Union (cosmetics ban)', 'USA (hand soaps ban by FDA)', 'Canada (regulated)'],
        'tartrazine': ['Austria', 'Norway', 'EU (warning label required)'],
        'sunset yellow': ['Norway', 'Finland', 'EU (warning label required)'],
        'allura red': ['Denmark', 'Belgium', 'France', 'Switzerland', 'Sweden', 'Austria', 'Norway', 'EU (warning label required)'],
        'ponceau 4r': ['USA', 'Norway', 'Finland', 'EU (warning label required)'],
        'carmoisine': ['USA', 'Canada', 'Japan', 'Austria', 'Norway', 'Sweden'],
        'quinoline yellow': ['USA', 'Canada', 'Japan', 'Australia', 'Norway'],
        'brown ht': ['USA', 'Canada', 'Australia', 'Belgium', 'France', 'Switzerland'],
        'erythrosine': ['Norway', 'USA (banned in cosmetics)'],
        'brilliant blue': ['Belgium', 'France', 'Germany', 'Greece', 'Italy', 'Spain', 'Switzerland'],
        'indigo carmine': ['Norway', 'UK (restricted)'],
        'methylparaben': ['Denmark (children\'s products)', 'EU (concentration restricted)'],
        'propylparaben': ['Denmark (children\'s products)', 'EU (banned in children under 3)'],
        'butylparaben': ['Denmark', 'EU (banned in children under 3)', 'Japan (restricted)'],
        'methylisothiazolinone': ['European Union (banned in leave-on cosmetics)', 'Canada (restricted)'],
        'methylchloroisothiazolinone': ['European Union (restricted)', 'Japan (restricted)'],
        'sodium nitrite': ['EU (concentration limits)', 'UK (restricted since 2022)', 'Several Nordic countries (restricted)'],
        'sodium nitrate': ['EU (restricted concentration)', 'Several Nordic countries (restricted)'],
        'caramel colour': ['EU (E150d restricted in some beverages)', 'California (Prop 65 warning)'],
        'caramel color': ['EU (E150d restricted in some beverages)', 'California (Prop 65 warning)'],
        'phosphoric acid': ['EU (labelling required)', 'Several countries (concentration limits)'],
        'sulfur dioxide': ['Australia (concentration limits)', 'EU (labelling required for asthmatics)'],
        'sodium metabisulphite': ['Australia (must declare)', 'EU (labelling required for asthmatics)'],
        'fragrance': ['EU (26 allergens must be individually declared)', 'USA (California Prop 65 for some components)'],
        'parfum': ['EU (26 allergens must be individually declared)', 'USA (California Prop 65 for some components)'],
        'perfume': ['EU (26 allergens must be individually declared)', 'USA (California Prop 65 for some components)'],
        'tbhq': ['Japan (banned)', 'EU (restricted, max 100mg/kg)', 'Australia (concentration limits)'],
        'tert-butylhydroquinone': ['Japan (banned)', 'EU (restricted)', 'Australia'],
        'bha': ['Japan (banned)', 'EU (restricted in some foods)', 'California (listed as carcinogen)'],
        'butylated hydroxyanisole': ['Japan (banned)', 'EU (restricted in some foods)', 'California (Prop 65)'],
        'potassium bromate': ['European Union', 'United Kingdom', 'Canada', 'Brazil', 'China', 'Sri Lanka', 'Nigeria', 'Peru', 'Australia'],
        'brominated vegetable oil': ['European Union', 'Japan', 'India'],
        'azodicarbonamide': ['European Union', 'United Kingdom', 'Australia', 'Singapore', 'most of Asia'],
        'titanium dioxide': ['European Union (banned as food additive E171 since 2022)'],
        'red 3': ['USA (banned in cosmetics)', 'EU (restricted)'],
        'erythrosine': ['Norway', 'USA (banned in cosmetics)'],
        'acesulfame': ['EU (labelling required)', 'Several countries (ADI limits)'],
        'aspartame': ['EU (phenylketonuria warning)', 'Some countries (quantity restricted)'],
    }

    # Check all known patterns
    for key, countries in bans.items():
        if key in ingredient_lower:
            return countries

    # Pattern-based checks
    if 'paraben' in ingredient_lower:
        return ['Denmark (children\'s products)', 'EU (concentration restricted)']
    if 'isothiazolinone' in ingredient_lower:
        return ['European Union (restricted/banned in cosmetics)', 'Canada (restricted)']
    if 'nitrite' in ingredient_lower or 'nitrate' in ingredient_lower:
        return ['EU (concentration limits)', 'UK (restricted)']
    if any(x in ingredient_lower for x in ['sunset yellow', 'allura red', 'tartrazine', 'ponceau']):
        return ['EU (warning label required)', 'Norway', 'Finland']

    return []


def get_fssai_position(ingredient_name):
    """Return FSSAI's position on the ingredient"""
    ingredient_lower = ingredient_name.lower()

    positions = {
        'tartrazine': 'Permitted as E102 under FSSAI with concentration limits. Advisory to watch for sensitivity.',
        'sunset yellow': 'Permitted as E110 under FSSAI. Quantity limits apply in food products.',
        'sodium benzoate': 'Permitted as E211 preservative under FSSAI Food Safety and Standards Regulations.',
        'monosodium glutamate': 'Permitted under FSSAI as a flavour enhancer with usage guidelines.',
        'sodium nitrite': 'Permitted in meat products under FSSAI with strict quantity limits.',
        'phosphoric acid': 'Permitted as acidulant E338 under FSSAI in non-alcoholic beverages.',
        'sodium metabisulphite': 'Permitted preservative under FSSAI with mandatory declaration for sulphite content above 10ppm.',
        'methylparaben': 'Permitted in cosmetics under India BIS/CDSCO guidelines with concentration limits.',
        'propylparaben': 'Permitted in cosmetics under India BIS/CDSCO guidelines with concentration limits.',
        'triclosan': 'Permitted in cosmetics and personal care products under Indian regulations.',
        'caramel colour': 'Permitted under FSSAI as colour E150. Class III and IV have usage restrictions.',
        'tbhq': 'Permitted antioxidant under FSSAI with concentration limits in edible oils.',
    }

    for key, pos in positions.items():
        if key in ingredient_lower:
            return pos

    if 'paraben' in ingredient_lower:
        return 'Permitted in cosmetics under India BIS/CDSCO guidelines with concentration limits.'
    if 'color' in ingredient_lower or 'colour' in ingredient_lower:
        return 'Artificial colours must be declared on labels under FSSAI regulations.'
    if 'preservative' in ingredient_lower or 'benzoate' in ingredient_lower or 'sorbate' in ingredient_lower:
        return 'Permitted preservative under FSSAI with quantity limits.'

    return 'Regulated under FSSAI Food Safety and Standards Act, 2006.'


def get_ingredient_details(ingredient_name):
    """Get detailed information about an ingredient"""
    classification_data = classify_ingredient(ingredient_name)

    # Add commonly found in based on ingredient type
    commonly_found_in = get_commonly_found_in(ingredient_name)

    # Add health effects based on classification
    health_effects = get_health_effects(ingredient_name, classification_data['classification'])

    # Countries where restricted/banned
    countries_restricted = get_countries_restricted(ingredient_name)

    # FSSAI position
    fssai_position = get_fssai_position(ingredient_name)

    return {
        'name': ingredient_name,
        'classification': classification_data['classification'],
        'what_it_is': classification_data['what_it_is'],
        'commonly_found_in': commonly_found_in,
        'one_line_note': classification_data['one_line_note'],
        'regulatory_note': classification_data['regulatory_note'],
        'health_effects': health_effects,
        'countries_restricted': countries_restricted,
        'fssai_position': fssai_position,
    }


def get_commonly_found_in(ingredient_name):
    """Return common products containing this ingredient"""
    ingredient_lower = ingredient_name.lower()
    
    # Preservatives
    if any(x in ingredient_lower for x in ['benzoate', 'sorbate', 'sulfite', 'metabisulphite']):
        return 'Soft drinks, pickles, dried fruits, processed foods'
    
    # Colors
    if any(x in ingredient_lower for x in ['tartrazine', 'sunset', 'allura', 'brilliant', 'color', 'colour']):
        return 'Candies, soft drinks, desserts, processed foods'
    
    # Flavor enhancers
    if any(x in ingredient_lower for x in ['guanylate', 'inosinate', 'glutamate']):
        return 'Chips, instant noodles, savory snacks, processed foods'
    
    # Sweeteners
    if any(x in ingredient_lower for x in ['sugar', 'syrup', 'sweetener']):
        return 'Beverages, desserts, baked goods, processed foods'
    
    # Oils
    if any(x in ingredient_lower for x in ['oil', 'fat']):
        return 'Fried foods, baked goods, processed snacks'
    
    # Personal care surfactants
    if any(x in ingredient_lower for x in ['sulfate', 'betaine']):
        return 'Shampoos, body washes, cleansers, soaps'
    
    # Emulsifiers
    if any(x in ingredient_lower for x in ['lecithin', 'glyceride', 'emulsifier']):
        return 'Chocolates, baked goods, margarine, processed foods'
    
    return 'Various food and cosmetic products'


def get_health_effects(ingredient_name, classification):
    """Return health effects based on ingredient and classification"""
    ingredient_lower = ingredient_name.lower()
    
    if classification == 'commonly_questioned':
        # Specific health effects for commonly questioned ingredients
        if 'triclosan' in ingredient_lower:
            return {
                'short_term': 'Skin irritation, allergic reactions',
                'long_term': 'Hormone disruption, antibiotic resistance, thyroid issues',
                'vulnerable_groups': 'Pregnant women, children, people with thyroid conditions'
            }
        elif any(x in ingredient_lower for x in ['tartrazine', 'sunset', 'allura', 'ponceau', 'carmoisine']):
            return {
                'short_term': 'Allergic reactions, hives, asthma attacks',
                'long_term': 'Hyperactivity in children, ADHD symptoms, potential carcinogenicity',
                'vulnerable_groups': 'Children, people with asthma, aspirin-sensitive individuals'
            }
        elif 'phosphoric acid' in ingredient_lower:
            return {
                'short_term': 'Tooth enamel erosion, digestive discomfort',
                'long_term': 'Reduced bone density, kidney issues, calcium depletion',
                'vulnerable_groups': 'Children, elderly, people with osteoporosis or kidney disease'
            }
        elif any(x in ingredient_lower for x in ['benzoate', 'metabisulphite', 'sulfite']):
            return {
                'short_term': 'Allergic reactions, asthma attacks, hives',
                'long_term': 'Chronic allergic sensitization, vitamin B1 depletion',
                'vulnerable_groups': 'Asthmatics, people with sulfite sensitivity'
            }
        elif any(x in ingredient_lower for x in ['guanylate', 'inosinate', 'glutamate']):
            return {
                'short_term': 'Headaches, flushing, sweating, numbness',
                'long_term': 'Potential neurotoxicity at high doses',
                'vulnerable_groups': 'MSG-sensitive individuals, children'
            }
        elif 'paraben' in ingredient_lower:
            return {
                'short_term': 'Skin irritation, allergic reactions',
                'long_term': 'Endocrine disruption, reproductive concerns, bioaccumulation',
                'vulnerable_groups': 'Pregnant women, children, people with hormone-sensitive conditions'
            }
        elif any(x in ingredient_lower for x in ['methylchloroisothiazolinone', 'methylisothiazolinone']):
            return {
                'short_term': 'Severe contact dermatitis, skin irritation',
                'long_term': 'Chronic skin sensitization, allergic reactions',
                'vulnerable_groups': 'People with sensitive skin, eczema sufferers'
            }
        else:
            return {
                'short_term': 'May cause allergic reactions or sensitivity',
                'long_term': 'Regulatory concerns or usage restrictions apply',
                'vulnerable_groups': 'Sensitive individuals, children, pregnant women'
            }
    
    elif classification == 'worth_knowing':
        # General health effects for worth knowing ingredients
        if 'sugar' in ingredient_lower or 'syrup' in ingredient_lower:
            return {
                'short_term': 'Blood sugar spikes, energy crashes',
                'long_term': 'Weight gain, diabetes risk, dental cavities',
                'vulnerable_groups': 'Diabetics, children, people with metabolic syndrome'
            }
        elif 'palm oil' in ingredient_lower or 'palmolein' in ingredient_lower:
            return {
                'short_term': 'High calorie content',
                'long_term': 'High saturated fat may increase cholesterol',
                'vulnerable_groups': 'People with heart disease, high cholesterol'
            }
        elif 'sulfate' in ingredient_lower:
            return {
                'short_term': 'Skin and scalp dryness, irritation',
                'long_term': 'Chronic dryness, potential hair damage',
                'vulnerable_groups': 'People with sensitive skin, dry skin, eczema'
            }
        elif 'caffeine' in ingredient_lower:
            return {
                'short_term': 'Jitters, increased heart rate, sleep disruption',
                'long_term': 'Dependency, tolerance, sleep disorders',
                'vulnerable_groups': 'Pregnant women, children, people with anxiety or heart conditions'
            }
        else:
            return {
                'short_term': 'Generally safe with minimal immediate effects',
                'long_term': 'Safe in moderation, consider cumulative exposure',
                'vulnerable_groups': 'May affect sensitive individuals'
            }
    
    else:  # generally_recognised
        return {
            'short_term': 'No known adverse effects',
            'long_term': 'Generally recognised as safe',
            'vulnerable_groups': 'Safe for general population'
        }
