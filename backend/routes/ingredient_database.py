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
    'sodium benzoate': 'The sodium salt of benzoic acid (E211), used as a preservative in acidic foods, beverages and cosmetics. It occurs naturally in small amounts in cranberries, prunes and cinnamon. If combined with Vitamin C (ascorbic acid) or citric acid, it can potentially produce benzene, a known carcinogen, although this is more common in beverages than in topical products. While generally safe within approved limits (0.5% in cosmetics), higher concentrations are more likely to cause irritant reactions.',
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

    # ── INS / E Numbered Food Additives ────────────────────────────────────────
    # Colours
    'curcumin': 'Curcumin (E100/INS 100) is the bright yellow polyphenol pigment responsible for the colour of turmeric root. Extracted from Curcuma longa, it has been used as a food colorant and spice for over 4,000 years. Approved by FSSAI, EU, FDA and CODEX as a natural yellow food colorant.',
    'e100': 'E100/INS 100 is curcumin, the natural yellow pigment extracted from turmeric (Curcuma longa). Approved as a food colorant by FSSAI, EU and CODEX at specified limits in food products.',
    'riboflavin': 'Riboflavin (Vitamin B2 / E101/INS 101) is an essential water-soluble B vitamin found in dairy, meat, eggs and green vegetables. Used both as a dietary supplement and as a natural yellow food colorant in foods and beverages.',
    'e101': 'E101/INS 101 is riboflavin (Vitamin B2), used as a yellow food colorant and nutritional supplement. Approved by FSSAI, EU and CODEX. Safe and beneficial as an essential vitamin.',
    'carmine': 'Carmine (E120/INS 120 / Cochineal Red A) is a vivid crimson-red dye produced from the dried body of the cochineal insect (Dactylopius coccus). Used for centuries as a natural red colorant in foods, cosmetics and textiles. Requires labelling as "carmine" or "cochineal" in many countries due to allergy risk.',
    'cochineal': 'The dried body of the female cochineal insect (Dactylopius coccus), which produces carminic acid — the basis for carmine dye (E120/INS 120). Ground into a powder and used to produce red colorants for food, cosmetics and textiles.',
    'e120': 'E120/INS 120 is carmine (cochineal extract), a natural red dye derived from cochineal insects. Approved by FSSAI, EU and FDA. Vegetarians and vegans should note it is animal-derived; some individuals are allergic.',
    'e160b': 'E160b/INS 160b is annatto extract (bixin/norbixin), a natural yellow-orange colorant from the seeds of the achiote tree. Approved by FSSAI, EU and CODEX for use in cheese, butter, snacks and beverages.',
    'e162': 'E162/INS 162 is betanin (beetroot red), the natural crimson-red pigment extracted from beetroot (Beta vulgaris). Approved by FSSAI and EU as a natural food colorant; the coloured urine or stools from beetroot are harmless.',
    'betanin': 'Betanin (E162/INS 162) is the natural red-violet pigment extracted from red beetroot (Beta vulgaris). Used as a natural food colorant in yoghurt, confectionery and beverages. Safe and CODEX-approved.',
    'e163': 'E163/INS 163 is anthocyanins, the natural blue-violet-red pigments found in berries, red cabbage, grapes and hibiscus flowers. Approved by FSSAI and EU as natural food colorants with antioxidant properties.',
    'anthocyanins': 'Anthocyanins (E163/INS 163) are the natural blue-violet-red pigments found in berries, red/purple grapes, red cabbage and hibiscus. Widely used as natural food colorants and recognised as powerful antioxidants. CODEX and FSSAI approved.',
    'e172': 'E172/INS 172 is iron oxides and hydroxides, naturally occurring mineral pigments in red, yellow and black forms. Approved by FDA and EU as safe colorants in cosmetics, food colouring and pharmaceutical tablet coatings.',
    # Sorbates
    'sorbic acid': 'Sorbic acid (E200/INS 200) is a naturally occurring unsaturated fatty acid first isolated from the unripe berries of the mountain ash tree (Sorbus aucuparia) in 1859. The most widely used antimould agent in foods worldwide. Inhibits growth of mould and yeast at concentrations as low as 0.025%. GRAS in USA, approved by FSSAI, EU and CODEX.',
    'e200': 'E200/INS 200 is sorbic acid, the most widely used mould inhibitor in food products. Approved by FSSAI, EU and CODEX for use in cheeses, baked goods, dried fruits and beverages at specified limits.',
    'sodium sorbate': 'The sodium salt of sorbic acid (E201/INS 201), used as a food preservative to inhibit mould and yeast. More soluble than sorbic acid and potassium sorbate. Approved by CODEX.',
    'e201': 'E201/INS 201 is sodium sorbate, a sorbic acid salt used as a mould and yeast inhibitor in food products. CODEX approved at specified limits.',
    # Benzoates
    'benzoic acid': 'A naturally occurring carboxylic acid (E210/INS 210) found in small amounts in cranberries, prunes and cinnamon. Used as a preservative in acidic foods and beverages to inhibit bacteria, yeast and mould. If combined with Vitamin C in acidic beverages, trace amounts of benzene may form.',
    'e210': 'E210/INS 210 is benzoic acid, a food preservative effective in acidic products. Approved by FSSAI, EU and CODEX. Can form trace benzene with ascorbic acid (Vitamin C) in acidic beverages — a concern at high concentrations.',
    'calcium benzoate': 'The calcium salt of benzoic acid (E213/INS 213), used as a food preservative in acidic products. Similar regulatory profile to sodium benzoate (E211).',
    'e213': 'E213/INS 213 is calcium benzoate, a calcium salt preservative used in acidic foods and beverages. Similar concerns as sodium benzoate at high concentrations with Vitamin C.',
    # Propionates
    'propionic acid': 'A short-chain saturated fatty acid (E280/INS 280) naturally produced by fermentation in the gut and found in small amounts in Swiss cheese. Used commercially as a mould inhibitor in bread and bakery products.',
    'e280': 'E280/INS 280 is propionic acid, a naturally occurring short-chain fatty acid used as a mould inhibitor in bread. Naturally present in some fermented dairy products. Approved by FSSAI, EU and CODEX.',
    'sodium propionate': 'The sodium salt of propionic acid (E281/INS 281), used as a mould inhibitor primarily in bread and baked goods. Approved by FSSAI, EU and CODEX at specified limits.',
    'e281': 'E281/INS 281 is sodium propionate, a bread preservative preventing mould growth. Approved by FSSAI, EU and CODEX at specified limits in bakery products.',
    'calcium propionate': 'The calcium salt of propionic acid (E282/INS 282), widely used as a mould inhibitor in bread, baked goods and processed cheese. Also provides calcium. Approved by FSSAI, EU, FDA and CODEX.',
    'e282': 'E282/INS 282 is calcium propionate, the most widely used preservative in bread and baked goods to prevent mould. FSSAI, EU and FDA approved at specified limits.',
    # Antioxidants
    'sodium ascorbate': 'The sodium salt of ascorbic acid (Vitamin C / E301/INS 301), used as an antioxidant preservative and a more stable, less acidic form of Vitamin C in food and pharmaceutical products.',
    'e301': 'E301/INS 301 is sodium ascorbate (Vitamin C sodium salt), an antioxidant preservative and Vitamin C source approved by FSSAI, EU and CODEX.',
    'calcium ascorbate': 'The calcium salt of ascorbic acid (Vitamin C / E302/INS 302), providing both antioxidant protection and dietary calcium. Used as a food additive and dietary supplement.',
    'e302': 'E302/INS 302 is calcium ascorbate (Vitamin C calcium salt), a buffered, non-acidic antioxidant and calcium supplement approved by FSSAI and CODEX.',
    'ascorbyl palmitate': 'A fat-soluble ester of ascorbic acid (Vitamin C) and palmitic acid (E304/INS 304). Used as an antioxidant in fatty and oil-based foods to prevent rancidity. Also used in cosmetics as a skin antioxidant.',
    'e304': 'E304/INS 304 is ascorbyl palmitate, a fat-soluble form of Vitamin C used as an antioxidant to protect oils, fats and fat-containing foods from oxidative rancidity. FSSAI, EU and CODEX approved.',
    'propyl gallate': 'A synthetic antioxidant (E310/INS 310) made by esterifying gallic acid with propyl alcohol. Used since the 1940s to prevent rancidity in edible fats, oils, chewing gum and some meat products. Subject to ongoing regulatory review in some jurisdictions.',
    'e310': 'E310/INS 310 is propyl gallate, a synthetic antioxidant used in fats, oils and baked goods. Approved by FSSAI and CODEX at specified limits, though under review in some jurisdictions for potential safety concerns.',
    # Thickeners & Stabilisers
    'e401': 'E401/INS 401 is sodium alginate, a natural polysaccharide thickener extracted from brown seaweed. Approved by FSSAI, EU and CODEX for use in dairy, bakery and processed foods.',
    'e402': 'E402/INS 402 is potassium alginate, a natural seaweed-derived thickener and stabiliser approved by CODEX and EU for food use.',
    'potassium alginate': 'A natural thickener and gel-former (E402/INS 402) extracted from brown seaweed, the potassium salt of alginic acid. Used in food and pharmaceutical applications.',
    'e404': 'E404/INS 404 is calcium alginate, a calcium salt of alginic acid extracted from brown seaweed. Used as a thickener, stabiliser and gelling agent in processed foods. CODEX and EU approved.',
    'calcium alginate': 'The calcium salt of alginic acid (E404/INS 404), extracted from brown seaweed. Forms a firm gel in the presence of calcium ions. Used in restructured foods and as an encapsulation material.',
    'agar': 'A natural polysaccharide (E406/INS 406) extracted from red algae (Gelidium and Gracilaria species). Used as a thickener, gelling agent and vegan alternative to gelatine. Has been used in Asian cooking for centuries and in microbiology as a culture medium.',
    'e406': 'E406/INS 406 is agar, a natural red algae-derived gelling agent and vegetarian alternative to gelatine. Approved by FSSAI, EU and CODEX for use in desserts, confectionery and dairy products.',
    'locust bean gum': 'A natural thickener and stabiliser (E410/INS 410) produced from the endosperm of carob beans (Ceratonia siliqua). Used in ice cream, dairy products and meat products to improve texture.',
    'carob bean gum': 'Another name for locust bean gum (E410/INS 410), a natural seed gum from carob trees used as a thickener and stabiliser in ice cream, dairy and processed meat products.',
    'e410': 'E410/INS 410 is locust bean gum (carob bean gum), a natural thickener from carob seeds. Approved by FSSAI, EU and CODEX for use in dairy products, sauces and processed meats.',
    'gum arabic': 'A natural gum (E414/INS 414) harvested from the sap of Acacia senegal and Acacia seyal trees in sub-Saharan Africa. One of the oldest and most widely used food additives, present in confectionery, soft drinks and encapsulated flavours. Also a prebiotic dietary fibre.',
    'acacia': 'Gum arabic from acacia trees (E414/INS 414), a natural water-soluble gum used as a thickener, emulsifier, encapsulating agent and prebiotic fibre in confectionery, beverages and food supplements.',
    'e414': 'E414/INS 414 is gum arabic (acacia gum), a natural thickener, stabiliser and encapsulant from acacia trees. Approved by FSSAI, EU and CODEX. Also a prebiotic dietary fibre with fermentation studies showing gut health benefits.',
    'gellan gum': 'A natural microbial polysaccharide (E418/INS 418) produced by the bacterium Sphingomonas elodea. Used as a thickener, gelling agent and suspension stabiliser in beverages, desserts and dairy products.',
    'e418': 'E418/INS 418 is gellan gum, a fermentation-derived thickener and gelling agent. Approved by FSSAI, EU and FDA for use in food products including beverages and dairy.',
    'pectin': 'A natural structural polysaccharide (E440/INS 440) found in the cell walls of fruits, especially citrus peel and apple pomace. The most widely used natural gelling agent in jams, jellies and confectionery. Also a soluble dietary fibre with prebiotic properties.',
    'e440': 'E440/INS 440 is pectin, a natural fruit-derived thickener and gelling agent used in jams, jellies, yoghurts and confectionery. Approved by FSSAI, EU and CODEX. A natural dietary fibre with no known health concerns.',
    'microcrystalline cellulose': 'Refined, purified cellulose (E460/INS 460) produced from wood pulp or cotton by partial acid hydrolysis. Used as a texturiser, anticaking agent, binder in tablets and as a fat replacer in reduced-calorie foods.',
    'e460': 'E460/INS 460 is microcrystalline cellulose (MCC), a refined cellulose used as a texturiser, bulking agent and tablet binder. Approved by FSSAI, EU and CODEX. Safe, indigestible structural carbohydrate.',
    'methyl cellulose': 'A modified cellulose (E461/INS 461) that forms a gel when heated and dissolves when cooled — the opposite of most gels. Used as a thickener, emulsifier and film-forming agent in food and pharmaceuticals.',
    'e461': 'E461/INS 461 is methyl cellulose, a thermoreversible gelling agent and thickener approved by EU and CODEX. Used in dietary supplements and food products.',
    'hydroxypropyl methylcellulose': 'A cellulose ether (E464/INS 464) used as a film-forming agent, thickener and vegetarian capsule material in pharmaceuticals and food products.',
    'e464': 'E464/INS 464 is hydroxypropyl methylcellulose (HPMC), used as a thickener and film-forming agent in food, and as a vegetarian/vegan capsule shell in supplements.',
    'cmc': 'Carboxymethyl cellulose (CMC / E466/INS 466) is a water-soluble cellulose derivative used as a thickener, stabiliser and texture modifier in ice cream, beverages, bakery products and pharmaceuticals.',
    'carboxymethyl cellulose': 'Sodium carboxymethyl cellulose (CMC / E466/INS 466), a water-soluble modified cellulose widely used as a thickener, stabiliser and water-binding agent in ice cream, beverages and pharmaceuticals.',
    'sodium carboxymethyl cellulose': 'The sodium salt of carboxymethyl cellulose (E466/INS 466), a semisynthetic food gum derived from natural cellulose used as a thickener, stabiliser and texture modifier.',
    'e466': 'E466/INS 466 is sodium carboxymethyl cellulose (CMC), a cellulose-derived thickener and stabiliser approved by FSSAI, EU and CODEX for use in ice cream, beverages, sauces and bakery products.',
    # Emulsifiers
    'datem': 'Diacetyl tartaric acid esters of mono- and diglycerides of fatty acids (E472e/INS 472e), a synthetic emulsifier made from edible fats and tartaric acid. Used primarily in baked goods to improve dough strength, volume and crumb structure.',
    'e472e': 'E472e/INS 472e is DATEM, a synthetic emulsifier used in bread and baked goods to strengthen gluten and improve loaf volume. Approved by FSSAI, EU, FDA and CODEX at specified limits.',
    'sodium stearoyl lactylate': 'An emulsifier and dough conditioner (E481/INS 481) produced by esterification of stearic acid with lactic acid, neutralised with sodium hydroxide. Approved by FDA, EU and FSSAI for use in bread, cakes and pastry products.',
    'ssl': 'Sodium stearoyl lactylate (E481/INS 481), a bread and pastry emulsifier made from stearic acid and lactic acid. Improves volume and softness of baked goods.',
    'e481': 'E481/INS 481 is sodium stearoyl lactylate (SSL), an emulsifier and dough conditioner used in bread, pastry and other baked goods. Approved by FSSAI, EU and FDA at specified limits.',
    'calcium stearoyl lactylate': 'A calcium-based emulsifier (E482/INS 482) similar to sodium stearoyl lactylate, produced by reacting stearic acid with lactic acid. Used as a dough conditioner and emulsifier in bakery products.',
    'e482': 'E482/INS 482 is calcium stearoyl lactylate (CSL), an emulsifier used in baked goods. Approved by EU and CODEX at specified limits.',
    # Sweeteners
    'mannitol': 'A naturally occurring sugar alcohol (E421/INS 421) found in mushrooms, seaweed and various fruits. Used as a low-calorie sweetener, bulking agent and anticaking agent. Has a tooth-friendly property as it is not fermented by oral bacteria.',
    'e421': 'E421/INS 421 is mannitol, a natural sugar alcohol from mushrooms and fruits. Approved by FSSAI, EU and CODEX as a sweetener and bulking agent. Laxative effect at doses above 20g/day.',
    'isomalt': 'A sugar alcohol (E953/INS 953) derived from sucrose by enzymatic isomerisation followed by hydrogenation. Half as sweet as sugar, with fewer calories and no impact on blood glucose. Used in sugar-free confectionery and chewing gum.',
    'e953': 'E953/INS 953 is isomalt, a sucrose-derived sugar alcohol used in sugar-free confectionery, chocolates and chewing gum. Approved by FSSAI, EU and CODEX. Laxative effect at high doses.',
    'steviol glycosides': 'The sweet compounds (E960/INS 960) naturally present in the leaves of the stevia plant (Stevia rebaudiana), 200–350 times sweeter than sucrose. Zero-calorie and non-glycaemic. Approved by FSSAI, EU, FDA (GRAS) and CODEX for use in beverages and foods.',
    'stevia': 'A natural plant-based sweetener extracted from Stevia rebaudiana leaves. The steviol glycosides are 200–350 times sweeter than sugar with zero calories and no effect on blood glucose. Approved by FSSAI, EU and FDA as a food additive (E960/INS 960).',
    'e960': 'E960/INS 960 is steviol glycosides (stevia extract), a natural zero-calorie sweetener approved by FSSAI, EU, FDA and CODEX. 200-350 times sweeter than sugar with no glycaemic impact.',
    'erythritol': 'A naturally occurring sugar alcohol (E968/INS 968) produced by fermentation of glucose by yeasts. Found in small amounts in grapes, melons and fermented foods. Zero calorie, zero glycaemic impact, and remarkably well-tolerated compared to other polyols. EU approved since 2008.',
    'e968': 'E968/INS 968 is erythritol, a fermentation-derived sugar alcohol with zero calories and zero glycaemic impact. Better tolerated than other polyols. Approved by EU and CODEX.',
    'xylitol': 'A naturally occurring sugar alcohol (E967/INS 967) found in birch wood, plums, strawberries and many vegetables. Widely used as a tooth-friendly sweetener in chewing gum and dental products. About the same sweetness as sugar but with 40% fewer calories. Highly toxic to dogs.',
    'e967': 'E967/INS 967 is xylitol, a natural sugar alcohol sweetener with dental health benefits (prevents cavity-causing bacteria). Approved by FSSAI, EU and FDA. Laxative at high doses. Toxic to dogs.',
    'neotame': 'An artificial sweetener (E961/INS 961) derived from aspartame but significantly more potent — 7,000 to 13,000 times sweeter than sucrose. Unlike aspartame, it does not require phenylketonuria warnings as it does not release significant phenylalanine.',
    'e961': 'E961/INS 961 is neotame, an ultra-high intensity artificial sweetener approved by FDA (2002), EU (2010) and CODEX. Unlike aspartame, it does not require PKU warnings.',
    # Anticaking & Mineral Salts
    'magnesium carbonate': 'A naturally occurring mineral salt (E504/INS 504) used as an anticaking agent in table salt and food powders, and as a dietary magnesium supplement and acidity regulator in food products.',
    'e504': 'E504/INS 504 is magnesium carbonate, a natural mineral used as an anticaking agent and dietary magnesium supplement. Approved by FSSAI, EU and CODEX.',
    'potassium chloride': 'A mineral salt (E508/INS 508) identical in structure to common salt but with potassium instead of sodium. Used as a sodium-reduced salt substitute in low-sodium foods and as a mineral supplement.',
    'e508': 'E508/INS 508 is potassium chloride, a natural mineral salt used as a sodium substitute in low-sodium products and as a potassium supplement. Approved by FSSAI, EU and CODEX.',
    'calcium chloride': 'A mineral salt (E509/INS 509) used as a firming agent, anticaking agent and mineral supplement. Commonly used in cheese making (for curd firming), tofu production and as a preservative in canned vegetables.',
    'e509': 'E509/INS 509 is calcium chloride, a mineral firming agent used in cheese making, tofu production and canned vegetables. Provides dietary calcium. Approved by FSSAI, EU and CODEX.',
    'calcium sulfate': 'A naturally occurring mineral (E516/INS 516) also known as gypsum. Used as a firming agent in tofu, a calcium supplement and an acidity regulator. The primary ingredient in traditional tofu production.',
    'e516': 'E516/INS 516 is calcium sulfate (gypsum), a natural mineral used as a firming agent in tofu, bread and vegetable products. Provides dietary calcium. Approved by FSSAI, EU and CODEX.',
    'magnesium oxide': 'A naturally occurring mineral oxide (E530/INS 530) used as an anticaking agent in food powders and as a dietary magnesium supplement with antacid properties.',
    'e530': 'E530/INS 530 is magnesium oxide, a mineral used as an anticaking agent and magnesium supplement in food products. Approved by EU and CODEX.',
    'e551': 'E551/INS 551 is silicon dioxide, a naturally occurring mineral used as an anticaking agent in powdered foods, spices and salt. Approved by FSSAI, EU and CODEX. Amorphous form is safe; crystalline silica (from different sources) is the occupational hazard.',
    # Flavour Enhancers (additional)
    'glutamic acid': 'The free amino acid form of MSG (E620/INS 620), a naturally occurring amino acid that contributes the umami taste found in fermented products, cheese, tomatoes and mushrooms. Unlike MSG it carries no sodium. Present in high amounts in Parmesan, soy sauce, miso and dried mushrooms.',
    'e620': 'E620/INS 620 is L-glutamic acid, the free amino acid form of MSG naturally found in high-protein fermented foods. Approved by FSSAI, EU and CODEX at specified limits. Same general safety profile as MSG.',
    'disodium ribonucleotides': 'A commercially prepared blend of disodium guanylate (E627) and disodium inosinate (E631) in a 1:1 ratio (E635/INS 635). Used in snack foods, instant noodles and savoury seasonings to intensify umami flavour synergistically with MSG. FSSAI and EU permit up to 500 mg/kg in most processed food categories. Raises uric acid — avoid if you have gout or hyperuricaemia. Not suitable for infants.',
    'e635': 'E635/INS 635 is Disodium 5\'-ribonucleotides, a combined nucleotide flavour enhancer (E627 + E631 in 1:1 ratio) used in crisps, instant noodles and processed savoury foods. FSSAI (India) and EU limit use to 500 mg/kg in most processed food categories. Raises uric acid — avoid if you have gout or hyperuricaemia. Not recommended for infants and young children. Those with MSG sensitivity may also react.',
    # Modified Starches
    'modified starch': 'Starch that has been physically, enzymatically or chemically treated to alter its properties — including freeze-thaw stability, thickening power, clarity and resistance to heat and acid. Approved by FSSAI, EU and CODEX at quantum satis in most food categories.',
    'acetylated distarch adipate': 'A cross-linked and acetylated modified starch (E1422/INS 1422) with excellent stability for freeze-thaw applications, high-temperature processing and acidic products. EFSA confirmed ADI "not specified" in 2017. FSSAI and CODEX approved.',
    'e1422': 'E1422/INS 1422 is acetylated distarch adipate, a modified starch used in sauces, yoghurts, dressings and canned foods for its freeze-thaw and heat-acid stability. Approved by FSSAI, EU, CODEX and FDA.',
    'hydroxypropyl distarch phosphate': 'A cross-linked hydroxypropylated modified starch (E1442/INS 1442) with excellent stability under heating, cooling, shear and acidic conditions. One of the most widely used modified starches globally in dairy, sauces and processed foods.',
    'e1442': 'E1442/INS 1442 is hydroxypropyl distarch phosphate, one of the most widely used food-grade modified starches. Approved by FSSAI, EU, CODEX and FDA. EFSA confirmed ADI "not specified" in 2017.',
    'starch sodium octenyl succinate': 'An emulsifying modified starch (E1450/INS 1450) with hydrophobic character, used as an encapsulant for flavours and oils in powdered foods and beverages. EFSA confirmed ADI "not specified". Approved by FSSAI, EU and CODEX.',
    'e1450': 'E1450/INS 1450 is starch sodium octenyl succinate, an emulsifying modified starch used in spray-dried flavours, powdered beverages and infant formula. Approved by FSSAI, EU and CODEX.',
    'distarch phosphate': 'A cross-linked modified starch (E1412/INS 1412) made by reacting starch with phosphorus oxychloride or sodium trimetaphosphate. Provides improved stability to heat and acid. Approved by FSSAI, EU and CODEX.',
    'e1412': 'E1412/INS 1412 is distarch phosphate, a cross-linked modified starch approved by FSSAI, EU and CODEX for use in sauces, soups and processed foods.',
    'acetylated starch': 'A mildly modified starch (E1420/INS 1420) treated with acetic anhydride to introduce acetyl groups, improving texture, clarity and freeze-thaw stability. Approved by FSSAI, EU and CODEX.',
    'e1420': 'E1420/INS 1420 is acetylated starch, a mildly modified food starch approved by FSSAI, EU and CODEX for use as a thickener and stabiliser.',
    # Antifoaming / Processing Aids
    'dimethyl polysiloxane': 'A silicon-based antifoaming agent (E900/INS 900) used in frying oils, cooking fats and some beverages to prevent excessive foam. Also the polymer in which potatoes are fried at fast-food restaurants. FDA GRAS; EU and CODEX approved at ≤10mg/kg in frying oils.',
    'dimethylpolysiloxane': 'Same as dimethyl polysiloxane (E900/INS 900), a silicon-based antifoaming agent approved for use in cooking oils and some beverages at FDA GRAS and EU/CODEX permitted levels.',
    'e900': 'E900/INS 900 is dimethylpolysiloxane, a silicon antifoaming agent used in frying oils, cooking fats and some beverages. FDA GRAS; approved by EU and CODEX at ≤10mg/kg in frying oils.',
    # Acidity Regulators
    'acetic acid': 'The organic acid that gives vinegar its sharp taste and smell (E260/INS 260). Naturally produced by fermentation of sugars. One of the oldest food preservatives, used in pickling and as a flavouring and acidity regulator.',
    'e260': 'E260/INS 260 is acetic acid (ethanoic acid), the active component of vinegar. Approved by FSSAI, EU and CODEX as a preservative, acidulant and flavouring. One of the safest food acids in common use.',
    'sodium acetate': 'The sodium salt of acetic acid (E262i/INS 262i), used as an acidity regulator, preservative and mild salt-and-vinegar flavouring in bread, chips and savoury snacks.',
    'e262': 'E262/INS 262 is sodium diacetate (or acetates), an acidity regulator and mild preservative approved by FSSAI, EU and CODEX in bakery and snack products.',
    'tartaric acid': 'A naturally occurring dicarboxylic acid found abundantly in grapes (E334/INS 334). One of the most common organic acids in wine, also produced industrially. Used as an acidulant in confectionery, baked goods and as the "sour" component of cream of tartar.',
    'e334': 'E334/INS 334 is L-tartaric acid, a natural grape-derived acidulant used in confectionery, baked goods and beverages. Approved by FSSAI, EU and CODEX. EFSA confirmed ADI of 30mg/kg body weight.',
    'cream of tartar': 'Potassium hydrogen tartrate (E336/INS 336i), a natural salt deposited on the inside of wine barrels during fermentation. Used as a stabiliser for whipped egg whites, in baking powder and as a leavening acid.',
    'sodium citrate': 'The sodium salt of citric acid (E331/INS 331), used as an acidity regulator, emulsifying salt in processed cheese, buffer in beverages and sequestrant in food products.',
    'e331': 'E331/INS 331 is sodium citrate, used as an acidity regulator and emulsifying salt in processed cheese, beverages and pharmaceutical formulations. Approved by FSSAI, EU and CODEX.',
    'calcium citrate': 'The calcium salt of citric acid (E333/INS 333), used as a firming agent, sequestrant and as a well-absorbed dietary calcium supplement in food and pharmaceutical products.',
    'e333': 'E333/INS 333 is calcium citrate, a firming agent and highly bioavailable calcium supplement approved by FSSAI, EU and CODEX.',
    'calcium carbonate': 'A naturally occurring mineral (E170/INS 170) found in chalk, limestone and marble. Used as an anticaking agent, white colorant, calcium supplement and pH regulator. Excellent calcium source with about 40% elemental calcium.',
    'e170': 'E170/INS 170 is calcium carbonate (chalk/limestone), a natural mineral used as a white colorant, calcium supplement, anticaking agent and pH regulator. Approved by FSSAI, EU and CODEX.',
    'sodium hydroxide': 'A strong alkali (E524/INS 524) used as a pH adjuster in food processing. Used in lye pretzels, olives and traditional ramen noodles. Food-grade sodium hydroxide is highly purified.',
    'e524': 'E524/INS 524 is sodium hydroxide (lye/caustic soda), a strong pH adjuster used in food processing for olives, pretzels and some Asian noodles. Approved by FSSAI, EU and CODEX for food use.',
    'calcium hydroxide': 'A mild alkali (E526/INS 526) known as slaked lime. Used in the nixtamalisation of maize (traditional corn tortilla process) to improve nutrition and flavour. Also used in water treatment and as a food firming agent.',
    'e526': 'E526/INS 526 is calcium hydroxide (slaked lime), used in nixtamalisation of corn, as a firming agent and acidity regulator. Approved by FSSAI, EU and CODEX.',
    # Enzymes
    'amylase': 'A naturally occurring enzyme (E1100/INS 1100) that breaks down starch into simpler sugars. Naturally present in human saliva, pancreatic fluid and many food-grade microorganisms. Used in baking to improve dough fermentation, bread volume and freshness.',
    'e1100': 'E1100/INS 1100 is alpha-amylase, a natural enzyme used as a flour treatment agent in baking. Approved by FSSAI, EU and FDA as GRAS. Produced from Bacillus subtilis or Aspergillus oryzae for food-grade use.',
    'lipase': 'A class of naturally occurring enzymes that break down fats (triglycerides) into glycerol and fatty acids. Used as processing aids in cheese making, baking and as a digestive enzyme supplement. GRAS in USA.',
    'protease': 'A broad class of naturally occurring enzymes that break down proteins into peptides and amino acids. Used in meat tenderising, cheese making, brewing and as digestive enzyme supplements. GRAS in USA.',
    'lactase': 'The enzyme (beta-galactosidase) that breaks down lactose into glucose and galactose. Added to dairy products to make them lactose-free. Also available as a digestive supplement for lactose-intolerant individuals.',
    # Nutritional ingredients
    'lecithin': 'A natural complex mixture of phospholipids found in egg yolk, soya and sunflower seeds. One of the most widely used food emulsifiers, present in chocolate, bread, margarine and many processed foods. May be sourced from soy (E322), sunflower or egg.',
    'sunflower lecithin': 'A natural emulsifier (E322) extracted from sunflower seeds, used as an allergen-free alternative to soy lecithin. It provides the same emulsifying functionality without soy allergen concerns.',
    'vanillin': 'The primary flavour compound in vanilla, also produced commercially by chemical synthesis from lignin or guaiacol. Approved by FDA, EU and CODEX as a generally safe flavouring. About 95% of "vanilla" flavouring used worldwide is synthetic vanillin.',
    'ethyl vanillin': 'A synthetic vanilla flavouring compound structurally similar to vanillin but 3–4 times more potent. Used as a vanilla flavour enhancer or substitute in chocolate, confectionery and baked goods. Approved by FDA, EU and CODEX.',
    'dextrose': 'Glucose (dextrose monohydrate) produced by the hydrolysis of starch, usually from corn or wheat. The primary energy source for the human body. Used as a sweetener, fermentation substrate and texture agent in bakery, confectionery and sports foods.',
    'fructose': 'A naturally occurring simple sugar found in fruits, honey and many vegetables. Commercially produced from high-fructose corn syrup or inversion of sucrose. Sweeter than sucrose. Regular high intake from added fructose is linked to fatty liver and metabolic concerns.',
    'lactose': 'The primary sugar in mammalian milk, consisting of glucose and galactose. Used as a filler, sweetener and texture agent in pharmaceuticals and some food products. Cannot be digested by individuals who lack the lactase enzyme (lactose intolerance).',
    'casein': 'The primary milk protein (about 80% of cow\'s milk protein), present in milk as a suspension of micelles. A slow-digesting, high-quality complete protein. Used in cheese, dairy products and as a protein supplement. Dairy allergen — must be declared.',
    'whey': 'The liquid byproduct of cheese making, processed into whey protein concentrate or isolate. A fast-digesting complete protein containing all essential amino acids. Used in protein supplements, infant formula and bakery products. Dairy allergen — must be declared.',
    'pea protein': 'A plant-based protein extracted from yellow split peas (Pisum sativum) by aqueous processing. Hypoallergenic and naturally free from the top 8 allergens. Used in plant-based meat alternatives, protein powders and dairy-free products.',
    'soy protein': 'Protein isolated from defatted soybean flakes. A complete plant protein used in meat analogues, infant formula and protein supplements. Soy is one of the 14 major allergens in the EU and 8 major allergens in the USA — mandatory declaration required.',
    'rice protein': 'A hypoallergenic plant protein extracted from brown rice by enzymatic processing. Used in protein supplements and plant-based foods. Popular choice for those with soy or dairy sensitivities.',
    'oat bran': 'The outer bran layer of the oat grain, exceptionally rich in beta-glucan (a soluble fibre). Beta-glucan from oat bran has EFSA-approved and FDA-approved health claims for reducing LDL cholesterol and risk of heart disease.',
    'psyllium husk': 'The outer coating (husk) of psyllium seeds (Plantago ovata), a rich source of soluble dietary fibre. Used in fibre supplements and IBS management. FDA has approved a health claim for psyllium husk reducing the risk of heart disease.',
    'wheat bran': 'The outer layers of the wheat grain, a rich source of insoluble dietary fibre. Used in high-fibre breads, breakfast cereals and supplements to promote digestive regularity and colon health.',
    'flaxseed': 'The seeds of the flax plant (Linum usitatissimum). Rich in ALA omega-3 fatty acids, lignans and soluble fibre. Best consumed ground (milled) as whole seeds may pass through the gut undigested.',
    'chia seeds': 'Tiny seeds from the Salvia hispanica plant, native to Mexico. Rich in ALA omega-3 fatty acids, soluble dietary fibre, protein and calcium. Absorb water to form a gel. Used in beverages, desserts and functional foods.',
    'canola oil': 'A vegetable oil derived from low-erucic acid rapeseed (Brassica napus / Brassica rapa). One of the most widely used cooking oils globally for its high smoke point, mild flavour and low saturated fat content.',
    'sunflower oil': 'A light vegetable oil extracted from sunflower seeds (Helianthus annuus). High in linoleic acid (omega-6) and Vitamin E. Widely used in cooking, food manufacturing and cosmetics.',
    'rapeseed oil': 'A vegetable oil extracted from rapeseed, known as canola oil when from low-erucic acid varieties. High in monounsaturated fats and ALA omega-3. Widely used in food manufacturing and cooking.',
    'sesame oil': 'A vegetable oil cold-pressed from sesame seeds (Sesamum indicum), cultivated in India for over 5,000 years. Rich in sesamin, sesamol and gamma-tocopherol antioxidants. Sesame is an allergen that must be declared in many jurisdictions.',
    'rice bran oil': 'A vegetable oil extracted from the outer bran layer of rice grains. Contains oryzanol, a phytosterol with clinically studied cholesterol-lowering effects. High smoke point makes it popular for deep frying.',
    'groundnut oil': 'Peanut oil (Arachis oil) extracted from peanuts (Arachis hypogaea). Widely used in Indian cooking for its high smoke point. Peanut is a major allergen — must be declared on packaging.',
    'mustard oil': 'A pungent oil extracted from mustard seeds (Brassica juncea), widely used in Indian, Bengali and Punjabi cooking. Contains allyl isothiocyanate (the sharp flavour compound) and erucic acid, which is subject to regulatory limits in some countries when used in imported food.',
    'groundnut': 'The Indian term for peanut (Arachis hypogaea), one of the most important oilseed crops in India. Rich in protein and healthy monounsaturated fats. Peanut is one of the most common and severe food allergens globally.',
    'sea salt': 'Salt produced by evaporation of seawater, retaining small amounts of trace minerals (magnesium, calcium, potassium) compared to refined table salt. Used as a seasoning and exfoliant. The same dietary considerations as regular salt apply.',
    'dextrose monohydrate': 'The hydrated crystalline form of glucose (dextrose), produced from starch hydrolysis. Used as a fermentation substrate, sweetener and texture agent in bread, confectionery and sports nutrition products.',

    # ── Cosmetic & Skincare Actives ────────────────────────────────────────────
    'niacinamide': 'Niacinamide (nicotinamide) is the amide form of Vitamin B3, a water-soluble vitamin found in meat, fish, eggs and green vegetables. Extensively studied in dermatology for its ability to reduce hyperpigmentation, minimise pore appearance, strengthen the skin barrier, reduce sebum production and improve fine lines. One of the best-tolerated cosmetic actives.',
    'nicotinamide': 'The amide form of Vitamin B3 (identical to niacinamide), used in skincare for skin-brightening and anti-inflammatory effects. Also used clinically as a dietary supplement for pellagra prevention and niacin deficiency.',
    'sodium hyaluronate': 'The sodium salt of hyaluronic acid, the primary moisture-binding molecule in the skin. Lower molecular weight than hyaluronic acid, allowing deeper penetration into the stratum corneum. Used extensively in serums and moisturisers for intense hydration.',
    'kojic acid': 'A naturally occurring chelation agent produced during fermentation of rice (sake production) and by Aspergillus and Penicillium fungi. Used in skincare as a tyrosinase inhibitor to reduce melanin production. Approved in Japan (1%); EU Cosmetics Regulation evaluated at 1% in face care products.',
    'alpha arbutin': 'A biosynthetic glycoside of hydroquinone derived from bearberry (Arctostaphylos uva-ursi). The alpha form is more stable and effective than beta-arbutin. Used in skincare as a skin-brightening agent. EU Cosmetics Regulation permits alpha-arbutin at up to 2% in face care.',
    'arbutin': 'A natural glycoside of hydroquinone found in bearberry, blueberry and cranberry plants. Used in skincare to reduce dark spots by inhibiting tyrosinase. EU permits alpha-arbutin at 2% (face) and 0.5% (body).',
    'glycolic acid': 'The smallest alpha hydroxy acid (AHA), derived from sugar cane (E-glycolic acid / Hydroxyacetic acid). Used as a chemical exfoliant in skincare to dissolve dead skin cells, improve texture, stimulate collagen and treat hyperpigmentation. FDA and EU approved for cosmetic use at specified concentrations.',
    'azelaic acid': 'A naturally occurring saturated dicarboxylic acid found in wheat, rye and barley, also produced by Malassezia yeasts on the skin. Prescription-strength (15–20%) is approved by FDA for acne and rosacea. OTC concentrations (≤10%) are widely available in skincare.',
    'bakuchiol': 'A meroterpene phenol extracted from the seeds and leaves of Psoralea corylifolia (babchi plant), used in Ayurvedic medicine. Clinical studies show retinol-like anti-ageing effects (collagen synthesis, skin smoothing) with significantly lower irritation. Safe in pregnancy unlike retinol.',
    'squalane': 'A stable, saturated form of squalene (a natural lipid found in the skin\'s sebum and shark liver), derived by hydrogenating plant-sourced squalene (from sugarcane, olive or amaranth). A lightweight, non-comedogenic, skin-identical emollient. Very well tolerated.',
    'centella asiatica': 'A tropical medicinal herb (Cica / Gotu kola) used in Ayurvedic, Chinese and African traditional medicine. Its active compounds (madecassoside, asiaticoside, asiatic acid) have clinically demonstrated wound-healing, anti-inflammatory and collagen-stimulating properties.',
    'allantoin': 'A naturally occurring phytochemical found in comfrey root, burdock root and sugar beet. Used in skincare for its soothing, keratolytic (softening) and wound-healing properties. CIR Expert Panel confirmed it safe for cosmetic use. Very well tolerated, including on sensitive skin.',
    'bisabolol': 'A naturally occurring sesquiterpene alcohol first isolated from German chamomile (Matricaria chamomilla) and also produced synthetically. Widely used in skincare for anti-inflammatory, anti-irritant, soothing and skin-penetration-enhancing properties. CIR reviewed and confirmed safe.',
    'adenosine': 'A naturally occurring nucleoside found in all living organisms, a building block of DNA. Used in skincare for its anti-ageing effects. EU Cosmetics Regulation approved at 0.04% in face care for skin smoothing. Well tolerated in clinical studies.',
    'zinc oxide': 'A naturally occurring mineral compound of zinc and oxygen (ZnO). Used as a broad-spectrum physical (mineral) UV filter in sunscreens (reflects both UVA and UVB), as a soothing anti-inflammatory agent in skin creams and as a baby powder ingredient. FDA approved Category I UV filter.',
    'zinc pyrithione': 'A zinc complex of the pyrithione ion (ZPT), used as the primary antifungal and antibacterial agent in anti-dandruff shampoos since the 1960s. Effective against Malassezia furfur, the yeast associated with dandruff and seborrhoeic dermatitis. EU Cosmetics Regulation updated restrictions in 2021.',
    'madecassoside': 'A key active compound from Centella asiatica, clinically studied for its wound-healing, collagen-stimulating and anti-inflammatory effects. Used as a concentrated active in skincare products for sensitive and damaged skin.',
    'sea buckthorn oil': 'A nutrient-dense oil from the berries and seeds of Hippophae rhamnoides. Exceptionally rich in Vitamin C, Vitamin E, carotenoids (including beta-carotene) and rare omega-7 (palmitoleic acid). Used in skincare for anti-ageing and wound-healing properties.',
    'rosehip oil': 'A plant oil cold-pressed from the seeds of wild rose (Rosa canina) hips. Rich in linoleic acid, alpha-linolenic acid and naturally occurring trans-retinoic acid. Widely used in skincare for anti-ageing, scar reduction and brightening.',
    'octinoxate': 'Ethylhexyl methoxycinnamate (OMC), a UV-B absorbing organic UV filter and one of the most widely used chemical sunscreen actives globally. Under regulatory review in some jurisdictions for potential endocrine activity and coral reef toxicity.',
    'oxybenzone': 'Benzophenone-3, an organic UV-A and UV-B absorbing filter used in chemical sunscreens. Penetrates the skin and is detected in blood, urine and breast milk. Associated with endocrine disruption concerns and coral bleaching. Banned for reef protection in Hawaii, Palau and the US Virgin Islands.',
    'avobenzone': 'Butyl methoxydibenzoylmethane, the most widely used UVA-only organic UV filter globally. Photounstable without stabilisers (e.g., octocrylene, homosalate). EU and FDA approved at specified concentrations.',
    'octocrylene': 'An organic UV-B and short UVA filter used in sunscreens to stabilise avobenzone and improve water resistance. Under study for potential accumulation in coral polyps. Approved by EU and FDA at specified limits.',
    'charcoal': 'Activated charcoal made by heating carbon-rich material (wood, coconut shells) at very high temperatures. Used in skincare as a purifying and pore-cleansing agent due to its high surface area and adsorptive capacity. Also used as a tooth-whitening ingredient and in medical activated charcoal for emergency poisoning.',

    # ── Indian Herbs & Ayurvedic Ingredients ───────────────────────────────────
    'amla': 'Indian gooseberry (Phyllanthus emblica / Emblica officinalis), one of the richest natural sources of Vitamin C. A cornerstone of Ayurvedic medicine (a rasayana — rejuvenating herb) for over 3,000 years. Widely used in hair oils, supplements, chutneys and traditional formulations. Rich in tannins, polyphenols and Vitamin C.',
    'amalaki': 'Another name for amla (Phyllanthus emblica / Indian gooseberry), one of the three fruits in triphala. A key Ayurvedic rejuvenative herb (rasayana) rich in Vitamin C and polyphenols.',
    'brahmi': 'Bacopa monnieri, a creeping marsh herb used in Ayurvedic medicine for over 3,000 years as a brain tonic (medhya rasayana). Clinically studied for cognitive enhancement and stress reduction. Used in supplements and hair oils.',
    'bhringraj': 'Eclipta prostrata (Eclipta alba), a traditional Ayurvedic herb used primarily in hair care. Known as "kesharaj" or "ruler of hair" in Sanskrit. Used in hair oils and shampoos for hair strengthening and promoting hair growth.',
    'shikakai': 'The pods, bark and leaves of Acacia concinna, a plant native to Asia. Rich in saponins that create a mild lather. Used for centuries in India as a natural hair cleanser, conditioner and mild shampoo alternative. Low pH is gentle on the hair shaft.',
    'reetha': 'The dried fruit shells of the soapnut tree (Sapindus mukorossi), also known as aritha or soapberry. Contains approximately 15% saponins, which create a natural lather. Used for centuries in India as a natural hair cleanser and laundry detergent.',
    'soapnut': 'The dried fruit of the soapberry tree (Sapindus mukorossi), known as reetha in Hindi. The shells contain 15% saponins, used as a natural surfactant and biodegradable cleanser in hair care, laundry and general cleaning.',
    'triphala': 'A traditional Ayurvedic herbal formulation containing three dried fruits: amla (Emblica officinalis), haritaki (Terminalia chebula) and bibhitaki (Terminalia bellirica) in equal proportions. One of the most prescribed formulations in Ayurveda for digestive, liver and ocular health.',
    'giloy': 'Tinospora cordifolia, known as "guduchi" or "amrita" (divine nectar) in Ayurveda. A climbing herb used as an immunomodulator and adaptogen. One of the three plants considered "divya aushadhi" (divine medicines) in classical Ayurvedic texts.',
    'guduchi': 'Another name for giloy (Tinospora cordifolia), an important Ayurvedic immunomodulatory herb used for fever, immunity and as a general tonic.',
    'moringa': 'Moringa oleifera, the drumstick tree or "miracle tree," native to the foothills of the Himalayas in northwestern India. The leaves are exceptionally nutrient-dense — rich in vitamins A, C, E, B vitamins, calcium, potassium, iron and all essential amino acids.',
    'karela': 'Bitter gourd or bitter melon (Momordica charantia), used extensively in Indian cooking and Ayurvedic medicine. Traditionally used for blood sugar management. Contains charantin, vicine and polypeptide-p which may help lower blood glucose.',
    'methi': 'Fenugreek (Trigonella foenum-graecum), one of the oldest cultivated medicinal plants native to India and the Mediterranean. Used as a spice, herb and medicinal plant for hair strengthening (in oils), blood sugar management and digestive health.',
    'mulethi': 'Licorice root (Glycyrrhiza glabra), used in Ayurvedic and Chinese medicine as a soothing, anti-inflammatory and expectorant herb. Used in oral care products, skin brightening formulations (inhibits tyrosinase) and respiratory health supplements.',
    'chandan': 'Sandalwood (Santalum album), a prized aromatic heartwood native to peninsular India. The oil and powder are used in skincare for their cooling, anti-inflammatory and antimicrobial properties. Used in perfumery, religious ceremonies and Ayurvedic preparations.',
    'haritaki': 'Terminalia chebula, known as the "king of medicines" in Tibetan medicine and one of the three fruits of triphala. Used in Ayurveda as a digestive tonic, mild laxative and rejuvenative herb.',
    'bibhitaki': 'Terminalia bellirica, one of the three fruits in the triphala formulation. Used in Ayurvedic medicine for respiratory health, digestive support and as a mild laxative.',
    'shatavari': 'Asparagus racemosus, a climbing plant whose tuberous roots are used in Ayurvedic medicine as the primary female reproductive tonic. Used to support reproductive health, lactation and as an adaptogen.',
    'multani mitti': 'Fuller\'s earth, a naturally occurring clay mineral rich in magnesium, aluminium, iron and silica deposits. Used extensively in Indian traditional beauty care as a face mask for its absorbent, pore-cleansing and oil-controlling properties.',
    'kaolin': 'A naturally occurring soft white clay mineral (aluminium silicate) mined worldwide. Used as a mild absorbent and mattifying ingredient in face masks, cosmetics and pharmaceutical tablet fillings.',
    'noni': 'The fruit of Morinda citrifolia, a plant native to Southeast Asia and the Pacific. Used in traditional Polynesian and Ayurvedic medicine. The fruit, leaves and bark are used in supplements for antioxidant and immune-supporting properties.',

    # ── Common Grain & Flour Ingredients ─────────────────────────────────────
    'refined wheat flour': 'Refined wheat flour (Maida) is produced by milling wheat and removing the bran and germ, leaving mainly the starchy endosperm. It is the base ingredient in breads, noodles, biscuits and pastries. Refining removes most fibre, vitamins and minerals; has a high glycaemic index.',
    'wheat flour': 'Wheat flour produced by grinding whole wheat grains. The most widely used cereal flour globally, the foundation of bread, pasta, noodles and baked goods. Contains gluten — not suitable for those with coeliac disease or wheat allergy.',
    'maida': 'Maida is the Indian term for refined white wheat flour, produced by milling wheat and sifting out the bran and germ. Very fine, high-starch flour with high glycaemic index. Used widely in Indian flatbreads, biscuits, noodles and fried snacks.',
    'wheat gluten': 'Wheat gluten is the natural protein network formed when wheat flour is hydrated and worked. It consists of glutenin and gliadin proteins and gives dough its elasticity and strength. Used as a protein supplement and dough strengthener in baked goods and noodles. Not suitable for coeliac or wheat-allergic individuals.',

    # ── Phosphates ────────────────────────────────────────────────────────────
    'pentasodium triphosphate': 'Pentasodium triphosphate (STPP / E451i / INS 451i) is a sodium salt of triphosphoric acid used as a sequestrant, moisture-retention agent and acidity regulator in processed foods including noodles, seafood and processed meats. Approved by FSSAI, EU and CODEX at specified limits.',
    'e451': 'E451/INS 451 is triphosphates (pentasodium or pentapotassium triphosphate), used as sequestrants and water-retention agents in processed foods. Approved by FSSAI, EU and CODEX. Excess phosphate intake is a concern for individuals with kidney disease.',
    'sodium triphosphate': 'Sodium triphosphate (STPP / E451i) is a food-grade phosphate salt used as a sequestrant and moisture retention agent in noodles, seafood products and processed meats. FSSAI and CODEX approved at specified limits.',
    'triphosphate': 'Triphosphates (E451/INS 451) are phosphate salts used as sequestrants, emulsifying salts and water-retention agents in processed and convenience foods. Approved by FSSAI and CODEX. Excess phosphate is a concern for kidney health at very high intakes.',

    # ── Iron Mineral ──────────────────────────────────────────────────────────
    'ferric pyrophosphate': 'Ferric pyrophosphate (E450 related / INS 450) is a water-insoluble iron compound used as a dietary iron fortification ingredient in foods such as instant noodles, cereals and flour. It has lower bioavailability than ferrous sulfate but causes less organoleptic (colour/taste) changes in food. Approved by FSSAI, WHO and CODEX for food fortification.',
    'ferrous sulfate': 'Ferrous sulfate is a highly bioavailable iron salt used for dietary iron fortification in foods and as a supplement for iron-deficiency anaemia treatment. Approved by FSSAI, WHO and CODEX for food fortification.',

    # ── Common Spices (Indian) ────────────────────────────────────────────────
    'onion powder': 'Dehydrated and ground onion (Allium cepa), used as a convenient flavouring in spice blends, soups, seasonings and instant foods. Retains most of the flavour compounds (organosulfur compounds) present in fresh onion. Safe and widely used globally.',
    'garlic': 'Garlic (Allium sativum), one of the most ancient and widely used culinary ingredients worldwide. Rich in allicin and organosulfur compounds with well-documented antimicrobial and cardiovascular-protective properties. Used fresh, dried or as powder in cooking and supplements.',
    'garlic powder': 'Dehydrated and ground garlic (Allium sativum), used as a convenient flavouring in spice blends, seasonings and processed foods. Retains organosulfur flavour compounds. Safe and widely used globally.',
    'red chilli': 'Dried red chilli (Capsicum annuum / Capsicum frutescens), one of the most widely used spices in Indian cooking. The pungent heat comes from capsaicin. Rich in Vitamin C, beta-carotene and antioxidants. Safe at culinary levels; capsaicin may irritate the gastrointestinal tract in sensitive individuals.',
    'red chilli powder': 'Ground dried red chilli (Capsicum annuum), a staple spice in Indian cuisine. Provides heat from capsaicin and colour from carotenoids (capsanthin). Rich in Vitamin C and antioxidants. Safe at normal culinary levels.',
    'ginger': 'Ginger (Zingiber officinale), a rhizome used as a spice and traditional medicine across Asia for over 5,000 years. The pungency comes from gingerols (fresh) and shogaols (dried). Well-documented as an anti-nausea, anti-inflammatory and digestive aid. Safe at culinary and supplement levels.',
    'ginger powder': 'Dried and ground ginger (Zingiber officinale), used as a spice in cooking and baking. Retains the bioactive shogaols and gingerols. Anti-inflammatory and digestive properties; safe at culinary levels.',
    'aniseed': 'Aniseed (Pimpinella anisum), a flowering plant whose seeds are used as a spice in Indian and Mediterranean cooking. Rich in anethole, which gives its characteristic sweet, liquorice-like flavour. Used in spice blends, digestive preparations and flavouring. Safe at culinary levels.',
    'black pepper': 'Black pepper (Piper nigrum), one of the most widely traded spices in history. Piperine is the active compound responsible for its pungency and also enhances the bioavailability of other nutrients (notably curcumin). Widely used in cooking globally; safe at normal dietary levels.',
    'clove': 'Cloves (Syzygium aromaticum), the dried flower buds of a tropical tree, one of the world\'s most prized spices. Rich in eugenol, which has potent antimicrobial, analgesic and antioxidant properties. Used in Indian cooking, oral care and traditional medicine. Safe at culinary levels.',
    'cardamom': 'Cardamom (Elettaria cardamomum), known as the "Queen of Spices," native to the Western Ghats of India. Used in Indian sweets, chai tea, biryanis and Ayurvedic medicine. Rich in cineole and terpene compounds with digestive and antioxidant properties. Safe at culinary levels.',
    'nutmeg': 'Nutmeg (Myristica fragrans), the seed of a tropical tree native to Indonesia, used as a warm spice in cooking and baking. Contains myristicin, elemicin and safrole. Safe at normal culinary amounts; very high doses (several teaspoons) can cause toxicity — not a concern at food levels.',
    'fenugreek': 'Fenugreek (Trigonella foenum-graecum), a legume whose seeds and leaves are used as a spice and medicinal herb across India and the Middle East. Rich in galactomannan (soluble fibre) and saponins. Traditionally used to support blood sugar management, digestion and lactation. Safe at culinary levels.',
    'coriander': 'Coriander (Coriandrum sativum), one of the world\'s oldest cultivated spice plants. Both leaves (cilantro) and seeds are used widely in Indian, Middle Eastern and Latin American cooking. Rich in linalool and other terpenes with antioxidant properties. Safe at normal culinary levels; rare allergies in those sensitive to other Apiaceae plants.',

    # ── Flavour Enhancers (name variants) ────────────────────────────────────
    "disodium 5'-ribonucleotides": 'Disodium 5\'-ribonucleotides (E635/INS 635) is a combined nucleotide flavour enhancer — a 1:1 blend of disodium guanylate (E627) and disodium inosinate (E631). Used in instant noodles, crisps, savoury seasonings and processed foods to synergistically intensify umami flavour with MSG. FSSAI (India) permits up to 500 mg/kg in processed foods; EU sets 500 mg/kg in most snacks and seasonings (Regulation EC 1333/2008 Annex II); CODEX permits quantum satis in certain categories. Should be avoided by people with gout or hyperuricaemia — nucleotides raise uric acid levels. Not recommended for infants and young children. Those sensitive to MSG may also react to nucleotide enhancers.',
    "disodium 5' ribonucleotides": 'Disodium 5\'-ribonucleotides (E635/INS 635), a combined nucleotide flavour enhancer used in savoury processed foods to boost umami flavour. FSSAI and EU limit use to 500 mg/kg in most processed food categories. Avoid if you have gout, high uric acid, or MSG sensitivity.',
    'disodium 5-ribonucleotides': 'Disodium 5\'-ribonucleotides (E635/INS 635), a combined nucleotide flavour enhancer (E627 + E631). Found on Maggi and other instant noodle labels. FSSAI and EU limit use to 500 mg/kg in most processed food categories. Raises uric acid — avoid if you have gout or hyperuricaemia. Not recommended for infants and young children.',

    # ── Hydrolysed Proteins ───────────────────────────────────────────────────
    'hydrolysed groundnut protein': 'Hydrolysed groundnut (peanut) protein is produced by breaking down peanut protein into amino acids and short peptides using acid, base or enzymatic hydrolysis. Used as a natural umami flavour enhancer in instant noodles, seasonings and soups. Contains free glutamates which contribute to savoury taste. Peanut allergen — must be declared on packaging.',
    'hydrolysed vegetable protein': 'Hydrolysed vegetable protein (HVP) is produced by breaking down plant proteins (soy, wheat, corn, groundnut) into amino acids and peptides. Rich in free glutamates, used as a natural umami flavour enhancer in soups, sauces, seasonings and instant noodles. May contain MSG-like amounts of glutamate.',
    'hydrolysed soy protein': 'Hydrolysed soy protein (HSP) is produced by enzymatic or acid hydrolysis of soy protein. Used as a flavour enhancer in savoury foods. Soy allergen — must be declared on packaging.',

    # ── Caramel Colour variants ────────────────────────────────────────────────
    'caramel iv': 'Caramel Colour Class IV (E150d/INS 150d), produced by heating carbohydrates with ammonium sulfite compounds. The most widely used caramel colour globally — in cola drinks, soy sauce and some noodle seasonings. Contains 4-methylimidazole (4-MEI), listed as a possible carcinogen (IARC Group 2B) in animal studies; California Prop 65 listed.',
    'caramel colour iv': 'Caramel Colour Class IV (E150d), the sulphite-ammonia process caramel colour. Contains 4-MEI, a possible carcinogen in animal studies; listed under California Prop 65. Widely used in cola drinks and savoury seasonings.',
    'e150d': 'E150d/INS 150d is Class IV caramel colour (sulphite-ammonia process). Contains 4-MEI, a possible carcinogen in animal studies. California Prop 65 listed. EU restricts use in certain beverage categories.',

    # ── Colorants E100–E199 (additions) ──────────────────────────────────────
    'e104': 'E104/INS 104 is Quinoline Yellow, a synthetic greenish-yellow food dye. Banned in USA, Australia and Japan; permitted in EU and India with mandatory "may have an adverse effect on activity and attention in children" warning. Used in smoked fish, ice creams and scotch eggs.',
    'quinoline yellow': 'Quinoline Yellow (E104/INS 104) is a synthetic greenish-yellow dye derived from coal tar. Banned in USA and Australia; EU requires an ADHD warning label on foods containing it. Used in some snacks, confectionery and medicines.',
    'e123': 'E123/INS 123 is Amaranth, a dark red-violet synthetic azo dye. Banned in USA (since 1976) due to carcinogenicity concerns; permitted in EU for caviar and fish roe only. Not widely used in Indian packaged foods.',
    'amaranth dye': 'Amaranth (E123) is a dark red synthetic azo dye banned in the USA. Permitted in the EU only for caviar. Not to be confused with the grain amaranth, which is a different, nutritious food.',
    'e140': 'E140/INS 140 is Chlorophylls and Chlorophyllins, natural green pigments extracted from plants. Used to colour foods, oils and beverages green. Completely natural and considered safe.',
    'chlorophyll': 'Chlorophyll (E140) is the natural green pigment found in all plants. As a food additive it is extracted and used to colour foods and beverages green. Safe and naturally derived.',
    'e141': 'E141/INS 141 is Copper Complexes of Chlorophylls, produced by replacing magnesium in chlorophyll with copper to give a stable bright green. Used in canned vegetables, peas and beverages. Generally safe.',
    'copper chlorophyll': 'Copper chlorophyll (E141) is a stabilised green colour made from plant chlorophyll. Used to give canned peas and vegetables a vivid green colour. Generally regarded as safe.',
    'e142': 'E142/INS 142 is Green S (Lissamine Green), a synthetic green food dye. Not approved in USA or Canada; permitted in EU and some Asian countries. Used in tinned peas, mint jelly and desserts.',
    'green s': 'Green S (E142/INS 142) is a synthetic green azo dye not approved in the USA. Permitted in the EU; used in peas, mint products and jellies.',
    'e150a': 'E150a/INS 150a is Plain Caramel, the simplest caramel colour made by heating carbohydrates without ammonium or sulfite compounds. Used in baked goods, syrups and confectionery. Does not contain 4-MEI.',
    'plain caramel': 'Plain Caramel (E150a) is caramel colour made without sulfite or ammonia compounds. Used in breads, syrups, and sauces. Considered the safest of the four caramel colour classes.',
    'e150b': 'E150b/INS 150b is Caustic Sulfite Caramel, made by heating carbohydrates with sulfite compounds. Used in some spirits and vinegars.',
    'e150c': 'E150c/INS 150c is Ammonia Caramel, made by heating carbohydrates with ammonium compounds. Contains some 4-MEI but less than Class IV. Used in beer, soy sauce and some confectionery.',
    'e151': 'E151/INS 151 is Brilliant Black BN (Black PN), a synthetic black azo dye. Not permitted in USA, Canada or Japan. Approved in EU; used in blackcurrant products, pastilles and some savoury foods.',
    'brilliant black': 'Brilliant Black BN (E151) is a synthetic black food dye banned in the USA. Permitted in the EU; used in liquorice, savoury snacks and some confectionery.',
    'e153': 'E153/INS 153 is Vegetable Carbon (activated charcoal), a natural black pigment made from charred plant material. Used to colour confectionery, jelly and cheese rinds black. Generally safe.',
    'vegetable carbon': 'Vegetable Carbon (E153) is activated charcoal from charred plant material. Used as a natural black food colour in biscuits, cheese and confectionery. Safe and naturally derived.',
    'e160a': 'E160a/INS 160a is Beta-Carotene, the orange pigment found naturally in carrots, sweet potatoes and many fruits. Used as a food colour and Vitamin A precursor. Converts to Vitamin A in the body; safe and beneficial.',
    'e160b': 'E160b/INS 160b is Annatto extract (bixin/norbixin), a natural orange-yellow colour from the seeds of the achiote tree. Widely used in cheese, butter, snacks and cereals. Generally safe but may cause allergic reactions in sensitive individuals.',
    'paprika extract': 'Paprika extract (E160c/INS 160c) is a natural red-orange colour derived from dried red peppers. Used in crisps, snacks, processed meats and sauces. Naturally derived and generally safe.',
    'e160c': 'E160c/INS 160c is Paprika extract (capsanthin/capsorubin), a natural red-orange colour from dried capsicum peppers. Used in snack foods, processed meats and cheese. Safe and naturally derived.',
    'lycopene': 'Lycopene (E160d/INS 160d) is a red carotenoid pigment found naturally in tomatoes, watermelon and guava. As a food additive it provides a natural red colour. Also studied as a dietary antioxidant.',
    'e160d': 'E160d/INS 160d is Lycopene, a natural red carotenoid from tomatoes. Used as a food colour in juices, soups and sauces. Also an antioxidant studied for potential health benefits.',
    'lutein': 'Lutein (E161b/INS 161b) is a yellow carotenoid pigment found in marigold flowers and egg yolks. Used as a natural yellow food colour. Also taken as a dietary supplement for eye health.',
    'e161b': 'E161b/INS 161b is Lutein, a natural yellow carotenoid used as a food colour. Extracted from marigold petals. Also important for eye health — accumulates in the retina.',
    'canthaxanthin': 'Canthaxanthin (E161g/INS 161g) is an orange-red carotenoid used as a food colour. Also used in fish farming to colour salmon flesh. High doses have been linked to retinal deposits.',
    'e161g': 'E161g/INS 161g is Canthaxanthin, an orange carotenoid colour. Used to colour certain foods and in aquaculture to give farmed salmon its pink colour. Generally safe at food use levels.',
    'e171': 'E171/INS 171 is Titanium Dioxide, a bright white pigment used in sweets, chewing gum, sauces and medicines. Banned as a food additive in the EU since 2022 due to genotoxicity concerns. Still permitted in India and the USA. Used in cosmetics and sunscreens as a UV filter.',
    'titanium dioxide': 'Titanium Dioxide (E171/INS 171) is a bright white food colour and opacity agent. Banned in the EU for food use since 2022 due to genotoxicity concerns. Still used in many countries including India in chewing gum, sweets and white sauces. Also a UV-blocking ingredient in sunscreens.',
    'e173': 'E173/INS 173 is Aluminium, a metallic silver food colour permitted only for decorating the surface of confectionery and cake decorations. Not for general food use. Aluminium accumulation in the body is a health concern at high exposures.',
    'e174': 'E174/INS 174 is Silver, a metallic food colour permitted only for decorating confectionery and chocolates. Used in edible silver leaf on sweets and cakes. Generally safe in tiny decorative amounts.',
    'e175': 'E175/INS 175 is Gold, a metallic food colour (edible gold leaf/gold powder) permitted only for decorating food surfaces. Chemically inert and safe in the tiny amounts used for decoration.',

    # ── Preservatives E200–E299 (additions) ──────────────────────────────────
    'sorbic acid': 'Sorbic acid (E200/INS 200) is a naturally occurring polyunsaturated fatty acid first isolated from rowan berries in 1859. Used as a preservative in cheese, baked goods, dried fruits and beverages. Generally regarded as safe; one of the mildest food preservatives.',
    'e200': 'E200/INS 200 is Sorbic Acid, a natural preservative found in rowan berries. Used in cheese, baked goods, dried fruit and beverages to inhibit mould and yeast. One of the safest food preservatives.',
    'potassium sorbate': 'Potassium sorbate (E202/INS 202) is the potassium salt of sorbic acid, used as a preservative in a vast range of foods including cheese, wine, baked goods and personal care products. One of the most widely used and well-tolerated food preservatives.',
    'e202': 'E202/INS 202 is Potassium Sorbate, the salt form of sorbic acid. Extremely widely used to preserve cheese, bread, wine, dried fruits and beverages. Well-studied and generally regarded as safe.',
    'calcium sorbate': 'Calcium sorbate (E203/INS 203) is the calcium salt of sorbic acid used as a preservative in foods and beverages. Less common than potassium sorbate but similarly safe.',
    'e203': 'E203/INS 203 is Calcium Sorbate, a preservative derived from sorbic acid. Used in some processed foods and beverages. Generally safe.',
    'potassium benzoate': 'Potassium benzoate (E212/INS 212) is the potassium salt of benzoic acid used as a preservative in beverages and acidic foods. Like sodium benzoate, it can form benzene in the presence of ascorbic acid.',
    'e212': 'E212/INS 212 is Potassium Benzoate, a preservative used in soft drinks and acidic foods. Can potentially form benzene when combined with Vitamin C.',
    'calcium benzoate': 'Calcium benzoate (E213/INS 213) is the calcium salt of benzoic acid. Used as a preservative in low-acid foods and beverages.',
    'e213': 'E213/INS 213 is Calcium Benzoate, a calcium-based preservative less common than sodium or potassium benzoate. Used in some jams and beverages.',
    'nisin': 'Nisin (E234/INS 234) is a natural antimicrobial peptide produced by the bacterium Lactococcus lactis. Used to preserve processed cheese, canned foods and meat products. Approved globally and generally safe.',
    'e234': 'E234/INS 234 is Nisin, a natural bacteriocin (antimicrobial peptide) produced by bacteria. Used to preserve processed cheeses and canned goods. Natural origin and generally regarded as safe.',
    'natamycin': 'Natamycin (E235/INS 235) is a natural antifungal compound produced by soil bacteria, used to coat the surface of cheese and some cured meats to prevent mould growth. Generally safe; not absorbed through the gut in significant amounts.',
    'e235': 'E235/INS 235 is Natamycin (Pimaricin), a natural antifungal preservative applied to cheese rinds and sausage surfaces. Naturally derived and considered safe.',
    'potassium nitrite': 'Potassium nitrite (E249/INS 249) is a curing salt used in processed meats to prevent botulism and fix colour. Like sodium nitrite, can form nitrosamines — classified as probable carcinogens — especially at high cooking temperatures.',
    'e249': 'E249/INS 249 is Potassium Nitrite, a curing agent in processed meats that prevents botulism but can form carcinogenic nitrosamines under high heat.',
    'potassium nitrate': 'Potassium nitrate (E252/INS 252) is also known as saltpetre, traditionally used to cure meats. It converts to nitrite during curing. Found naturally in some vegetables.',
    'e252': 'E252/INS 252 is Potassium Nitrate (saltpetre), a traditional meat curing agent. Slower-acting than nitrite; converts to nitrite during the curing process.',
    'lactic acid': 'Lactic acid (E270/INS 270) is an organic acid produced naturally by fermentation. Found in yoghurt, pickles and fermented vegetables. Used as a preservative, flavouring and acidity regulator. Naturally derived and generally safe.',
    'e270': 'E270/INS 270 is Lactic Acid, produced by fermentation of sugars. Found naturally in yoghurt, sauerkraut and pickles. Used as a preservative and flavouring. Safe and naturally derived.',
    'potassium propionate': 'Potassium propionate (E283/INS 283) is the potassium salt of propionic acid. Used as an antifungal preservative in bread and baked goods. Generally safe but may cause migraine in sensitive individuals.',
    'e283': 'E283/INS 283 is Potassium Propionate, a preservative used in bread to prevent mould. Generally safe; some individuals report migraine sensitivity.',
    'carbon dioxide': 'Carbon dioxide (E290/INS 290) is used as a carbonation agent in fizzy drinks, a preservation gas in modified atmosphere packaging, and a propellant. Naturally present in the atmosphere. Safe in food use.',
    'e290': 'E290/INS 290 is Carbon Dioxide, the gas responsible for carbonation in fizzy drinks. Also used in packaging to preserve freshness. Safe and naturally occurring.',
    'malic acid': 'Malic acid (E296/INS 296) is a naturally occurring organic acid found in apples, cherries and many fruits. Used as an acidity regulator and flavouring in confectionery, beverages and baked goods. Generally safe.',
    'e296': 'E296/INS 296 is Malic Acid, the tart acid found naturally in apples and grapes. Used to add tartness to sweets, beverages and jams. Safe and naturally derived.',
    'fumaric acid': 'Fumaric acid (E297/INS 297) is an organic acid found naturally in mushrooms and lichen. Used as an acidity regulator and leavening aid in baked goods, beverages and confectionery. Generally safe.',
    'e297': 'E297/INS 297 is Fumaric Acid, a natural organic acid used as an acidulant in baked goods, soft drinks and jelly. Safe and naturally occurring.',

    # ── Antioxidants & Acidity Regulators E300–E399 (additions) ─────────────
    'ascorbic acid': 'Ascorbic acid (E300/INS 300) is Vitamin C, an essential nutrient and powerful natural antioxidant. Used to preserve colour and freshness in juices, jams and processed foods. Safe and beneficial in normal food amounts.',
    'e300': 'E300/INS 300 is Ascorbic Acid (Vitamin C), used as an antioxidant and preservative in foods. Essential vitamin and generally very safe.',
    'tocopherols': 'Tocopherols (E306/INS 306) are naturally occurring forms of Vitamin E found in vegetable oils, nuts and seeds. Used as antioxidants to prevent rancidity in oils and fat-containing foods. Safe and nutritionally beneficial.',
    'e306': 'E306/INS 306 is mixed Tocopherols (natural Vitamin E), used as an antioxidant in oils and fat-based foods. Naturally derived and considered safe.',
    'alpha tocopherol': 'Alpha-tocopherol (E307/INS 307) is the most biologically active form of Vitamin E, used as an antioxidant in foods and dietary supplements. Naturally derived from vegetable oils.',
    'e307': 'E307/INS 307 is Alpha-Tocopherol (Vitamin E), a natural antioxidant used to prevent rancidity in oils and fat-containing products.',
    'e308': 'E308/INS 308 is Gamma-Tocopherol, a form of Vitamin E used as a food antioxidant. Naturally present in soybean and corn oils.',
    'e309': 'E309/INS 309 is Delta-Tocopherol, a form of Vitamin E found in soybean oil. Used as a food antioxidant.',
    'octyl gallate': 'Octyl gallate (E311/INS 311) is a synthetic antioxidant used to prevent rancidity in fats and oils. Less common than propyl gallate. May cause reactions in aspirin-sensitive individuals.',
    'e311': 'E311/INS 311 is Octyl Gallate, a synthetic antioxidant in oils and fats. May cause reactions in aspirin-sensitive people.',
    'dodecyl gallate': 'Dodecyl gallate (E312/INS 312) is a synthetic antioxidant used in edible fats and oils. May cause skin sensitisation.',
    'e312': 'E312/INS 312 is Dodecyl Gallate (Lauryl Gallate), a synthetic antioxidant in fats. Potential skin sensitiser.',
    'erythorbic acid': 'Erythorbic acid (E315/INS 315) is a stereo-isomer of Vitamin C used as an antioxidant preservative in cured meats, beverages and frozen fish. Has little Vitamin C activity in the body but is an effective antioxidant.',
    'e315': 'E315/INS 315 is Erythorbic Acid (Isoascorbic Acid), an antioxidant preservative used in meats and beverages. Does not have vitamin C activity. Generally safe.',
    'sodium erythorbate': 'Sodium erythorbate (E316/INS 316) is the sodium salt of erythorbic acid, widely used in cured and processed meats to accelerate colour development and prevent rancidity. Generally safe.',
    'e316': 'E316/INS 316 is Sodium Erythorbate, an antioxidant used in cured meats and beverages to maintain colour and freshness.',
    'tbhq': 'TBHQ (E319/INS 319 — Tertiary Butylhydroquinone) is a synthetic antioxidant used in edible oils, frying fats, crackers and instant noodles to prevent rancidity. At high doses it is toxic; at approved food levels it is considered safe. Some studies raise concern about immune effects.',
    'e319': 'E319/INS 319 is TBHQ (Tertiary Butylhydroquinone), a synthetic antioxidant used in edible oils, instant noodles and crackers. Considered safe at approved doses; high doses are toxic.',
    'tertiary butylhydroquinone': 'Tertiary Butylhydroquinone (TBHQ/E319) is a petroleum-derived antioxidant used in cooking oils, instant noodles and snack foods to prevent rancidity. Approved but controversial; some animal studies link high doses to immune effects.',
    'lecithin': 'Lecithin (E322/INS 322) is a natural emulsifier found in egg yolks, soybeans and sunflower seeds. One of the most widely used emulsifiers in chocolate, margarine, baked goods and infant formula. Safe and naturally derived.',
    'e322': 'E322/INS 322 is Lecithin, a natural emulsifier from soy, sunflower or eggs. Widely used in chocolate, mayonnaise and baked goods. Safe and naturally occurring.',
    'soy lecithin': 'Soy lecithin (E322) is lecithin derived specifically from soybeans. Widely used as an emulsifier in chocolate, bread and margarine. Generally safe; those with severe soy allergies should be aware, though soy lecithin typically contains minimal soy protein.',
    'sunflower lecithin': 'Sunflower lecithin is lecithin extracted from sunflower seeds (E322). Used as a soy-free emulsifier alternative in chocolate and baked goods. Considered safe.',
    'sodium lactate': 'Sodium lactate (E325/INS 325) is the sodium salt of lactic acid, used as a humectant, acidity regulator and preservative in meat products and baked goods. Generally safe.',
    'e325': 'E325/INS 325 is Sodium Lactate, used as an acidity regulator and humectant in meats and baked goods. Safe and naturally derived from fermentation.',
    'potassium lactate': 'Potassium lactate (E326/INS 326) is the potassium salt of lactic acid used as a preservative and acidity regulator in meat and fish products. Safe.',
    'e326': 'E326/INS 326 is Potassium Lactate, a preservative from lactic acid used in meat and fish products.',
    'calcium lactate': 'Calcium lactate (E327/INS 327) is the calcium salt of lactic acid, used as an acidity regulator, firming agent and calcium supplement in foods. Also used to keep cut fruits firm.',
    'e327': 'E327/INS 327 is Calcium Lactate, an acidity regulator and calcium supplement used in fruits, vegetables and beverages.',
    'citric acid': 'Citric acid (E330/INS 330) is the natural acid found in citrus fruits, produced commercially by fermenting sugars with Aspergillus niger mould. Widely used as a flavouring, preservative and acidity regulator in beverages, confectionery and processed foods.',
    'e330': 'E330/INS 330 is Citric Acid, the tart acid found naturally in lemons and oranges. One of the most widely used food additives globally — in beverages, sweets, jams and as a pH adjuster.',
    'potassium citrates': 'Potassium citrate (E332/INS 332) is the potassium salt of citric acid, used as an acidity regulator, sequestrant and emulsifying salt in processed cheese and beverages. Also used medically to treat kidney stones.',
    'e332': 'E332/INS 332 is Potassium Citrate, used as an acidity regulator and emulsifying salt in cheese and beverages. Generally safe.',
    'sodium tartrate': 'Sodium tartrate (E335/INS 335) is the sodium salt of tartaric acid, used as an acidity regulator in foods. Generally safe.',
    'e335': 'E335/INS 335 is Sodium Tartrate, an acidity regulator used in jellies, jams and confectionery.',
    'potassium tartrate': 'Potassium tartrate (E336/INS 336), also known as cream of tartar, is a natural by-product of wine-making. Used as a leavening aid, stabiliser and acidity regulator in baking. Safe and naturally derived.',
    'cream of tartar': 'Cream of Tartar (Potassium Tartrate/E336) is a natural by-product of wine-making used as a leavening agent in baking and to stabilise whipped egg whites. Safe and naturally derived.',
    'e336': 'E336/INS 336 is Potassium Tartrate (Cream of Tartar), a natural by-product of wine fermentation. Used in baking as a leavening aid and egg-white stabiliser.',
    'rochelle salt': 'Rochelle Salt (Sodium Potassium Tartrate/E337/INS 337) is a double salt of tartaric acid used as an acidity regulator and leavening agent. Historically used in baking powder.',
    'e337': 'E337/INS 337 is Sodium Potassium Tartrate (Rochelle Salt), used as an acidity regulator in baking. Safe.',
    'sodium phosphates': 'Sodium phosphates (E339/INS 339) are phosphate salts used as emulsifying agents, leavening agents and acidity regulators in processed cheese, baked goods and meats. High phosphate intake may affect kidney function.',
    'e339': 'E339/INS 339 is Sodium Phosphates, used in processed cheese, meat products and baked goods. Excessive phosphate intake from processed foods is a concern for kidney health.',
    'potassium phosphates': 'Potassium phosphates (E340/INS 340) are used as emulsifying agents, acidity regulators and sequestrants in processed cheese, beverages and meats. Generally safe in moderate amounts.',
    'e340': 'E340/INS 340 is Potassium Phosphates, used as emulsifiers and acidity regulators in processed foods.',
    'calcium phosphates': 'Calcium phosphates (E341/INS 341) are used as leavening agents, anti-caking agents, and calcium supplements in baked goods, breakfast cereals and infant formula. Safe and provide dietary calcium.',
    'e341': 'E341/INS 341 is Calcium Phosphates, used as leavening agents in baking and as calcium supplements. Safe and nutritionally beneficial.',
    'adipic acid': 'Adipic acid (E355/INS 355) is an organic acid used as an acidity regulator and leavening agent in powdered beverages, baking mixes and confectionery. Generally safe.',
    'e355': 'E355/INS 355 is Adipic Acid, used as an acidity regulator and leavening aid in baking mixes and powdered drink mixes.',
    'succinic acid': 'Succinic acid (E363/INS 363) is a natural organic acid found in plant and animal tissues. Used as an acidity regulator and flavouring in powdered beverages and baked goods. Safe.',
    'e363': 'E363/INS 363 is Succinic Acid, a natural acidity regulator found in many plants. Used in beverages and baked goods.',
    'edta': 'EDTA (Ethylenediaminetetraacetic acid / E385/INS 385) is a chelating agent used to preserve colour and freshness in canned and jarred foods by binding trace metals that cause rancidity. Also used widely in cosmetics. Generally safe in food use levels.',
    'calcium disodium edta': 'Calcium Disodium EDTA (E385/INS 385) is a chelating preservative used in mayonnaise, salad dressings, canned vegetables and some pickled foods to prevent metal-catalysed oxidation. Safe at approved food levels.',
    'e385': 'E385/INS 385 is Calcium Disodium EDTA, a chelating preservative used in mayonnaise, sauces and canned foods to maintain colour and shelf life. Safe at food use levels.',
    'rosemary extract': 'Rosemary extract (E392/INS 392) is a natural antioxidant derived from rosemary leaves. Used to prevent rancidity in fats, oils and meat products. Safe and naturally derived.',
    'e392': 'E392/INS 392 is Rosemary Extracts, natural antioxidants used to preserve oils and fat-containing foods from rancidity.',

    # ── Emulsifiers & Stabilisers E400–E499 (additions) ─────────────────────
    'alginic acid': 'Alginic acid (E400/INS 400) is a natural polysaccharide extracted from brown seaweed. Used as a thickener and stabiliser in ice cream, salad dressings and dairy products. Safe and naturally derived.',
    'e400': 'E400/INS 400 is Alginic Acid, a natural seaweed-derived thickener and stabiliser used in ice cream and dairy products.',
    'sodium alginate': 'Sodium alginate (E401/INS 401) is the sodium salt of alginic acid, derived from brown seaweed. Widely used as a thickener, gelling agent and stabiliser in ice cream, noodles, salad dressings and molecular gastronomy. Safe.',
    'potassium alginate': 'Potassium alginate (E402/INS 402) is a seaweed-derived thickener and stabiliser used in foods as a gelling agent. Safe and naturally derived.',
    'ammonium alginate': 'Ammonium alginate (E403/INS 403) is a seaweed-derived stabiliser and thickener used in foods and beverages.',
    'e403': 'E403/INS 403 is Ammonium Alginate, a seaweed-derived thickener. Safe.',
    'calcium alginate': 'Calcium alginate (E404/INS 404) is a calcium salt of alginic acid used as a stabiliser and gel-forming agent in foods. Also used to form food capsules in molecular gastronomy.',
    'propylene glycol alginate': 'Propylene Glycol Alginate (E405/INS 405) is an ester of alginic acid used as an emulsifier and stabiliser in salad dressings, beer and ice cream. Generally safe.',
    'e405': 'E405/INS 405 is Propylene Glycol Alginate, a seaweed-derived emulsifier used in dressings and ice cream.',
    'pectin': 'Pectin (E440/INS 440) is a natural structural polysaccharide found in fruit cell walls, especially citrus peel and apple pomace. Widely used as a gelling agent in jams, jellies and marmalades. Also a soluble dietary fibre with benefits for gut health and cholesterol levels.',
    'e440': 'E440/INS 440 is Pectin, a natural plant fibre used as a gelling agent in jams and jellies. Derived from citrus peel or apple pomace. Safe and also a beneficial dietary fibre.',
    'microcrystalline cellulose': 'Microcrystalline Cellulose (E460/INS 460) is purified cellulose from plant fibre, used as an anti-caking agent, filler and fat replacer in processed foods and as a tablet binder in pharmaceuticals. Safe and non-digestible.',
    'methyl cellulose': 'Methyl Cellulose (E461/INS 461) is a modified cellulose derivative used as a thickener, emulsifier and gelling agent in foods. Unique property: gels when heated, liquefies when cooled. Safe and non-digestible.',
    'e461': 'E461/INS 461 is Methyl Cellulose, a modified plant fibre used as a thickener. Gels when hot, liquefies when cold. Safe.',
    'hydroxypropyl cellulose': 'Hydroxypropyl Cellulose (E463/INS 463) is a modified cellulose used as a thickener and film-forming agent in foods and pharmaceuticals. Safe.',
    'e463': 'E463/INS 463 is Hydroxypropyl Cellulose, a modified fibre used as a thickener in foods and as a tablet coating.',
    'hydroxypropyl methylcellulose': 'Hydroxypropyl Methylcellulose (HPMC/E464/INS 464) is a modified cellulose used as a thickener, emulsifier and coating agent in foods and pharmaceuticals. Used in gluten-free baking to mimic gluten structure. Safe.',
    'hpmc': 'HPMC (Hydroxypropyl Methylcellulose / E464) is a modified plant-based thickener and binder used in gluten-free foods, sauces and pharmaceutical tablets. Safe.',
    'e464': 'E464/INS 464 is Hydroxypropyl Methylcellulose (HPMC), a modified cellulose thickener and emulsifier used in gluten-free baked goods and pharmaceutical coatings.',
    'mono and diglycerides': 'Mono- and Diglycerides of Fatty Acids (E471/INS 471) are the most widely used food emulsifiers, produced from glycerol and fatty acids. Used in bread, margarine, ice cream, chocolate and baked goods to improve texture and shelf life. Generally safe, though may contain trans fats if derived from partially hydrogenated oils.',
    'e471': 'E471/INS 471 is Mono- and Diglycerides of Fatty Acids, the world\'s most common food emulsifier. Used in bread, ice cream, margarine and chocolate. Generally safe.',
    'acetylated distarch phosphate': 'Acetylated Distarch Phosphate (E1414/INS 1414) is a modified starch used as a thickener and stabiliser in soups, sauces, baby foods and dairy products. Resistant to heat and acidity. Safe.',
    'e1414': 'E1414/INS 1414 is Acetylated Distarch Phosphate, a modified starch thickener used in soups and sauces. Safe.',
    'hydroxypropyl starch': 'Hydroxypropyl Starch (E1440/INS 1440) is a modified starch used as a thickener and stabiliser in foods. More stable than native starch under heat and acidity.',
    'e1440': 'E1440/INS 1440 is Hydroxypropyl Starch, a modified food starch thickener. Safe.',
    'hydroxypropyl distarch phosphate': 'Hydroxypropyl Distarch Phosphate (E1442/INS 1442) is a chemically modified starch used as a thickener in soups, sauces, dairy desserts and baby foods. Very stable under heat and acidic conditions. Safe.',
    'starch sodium octenyl succinate': 'Starch Sodium Octenyl Succinate (E1450/INS 1450) is an emulsifying modified starch used in beverage emulsions, flavour encapsulation and salad dressings. Safe.',
    'e1450': 'E1450/INS 1450 is Starch Sodium Octenyl Succinate, an emulsifying modified starch used in beverages and dressings.',

    # ── Acidity Regulators & Anti-caking E500–E599 (additions) ──────────────
    'ammonium bicarbonate': 'Ammonium bicarbonate (E503/INS 503) is a leavening agent used in biscuits, crackers and some traditional baked goods. It completely decomposes during baking releasing CO₂ and ammonia gas — no residue remains in the food.',
    'e503': 'E503/INS 503 is Ammonium Bicarbonate, a leavening agent used in biscuits and crackers. Decomposes completely during baking — no residue. Safe.',
    'ammonium carbonate': 'Ammonium carbonate (E503) is a leavening agent in baked goods that releases CO₂ and ammonia when heated. Used in traditional European biscuits (hartshorn).',
    'potassium chloride': 'Potassium chloride (E508/INS 508) is a mineral salt used as a salt substitute, flavour enhancer and acidity regulator. Found naturally in many foods. Used in low-sodium products to partially replace table salt. Generally safe; those with kidney disease should moderate intake.',
    'calcium chloride': 'Calcium chloride (E509/INS 509) is a mineral salt used as a firming agent in canned vegetables, tofu and cheese-making. Also used to harden water in brewing. Safe in food amounts; provides dietary calcium.',
    'magnesium carbonate': 'Magnesium carbonate (E504/INS 504) is an anti-caking agent and acidity regulator used in table salt, confectionery and baked goods. Provides magnesium — an essential mineral. Safe.',
    'e504': 'E504/INS 504 is Magnesium Carbonate, an anti-caking agent used in salt and confectionery. Also a source of dietary magnesium.',
    'calcium sulfate': 'Calcium sulfate (E516/INS 516), also known as food-grade gypsum or plaster of Paris, is used as a firming agent and acidity regulator in tofu, flour, brewing and baked goods. Provides dietary calcium. Safe.',
    'sodium hydroxide': 'Sodium hydroxide (E524/INS 524), also called lye or caustic soda, is used in food processing to cure olives, pretzels, bagels and hominy. It is highly caustic in pure form but safe when used at controlled levels in food processing — neutralised by reactions during processing.',
    'e524': 'E524/INS 524 is Sodium Hydroxide (Lye), used to treat olives, pretzels and bagels. Caustic in pure form but safe after processing neutralisation.',
    'calcium hydroxide': 'Calcium hydroxide (E526/INS 526), also known as slaked lime or chuna, is used in nixtamalisation of corn, pickling, and as a firming agent. Also used in paan/betel preparations. Food-safe at approved levels.',
    'magnesium oxide': 'Magnesium oxide (E530/INS 530) is an anti-caking agent used in cocoa powder, table salt and confectionery. Also an antacid and magnesium supplement. Safe.',
    'e530': 'E530/INS 530 is Magnesium Oxide, an anti-caking agent and acidity regulator. Also provides dietary magnesium.',
    'silicon dioxide': 'Silicon dioxide (E551/INS 551), also called silica, is a natural anti-caking agent used to prevent clumping in powdered foods, salt, spices, dried milk and seasoning mixes. Naturally present in many foods. Generally safe.',
    'silica': 'Silica (Silicon Dioxide/E551/INS 551) is a natural anti-caking agent used in powdered foods and seasonings to prevent clumping. Present naturally in many grains and vegetables. Safe.',
    'e551': 'E551/INS 551 is Silicon Dioxide (Silica), a natural anti-caking agent used in powdered foods, salt and spice blends to prevent clumping.',
    'calcium silicate': 'Calcium silicate (E552/INS 552) is an anti-caking agent used in table salt, baking powder and powdered foods to prevent moisture absorption and clumping. Safe.',
    'e552': 'E552/INS 552 is Calcium Silicate, an anti-caking agent used in powdered foods and salt.',
    'magnesium silicate': 'Magnesium silicate (E553/INS 553a) is an anti-caking agent (related to talc) used in confectionery and powdered foods. Safe in food use.',
    'talc': 'Talc (E553b/INS 553b) is a mineral anti-caking and glazing agent. Food-grade talc is used on rice, confectionery and chewing gum. Safety concerns exist for cosmetic talc near reproductive organs; food-grade use is considered safe.',
    'e553b': 'E553b/INS 553b is Talc, a mineral used as an anti-caking agent and rice-glazing agent. Food-grade use is considered safe.',
    'sodium ferrocyanide': 'Sodium ferrocyanide (E535/INS 535) is an anti-caking agent added to table salt in tiny amounts to prevent clumping. Despite the "cyanide" in the name, the compound is very stable and the cyanide is firmly bound — safe at food additive levels.',
    'e535': 'E535/INS 535 is Sodium Ferrocyanide, an anti-caking agent used in table salt. Safe at food levels despite the misleading "cyanide" name — the cyanide is chemically bound.',

    # ── Flavour Enhancers E600–E699 (additions) ──────────────────────────────
    'glutamic acid': 'Glutamic acid (E620/INS 620) is a naturally occurring amino acid found in tomatoes, parmesan, mushrooms and many protein-rich foods. It is the basis of umami (the fifth basic taste). Safe; naturally present in many everyday foods.',
    'e620': 'E620/INS 620 is Glutamic Acid, the free amino acid responsible for umami flavour. Naturally found in tomatoes, cheese and meat. Safe.',
    'monosodium glutamate': 'Monosodium Glutamate (MSG/E621/INS 621) is the sodium salt of glutamic acid, used since 1908 to enhance savoury/umami flavour. Found naturally in parmesan, tomatoes and soy sauce. Extensively studied; FDA and WHO consider it safe. "Chinese Restaurant Syndrome" has not been confirmed in double-blind studies.',
    'msg': 'MSG (Monosodium Glutamate / E621/INS 621) is one of the most studied food additives. FDA classifies it as generally recognised as safe. Naturally occurring glutamate is identical to added MSG. Not proven to cause headaches in controlled studies.',
    'e621': 'E621/INS 621 is Monosodium Glutamate (MSG), the most widely used flavour enhancer in the world. Safe for the general population according to FDA, WHO, and EFSA. Naturally present in parmesan, mushrooms and tomatoes.',
    'disodium guanylate': 'Disodium Guanylate (E627/INS 627) is a flavour enhancer derived from fish or yeast, used with MSG to synergistically boost umami flavour. Often appears alongside MSG in instant noodles, snacks and soups.',
    'e627': 'E627/INS 627 is Disodium Guanylate (GMP), a flavour enhancer that works synergistically with MSG. Usually combined with MSG in instant foods. Derived from fish or yeast.',
    'disodium inosinate': 'Disodium Inosinate (E631/INS 631) is a flavour enhancer derived from meat or fish, used with MSG to amplify umami flavour. Very commonly used in instant noodles, chips and soups.',
    'e631': 'E631/INS 631 is Disodium Inosinate (IMP), a meat/fish-derived flavour enhancer. Works with MSG to create a powerful umami boost.',
    'disodium ribonucleotides': 'Disodium 5\'-Ribonucleotides (E635/INS 635) is a blend of disodium inosinate (E631) and disodium guanylate (E627). Used as a cost-effective flavour enhancer in instant noodles, snacks and soups. Derived from fish, meat or yeast.',
    'e635': 'E635/INS 635 is Disodium 5\'-Ribonucleotides, a flavour enhancer blend of IMP and GMP. Common in instant noodles and flavoured snacks.',

    # ── Sweeteners E900–E999 (additions) ─────────────────────────────────────
    'dimethyl polysiloxane': 'Dimethyl Polysiloxane (E900/INS 900) is a silicone-based anti-foaming agent added to cooking oils for deep frying and in fruit juices and wines. Safe at approved levels.',
    'e900': 'E900/INS 900 is Dimethylpolysiloxane (PDMS), an anti-foaming agent used in cooking oils and beverages. Safe at food use levels.',
    'acesulfame k': 'Acesulfame-K (E950/INS 950) is a calorie-free synthetic sweetener about 200 times sweeter than sugar. Used in diet drinks, sugar-free confectionery, dairy products and tabletop sweeteners. FDA-approved; generally considered safe.',
    'acesulfame potassium': 'Acesulfame Potassium (Acesulfame-K/E950/INS 950) is a heat-stable, zero-calorie sweetener 200× sweeter than sugar. Widely used in diet beverages, reduced-sugar foods and tabletop sweeteners. Approved globally.',
    'e950': 'E950/INS 950 is Acesulfame-K (Acesulfame Potassium), a zero-calorie sweetener 200× sweeter than sugar. Heat-stable; used in baked goods, diet drinks and sugar-free confectionery.',
    'e951': 'E951/INS 951 is Aspartame, a low-calorie sweetener 200× sweeter than sugar. Must be avoided by people with phenylketonuria (PKU). IARC classified it as "possibly carcinogenic" (Group 2B) in 2023 but FDA and EFSA maintain it is safe at approved intake levels.',
    'cyclamate': 'Cyclamate (E952/INS 952) is a synthetic sweetener 30–50× sweeter than sugar. Banned in the USA since 1969 due to animal study concerns (though more recent data suggests it may be safe). Still permitted in India, EU and over 100 countries.',
    'sodium cyclamate': 'Sodium Cyclamate (E952/INS 952) is the sodium salt form of cyclamate sweetener. Banned in USA; permitted in India and EU. Often combined with saccharin in soft drinks.',
    'e952': 'E952/INS 952 is Cyclamate (often as sodium cyclamate), a synthetic sweetener banned in USA but permitted in India and EU. Often used with saccharin in diet beverages.',
    'isomalt': 'Isomalt (E953/INS 953) is a sugar alcohol derived from sucrose, used as a low-calorie bulk sweetener and sugar replacer in hard candies, chocolate and bakery products. Provides 2 kcal/g vs 4 kcal/g for sugar. May cause digestive discomfort in large amounts.',
    'e953': 'E953/INS 953 is Isomalt, a sugar alcohol bulk sweetener used in sugar-free sweets and chocolate. Half the calories of sugar; may cause bloating in large amounts.',
    'saccharin': 'Saccharin (E954/INS 954) is the oldest artificial sweetener, 300–400× sweeter than sugar. Once feared as a carcinogen due to rat studies, but the mechanism was found not to apply to humans. Currently FDA-approved and delisted from carcinogens. Still avoided by many consumers.',
    'e954': 'E954/INS 954 is Saccharin, the oldest synthetic sweetener (discovered 1879). 300-400× sweeter than sugar; zero calories. Previously feared as a carcinogen but cleared by FDA and WHO.',
    'steviol glycosides': 'Steviol glycosides (E960/INS 960) are natural sweeteners extracted from the leaves of the stevia plant, native to South America. 200–350× sweeter than sugar with zero calories. Approved globally and considered safe.',
    'stevia': 'Stevia (E960/INS 960) refers to steviol glycosides extracted from the Stevia rebaudiana plant. A natural, zero-calorie sweetener 200–350× sweeter than sugar. FDA-approved; widely used in beverages, dairy and tabletop sweeteners.',
    'e960': 'E960/INS 960 is Steviol Glycosides (from stevia plant), a natural zero-calorie sweetener. 200-350× sweeter than sugar. Approved in India, EU and USA.',
    'neotame': 'Neotame (E961/INS 961) is a synthetic sweetener approximately 7,000–13,000× sweeter than sugar, requiring only tiny amounts. Unlike aspartame it is safe for PKU patients. Approved by FDA and EU.',
    'e961': 'E961/INS 961 is Neotame, an extremely potent synthetic sweetener (7,000-13,000× sweeter than sugar). Does not require PKU warning unlike aspartame. Approved by FDA.',
    'xylitol': 'Xylitol (E967/INS 967) is a sugar alcohol found naturally in birch bark, corn cobs and many fruits and vegetables. Used as a low-calorie sweetener in chewing gum, toothpaste and sugar-free confectionery. Has dental benefits — inhibits the bacteria that cause cavities. Toxic to dogs.',
    'e967': 'E967/INS 967 is Xylitol, a natural sugar alcohol with dental benefits. Used in sugar-free gum, toothpaste and sweets. 40% fewer calories than sugar. Toxic to dogs.',
    'erythritol': 'Erythritol (E968/INS 968) is a sugar alcohol that occurs naturally in fermented foods. Nearly zero calories (0.2 kcal/g), 60–70% as sweet as sugar. Better tolerated than other sugar alcohols — less likely to cause digestive discomfort. Used in keto and diabetic-friendly products.',
    'e968': 'E968/INS 968 is Erythritol, a nearly zero-calorie sugar alcohol used in keto products, sugar-free gum and beverages. Better digestive tolerance than other sugar alcohols. Naturally occurring.',
    'sorbitol': 'Sorbitol (E420/INS 420) is a sugar alcohol found naturally in fruits like apples, pears and prunes. Used as a low-calorie sweetener and humectant in sugar-free confectionery, baked goods and medicines. About 60% as sweet as sugar. May cause digestive discomfort in large amounts.',
    'e420': 'E420/INS 420 is Sorbitol, a natural sugar alcohol from fruits. Used in sugar-free sweets and as a humectant in bakery products. Causes digestive discomfort if consumed excessively.',
    'mannitol': 'Mannitol (E421/INS 421) is a sugar alcohol found naturally in mushrooms, olives and seaweed. Used as a low-calorie sweetener, anti-caking agent and bulking agent. Has a cooling sensation in the mouth. Less likely to cause digestive issues than sorbitol.',
    'maltitol': 'Maltitol (E965/INS 965) is a sugar alcohol produced from maltose. 75–90% as sweet as sugar with about half the calories. Widely used in sugar-free chocolate and confectionery. May cause digestive discomfort in large quantities.',
    'e965': 'E965/INS 965 is Maltitol, a sugar alcohol used in sugar-free chocolate and confectionery. About 75% as sweet as sugar with half the calories.',
    'lactitol': 'Lactitol (E966/INS 966) is a sugar alcohol derived from lactose. 30–40% as sweet as sugar; used in sugar-free confectionery and as a prebiotic. Not suitable for people with lactose intolerance.',
    'e966': 'E966/INS 966 is Lactitol, a sugar alcohol from lactose used in sugar-free sweets and as a prebiotic. Not suitable for lactose intolerant individuals.',

    # ── Common food ingredients (additions) ──────────────────────────────────
    'maltodextrin': 'Maltodextrin is a highly processed carbohydrate produced from starch (corn, wheat or potato) by partial hydrolysis. Used as a filler, thickener and carrier for flavourings and spray-dried ingredients. High glycaemic index — raises blood sugar rapidly. Found in protein powders, instant beverages, snacks and many processed foods.',
    'dextrose': 'Dextrose (glucose) is a simple sugar produced from starch (usually corn). Used as a sweetener, energy source, fermentation substrate and anti-caking agent. High glycaemic index. Used in baked goods, sports drinks and processed foods.',
    'glucose syrup': 'Glucose syrup is a liquid sweetener made by hydrolyzing starch, consisting mainly of glucose with some maltose and longer chains. Widely used in confectionery, baked goods, jams and beverages. High glycaemic index.',
    'high fructose corn syrup': 'High Fructose Corn Syrup (HFCS) is a liquid sweetener made from corn starch where some glucose is converted to fructose by enzymes. The most controversial processed sweetener — linked in large-scale studies to obesity, insulin resistance and fatty liver disease.',
    'hfcs': 'HFCS (High Fructose Corn Syrup) is a processed corn-derived sweetener. Linked in multiple studies to metabolic disorders, obesity and fatty liver disease at high consumption levels. Rarely labelled as such in India — may appear as "liquid glucose" or "glucose-fructose syrup".',
    'corn syrup': 'Corn syrup is a glucose-rich sweetener made from corn starch. Used in confectionery, baked goods and beverages. Raises blood sugar rapidly.',
    'invert sugar': 'Invert sugar is a mixture of equal parts glucose and fructose produced by hydrolysing sucrose. Sweeter than regular sugar and retains moisture better. Used in confectionery, baked goods and beverages.',
    'treacle': 'Treacle (black treacle or molasses) is a thick dark syrup — a by-product of sugar refining. Contains minerals like iron, calcium and potassium. Used in baking and confectionery.',
    'molasses': 'Molasses is the dark, thick syrup remaining after sugar extraction. Rich in iron, calcium, magnesium and potassium. Used in baking, rum production and as an animal feed supplement.',
    'coconut sugar': 'Coconut sugar is made from the sap of coconut palm flowers. Contains trace minerals and a small amount of inulin fibre. Has a slightly lower glycaemic index than regular sugar but is still primarily sucrose and should be treated like sugar.',
    'palm sugar': 'Palm sugar is made from the sap of various palm trees. Used extensively in South and Southeast Asian cooking. Primarily sucrose; similar nutritional profile to regular sugar.',
    'jaggery': 'Jaggery (gur) is unrefined cane sugar or palm sugar common in South Asian cooking. Contains trace minerals (iron, calcium, potassium) and molasses. Less processed than white sugar but nutritionally still primarily sucrose.',
    'stevia leaf extract': 'Stevia leaf extract contains steviol glycosides (E960), the sweet compounds from the stevia plant. Zero calories; 200–350× sweeter than sugar. Approved as safe by FDA, EFSA and FSSAI.',
    'canola oil': 'Canola oil is a refined vegetable oil from a cultivar of rapeseed, bred to be low in erucic acid. One of the healthiest cooking oils — high in monounsaturated fat and omega-3 fatty acids, low in saturated fat. Widely used in Indian food manufacturing.',
    'sunflower oil': 'Sunflower oil is a common cooking and frying oil high in polyunsaturated omega-6 fatty acids (linoleic acid) and Vitamin E. Used extensively in Indian snack food manufacturing. High omega-6 intake in imbalance with omega-3 may promote inflammation.',
    'soybean oil': 'Soybean oil is the world\'s most produced vegetable oil. High in polyunsaturated omega-6 and omega-3 fatty acids. Widely used in cooking, margarine and processed foods. Partially hydrogenated soybean oil (now largely phased out) contained harmful trans fats.',
    'cottonseed oil': 'Cottonseed oil is a vegetable oil from cotton plant seeds. Widely used in commercial frying and snack food production in India. High in omega-6 fatty acids. Naturally contains gossypol (removed in refining).',
    'rice bran oil': 'Rice bran oil is extracted from the outer bran layer of rice. Used extensively in India for cooking and commercial food manufacturing. Contains oryzanol, gamma-tocopherol and other beneficial phytonutrients.',
    'groundnut oil': 'Groundnut oil (peanut oil) is a cooking oil pressed from groundnuts (peanuts). Widely used for frying in India. High in monounsaturated fats; relatively heat-stable. Allergen — must be declared.',
    'sesame oil': 'Sesame oil is extracted from sesame seeds. Used as a flavouring oil in Asian cooking and Indian cuisine. Contains sesamin and sesamolin — natural antioxidants. Light sesame oil is used for cooking; dark sesame oil as a flavour condiment.',
    'mustard oil': 'Mustard oil is pressed from mustard seeds and widely used in North and East India for cooking. Contains erucic acid, which was historically a concern but current research suggests it is safe at normal dietary levels. Rich in omega-3 and omega-6 fatty acids.',
    'vanaspati': 'Vanaspati is a partially or fully hydrogenated vegetable fat widely used in Indian commercial baking and cooking. Partially hydrogenated vanaspati contains harmful trans fats. India has moved to limit trans fats in food to ≤2% since 2021.',
    'shortening': 'Shortening is a fat product (animal or vegetable-based) used in baking to create tender, flaky textures. Vegetable shortenings were traditionally partially hydrogenated, containing trans fats. Modern shortenings are increasingly trans-fat-free.',
    'margarine': 'Margarine is a butter substitute made from vegetable oils. Historically made with partially hydrogenated oils (containing trans fats); modern margarines are typically trans-fat-free. Contains added vitamins A and D.',
    'ghee': 'Ghee is clarified butter made by simmering butter to remove water and milk solids. Widely used in Indian cooking and Ayurvedic medicine. High in saturated fat and butyric acid. Contains conjugated linoleic acid (CLA). Generally safe in moderation.',
    'sodium bicarbonate': 'Sodium bicarbonate (baking soda/E500) is a leavening agent that releases CO₂ when combined with acid, making baked goods rise. Also used as an acidity regulator and anti-caking agent. Safe and naturally derived.',
    'baking soda': 'Baking soda is sodium bicarbonate (E500/INS 500), a leavening agent used in baked goods to make them rise. Also used as a gentle abrasive in toothpaste and as an antacid.',
    'baking powder': 'Baking powder is a mixture of sodium bicarbonate, an acid (cream of tartar or sodium acid pyrophosphate) and a filler (cornstarch). A complete leavening agent used in cakes and quick breads.',
    'cream of tartar': 'Cream of tartar (potassium bitartrate/E336) is a natural by-product of wine-making used as a leavening acid in baking, to stabilise egg whites and to prevent sugar crystallisation in confectionery.',
    'sodium acid pyrophosphate': 'Sodium Acid Pyrophosphate (SAPP/E450) is a leavening agent used in baking powder, canned potatoes and seafood. Can inhibit discolouration in potato products.',
    'e450': 'E450/INS 450 is Sodium Acid Pyrophosphate (SAPP), a leavening agent and acidity regulator used in baking powder and processed potatoes.',
    'yeast extract': 'Yeast extract is a concentrated paste or powder made from the intracellular contents of yeast cells. Rich in glutamates (natural umami), B vitamins and amino acids. Used as a flavour enhancer in soups, stocks, sauces and instant foods.',
    'autolysed yeast': 'Autolysed yeast extract is produced by allowing yeast to self-digest, releasing amino acids and flavour compounds. Used as a natural flavour enhancer high in glutamates — similar in effect to MSG but naturally derived.',
    'malt extract': 'Malt extract is a concentrated extract from malted barley. Rich in maltose, amino acids and B vitamins. Used as a natural sweetener and flavour enhancer in baked goods, beverages, breakfast cereals and confectionery.',
    'whey powder': 'Whey powder is dried whey — the liquid remaining after milk is curdled and strained. Rich in whey protein, lactose and minerals. Used in baked goods, confectionery, ice cream and protein supplements. Contains lactose — not suitable for lactose-intolerant individuals.',
    'whey protein concentrate': 'Whey protein concentrate (WPC) is a processed form of whey retaining some lactose and fat. Used in protein supplements, sports nutrition and processed foods. High-quality complete protein.',
    'casein': 'Casein is the primary protein in milk, making up about 80% of milk protein. Used in cheese-making, protein supplements, coffee whiteners and processed foods. Digested slowly — provides sustained amino acid release.',
    'sodium caseinate': 'Sodium caseinate is a soluble form of casein made by reacting casein with sodium hydroxide. Used as an emulsifier and protein source in coffee whiteners, whipped toppings and processed foods. Milk-derived — not suitable for vegans.',
    'skimmed milk powder': 'Skimmed milk powder (SMP) is dehydrated skim milk. Used in baked goods, confectionery, ice cream and infant formula. Rich in protein, calcium and B vitamins. Contains lactose.',
    'full cream milk powder': 'Full cream milk powder is dehydrated whole milk retaining all milk fat. Used in confectionery, beverages and baked goods. Good source of protein, calcium and fat-soluble vitamins.',
    'condensed milk': 'Condensed milk is milk with most water removed and sugar added. Very high in sugar (about 55%). Used in desserts, confectionery and beverages.',
    'inulin': 'Inulin is a naturally occurring fructan dietary fibre found in chicory root, garlic, onion and Jerusalem artichoke. Used as a prebiotic fibre supplement and fat replacer in low-calorie foods. Feeds beneficial gut bacteria.',
    'fructooligosaccharides': 'Fructooligosaccharides (FOS) are short-chain inulin-type fibres that occur naturally in many plants. Used as prebiotic dietary fibre supplements. Feed beneficial gut bacteria (Bifidobacterium and Lactobacillus).',
    'fos': 'FOS (Fructooligosaccharides) are prebiotic dietary fibres from plants. Used in functional foods and supplements to support gut microbiome health.',
    'resistant starch': 'Resistant starch is a type of starch that resists digestion in the small intestine, reaching the large intestine intact where it acts as a prebiotic fibre. Found in uncooked oats, slightly underripe bananas and cooked-then-cooled potato and rice.',
    'dextrin': 'Dextrin is a partially hydrolysed starch used as a thickener, binder and coating agent in foods, pharmaceuticals and adhesives. Used in breadcrumb coatings and encapsulation of flavours.',
    'modified corn starch': 'Modified corn starch (E1400-1442 range) is corn starch chemically or physically treated to improve its stability under heat, acidity or freezing. Used as a thickener in soups, sauces, gravies and baby foods.',
    'tapioca starch': 'Tapioca starch is extracted from cassava root. Used as a thickener in soups, sauces and desserts. Gluten-free and bland in flavour. Also used to make tapioca pearls.',
    'arrowroot': 'Arrowroot is a starch extracted from the roots of Maranta arundinacea. Used as a gentle thickener in sauces and baby foods. Gluten-free and easily digestible.',
    'corn flour': 'Corn flour (cornstarch) is finely ground starch from maize. Used as a thickener in soups, sauces, custards and gravies. Gluten-free.',
    'rice flour': 'Rice flour is finely ground rice, used as a gluten-free flour alternative in baked goods, coatings and thickeners. Widely used in South Indian cooking (idli, dosa batter).',
    'chickpea flour': 'Chickpea flour (besan) is ground from dried chickpeas. High in protein and fibre. Widely used in Indian cooking for pakoras, bhajis, kadhi and sweets. Gluten-free.',
    'soy flour': 'Soy flour is ground from defatted soybeans. High in protein; used in baked goods, processed meats and as a meat extender. Soy allergen.',
    'vital wheat gluten': 'Vital wheat gluten is concentrated gluten protein extracted from wheat flour. Used to strengthen bread dough, in seitan (wheat meat) and as a protein source. Strong wheat allergen.',
    'pea protein': 'Pea protein is extracted from yellow split peas. A high-quality plant-based protein used in protein supplements, plant-based meat alternatives and dairy alternatives. Free from major allergens.',
    'soy protein isolate': 'Soy protein isolate (SPI) is a highly processed form of soy protein (≥90% protein content). Used in protein supplements, plant-based meats and processed foods. Contains phytoestrogens (isoflavones); soy allergen.',
    'modified starch': 'Modified starch refers to any of the E1400-1442 range of starches chemically or physically treated to improve their cooking properties. Used widely as thickeners and stabilisers in sauces, soups and processed foods.',
    'vegetable oil': 'Vegetable oil on ingredient labels usually refers to a blend of refined plant oils (typically palm, soybean, sunflower or canola). The specific oils are often not disclosed. Palm and soybean oil are most common.',
    'hydrogenated vegetable oil': 'Hydrogenated vegetable oil is vegetable oil treated with hydrogen to make it solid or semi-solid. Partially hydrogenated oils contain harmful trans fats linked to cardiovascular disease. Fully hydrogenated oils are trans-fat-free but high in saturated fat.',
    'interesterified fat': 'Interesterified fat is a processed fat made by rearranging fatty acids in oils to change their physical properties. Used as a trans-fat-free alternative to partially hydrogenated oils in margarine and shortening. Research on long-term health effects is ongoing.',
    'acidity regulator': 'Acidity regulator is a general term for food additives that control and maintain pH (acidity/alkalinity) in foods. Common examples include citric acid (E330), lactic acid (E270), acetic acid (E260) and phosphoric acid (E338).',
    'raising agent': 'Raising agent (leavening agent) is a substance that produces gas (usually CO₂) in dough or batter to make baked goods light and porous. Common examples include baking powder, sodium bicarbonate (E500) and ammonium bicarbonate (E503).',
    'anti caking agent': 'Anti-caking agent is a food additive that prevents powdered or granulated materials from clumping. Common examples include silicon dioxide (E551), calcium silicate (E552) and magnesium carbonate (E504).',
    'humectant': 'Humectant is a substance that attracts and retains moisture. Used in baked goods, confectionery and cosmetics to prevent drying out. Common food humectants include glycerol (E422), sorbitol (E420) and propylene glycol (E1520).',
    'glycerol': 'Glycerol (Glycerin/E422/INS 422) is a sweet, colourless liquid used as a humectant in baked goods, confectionery and beverages to retain moisture and improve texture. Safe and naturally derived from fats.',
    'e422': 'E422/INS 422 is Glycerol (Glycerin), a humectant used to retain moisture in foods. Naturally derived from fats. Safe.',
    'propylene glycol': 'Propylene Glycol (E1520/INS 1520) is used as a humectant, solvent and carrier for flavourings in foods. Generally regarded as safe in food use; different from ethylene glycol (antifreeze) which is toxic.',
    'e1520': 'E1520/INS 1520 is Propylene Glycol, a humectant and solvent used in flavourings and food coatings. Generally safe in food use levels.',
    'shellac': 'Shellac (E904/INS 904) is a natural resin secreted by the lac bug. Used as a glazing agent on confectionery, pills and fresh citrus fruit. Provides a shiny coating. Animal-derived; not vegan.',
    'e904': 'E904/INS 904 is Shellac, a natural animal-derived resin used as a glazing agent on sweets, chocolates and citrus fruit. Not vegan.',
    'beeswax': 'Beeswax (E901/INS 901) is a natural wax produced by honeybees. Used as a glazing agent on confectionery and fresh fruit. Animal-derived; not vegan.',
    'e901': 'E901/INS 901 is Beeswax, a natural glaze from honeybees used on sweets and fresh fruit. Not vegan.',
    'carnauba wax': 'Carnauba wax (E903/INS 903) is a plant-based wax from Brazilian carnauba palm leaves. Used as a glazing agent on confectionery, chewing gum and fresh fruit. Vegan-friendly.',
    'e903': 'E903/INS 903 is Carnauba Wax, a plant-based glazing agent used on sweets and fruit. Vegan-friendly.',
    'mineral oil': 'White mineral oil (E905/INS 905) is a highly refined petroleum-derived oil used as a glazing and coating agent on fresh fruit, dried fruit and confectionery. Concern exists around contamination with mineral oil aromatic hydrocarbons (MOAH) which are potentially carcinogenic.',
    'e905': 'E905/INS 905 is Mineral Oil (White Oil), a petroleum-derived glazing agent on fresh and dried fruit. Potential MOAH contamination concern.',
    'polysorbate 80': 'Polysorbate 80 (E433/INS 433) is a synthetic emulsifier made from sorbitol and oleic acid. Widely used in ice cream, baked goods and pharmaceuticals. Some animal studies suggest effects on gut microbiome at high doses.',
    'e433': 'E433/INS 433 is Polysorbate 80, a synthetic emulsifier used in ice cream and pharmaceuticals. Generally safe; some research on gut microbiome effects at high animal doses.',
    'polysorbate 60': 'Polysorbate 60 (E435/INS 435) is a synthetic emulsifier used in baked goods, whipped toppings and non-dairy creamers. Similar to Polysorbate 80.',
    'e435': 'E435/INS 435 is Polysorbate 60, a synthetic emulsifier used in baked goods and whipped toppings.',
    'polysorbate 20': 'Polysorbate 20 (E432/INS 432) is a mild synthetic emulsifier used in foods and cosmetics. Generally safe.',
    'e432': 'E432/INS 432 is Polysorbate 20, a mild synthetic emulsifier used in some foods and widely in cosmetics.',
    'sodium stearoyl lactylate': 'Sodium Stearoyl Lactylate (SSL/E481/INS 481) is an emulsifier made from stearic acid and lactic acid. Widely used in bread, biscuits and pasta to strengthen gluten network, improve volume and extend shelf life.',
    'calcium stearoyl lactylate': 'Calcium Stearoyl Lactylate (CSL/E482/INS 482) is similar to SSL but uses calcium instead of sodium. Used as a dough conditioner in bread and as an emulsifier in coffee whiteners.',
    'sorbitan monostearate': 'Sorbitan Monostearate (Span 60/E491/INS 491) is an emulsifier used in baked goods, confectionery and cream fillings. Generally safe.',
    'e491': 'E491/INS 491 is Sorbitan Monostearate, an emulsifier used in baked goods and confectionery.',
    'quillaia extract': 'Quillaia extract (E999/INS 999) is a natural foaming agent from the bark of the soapbark tree, used in beverages (root beer, ginger beer) to create foam. Also used in frothy coffee drinks.',
    'e999': 'E999/INS 999 is Quillaia Extract, a natural foaming agent from soapbark tree bark. Used in beverages and cocktails.',

    # ── Common cosmetic & personal care additions ─────────────────────────────
    'dimethicone': 'Dimethicone is a silicone polymer widely used in hair conditioners, moisturisers, sunscreens and makeup primers. Creates a smooth, silky feel and forms a protective barrier on skin and hair. Non-comedogenic at standard concentrations. Considered safe by regulatory bodies.',
    'cyclomethicone': 'Cyclomethicone is a lightweight, volatile silicone used in hair care and skin care products. Evaporates after application, leaving no residue. Considered safe at current use levels.',
    'cyclopentasiloxane': 'Cyclopentasiloxane (D5) is a volatile silicone used in deodorants, hair care and skin care. The EU has restricted its use in rinse-off cosmetics citing environmental persistence concerns, though it is considered safe for human health.',
    'phenoxyethanol': 'Phenoxyethanol is a widely used preservative in cosmetics and personal care products, replacing parabens. Effective against bacteria and some fungi. Generally safe at ≤1%; high concentrations may irritate skin. EU and FDA permit use up to 1%.',
    'ethylhexylglycerin': 'Ethylhexylglycerin is a multifunctional cosmetic ingredient — a humectant, skin conditioner and mild preservative booster. Often used alongside phenoxyethanol. Generally safe.',
    'caprylyl glycol': 'Caprylyl Glycol is a humectant and mild antimicrobial agent used in cosmetics as a preservative booster. Often paired with phenoxyethanol or parabens. Generally safe.',
    'sodium pca': 'Sodium PCA (Sodium Pyrrolidone Carboxylic Acid) is a natural humectant — one of the skin\'s natural moisturising factors (NMF). Used in moisturisers and hair conditioners to attract and retain water. Safe and skin-compatible.',
    'glycerin': 'Glycerin (Glycerol) is a natural humectant found in all fats and oils. Widely used in skincare to attract moisture from the air into the skin. Effective, safe and well-tolerated by all skin types.',
    'propanediol': 'Propanediol (1,3-Propanediol) is a plant-derived humectant and solvent used in cosmetics as an alternative to propylene glycol. Used in serums, moisturisers and sunscreens. Generally well-tolerated.',
    'butylene glycol': 'Butylene Glycol (1,3-Butanediol) is a humectant and solvent used in cosmetics. Helps other ingredients penetrate skin. Generally safe; occasionally causes contact dermatitis in sensitive individuals.',
    'pentylene glycol': 'Pentylene Glycol is a humectant and mild preservative used in skincare products. Provides moisture retention and antimicrobial properties. Generally safe and well-tolerated.',
    'octyldodecanol': 'Octyldodecanol is a fatty alcohol used as an emollient and solvent in cosmetics. Helps dissolve other ingredients and creates a smooth skin feel. Safe.',
    'isopropyl myristate': 'Isopropyl Myristate is an ester of isopropanol and myristic acid used as an emollient in cosmetics. Provides a lightweight, non-greasy feel. Can be comedogenic for some people.',
    'caprylic capric triglyceride': 'Caprylic/Capric Triglyceride (MCT oil) is a fraction of coconut or palm kernel oil. Used as a light emollient and carrier oil in cosmetics. Non-comedogenic and well-tolerated.',
    'coco caprylate': 'Coco-Caprylate is a lightweight emollient from coconut alcohol. Used in sunscreens and moisturisers for a silky texture. Safe and skin-compatible.',
    'squalane': 'Squalane is a stable, saturated form of squalene used as an emollient in skincare. Derived from olive oil (plant-based) or shark liver oil (animal). Plant-based squalane is widely preferred. Non-comedogenic and excellent skin compatibility.',
    'squalene': 'Squalene is an unsaturated lipid naturally produced by the human body and found in olive oil, amaranth and shark liver. Used in cosmetics as a moisturiser; however, due to instability it is usually converted to squalane for use.',
    'jojoba oil': 'Jojoba oil is technically a liquid wax extracted from jojoba plant seeds. Closely resembles skin\'s natural sebum; used in moisturisers, hair care and lip products. Non-comedogenic and stable.',
    'argan oil': 'Argan oil is pressed from the kernels of the argan tree from Morocco. Rich in oleic acid, linoleic acid, tocopherols and polyphenols. Used in hair care and skincare for its nourishing and antioxidant properties.',
    'rosehip oil': 'Rosehip oil is cold-pressed from rosehip seeds. Rich in Vitamin A (as retinol precursor), Vitamin C, and linoleic acid. Used in anti-ageing skincare. May cause sensitivity in some individuals.',
    'marula oil': 'Marula oil is pressed from the kernels of the marula fruit. Rich in oleic acid and antioxidants. Used as a lightweight face and hair oil.',
    'shea butter': 'Shea butter is a fat extracted from the nuts of the shea tree, native to Africa. Rich in oleic acid, stearic acid and various vitamins. Widely used in moisturisers, hair care and lip balms. Generally safe; tree nut allergy may be relevant for sensitive individuals.',
    'cocoa butter': 'Cocoa butter is a vegetable fat from cocoa beans. Used in moisturisers, lip products and chocolate manufacturing. Rich in saturated fats and antioxidants. Generally safe for topical use.',
    'cetyl alcohol': 'Cetyl alcohol is a fatty alcohol derived from coconut or palm oil. Used as an emulsifier, emollient and thickener in creams and lotions. Not drying like ethyl alcohol — fatty alcohols are beneficial in skincare.',
    'stearyl alcohol': 'Stearyl alcohol is a fatty alcohol used as an emollient and emulsifier in creams and lotions. Safe and non-irritating for most skin types.',
    'cetearyl alcohol': 'Cetearyl alcohol is a mixture of cetyl and stearyl fatty alcohols used as an emulsifier and emollient in skincare. Safe and beneficial for skin; not the same as drying alcohols.',
    'behenyl alcohol': 'Behenyl Alcohol (Docosanol) is a fatty alcohol used as an emollient and emulsifier in cosmetics. Also FDA-approved as an antiviral for cold sore treatment. Safe.',
    'stearic acid': 'Stearic acid is a saturated fatty acid found naturally in animal and vegetable fats. Used as an emulsifier, stabiliser and thickener in cosmetics and personal care. Safe.',
    'palmitic acid': 'Palmitic acid is a saturated fatty acid found in palm oil, meat and dairy. Used as an emollient and thickener in cosmetics. In diet, high intake is linked to cardiovascular risk.',
    'myristic acid': 'Myristic acid is a saturated fatty acid found in coconut oil and dairy. Used as a skin-conditioning agent and surfactant in cosmetics. Generally safe topically.',
    'lauric acid': 'Lauric acid is a saturated fatty acid in coconut and palm kernel oil. Antimicrobial properties; used in soaps and personal care. Also naturally present in breast milk.',
    'carbomer': 'Carbomer is a synthetic polymer used as a thickener and gelling agent in gels, creams and serums. Creates a clear, stable gel texture. Generally safe; may cause irritation in sensitive individuals.',
    'xanthan gum': 'Xanthan gum (E415/INS 415) is a natural polysaccharide produced by fermenting sugars with the bacterium Xanthomonas campestris. Widely used as a thickener and stabiliser in dressings, sauces, gluten-free baking and beverages. Safe.',
    'e415': 'E415/INS 415 is Xanthan Gum, a fermentation-derived polysaccharide thickener. Used in salad dressings, sauces and gluten-free products. Safe.',
    'gellan gum': 'Gellan gum (E418/INS 418) is a microbial polysaccharide used as a gelling and stabilising agent in plant-based milks, beverages and gel desserts. Generally safe.',
    'locust bean gum': 'Locust bean gum (Carob gum/E410/INS 410) is a natural thickener from carob seeds. Used in ice cream, cheese and infant formula to improve texture and prevent ice crystal formation.',
    'tara gum': 'Tara gum (E417/INS 417) is a natural thickener from tara tree seeds, related to locust bean gum. Used in processed meats, dairy products and baked goods.',
    'e417': 'E417/INS 417 is Tara Gum, a natural thickener from tara tree seeds. Used in processed meats and dairy.',
    'konjac gum': 'Konjac gum (Konjac glucomannan/E425/INS 425) is extracted from the konjac plant root. A highly viscous soluble fibre used as a thickener and gelling agent. Also sold as a dietary supplement for weight management. Safe but must be consumed with adequate water.',
    'e425': 'E425/INS 425 is Konjac Gum (Glucomannan), a highly viscous natural thickener. Also used as a dietary fibre supplement for weight management.',
    'tragacanth': 'Tragacanth (E413/INS 413) is a natural gum from the Astragalus shrub. Used as a thickener and stabiliser in confectionery, dressings and pharmaceuticals. Rare allergen.',
    'e413': 'E413/INS 413 is Tragacanth Gum, a natural stabiliser from Astragalus shrub. Used in confectionery and pharmaceuticals.',
    'modified potato starch': 'Modified potato starch (E1404-1442 range) is potato starch treated to improve its performance under heat, cold and acidic conditions. Used as a thickener in soups, sauces and ready meals. Safe.',
    'oxidised starch': 'Oxidised Starch (E1404/INS 1404) is a modified starch treated with oxidising agents to reduce viscosity and improve stability. Used in paper manufacturing and some foods as a thickener.',
    'e1404': 'E1404/INS 1404 is Oxidised Starch, a modified starch with reduced viscosity used in certain food applications.',
    'phosphoric acid': 'Phosphoric acid (E338/INS 338) is a mineral acid used to acidify beverages — especially colas — giving them their characteristic sharp taste. Also used in cheese processing. May affect tooth enamel and bone density with chronic high consumption.',
    'sodium hexametaphosphate': 'Sodium Hexametaphosphate (E452/INS 452) is a polyphosphate used as an emulsifier, sequestrant and texture modifier in processed cheeses, surimi and seafood products.',
    'e452': 'E452/INS 452 is Sodium Hexametaphosphate, an emulsifier and sequestrant used in processed cheese and seafood products.',
    'potassium chloride': 'Potassium chloride (E508/INS 508) is used as a salt substitute and flavour enhancer. Provides a salty taste with less sodium. Important mineral for heart and kidney function — but those with kidney disease should consult a doctor before using high-potassium salt substitutes.',
    'acetylated starch': 'Acetylated Starch (E1420/INS 1420) is a modified starch where some hydroxyl groups are replaced with acetyl groups. More stable under acidic conditions and lower temperatures. Used as a thickener in sauces, dressings and dairy products.',
    'hydroxypropyl starch e1440': 'Hydroxypropyl Starch (E1440/INS 1440) is a modified starch with improved freeze-thaw stability. Used in frozen foods, dairy desserts and sauces.',
    'distarch phosphate': 'Distarch Phosphate (E1412/INS 1412) is a cross-linked modified starch providing enhanced stability under heat, shear and acidic conditions. Used in soups, sauces and canned foods.',
    'e1412': 'E1412/INS 1412 is Distarch Phosphate, a cross-linked modified starch thickener with high stability. Used in soups and canned foods.',


    # ── INS/E-Number entries added for searchability by number ────────────────

    # --- Raising Agents / Leavening Agents ---
    'e500': 'E500 / INS 500 — Sodium Carbonates. A group of leavening and pH-adjusting agents used in baking, confectionery and biscuits. Sodium bicarbonate (500ii) is common baking soda; sodium carbonate (500i) is washing soda. Permitted by FSSAI and Codex as a safe food additive.',
    'e500i': 'E500(i) / INS 500(i) — Sodium Carbonate (soda ash / washing soda). Used as a leavening agent, pH adjuster and firming agent in baked goods, cocoa powder and noodles. Safe at permitted food levels.',
    'e500ii': 'E500(ii) / INS 500(ii) — Sodium Bicarbonate (baking soda). The most widely used leavening agent in baking — reacts with acidic ingredients to produce CO₂ bubbles that make cakes, cookies and bread rise. Safe; the body handles it like ordinary sodium and CO₂.',
    'e500iii': 'E500(iii) / INS 500(iii) — Sodium Sesquicarbonate. A mixture of sodium carbonate and sodium bicarbonate used as a leavening and pH-control agent. Safe at food-use levels.',
    'e501': 'E501 / INS 501 — Potassium Carbonates. Used as leavening agents and acidity regulators in biscuits, cocoa and baked goods. Provide a milder alkalinity than sodium carbonates.',
    'e501i': 'E501(i) / INS 501(i) — Potassium Carbonate. Used as a leavening agent and pH adjuster in baked goods and cocoa products. Generally safe.',
    'e501ii': 'E501(ii) / INS 501(ii) — Potassium Bicarbonate. A leavening agent used in baking as a sodium-free alternative to baking soda. Safe.',
    'e503': 'E503 / INS 503 — Ammonium Carbonates. Leavening agents used in dry biscuits, crackers and cookies. At baking temperatures they fully decompose to CO₂, ammonia and water — no ammonia remains in the finished product.',
    'e503i': 'E503(i) / INS 503(i) — Ammonium Carbonate (bakers ammonia). Traditional leavening agent for crisp baked goods. Fully decomposes during baking; no ammonia residue in finished product.',
    'e503ii': 'E503(ii) / INS 503(ii) — Ammonium Bicarbonate. A leavening agent used in dry biscuits, crackers and cookies. Decomposes completely at baking temperatures into CO₂, water and ammonia gas — no ammonia remains in the baked product.',
    'e504': 'E504 / INS 504 — Magnesium Carbonates. Used as an anti-caking agent, colour retention agent and leavening agent. Also used as a dietary magnesium supplement.',
    'e504i': 'E504(i) / INS 504(i) — Magnesium Carbonate. Anti-caking and leavening agent; also used as a dietary magnesium source.',
    'e504ii': 'E504(ii) / INS 504(ii) — Magnesium Hydroxide Carbonate (magnesite). Used as an anti-caking agent and leavening agent. Safe.',
    'e450': 'E450 / INS 450 — Diphosphates (Pyrophosphates). A group of raising agents and emulsifying salts used in baking powder, processed meats and processed cheese. The most common is sodium acid pyrophosphate (SAPP/E450i). Excessive phosphate intake is a concern for kidney health.',
    'e450i': 'E450(i) / INS 450(i) — Disodium Diphosphate (SAPP). Used in baking powder as a slow-acting leavening acid, and in processed meats and seafood to retain moisture.',
    'e451': 'E451 / INS 451 — Triphosphates (Tripolyphosphates). Used as emulsifying salts in processed cheese and as water-retention agents in seafood and processed meats. High phosphate intake may affect kidney function.',
    'e451i': 'E451(i) / INS 451(i) — Pentasodium Triphosphate (STPP). Used in processed cheese, seafood and meat products to retain moisture and improve texture.',
    'e452': 'E452 / INS 452 — Polyphosphates. Used as emulsifying salts in processed cheese and as stabilisers and moisture-retention agents in meat and seafood products.',

    # --- Emulsifiers ---
    'e322': 'E322 / INS 322 — Lecithins. Natural emulsifiers extracted from soybean oil, sunflower or egg yolk. Widely used in chocolate, bread, margarine and baked goods to blend fat and water smoothly. The most commonly used food emulsifier globally. Important soy allergen if soy-derived.',
    'e322i': 'E322(i) / INS 322(i) — Lecithin. The most widely used natural emulsifier, typically from soybean or sunflower. Used in chocolate, baked goods, margarine and confectionery. Natural and well-tolerated; note soy allergen if soy-sourced.',
    'e322ii': 'E322(ii) / INS 322(ii) — Hydroxylated Lecithin. Chemically modified lecithin with improved emulsifying efficiency. Used in bread, margarine and confectionery. Same allergen profile as standard lecithin.',
    'e471': 'E471 / INS 471 — Mono- and Diglycerides of Fatty Acids. Emulsifiers produced from glycerol and fatty acids (from vegetable or animal fats). Widely used in bread, margarine, ice cream and baked goods to improve texture, volume and shelf life. May contain residual trans-fatty acids if made from partially hydrogenated oils; also contains glycidol fatty acid esters (GFAEs) at trace levels — the European Food Safety Authority has reviewed this and set limits.',
    'e472a': 'E472a / INS 472a — Acetic Acid Esters of Mono- and Diglycerides (ACETEM). Emulsifier used in bread and baked goods. Derived from E471 esterified with acetic acid. Generally safe.',
    'e472b': 'E472b / INS 472b — Lactic Acid Esters of Mono- and Diglycerides (LACTEM). Emulsifier used in bread, whipped products and dairy analogs. Improves aeration and shelf life. Generally safe.',
    'e472c': 'E472c / INS 472c — Citric Acid Esters of Mono- and Diglycerides (CITREM). Emulsifier used in margarine and processed foods as an antioxidant emulsifier. Generally safe.',
    'e472e': 'E472e / INS 472e — Diacetyl Tartaric Acid Esters of Mono- and Diglycerides (DATEM). A powerful dough emulsifier and gluten network strengthener used in bread, rolls and wraps to improve volume and crumb structure. Widely used in commercial bread-making. Generally safe.',
    'e473': 'E473 / INS 473 — Sucrose Esters of Fatty Acids. Emulsifiers made from sucrose and fatty acids, used in coffee creamers, baked goods and dairy products. Generally safe.',
    'e475': 'E475 / INS 475 — Polyglycerol Esters of Fatty Acids. Emulsifiers used in low-fat spreads, margarine and baked goods. Generally recognised as safe.',
    'e476': 'E476 / INS 476 — Polyglycerol Polyricinoleate (PGPR). A synthetic emulsifier made from glycerol and castor oil, primarily used in chocolate to improve flow and reduce cocoa butter usage. Generally safe at permitted levels.',
    'e481': 'E481 / INS 481 — Sodium Stearoyl Lactylate (SSL). An emulsifier and dough conditioner made from stearic acid and lactic acid. Strengthens gluten networks in bread, improves volume and extends shelf life. Widely used in commercial bread. Generally safe.',
    'e482': 'E482 / INS 482 — Calcium Stearoyl Lactylate (CSL). Similar to SSL but calcium-based. Used as a dough conditioner in bread and as an emulsifier in coffee whiteners and whipped toppings. Generally safe.',
    'e491': 'E491 / INS 491 — Sorbitan Monostearate (Span 60). An emulsifier used in baked goods, confectionery fillings and yeast-raised products. Generally safe.',
    'e442': 'E442 / INS 442 — Ammonium Phosphatides. An emulsifier from rapeseed oil used in chocolate as a lecithin alternative to improve flow properties. Generally safe.',

    # --- Acidity Regulators / Acidulants ---
    'e260': 'E260 / INS 260 — Acetic Acid (Vinegar acid). The acid responsible for the sour taste and preserving properties of vinegar. Used as an acidulant and preservative in pickles, sauces, condiments and baked goods. Safe.',
    'e270': 'E270 / INS 270 — Lactic Acid. A naturally occurring organic acid produced by fermentation, present in yoghurt, cheese, sauerkraut and sourdough. Used as an acidulant, pH adjuster and preservative in a wide range of foods. Safe.',
    'e296': 'E296 / INS 296 — Malic Acid. A naturally occurring fruit acid found in apples, pears and cherries. Used as an acidulant to give a smooth, tart flavour in beverages, confectionery and bakery products. Safe.',
    'e297': 'E297 / INS 297 — Fumaric Acid. A dicarboxylic acid used as an acidulant and leavening acid in baked goods, beverages and confectionery. Used as a natural alternative to citric acid. Safe.',
    'e325': 'E325 / INS 325 — Sodium Lactate. The sodium salt of lactic acid, used as a humectant, acidity regulator and preservative in meat products, confectionery and baked goods. Generally safe.',
    'e327': 'E327 / INS 327 — Calcium Lactate. The calcium salt of lactic acid, used as a firming agent, acidity regulator and calcium fortification agent. Generally safe.',
    'e330': 'E330 / INS 330 — Citric Acid. The most widely used acidulant in the food industry, naturally found in citrus fruits. Used in beverages, confectionery, jams and processed foods to add tartness and act as a pH adjuster and preservative. Safe.',
    'e331': 'E331 / INS 331 — Sodium Citrates. Sodium salts of citric acid used as acidity regulators, emulsifying salts and preservatives in beverages, processed cheese, confectionery and sausages. Safe.',
    'e332': 'E332 / INS 332 — Potassium Citrates. Potassium salts of citric acid used as acidity regulators and sequestrants in beverages and confectionery. Safe.',
    'e333': 'E333 / INS 333 — Calcium Citrates. Calcium salts of citric acid used as acidity regulators, firming agents and calcium supplements. Safe.',
    'e334': 'E334 / INS 334 — Tartaric Acid. A naturally occurring acid from grapes and other fruits, used as an acidulant and antioxidant in baking powder, wine, confectionery and beverages. Safe.',
    'e335': 'E335 / INS 335 — Sodium Tartrates. Sodium salts of tartaric acid used as acidity regulators and stabilisers in confectionery and processed foods. Safe.',
    'e336': 'E336 / INS 336 — Potassium Tartrates (Cream of Tartar). Potassium salt of tartaric acid used as a leavening agent with baking soda, a stabiliser for whipped egg whites and a wine stabiliser. Safe.',
    'e337': 'E337 / INS 337 — Potassium Sodium Tartrate (Rochelle Salt). A mixed tartrate salt used as an acidity regulator and sequestrant in confectionery and meat products. Safe.',
    'e339': 'E339 / INS 339 — Sodium Phosphates. A group of sodium salts of phosphoric acid used as emulsifying salts, acidity regulators and nutrient supplements. Used in processed cheese, meat products and cereals. High phosphate intake may affect kidney health with chronic excess.',
    'e340': 'E340 / INS 340 — Potassium Phosphates. Potassium salts of phosphoric acid used as acidity regulators, emulsifying salts and potassium supplements. Used in processed cheese and instant beverages.',
    'e341': 'E341 / INS 341 — Calcium Phosphates. Calcium salts of phosphoric acid used as a raising agent, firming agent, anti-caking agent and calcium supplement. Found in baking powder, flour treatment and cereals. Safe.',
    'e341i': 'E341(i) / INS 341(i) — Monocalcium Phosphate (MCP). A fast-acting leavening acid used in baking powder. Reacts with sodium bicarbonate during mixing to produce CO₂. Used in cakes, muffins and self-raising flour.',
    'e341ii': 'E341(ii) / INS 341(ii) — Dicalcium Phosphate (DCP). Used as a leavening agent, calcium supplement and anti-caking agent in flour and cereals. Safe.',
    'e341iii': 'E341(iii) / INS 341(iii) — Tricalcium Phosphate (TCP). Used as an anti-caking agent, calcium fortification agent and leavening agent in powdered foods, cereals and supplements. Safe.',

    # --- Antioxidants ---
    'e300': 'E300 / INS 300 — Ascorbic Acid (Vitamin C). The most widely used food antioxidant — prevents browning, rancidity and vitamin degradation. Used in fruit juices, meat products, bread and cereals. Same as supplemental Vitamin C; safe and beneficial.',
    'e301': 'E301 / INS 301 — Sodium Ascorbate. The sodium salt of Vitamin C, used as an antioxidant preservative in processed meats, cured meats and bakery products. Provides the same antioxidant action as ascorbic acid. Safe.',
    'e302': 'E302 / INS 302 — Calcium Ascorbate. The calcium salt of Vitamin C, used as an antioxidant and calcium supplement. Safe.',
    'e304': 'E304 / INS 304 — Ascorbyl Palmitate / Ascorbyl Stearate. Fat-soluble esters of Vitamin C used to protect oils and fat-containing foods from oxidation. Used in frying oils, margarines and infant formula. Safe.',
    'e306': 'E306 / INS 306 — Mixed Tocopherols (Natural Vitamin E). A natural antioxidant extract from vegetable oils containing alpha, beta, gamma and delta tocopherols. Used to protect oils and fat-containing foods. Safe.',
    'e307': 'E307 / INS 307 — Alpha-Tocopherol (Vitamin E). The most biologically active form of Vitamin E, used as a natural antioxidant in oils, margarines and infant formula. Safe and nutritionally beneficial.',
    'e308': 'E308 / INS 308 — Gamma-Tocopherol. A form of Vitamin E used as an antioxidant in edible fats and oils. Safe.',
    'e309': 'E309 / INS 309 — Delta-Tocopherol. A form of Vitamin E used as an antioxidant. Safe.',
    'e315': 'E315 / INS 315 — Erythorbic Acid (Isoascorbic Acid). A stereoisomer of Vitamin C used as an antioxidant in cured meats and beverages. Not equivalent to Vitamin C nutritionally, but effective as an antioxidant preservative. Safe.',
    'e316': 'E316 / INS 316 — Sodium Erythorbate. The sodium salt of erythorbic acid, widely used in hot dogs, sausages and cured meats to preserve colour and prevent rancidity. Safe.',

    # --- Sweeteners (Sugar Alcohols and Novel) ---
    'e420': 'E420 / INS 420 — Sorbitol. A naturally occurring sugar alcohol found in fruits, also produced commercially. Used as a low-calorie sweetener, humectant and bulking agent in sugar-free confectionery, diabetic foods and cosmetics. May cause digestive upset at high doses (>50g). About 60% as sweet as sugar.',
    'e420i': 'E420(i) / INS 420(i) — Sorbitol. Sugar alcohol sweetener and humectant. See E420.',
    'e421': 'E421 / INS 421 — Mannitol. A naturally occurring sugar alcohol found in mushrooms, seaweed and sweet potatoes. Used as a low-calorie sweetener and anti-caking agent in sugar-free confectionery. Poorly absorbed; may cause laxative effect at high doses.',
    'e953': 'E953 / INS 953 — Isomalt. A sugar substitute derived from sucrose, approximately half as sweet. Used in sugar-free confectionery, chewing gum and diabetic foods. Low glycaemic index; may cause digestive discomfort in large quantities.',
    'e960': 'E960 / INS 960 — Steviol Glycosides (Stevia). Natural zero-calorie sweeteners extracted from the stevia plant (Stevia rebaudiana), 200–400 times sweeter than sugar. Used in beverages, dairy products and tabletop sweeteners. Approved by FSSAI, FDA and EU. Generally well-tolerated.',
    'e960a': 'E960a / INS 960a — Steviol Glycosides from Stevia. Natural high-intensity sweetener from stevia leaves. Zero calorie. Generally safe.',
    'e961': 'E961 / INS 961 — Neotame. A synthetic high-intensity sweetener (7,000–13,000 times sweeter than sugar) derived from aspartame but metabolised differently — safe for people with phenylketonuria. Used in tiny amounts in beverages and processed foods.',
    'e962': 'E962 / INS 962 — Aspartame-Acesulfame Salt. A blend of aspartame and acesulfame potassium in a 2:1 ratio, providing a more sugar-like taste profile than either alone. Used in beverages and sugar-free products. Contains phenylalanine (PKU warning).',
    'e965': 'E965 / INS 965 — Maltitol. A sugar alcohol approximately 75–90% as sweet as sugar, derived from maltose. Used in sugar-free chocolates, baked goods and confectionery. Low glycaemic impact; may cause laxative effects at high intakes.',
    'e966': 'E966 / INS 966 — Lactitol. A sugar alcohol made from lactose (milk sugar), approximately 40% as sweet as sugar. Used in sugar-free confectionery and as a bulk laxative in pharmaceutical use. Contains lactose backbone — relevant for lactose-intolerant individuals.',
    'e967': 'E967 / INS 967 — Xylitol. A naturally occurring sugar alcohol found in birch trees, plums and corn cobs. Approximately as sweet as sugar with 40% fewer calories. Used in sugar-free gum, confectionery and dental products — proven to reduce tooth decay. High doses cause laxative effects.',
    'e968': 'E968 / INS 968 — Erythritol. A naturally occurring sugar alcohol found in fermented foods. Zero calories, approximately 60–70% as sweet as sugar. Does not spike blood glucose or insulin. Best tolerated of all sugar alcohols; rarely causes digestive upset.',

    # --- Food Colours ---
    'e100': 'E100 / INS 100 — Curcumin. A natural bright-yellow pigment derived from turmeric (Curcuma longa) rhizomes. Used to colour mustard, dairy products, confectionery and sauces. Also used as a dietary supplement for its anti-inflammatory properties. Safe.',
    'e100i': 'E100(i) / INS 100(i) — Curcumin. Natural yellow pigment from turmeric. Permitted food colour. Safe.',
    'e101': 'E101 / INS 101 — Riboflavin (Vitamin B2). A natural yellow-orange pigment used as a food colour and nutritional supplement. Found naturally in milk, eggs, meat and leafy greens. Used to colour pasta, bread and dairy products. Safe and nutritionally beneficial.',
    'e101i': 'E101(i) / INS 101(i) — Riboflavin. Natural Vitamin B2 used as a yellow food colour and nutritional supplement. Safe.',
    'e120': 'E120 / INS 120 — Cochineal / Carmine / Carminic Acid. A red dye derived from dried female cochineal insects (Dactylopius coccus). Used to colour yoghurts, juices, confectionery and cosmetics. Animal-derived — not vegan. Can cause severe allergic reactions including anaphylaxis in susceptible individuals; FDA mandates explicit labelling.',
    'e140': 'E140 / INS 140 — Chlorophylls and Chlorophyllins. Natural green pigments extracted from plants. Used to give green colour to oils, fats, confectionery and beverages. Safe.',
    'e141': 'E141 / INS 141 — Copper Complexes of Chlorophylls / Chlorophyllins. Copper-stabilised versions of chlorophyll used to create a more stable, brighter green colour in foods. Approved by FSSAI and EU. Safe at permitted levels.',
    'e142': 'E142 / INS 142 — Green S (Lissamine Green). A synthetic green dye used in canned vegetables, mint jelly and some confectionery. Banned in USA, Canada, Japan and Australia. Approved in EU and India with restrictions.',
    'e150a': 'E150a / INS 150a — Plain Caramel (Caramel I). Produced by heating carbohydrates without acids or alkalis. Used in spirits, vinegar and confectionery. Considered the safest class of caramel colour.',
    'e150b': 'E150b / INS 150b — Caustic Sulfite Caramel (Caramel II). Produced by reacting carbohydrates with sulfite compounds. Used in spirits. Rare in other foods.',
    'e150c': 'E150c / INS 150c — Ammonia Caramel (Caramel III). Produced by reacting carbohydrates with ammonium compounds. Used in beer and soy sauce. Contains 2-methylimidazole and 4-methylimidazole (4-MEI) as trace by-products — 4-MEI is listed as a possible carcinogen by IARC (Group 2B); California Prop 65 warning required.',
    'e150d': 'E150d / INS 150d — Sulfite Ammonia Caramel (Caramel IV). Produced with both sulfite and ammonium compounds. The most widely used caramel colour — in colas, soy sauce, beer and baked goods. Contains 4-MEI (possible carcinogen, IARC Group 2B); Coca-Cola reformulated in some markets due to Prop 65. FSSAI permits it; California requires a cancer warning label.',
    'e151': 'E151 / INS 151 — Brilliant Black BN (Black PN). A synthetic black azo dye used to colour confectionery, sauces and condiments. Banned in USA, Canada, Japan and Australia. Carries the EU hyperactivity warning label. Approved in EU and India with restrictions.',
    'e160b': 'E160b / INS 160b — Annatto (Bixin / Norbixin). A natural orange-yellow colour derived from the seeds of the annatto tree (Bixa orellana). Widely used in cheeses, butter, margarines, snacks and ice cream. Generally safe; occasional allergic reactions reported. No hyperactivity concerns.',
    'e160c': 'E160c / INS 160c — Paprika Extract / Capsanthin / Capsorubin. Natural orange-red colour from dried red peppers. Used in sausages, processed meats, sauces, snacks and dairy products. Safe.',
    'e162': 'E162 / INS 162 — Beetroot Red (Betanin). Natural red pigment extracted from red beetroot. Used in yoghurts, ice cream, confectionery and beverages. Safe. Not stable to heat; colour may fade in cooking.',
    'e163': 'E163 / INS 163 — Anthocyanins. Natural blue-purple to red pigments found in berries, red cabbage, grapes and other fruits. Used to colour beverages, confectionery and dairy products. Safe and rich in antioxidants.',
    'e172': 'E172 / INS 172 — Iron Oxides and Iron Hydroxides. Inorganic colouring agents (yellow, red, black) used in sugar coatings, chocolate casings, olives and pharmaceuticals. Also provide a small amount of dietary iron. Safe at food-use levels.',

    # --- Preservatives (additional) ---
    'e200': 'E200 / INS 200 — Sorbic Acid. A natural organic acid originally isolated from rowan berries, now produced synthetically. The parent compound of the sorbate preservatives (E202, E203). Used to inhibit mould and yeast in cheese, wine, dried fruits and baked goods. Safe.',
    'e201': 'E201 / INS 201 — Sodium Sorbate. The sodium salt of sorbic acid, used as a preservative. Inhibits mould and yeast in foods and beverages. Generally safe at permitted levels.',
    'e203': 'E203 / INS 203 — Calcium Sorbate. The calcium salt of sorbic acid, used as a preservative to inhibit mould and yeast. Provides a calcium source alongside the preservative function. Safe.',
    'e210': 'E210 / INS 210 — Benzoic Acid. The acid form of sodium benzoate (E211). Naturally present in cranberries, cinnamon and prunes. Used as a preservative in acidic foods and beverages. Same benzene-formation concern as E211 when combined with Vitamin C.',
    'e212': 'E212 / INS 212 — Potassium Benzoate. The potassium salt of benzoic acid, used as an antimicrobial preservative in foods and beverages. Same benzene-formation risk as sodium benzoate (E211) in combination with Vitamin C.',
    'e213': 'E213 / INS 213 — Calcium Benzoate. The calcium salt of benzoic acid used as a preservative. Similar properties and concerns as sodium benzoate (E211).',
    'e218': 'E218 / INS 218 — Methyl p-Hydroxybenzoate (Methylparaben). The INS/E-number code for methylparaben, a widely used preservative in cosmetics, pharmaceuticals and foods. Hormone-disrupting paraben — same concerns as "methylparaben".',
    'e219': 'E219 / INS 219 — Sodium Methyl p-Hydroxybenzoate (Sodium Methylparaben). Sodium salt of methylparaben used as a preservative in cosmetics and some food products. Same endocrine disruption concerns as methylparaben.',
    'e221': 'E221 / INS 221 — Sodium Sulfite. A sulfite preservative used to prevent browning in dried fruits, potatoes and wines. Same allergen concerns as other sulfites — can trigger asthma attacks; must be declared on labels.',
    'e222': 'E222 / INS 222 — Sodium Bisulfite (Sodium Hydrogen Sulfite). A sulfite preservative used in winemaking, food processing and brewing. Asthma and allergy risk; mandatory label declaration for sulfite content.',
    'e224': 'E224 / INS 224 — Potassium Metabisulfite. A sulfite preservative used in winemaking, brewing and food processing. Same asthma and allergy risks as other sulfites; mandatory declaration.',
    'e225': 'E225 / INS 225 — Potassium Sulfite. A sulfite preservative with the same allergen/asthma profile as other sulfites. Mandatory declaration required.',
    'e234': 'E234 / INS 234 — Nisin. A natural antimicrobial peptide produced by the bacterium Lactococcus lactis during fermentation. Used to prevent growth of pathogenic bacteria (especially Listeria and Clostridium) in processed cheese, dairy products and canned goods. Considered safe.',
    'e235': 'E235 / INS 235 — Natamycin (Pimaricin). A natural antifungal agent produced by Streptomyces natalensis bacteria. Used as a surface treatment on hard cheeses, sausage casings and dried meats to prevent mould growth. Not absorbed through the gut. Safe.',
    'e280': 'E280 / INS 280 — Propionic Acid. A naturally occurring short-chain fatty acid produced during fermentation and digestion. Used as an antifungal preservative in bread, baked goods and dairy products to prevent mould growth. Safe.',
    'e281': 'E281 / INS 281 — Sodium Propionate. The sodium salt of propionic acid, used as an antifungal preservative primarily in bread and baked goods. Generally safe; some links to migraine in sensitive individuals.',
    'e282': 'E282 / INS 282 — Calcium Propionate. The calcium salt of propionic acid — the most widely used bread preservative in commercial baking. Inhibits mould and rope bacteria in bread. Provides small amount of dietary calcium. Generally safe; occasional migraine reports.',
    'e283': 'E283 / INS 283 — Potassium Propionate. The potassium salt of propionic acid used as a preservative in baked goods. Same function and safety profile as calcium propionate.',
    'e290': 'E290 / INS 290 — Carbon Dioxide. The natural gas used in carbonated beverages, beer, wine and modified atmosphere packaging to prevent oxidation and microbial growth. Safe.',

    # --- Thickeners / Stabilisers / Hydrocolloids ---
    'e400': 'E400 / INS 400 — Alginic Acid. A natural polysaccharide extracted from brown seaweed. Used as a thickener and gelling agent in ice cream, salad dressings and pharmaceuticals. Safe.',
    'e401': 'E401 / INS 401 — Sodium Alginate. The sodium salt of alginic acid, widely used as a thickener and gel-former in ice cream, sauces, bakery and restructured foods. Safe.',
    'e402': 'E402 / INS 402 — Potassium Alginate. Potassium salt of alginic acid, similar uses to sodium alginate. Safe.',
    'e404': 'E404 / INS 404 — Calcium Alginate. Calcium salt of alginic acid — forms firmer gels. Used in restructured fish and meat products and controlled-release pharmaceuticals. Safe.',
    'e406': 'E406 / INS 406 — Agar (Agar-agar). A natural gelling agent derived from red algae (primarily Gelidium species), used for centuries in Asian cuisine. Sets at lower concentrations than gelatin. Widely used in desserts, confectionery and as a vegetarian gelatin substitute. Safe.',
    'e410': 'E410 / INS 410 — Locust Bean Gum (Carob Gum). A natural thickener from the seeds of the carob tree. Used in ice cream, cheese, salad dressings and infant formula to improve texture and prevent ice crystal formation. Safe.',
    'e412': 'E412 / INS 412 — Guar Gum. A natural thickener and emulsifier ground from guar bean seeds, primarily grown in India and Pakistan. Widely used in ice cream, dairy products, sauces and gluten-free baked goods. One of the most widely used food hydrocolloids globally. Safe.',
    'e414': 'E414 / INS 414 — Acacia Gum (Gum Arabic). A natural gum from acacia trees, used as a thickener, stabiliser and encapsulant in confectionery, beverages, flavour emulsions and pharmaceutical coating. One of the oldest food additives, used for over 4,000 years. Also a prebiotic fibre. Safe.',
    'e440': 'E440 / INS 440 — Pectins. Natural gelling agents from citrus peel, apple pomace and sugar beet. Used to make jams, jellies and marmalades set; also used in confectionery, dairy and beverages. A source of soluble dietary fibre. Safe and beneficial.',
    'e440i': 'E440(i) / INS 440(i) — Pectin (amidated). Amidated pectin forms gels that are more tolerant to calcium levels and temperature. Used in jams, dairy products and low-sugar preserves. Safe.',
    'e460': 'E460 / INS 460 — Cellulose. The most abundant natural polymer — the structural component of plant cell walls. Used as a filler, anti-caking agent and dietary fibre in processed foods and pharmaceuticals. Not digestible; provides bulk. Safe.',
    'e460i': 'E460(i) / INS 460(i) — Microcrystalline Cellulose (MCC/Avicel). Refined cellulose used as an anti-caking agent, bulking agent, fat replacer and texturiser in processed foods and supplements. Safe.',
    'e461': 'E461 / INS 461 — Methyl Cellulose. A cellulose derivative used as a thickener, stabiliser and fat replacer in foods. Unique property: forms a gel when heated and dissolves when cooled (opposite of gelatin). Used in vegetarian burgers. Safe.',
    'e462': 'E462 / INS 462 — Ethyl Cellulose. A cellulose ether used as a film former and binder in pharmaceutical tablet coating and as an edible packaging material. Safe.',
    'e463': 'E463 / INS 463 — Hydroxypropyl Cellulose (HPC). A cellulose derivative used as a thickener, binder and film former in food products and pharmaceuticals. Safe.',
    'e464': 'E464 / INS 464 — Hydroxypropyl Methyl Cellulose (HPMC). A cellulose derivative used as a thickener, emulsifier and film former in gluten-free bread, sauces and pharmaceuticals. Safe.',
    'e466': 'E466 / INS 466 — Sodium Carboxymethyl Cellulose (CMC / Cellulose Gum). A cellulose derivative used as a thickener, stabiliser and water-retention agent in ice cream, baked goods and beverages. Also used in pharmaceutical tablets and personal care products. Some animal studies at very high doses showed effects; at food-use levels it is safe.',

    # --- Anti-caking Agents ---
    'e530': 'E530 / INS 530 — Magnesium Oxide. Used as an anti-caking agent in cocoa powder and as a dietary magnesium supplement. Safe.',
    'e551': 'E551 / INS 551 — Silicon Dioxide (Silica). An inorganic anti-caking agent used to prevent powdered foods (spices, instant soups, protein powders) from clumping. Not absorbed by the body. Safe. Note: nanoparticle forms are under review by regulators.',
    'e552': 'E552 / INS 552 — Calcium Silicate. An inorganic anti-caking agent used in baking powder, table salt and powdered mixes. Safe.',
    'e553a': 'E553a / INS 553(i) and 553(ii) — Magnesium Silicates. Anti-caking agents used in spices, baking powder and powdered foods. Safe.',
    'e553b': 'E553b / INS 553b — Talc (Magnesium Silicate). A naturally occurring mineral used as an anti-caking agent and coating for confectionery (e.g., rice-paper coating on sweets). Concerns exist about asbestos contamination of some talc deposits; some regulatory bodies restrict its food use. Distinct from cosmetic talc used in powders.',
    'e554': 'E554 / INS 554 — Sodium Aluminosilicate (Zeolite). An anti-caking agent used in salt, powdered foods and spices. Contains aluminium; generally considered safe at food-use levels, but populations with kidney disease should limit aluminium exposure.',
    'e559': 'E559 / INS 559 — Aluminium Silicate (Kaolin). An anti-caking agent used in some food products. Contains aluminium. Assess as with other aluminium-containing additives.',

    # --- Flavour Enhancers (additional) ---
    'e620': 'E620 / INS 620 — Glutamic Acid. The amino acid form of MSG, found naturally in tomatoes, parmesan, mushrooms and soy sauce. Produced by fermentation. Used as a flavour enhancer to intensify umami taste. Safe.',
    'e622': 'E622 / INS 622 — Monopotassium Glutamate. The potassium salt of glutamic acid, used as a flavour enhancer similarly to MSG (E621). Generally safe.',
    'e623': 'E623 / INS 623 — Calcium Glutamate. The calcium salt of glutamic acid, used as a flavour enhancer. Generally safe.',
    'e624': 'E624 / INS 624 — Monoammonium Glutamate. The ammonium salt of glutamic acid, used as a flavour enhancer. Generally safe.',
    'e625': 'E625 / INS 625 — Magnesium Glutamate. The magnesium salt of glutamic acid, used as a flavour enhancer. Provides dietary magnesium alongside flavour-enhancing action. Safe.',
    'e626': 'E626 / INS 626 — Guanylic Acid. A ribonucleotide flavour enhancer found naturally in mushrooms, meat and fish. Used to amplify umami taste. Generally safe.',
    'e628': 'E628 / INS 628 — Dipotassium Guanylate. Potassium salt of guanylic acid, used as a flavour enhancer in chips and savoury snacks. Safe.',
    'e629': 'E629 / INS 629 — Calcium Guanylate. Calcium salt of guanylic acid, used as a flavour enhancer. Safe.',
    'e630': 'E630 / INS 630 — Inosinic Acid. A ribonucleotide found naturally in meat and fish, used as a flavour enhancer to boost umami taste. Usually used with MSG and guanylates. Safe.',
    'e632': 'E632 / INS 632 — Dipotassium Inosinate. Potassium salt of inosinic acid, used as a flavour enhancer. Often combined with MSG and disodium guanylate. Safe.',
    'e633': 'E633 / INS 633 — Calcium Inosinate. Calcium salt of inosinic acid, used as a flavour enhancer in processed foods. Safe.',
    'e635': 'E635 / INS 635 — Disodium 5\'\'-Ribonucleotides. A blend of disodium inosinate (E631) and disodium guanylate (E627) in an optimised ratio for maximum umami enhancement. Used in chips, instant noodles and savoury snacks. Safe at permitted levels. Not suitable for gout sufferers (high purine content).',

    # --- Modified Starches (additional E-numbers) ---
    'e1410': 'E1410 / INS 1410 — Monostarch Phosphate. A modified starch with a small degree of phosphate cross-linking. Used as a thickener with improved acid and heat stability in sauces, soups and ready meals. Safe.',
    'e1420': 'E1420 / INS 1420 — Acetylated Starch. Starch modified by reaction with acetic anhydride to reduce retrogradation (staling). Used in sauces, dressings and dairy products. Safe.',
    'e1422': 'E1422 / INS 1422 — Acetylated Distarch Adipate. A more extensively modified starch with excellent freeze-thaw stability. Used in frozen sauces, soups and ready meals. Safe.',
    'e1440': 'E1440 / INS 1440 — Hydroxypropyl Starch. Starch modified with propylene oxide for improved freeze-thaw stability. Used in frozen foods and dairy products. Safe.',
    'e1442': 'E1442 / INS 1442 — Hydroxypropyl Distarch Phosphate. Combines cross-linking (phosphate) and substitution (hydroxypropyl) for maximum stability under heat, acid and freezing. Used in sauces, soups and canned foods. Safe.',
    'e1201': 'E1201 / INS 1201 — Polyvinylpyrrolidone (PVP / Povidone). A synthetic polymer used as a clarifying agent in beer and wine, and as a binder in pharmaceutical tablets. Safe at food-use levels.',

}


# Ingredients that are commonly_questioned in food but only worth_knowing in topical/cosmetic products
COSMETIC_WORTH_OVERRIDES = {
    'sodium benzoate': (
        'Preservative E211',
        'If combined with Vitamin C (ascorbic acid) or citric acid, it can potentially produce benzene, a known carcinogen, although this is more common in beverages than in topical products. While generally safe within approved limits (0.5% in cosmetics), higher concentrations are more likely to cause irritant reactions.'
    ),
    'e211': (
        'Sodium benzoate (E211)',
        'Benzene formation risk is specific to acidic beverages with Vitamin C — not a topical concern. Approved in cosmetics at ≤0.5%; may cause skin irritation at higher concentrations.'
    ),
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


def _normalize_ins(name: str) -> str:
    """
    Normalize additive number formats to a lowercase 'eNNN[sub]' key:
      'INS 322'       → 'e322'
      'INS322(i)'     → 'e322i'
      '322(i)'        → 'e322i'
      '500(ii)'       → 'e500ii'
      '503 ii'        → 'e503ii'
      '471'           → 'e471'
      'E471'          → 'e471'
      'E 500(ii)'     → 'e500ii'
    """
    import re
    s = name.strip()
    # Pattern: optional 'INS' or 'E' prefix + optional space, then digits,
    # then optional sub-type: (i), (ii), (iii), (iv), (v) or bare i/ii/iii/iv
    m = re.match(
        r'^(?:ins[\s\-]?|e[\s]?)?(\d+)\s*[\(\s\-]*(i{1,3}v?|iv|v)\s*\)?\s*$',
        s, re.IGNORECASE
    )
    if m:
        return 'e' + m.group(1) + m.group(2).lower()
    # Just a number (bare, or with INS/E prefix, no sub-type)
    m2 = re.match(r'^(?:ins[\s\-]?|e[\s]?)?(\d+)', s, re.IGNORECASE)
    if m2:
        return 'e' + m2.group(1)
    # Old behaviour: 'INS 200' → 'e200'
    m3 = re.match(r'^ins[\s\-]*(\d+)', s, re.IGNORECASE)
    if m3:
        return 'e' + m3.group(1)
    return s.lower()



def classify_ingredient(ingredient_name, category=None):
    """Classify ingredients based on regulatory and health concerns - SINGLE SOURCE OF TRUTH"""
    import re as _re
    # Normalize INS numbers first: "INS 200" / "471" / "500(ii)" → "e200" / "e471" / "e500ii"
    ingredient_name = _normalize_ins(ingredient_name)
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

        # Sunscreen UV filters with endocrine/environmental concerns
        'oxybenzone': ('Chemical UV filter (Benzophenone-3)', 'Penetrates skin and detected in blood, urine and breast milk; endocrine disruption concerns; Hawaii, Palau and US Virgin Islands banned it to protect coral reefs; EU restricts to 6% in face/body, 0.5% in children\'s products'),
        'benzophenone-3': ('Chemical UV filter (Oxybenzone)', 'Same compound as oxybenzone; endocrine disruptor; coral bleaching agent; restricted in EU; banned in several reef-protection jurisdictions'),

        # Propyl gallate / E310 — under regulatory review, potential carcinogen
        'propyl gallate': ('Synthetic antioxidant E310', 'Associated with tumour promotion in some animal studies; banned in baby foods in EU; EU restricts to 0.1% in fat-containing foods; EFSA review ongoing; avoid in products for infants'),
        'e310': ('Propyl gallate (E310)', 'Potential carcinogen in animal studies at high doses; banned in baby foods in EU; under EFSA review; restricted in several food categories'),

        # Cyclamate E952 — banned in USA, UK
        'cyclamate': ('Artificial sweetener E952', 'Banned in the USA (1969) and UK — bladder cancer in rat studies; hydrolysed to cyclohexylamine which is toxic at high doses; JECFA reviewed and maintained ADI in some jurisdictions but US ban stands'),
        'e952': ('Cyclamate (E952)', 'Banned in USA (since 1969) and UK — bladder cancer in animal studies; still permitted in India and EU at specified limits but under ongoing review'),
        'sodium cyclamate': ('Artificial sweetener (cyclamate sodium salt)', 'Banned in USA and UK; approved in EU and India; bladder cancer in rat studies; converts to toxic cyclohexylamine'),

        # Cocamide DEA/MEA — California Prop 65 carcinogen
        'cocamide dea': ('Surfactant/foam booster', 'California Prop 65 listed as carcinogen; forms nitrosamines (IARC Group 2A carcinogens) with other ingredients; EU restricts concentration; NICNAS identified concerns in Australian market'),
        'cocamide mea': ('Surfactant/foam booster', 'May form nitrosamines (potential carcinogens); Prop 65 listed in California; should be avoided in products also containing nitrosating agents'),

        # Potassium iodate — banned in EU, concerns about iodine toxicity
        'potassium iodate': ('Bread improver / oxidising agent', 'Banned in EU, Canada, Australia and most developed markets; not fully reduced to iodide during baking; excess iodine causes thyroid dysfunction; India permits it but under review'),

        # Amaranth dye — banned in USA since 1976
        'amaranth dye': ('Synthetic red azo dye E123/INS 123', 'Banned in the USA since 1976 due to carcinogenicity concerns in animal studies; EU permits only in caviar; not widely used in India; avoid where possible'),
        'e123': ('Amaranth (E123)', 'Banned in USA since 1976; EU restricts to caviar only; not the same as the grain amaranth; azo dye with historical carcinogenicity concerns'),

        # TBHQ — petroleum-derived, controversial antioxidant
        'tbhq': ('Antioxidant E319/INS 319', 'Petroleum-derived synthetic antioxidant; high doses are toxic; some animal studies show immune effects; banned in Japan; FSSAI and EU permit at ≤200mg/kg in oils — India allows in edible oils and instant noodles'),
        'tertiary butylhydroquinone': ('Antioxidant E319/INS 319', 'Petroleum-derived; toxic at high doses; animal studies link very high intakes to immune effects; banned in Japan; FDA permits up to 0.02% of fat content in the USA'),
        'e319': ('TBHQ (E319)', 'Petroleum-derived antioxidant in cooking oils and instant noodles; banned in Japan; FSSAI-permitted at specified limits; controversial — some animal research on immune effects at high doses'),


        # E-number aliases for existing commonly_questioned ingredients
        'e142': ('Synthetic green dye E142 (Green S)', 'Banned in USA, Canada, Japan, Australia — hyperactivity concerns and lack of comprehensive safety data'),
        'e150c': ('Ammonia Caramel (E150c / Caramel III)', '4-MEI by-product is IARC Group 2B possible carcinogen; California Prop 65 cancer warning required; used in beer and soy sauce'),
        'e150d': ('Sulfite Ammonia Caramel (E150d / Caramel IV)', '4-MEI by-product is IARC Group 2B possible carcinogen; used in colas — Coca-Cola reformulated in some markets; California Prop 65 warning required'),
        'e151': ('Brilliant Black BN (E151)', 'Banned in USA, Canada, Japan, Australia; hyperactivity warning required in EU; azo dye with cancer and hyperactivity concerns'),
        'e218': ('Methylparaben as E218', 'Same as methylparaben — estrogen mimic, accumulates in breast tissue, endocrine disruptor; EU restricts concentration'),
        'e219': ('Sodium Methylparaben (E219)', 'Sodium salt of methylparaben; same hormone disruption concerns; EU restricts concentration'),
        'e471': ('Mono- and Diglycerides of Fatty Acids (E471)', 'May contain residual trans-fatty acids; glycidol fatty acid esters (probable carcinogen IARC Group 2A) found as contaminant; EFSA reviewed and set limits; widely used in bread and margarine'),

        # Potassium nitrite — curing salt, forms nitrosamines
        'potassium nitrite': ('Curing agent E249/INS 249', 'Curing salt in processed meats; can form N-nitrosamines (IARC Group 2A probable carcinogens) when heated to high temperatures, especially in combination with amines in meat; FSSAI and EU set strict maximum levels'),
        'e249': ('Potassium nitrite (E249)', 'Curing agent in processed meats; same nitrosamine formation risk as sodium nitrite (E250); FSSAI, EU and Codex permit at strict limits; avoid heavily cured meats in diet'),
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
        # e954 / saccharin → moved to commonly_questioned

        # Raising agents — safe but worth knowing what they are
        'e500': ('Sodium Carbonates (E500)', 'Safe leavening and pH agents; high sodium intake concern if excessive'),
        'e500i': ('Sodium Carbonate (E500i)', 'Safe leavening agent; standard baking ingredient'),
        'e500ii': ('Sodium Bicarbonate / Baking Soda (E500ii)', 'Widely used, safe leavening agent; standard baking soda'),
        'e500iii': ('Sodium Sesquicarbonate (E500iii)', 'Safe leavening and pH agent'),
        'e501': ('Potassium Carbonates (E501)', 'Safe leavening agents'),
        'e501i': ('Potassium Carbonate (E501i)', 'Safe leavening agent'),
        'e501ii': ('Potassium Bicarbonate (E501ii)', 'Safe sodium-free leavening agent'),
        'e503': ('Ammonium Carbonates (E503)', 'Safe leavening agent; fully decomposes during baking — no ammonia in finished product'),
        'e503i': ('Ammonium Carbonate (E503i)', 'Traditional baking leavening agent; fully decomposes on heating'),
        'e503ii': ('Ammonium Bicarbonate (E503ii)', 'Safe leavening agent in dry baked goods; fully decomposes during baking'),
        'e504': ('Magnesium Carbonates (E504)', 'Safe anti-caking and leavening agent; provides dietary magnesium'),
        'e504i': ('Magnesium Carbonate (E504i)', 'Safe anti-caking and leavening agent'),
        'e504ii': ('Magnesium Hydroxide Carbonate (E504ii)', 'Safe anti-caking and leavening agent'),
        'e450': ('Diphosphates (E450)', 'Baking powder component; excessive phosphate intake may affect kidney health and bone metabolism'),
        'e450i': ('Disodium Diphosphate/SAPP (E450i)', 'Leavening acid in baking powder; excess phosphate concern for kidney health'),
        'e451': ('Triphosphates (E451)', 'Used in processed cheese and meats; excess phosphate concern for kidney health'),
        'e451i': ('Pentasodium Triphosphate/STPP (E451i)', 'Emulsifying salt in processed cheese; excess phosphate concern'),
        'e452': ('Polyphosphates (E452)', 'Emulsifying salt in processed cheese; excess phosphate concern for kidney health'),
        # Emulsifiers
        'e322': ('Lecithin (E322)', 'Natural emulsifier; generally safe but soy allergen if soy-derived; sunflower lecithin is allergen-free'),
        'e322i': ('Lecithin (E322i)', 'Natural emulsifier; soy allergen if soy-derived'),
        'e322ii': ('Hydroxylated Lecithin (E322ii)', 'Modified lecithin; soy allergen if soy-derived'),
        'e472e': ('DATEM (E472e)', 'Synthetic emulsifier derived from mono/diglycerides and tartaric acid; widely used in bread; generally safe but processed ingredient'),
        'e472a': ('ACETEM (E472a)', 'Acetic acid ester of mono/diglycerides; synthetic emulsifier; generally safe in bread and baked goods'),
        'e472b': ('LACTEM (E472b)', 'Lactic acid ester of mono/diglycerides; synthetic emulsifier; generally safe'),
        'e472c': ('CITREM (E472c)', 'Citric acid ester of mono/diglycerides; synthetic emulsifier; generally safe'),
        'e473': ('Sucrose Esters (E473)', 'Synthetic emulsifier from sucrose and fatty acids; generally safe'),
        'e475': ('Polyglycerol Esters (E475)', 'Synthetic emulsifier; generally safe'),
        'e476': ('PGPR (E476)', 'Synthetic emulsifier from castor oil; may cause digestive upset at high doses; animal studies at very high doses showed liver effects'),
        'e481': ('Sodium Stearoyl Lactylate/SSL (E481)', 'Synthetic dough emulsifier; generally safe; improves bread quality'),
        'e482': ('Calcium Stearoyl Lactylate/CSL (E482)', 'Synthetic emulsifier; generally safe in bread and dairy'),
        'e491': ('Sorbitan Monostearate (E491)', 'Synthetic emulsifier; generally safe in confectionery and baked goods'),
        'e442': ('Ammonium Phosphatides (E442)', 'Chocolate emulsifier; synthetic; limited safety data; generally considered safe'),
        # Sweeteners (moderate concern)
        'e420': ('Sorbitol / Sugar alcohol (E420)', 'May cause digestive discomfort, bloating and diarrhoea at doses above 50g; laxative effect'),
        'e420i': ('Sorbitol (E420i)', 'Sugar alcohol — laxative effect at high intake; generally safe in moderate amounts'),
        'e421': ('Mannitol / Sugar alcohol (E421)', 'Poorly absorbed; laxative and gas-forming at high doses; generally safe in small amounts'),
        'e953': ('Isomalt / Sugar alcohol (E953)', 'May cause digestive discomfort at high intake; low glycaemic index'),
        'e965': ('Maltitol / Sugar alcohol (E965)', 'Digestive discomfort and laxative effect at high doses; raises blood sugar more than other sugar alcohols'),
        'e966': ('Lactitol / Sugar alcohol (E966)', 'Laxative effect at high doses; contains lactose backbone — relevant for lactose-intolerant people'),
        'e967': ('Xylitol / Sugar alcohol (E967)', 'Digestive discomfort at high doses; safe for teeth; toxic to dogs — keep out of pet reach'),
        'e961': ('Neotame (E961)', 'High-intensity synthetic sweetener; generally safe; metabolised differently from aspartame'),
        'e962': ('Aspartame-Acesulfame Salt (E962)', 'Contains phenylalanine — PKU warning required; same aspartame concerns apply'),
        'e960': ('Steviol Glycosides / Stevia (E960)', 'Natural zero-calorie sweetener; generally safe; very high doses may affect blood pressure or interact with diabetes medication'),
        'e960a': ('Steviol Glycosides from Stevia (E960a)', 'Natural sweetener from stevia; generally safe at normal use levels'),
        # Caramel colours (safer variants)
        'e150a': ('Plain Caramel / Caramel I (E150a)', 'Safest class of caramel colour; no ammonia or sulfite process; generally safe'),
        'e150b': ('Caustic Sulfite Caramel / Caramel II (E150b)', 'Contains sulfite process by-products; generally safe at food levels; sulfite allergen note'),
        # Preservatives (moderate)
        'e200': ('Sorbic Acid (E200)', 'Generally safe preservative; may cause contact sensitisation in some individuals'),
        'e201': ('Sodium Sorbate (E201)', 'Generally safe preservative; may cause mild allergic reactions in sensitive people'),
        'e203': ('Calcium Sorbate (E203)', 'Generally safe preservative; similar profile to potassium sorbate'),
        'e210': ('Benzoic Acid (E210)', 'Forms benzene with Vitamin C in acidic beverages; hyperactivity links in children; mandatory EU label declaration'),
        'e212': ('Potassium Benzoate (E212)', 'Same benzene-formation and hyperactivity concerns as sodium benzoate (E211)'),
        'e213': ('Calcium Benzoate (E213)', 'Similar concerns to sodium benzoate (E211); benzene formation with Vitamin C'),
        'e221': ('Sodium Sulfite (E221)', 'Sulfite allergen — can trigger asthma attacks; mandatory label declaration'),
        'e222': ('Sodium Bisulfite (E222)', 'Sulfite allergen — asthma trigger; mandatory declaration'),
        'e224': ('Potassium Metabisulfite (E224)', 'Sulfite allergen — asthma trigger; mandatory declaration'),
        'e225': ('Potassium Sulfite (E225)', 'Sulfite allergen — asthma trigger; mandatory declaration'),
        'e280': ('Propionic Acid (E280)', 'Antifungal preservative; safe at food use levels; some migraine sensitivity reports'),
        'e281': ('Sodium Propionate (E281)', 'Bread preservative; generally safe; occasional migraine sensitivity'),
        'e282': ('Calcium Propionate (E282)', 'Most widely used bread preservative; generally safe; occasional migraine sensitivity reported'),
        'e283': ('Potassium Propionate (E283)', 'Bread preservative; generally safe; occasional migraine sensitivity'),
        # Phosphate additives
        'e339': ('Sodium Phosphates (E339)', 'Excess phosphate intake may affect kidney function and bone metabolism; generally safe at food levels'),
        'e340': ('Potassium Phosphates (E340)', 'Excess phosphate concern for kidney health at high intake'),
        'e341': ('Calcium Phosphates (E341)', 'Safe at food levels; provides calcium; generally recognised as safe'),
        'e341i': ('Monocalcium Phosphate/MCP (E341i)', 'Common baking powder ingredient; generally safe'),
        'e341ii': ('Dicalcium Phosphate/DCP (E341ii)', 'Safe leavening and supplement ingredient'),
        'e341iii': ('Tricalcium Phosphate/TCP (E341iii)', 'Safe anti-caking agent and calcium supplement'),
        # Silicates — aluminium content
        'e554': ('Sodium Aluminosilicate (E554)', 'Contains aluminium; generally safe at food levels; caution for kidney disease patients'),
        'e559': ('Kaolin / Aluminium Silicate (E559)', 'Contains aluminium; generally safe at food levels; concern for kidney patients'),
        # Colours with mild concerns
        'e120': ('Cochineal / Carmine (E120)', 'Animal-derived (insect); can cause severe allergic reactions including anaphylaxis; not vegan; must be labelled explicitly'),
        'e142': ('Green S (E142)', 'Banned in USA, Canada, Japan and Australia; approved in EU and India with restrictions; hyperactivity concern'),
        'e160b': ('Annatto (E160b)', 'Natural colour from annatto seeds; generally safe; occasional allergic reactions reported'),
        # Flavour enhancers (additional)
        'e620': ('Glutamic Acid (E620)', 'Natural amino acid; some sensitivity similar to MSG reported; generally safe'),
        'e622': ('Monopotassium Glutamate (E622)', 'Similar to MSG; generally safe for most people'),
        'e623': ('Calcium Glutamate (E623)', 'Similar to MSG; generally safe'),
        'e624': ('Monoammonium Glutamate (E624)', 'Similar to MSG; generally safe'),
        'e625': ('Magnesium Glutamate (E625)', 'Similar to MSG; also provides magnesium; generally safe'),
        'e626': ('Guanylic Acid (E626)', 'Natural flavour enhancer; gout sufferers should limit purine-rich foods including guanylates'),
        'e628': ('Dipotassium Guanylate (E628)', 'Flavour enhancer; high purine content — concern for gout sufferers'),
        'e629': ('Calcium Guanylate (E629)', 'Flavour enhancer; high purine content — concern for gout sufferers'),
        'e630': ('Inosinic Acid (E630)', 'Flavour enhancer found in meat and fish; high purine content — concern for gout sufferers'),
        'e632': ('Dipotassium Inosinate (E632)', 'Flavour enhancer; high purine — concern for gout sufferers'),
        'e633': ('Calcium Inosinate (E633)', 'Flavour enhancer; high purine — concern for gout sufferers'),
        'e635': ('Disodium Ribonucleotides (E635)', 'Blend of E631+E627; strong flavour enhancer; high purine — avoid if prone to gout'),
        # Cellulose derivatives
        'e466': ('Sodium CMC / Cellulose Gum (E466)', 'Synthetic cellulose thickener; animal studies at very high doses showed gut effects; safe at normal food levels'),
        # Polysorbates / modified
        'e533': ('Magnesium Silicate (E553a)', 'Anti-caking agent; safe at food levels'),
        'e553b': ('Talc (E553b)', 'Anti-caking agent; concerns about asbestos contamination of some talc deposits; FDA and EU regulate its use'),
        # Colours (safe variants)
        'e150': ('Caramel Colour (E150)', 'Most widely used food colour; Classes III and IV contain 4-MEI (possible carcinogen); California Prop 65 warning required for Caramel IV'),
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

        # Generic colour labels — brand has not named the specific dye(s)
        'colours': ('Undisclosed colorant(s)', 'Generic label — brand has not named the specific dye(s) used; individual colorants may include synthetic azo dyes, coal tar dyes or natural pigments; safety cannot be assessed without disclosure'),
        'colors': ('Undisclosed colorant(s)', 'Generic label — brand has not named the specific dye(s) used; individual colorants may include synthetic azo dyes, coal tar dyes or natural pigments; safety cannot be assessed without disclosure'),
        'colour': ('Undisclosed colorant', 'Generic label — exact colorant not disclosed; may include synthetic azo dyes or natural pigments'),
        'color': ('Undisclosed colorant', 'Generic label — exact colorant not disclosed; may include synthetic azo dyes or natural pigments'),

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

        # ── INS / E Numbered Food Additives ─────────────────────────────────────
        # Preservatives (sorbates, benzoates, propionates) — FSSAI approved, mild concerns
        'sorbic acid': ('Preservative E200/INS 200', 'FSSAI, EU and CODEX approved; generally safe; rare allergic reactions in sensitive individuals at high levels'),
        'e200': ('Sorbic acid (E200)', 'FSSAI, EU and CODEX approved mould inhibitor; generally safe; rare contact allergy reactions reported'),
        'sodium sorbate': ('Preservative E201', 'CODEX approved preservative; same general profile as potassium sorbate; safe at specified limits'),
        'e201': ('Sodium sorbate (E201)', 'CODEX approved preservative; generally well tolerated; similar profile to potassium sorbate E202'),
        'benzoic acid': ('Preservative E210/INS 210', 'FSSAI, EU and CODEX approved; naturally occurs in some fruits; forms trace benzene with Vitamin C in acidic beverages at elevated temperatures — a concern noted by WHO'),
        'e210': ('Benzoic acid (E210)', 'FSSAI approved preservative; benzene formation risk with Vitamin C in acidic drinks; safe at approved limits in food products'),
        'calcium benzoate': ('Preservative E213/INS 213', 'Calcium salt of benzoic acid; same benzene formation concern with Vitamin C as sodium benzoate; approved by CODEX at specified limits'),
        'e213': ('Calcium benzoate (E213)', 'CODEX approved preservative; trace benzene formation risk with ascorbic acid in acidic beverages'),
        'propionic acid': ('Preservative E280/INS 280', 'Naturally occurring acid in Swiss cheese; FSSAI, EU and CODEX approved bread mould inhibitor; safe at specified limits; rare migraines reported in sensitive individuals'),
        'e280': ('Propionic acid (E280)', 'Natural bread preservative from fermentation; approved by FSSAI, EU and CODEX; well tolerated'),
        'sodium propionate': ('Preservative E281/INS 281', 'FSSAI, EU and CODEX approved bread mould inhibitor; generally safe; rare migraines reported'),
        'e281': ('Sodium propionate (E281)', 'Approved preservative in bread and baked goods by FSSAI, EU and CODEX; generally safe at specified limits'),
        'calcium propionate': ('Preservative E282/INS 282', 'FSSAI, EU, FDA and CODEX approved bread preservative; provides calcium; generally safe — some studies note behaviour effects in children at very high intakes'),
        'e282': ('Calcium propionate (E282)', 'Widely used bread preservative; FSSAI, EU and FDA approved; safe at specified limits; possible migraines in sensitive individuals'),

        # Antioxidants
        'sodium ascorbate': ('Antioxidant E301', 'Sodium salt of Vitamin C; FSSAI, EU and CODEX approved; generally safe; watch sodium intake if on restricted diet'),
        'e301': ('Sodium ascorbate (E301)', 'Vitamin C antioxidant; FSSAI and CODEX approved; safe; adds a small amount of sodium'),
        'calcium ascorbate': ('Antioxidant E302', 'Non-acidic Vitamin C form; FSSAI and CODEX approved; beneficial as calcium supplement; safe'),
        'e302': ('Calcium ascorbate (E302)', 'Buffered Vitamin C; FSSAI and CODEX approved; antioxidant and calcium supplement; safe'),
        'ascorbyl palmitate': ('Fat-soluble antioxidant E304', 'FSSAI, EU and CODEX approved antioxidant; used in fatty foods to prevent rancidity; safe'),
        'e304': ('Ascorbyl palmitate (E304)', 'Fat-soluble Vitamin C ester antioxidant; FSSAI, EU and CODEX approved; safe at permitted levels'),

        # Thickeners and gelling agents
        'e401': ('Sodium alginate (E401)', 'Natural seaweed-derived thickener; FSSAI, EU and CODEX approved; generally safe; may interact with some mineral supplements'),
        'e402': ('Potassium alginate (E402)', 'Natural seaweed-derived thickener; CODEX and EU approved; generally safe'),
        'potassium alginate': ('Thickener E402/INS 402', 'Natural seaweed-derived gum; EU and CODEX approved; generally safe'),
        'e404': ('Calcium alginate (E404)', 'Natural seaweed-derived gelling agent; CODEX and EU approved; generally safe'),
        'calcium alginate': ('Thickener E404/INS 404', 'Natural seaweed-derived gelling agent; CODEX and EU approved; generally safe'),
        'agar': ('Gelling agent E406/INS 406', 'Natural red algae-derived vegetarian gelatine substitute; FSSAI, EU and CODEX approved; generally safe; may cause mild digestive discomfort in large amounts'),
        'e406': ('Agar (E406)', 'Natural seaweed-derived gelling agent; FSSAI, EU and CODEX approved; safe; mild laxative at large doses'),
        'locust bean gum': ('Thickener E410/INS 410', 'Natural carob seed gum; FSSAI, EU and CODEX approved; generally safe; high doses may cause flatulence'),
        'carob bean gum': ('Thickener E410/INS 410', 'Natural carob seed gum; EU and CODEX approved; generally safe'),
        'e410': ('Locust bean gum (E410)', 'Natural seed gum; FSSAI, EU and CODEX approved; generally safe; mild digestive effects at high doses'),
        'gum arabic': ('Emulsifier/thickener E414/INS 414', 'Natural acacia gum; FSSAI, EU and CODEX approved prebiotic fibre; generally safe; may cause bloating in sensitive individuals'),
        'acacia': ('Gum arabic (E414/INS 414)', 'Natural acacia gum; prebiotic fibre; FSSAI, EU and CODEX approved; generally safe'),
        'e414': ('Gum arabic (E414)', 'Natural acacia gum; FSSAI, EU and CODEX approved; prebiotic fibre with gut health benefits; may cause mild bloating'),
        'gellan gum': ('Thickener E418/INS 418', 'Fermentation-derived gelling agent; FSSAI, EU and FDA approved; generally safe; no significant adverse effects at food-use concentrations'),
        'e418': ('Gellan gum (E418)', 'Fermentation-derived gelling agent; FSSAI, EU and FDA approved; generally safe'),
        'pectin': ('Gelling agent E440/INS 440', 'Natural fruit-derived soluble fibre; FSSAI, EU and CODEX approved; excellent safety profile; minor digestive effects at very high doses'),
        'e440': ('Pectin (E440)', 'Natural fruit-derived gelling agent; FSSAI, EU and CODEX approved; safe dietary fibre with no known concerns'),
        'microcrystalline cellulose': ('Texturiser E460/INS 460', 'Refined plant cellulose; FSSAI, EU and CODEX approved; indigestible; safe as a bulking agent'),
        'e460': ('Microcrystalline cellulose (E460)', 'Refined cellulose; FSSAI, EU and CODEX approved; safe indigestible bulking agent'),
        'methyl cellulose': ('Thickener E461/INS 461', 'Modified plant cellulose; EU and CODEX approved; indigestible; may cause gas and bloating at high doses'),
        'e461': ('Methyl cellulose (E461)', 'Modified plant cellulose; EU and CODEX approved thickener; may cause gas and bloating at high doses'),
        'hydroxypropyl methylcellulose': ('Thickener E464/INS 464', 'Modified cellulose; EU and CODEX approved; safe; used as vegetarian capsule material'),
        'e464': ('HPMC (E464)', 'Modified cellulose; EU and CODEX approved; safe as thickener and capsule material'),
        'cmc': ('Thickener E466/INS 466', 'Cellulose-derived thickener; FSSAI, EU and CODEX approved; generally safe; some studies suggest disruption of gut microbiome at high doses'),
        'carboxymethyl cellulose': ('Thickener E466/INS 466', 'Cellulose-derived thickener; FSSAI, EU and CODEX approved; some mouse studies link high doses to gut microbiome disruption and low-grade intestinal inflammation'),
        'sodium carboxymethyl cellulose': ('Thickener E466/INS 466', 'Cellulose-derived stabiliser; FSSAI, EU and CODEX approved; precautionary note from recent gut microbiome research at high doses'),
        'e466': ('CMC / Sodium carboxymethyl cellulose (E466)', 'Cellulose-derived thickener; FSSAI, EU and CODEX approved; generally safe; some animal research at high doses shows potential gut microbiome effects'),

        # Emulsifiers
        'datem': ('Emulsifier E472e/INS 472e', 'FSSAI, EU, FDA and CODEX approved bread emulsifier; generally safe; derived from edible fats and tartaric acid'),
        'e472e': ('DATEM (E472e)', 'FSSAI, EU, FDA and CODEX approved emulsifier used in baked goods; generally safe at specified limits'),
        'sodium stearoyl lactylate': ('Emulsifier E481/INS 481', 'FDA, EU and FSSAI approved bread emulsifier derived from stearic acid and lactic acid; generally safe'),
        'ssl': ('Sodium stearoyl lactylate (E481)', 'FDA, EU and FSSAI approved emulsifier in bread and pastries; generally safe'),
        'e481': ('SSL — Sodium stearoyl lactylate (E481)', 'FDA, EU and FSSAI approved bread emulsifier; generally safe at specified limits'),
        'calcium stearoyl lactylate': ('Emulsifier E482/INS 482', 'EU and CODEX approved emulsifier for baked goods; generally safe'),
        'e482': ('CSL — Calcium stearoyl lactylate (E482)', 'EU and CODEX approved emulsifier; generally safe at specified limits'),

        # Sweeteners with considerations
        'mannitol': ('Sugar alcohol sweetener E421/INS 421', 'FSSAI, EU and CODEX approved; laxative effect when consumed above 20g/day; may cause gas and bloating'),
        'e421': ('Mannitol (E421)', 'Natural sugar alcohol; approved by FSSAI, EU and CODEX; laxative at >20g/day; may cause gas'),
        'isomalt': ('Sugar alcohol sweetener E953/INS 953', 'FSSAI, EU and CODEX approved; laxative effect above 25g/day; may cause flatulence and bloating'),
        'e953': ('Isomalt (E953)', 'Sugar-derived sweetener; FSSAI, EU and CODEX approved; laxative at high doses; mild digestive effects'),
        'xylitol': ('Sugar alcohol sweetener E967/INS 967', 'FSSAI, EU and FDA approved; dental health benefits; laxative above 40g/day; TOXIC TO DOGS — do not share products with pets'),
        'e967': ('Xylitol (E967)', 'FSSAI, EU and FDA approved sweetener; dental protective; laxative at high doses; TOXIC TO DOGS'),
        'erythritol': ('Sugar alcohol sweetener E968/INS 968', 'EU and CODEX approved; zero calories; better tolerated than other polyols; high doses (>50g) may cause nausea in some individuals'),
        'e968': ('Erythritol (E968)', 'EU and CODEX approved zero-calorie sweetener; very well tolerated; very high doses may cause nausea'),
        'steviol glycosides': ('Natural sweetener E960/INS 960', 'FSSAI, EU, FDA GRAS and CODEX approved; zero calorie; ADI 4mg/kg bw as steviol equivalents; very safe profile'),
        'stevia': ('Natural sweetener E960/INS 960', 'FSSAI, EU and FDA approved; zero-calorie natural sweetener; excellent safety record; some individuals report a slightly bitter aftertaste'),
        'e960': ('Steviol glycosides / Stevia (E960)', 'FSSAI, EU, FDA and CODEX approved; zero-calorie natural sweetener; good safety profile at approved ADI'),
        'neotame': ('Artificial sweetener E961/INS 961', 'FDA (2002), EU (2010) and CODEX approved; ultra-high potency — 7,000–13,000x sweeter than sugar; no PKU concern unlike aspartame; limited long-term human data'),
        'e961': ('Neotame (E961)', 'FDA, EU and CODEX approved artificial sweetener; safe — no PKU risk; limited long-term human exposure data compared to older sweeteners'),

        # Mineral salts / Anticaking
        'magnesium carbonate': ('Anticaking agent E504/INS 504', 'FSSAI, EU and CODEX approved mineral; generally safe; provides dietary magnesium'),
        'e504': ('Magnesium carbonate (E504)', 'FSSAI, EU and CODEX approved anticaking mineral; generally safe'),
        'potassium chloride': ('Salt substitute E508/INS 508', 'FSSAI, EU and CODEX approved; safe mineral for most adults; high intake may affect kidney function in individuals with renal disease'),
        'e508': ('Potassium chloride (E508)', 'FSSAI, EU and CODEX approved salt substitute; safe for most; caution in kidney disease'),
        'calcium chloride': ('Firming agent E509/INS 509', 'FSSAI, EU and CODEX approved mineral; safe; provides dietary calcium'),
        'e509': ('Calcium chloride (E509)', 'FSSAI, EU and CODEX approved firming agent; generally safe; provides calcium'),
        'calcium sulfate': ('Firming agent E516/INS 516', 'FSSAI, EU and CODEX approved mineral; generally safe; traditional tofu coagulant; provides dietary calcium'),
        'e516': ('Calcium sulfate (E516)', 'FSSAI, EU and CODEX approved mineral firming agent; generally safe; provides calcium'),
        'magnesium oxide': ('Anticaking agent E530/INS 530', 'EU and CODEX approved mineral; provides dietary magnesium; generally safe'),
        'e530': ('Magnesium oxide (E530)', 'EU and CODEX approved anticaking agent; provides magnesium; generally safe'),
        'e551': ('Silicon dioxide (E551)', 'FSSAI, EU and CODEX approved anticaking agent; generally safe; amorphous form (food-grade) is safe — crystalline form is a different occupational hazard'),

        # Flavour enhancers
        'glutamic acid': ('Flavour enhancer E620/INS 620', 'Natural amino acid form of MSG; FSSAI, EU and CODEX approved; safe at normal dietary levels; sensitive individuals may experience MSG-like effects'),
        'e620': ('L-Glutamic acid (E620)', 'FSSAI, EU and CODEX approved; same safety profile as MSG; naturally present in high amounts in fermented foods'),
        'disodium ribonucleotides': ('Flavour enhancer E635/INS 635', 'FSSAI and EU limit use to 500 mg/kg in most processed food categories; raises uric acid — avoid if you have gout or hyperuricaemia; not recommended for infants; MSG-sensitive individuals may also react'),
        "disodium 5'-ribonucleotides": ('Flavour enhancer E635/INS 635', 'FSSAI and EU permit up to 500 mg/kg in most processed foods; raises uric acid levels — avoid if you have gout or hyperuricaemia; not recommended for infants and young children; those with MSG sensitivity may also react'),
        "disodium 5' ribonucleotides": ('Flavour enhancer E635/INS 635', 'FSSAI and EU limit to 500 mg/kg; raises uric acid — avoid if you have gout or high uric acid; not suitable for infants'),
        'disodium 5-ribonucleotides': ('Flavour enhancer E635/INS 635', 'FSSAI and EU limit to 500 mg/kg in most processed foods; raises uric acid — avoid if you have gout or hyperuricaemia; not recommended for infants; MSG-sensitive individuals may also react'),
        'e635': ('Disodium 5\'-ribonucleotides (E635)', 'FSSAI and EU limit to 500 mg/kg in most processed food categories; raises uric acid — avoid if you have gout or hyperuricaemia; not recommended for infants; MSG-sensitive individuals may also react'),

        # Modified Starches
        'acetylated distarch adipate': ('Modified starch E1422/INS 1422', 'FSSAI, EU, CODEX and FDA approved; excellent safety data — EFSA ADI "not specified" in 2017; very widely used'),
        'e1422': ('Acetylated distarch adipate (E1422)', 'FSSAI, EU, CODEX and FDA approved modified starch; EFSA confirmed ADI "not specified"; very safe profile'),
        'hydroxypropyl distarch phosphate': ('Modified starch E1442/INS 1442', 'FSSAI, EU, CODEX and FDA approved; EFSA ADI "not specified" in 2017; one of the most widely used modified starches globally'),
        'e1442': ('Hydroxypropyl distarch phosphate (E1442)', 'FSSAI, EU, CODEX and FDA approved; EFSA ADI "not specified"; widely used and well studied'),
        'starch sodium octenyl succinate': ('Modified starch E1450/INS 1450', 'FSSAI, EU and CODEX approved emulsifying starch; EFSA ADI "not specified"; very safe profile'),
        'e1450': ('Starch sodium octenyl succinate (E1450)', 'FSSAI, EU and CODEX approved modified starch; EFSA ADI "not specified"; safe at permitted levels'),
        'distarch phosphate': ('Modified starch E1412/INS 1412', 'FSSAI, EU and CODEX approved cross-linked starch; generally safe; ADI not specified by EFSA'),
        'e1412': ('Distarch phosphate (E1412)', 'FSSAI, EU and CODEX approved cross-linked starch; generally safe'),
        'acetylated starch': ('Modified starch E1420/INS 1420', 'FSSAI, EU and CODEX approved; mildly modified starch; generally safe'),
        'e1420': ('Acetylated starch (E1420)', 'FSSAI, EU and CODEX approved mildly modified starch; generally safe'),

        # Antifoaming
        'dimethyl polysiloxane': ('Antifoaming agent E900/INS 900', 'FDA GRAS; EU and CODEX approved; generally safe at food use levels (≤10mg/kg in frying oils)'),
        'dimethylpolysiloxane': ('Antifoaming agent E900/INS 900', 'FDA GRAS; EU and CODEX approved antifoaming agent; generally safe at specified limits in cooking oils'),
        'e900': ('Dimethylpolysiloxane (E900)', 'FDA GRAS; EU and CODEX approved; generally safe as antifoaming agent in frying oils and some beverages'),

        # Acidity regulators
        'acetic acid': ('Acidity regulator E260/INS 260 (Vinegar acid)', 'FSSAI, EU and CODEX approved; one of the safest food acids; tooth enamel erosion concern with frequent direct contact'),
        'e260': ('Acetic acid (E260)', 'FSSAI, EU and CODEX approved; safe at normal food use levels; minimal concerns'),
        'sodium acetate': ('Acidity regulator E262/INS 262', 'FSSAI, EU and CODEX approved; generally safe; watch sodium intake if on restricted diet'),
        'e262': ('Sodium acetate (E262)', 'FSSAI, EU and CODEX approved acidity regulator; generally safe'),
        'tartaric acid': ('Acidulant E334/INS 334', 'FSSAI, EU and CODEX approved; natural grape-derived acid; EFSA ADI 30mg/kg bw; generally safe at food use levels'),
        'e334': ('L-Tartaric acid (E334)', 'FSSAI, EU and CODEX approved; natural acidulant; generally safe at specified levels'),
        'sodium citrate': ('Acidity regulator E331/INS 331', 'FSSAI, EU and CODEX approved; generally safe; watch sodium intake; safe for most people'),
        'e331': ('Sodium citrate (E331)', 'FSSAI, EU and CODEX approved; generally safe acidity regulator'),
        'calcium citrate': ('Firming agent/supplement E333/INS 333', 'FSSAI, EU and CODEX approved; well-absorbed calcium supplement; generally safe'),
        'e333': ('Calcium citrate (E333)', 'FSSAI, EU and CODEX approved; bioavailable calcium supplement; generally safe'),
        'calcium carbonate': ('Mineral / white colorant E170/INS 170', 'FSSAI, EU and CODEX approved; natural mineral; excellent calcium source; very safe profile'),
        'e170': ('Calcium carbonate (E170)', 'FSSAI, EU and CODEX approved; natural chalk; calcium supplement; very safe'),
        'sodium hydroxide': ('pH adjuster E524/INS 524', 'FSSAI, EU and CODEX approved for food processing; fully neutralised in the final product; safe when used correctly'),
        'e524': ('Sodium hydroxide (E524)', 'FSSAI, EU and CODEX approved pH adjuster; safe in finished food when fully neutralised'),
        'calcium hydroxide': ('pH adjuster / firming agent E526/INS 526', 'FSSAI, EU and CODEX approved; used in nixtamalisation — improves nutrition of maize; generally safe'),
        'e526': ('Calcium hydroxide (E526)', 'FSSAI, EU and CODEX approved; safe when used in food processing at specified levels'),
        'cream of tartar': ('Baking acid E336', 'Natural potassium salt from wine fermentation; FSSAI and CODEX approved; generally safe'),

        # Enzymes
        'amylase': ('Flour treatment enzyme E1100/INS 1100', 'FSSAI, EU and FDA GRAS approved; natural enzyme used in baking; no safety concerns at bread-use concentrations'),
        'e1100': ('Alpha-amylase (E1100)', 'FSSAI, EU and FDA GRAS enzyme; very safe at food-use concentrations; bakers\' asthma — occupational inhalation concern, not dietary concern'),
        'lipase': ('Natural fat-digesting enzyme', 'FDA GRAS; EU approved processing aid; very safe at food use concentrations; digestive enzyme supplement benefits'),
        'protease': ('Natural protein-digesting enzyme', 'FDA GRAS; EU approved processing aid; safe at food use concentrations; digestive enzyme supplement'),
        'lactase': ('Lactose-digesting enzyme', 'FDA GRAS; EU approved; safe — allows lactose-intolerant individuals to digest dairy products'),

        # Food ingredients
        'fructose': ('Fruit sugar', 'Naturally found in fruits; excess intake from added fructose (not whole fruit) linked to fatty liver, insulin resistance and metabolic syndrome'),
        'ethyl vanillin': ('Synthetic vanilla flavouring', 'FDA and EU approved synthetic flavouring; 3–4 times stronger than vanillin; generally safe at food use concentrations; some reports of sensitivity at high doses'),
        'dextrose monohydrate': ('Glucose (Dextrose) sweetener', 'High glycemic index food sugar; provides rapid energy; watch blood glucose impact for diabetics'),
        'groundnut': ('Peanut (major allergen)', 'One of the most common and severe food allergens globally; mandatory declaration in EU and India under FSSAI; risk of anaphylaxis in allergic individuals'),
        'groundnut oil': ('Peanut oil (potential allergen)', 'High smoke point cooking oil; peanut allergen may persist in refined oil — refined peanut oil is generally considered safe for peanut allergy, but cold-pressed/unrefined peanut oil is not safe for peanut allergics'),
        'sesame oil': ('Sesame oil (allergen)', 'Rich in healthy fats; sesame is a mandatory declaration allergen in EU, USA (since 2023), and under Indian FSSAI labelling rules; cold-pressed oil retains allergen'),
        'mustard oil': ('Mustard seed oil (allergen / erucic acid)', 'Pungent cooking oil; mustard is a major EU allergen (declaration required); contains erucic acid — EU limits erucic acid in food oils to 2% (20g/kg); FDA does not approve for cooking in the USA'),
        'soy protein': ('Soy protein concentrate/isolate (major allergen)', 'Complete plant protein; soy is one of the 14 major EU allergens and 8 US major allergens — mandatory declaration required; rare anaphylaxis possible'),

        # Cosmetic actives with considerations
        'kojic acid': ('Skin-brightening active', 'Tyrosinase inhibitor used to reduce dark spots; approved in Japan at 1% and EU evaluating at 1% in face care; may cause skin irritation or contact dermatitis in sensitive individuals'),
        'glycolic acid': ('Alpha hydroxy acid (AHA) exfoliant', 'FDA and EU approved cosmetic exfoliant; increases sun sensitivity — SPF protection essential; may cause irritation, burning, peeling especially above 10%'),
        'azelaic acid': ('Multi-functional skincare acid', 'FDA prescription approved at 15–20% for acne and rosacea; OTC concentrations safe; may cause temporary burning, stinging, tingling especially initially'),
        'zinc pyrithione': ('Antifungal/antibacterial active', 'EU Cosmetics Regulation updated restrictions in 2021 — permitted in rinse-off products (shampoos) at up to 1%; banned in leave-on products and cosmetic products that may be accidentally ingested'),
        'octinoxate': ('Chemical UV-B filter', 'EU and FDA approved UV filter (OMC); under regulatory review for potential endocrine activity and coral reef toxicity; Hawaii restricts sale; use with physical filters recommended for reef safety'),
        'avobenzone': ('Chemical UV-A filter', 'EU and FDA approved broad UVA filter; photounstable without stabilisers; generally safe in sunscreens at approved concentrations'),
        'octocrylene': ('Chemical UV-B/UVA filter', 'EU and FDA approved UV filter; under study for potential coral accumulation; generally safe at approved cosmetic concentrations'),
        'charcoal': ('Activated charcoal skincare/oral ingredient', 'Generally safe in topical and oral use; may reduce absorption of medications if swallowed; no proven whitening effect on teeth despite marketing claims'),

        # Additional E numbers needing worth_knowing classification
        'green s': ('Synthetic green dye E142/INS 142', 'Not approved in USA, Canada or Japan; permitted in EU and some Asian countries; watch for potential sensitivities'),
        'e142': ('Green S (E142)', 'Synthetic azo dye not approved in USA or Canada; EU permitted; used in peas and mint products'),
        'brilliant black': ('Synthetic black dye E151/INS 151', 'Not permitted in USA, Canada or Japan; EU approved; azo dye — some sensitivity concerns'),
        'e151': ('Brilliant Black BN (E151)', 'Synthetic azo dye banned in USA; EU approved; used in some confectionery and savoury foods'),
        'e173': ('Aluminium (E173)', 'Metallic food colour; permitted only on surface of confectionery; aluminium accumulation in body is a concern at high repeated exposures; not for general food use'),
        'e212': ('Potassium benzoate (E212)', 'Potassium salt of benzoic acid; same benzene formation risk with ascorbic acid as E211; FSSAI approved; worth monitoring in acidic drinks with added Vitamin C'),
        'potassium benzoate': ('Preservative E212/INS 212', 'Can form trace benzene in the presence of Vitamin C (ascorbic acid) in acidic beverages; FSSAI and EU approved at specified limits'),
        'e252': ('Potassium nitrate (E252)', 'Traditional curing salt; converts to nitrite during curing; FSSAI and EU permit at strict limits in cured meats; consume processed meats in moderation'),
        'e283': ('Potassium propionate (E283)', 'Antifungal preservative in bread; EU and CODEX approved; may cause migraine in sensitive individuals'),
        'potassium propionate': ('Preservative E283/INS 283', 'Used in bread and baked goods to prevent mould; EU and CODEX approved; migraine trigger in sensitive individuals'),
        'e311': ('Octyl gallate (E311)', 'Synthetic antioxidant in fats/oils; may cause reactions in aspirin-sensitive individuals; EU permitted'),
        'e312': ('Dodecyl gallate (E312)', 'Synthetic antioxidant in fats/oils; potential skin sensitiser; EU permitted'),
        'e905': ('Mineral oil (E905)', 'Petroleum-derived glazing agent on fresh/dried fruit; concern over MOAH (mineral oil aromatic hydrocarbons) contamination — potentially carcinogenic; EFSA is evaluating'),
        'mineral oil': ('Petroleum-derived glazing agent E905', 'Used on fresh/dried fruit surfaces; EFSA has raised concern about MOAH (aromatic hydrocarbon) contaminants in mineral oil; under regulatory review'),
        'e535': ('Sodium ferrocyanide (E535)', 'Anti-caking agent in table salt; despite the "cyanide" name, it is chemically stable and safe at food-use levels; FSSAI, EU and CODEX approved'),
        'sodium ferrocyanide': ('Anti-caking agent E535/INS 535', 'Used in table salt; FSSAI, EU and CODEX approved; stable compound — cyanide is tightly bound and not released; safe at food additive levels'),
        'e249': ('Potassium nitrite (E249)', 'Curing agent that can form nitrosamines (probable carcinogens) at high cooking temperatures; FSSAI and EU strictly limit use; consume cured meats in moderation'),
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

        # ── Indian Herbs & Ayurvedic Ingredients ─────────────────────────────────
        'amla': ('Indian gooseberry (Vitamin C-rich Ayurvedic herb)', 'One of the richest natural Vitamin C sources; cornerstone of Ayurveda for 3,000+ years; well tolerated; safe'),
        'amalaki': ('Indian gooseberry (Ayurvedic name for amla)', 'Ayurvedic rasayana herb; rich in Vitamin C and polyphenols; safe'),
        'brahmi': ('Bacopa monnieri (Ayurvedic brain tonic)', 'Clinically studied adaptogenic herb; generally safe; high doses may cause nausea or stomach cramping in some individuals'),
        'bhringraj': ('Eclipta prostrata (Ayurvedic hair herb)', 'Traditional Ayurvedic herb used in hair oils; generally safe for topical use'),
        'shikakai': ('Acacia concinna (Natural hair cleanser)', 'Traditional Indian hair-washing herb with natural saponins; gentle and safe for hair'),
        'reetha': ('Soapnut (Sapindus mukorossi)', 'Natural saponin-rich fruit used as a hair cleanser; safe and biodegradable'),
        'soapnut': ('Soapnut / Reetha (Sapindus mukorossi)', 'Natural surfactant from soapberry; safe and biodegradable hair cleanser'),
        'triphala': ('Three-fruit Ayurvedic formulation (amla, haritaki, bibhitaki)', 'Classical Ayurvedic blend; generally safe; high doses may cause loose stools; well-established safety profile'),
        'giloy': ('Tinospora cordifolia (Guduchi / Ayurvedic immunomodulator)', 'Important Ayurvedic immunomodulatory herb; generally safe; very high doses may lower blood sugar'),
        'guduchi': ('Tinospora cordifolia (Giloy)', 'Ayurvedic herb; generally safe as supplement'),
        'moringa': ('Moringa oleifera (Drumstick tree / Superfood)', 'Highly nutrient-dense leaves; generally safe; root extracts not recommended in pregnancy'),
        'karela': ('Bitter gourd / Bitter melon (Momordica charantia)', 'Traditional blood sugar herb; generally safe in food amounts; caution with diabetes medications due to potential additive blood-glucose lowering'),
        'methi': ('Fenugreek (Trigonella foenum-graecum)', 'Safe traditional spice and Ayurvedic herb; high doses may interact with blood-thinning medications'),
        'mulethi': ('Licorice root (Glycyrrhiza glabra)', 'Traditional Ayurvedic herb; safe in moderate amounts; very high long-term doses can raise blood pressure and cause electrolyte imbalance'),
        'chandan': ('Sandalwood (Santalum album)', 'Traditional Ayurvedic skincare ingredient; soothing and antimicrobial; generally safe for topical use'),
        'haritaki': ('Terminalia chebula (Ayurvedic digestive herb)', 'One of the three fruits of triphala; generally safe as food supplement'),
        'bibhitaki': ('Terminalia bellirica (Ayurvedic herb)', 'One of the three fruits of triphala; generally safe'),
        'shatavari': ('Asparagus racemosus (Ayurvedic female tonic)', 'Traditional female health herb; generally safe; may cause mild digestive effects in some individuals'),
        'multani mitti': ('Fuller\'s Earth clay (Multani Mitti)', 'Natural absorbent clay mineral; safe for topical use; traditional Indian beauty ingredient'),
        'kaolin': ('Natural white clay mineral', 'Safe absorbent and mattifying ingredient; widely used in cosmetics and pharmaceuticals'),
        'noni': ('Morinda citrifolia fruit (Traditional Polynesian herb)', 'Traditional supplement; generally safe at normal intake; very high doses of noni juice have been linked to rare liver toxicity cases'),

        # ── Cosmetic Actives — Generally Recognised ──────────────────────────────
        'niacinamide': ('Vitamin B3 (Nicotinamide) skincare active', 'One of the best-tolerated and most studied cosmetic actives; extensive evidence for skin-brightening, barrier-strengthening and sebum-reducing effects; very safe'),
        'nicotinamide': ('Vitamin B3 skincare active (Niacinamide)', 'Same as niacinamide; well-studied; very safe; no significant adverse effects at cosmetic use concentrations'),
        'sodium hyaluronate': ('Hyaluronic acid salt (skin hydrator)', 'Safe, well-tolerated moisture-binding ingredient; natural to the body; no known adverse effects'),
        'alpha arbutin': ('Skin-brightening glycoside (from bearberry)', 'EU permits at up to 2% in face care; excellent safety profile; well-tolerated; no significant adverse effects'),
        'arbutin': ('Natural skin-brightening compound (from bearberry)', 'EU permitted in cosmetics at specified limits; well-tolerated skin-brightening ingredient'),
        'bakuchiol': ('Plant-based retinol alternative (from babchi plant)', 'Natural meroterpene with retinol-like effects; safe in pregnancy unlike retinol; well-tolerated with minimal irritation; clinically studied'),
        'squalane': ('Plant-derived skin-identical emollient', 'Skin-identical, non-comedogenic, very well tolerated emollient; sourced from sugarcane, olive or amaranth; excellent safety profile'),
        'centella asiatica': ('Centella asiatica (Cica / Gotu kola) extract', 'Clinically studied wound-healing and anti-inflammatory herb; safe and well-tolerated; widely used in sensitive skin care'),
        'allantoin': ('Natural skin-soothing compound (from comfrey)', 'CIR confirmed safe for cosmetic use; very well tolerated including on sensitive skin; soothing and healing properties'),
        'bisabolol': ('Chamomile-derived soothing compound', 'CIR reviewed and confirmed safe; anti-inflammatory, anti-irritant; very well tolerated'),
        'adenosine': ('Naturally occurring nucleoside (anti-ageing active)', 'EU Cosmetics Regulation approved at 0.04% in face care; well tolerated in clinical studies; safe'),
        'zinc oxide': ('Mineral UV filter and skin-soothing ingredient', 'FDA Category I UV filter (GRAS); EU approved mineral sunscreen; anti-inflammatory; safe for sensitive and baby skin'),
        'madecassoside': ('Centella asiatica active compound', 'Key wound-healing and collagen-stimulating compound; safe and well-tolerated'),
        'sea buckthorn oil': ('Sea buckthorn berry/seed oil', 'Nutrient-rich natural oil; rich in Vitamin C, E and omega-7; generally safe; may stain skin/clothes orange due to high carotenoid content'),
        'rosehip oil': ('Rosa canina seed oil', 'Natural plant oil with skin-brightening and anti-ageing properties; generally safe; patch test recommended for sensitive individuals'),

        # ── Food Ingredients — Generally Recognised ──────────────────────────────
        'lecithin': ('Natural emulsifier (from soy, sunflower or egg)', 'Natural phospholipid emulsifier; very widely used; safe; soy lecithin may be a concern for severe soy-allergic individuals — sunflower lecithin is allergen-free'),
        'sunflower lecithin': ('Natural emulsifier from sunflower seeds (allergen-free)', 'Allergen-free alternative to soy lecithin; same emulsifying function; very safe'),
        'vanillin': ('Primary vanilla flavour compound (natural or synthetic)', 'FDA, EU and CODEX approved flavouring; generally safe at food use concentrations; identical compound whether from natural or synthetic source'),
        'dextrose': ('Glucose (dextrose) sweetener', 'The body\'s primary energy source; safe; high GI — watch blood glucose if diabetic'),
        'sea salt': ('Unrefined sea salt', 'Natural salt from seawater; same dietary sodium concerns as table salt; trace minerals present in small amounts'),
        'pea protein': ('Plant-based pea protein (hypoallergenic)', 'Hypoallergenic plant protein; free from top-8 allergens; safe; well tolerated'),
        'rice protein': ('Plant-based rice protein (hypoallergenic)', 'Hypoallergenic plant protein; free from top-8 allergens; safe'),
        'oat bran': ('Oat bran (beta-glucan rich fibre)', 'FDA and EFSA approved heart health claim for beta-glucan; safe; may cause gas and bloating at very high doses'),
        'psyllium husk': ('Psyllium husk (soluble dietary fibre)', 'FDA approved heart health claim; safe; take with plenty of water; may reduce absorption of medications if taken simultaneously'),
        'wheat bran': ('Wheat bran (insoluble dietary fibre)', 'Natural whole grain fibre; safe; not suitable for coeliac disease or wheat allergy; flatulence at high initial doses'),
        'flaxseed': ('Flaxseed / Linseed (omega-3 and fibre)', 'Rich in ALA omega-3; best consumed ground; very safe at normal food amounts; excessive raw flaxseed contains trace cyanogenic glycosides — not a concern at food doses'),
        'chia seeds': ('Chia seeds (Salvia hispanica, omega-3 and fibre)', 'Rich in ALA omega-3 and soluble fibre; generally safe; absorb water and expand — take with adequate fluid'),
        'canola oil': ('Canola oil (low-erucic acid rapeseed oil)', 'One of the healthiest cooking oils — low saturated fat, good omega-3; FDA GRAS; EU and FSSAI approved; safe'),
        'sunflower oil': ('Sunflower seed oil', 'Widely used cooking oil; high in linoleic acid; safe; high omega-6 content — balance with omega-3 sources'),
        'rapeseed oil': ('Rapeseed oil (canola variety)', 'High in monounsaturated fats and ALA; safe cooking oil; EU and FSSAI approved'),
        'rice bran oil': ('Rice bran oil (oryzanol-rich)', 'High smoke point cooking oil; contains oryzanol with studied cholesterol benefits; safe'),
        'lactic acid culture': ('Probiotic lactic acid culture', 'Beneficial bacteria; safe; promotes gut health'),
        'cream of tartar': ('Potassium hydrogen tartrate (natural baking acid)', 'Natural from wine fermentation; safe leavening acid'),
        'dextrose monohydrate': ('Glucose / Dextrose sweetener', 'Safe natural sugar; high GI — moderate use recommended for diabetics'),
        'calcium propionate': ('Bread preservative E282/INS 282', 'FSSAI, EU, FDA and CODEX approved; widely used bread mould inhibitor; generally safe'),
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

    # Cosmetic worth overrides — ingredients that are commonly_questioned in food
    # but only worth_knowing when used topically (e.g. sodium benzoate)
    if is_cosmetic:
        for pat, (what_it_is, note) in COSMETIC_WORTH_OVERRIDES.items():
            if pat in ingredient_lower:
                return {
                    'classification': 'worth_knowing',
                    'what_it_is': what_it_is,
                    'one_line_note': note,
                    'regulatory_note': 'Approved in cosmetics within regulatory limits; benzene formation risk applies to food/beverages, not topical use'
                }

    # Additional generally recognised E-number entries
    generally_recognised_patterns.update({

        # Antioxidants (Vitamin C family)
        'e300': ('Ascorbic Acid / Vitamin C (E300)', 'Vitamin C as food antioxidant — safe and nutritionally beneficial'),
        'e301': ('Sodium Ascorbate (E301)', 'Sodium salt of Vitamin C — safe antioxidant and preservative'),
        'e302': ('Calcium Ascorbate (E302)', 'Calcium salt of Vitamin C — safe antioxidant with calcium benefit'),
        'e304': ('Ascorbyl Palmitate (E304)', 'Fat-soluble Vitamin C ester — safe natural antioxidant for oils'),
        'e306': ('Mixed Tocopherols / Natural Vitamin E (E306)', 'Natural Vitamin E extract — safe antioxidant from vegetable oils'),
        'e307': ('Alpha-Tocopherol / Vitamin E (E307)', 'Active Vitamin E — safe and nutritionally beneficial antioxidant'),
        'e308': ('Gamma-Tocopherol / Vitamin E (E308)', 'Natural Vitamin E — safe antioxidant'),
        'e309': ('Delta-Tocopherol / Vitamin E (E309)', 'Natural Vitamin E — safe antioxidant'),
        'e315': ('Erythorbic Acid (E315)', 'Antioxidant isomer of Vitamin C — safe preservative in cured meats'),
        'e316': ('Sodium Erythorbate (E316)', 'Sodium salt of erythorbic acid — safe antioxidant in cured meats'),
        # Safe natural colours
        'e100': ('Curcumin / Turmeric (E100)', 'Natural yellow colour from turmeric — safe and traditionally consumed'),
        'e100i': ('Curcumin (E100i)', 'Natural turmeric extract — safe food colour'),
        'e101': ('Riboflavin / Vitamin B2 (E101)', 'Natural yellow colour — also a B vitamin; safe and nutritionally beneficial'),
        'e101i': ('Riboflavin (E101i)', 'Vitamin B2 used as food colour — safe and nutritious'),
        'e140': ('Chlorophylls (E140)', 'Natural green plant pigments — safe food colour'),
        'e141': ('Copper Complexes of Chlorophylls (E141)', 'Stabilised natural green colour — safe at permitted levels'),
        'e160c': ('Paprika Extract (E160c)', 'Natural orange-red colour from red peppers — safe'),
        'e162': ('Beetroot Red (E162)', 'Natural red colour from beetroot — safe and rich in antioxidants'),
        'e163': ('Anthocyanins (E163)', 'Natural plant pigments from berries and red cabbage — safe and rich in antioxidants'),
        'e172': ('Iron Oxides (E172)', 'Natural inorganic mineral colouring — safe; also provides small amount of dietary iron'),
        # Vitamins and minerals
        'e101': ('Riboflavin / Vitamin B2 (E101)', 'Vitamin B2 — safe, essential nutrient used also as a food colour'),
        # Natural hydrocolloids (generally safe)
        'e400': ('Alginic Acid (E400)', 'Natural seaweed fibre — safe thickener and gelling agent'),
        'e401': ('Sodium Alginate (E401)', 'Natural seaweed thickener — safe and widely used'),
        'e402': ('Potassium Alginate (E402)', 'Natural seaweed gum — safe thickener'),
        'e404': ('Calcium Alginate (E404)', 'Natural seaweed gel-former — safe'),
        'e406': ('Agar-Agar (E406)', 'Natural seaweed gelling agent — safe; vegan gelatin substitute'),
        'e410': ('Locust Bean Gum / Carob Gum (E410)', 'Natural seed thickener — safe; dietary fibre source'),
        'e412': ('Guar Gum (E412)', 'Natural seed thickener from India — safe; source of dietary fibre'),
        'e414': ('Acacia / Gum Arabic (E414)', 'Natural tree gum — safe; prebiotic fibre; used for 4000+ years'),
        'e440': ('Pectins (E440)', 'Natural fruit gelling agent — safe; source of soluble dietary fibre'),
        'e440i': ('Amidated Pectin (E440i)', 'Modified natural pectin — safe gelling agent'),
        # Cellulose (inert)
        'e460': ('Cellulose (E460)', 'Natural plant fibre — indigestible and inert; safe bulking agent'),
        'e460i': ('Microcrystalline Cellulose/MCC (E460i)', 'Refined plant fibre — safe inert bulking agent'),
        'e461': ('Methyl Cellulose (E461)', 'Cellulose derivative — safe thickener and fat replacer'),
        'e462': ('Ethyl Cellulose (E462)', 'Cellulose derivative used in coatings — safe'),
        'e463': ('Hydroxypropyl Cellulose/HPC (E463)', 'Cellulose derivative — safe thickener and binder'),
        'e464': ('Hydroxypropyl Methyl Cellulose/HPMC (E464)', 'Cellulose derivative — safe in gluten-free bread and pharmaceuticals'),
        # Safe anti-caking
        'e530': ('Magnesium Oxide (E530)', 'Safe inorganic anti-caking agent; dietary magnesium source'),
        'e551': ('Silicon Dioxide / Silica (E551)', 'Inorganic anti-caking agent — not absorbed; safe at food levels'),
        'e552': ('Calcium Silicate (E552)', 'Inorganic anti-caking agent — safe'),
        'e553a': ('Magnesium Silicates (E553a)', 'Inorganic anti-caking agent — safe'),
        # Acidity regulators (natural)
        'e260': ('Acetic Acid / Vinegar Acid (E260)', 'The acid in vinegar — safe natural acidulant and preservative'),
        'e270': ('Lactic Acid (E270)', 'Natural fermentation acid — safe; found in yoghurt, cheese and sourdough'),
        'e296': ('Malic Acid (E296)', 'Natural fruit acid from apples — safe acidulant'),
        'e297': ('Fumaric Acid (E297)', 'Natural organic acid — safe leavening acid and acidulant'),
        'e325': ('Sodium Lactate (E325)', 'Sodium salt of lactic acid — safe humectant and preservative'),
        'e327': ('Calcium Lactate (E327)', 'Calcium salt of lactic acid — safe; provides calcium'),
        'e330': ('Citric Acid (E330)', 'Natural fruit acid — most widely used acidulant; safe'),
        'e331': ('Sodium Citrates (E331)', 'Sodium salts of citric acid — safe acidity regulators and emulsifying salts'),
        'e332': ('Potassium Citrates (E332)', 'Potassium salts of citric acid — safe acidity regulators'),
        'e333': ('Calcium Citrates (E333)', 'Calcium salts of citric acid — safe; provides calcium'),
        'e334': ('Tartaric Acid (E334)', 'Natural grape acid — safe; used in wine and baking powder'),
        'e335': ('Sodium Tartrates (E335)', 'Sodium salts of tartaric acid — safe'),
        'e336': ('Potassium Tartrates / Cream of Tartar (E336)', 'Natural wine-derived salt — safe; classic baking ingredient'),
        'e337': ('Potassium Sodium Tartrate / Rochelle Salt (E337)', 'Mixed tartrate — safe acidity regulator'),
        # Carbon dioxide
        'e290': ('Carbon Dioxide (E290)', 'Natural gas — safe; responsible for carbonation in beverages'),
        # Preservatives (safe ones)
        'e200': ('Sorbic Acid (E200)', 'Natural preservative from rowan berries — safe at food levels'),
        'e201': ('Sodium Sorbate (E201)', 'Safe natural-origin preservative'),
        'e203': ('Calcium Sorbate (E203)', 'Safe natural-origin preservative'),
        'e234': ('Nisin (E234)', 'Natural antimicrobial peptide from fermentation — safe; not absorbed by gut'),
        'e235': ('Natamycin / Pimaricin (E235)', 'Natural antifungal from fermentation — safe; used on cheese surfaces only'),
        'e280': ('Propionic Acid (E280)', 'Natural fermentation acid — safe mould inhibitor in bread'),
        # Sugar alcohols (safe ones)
        'e968': ('Erythritol (E968)', 'Natural zero-calorie sugar alcohol — best tolerated of all; rarely causes digestive issues'),
        'e967': ('Xylitol (E967)', 'Natural sugar alcohol — safe for teeth; digestive discomfort only at high doses'),
        # Starch modifications (generally safe)
        'e1410': ('Monostarch Phosphate (E1410)', 'Modified starch — safe thickener'),
        'e1420': ('Acetylated Starch (E1420)', 'Modified starch — safe thickener'),
        'e1422': ('Acetylated Distarch Adipate (E1422)', 'Modified starch — safe in frozen foods'),
        'e1440': ('Hydroxypropyl Starch (E1440)', 'Modified starch — safe in frozen foods'),
        'e1442': ('Hydroxypropyl Distarch Phosphate (E1442)', 'Modified starch — safe; high stability under heat and acid'),
        'e1201': ('Polyvinylpyrrolidone / PVP (E1201)', 'Synthetic clarifying agent — safe at food/pharmaceutical use levels'),

    })

    # IFRA certified / allergen-free fragrance → worth_knowing
    if any(w in ingredient_lower for w in ('fragrance', 'parfum', 'perfume')) and \
            ('ifra' in ingredient_lower or 'allergen free' in ingredient_lower or 'allergen-free' in ingredient_lower):
        return {
            'classification': 'worth_knowing',
            'what_it_is': 'IFRA Certified Fragrance',
            'one_line_note': 'IFRA certified fragrance — independently tested for allergen safety; lower sensitisation risk than undisclosed fragrance blends; individual compounds still not disclosed on label',
            'regulatory_note': 'IFRA (International Fragrance Association) certified; meets global fragrance safety standards'
        }

    # Certified organic fragrance override — must run before 'fragrance' → commonly_questioned
    if any(w in ingredient_lower for w in ('fragrance', 'parfum', 'perfume')) and 'certified organic' in ingredient_lower:
        return {
            'classification': 'generally_recognised',
            'what_it_is': 'Certified Organic Fragrance',
            'one_line_note': 'Certified organic fragrance — sourced from organically grown botanicals with full certification; no undisclosed synthetic chemical concern',
            'regulatory_note': 'Certified organic; generally recognised as safe'
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

    # Sub-type fallback: if 'e500ii' not found in any pattern, retry with parent 'e500'
    if _re.match(r'^e\d+(i{1,3}v?|iv|v)$', ingredient_lower):
        parent = _re.sub(r'(i{1,3}v?|iv|v)$', '', ingredient_lower)
        if parent != ingredient_lower:
            return classify_ingredient(parent, category)

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
