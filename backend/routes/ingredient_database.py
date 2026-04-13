"""
Comprehensive Ingredient Database - Single Source of Truth
This ensures consistency between product search and ingredient check pages
"""

def classify_ingredient(ingredient_name):
    """Classify ingredients based on regulatory and health concerns - SINGLE SOURCE OF TRUTH"""
    ingredient_lower = ingredient_name.lower()
    
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
        'turmeric': ('Natural yellow color', 'Generally safe but high doses may cause digestive upset, iron absorption issues'),
        'paprika': ('Natural red color', 'Generally safe but may cause allergic reactions in sensitive individuals'),
        'beetroot': ('Natural red color', 'Generally safe but may cause red urine/stools (harmless but alarming)'),
        
        # Waxes and glazing agents
        'shellac': ('Glazing agent E904', 'Natural resin from insects, rare allergic reactions, digestive issues'),
        'beeswax': ('Glazing agent E901', 'Generally safe but rare allergic reactions, may cause digestive upset'),
        'carnauba wax': ('Glazing agent E903', 'Generally safe but indigestible, may cause digestive discomfort'),
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


def get_ingredient_details(ingredient_name):
    """Get detailed information about an ingredient"""
    classification_data = classify_ingredient(ingredient_name)
    
    # Add commonly found in based on ingredient type
    commonly_found_in = get_commonly_found_in(ingredient_name)
    
    # Add health effects based on classification
    health_effects = get_health_effects(ingredient_name, classification_data['classification'])
    
    return {
        'name': ingredient_name,
        'classification': classification_data['classification'],
        'what_it_is': classification_data['what_it_is'],
        'commonly_found_in': commonly_found_in,
        'one_line_note': classification_data['one_line_note'],
        'regulatory_note': classification_data['regulatory_note'],
        'health_effects': health_effects
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
