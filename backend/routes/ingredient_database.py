"""
Comprehensive Ingredient Database - Single Source of Truth
This ensures consistency between product search and ingredient check pages
"""

COSMETIC_CATEGORIES = {
    "Skincare", "Hair Care", "Cosmetics", "Personal Care", "Baby Care", "Oral Care", "Household"
}

# Factual "what is it" descriptions shown in the Check Ingredient page
# Keys match the pattern keys in classify_ingredient (lowercased)
INGREDIENT_DESCRIPTIONS = {
    # --- Preservatives ---
    'triclosan': 'An antimicrobial agent first used in hospitals in the 1960s, later added to soaps, toothpastes and body washes. It was one of the most widely used antibacterial additives in consumer products for over 40 years.',
    'triclocarban': 'An antimicrobial compound (TCC) used in bar soaps and personal care products to kill bacteria and fungi. Structurally similar to triclosan, it was a common ingredient in antibacterial bar soaps.',
    'sodium benzoate': 'The sodium salt of benzoic acid (E211), used as a preservative in acidic foods and beverages since the 1900s. It occurs naturally in small amounts in cranberries, prunes and cinnamon.',
    'e211': 'E211 is the EU code for sodium benzoate, a widely used preservative in soft drinks, pickles, condiments and fruit juices that prevents the growth of bacteria, yeast and mould.',
    'sodium metabisulphite': 'A sulfite-based preservative and antioxidant (E223) used to prevent discolouration and bacterial growth in foods, beverages and medicines. Also widely used in winemaking and brewing.',
    'e223': 'E223 is the EU code for sodium metabisulphite, a sulfite preservative used to preserve colour and freshness in dried fruits, wine, fruit juices and processed foods.',
    'sulfur dioxide': 'Sulfur dioxide (E220) is a gaseous preservative and antioxidant used since ancient times to preserve food and wine. It prevents browning and inhibits microbial growth in dried fruits, wine and fruit products.',
    'e220': 'E220 is the EU code for sulfur dioxide, one of the oldest preservatives used in winemaking and food processing to prevent spoilage, oxidation and maintain colour.',
    'sodium nitrite': 'A salt used as a curing agent and colour fixative in processed meats like bacon, ham, hot dogs and sausages. It has been used in meat preservation since the 1920s and prevents the dangerous bacterium Clostridium botulinum.',
    'e250': 'E250 is the EU code for sodium nitrite, the curing salt used in processed meats to prevent botulism, fix the characteristic pink colour and extend shelf life.',
    'sodium nitrate': 'A salt used as a curing agent in preserved meats and a slow-release source of nitrite during the curing process. Also found naturally in many vegetables like spinach, celery and beetroot.',
    'e251': 'E251 is the EU code for sodium nitrate, a curing salt used in processed and preserved meats that converts to nitrite during curing.',
    'methylparaben': 'A paraben ester preservative widely used since the 1920s in cosmetics, pharmaceuticals and foods to prevent mould and bacterial growth. One of the most commonly used preservatives in personal care products worldwide.',
    'propylparaben': 'A longer-chain paraben ester used as a preservative in cosmetics, pharmaceuticals and foods. More potent as an antimicrobial agent than methylparaben but also more closely regulated.',
    'butylparaben': 'The longest-chain of the common parabens, used as a preservative in cosmetics and pharmaceuticals. More potent than shorter-chain parabens but also the most tightly regulated member of the family.',
    'sodium lauryl sulfate': 'A powerful foaming surfactant (SLS) derived from coconut or palm oil, used since the 1930s in shampoos, toothpastes, face washes and household cleaners to create lather and remove oils and dirt.',
    'sodium lauryl sulphate': 'The UK/Australian spelling of sodium lauryl sulfate (SLS), a strong surfactant derived from coconut or palm oil used as a foaming and cleansing agent in shampoos and toothpastes.',
    # --- Artificial colours ---
    'tartrazine': 'A synthetic lemon-yellow azo dye (E102) used to colour foods, drinks, medicines and cosmetics. Derived from petroleum, it produces a vivid yellow and is one of the oldest synthetic food dyes, first used in the 1880s.',
    'e102': 'E102 is the EU code for tartrazine, a synthetic yellow food dye used in sweets, soft drinks, crisps, breakfast cereals and medicines to add a bright yellow colour.',
    'sunset yellow': 'A synthetic orange-yellow azo dye (E110) used to colour foods and beverages. Also called FD&C Yellow 6 in the USA, it was first approved for food use in 1929.',
    'e110': 'E110 is the EU code for Sunset Yellow FCF, a synthetic orange food dye used in snacks, jelly, drinks and medicines. Also known as FD&C Yellow 6 in North America.',
    'allura red': 'A synthetic dark-red azo dye (E129) used to colour foods and beverages. Also called FD&C Red 40, it is the most widely used red food dye in the United States and was approved in 1971.',
    'red 40': 'Red 40 (Allura Red / E129) is a synthetic dark-red azo dye used to colour sweets, drinks, cereals and snack foods. It is the most widely used food dye in the USA.',
    'e129': 'E129 is the EU code for Allura Red AC, a synthetic red food dye used in sweets, soft drinks and snacks. Known as Red 40 or FD&C Red 40 in North America.',
    'ponceau 4r': 'A synthetic red azo dye (E124) used to add red or pink colour to foods and drinks. Also known as Cochineal Red A, it has been used in food since the early 20th century.',
    'e124': 'E124 is the EU code for Ponceau 4R (Cochineal Red A), a synthetic red food dye used in strawberry desserts, tinned cherries and some fizzy drinks.',
    'carmoisine': 'A synthetic red azo dye (E122) also known as Azorubine, used to colour jams, jellies, desserts and alcoholic drinks with a deep reddish-crimson shade.',
    'e122': 'E122 is the EU code for Carmoisine (Azorubine), a synthetic crimson-red food dye used in sweets, jellies, soft drinks and some medicines.',
    'brilliant blue': 'A synthetic blue triphenylmethane dye (E133) used to colour foods, drinks, cosmetics and medicines. Also known as FD&C Blue 1, it has been approved for food use in the USA since 1929.',
    'e133': 'E133 is the EU code for Brilliant Blue FCF (FD&C Blue 1), a synthetic blue food and cosmetic dye used in sweets, ice cream, cereals and sports drinks.',
    'indigo carmine': 'A synthetic blue dye (E132) based on the indigo structure, used to colour foods, medicines and surgical marking. Also known as FD&C Blue 2, it was one of the first synthetic dyes approved for food.',
    'e132': 'E132 is the EU code for Indigo Carmine (FD&C Blue 2), a synthetic blue food dye used in confectionery, pharmaceuticals and as a diagnostic dye in medicine.',
    'erythrosine': 'A synthetic cherry-red dye (E127) based on fluorescein, used to colour maraschino cherries, tinned strawberries, some confectionery and medicines. Also known as FD&C Red 3.',
    'e127': 'E127 is the EU code for Erythrosine (FD&C Red 3), a synthetic pink food dye used in cocktail cherries, canned fruit and pharmaceutical tablets.',
    'quinoline yellow': 'A synthetic yellow dye (E104) used to colour foods, medicines and cosmetics with a dull yellow or greenish-yellow shade. Produced from coal tar derivatives.',
    'e104': 'E104 is the EU code for Quinoline Yellow, a synthetic yellow food and pharmaceutical dye used to give medicines and some foods a distinctive yellow-green shade.',
    'brown ht': 'A synthetic brown azo dye (E155) used to colour chocolate-flavoured products like cakes, biscuits, desserts and drinks with a warm brown hue.',
    'e155': 'E155 is the EU code for Brown HT, a synthetic food dye used to colour chocolate cakes, biscuits and desserts. The HT stands for "high temperature" stability.',
    'patent blue v': 'A synthetic blue dye (E131) used to colour foods, drinks and medicines with a bright blue or violet shade. Also used as a lymphatic tracer in sentinel lymph node biopsies.',
    'e131': 'E131 is the EU code for Patent Blue V, a synthetic triarylmethane dye used in food, pharmaceutical and cosmetic applications as a blue colorant.',
    'azorubine': 'A synthetic crimson-red azo dye (E122) also called Carmoisine, used to colour jams, jellies, alcoholic beverages and other products with a deep red shade.',
    'e951': 'E951 is the EU code for aspartame, an artificial sweetener approximately 200 times sweeter than sugar, widely used in diet drinks, chewing gum and sugar-free foods since FDA approval in 1981.',
    'e950': 'E950 is the EU code for acesulfame potassium (Ace-K), an artificial sweetener about 200 times sweeter than sugar, commonly blended with aspartame in diet beverages and sugar-free products.',
    # --- Flavor enhancers ---
    'disodium guanylate': 'A flavour enhancer (E627) made from dried fish or seaweed, used to intensify savoury umami flavours in processed foods. Almost always used in combination with MSG and disodium inosinate.',
    'e627': 'E627 is the EU code for disodium guanylate, a nucleotide-based flavour enhancer extracted from dried fish or yeast that amplifies the savoury taste of foods.',
    'disodium inosinate': 'A flavour enhancer (E631) derived from meat or fish, used to boost the savoury umami taste in soups, crisps and instant noodles. Typically used alongside MSG and disodium guanylate.',
    'e631': 'E631 is the EU code for disodium inosinate, a nucleotide flavour enhancer derived from meat or sardines, commonly found in instant noodles, crisps and savoury snacks.',
    # --- Acids ---
    'phosphoric acid': 'E338 is the E number for phosphoric acid, a common inorganic acidulant used in the food industry to add a sharp, sour or tangy taste to cola drinks and processed foods. It also acts as a pH regulator and flavour balancer.',
    'e338': 'E338 is the EU code for phosphoric acid, an inorganic acid used as an acidulant, pH regulator and flavour agent in cola beverages, processed cheese and baked goods.',
    'caramel colour': 'A brown food colouring (E150) produced by controlled heating of carbohydrates like sugar or corn syrup. One of the oldest and most widely used food colourings in the world, used in cola drinks, beer, soy sauce and baked goods.',
    'caramel color': 'A brown food colouring (E150) made by heating sugars under controlled conditions, used to give cola beverages, beer and many sauces their characteristic brown colour.',
    'e150': 'E150 is the EU code for caramel colouring, one of the most widely produced food additives globally, made by heating carbohydrates and used in cola drinks, beer, biscuits, bread and soy sauce.',
    # --- Personal care preservatives ---
    'methylchloroisothiazolinone': 'A synthetic preservative (MCI/CMIT) used in rinse-off personal care products like shampoos, conditioners and body washes to prevent microbial growth. Usually paired with methylisothiazolinone (MIT).',
    'methylisothiazolinone': 'A synthetic preservative (MI/MIT) used in personal care products and household cleaners to prevent mould and bacterial contamination. Part of the isothiazolinone family of biocides, first introduced in the 1970s.',
    'dmdm hydantoin': 'A synthetic preservative used in cosmetics and personal care products that works by slowly releasing small amounts of formaldehyde to prevent bacterial and fungal growth.',
    'imidazolidinyl urea': 'A synthetic preservative widely used in cosmetics and personal care products since the 1950s. It releases formaldehyde gradually, providing broad-spectrum antimicrobial protection.',
    'diazolidinyl urea': 'A synthetic preservative derived from allantoin, used in cosmetics and personal care products. It releases formaldehyde over time to prevent microbial contamination.',
    'quaternium-15': 'A synthetic quaternary ammonium preservative used in cosmetics, shampoos and skincare products. It is one of the most commonly used formaldehyde-releasing preservatives in personal care.',
    'phenyl mercuric': 'A mercury-containing compound historically used as a preservative in eye drops, nasal sprays and some topical preparations. Now largely phased out due to toxicity concerns.',
    'formaldehyde': 'A simple aldehyde (CH₂O) naturally produced in small amounts by all living organisms. Industrially used as a preservative, disinfectant and in the production of resins and plastics.',
    'bronopol': 'A synthetic broad-spectrum preservative (2-bromo-2-nitropropane-1,3-diol) used in personal care products, cosmetics and industrial water systems to prevent bacterial and fungal growth.',
    # --- Sweeteners ---
    'aspartame': 'An artificial sweetener approximately 200 times sweeter than sugar, made from two amino acids (aspartic acid and phenylalanine). Used in diet drinks, chewing gum, sugar-free foods and medicines since FDA approval in 1981.',
    'acesulfame potassium': 'An artificial sweetener (Ace-K / E950) about 200 times sweeter than sucrose, often blended with aspartame to improve taste in diet beverages and sugar-free products. Passes through the body without being metabolised.',
    'acesulfame-k': 'Acesulfame-K (E950) is an artificial sweetener about 200 times sweeter than sugar. Widely used in diet drinks, sugar-free sweets and pharmaceuticals since the 1980s.',
    # --- Antioxidant preservatives ---
    'butylated hydroxyanisole': 'BHA is a synthetic antioxidant preservative approved since the 1940s, added to edible fats, snack foods, cereals and cosmetics to prevent oxidation and extend shelf life.',
    'bha': 'BHA (butylated hydroxyanisole) is a synthetic antioxidant added to fatty foods, snack packaging, cereals and cosmetics to prevent oils from going rancid.',
    'butylated hydroxytoluene': 'BHT is a synthetic antioxidant preservative used in fats, oils, cereals and packaged foods to prevent oxidative rancidity and extend shelf life. Chemically similar to BHA.',
    'bht': 'BHT (butylated hydroxytoluene) is a synthetic phenolic antioxidant used to stabilise fats and oils in packaged foods, cosmetics and rubber products.',
    'tert-butylhydroquinone': 'TBHQ is a synthetic antioxidant used in edible fats and oils, instant noodles, chips and packaged goods to prevent oxidation. Commonly used in fast-food frying oils.',
    'tbhq': 'TBHQ (tert-butylhydroquinone) is a synthetic antioxidant preservative found in cooking oils, chips, instant noodles and crackers to slow rancidity and extend shelf life.',
    # --- Banned additives ---
    'potassium bromate': 'A bread-improving oxidising agent that strengthens dough and produces a consistent, high-rising loaf. Used in commercial baking since the early 20th century.',
    'azodicarbonamide': 'A synthetic dough conditioner and bleaching agent used in the baking industry to improve flour performance, speed bread rising and create a fine, consistent crumb texture.',
    'brominated vegetable oil': 'An emulsifier made by reacting bromine with vegetable oil, used to keep citrus flavour oils suspended in water-based soft drinks and sports beverages.',
    # --- Talc ---
    'talcum': 'Talcum is a finely ground mineral powder (hydrated magnesium silicate) derived from natural talc deposits. Used in baby powders, cosmetics, pharmaceuticals and industrial applications for its absorbent and lubricating properties.',
    'talc': 'Talc is a naturally occurring clay mineral (magnesium silicate) mined worldwide. Ground into a fine powder, it is used as a filler, lubricant and anti-caking agent in cosmetics, food supplements and pharmaceuticals.',
    # --- CI colorants (commonly questioned) ---
    'ci 47000': 'CI 47000 is the Colour Index number for Quinoline Yellow (E104), a synthetic yellow azo dye used in food products, pharmaceuticals and some cosmetics.',
    'ci 19140': 'CI 19140 is the Colour Index number for Tartrazine (E102), a synthetic lemon-yellow food dye widely used in sweets, drinks and medicines.',
    'ci 15985': 'CI 15985 is the Colour Index number for Sunset Yellow FCF (E110), a synthetic orange food dye used in snacks, drinks and confectionery.',
    'ci 16035': 'CI 16035 is the Colour Index number for Allura Red AC (E129 / Red 40), a widely used synthetic red food dye in beverages and confectionery.',
    'ci 42090': 'CI 42090 is the Colour Index number for Brilliant Blue FCF (E133 / FD&C Blue 1), a synthetic blue dye used in food and cosmetics.',
    # --- Sugars and sweeteners ---
    'sugar': 'Sucrose extracted from sugar cane or sugar beet, the most widely consumed sweetener in the world. A simple carbohydrate that provides 4 calories per gram and has been used in food for thousands of years.',
    'high fructose corn syrup': 'A liquid sweetener made by enzymatically converting glucose in corn starch to fructose. Developed in the 1960s and widely used in North American soft drinks, condiments and processed foods from the 1970s onwards.',
    'glucose syrup': 'A refined liquid sweetener produced by hydrolysing starch (from corn, wheat or potato) into shorter glucose chains. Used in confectionery, baked goods and soft drinks to add sweetness, moisture retention and smooth texture.',
    'invert sugar': 'A mixture of equal parts glucose and fructose produced by splitting sucrose molecules, used in confectionery and baking to retain moisture, improve texture and prevent sugar crystallisation.',
    'maltodextrin': 'A refined carbohydrate powder produced from starch (corn, wheat or potato) by partial hydrolysis. Used as a filler, thickener, texture agent and carrier in protein powders, sauces, infant formula and processed foods.',
    'corn syrup solids': 'Dried glucose syrup made from corn starch, with most of the water removed. Used as a sweetener, filler and texturiser in creamers, infant formula and processed foods.',
    # --- Sweeteners (moderate) ---
    'sucralose': 'A zero-calorie artificial sweetener (E955) made by selectively chlorinating sugar molecules, approximately 600 times sweeter than sucrose. Discovered in 1976 and used widely in diet drinks, sugar-free products and baked goods.',
    'e955': 'E955 is the EU code for sucralose, a zero-calorie artificial sweetener about 600 times sweeter than table sugar, used in diet drinks, sugar-free sweets and baked goods.',
    'saccharin': 'The oldest artificial sweetener, first discovered in 1879. About 300–400 times sweeter than sugar with no caloric value, used in diet soft drinks, tabletop sweeteners and pharmaceutical preparations.',
    'e954': 'E954 is the EU code for saccharin, the world\'s first artificial sweetener (discovered 1879), used in diet soft drinks, sugar-free confectionery and pharmaceutical products.',
    # --- Fragrance ---
    'fragrance': 'A complex proprietary mixture of aromatic chemicals used to give personal care products their distinctive scent. A single "fragrance" entry on a label may represent dozens or even hundreds of individual chemical ingredients.',
    'perfume': 'A mixture of natural and synthetic aromatic compounds used to create a pleasant scent, listed as a single ingredient to protect proprietary formulas. May contain essential oils, synthetic musks and fixatives.',
    'parfum': 'The French/EU INCI term for fragrance in cosmetics. Under EU Regulation, 26 specific fragrance allergens found within a parfum mixture must be individually declared on the label.',
    'artificial flavor': 'A synthetic flavour compound created in a laboratory to replicate or enhance specific natural tastes. Used widely in processed foods, drinks and confectionery to deliver consistent flavour at lower cost.',
    'artificial flavour': 'A synthetically produced flavouring agent used in processed food products to add or enhance taste. Used in snacks, drinks, confectionery and instant foods for flavour consistency.',
    # --- MSG ---
    'monosodium glutamate': 'The sodium salt of glutamic acid (E621), an amino acid that occurs naturally in tomatoes, parmesan, mushrooms and fermented foods. Used as a flavour enhancer to intensify savoury umami taste, discovered in Japan in 1908.',
    'msg': 'MSG (monosodium glutamate / E621) is a flavour enhancer and the sodium salt of glutamic acid, an amino acid naturally present in tomatoes, aged cheese and mushrooms. Produced commercially by fermenting plant starch or sugar.',
    'e621': 'E621 is the EU code for monosodium glutamate (MSG), a flavour enhancer produced by fermentation of starch or sugar that amplifies the savoury umami taste in foods.',
    # --- Fiber additives ---
    'inulin': 'A naturally occurring prebiotic dietary fibre extracted from chicory root, Jerusalem artichoke or agave. Used as a fat replacer, texture agent and probiotic supplement in yoghurts, baked goods and protein bars.',
    'polydextrose': 'A synthetic soluble fibre (E1200) made from glucose by polymerisation. Used as a low-calorie bulking agent and fat replacer in reduced-calorie foods like baked goods, dairy products and sweets.',
    # --- Oils and fats ---
    'palm oil': 'A vegetable oil extracted from the fruit of the oil palm tree (Elaeis guineensis), originating from West Africa. One of the most widely produced vegetable oils in the world, used in frying, baking, margarine and a vast range of packaged foods.',
    'palmolein': 'The liquid fraction of palm oil separated by fractional crystallisation. Widely used as a cooking and frying oil in tropical countries and in the manufacture of packaged foods.',
    'hydrogenated': 'A fat produced by adding hydrogen to liquid vegetable oil under pressure, turning it solid or semi-solid at room temperature. Used to improve texture, spreadability and shelf life in margarine, biscuits and baked goods.',
    'partially hydrogenated': 'A fat produced by the incomplete hydrogenation of liquid vegetable oils, resulting in a semi-solid fat with a long shelf life. The hydrogenation process creates trans fatty acids as a by-product.',
    # --- Emulsifiers and stabilizers ---
    'soy lecithin': 'A natural emulsifier (E322) extracted from soybean oil during processing. Widely used in chocolate, bread, margarine and baked goods to blend fats and water smoothly and improve texture.',
    'mono and diglycerides': 'Emulsifiers (E471) made from glycerol combined with one or two fatty acids. Found in baked goods, margarine and dairy products to improve texture, extend freshness and help fats and water mix.',
    'polyglycerol polyricinoleate': 'A synthetic emulsifier (E476) made from glycerol and castor bean oil (ricinoleic acid), used primarily in chocolate manufacturing to improve flow properties and reduce the amount of cocoa butter needed.',
    'ammonium phosphatides': 'An emulsifier (E442) derived from rapeseed oil, used in chocolate and cocoa products as an alternative to soy lecithin to improve texture and consistency.',
    'carrageenan': 'A natural thickener and gelling agent (E407) extracted from red edible seaweed, used for over 600 years in food preparation. Widely used in dairy products, plant milks, deli meats and infant formula to improve texture.',
    # --- Surfactants (personal care) ---
    'sodium laureth sulfate': 'A milder sulfate surfactant (SLES) derived from coconut or palm oil, created by ethoxylating SLS to reduce its irritation potential. Used in shampoos, body washes and skin cleansers as a foaming agent.',
    'sodium laureth sulphate': 'The sulphate spelling variant of SLES (sodium laureth sulfate), a widely used foaming surfactant in shampoos, shower gels and skin cleansers.',
    'ammonium laureth sulfate': 'An ammonium-based sulfate surfactant similar to SLES, used in shampoos and body washes as a foaming and cleansing agent. Slightly different pH profile to its sodium counterpart.',
    'cocamidopropyl betaine': 'A mild amphoteric surfactant derived from coconut oil, used in shampoos, body washes and baby products. Added to reduce irritation from stronger surfactants and to improve conditioning and lather.',
    # --- Preservatives (milder) ---
    'phenoxyethanol': 'A synthetic preservative and solvent used in cosmetics and pharmaceuticals since the 1950s to prevent microbial growth. Found in skincare, haircare, eye cosmetics and baby products.',
    'benzyl alcohol': 'A naturally occurring aromatic alcohol found in jasmine, hyacinth and ylang-ylang, also produced synthetically. Used as a preservative, solvent and fragrance ingredient in cosmetics and pharmaceuticals.',
    'potassium sorbate': 'The potassium salt of sorbic acid (E202), a natural preservative originally isolated from rowan berries. Used to inhibit mould and yeast in cheese, wine, dried fruits, baked goods and cosmetics.',
    'e202': 'E202 is the EU code for potassium sorbate, a widely used food and cosmetic preservative that inhibits the growth of mould, yeast and some bacteria at low concentrations.',
    'e407': 'E407 is the EU code for carrageenan, a natural thickener and stabiliser extracted from red seaweed, used in dairy products, meat products and plant-based alternatives.',
    # --- Petroleum-derived ---
    'mineral oil': 'A highly refined petroleum-derived oil used as a moisturiser and emollient in cosmetics and as a laxative in medicines. Also used as a food-grade lubricant on processing machinery and as a coating on some foods.',
    'petrolatum': 'Petroleum jelly (e.g., Vaseline), a semi-solid mixture of hydrocarbons refined from petroleum. Used as a skin protectant and occlusive moisturiser since 1872 and as a base for ointments.',
    'paraffinum liquidum': 'The INCI name for liquid paraffin or white mineral oil, a highly refined petroleum-derived ingredient used as an emollient and skin-conditioning agent in cosmetics and as a laxative.',
    'paraffin wax': 'A petroleum-derived solid wax used as a coating and glazing agent in food (E905) and as an occlusive ingredient in cosmetics. Also widely used in candles and as a waterproofing material.',
    # --- PEG compounds ---
    'peg-': 'PEG (polyethylene glycol) compounds are petroleum-derived polymers used as emollients, emulsifiers, thickeners and surfactants in cosmetics and pharmaceuticals. The number after PEG indicates the average molecular weight.',
    'polyethylene glycol': 'A synthetic polymer made from ethylene oxide, used as a solvent, emollient, thickener and penetration enhancer in cosmetics, pharmaceuticals and industrial products.',
    # --- Denatured alcohols ---
    'alcohol denat': 'Denatured ethyl alcohol with bittering or denaturing agents added to make it unfit for drinking. Used as a solvent, antiseptic and quick-drying carrier in cosmetics, toiletries and household products.',
    'denatured alcohol': 'Ethanol made undrinkable by adding denaturants such as denatonium. Used widely as a solvent, astringent and preservative in cosmetics, skin toners, antiseptics and cleaning products.',
    'sd alcohol': 'Specially denatured (SD) alcohol, a form of denatured ethanol approved for specific industrial and cosmetic uses. Functions as a solvent, antiseptic and quick-drying ingredient in personal care products.',
    # --- Allergens ---
    'lanolin': 'A natural waxy substance produced by the sebaceous glands of wool-bearing animals, mainly sheep. Extracted during wool processing, it is used as a skin softener and emollient in lip balms, creams and nipple creams.',
    'wool wax': 'Another name for lanolin, the natural secretion produced by sheep to waterproof their wool. Used in cosmetics, ointments, leather conditioners and industrial lubricants.',
    # --- Silicones (cyclic) ---
    'cyclomethicone': 'A blend of cyclic silicone compounds (typically D4, D5 and D6) used in cosmetics as a lightweight, volatile carrier. Found in hair products, moisturisers and deodorants, it evaporates after application leaving other ingredients behind.',
    'cyclopentasiloxane': 'A cyclic silicone (D5) widely used in haircare and skincare as a lightweight conditioning agent that evaporates after application, leaving no residue and imparting silky smoothness.',
    'cyclohexasiloxane': 'A cyclic silicone (D6) used in personal care products as a lightweight emollient and carrier ingredient that evaporates quickly after application.',
    'amodimethicone': 'A modified silicone polymer with reactive amino groups, used in hair conditioners and treatments to provide slip, reduce frizz and deposit evenly on damaged areas of the hair shaft.',
    # --- Retinoids ---
    'retinol': 'The alcohol form of Vitamin A (a retinoid), used in anti-ageing skincare since the 1980s to increase cell turnover, stimulate collagen production and improve fine lines, wrinkles and uneven skin tone.',
    'retinyl palmitate': 'An ester of retinol (Vitamin A) and palmitic acid, used as a milder retinoid in cosmetics and as a Vitamin A supplement and antioxidant in skincare and some food products.',
    'tretinoin': 'The acid form of Vitamin A (all-trans retinoic acid), a prescription-only topical retinoid used to treat acne, photodamage and wrinkles. Regarded as the gold standard topical anti-ageing agent.',
    'hydroxypinacolone retinoate': 'A newer ester of retinoic acid used in over-the-counter cosmetics as a gentler alternative to retinol, designed to deliver anti-ageing benefits with reportedly less irritation and dryness.',
    'retinal': 'Retinaldehyde, an intermediate form of Vitamin A between retinol and retinoic acid, used in high-performance anti-ageing skincare. Converts to retinoic acid on the skin more readily than retinol.',
    # --- Silicones ---
    'dimethiconol': 'A high-molecular-weight silicone polymer used in hair conditioners and styling products to add shine, smooth the cuticle and improve detangling. Unlike cyclic silicones, it is non-volatile and remains on the hair.',
    'dimethicone': 'The most widely used silicone in cosmetics, a linear polydimethylsiloxane polymer. Creates a smooth, silky feel on skin and hair, acts as a skin protectant and is used in everything from moisturisers to wound dressings.',
    # --- CI cosmetic colorants (worth knowing) ---
    'ci 26100': 'CI 26100 (Solvent Red 23 / D&C Red No. 17) is a synthetic azo dye used to add red colour to cosmetics such as lipsticks, nail polish and hair products.',
    'ci 61565': 'CI 61565 (Vat Green 1) is a synthetic vat dye used to impart green colour in some cosmetics and textile dyeing applications.',
    'ci 17200': 'CI 17200 (Acid Red 33 / D&C Red No. 33) is a synthetic azo dye used to colour cosmetics and pharmaceutical products red.',
    'ci 15510': 'CI 15510 (Acid Orange 7) is a synthetic azo dye used in cosmetics, hair dyes and pharmaceutical colouring applications.',
    'ci 45410': 'CI 45410 (Acid Red 92 / D&C Red No. 27) is a synthetic fluorescein dye used to add red or pink colour to lip products and other cosmetics.',
    # --- Titanium Dioxide ---
    'titanium dioxide': 'A naturally occurring white mineral (E171) mined from ilmenite or rutile ore. Used as a bright white pigment in paints, sunscreens, toothpastes, tablets and food products since the early 20th century.',
    # --- Chelating agents ---
    'tetrasodium edta': 'A synthetic chelating agent (a tetrasodium salt of EDTA) used in cosmetics, pharmaceuticals and food products to bind and inactivate trace metal ions that could otherwise cause discolouration or product degradation.',
    'disodium edta': 'A synthetic chelating agent used in cosmetics, shampoos and food products to sequester metal ions (like calcium and magnesium) that could interfere with product performance or cause oxidation.',
    'tetrasodium etidronate': 'A chelating and sequestering agent used as an alternative to EDTA in cosmetic formulations, particularly in rinse-off products and oral care, to improve product stability.',
    # --- Mild acids ---
    'citric acid': 'A naturally occurring weak organic acid found abundantly in citrus fruits, produced commercially by fermenting sugars. Widely used as an acidulant, flavour enhancer, pH adjuster and preservative in foods, drinks and cosmetics.',
    # --- Colorants ---
    'beta carotene': 'A naturally occurring orange-red pigment (provitamin A / E160a) found in carrots, sweet potatoes and leafy greens. Used as a food colorant and as a precursor that the body converts to Vitamin A.',
    'caramel': 'A natural brown colouring and flavouring produced by heating sugar. The word caramel refers both to the confectionery and to the flavour/colour ingredient used in biscuits, beverages and desserts.',
    # --- Thickeners ---
    'guar gum': 'A natural thickener and emulsifier (E412) ground from the endosperm of guar beans, grown primarily in India and Pakistan. Widely used in ice cream, dairy products, sauces and gluten-free baked goods.',
    'xanthan gum': 'A natural polysaccharide (E415) produced by fermenting glucose with the bacterium Xanthomonas campestris. Used as a thickener and stabiliser in salad dressings, sauces, gluten-free bread and cosmetics.',
    # --- Humectants ---
    'propylene glycol': 'A synthetic, odourless viscous liquid derived from petroleum or bio-based sources. Used as a humectant, solvent and stabiliser in food, cosmetics, pharmaceuticals and as an aircraft de-icing fluid.',
    'glycerin': 'Also known as glycerol, a naturally occurring compound found in all plant and animal fats. A versatile ingredient used as a humectant, sweetener and solvent in foods, cosmetics and medicines for over 150 years.',
    'sorbitol': 'A naturally occurring sugar alcohol found in apples, pears and plums, also produced commercially from glucose. Used as a low-calorie sweetener, humectant and laxative in foods, cosmetics and pharmaceutical preparations.',
    # --- Caffeine ---
    'caffeine': 'A natural alkaloid stimulant found in coffee beans, tea leaves, cacao pods and guarana berries, and also produced synthetically. The world\'s most widely consumed psychoactive substance, used in beverages, medicines and topical cosmetics.',
    # --- Alcohol ---
    'alcohol': 'Ethyl alcohol (ethanol), a short-chain alcohol produced by fermentation of sugars. Used across industries as a solvent, preservative, antiseptic and carrier in cosmetics, medicines and cleaning products.',
    'ethanol': 'The chemical name for drinking alcohol, produced by fermentation of plant sugars. In cosmetics and personal care products, it is usually denatured (made undrinkable) and used as a solvent, antiseptic and quick-drying carrier.',
    # --- Salts ---
    'salt': 'Sodium chloride (NaCl), an essential mineral found in seawater and rock deposits. The most widely used food seasoning and preservative in human history, essential for nerve function and fluid balance.',
    'sodium chloride': 'The chemical compound commonly known as table salt, consisting of sodium and chloride ions. An essential dietary mineral used as a seasoning, preservative and ingredient in thousands of food, cosmetic and pharmaceutical products.',
    # --- Acids (milder) ---
    'lactic acid': 'An organic acid naturally produced during fermentation (in yoghurt, cheese, sauerkraut) and by muscles during exercise. Used as a preservative, acidulant and pH adjuster in foods, beverages and skincare products.',
    'malic acid': 'A naturally occurring organic acid found abundantly in apples, pears and other fruits. Used as a flavour enhancer, acidulant and pH balancer in foods, beverages and oral care products.',
    # --- Vitamins ---
    'ascorbic acid': 'The chemical name for Vitamin C, an essential water-soluble vitamin found in citrus fruits, berries and vegetables. Used as a nutritional supplement, antioxidant preservative and skin-brightening agent in foods and cosmetics.',
    'tocopherol': 'The chemical name for Vitamin E, a fat-soluble antioxidant found in nuts, seeds and vegetable oils. Used as a natural antioxidant preservative and skin-conditioning ingredient in foods, cosmetics and supplements.',
    'vitamin': 'An essential organic micronutrient that the body requires in small amounts. Added to food products for fortification, to replace vitamins lost during processing or to supplement dietary intake.',
    'mineral': 'An inorganic element required by the body in small amounts for functions including bone formation, enzyme activity and fluid regulation. Added to foods for fortification purposes.',
    # --- Proteins ---
    'whey': 'The liquid portion of milk that separates during cheese-making, containing whey proteins (beta-lactoglobulin, alpha-lactalbumin). Dried into whey powder and widely used as a protein supplement and in baked goods.',
    'casein': 'The dominant protein in cow\'s milk, making up about 80% of total milk protein. Used as a slow-digesting protein supplement and as a food ingredient in processed cheese, adhesives and pharmaceutical tablets.',
    'lactose': 'The natural disaccharide sugar found in milk and dairy products, composed of glucose and galactose. Widely used as a filler, binder and mild sweetener in pharmaceuticals and processed foods.',
    # --- Starches ---
    'starch': 'A natural carbohydrate polymer (polysaccharide) found in wheat, maize, potato and rice. The most widely used thickening and texturising agent in processed foods worldwide.',
    'modified starch': 'Starch that has been chemically or physically treated (e.g., by cross-linking or acetylation) to improve its functional properties such as stability under heat, acid or freezing.',
    # --- Raising agents ---
    'sodium bicarbonate': 'Also known as baking soda (E500), a naturally occurring white crystalline mineral that produces carbon dioxide gas when combined with acid or heat, used as a leavening agent in baking.',
    'ammonium bicarbonate': 'A raising agent (E503) used in baking that decomposes completely during baking into ammonia, carbon dioxide and water, leaving no residue in the finished product.',
    'sodium carbonate': 'A raising agent and pH adjuster (E500ii) also known as washing soda, used in baked goods, noodles and as a food-grade alkali to adjust acidity.',
    'potassium carbonate': 'A raising agent (E501) and pH adjuster used in baked goods, cocoa processing and some Asian noodles to improve texture and alkalinity.',
    # --- Anticaking ---
    'silicon dioxide': 'A naturally occurring mineral (E551) that occurs as quartz sand and diatomite. Purified to a fine powder, it is used as an anticaking agent to prevent clumping in powdered foods, spices, salt and nutritional supplements.',
    # --- Flavor enhancers (natural) ---
    'yeast extract': 'A concentrated paste or powder made from the cellular contents of yeast, rich in amino acids, B vitamins and natural glutamates. Used as a savoury, umami-rich flavour enhancer in soups, sauces, stocks and snack foods.',
    'hydrolysed': 'A protein that has been broken down into amino acids and shorter peptide chains by hydrolysis using acid, base or enzymes. Used as a natural-source flavour enhancer in soups, sauces and processed meat products.',
    # --- Natural colorants ---
    'annatto': 'A natural orange-yellow food colouring (E160b) extracted from the seeds of the achiote tree (Bixa orellana), native to tropical America. Used for centuries to colour cheeses like Red Leicester, butter, rice dishes and snacks.',
    'paprika': 'A spice and natural food colorant made from dried and ground red peppers (Capsicum annuum). Used both for its warm, slightly sweet flavour and as a natural red-orange colouring agent in foods.',
    'beetroot': 'A natural red-purple food colorant extracted from the juice of red beets (Beta vulgaris). Used to colour juices, jams, meat products, confectionery and some cosmetics.',
    # --- Waxes ---
    'shellac': 'A natural resin secreted by the female lac bug (Kerria lacca) on trees in India and Thailand. Used as a glazing agent (E904) on confectionery, fresh fruit and pharmaceutical tablets to add shine and reduce moisture loss.',
    'beeswax': 'A natural wax produced by honey bees to build honeycomb. Used as a glazing and coating agent (E901) in confectionery and cheese, and widely used in cosmetics as a thickener, emulsifier and emollient.',
    'carnauba wax': 'A natural wax obtained from the leaves of the carnauba palm tree (Copernicia prunifera) in Brazil. The hardest natural wax available, used as a glazing agent (E903) in confectionery, cosmetics and car polish.',
    # --- Herbal / generally recognised ---
    'neem': 'An extract from the neem tree (Azadirachta indica), an evergreen native to the Indian subcontinent. Used for thousands of years in Ayurvedic medicine, today found in soaps, shampoos, toothpastes and skincare products.',
    'neem extract': 'A concentrated extract from the neem tree (Azadirachta indica), prized in Ayurvedic practice for its antimicrobial and antifungal properties. Used in personal care and oral care products.',
    'neem oil': 'A cold-pressed vegetable oil extracted from the fruits and seeds of the neem tree. Used in Ayurvedic medicine, agriculture and personal care products for its antibacterial, antifungal and insecticidal properties.',
    'tulsi': 'Holy basil (Ocimum tenuiflorum), a plant sacred in Hinduism and a cornerstone of Ayurvedic medicine for over 3,000 years. Used in herbal teas, supplements and personal care products for its adaptogenic and antimicrobial properties.',
    'aloe vera': 'A succulent plant native to the Arabian Peninsula, used medicinally for over 6,000 years. The clear gel from its leaves is used in skincare, cosmetics, beverages and medicines for its soothing and moisturising properties.',
    'aloe': 'Extract from the aloe vera plant (Aloe barbadensis miller), used in skincare and haircare products for its soothing, moisturising and wound-healing properties.',
    'turmeric extract': 'A concentrated extract of turmeric root (Curcuma longa) standardised for curcumin, the primary active polyphenol. Used in dietary supplements and functional foods for its anti-inflammatory properties.',
    'turmeric': 'A bright yellow spice derived from the rhizome of Curcuma longa, a plant in the ginger family. Cultivated in South Asia for over 4,000 years, used in cooking, traditional medicine and as a natural yellow food colorant.',
    'haldi': 'The Hindi/Urdu name for turmeric (Curcuma longa), a traditional Indian spice used in cooking, Ayurvedic medicine and religious ceremonies.',
    'ashwagandha': 'An Ayurvedic medicinal herb (Withania somnifera), also called Indian ginseng or winter cherry. Used for over 3,000 years in traditional Indian medicine to reduce stress and support vitality.',
    'aloe vera gel': 'The translucent gel extracted from inside the leaves of the aloe vera plant. Widely used in skincare and hair products for its hydrating, soothing and cooling properties.',
    'coconut oil': 'A natural plant oil extracted from the kernel of mature coconuts. One of the most widely used plant oils, prized for its high lauric acid content and used in cooking, cosmetics and haircare.',
    'olive oil': 'A natural oil extracted from the fruit of the olive tree (Olea europaea), a staple of Mediterranean cuisine for millennia. Rich in oleic acid and polyphenol antioxidants, used in cooking and cosmetics.',
    'honey': 'A natural viscous sweetener produced by bees from flower nectar. Composed primarily of fructose and glucose, honey has been used as food, medicine and a cosmetic ingredient for thousands of years.',
    'salicylic acid': 'A naturally occurring beta hydroxy acid (BHA) found in willow bark and other plants. Used as a keratolytic and acne treatment in skincare and as a food preservative in some applications.',
    'hyaluronic acid': 'A natural polysaccharide (glycosaminoglycan) found in the skin, eyes and joint fluid of all vertebrates. Used extensively in skincare for its exceptional ability to bind and retain moisture.',
    'ceramide': 'A class of lipid molecules that are the primary component of the skin\'s stratum corneum (outer barrier layer). Used in skincare products to reinforce the skin barrier and prevent moisture loss.',
    'collagen': 'The most abundant structural protein in the human body, found in skin, tendons, bones and cartilage. Used in skincare products and dietary supplements for skin elasticity and wound healing.',
    # --- CI iron oxides (generally recognised) ---
    'ci 77491': 'CI 77491 is the Colour Index number for Iron Oxide Red, a naturally occurring mineral pigment widely used in cosmetics, face makeup and some foods as a safe, stable red colourant.',
    'ci 77492': 'CI 77492 is the Colour Index number for Iron Oxide Yellow, a naturally occurring mineral pigment used in cosmetics and some food colourants as a safe yellow or buff colourant.',
    'ci 77499': 'CI 77499 is the Colour Index number for Iron Oxide Black, a naturally occurring mineral pigment used in cosmetics like mascara, eyeliner and nail products as a stable black colourant.',
    'iron oxide': 'Iron oxide is a naturally occurring mineral pigment (rust) that comes in red, yellow and black forms. Approved by FDA and EU as a safe colourant in cosmetics and some food applications.',
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
    # Normalize "CI No. 47000" → "ci 47000", collapse extra spaces
    ingredient_lower = (
        ingredient_name.lower()
        .replace('no.', '')
        .replace('  ', ' ')
        .strip()
    )
    # Compact form strips spaces/hyphens so "Methyl Paraben" matches "methylparaben"
    ingredient_compact = ingredient_lower.replace(' ', '').replace('-', '').replace('/', '')
    is_cosmetic = category in COSMETIC_CATEGORIES
    
    # COMMONLY QUESTIONED INGREDIENTS (RED) - Regulatory concerns, banned substances, health risks
    commonly_questioned_patterns = {
        # Preservatives with serious concerns
        'triclosan': ('Antibacterial agent', 'Hormone disruption, antibiotic resistance, thyroid problems; banned in EU cosmetics; FDA banned from USA hand soaps'),
        'triclocarban': ('Antimicrobial agent TCC', 'Endocrine disruptor; environmental persistence; FDA banned from USA antiseptic products'),
        'sodium benzoate': ('Preservative E211', 'Forms benzene (carcinogen) with vitamin C in acidic drinks; linked to hyperactivity in children; EU/India require label declaration'),
        'e211': ('Sodium benzoate (E211)', 'Forms benzene with vitamin C; hyperactivity link in children; mandatory label declaration in EU'),
        'sodium metabisulphite': ('Sulfite preservative E223', 'Severe allergic reactions, asthma attacks, can cause anaphylaxis; must be declared on labels'),
        'e223': ('Sodium metabisulphite (E223)', 'Severe allergic reactions, asthma attacks; mandatory label declaration as allergen'),
        'sulfur dioxide': ('Preservative E220', 'Destroys vitamin B1, triggers severe asthma attacks, allergic reactions; declared as allergen on labels'),
        'e220': ('Sulfur dioxide (E220)', 'Destroys vitamin B1; triggers asthma; mandatory allergen declaration'),
        'sodium nitrite': ('Meat preservative E250', 'Forms nitrosamines (cancer-causing) when cooked at high heat; linked to colorectal cancer'),
        'e250': ('Sodium nitrite (E250)', 'Forms nitrosamines (carcinogens) when cooked at high heat; colorectal cancer risk'),
        'sodium nitrate': ('Meat preservative E251', 'Converts to nitrite in body, linked to colorectal cancer'),
        'e251': ('Sodium nitrate (E251)', 'Converts to nitrite in body; colorectal cancer concerns'),
        'methylparaben': ('Paraben preservative', 'Mimics estrogen, hormone disruption, accumulates in breast tissue; EU restricts concentration'),
        'propylparaben': ('Paraben preservative', 'Endocrine disruptor, linked to reduced sperm count, reproductive harm; banned in children\'s products in Denmark/EU'),
        'butylparaben': ('Paraben preservative', 'Strongest hormone disruptor among parabens; bioaccumulation; reproductive toxicity; banned for children under 3 in EU'),

        # Harsh surfactants
        'sodium lauryl sulfate': ('Harsh surfactant SLS', 'Strong skin irritant; strips protective oils; can cause mouth ulcers; scalp damage; EU requires safety testing'),
        'sodium lauryl sulphate': ('Harsh surfactant SLS', 'Strong skin irritant; strips protective oils; mouth ulcers; scalp damage'),
        
        # Artificial colors with serious concerns
        'tartrazine': ('Yellow artificial color E102', 'Hyperactivity & ADHD in children, asthma attacks; EU warning label required; banned in Austria, Norway'),
        'e102': ('Tartrazine (E102)', 'EU warning label required; hyperactivity and ADHD in children; banned in several countries'),
        'sunset yellow': ('Orange artificial color E110', 'Hyperactivity in children, allergic reactions; banned in Norway & Finland; EU warning label'),
        'e110': ('Sunset Yellow (E110)', 'Banned in Norway and Finland; EU warning label required; hyperactivity concerns'),
        'allura red': ('Red artificial color E129', 'Hyperactivity, immune system tumors in mice; EU warning label; banned in several European countries'),
        'red 40': ('Allura Red (Red 40 / E129)', 'EU warning label required; banned in Denmark, Belgium, France, Switzerland, Sweden, Austria, Norway'),
        'e129': ('Allura Red (E129)', 'EU warning label required; banned in multiple European countries; hyperactivity concerns'),
        'ponceau 4r': ('Red artificial color E124', 'Banned in USA, Norway, Finland — cancer concerns, hyperactivity'),
        'e124': ('Ponceau 4R (E124)', 'Banned in USA, Norway, Finland — cancer and hyperactivity concerns'),
        'carmoisine': ('Red artificial color E122', 'Banned in USA, Canada, Japan — hyperactivity, asthma, allergic reactions'),
        'e122': ('Carmoisine (E122)', 'Banned in USA, Canada, Japan — hyperactivity and allergic reactions'),
        'brilliant blue': ('Blue artificial color E133', 'Crosses blood-brain barrier, neurotoxicity, chromosomal damage; banned in 6 EU countries'),
        'e133': ('Brilliant Blue FCF (E133)', 'Banned in Belgium, France, Germany, Greece, Italy, Spain, Switzerland'),
        'indigo carmine': ('Blue artificial color E132', 'Brain tumors in animal studies; banned in Norway'),
        'e132': ('Indigo Carmine (E132)', 'Brain tumors in animal studies; banned in Norway'),
        'erythrosine': ('Red artificial color E127', 'Thyroid tumors in rats; interferes with thyroid function'),
        'e127': ('Erythrosine (E127)', 'Thyroid tumors in animal studies; banned in cosmetics in USA'),
        'quinoline yellow': ('Yellow artificial color E104', 'Banned in USA, Canada, Japan, Australia — hyperactivity, dermatitis'),
        'e104': ('Quinoline Yellow (E104)', 'Banned in USA, Canada, Japan, Australia — hyperactivity and dermatitis'),
        'brown ht': ('Brown artificial color E155', 'Banned in USA, Canada, Australia — hyperactivity, asthma'),
        'e155': ('Brown HT (E155)', 'Banned in USA, Canada, Australia — hyperactivity and asthma'),
        'patent blue v': ('Blue artificial color E131', 'May cause anaphylaxis, urticaria; banned in USA, Canada, Australia'),
        'e131': ('Patent Blue V (E131)', 'May cause severe allergic reactions including anaphylaxis; banned in USA, Canada, Australia'),
        'azorubine': ('Red artificial color E122', 'Banned in USA, Canada, Japan; hyperactivity, asthma concerns (same as Carmoisine)'),
        'e951': ('Aspartame (E951)', 'IARC Group 2B possible carcinogen (2023); phenylalanine risk for PKU sufferers'),
        'e950': ('Acesulfame potassium (E950)', 'Animal studies show effects on gut bacteria and insulin; FDA approved but limited human long-term data'),

        # Flavor enhancers
        'disodium guanylate': ('Flavor enhancer E627', 'MSG-like effects: headaches, numbness, flushing; avoid if MSG-sensitive; neurotoxicity concerns at high doses'),
        'e627': ('Disodium guanylate (E627)', 'MSG-like effects; headaches, numbness; avoid if MSG-sensitive'),
        'disodium inosinate': ('Flavor enhancer E631', 'MSG-like effects: headaches, sweating, chest pain; avoid if MSG-sensitive'),
        'e631': ('Disodium inosinate (E631)', 'MSG-like effects; headaches, sweating, chest pain; avoid if MSG-sensitive'),

        # Acids with concerns
        'phosphoric acid': ('Acidulant E338', 'Erodes tooth enamel, reduces bone density, kidney stones, calcium depletion'),
        'e338': ('Phosphoric acid (E338)', 'Erodes tooth enamel, reduces bone density, calcium depletion'),
        'caramel colour': ('Color additive E150c/d', 'Class III/IV caramel contains 4-MEI (potential carcinogen in animal studies); California Prop 65 listed'),
        'caramel color': ('Color additive E150c/d', 'Class III/IV caramel contains 4-MEI (potential carcinogen); California Prop 65 listed'),
        'e150': ('Caramel colour (E150)', 'Class III/IV contains 4-MEI — potential carcinogen in animal studies; California Prop 65 listed'),

        # Preservatives in personal care
        'methylchloroisothiazolinone': ('Preservative MCI', 'Severe contact dermatitis, skin allergies, neurotoxic; EU banned in leave-on cosmetics; strong allergen'),
        'methylisothiazolinone': ('Preservative MI', 'Strong allergen, contact dermatitis; EU banned in all leave-on cosmetics; frequent occupational allergen'),
        'dmdm hydantoin': ('Formaldehyde-releasing preservative', 'Slowly releases formaldehyde (IARC Group 1 carcinogen); contact dermatitis, hair loss reports; restricted in EU cosmetics'),
        'imidazolidinyl urea': ('Formaldehyde-releasing preservative', 'Releases formaldehyde over time; skin sensitiser, potential carcinogen, contact allergy risk'),
        'diazolidinyl urea': ('Formaldehyde-releasing preservative', 'Releases formaldehyde; strongest formaldehyde releaser in cosmetics; contact dermatitis'),
        'quaternium-15': ('Formaldehyde-releasing preservative', 'Highest formaldehyde release rate among cosmetic preservatives; restricted in EU'),
        'phenyl mercuric': ('Mercury-based preservative', 'Mercury compound — toxic to kidneys and nervous system; banned in most countries'),
        'formaldehyde': ('Known carcinogen (IARC Group 1)', 'Direct carcinogen; causes DNA damage and cancer; banned as preservative in EU cosmetics; released by formaldehyde-releaser preservatives'),
        'bronopol': ('Formaldehyde-releasing preservative', 'Releases formaldehyde and can form nitrosamines; EU restricted; skin and eye irritant'),

        # Sweeteners — commonly questioned
        'aspartame': ('Artificial sweetener E951', 'IARC Group 2B possible carcinogen (2023); contains phenylalanine — dangerous for PKU sufferers; headaches, mood changes reported'),
        'acesulfame potassium': ('Artificial sweetener Ace-K (E950)', 'Animal studies show effects on gut bacteria and insulin signalling; FDA-approved but limited long-term human data'),
        'acesulfame-k': ('Artificial sweetener Ace-K (E950)', 'Animal studies show metabolic effects; FDA-approved but limited long-term human data'),

        # Antioxidant preservatives
        'butylated hydroxyanisole': ('Antioxidant preservative (BHA)', 'IARC Group 2B possible carcinogen; banned in Japan; EU-restricted in some foods; California Prop 65 listed'),
        'butylated hydroxytoluene': ('Antioxidant preservative (BHT)', 'Liver and thyroid effects in animal studies; hormonal disruption; restricted in several countries'),
        'tert-butylhydroquinone': ('Antioxidant preservative (TBHQ)', 'Banned in Japan; EU-restricted; high doses linked to DNA damage; stomach tumour promotion in animal studies'),
        'tbhq': ('Antioxidant preservative (TBHQ)', 'Banned in Japan; EU-restricted; high doses linked to DNA damage; stomach tumour promotion in animal studies'),

        # Banned dough conditioners / emulsifiers
        'potassium bromate': ('Bread improver', 'Banned in EU, UK, Canada, Australia, China — oxidises to bromide; classified as possible carcinogen by IARC'),
        'azodicarbonamide': ('Dough conditioner', 'Banned in EU, UK, Australia, Singapore — breaks down to semicarbazide, a possible carcinogen'),
        'brominated vegetable oil': ('Citrus-drink emulsifier', 'Banned in EU, Japan, India — bromine accumulates in body; thyroid and neurological effects'),

        # Talc — asbestos contamination risk
        'talcum': ('Talcum powder', 'Natural talc deposits may contain asbestos fibres; IARC classifies inhaled talc-with-asbestos as carcinogenic; FDA recalled multiple talc products'),
        'talc': ('Cosmetic talc', 'Natural talc deposits may contain asbestos fibres; IARC classifies inhaled talc-with-asbestos as carcinogenic; FDA recalled multiple talc products'),

        # CI food/cosmetic colorants banned or restricted in multiple countries
        'ci 47000': ('Quinoline Yellow (E104)', 'Banned in USA, Canada, Japan, Australia — linked to hyperactivity and ADHD in children; EU requires warning label'),
        'ci 19140': ('Tartrazine (E102)', 'EU warning label required — hyperactivity and ADHD in children; banned in Austria, Norway; restricted in many countries'),
        'ci 15985': ('Sunset Yellow (E110)', 'Banned in Norway and Finland; EU warning label required; linked to hyperactivity in children'),
        'ci 16035': ('Allura Red (E129)', 'EU warning label required; banned in Denmark, Belgium, France, Switzerland, Sweden, Austria, Norway'),
        'ci 42090': ('Brilliant Blue FCF (E133)', 'Banned in Belgium, France, Germany, Greece, Italy, Spain, Switzerland; chromosomal damage in animal studies'),

        # Titanium Dioxide — EU banned as food additive 2022
        'titanium dioxide': ('White pigment (E171)', 'Banned as food additive in EU since 2022 — genotoxicity concerns; EFSA ruled cannot be considered safe; nanoparticles may penetrate skin; inhalation causes lung inflammation'),
        'e171': ('Titanium dioxide (E171)', 'EU banned as food additive since 2022 — EFSA found cannot exclude genotoxicity; nanoparticles implicated in lung and DNA damage'),

        # Carrageenan — banned in EU infant formula, gut inflammation
        'carrageenan': ('Thickener E407', 'Banned in EU infant formula; IARC linked to gut inflammation and colitis in animal studies; possible promoter of colon cancer in research'),
        'e407': ('Carrageenan (E407)', 'Banned in EU infant formula; gut inflammation studies; possible colon cancer promoter in animal research'),

        # PEG compounds — carcinogen contamination risk
        'peg-': ('PEG compound (polyethylene glycol)', 'May be contaminated with 1,4-dioxane (IARC Group 2B carcinogen); acts as penetration enhancer, increasing absorption of other potentially toxic ingredients'),
        'polyethylene glycol': ('PEG polymer', 'Possible 1,4-dioxane contamination (carcinogen); increases skin permeability to other chemicals'),

        # Chelating agents — mineral stripping and toxin penetration
        'tetrasodium edta': ('Chelating agent EDTA', 'Strips essential minerals (calcium, zinc, iron) from body; enhances skin penetration of other ingredients including toxins; environmental persistence'),
        'disodium edta': ('Chelating agent EDTA', 'Strips minerals; penetration enhancer for other chemicals; environmental toxin; restricted in some jurisdictions'),
        'tetrasodium etidronate': ('Chelating agent', 'Binds calcium and other essential minerals; may affect bone health with prolonged use'),

        # Propylene Glycol — neurotoxic at high doses
        'propylene glycol': ('Humectant/solvent', 'Neurotoxicity at high doses (documented in medical literature); skin and eye irritant; penetration enhancer; may cause kidney and liver damage in large systemic exposure'),

        # SLES / ALES — consistent with SLS policy; contamination risk
        'sodium laureth sulfate': ('Surfactant SLES', 'Strips natural skin oils; may be contaminated with 1,4-dioxane (carcinogen) from ethoxylation process; scalp, skin and eye irritant'),
        'sodium laureth sulphate': ('Surfactant SLES', 'Strips natural skin oils; potential 1,4-dioxane contamination from ethoxylation; scalp and eye irritation'),
        'ammonium laureth sulfate': ('Surfactant ALES', 'Similar to SLES; potential 1,4-dioxane contamination; strips natural oils; scalp irritation'),
        'cocamidopropyl betaine': ('Amphoteric surfactant', 'Causes allergic contact dermatitis and skin sensitization; EU flagged as allergen; eye irritant; impurities (DMAPA, amidoamine) are known allergens'),

        # Trans fats — banned in USA/EU/many countries
        'partially hydrogenated': ('Trans fat source', 'Contains trans fatty acids — banned in USA (2018), EU, Canada, many countries; raises LDL cholesterol, lowers HDL; significantly increases heart disease and stroke risk'),

        # Emulsifiers with trans fat and glycidol concerns
        'mono and diglycerides': ('Emulsifier E471', 'May contain trans fats from hydrogenated oil sources; can contain glycidol fatty acid esters (IARC Group 2A carcinogen); EFSA raised safety concerns in 2018 review'),

        # Preservatives with severe toxicity
        'benzyl alcohol': ('Preservative/solvent', 'Toxic to neonates — can cause fatal gasping syndrome; metabolizes to benzaldehyde and benzoic acid; banned in products for infants; contact dermatitis in sensitive individuals'),

        # Cyclic silicones — EU banned/restricted, endocrine disruption, environmental persistence
        'cyclomethicone': ('Cyclic silicone blend (D4/D5/D6)', 'EU restricted >0.1% in rinse-off cosmetics; persistent environmental pollutant; bioaccumulates in aquatic organisms; endocrine disruption concerns'),
        'cyclopentasiloxane': ('Cyclic silicone D5', 'EU banned in rinse-off cosmetics at >0.1% since 2020; classified as Substance of Very High Concern; persistent organic pollutant; endocrine disruptor'),
        'cyclohexasiloxane': ('Cyclic silicone D6', 'EU restricted in wash-off cosmetics; environmental persistence and bioaccumulation; similar endocrine disruption concerns as D4/D5'),

        # Petroleum-derived — PAH/MOAH contamination and EU bans
        'mineral oil': ('Petroleum-derived oil', 'EU restricts in food unless PAH safety established; MOAH (mineral oil aromatic hydrocarbons) are IARC Group 1 carcinogens; contamination risk from refining'),
        'petrolatum': ('Petroleum jelly (petroleum-derived)', 'EU bans unless full refining history is established — PAH contamination risk; MOAH are IARC Group 1 carcinogens; restricted in EU cosmetics regulation'),
        'paraffinum liquidum': ('Liquid paraffin (petroleum-derived)', 'EU requires PAH safety data before approval; MOAH (IARC Group 1 carcinogens) contamination risk from petrochemical refining'),
        'paraffin wax': ('Paraffin wax (petroleum-derived)', 'Petroleum-derived; potential PAH/MOAH contamination (IARC Group 1 carcinogens); EU restricts in food applications (E905)'),

        # Retinoids — teratogenic in pregnancy, sunlight-activated tumour risk
        'retinol': ('Vitamin A retinoid', 'Teratogenic — contraindicated in pregnancy (causes severe birth defects); increases UV sensitivity; NTP study linked retinyl palmitate metabolite to accelerated skin tumour growth in sunlight'),
        'retinyl palmitate': ('Vitamin A ester retinoid', 'NTP study showed accelerated photocarcinogenesis (skin tumour growth) when applied to skin exposed to sunlight; teratogenic at high doses; avoid daytime use'),
        'tretinoin': ('Prescription retinoid (retinoic acid)', 'Prescription-only in India and most countries; Pregnancy Category X — highly teratogenic, causes craniofacial and CNS birth defects; requires medical supervision'),
        'retinal': ('Retinaldehyde (Vitamin A form)', 'More potent than retinol; teratogenic — contraindicated in pregnancy; significantly increases UV/sun sensitivity and photocarcinogenesis risk'),
        'hydroxypinacolone retinoate': ('Ester of retinoic acid', 'Retinoid compound — contraindicated in pregnancy; photosensitizing; limited long-term safety data despite milder irritation profile than retinol'),

        # Saccharin — bladder cancer in animal studies
        'saccharin': ('Artificial sweetener E954', 'Caused bladder tumours in male rats at high doses; banned in Canada 1977–2014; FDA temporarily removed GRAS status; precautionary concern remains despite reversal'),
        'e954': ('Saccharin (E954)', 'Bladder cancer in rats at high doses; historical bans in multiple countries; FDA warning label required until 2000; precautionary concerns remain'),

        # Undisclosed colorants — exact dye identity hidden behind Q.S notation
        'colour q.s': ('Undisclosed colorant (Q.S)', 'Brand is hiding the exact dye or pigment used — coloring agents include synthetic azo dyes, heavy-metal-based pigments and sensitizers; without disclosure there is no way to assess safety'),
        'color q.s': ('Undisclosed colorant (Q.S)', 'Brand is hiding the exact dye or pigment used — coloring agents include synthetic azo dyes, heavy-metal-based pigments and sensitizers; without disclosure there is no way to assess safety'),
        'colour q.s.': ('Undisclosed colorant (Q.S.)', 'Brand hiding exact colorant identity; may include restricted or banned dyes'),
        'color q.s.': ('Undisclosed colorant (Q.S.)', 'Brand hiding exact colorant identity; may include restricted or banned dyes'),

        # Fragrance — hidden allergens, phthalates, undisclosed endocrine disruptors
        'fragrance': ('Proprietary fragrance mixture', 'A single "fragrance" label entry may hide dozens of undisclosed chemicals including known allergens, phthalates and synthetic musks; EU requires 26 specific allergens declared separately; contact dermatitis and respiratory sensitization risk'),
        'perfume': ('Proprietary fragrance/parfum blend', 'Proprietary blend of chemicals — may contain undisclosed allergens, phthalates, endocrine disruptors and sensitizers; contact dermatitis and respiratory sensitization risk'),
        'parfum': ('Proprietary fragrance (EU INCI term)', 'EU requires 26 specific allergens listed if found in parfum; may contain undisclosed phthalates, synthetic nitromusks (several banned in EU) and other sensitizers'),

        # Artificial flavors — undisclosed synthetic chemicals
        'artificial flavor': ('Synthetic flavoring agent', 'Synthetic chemical blend used to mimic natural flavour; individual compounds not disclosed on labels; may include diacetyl (linked to lung disease), benzaldehyde, propylene glycol derivatives and other synthetic chemicals'),
        'artificial flavour': ('Synthetic flavoring agent', 'Synthetic flavouring not derived from natural sources; compounds undisclosed; may include diacetyl (lung disease risk), propylene glycol derivatives and other synthetic chemicals with varying safety profiles'),
    }

    # WORTH KNOWING INGREDIENTS (YELLOW) - Generally safe but with considerations
    worth_knowing_patterns = {
        # Sugars and sweeteners
        'sugar': ('Sweetener', 'Excess causes obesity, type 2 diabetes, tooth decay, energy crashes, inflammation'),
        'high fructose corn syrup': ('Sweetener', 'Linked to obesity, fatty liver disease, insulin resistance, metabolic syndrome'),
        'glucose syrup': ('Sweetener', 'Rapid blood sugar spikes, weight gain, diabetes risk with regular consumption'),
        'invert sugar': ('Sweetener', 'High calorie, tooth decay, blood sugar spikes, similar concerns as regular sugar'),
        'maltodextrin': ('Carbohydrate additive', 'Very high glycemic index — faster blood sugar spike than table sugar; may harm gut microbiome with regular use'),
        'corn syrup solids': ('Dried glucose syrup', 'High-GI refined carbohydrate; rapid blood sugar spike; often used in creamers in protein powders'),

        # Artificial sweeteners (moderate evidence)
        'sucralose': ('Artificial sweetener E955', 'Alters gut microbiome composition; may impair insulin response; some studies link to increased appetite and glucose intolerance'),
        'e955': ('Sucralose (E955)', 'Alters gut microbiome; may impair insulin response; glucose intolerance in some studies'),

        # MSG — flavor enhancer (FDA GRAS, some sensitivity)
        'monosodium glutamate': ('Flavor enhancer MSG (E621)', 'FDA-approved GRAS; some individuals report sensitivity; generally safe at normal dietary levels'),
        'msg': ('Monosodium glutamate (MSG / E621)', 'FDA-approved GRAS; some people report sensitivity; generally safe for most at normal dietary levels'),
        'e621': ('MSG / Monosodium glutamate (E621)', 'FDA-approved GRAS; some people report sensitivity; generally safe at normal dietary levels'),

        # Fiber additives
        'inulin': ('Prebiotic fiber', 'Causes gas, bloating and abdominal discomfort in doses above 5g; ferments rapidly in colon — problematic for IBS sufferers'),
        'polydextrose': ('Synthetic soluble fiber E1200', 'May cause gas and bloating in large amounts; generally well tolerated at moderate doses'),
        
        # Oils and fats
        'palm oil': ('Vegetable oil', 'High saturated fat (50%), raises LDL cholesterol, heart disease risk'),
        'palmolein': ('Refined palm oil', 'High saturated fat, may increase cardiovascular disease risk'),
        'hydrogenated': ('Modified fat', 'May contain trans fats, increases heart disease risk, raises bad cholesterol'),
        # partially hydrogenated → moved to commonly_questioned (trans fats, banned in USA/EU/Canada)

        # Emulsifiers and stabilizers
        'soy lecithin': ('Emulsifier E322', 'Generally safe but soy allergen, may cause digestive issues in sensitive people'),
        # mono and diglycerides → moved to commonly_questioned (trans fat risk, glycidol concern)
        'polyglycerol polyricinoleate': ('Emulsifier E476', 'Synthetic, may cause digestive upset, liver enlargement in animal studies'),
        'ammonium phosphatides': ('Emulsifier E442', 'Synthetic, limited safety data, may affect mineral absorption'),
        # carrageenan → moved to commonly_questioned (EU infant formula ban)
        'phenoxyethanol': ('Preservative (EU max 1%)', 'Synthetic preservative permitted in cosmetics worldwide; EU restricts to max 1%; generally safe at permitted levels; FDA cautioned against use in nipple creams for nursing infants specifically'),
        # benzyl alcohol → in commonly_questioned (toxic to neonates)

        # Preservatives (milder concerns)
        'potassium sorbate': ('Preservative E202', 'Generally safe; may cause skin irritation and allergic reactions; migraines reported'),
        'e202': ('Potassium sorbate (E202)', 'Generally safe preservative; may cause contact allergies in sensitive individuals'),
        'e955': ('Sucralose (E955)', 'Alters gut microbiome; may impair insulin response; glucose intolerance in some studies'),
        # e954 / saccharin → moved to commonly_questioned (bladder cancer in rats, historical bans)
        # mineral oil, petrolatum, paraffinum liquidum, paraffin wax → moved to commonly_questioned (PAH/MOAH contamination)

        # Denatured alcohols
        'alcohol denat': ('Denatured alcohol', 'Drying to skin; disrupts protective skin barrier with repeated use; may cause sensitivity'),
        'denatured alcohol': ('Denatured alcohol', 'Drying to skin and scalp; disrupts skin barrier function with repeated use'),
        'sd alcohol': ('Specially denatured alcohol', 'Drying to skin; disrupts barrier; can cause irritation with frequent use'),

        # Allergens
        'lanolin': ('Wool-derived emollient', 'Natural but common allergen (~1.7% population); may contain pesticide residues from sheep wool'),
        'wool wax': ('Lanolin derivative', 'Wool-derived; contact allergy risk in lanolin-sensitive individuals'),

        # Silicones (cyclic) → moved to commonly_questioned (EU bans, endocrine disruption)
        # cyclomethicone, cyclopentasiloxane, cyclohexasiloxane → see commonly_questioned_patterns
        'amodimethicone': ('Modified silicone', 'Builds up on hair; environmental persistence; hard to biodegrade'),

        # Sweeteners
        # saccharin / e954 → moved to commonly_questioned (bladder cancer in rats, historical bans)

        # Retinoids → moved to commonly_questioned (teratogenic, sunlight tumour risk)
        
        # Silicones
        'dimethiconol': ('Silicone', 'Builds up on hair/skin, clogs pores, environmental persistence, hard to remove'),
        'dimethicone': ('Silicone', 'Can trap dirt/bacteria, may cause breakouts, environmental concerns'),

        # CI cosmetic colorants — permitted but limited long-term safety data
        'ci 26100': ('Cosmetic colorant Red 17 (Solvent Red 23)', 'Synthetic azo dye permitted in cosmetics; limited long-term human data; restricted in some countries'),
        'ci 61565': ('Cosmetic colorant Vat Green 1', 'Synthetic vat dye permitted in EU cosmetics; limited toxicology data; patch test advised for sensitive skin'),
        'ci 17200': ('Cosmetic colorant Red 33 (Acid Red 33)', 'Synthetic dye; restricted in some countries; may cause contact dermatitis in sensitive individuals'),
        'ci 15510': ('Cosmetic colorant Orange 4 (Acid Orange 7)', 'Synthetic azo dye; permitted in most countries; may cause contact dermatitis'),
        'ci 45410': ('Cosmetic colorant Red 27 (Acid Red 92)', 'Synthetic dye permitted in EU; some data suggesting skin sensitization'),

        # Chelating agents (moved to commonly_questioned — see below)
        
        # Mild acids
        'citric acid': ('Preservative/acidulant E330', 'Tooth enamel erosion with frequent exposure, stomach upset in large amounts'),

        # Colorants (natural/mineral)
        'beta carotene': ('Provitamin A colorant E160a', 'Safe at normal food exposure levels; concern only at very high supplement doses (20mg+/day) in active smokers'),
        'caramel': ('Brown color', 'Natural but may contain trace amounts of carcinogenic compounds'),
        
        # Thickeners
        'guar gum': ('Thickener E412', 'Digestive issues, bloating, gas, may interfere with medication absorption'),
        'xanthan gum': ('Thickener E415', 'Digestive issues in large amounts, bloating, may cause allergic reactions'),
        
        # Humectants
        # propylene glycol → moved to commonly_questioned (neurotoxicity, penetration enhancer)
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
        
        # Vague / undisclosed descriptors — brand hiding full composition
        'q.s': ('Undisclosed filler (Q.S)', 'Brand has not disclosed the full ingredient — "quantum sufficit" means added in unspecified quantity; exact composition unknown'),
        'q.s.': ('Undisclosed filler (Q.S.)', 'Brand has not disclosed the full ingredient — added in unspecified quantity; exact composition unknown'),
        'quantum sufficit': ('Undisclosed filler', 'Latin for "as much as needed" — brand intentionally hiding exact ingredient or quantity'),

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
        # Iron oxide must come before generic 'iron' so more specific pattern wins
        'iron oxide': ('Mineral pigment', 'FDA and EU approved; widely used in cosmetics and food colouring; no known health concerns'),
        'ci 77491': ('Iron Oxide Red', 'FDA and EU approved mineral pigment; widely used in cosmetics; no known health concerns'),
        'ci 77492': ('Iron Oxide Yellow', 'FDA and EU approved mineral pigment; widely used in cosmetics; no known health concerns'),
        'ci 77499': ('Iron Oxide Black', 'FDA and EU approved mineral pigment; widely used in cosmetics; no known health concerns'),
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

    # Safe Q.S override — known-safe ingredients stay generally_recognised even with Q.S appended
    # Must run before commonly_questioned/worth_knowing loops (colour/q.s patterns would catch them)
    _QS_SAFE_PATTERNS = {
        'multani mitti': ('Fuller\'s Earth (Multani Mitti)', 'Natural clay mineral with absorbent properties; safe for topical use'),
        "fuller's earth": ('Fuller\'s Earth', 'Natural absorbent clay mineral; safe for topical use'),
        'fullers earth': ('Fuller\'s Earth', 'Natural absorbent clay mineral; safe for topical use'),
    }
    if 'q.s' in ingredient_lower:
        for safe_pat, (what_it_is, note) in _QS_SAFE_PATTERNS.items():
            if safe_pat in ingredient_lower:
                return {
                    'classification': 'generally_recognised',
                    'what_it_is': what_it_is,
                    'one_line_note': note,
                    'regulatory_note': 'Safe ingredient; Q.S notation indicates quantity added as needed'
                }

    # Check commonly questioned first (highest priority — serious concerns)
    # Also check compact form so "Methyl Paraben" matches keyword "methylparaben"
    for pattern, (what_it_is, note) in commonly_questioned_patterns.items():
        pattern_compact = pattern.replace(' ', '').replace('-', '').replace('/', '')
        if pattern in ingredient_lower or pattern_compact in ingredient_compact:
            return {
                'classification': 'commonly_questioned',
                'what_it_is': what_it_is,
                'one_line_note': INGREDIENT_DESCRIPTIONS.get(pattern, note),
                'regulatory_note': 'Check usage guidelines and restrictions'
            }

    # Check worth knowing second (specific ingredient concerns take priority over generic natural labels)
    for pattern, (what_it_is, note) in worth_knowing_patterns.items():
        pattern_compact = pattern.replace(' ', '').replace('-', '').replace('/', '')
        if pattern in ingredient_lower or pattern_compact in ingredient_compact:
            return {
                'classification': 'worth_knowing',
                'what_it_is': what_it_is,
                'one_line_note': INGREDIENT_DESCRIPTIONS.get(pattern, note),
                'regulatory_note': 'FSSAI approved with usage guidelines'
            }

    # Check generally recognised (natural/herbal ingredients — checked last to avoid overriding specific flags)
    for pattern, (what_it_is, note) in generally_recognised_patterns.items():
        if pattern in ingredient_lower:
            return {
                'classification': 'generally_recognised',
                'what_it_is': what_it_is,
                'one_line_note': INGREDIENT_DESCRIPTIONS.get(pattern, note),
                'regulatory_note': 'No specific restrictions, widely used'
            }

    # Default to generally recognised
    return {
        'classification': 'generally_recognised',
        'what_it_is': 'Food or cosmetic ingredient',
        'one_line_note': 'Generally recognised as safe for use in food and cosmetic products.',
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
