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

    # ── New Cosmetic & Personal Care Ingredients ──────────────────────────────
    'cetyl esters': 'Cetyl Esters is a mixture of esters of saturated fatty alcohols and fatty acids, used as a waxy emollient in hair conditioners and skin creams. It gives a rich, creamy texture without greasiness and is a plant-derived alternative to spermaceti wax (historically from sperm whales). CIR Expert Panel has confirmed it is safe for cosmetic use.',
    'quaternium-33': 'Quaternium-33 is a quaternary ammonium conditioning polymer used in hair care products to reduce static and improve combability. It provides anti-static and softening effects by adsorbing onto the negatively charged hair surface. Generally considered safe at cosmetic use concentrations.',
    'hydroxypropyltrimonium hydrolyzed wheat protein': 'Hydroxypropyltrimonium Hydrolyzed Wheat Protein is a cationic (positively charged) derivative of hydrolyzed wheat protein. The quaternary ammonium group allows it to bond electrostatically to damaged, negatively charged hair, depositing protein to reinforce and strengthen the hair shaft. Effective for frizz control and damage repair. Safe at cosmetic concentrations. Note: contains wheat — relevant for those with wheat allergy using rinse-off products with prolonged contact.',
    'behentrimonium chloride': 'Behentrimonium Chloride (BTAC-22) is a quaternary ammonium salt derived from rapeseed or coconut oil, used as a conditioning agent in hair conditioners and treatments. It imparts smoothness, reduces frizz and improves detangling. EU Cosmetics Regulation restricts its use to 3% in rinse-off and 1% in leave-on products. Generally safe within these limits; higher concentrations can irritate skin and eyes.',
    'trideceth-6': 'Trideceth-6 is a non-ionic surfactant and emulsifier produced by ethoxylating tridecanol (a fatty alcohol) with approximately 6 moles of ethylene oxide. Used to emulsify oils in water in creams and conditioners. The ethoxylation process can introduce trace amounts of 1,4-dioxane, a possible carcinogen (IARC Group 2B) — manufacturers can minimise this through vacuum stripping. Generally considered safe within approved cosmetic use concentrations.',
    'chlorhexidine digluconate': 'Chlorhexidine Digluconate is a water-soluble salt of chlorhexidine — a potent broad-spectrum antiseptic effective against a wide range of bacteria, fungi and some viruses. Used in mouthwashes, wound care and surgical scrubs. EU Cosmetics Regulation restricts it to 0.3% in oral hygiene products and 0.5% in other applications. Rare but serious risk of severe allergic reactions (anaphylaxis) has been documented, primarily from medical-grade products. Ototoxic — must not contact the middle ear. Not recommended for daily home cosmetic use.',
    'limonene': 'Limonene is a naturally occurring cyclic terpene found in the peel of citrus fruits (lemons, oranges, limes) and in many plant essential oils. It is widely used as a fragrance ingredient and is one of the most prevalent terpenes in nature. However, it is also one of the most common causes of fragrance-related contact dermatitis. The EU Cosmetics Regulation requires individual declaration on labels when present above 0.001% in leave-on products or 0.01% in rinse-off products. Limonene can also auto-oxidise on storage to form more potent skin sensitisers.',
    'linalool': 'Linalool is a naturally occurring terpene alcohol found in lavender, coriander, rosewood and many other plants. It contributes to floral, woody scents in perfumes, personal care products and household products. Like limonene, linalool is an EU-mandated fragrance allergen that must be individually declared on cosmetic labels above threshold concentrations. Linalool can oxidise on storage to form linalool hydroperoxides, which are stronger skin sensitisers than the parent compound. A common trigger for fragrance-related contact dermatitis.',
    'benzyl salicylate': 'Benzyl Salicylate is a synthetic ester with a sweet, floral, balsamic fragrance, used in perfumes, shampoos and lotions. It is one of the 26 fragrance allergens required by EU Cosmetics Regulation to be individually declared on labels when present above threshold concentrations. Associated with contact allergic reactions in sensitised individuals, particularly those with fragrance allergy.',
    'hexyl cinnamal': 'Hexyl Cinnamal (Hexyl Cinnamaldehyde) is a synthetic aldehyde with a strong jasmine-like fragrance, widely used in personal care products, perfumes and household cleaners. It is one of the 26 EU-mandated fragrance allergens that must be individually declared on cosmetic labels. Can cause contact allergic dermatitis in sensitised individuals. One of the more common fragrance allergens identified in patch testing.',
    'isopropyl alcohol': 'Isopropyl Alcohol (IPA / Isopropanol) is a petroleum-derived short-chain alcohol used as a solvent, antiseptic and astringent in cosmetics, hand sanitisers, antiseptic wipes and pharmaceuticals. Effective at denaturing proteins and killing bacteria and viruses. However, frequent application is drying to the skin — it can strip natural oils and disrupt the skin barrier, leading to dryness, irritation and potential sensitisation. Not recommended for daily cosmetic use on the face or as a primary skincare ingredient.',
    'cetrimonium chloride': 'Cetrimonium Chloride (CTAC) is a quaternary ammonium salt used as a conditioning agent in hair rinses, conditioners and hair masks. It imparts smoothness and reduces static by coating the negatively charged hair surface. EU Cosmetics Regulation restricts it to 0.25% in rinse-off products due to its potential to cause skin and eye irritation at higher concentrations. Also used as a mild preservative at low concentrations. Toxic to aquatic organisms — environmental persistence noted.',
    'butylphenyl methylpropional': 'Butylphenyl Methylpropional (Lilial) is a synthetic fragrance ingredient with a floral, lily-like scent that was widely used in perfumes, shampoos, conditioners, lotions and household products for decades. It has been BANNED in the European Union since March 2022 under the EU Cosmetics Regulation (Regulation EC 1223/2009, Amendment 2021/1099) due to its classification as a Category 1B reproductive toxicant (toxic to reproduction). Studies demonstrated adverse effects on fertility in animal studies. Products containing Lilial can no longer be sold in the EU. Consumers should avoid products still listing this ingredient.',
    'arginine': 'Arginine is a semi-essential amino acid naturally present in the body and in protein-rich foods such as meat, dairy, nuts and legumes. In cosmetics, it is used as a hair and skin conditioning agent — it helps neutralise negative charges on damaged hair and can help repair the cortex. In skincare, it supports wound healing and barrier function. Safe and well-tolerated; naturally occurring.',
    'serine': 'Serine is a non-essential amino acid naturally found in the skin as part of the Natural Moisturising Factor (NMF) — the collection of water-soluble compounds in the stratum corneum that keep skin hydrated. Used in cosmetics as a humectant and skin-conditioning agent to help maintain skin hydration. Safe and naturally occurring.',
    '2-oleamido-1,3-octadecanediol': '2-Oleamido-1,3-Octadecanediol is a synthetic ceramide analogue (a compound that structurally mimics natural skin ceramides). It contains both an oleic acid-derived amide group and a diol that replicate the sphingolipid backbone of endogenous ceramides. Used in advanced barrier-repair skin care formulations to restore the skin lipid lamellar structure, reduce transepidermal water loss (TEWL) and soothe dry, eczema-prone or compromised skin. Safe and well tolerated.',
    'glyceryl linoleate': 'Glyceryl Linoleate is a naturally occurring glyceryl ester of linoleic acid (omega-6 fatty acid). Found naturally in many vegetable oils including safflower and sunflower oil. Used in cosmetics as an emollient and skin-conditioning agent. Linoleic acid is an essential fatty acid for healthy skin barrier function — it is depleted in acne-prone and atopic skin. Restores the skin lipid barrier, reduces inflammation and supports the ceramide pathway. Safe and skin-compatible.',
    'glyceryl oleate': 'Glyceryl Oleate (Glyceryl Monooleate) is a natural emulsifier and emollient derived from oleic acid and glycerol. Found naturally in olive and sunflower oils. Used in skin and hair care as a gentle emulsifier, emollient and conditioner. Helps maintain the skin moisture barrier. Safe and well-tolerated.',
    'glyceryl linolenate': 'Glyceryl Linolenate is a glyceryl ester of alpha-linolenic acid (ALA, omega-3 fatty acid), found naturally in flaxseed, perilla and hemp oils. Used in cosmetics as an emollient and skin barrier-restoring ingredient. Omega-3 fatty acids have anti-inflammatory properties and support ceramide synthesis in skin. Safe and skin-compatible.',

    # ── EU Fragrance Allergens (additional) ──────────────────────────────────
    'eugenol': 'Eugenol is a naturally occurring phenol found abundantly in clove oil, cinnamon, basil and nutmeg. Used as a flavouring in food and as a fragrance ingredient in cosmetics. It is also used as a local anaesthetic and antiseptic in dentistry. One of the 26 EU mandatory fragrance allergens that must be declared on cosmetic labels. Can cause contact allergic dermatitis in sensitised individuals.',
    'geraniol': 'Geraniol is a naturally occurring terpene alcohol found in geranium, rose, palmarosa and citronella essential oils. Used as a fragrance ingredient in cosmetics, personal care and household products. One of the 26 EU mandatory fragrance allergens that must be individually declared. Can oxidise on storage to form stronger skin sensitisers. A common fragrance allergen in patch testing.',
    'coumarin': 'Coumarin is a naturally occurring lactone found in tonka beans, sweet clover, cassia cinnamon and many essential oils. Used as a fragrance ingredient in perfumes, cosmetics and formerly as a flavouring. EU Cosmetics Regulation requires individual declaration as an allergen. In food, EU restricts coumarin content due to hepatotoxicity at very high doses (studies in rodents at high doses showed liver damage). Safe at the very low amounts typical of cosmetic use.',
    'cinnamal': 'Cinnamal (Cinnamic Aldehyde) is the primary fragrance compound responsible for the characteristic scent of cinnamon. A potent skin sensitiser and one of the 26 EU mandatory fragrance allergens. Must be declared individually on cosmetic labels. Can cause contact allergic dermatitis — particularly in occupational settings (bakers, confectioners) and in leave-on personal care products.',
    'benzyl alcohol': 'Benzyl Alcohol is a naturally occurring aromatic alcohol found in jasmine, hyacinth and many other plant essential oils; also produced synthetically. Used as a preservative, solvent and fragrance ingredient in cosmetics and pharmaceuticals. One of the 26 EU mandatory fragrance allergens — must be declared above threshold concentrations. At high concentrations, it metabolises to benzaldehyde and benzoic acid, which can be irritating. Critically, benzyl alcohol is toxic to neonates — it can cause fatal "gasping syndrome" in premature or newborn infants; never use products containing it on newborns.',
    'farnesol': 'Farnesol is a naturally occurring sesquiterpene alcohol found in ylang-ylang, rose, musk and many other essential oils. Used in fragrances and cosmetics. One of the 26 EU mandatory fragrance allergens. Can cause contact allergic dermatitis in sensitised individuals. Also has antimicrobial properties at higher concentrations.',
    'citronellol': 'Citronellol is a natural terpene alcohol found in geranium, rose, citronella and lemon essential oils. Widely used in perfumes and cosmetics for its floral, rosy scent. One of the 26 EU mandatory fragrance allergens — must be declared individually on cosmetic labels. Can cause contact allergy in sensitised individuals.',
    'hydroxycitronellal': 'Hydroxycitronellal is a synthetic aldehyde fragrance with a strong lily-of-the-valley and muguet scent. Used in perfumes and personal care products. One of the 26 EU mandatory fragrance allergens. Can cause contact sensitisation and allergic reactions in some individuals.',
    'isoeugenol': 'Isoeugenol is a structural isomer of eugenol found in ylang-ylang, nutmeg and clove oils. Used as a fragrance ingredient. One of the 26 EU mandatory fragrance allergens. Considered a stronger sensitiser than eugenol — it has been voluntarily restricted or banned in some cosmetic applications by the fragrance industry.',
    'benzyl benzoate': 'Benzyl Benzoate is a naturally occurring ester in Peru balsam and some essential oils; also produced synthetically. Used as a fragrance fixative and in cosmetics. Also used medically as an antiparasitic agent (scabies, lice treatment). One of the 26 EU mandatory fragrance allergens. Can cause contact allergy in sensitive individuals.',
    'benzyl cinnamate': 'Benzyl Cinnamate (Cinnamein) is a naturally occurring ester in Peru balsam, styrax and tolu balsam. Used as a fragrance fixative. One of the 26 EU mandatory fragrance allergens. Found to cause contact sensitisation in some individuals.',
    'amyl cinnamal': 'Amyl Cinnamal (Amyl Cinnamic Aldehyde) is a synthetic fragrance with a jasmine-like floral scent. Used in perfumes and personal care products. One of the 26 EU mandatory fragrance allergens that must be individually declared on cosmetic labels. Potential skin sensitiser in sensitive individuals.',
    'alpha-isomethyl ionone': 'Alpha-Isomethyl Ionone is a synthetic fragrance compound with a violet and iris-like floral scent. Widely used in fine fragrance, personal care and household products. One of the 26 EU mandatory fragrance allergens. Can cause contact allergic dermatitis in sensitised individuals.',

    # ── Quaternary Ammonium Compounds ────────────────────────────────────────
    'behentrimonium methosulfate': 'Behentrimonium Methosulfate (BTMS) is a cationic conditioning agent derived from rapeseed oil, widely used in hair conditioners and detangling products. Compared to behentrimonium chloride, it has a more neutral pH, can be used in emulsifier blends (BTMS-50), and is considered milder and less irritating. Popular in natural and "clean" formulation. Safe at cosmetic use concentrations.',
    'cetrimonium bromide': 'Cetrimonium Bromide (CTAB) is a quaternary ammonium surfactant and preservative used in hair rinses and conditioners. Has similar conditioning properties to cetrimonium chloride. Also used as an antimicrobial in laboratory settings. EU restricts its use in cosmetics. Potential irritant at higher concentrations.',
    'guar hydroxypropyltrimonium chloride': 'Guar Hydroxypropyltrimonium Chloride is a cationic guar gum derivative — natural guar gum modified with a quaternary ammonium group. Used as a conditioning polymer in shampoos and conditioners to provide detangling and softness. Better biodegradable profile than fully synthetic cationic polymers. Generally well tolerated.',
    'quaternium-18': 'Quaternium-18 (Dimethyldioctadecyl Ammonium Chloride) is a quaternary ammonium conditioning compound used in hair care. Provides conditioning and anti-static effects. Similar environmental persistence concerns as other quats; generally safe at cosmetic use concentrations.',

    # ── Cosmetic Skin-Brightening and Active Ingredients ─────────────────────
    'tranexamic acid': 'Tranexamic Acid is an amino acid derivative (a lysine analogue) clinically used as a haemostatic drug at high doses. In dermatology and cosmetics, it is used at much lower concentrations (2–5%) as a skin-brightening and anti-melasma active. Clinical studies have shown effectiveness in reducing hyperpigmentation. At cosmetic concentrations, it does not carry the systemic procoagulant risks of the pharmaceutical form. Safe and well-tolerated topically.',
    'tetrahexyldecyl ascorbate': 'Tetrahexyldecyl Ascorbate (THD Ascorbate) is an oil-soluble, lipid-stable form of Vitamin C. Unlike water-soluble ascorbic acid, it penetrates the lipid-rich stratum corneum more effectively and is significantly more stable against oxidation. Converts to ascorbic acid once inside the skin. Used in anti-ageing and brightening serums at concentrations of 10–30%. Safe and well-tolerated.',
    'ascorbyl glucoside': 'Ascorbyl Glucoside is a water-soluble glycoside of Vitamin C produced by bonding ascorbic acid to glucose. More stable than ascorbic acid; enzymes in the skin cleave the glucose to release free ascorbic acid. Used in brightening and antioxidant skincare at 2–3%. Gentler than ascorbic acid; well-tolerated.',
    'ethyl ascorbic acid': 'Ethyl Ascorbic Acid (3-O-Ethyl Ascorbic Acid) is a stable, water-soluble Vitamin C derivative that is both more stable and potentially more potent than ascorbyl glucoside. Converts to ascorbic acid in the skin. Used at 0.5–3% in brightening serums. Safe and generally well-tolerated.',
    'kojic dipalmitate': 'Kojic Dipalmitate is a more stable, oil-soluble form of kojic acid — a natural tyrosinase inhibitor produced by Aspergillus fermentation of rice and sake. Inhibits melanin production for skin brightening. Less irritating than kojic acid itself. Safe for cosmetic use within approved concentrations.',
    'resveratrol': 'Resveratrol is a naturally occurring polyphenolic stilbenoid found in grape skin, red wine, blueberries and Japanese knotweed. A potent antioxidant with studied anti-inflammatory and anti-ageing properties in laboratory research. Used in premium skincare serums and supplements. Safe for topical and oral use; oral bioavailability is limited — topical delivery is more direct. The evidence for anti-ageing effects is promising but requires further human clinical validation.',
    'ferulic acid': 'Ferulic Acid is a natural hydroxycinnamic acid found in the cell walls of rice, wheat and oat bran. A potent antioxidant that acts as a photoprotectant and synergises strongly with Vitamins C and E in skincare (stabilising them and enhancing their antioxidant effect). Used in cosmetics as an antioxidant active and food-grade preservative. Safe; well-tolerated.',

    # ── Additional Functional Cosmetic Ingredients ────────────────────────────
    'caprylyl methicone': 'Caprylyl Methicone is a lightweight, low-viscosity silicone fluid with an organic (caprylyl) modification that makes it more skin-compatible and with a lower environmental persistence than cyclic silicones. Used for a smooth, non-greasy skin feel. Safe for topical cosmetic use.',
    'trimethylsilylamodimethicone': 'Trimethylsilylamodimethicone is a non-cyclic, trimethylsilyl-terminated amino-functional silicone. Used in hair care products for long-lasting conditioning, anti-frizz effects and shine. The non-cyclic structure means it does not share the EU restrictions placed on cyclic silicones (D4, D5). Generally safe.',
    'sodium phytate': 'Sodium Phytate is the sodium salt of phytic acid, a natural compound found in rice bran, sesame and other grains. Used in cosmetics as a chelating agent (sequestering trace metal ions that could degrade products) and as a mild skin-brightening ingredient. Safe natural alternative to synthetic chelators like EDTA.',
    'phytic acid': 'Phytic Acid is a naturally occurring organic acid (inositol hexaphosphoric acid) found in cereal brans, legumes and seeds. In cosmetics, it functions as a chelating agent (binds and inactivates trace metal ions) and as a gentle skin-brightening and exfoliating agent. Safe for cosmetic use.',
    'gluconolactone': 'Gluconolactone is a polyhydroxy acid (PHA) — a gentler, larger-molecular relative of AHAs (alpha-hydroxy acids) like glycolic acid. Provides mild exfoliation without significant irritation, making it suitable for sensitive and post-procedure skin. Also acts as a humectant and antioxidant chelator. Safe and well-tolerated.',
    'lactobionic acid': 'Lactobionic Acid is a polyhydroxy acid (PHA) derived from lactose. Like gluconolactone, it is a larger molecule that exfoliates more gently than AHAs. Additionally acts as a strong humectant and antioxidant through its metal-chelating properties. Well-tolerated by sensitive skin. Safe.',
    'mandelic acid': 'Mandelic Acid is an alpha-hydroxy acid (AHA) derived from bitter almonds. Its larger molecular size (compared to glycolic acid) means it penetrates the skin more slowly, resulting in a gentler exfoliating action with fewer side effects. Also has antibacterial properties, making it useful for acne-prone skin. Photosensitising — SPF protection recommended. Safe at cosmetic concentrations.',
    'propanediol': 'Propanediol (1,3-Propanediol) is a naturally derived glycol produced by fermenting corn sugars, used as a humectant and solvent in cosmetics. It is a sustainable alternative to petroleum-derived propylene glycol, with a gentler skin feel and minimal irritation potential. FDA GRAS status. Very safe and well-tolerated.',
    'caprylyl glycol': 'Caprylyl Glycol (1,2-Octanediol) is an 8-carbon diol used in cosmetics both as a humectant and a preservative booster. It has intrinsic antimicrobial activity against Gram-positive bacteria and Candida, allowing it to enhance the efficacy of preservative systems. Safe and generally well-tolerated at typical cosmetic concentrations.',
    'pentylene glycol': 'Pentylene Glycol (1,5-Pentanediol) is a multifunctional glycol used as a humectant, solvent and mild preservative booster in cosmetics. It has good skin compatibility, provides moisture retention and enhances the penetration of other actives. Generally well-tolerated. Often used in natural-oriented formulations.',
    'betaine': 'Betaine (Trimethylglycine) is a naturally occurring compound derived from sugar beet processing. Used in cosmetics as a humectant, anti-irritant and osmoprotectant — it helps protect the skin from environmental stressors. Also used in hair care to provide gentle conditioning and reduce the irritation potential of surfactants. Safe and well-tolerated.',
    'colloidal oatmeal': 'Colloidal Oatmeal is finely milled whole oat grain (Avena sativa) that has been processed to remain suspended in water. FDA-approved as an OTC skin protectant at 0.5–2%. Rich in avenanthramides (unique oat polyphenols with potent anti-inflammatory properties), beta-glucan and natural oils. Clinical evidence supports its use for atopic dermatitis (eczema), dry skin and skin barrier repair. Excellent tolerability; safe. Possible concern only for individuals with severe oat or wheat allergy via topical route.',
    'saccharide isomerate': 'Saccharide Isomerate (trade name PENTAVITIN) is a carbohydrate complex derived from corn. It is claimed to form lasting covalent bonds with skin keratins, providing long-duration hydration effects. Used in premium moisturisers. Generally safe and well-tolerated.',
    'trehalose': 'Trehalose is a naturally occurring disaccharide found in mushrooms, yeast, insects and resurrection plants (which use it to survive desiccation). Used in cosmetics as a humectant and cryoprotectant. Also used in some food products. Safe and well-tolerated.',

    # ── Isopropyl Alcohol ─────────────────────────────────────────────────────
    'isopropanol': 'Isopropanol (Isopropyl Alcohol / IPA / 2-Propanol) is a petroleum-derived secondary alcohol used as a solvent, antiseptic and astringent. Effective as a disinfectant at 60–70% concentrations. In cosmetics, used as a solvent or quick-drying agent, but frequent application is drying and can disrupt the skin barrier. Not suitable as a primary skincare ingredient for regular use.',

    # ── Ceramide Analogues ────────────────────────────────────────────────────
    'ceramide np': 'Ceramide NP (N-Palmitoyl Sphinganine) is the most abundant ceramide type in human stratum corneum, making up approximately 20% of total skin ceramides. Critical for maintaining the lamellar lipid barrier of the skin. Used in barrier-repair moisturisers for dry skin, eczema and aged skin. Safe and bioidentical to skin lipids.',
    'ceramide ap': 'Ceramide AP (N-Palmitoyldihydrosphingosine) is another important skin ceramide type. Works alongside ceramide NP and other ceramides to form the intercellular lipid matrix of the stratum corneum. Used in barrier-repair formulations. Safe.',
    'phytosphingosine': 'Phytosphingosine is a sphingoid base (the backbone component of ceramides) naturally found in yeast and skin. It has intrinsic anti-inflammatory and antimicrobial properties in addition to its role as a ceramide precursor. Used in acne-prone and sensitive skin formulations. Safe.',

    # ── Butylphenyl Methylpropional ───────────────────────────────────────────
    'lilial': 'Lilial (Butylphenyl Methylpropional / p-t-Bucinal) is a synthetic fragrance ingredient formerly used for its fresh, lily-like floral scent in numerous cosmetics and personal care products. It has been BANNED in the European Union since 1 March 2022, classified as a Category 1B reproductive toxicant under CLP Regulation — animal studies demonstrated adverse effects on fertility. Products containing Lilial cannot be placed on the EU market. Consumers should avoid any product still listing this ingredient.',

    # ══ Cosmetic Polymers / Film-formers ══════════════════════════════════════
    'polyethylene': 'Polyethylene (PE) is a synthetic thermoplastic polymer used in cosmetics as a texture modifier, thickener and emollient in anhydrous formulations like lipsticks, foundations and mascaras. High-molecular-weight polyethylene wax is safe for topical use. Note: low-molecular-weight PE microbeads have been banned in rinse-off products in many countries (UK, USA, EU) due to marine microplastic pollution — but the wax form used in leave-on cosmetics is different and not banned.',
    'polysilicone-11': 'Polysilicone-11 is a cross-linked dimethicone silicone elastomer used in long-wear makeup formulations (foundations, eye shadows, lipsticks) as a film-former and suspension agent. It provides a smooth, non-tacky film and excellent wear-resistance. Not absorbed through the skin; safe for topical use.',
    'nylon-12': 'Nylon-12 (Polyamide-12) is a synthetic polyamide polymer used as a texture agent and film-former in cosmetics including foundations, eyeshadows and mascara. It produces a smooth, soft-focus finish and improves long-wear properties. Safe for topical cosmetic use; not absorbed.',
    'methyl methacrylate crosspolymer': 'Methyl Methacrylate Crosspolymer is a cross-linked acrylic polymer used as a soft-focus agent, mattifying powder and film-former in foundations, primers and skincare products. Creates a blurring effect by scattering light. Safe for topical use; not absorbed.',

    # ══ Cosmetic Emollients / Esters ══════════════════════════════════════════
    'caprylic/capric triglyceride': 'Caprylic/Capric Triglyceride (CCT) is a light, non-greasy emollient derived from coconut oil by esterifying glycerol with caprylic (C8) and capric (C10) fatty acids. It is one of the most widely used cosmetic emollients — hypoallergenic, non-comedogenic, and exceptionally well-tolerated by all skin types including sensitive and acne-prone skin. Also functions as an excellent carrier oil for active ingredients. Safe.',
    'polyhydroxystearic acid': 'Polyhydroxystearic Acid (PHSA) is a branched, polymeric ester of 12-hydroxystearic acid used as an emulsifier and dispersing agent, particularly to stabilise inorganic UV filters (zinc oxide, titanium dioxide) in sunscreens and mineral makeup. It prevents nanoparticle clumping and ensures even distribution. Safe for topical cosmetic use.',
    'pentaerythrityl tetra-di-t-butyl hydroxyhydrocinnamate': 'Pentaerythrityl Tetra-di-t-butyl Hydroxyhydrocinnamate (trade name Irganox 1010) is a synthetic hindered phenol antioxidant used at trace levels in cosmetics to prevent oxidation of oils, fats and polymers during manufacturing and storage. It is not a skin-active ingredient — it protects the formula, not the skin. Safe at the trace concentrations used.',
    'tocopheryl acetate': 'Tocopheryl Acetate (Vitamin E Acetate) is the most widely used esterified form of Vitamin E in cosmetics. More stable against oxidation than tocopherol itself. It acts as an antioxidant, protects the skin lipid barrier from free-radical damage, and is used as a skin conditioner in moisturisers, sunscreens and anti-ageing products. Converts to free tocopherol on the skin. Safe and very well-tolerated.',
    'cholesterol': 'Cholesterol is a natural lipid found abundantly in the stratum corneum as a key component of the skin\'s lamellar lipid barrier (alongside ceramides and fatty acids in a roughly 1:1:1 ratio). In cosmetics, it is derived from animal or plant sources (lanolin-derived or from wool). Used in barrier-repair formulations for dry skin, eczema and aged skin. Safe; bioidentical to skin lipids.',

    # ══ Cosmetic Minerals / Clays ══════════════════════════════════════════════
    'mica': 'Mica is a group of naturally occurring phyllosilicate minerals (muscovite, phlogopite, lepidolite) that split into thin, shiny, reflective sheets. Widely used in makeup (eyeshadows, highlighters, foundations, lip products) for shimmer, sparkle and light-reflective effects. Safe for topical cosmetic use. The primary concern with mica is ethical rather than toxicological — large-scale mica mining in India (Jharkhand, Rajasthan) and Madagascar has been linked to child labour, and reputable brands now use responsibly sourced or synthetic mica.',
    'dicalcium phosphate': 'Dicalcium Phosphate (DCP) is a calcium phosphate mineral (CaHPO4) used in toothpaste as a mild polishing abrasive and in cosmetics as an opacifier and bulking agent. In food, it is used as a calcium supplement and leavening agent (E341). Safe and nutritionally beneficial as a calcium source.',
    'stearalkonium bentonite': 'Stearalkonium Bentonite is a clay mineral (bentonite) that has been organically modified with stearalkonium chloride (a quaternary ammonium salt) to become compatible with anhydrous (non-water) formulations. Used as a rheology modifier — it thickens and stabilises anhydrous cosmetic formulations such as foundations, lipsticks and eyeshadows, suspending pigments evenly. Safe for topical cosmetic use.',

    # ══ UV Filters / Sunscreen Actives ════════════════════════════════════════
    'ethylhexyl salicylate': 'Ethylhexyl Salicylate (Octyl Salicylate / 2-Ethylhexyl Salicylate) is an organic UVB-absorbing sunscreen active that absorbs UV radiation in the 295–315nm range. Used at concentrations up to 5% (EU) to protect skin from UVB-induced sunburn. Generally well-tolerated; low sensitisation risk. Some in-vitro endocrine activity detected at high concentrations but not considered clinically relevant at sunscreen-use levels. Safe and approved by EU, FDA (as Octyl Salicylate) and CDSCO.',
    'phenylbenzimidazole sulfonic acid': 'Phenylbenzimidazole Sulfonic Acid (Ensulizole / PBSA) is a water-soluble UVB sunscreen filter approved by the EU, FDA and many other regulatory bodies. Absorbs UVB radiation in the 290–320nm range. The water-soluble nature makes it suitable for lightweight, non-greasy sunscreen formulations. Safe at approved concentrations (up to 8% EU, 4% FDA).',
    'butyl methoxydibenzoylmethane': 'Butyl Methoxydibenzoylmethane (Avobenzone / Parsol 1789) is the most widely used broad-spectrum UVA filter, absorbing UVA1 radiation in the 320–400nm range. A key ingredient in most broad-spectrum sunscreens globally. Its main limitation is photostability — it degrades in sunlight when used alone. Combined with photostabilisers (Octocrylene, Tinosorb S) it remains effective. Safe at approved concentrations (up to 5% EU, 3% FDA). Some studies showed skin penetration and trace detection in blood — FDA has requested additional data, but current evidence does not indicate a safety concern.',
    'octocrylene food': 'Octocrylene is both a UVB/UVA2 sunscreen filter and a photostabiliser for unstable UV filters like Avobenzone. See the main "Octocrylene" entry for full details.',

    # ══ Cosmetic Surfactants / Emulsifiers ════════════════════════════════════
    'laureth-12': 'Laureth-12 is a non-ionic surfactant and emulsifier produced by ethoxylating lauryl alcohol with 12 ethylene oxide units. Like all ethoxylated ingredients, manufacturing may leave trace amounts of 1,4-dioxane (IARC Group 2B possible carcinogen) — reputable manufacturers vacuum-strip this contaminant to well below safe limits. Used in cleansers and emulsions. Safe within approved limits; the 1,4-dioxane concern is a manufacturing quality issue.',
    'steareth-21': 'Steareth-21 is a non-ionic emulsifier produced by ethoxylating stearyl alcohol with 21 ethylene oxide units. Used as an O/W emulsifier in lotions, creams and conditioners. Ethoxylation may leave trace 1,4-dioxane (IARC Group 2B) — manufacturers control this via vacuum stripping. Safe within approved limits.',
    'steareth-2': 'Steareth-2 is a non-ionic emulsifier produced by ethoxylating stearyl alcohol with 2 ethylene oxide units. Used alongside Steareth-21 in classic emulsion systems. Same trace 1,4-dioxane concern as other ethoxylates. Safe within approved limits.',
    'sodium lauroyl lactylate': 'Sodium Lauroyl Lactylate (SLL) is a mild, biodegradable anionic surfactant and emulsifier derived from coconut-sourced lauric acid and lactic acid. Used in gentle cleansers, moisturisers and hair care. Excellent skin tolerability; milder than SLS. Safe.',

    # ══ Conditioning / Quat Agents ════════════════════════════════════════════
    'linoleamidopropyl pg-dimonium chloride phosphate': 'Linoleamidopropyl PG-Dimonium Chloride Phosphate is a quaternary ammonium conditioning agent derived from linoleic acid (an omega-6 fatty acid). Used as an antistatic conditioning agent in hair care and skincare products. The quaternary ammonium group improves hair manageability and reduces static. Safe at cosmetic-use concentrations; biodegradable.',

    # ══ Hyaluronic Acid Variants ══════════════════════════════════════════════
    'sodium acetylated hyaluronate': 'Sodium Acetylated Hyaluronate is a modified form of sodium hyaluronate in which acetyl groups are attached to the hyaluronic acid polymer. The acetylation makes it more lipophilic (fat-attracting), improving its affinity for the skin surface and enabling longer-lasting moisture retention compared to standard sodium hyaluronate. Safe and very well-tolerated.',
    'sodium hyaluronate crosspolymer': 'Sodium Hyaluronate Crosspolymer is a cross-linked, high-molecular-weight form of sodium hyaluronate. The cross-linking increases its molecular size so it remains on the skin surface, providing a long-lasting film that continuously releases moisture. Used in premium anti-ageing and hydrating formulations. Safe.',
    'hydrolyzed sodium hyaluronate': 'Hydrolyzed Sodium Hyaluronate consists of very small fragments of sodium hyaluronate produced by enzymatic hydrolysis. The small molecular size (typically under 10 kDa) allows deeper penetration into the upper layers of the stratum corneum compared to high-molecular-weight HA. Used in serums and moisturisers for deeper hydration. Safe.',

    # ══ Cosmetic Polymers / Rheology Modifiers ════════════════════════════════
    'acrylates/c10-30 alkyl acrylate crosspolymer': 'Acrylates/C10-30 Alkyl Acrylate Crosspolymer is a synthetic thickener and stabiliser related to Carbomer but with added long-chain alkyl groups, making it more effective at stabilising emulsions with oil droplets. Widely used in sunscreens, moisturisers and gel formulations. Safe for topical use.',
    'propylene carbonate': 'Propylene Carbonate is an organic solvent and plasticiser used in cosmetics to dissolve and stabilise ingredients, improve spreadability and act as a coupling agent. Also used in pharmaceutical formulations. Safe at cosmetic-use concentrations; good skin tolerability.',

    # ══ Cosmetic Colourants / Pigments ════════════════════════════════════════
    'red 7 lake': 'Red 7 Lake (D&C Red 7 Lake / CI 15850:1 / Lithol Rubine BCA) is a synthetic azo dye lake used in cosmetics (lipsticks, blushers, eyeshadows) for its bright, vivid red-pink colour. "Lake" pigments are precipitated onto a substrate (usually aluminium), making them more opaque and bleed-resistant than their soluble counterparts. EU and FDA approved for cosmetic use within specified limits. Safe for external cosmetic use.',
    'red 6': 'Red 6 (D&C Red 6 / CI 15850 / Lithol Rubine B) is a synthetic azo dye used as a cosmetic colorant in lipsticks, blushers and other makeup products. The non-lake (soluble salt) form. FDA approved for cosmetic use; EU permitted in cosmetics. Safe for external cosmetic application.',
    'red 28 lake': 'Red 28 Lake (D&C Red 28 Lake / CI 45410 / Phloxine B Lake) is a synthetic xanthene dye lake used as a cosmetic colorant in lipsticks and other makeup. Approved by FDA for cosmetic use (not for use around the eyes in the US). EU permitted at specified limits. Generally safe for topical cosmetic use; some photosensitisation concern at high concentrations.',
    'ci 15850': 'CI 15850 is the Colour Index number for Lithol Rubine, a synthetic azo dye. Used in cosmetics (Red 6, Red 7 and their lake forms) for red-pink shades in lipsticks and blushers. EU and FDA approved for cosmetic use.',
    'ci 45410': 'CI 45410 is the Colour Index number for Phloxine B (Red 28), a synthetic xanthene dye used as a cosmetic colorant. FDA approved for lipsticks; EU permitted in cosmetics at specified limits.',
    'ci 77491': 'CI 77491 is the Colour Index number for Red Iron Oxide (ferric oxide, Fe2O3). A natural inorganic mineral pigment providing red-brown shades in foundations, eyeshadows and lipsticks. Very safe; chemically inert; approved globally.',
    'ci 77492': 'CI 77492 is the Colour Index number for Yellow Iron Oxide (goethite, FeOOH). A natural inorganic mineral pigment providing yellow-gold shades in foundations and makeup. Very safe; chemically inert; approved globally.',

    # ══ Bis-PEG Silicone Compounds ════════════════════════════════════════════
    'bis-peg-12 dimethicone beeswax': 'Bis-PEG-12 Dimethicone Beeswax is a PEG-modified dimethicone-based wax used as an emulsifier and skin conditioner in anhydrous cosmetic formulations. The PEG modification makes the silicone wax water-dispersible. Contains a PEG group (ethylene oxide-based) — ethoxylation may introduce trace 1,4-dioxane (IARC Group 2B possible carcinogen); reputable manufacturers minimise this. Also contains a beeswax-derived component — not suitable for strict vegans. Safe at cosmetic-use concentrations within approved limits.',

    # ══ Ceramide EOP ══════════════════════════════════════════════════════════
    'ceramide eop': 'Ceramide EOP (Ceramide 1 / N-[(1R,2R)-2-Hydroxy-1-(hydroxymethyl)heptadecyl]-... ester) is one of the nine ceramide types identified in human skin. It is unique among ceramides for having an ester-linked omega-hydroxy fatty acid — it forms the structural backbone of the lamellar lipid sheets in the stratum corneum. Critically important for maintaining the skin\'s water-permeability barrier. Used in barrier-repair and eczema-care formulations alongside other ceramides (NP, AP). Safe; bioidentical to skin lipids.',

    # ══ Food Additive E Numbers / INS Numbers (comprehensive) ══════════════════

    # ── Colours ──────────────────────────────────────────────────────────────
    'curcumin': 'Curcumin (E100/INS 100) is the natural yellow pigment from turmeric. Safe and anti-inflammatory. FSSAI, EU and Codex approved.',
    'e100': 'E100 is the EU/INS code for Curcumin. Natural turmeric yellow food colour. Safe and beneficial.',
    'annatto': 'Annatto (E160b/INS 160b) is a natural orange-yellow pigment from achiote seeds, used in cheeses, margarine and snacks. Safe; rare allergy in aspirin-sensitive individuals.',
    'e160b': 'E160b is the EU/INS code for Annatto (Bixin/Norbixin). Natural orange-red colour. Safe.',
    'paprika extract': 'Paprika Extract (E160c/INS 160c) is a natural red-orange carotenoid from red capsicum peppers. Safe.',
    'e160c': 'E160c is the EU/INS code for Paprika Extract. Natural red-orange colour from capsicum. Safe.',
    'lycopene': 'Lycopene (E160d/INS 160d) is the natural red carotenoid from tomatoes with antioxidant benefits. Safe.',
    'e160d': 'E160d is the EU/INS code for Lycopene. Natural red colour from tomatoes. Safe.',
    'lutein': 'Lutein (E161b/INS 161b) is a natural yellow carotenoid from marigold flowers. Associated with eye health. Safe.',
    'e161b': 'E161b is the EU/INS code for Lutein. Natural yellow colour with eye health benefits. Safe.',
    'beetroot red': 'Beetroot Red / Betanin (E162/INS 162) is the natural red-purple pigment from red beetroot. Safe; harmless pink urine (beeturia) possible.',
    'betanin': 'Betanin (E162/INS 162) is the red pigment from beetroot used as a natural food colour. Safe.',
    'e162': 'E162 is the EU/INS code for Beetroot Red (Betanin). Natural red-purple colour. Safe.',
    'anthocyanins': 'Anthocyanins (E163/INS 163) are natural red-purple-blue pigments from berries, grapes and red cabbage. Rich in antioxidants. Safe.',
    'e163': 'E163 is the EU/INS code for Anthocyanins. Natural plant pigments from berries. Safe.',
    'calcium carbonate food': 'Calcium Carbonate (E170/INS 170) is used as a white food colour, anti-caking agent and calcium supplement. Safe and nutritionally beneficial.',
    'e170': 'E170 is the EU/INS code for Calcium Carbonate. White colour and calcium supplement. Safe.',
    'iron oxides': 'Iron Oxides (E172/INS 172) are mineral pigments producing red, yellow, brown and black food colours. Safe at approved levels.',
    'e172': 'E172 is the EU/INS code for Iron Oxides and Hydroxides. Mineral food colours. Safe at approved levels.',
    'e174': 'E174 is the EU code for Silver. Metallic surface decoration on confectionery. Chemically inert; safe in decorative amounts.',
    'e175': 'E175 is the EU code for Gold. Metallic food decoration. Chemically inert; safe.',
    'e140': 'E140 is the EU/INS code for Chlorophylls. Natural green plant pigments. Safe.',
    'e141': 'E141 is the EU/INS code for Copper Complexes of Chlorophylls. Stabilised natural green colours. Safe at permitted levels.',
    'e150a': 'E150a is Plain Caramel (Class I). Produced without ammonia or sulphites. Used in spirits. Safest caramel class.',
    'e150b': 'E150b is Caustic Sulphite Caramel (Class II). Used in cognac and sherry. Safe.',
    'e150c': 'E150c is Ammonia Caramel (Class III). Used in beer and sauces. Safe at typical food levels.',

    # ── Acidity regulators ─────────────────────────────────────────────────
    'acetic acid': 'Acetic Acid (E260/INS 260) is the acid in vinegar. Naturally produced by fermentation. Safe acidity regulator and preservative in pickles, sauces and condiments.',
    'e260': 'E260 is the EU/INS code for Acetic Acid (vinegar acid). Safe acidity regulator.',
    'potassium acetate': 'Potassium Acetate (E261/INS 261) is the potassium salt of acetic acid. Acidity regulator and low-sodium salt substitute. Safe.',
    'e261': 'E261 is the EU/INS code for Potassium Acetate. Acidity regulator and salt substitute. Safe.',
    'sodium acetate': 'Sodium Acetate (E262/INS 262) is the sodium salt of acetic acid. Acidity regulator; gives salt-and-vinegar crisps their flavour. Safe.',
    'e262': 'E262 is the EU/INS code for Sodium Acetates. Acidity regulator. Safe.',
    'e270': 'E270 is the EU/INS code for Lactic Acid. Natural fermentation acid found in yoghurt and pickles. Safe.',
    'propionic acid': 'Propionic Acid (E280/INS 280) is a short-chain fatty acid naturally in Swiss cheese. Used as a mould inhibitor in bread. Safe -- metabolised as a normal fatty acid.',
    'e280': 'E280 is the EU/INS code for Propionic Acid. Natural mould inhibitor in bread. Safe.',
    'sodium propionate': 'Sodium Propionate (E281/INS 281) is the sodium salt of propionic acid. Mould inhibitor in bakery products. Safe.',
    'e281': 'E281 is the EU/INS code for Sodium Propionate. Mould inhibitor in baked goods. Safe.',
    'calcium propionate': 'Calcium Propionate (E282/INS 282) is the most widely used bread preservative. Inhibits mould and adds dietary calcium. Safe.',
    'e282': 'E282 is the EU/INS code for Calcium Propionate. Most widely used bread mould inhibitor; adds calcium. Safe.',
    'potassium propionate': 'Potassium Propionate (E283/INS 283) is the potassium salt of propionic acid. Mould inhibitor in baked goods. Safe.',
    'e283': 'E283 is the EU/INS code for Potassium Propionate. Mould inhibitor in baked goods. Safe.',
    'e290': 'E290 is the EU/INS code for Carbon Dioxide. Used to carbonate drinks and preserve freshness. Safe -- the gas we exhale.',
    'malic acid': 'Malic Acid (E296/INS 296) is the natural tart acid from apples and grapes. Used as an acidity regulator in beverages and confectionery. Safe.',
    'e296': 'E296 is the EU/INS code for Malic Acid. Natural apple acid; acidity regulator. Safe.',
    'fumaric acid': 'Fumaric Acid (E297/INS 297) is a naturally occurring acid from the Krebs cycle. Used as an acidity regulator and raising acid. Safe.',
    'e297': 'E297 is the EU/INS code for Fumaric Acid. Natural acidity regulator. Safe.',

    # ── Antioxidants (E300-E329) ─────────────────────────────────────────
    'e300': 'E300 is the EU/INS code for Ascorbic Acid (Vitamin C). Essential vitamin and food antioxidant. Safe and nutritionally beneficial.',
    'sodium ascorbate': 'Sodium Ascorbate (E301/INS 301) is a non-acidic form of Vitamin C. Antioxidant in processed meats and beverages. Safe.',
    'e301': 'E301 is the EU/INS code for Sodium Ascorbate. Non-acidic Vitamin C antioxidant. Safe.',
    'calcium ascorbate': 'Calcium Ascorbate (E302/INS 302) is the calcium salt of Vitamin C. Antioxidant and calcium supplement. Safe.',
    'e302': 'E302 is the EU/INS code for Calcium Ascorbate. Vitamin C and calcium supplement. Safe.',
    'ascorbyl palmitate': 'Ascorbyl Palmitate (E304/INS 304) is a fat-soluble Vitamin C ester. Antioxidant in oils and fats. Safe.',
    'e304': 'E304 is the EU/INS code for Ascorbyl Palmitate. Fat-soluble Vitamin C antioxidant. Safe.',
    'e306': 'E306 is the EU/INS code for Tocopherol-rich extract (Vitamin E). Natural antioxidant. Safe and nutritionally beneficial.',
    'e307': 'E307 is the EU/INS code for Alpha-Tocopherol (most active Vitamin E form). Safe.',
    'e308': 'E308 is the EU/INS code for Gamma-Tocopherol (Vitamin E form). Safe.',
    'e309': 'E309 is the EU/INS code for Delta-Tocopherol (Vitamin E form). Safe.',
    'propyl gallate': 'Propyl Gallate (E310/INS 310) is a synthetic antioxidant in fats and oils. Associated with tumour promotion in animal studies; banned in baby foods in the EU; under EFSA review. Approved with quantity limits for general food use.',
    'e310': 'E310 is the EU/INS code for Propyl Gallate. Synthetic antioxidant under regulatory review; banned in baby foods in EU.',
    'octyl gallate': 'Octyl Gallate (E311/INS 311) is a synthetic gallate antioxidant in edible fats. Approved with quantity limits.',
    'e311': 'E311 is the EU/INS code for Octyl Gallate. Synthetic antioxidant. Approved with limits.',
    'dodecyl gallate': 'Dodecyl Gallate (E312/INS 312) is a synthetic gallate antioxidant in edible fats. Approved with quantity limits.',
    'e312': 'E312 is the EU/INS code for Dodecyl Gallate. Synthetic antioxidant. Approved with limits.',
    'sodium lactate': 'Sodium Lactate (E325/INS 325) is the sodium salt of lactic acid. Humectant and low-sodium salt substitute. Safe.',
    'e325': 'E325 is the EU/INS code for Sodium Lactate. Humectant and salt substitute. Safe.',
    'potassium lactate': 'Potassium Lactate (E326/INS 326) is the potassium salt of lactic acid. Antimicrobial in processed meats. Safe.',
    'e326': 'E326 is the EU/INS code for Potassium Lactate. Antimicrobial in processed meats. Safe.',
    'calcium lactate': 'Calcium Lactate (E327/INS 327) is the calcium salt of lactic acid. Firming agent and calcium supplement. Safe.',
    'e327': 'E327 is the EU/INS code for Calcium Lactate. Firming agent and calcium source. Safe.',
    'tartaric acid': 'Tartaric Acid (E334/INS 334) is the natural acid from grapes, responsible for wine tartness. Used as an acidity regulator in baked goods and confectionery. Safe.',
    'e334': 'E334 is the EU/INS code for Tartaric Acid. Natural grape acid. Safe.',
    'e335': 'E335 is the EU/INS code for Sodium Tartrates. Acidity regulators. Safe.',
    'e336': 'E336 is the EU/INS code for Potassium Tartrates (Cream of Tartar). Classic baking ingredient. Safe.',
    'e337': 'E337 is the EU/INS code for Sodium Potassium Tartrate (Rochelle Salt). Acidity regulator. Safe.',
    'e340': 'E340 is the EU/INS code for Potassium Phosphates. Acidity regulators. Safe at approved levels.',
    'calcium phosphate': 'Calcium Phosphates (E341/INS 341) are used as raising agents and calcium supplements in baked goods and fortified foods. Safe.',
    'e341': 'E341 is the EU/INS code for Calcium Phosphates. Raising agents and calcium supplements. Safe.',
    'adipic acid': 'Adipic Acid (E355/INS 355) is an organic dicarboxylic acid used as an acidity regulator and raising acid. Safe.',
    'e355': 'E355 is the EU/INS code for Adipic Acid. Acidity regulator and raising acid. Safe.',
    'succinic acid': 'Succinic Acid (E363/INS 363) is a naturally occurring acid from fermentation. Acidity regulator. Safe.',
    'e363': 'E363 is the EU/INS code for Succinic Acid. Natural acidity regulator. Safe.',
    'gluconic acid': 'Gluconic Acid (E574/INS 574) is a natural acid from fermentation found in honey and wine. Safe.',
    'e574': 'E574 is the EU/INS code for Gluconic Acid. Natural fermentation acid. Safe.',
    'glucono delta-lactone': 'Glucono Delta-Lactone (GDL/E575/INS 575) is a natural mild acidifier used in tofu, cheese and baked goods. Safe.',
    'e575': 'E575 is the EU/INS code for Glucono Delta-Lactone (GDL). Natural mild acidifier. Safe.',
    'sodium gluconate': 'Sodium Gluconate (E576/INS 576) is the sodium salt of gluconic acid. Sequestrant and acidity regulator. Safe.',
    'e576': 'E576 is the EU/INS code for Sodium Gluconate. Sequestrant. Safe.',
    'potassium gluconate': 'Potassium Gluconate (E577/INS 577) is the potassium salt of gluconic acid. Potassium supplement. Safe.',
    'e577': 'E577 is the EU/INS code for Potassium Gluconate. Potassium supplement. Safe.',
    'calcium gluconate': 'Calcium Gluconate (E578/INS 578) is the calcium salt of gluconic acid. Calcium supplement. Safe.',
    'e578': 'E578 is the EU/INS code for Calcium Gluconate. Calcium supplement. Safe.',
    'ferrous gluconate': 'Ferrous Gluconate (E579/INS 579) is used to colour black olives and as an iron supplement. Safe.',
    'e579': 'E579 is the EU/INS code for Ferrous Gluconate. Iron source and colour fixative. Safe.',

    # ── Emulsifiers / Hydrocolloids (E400-E499) ──────────────────────────
    'alginic acid': 'Alginic Acid (E400/INS 400) is a natural polysaccharide from brown seaweed. Thickener and gelling agent. Safe; dietary fibre.',
    'e400': 'E400 is the EU/INS code for Alginic Acid. Natural seaweed thickener. Safe.',
    'sodium alginate': 'Sodium Alginate (E401/INS 401) is the most widely used alginate from brown seaweed. Gelling agent in ice cream, salad dressings and molecular gastronomy. Safe; dietary fibre.',
    'e401': 'E401 is the EU/INS code for Sodium Alginate. Widely used seaweed gelling agent. Safe.',
    'potassium alginate': 'Potassium Alginate (E402/INS 402) is the potassium salt of alginic acid. Seaweed thickener. Safe.',
    'e402': 'E402 is the EU/INS code for Potassium Alginate. Seaweed thickener. Safe.',
    'e403': 'E403 is the EU/INS code for Ammonium Alginate. Seaweed thickener. Safe.',
    'calcium alginate': 'Calcium Alginate (E404/INS 404) forms thermo-irreversible gels from seaweed. Used in food and wound dressings. Safe.',
    'e404': 'E404 is the EU/INS code for Calcium Alginate. Natural seaweed gel-former. Safe.',
    'propylene glycol alginate': 'Propylene Glycol Alginate (E405/INS 405) is an acid-stable alginate ester used in salad dressings and beer foam. Safe at approved levels.',
    'e405': 'E405 is the EU/INS code for Propylene Glycol Alginate. Acid-stable seaweed gum. Safe.',
    'agar': 'Agar (E406/INS 406, Agar-Agar) is a natural polysaccharide from red algae. The vegetarian/vegan alternative to gelatin. Forms firm, clear gels. Safe; dietary fibre.',
    'e406': 'E406 is the EU/INS code for Agar (Agar-Agar). Natural red algae gelling agent. Vegetarian gelatin. Safe.',
    'locust bean gum': 'Locust Bean Gum (E410/INS 410, Carob Bean Gum) is a natural polysaccharide from carob seeds. Thickener in ice cream and dairy. Safe; dietary fibre.',
    'e410': 'E410 is the EU/INS code for Locust Bean Gum (Carob Gum). Natural seed thickener. Safe.',
    'tragacanth': 'Tragacanth (E413/INS 413) is a natural gum from Astragalus shrubs. One of the oldest food gums; used in confectionery. Safe.',
    'e413': 'E413 is the EU/INS code for Tragacanth. Natural plant gum thickener. Safe.',
    'gum arabic': 'Gum Arabic (E414/INS 414, Acacia Gum) is a natural gum from acacia trees of Africa. The world\'s most widely used food gum. Safe; prebiotic dietary fibre.',
    'acacia gum': 'Acacia Gum (E414/INS 414, Gum Arabic) from acacia trees is the world\'s most widely used food gum. Safe; prebiotic.',
    'e414': 'E414 is the EU/INS code for Gum Arabic (Acacia Gum). World\'s most used food gum. Safe.',
    'karaya gum': 'Karaya Gum (E416/INS 416) is a natural gum from Indian Sterculia trees. Thickener and stabiliser. Safe; rare sensitivity possible.',
    'e416': 'E416 is the EU/INS code for Karaya Gum. Indian plant gum. Safe.',
    'tara gum': 'Tara Gum (E417/INS 417) is a natural polysaccharide from tara plant seeds. Thickener. Safe.',
    'e417': 'E417 is the EU/INS code for Tara Gum. Natural seed gum. Safe.',
    'gellan gum': 'Gellan Gum (E418/INS 418) is a polysaccharide from bacterial fermentation. Gelling agent in plant-based milks and confectionery. Safe.',
    'e418': 'E418 is the EU/INS code for Gellan Gum. Microbial gelling agent. Safe.',
    'e420': 'E420 is the EU/INS code for Sorbitol. Sugar alcohol sweetener from fruits; laxative effects at >50g/day; label warning required.',
    'e421': 'E421 is the EU/INS code for Mannitol. Natural sugar alcohol; laxative effects; label warning required.',
    'e422': 'E422 is the EU/INS code for Glycerol (Glycerine). Natural humectant from fats. Safe.',
    'konjac': 'Konjac (E425/INS 425) is a polysaccharide from the konjac plant. Rich in glucomannan fibre with cholesterol-lowering benefits. EU restricts certain firm jelly formats for children due to choking risk.',
    'e425': 'E425 is the EU/INS code for Konjac (Konjac Gum). High-fibre gelling agent; EU restricts certain children\'s jelly formats.',
    'e440': 'E440 is the EU/INS code for Pectins. Natural gelling agent from citrus peel. Safe; soluble dietary fibre.',
    'e441': 'E441 is the EU/INS code for Gelatin. Animal-derived gelling protein. Not suitable for vegetarians, vegans or halal/kosher.',
    'ammonium phosphatides': 'Ammonium Phosphatides (E442/INS 442) are emulsifiers from vegetable oils used in chocolate to reduce viscosity. Safe.',
    'e442': 'E442 is the EU/INS code for Ammonium Phosphatides. Chocolate emulsifier. Safe.',
    'sucrose esters': 'Sucrose Esters of Fatty Acids (E473/INS 473) are emulsifiers from sucrose and fatty acids. Used in baked goods and dairy. Safe.',
    'e473': 'E473 is the EU/INS code for Sucrose Esters of Fatty Acids. Emulsifiers. Safe.',
    'e475': 'E475 is the EU/INS code for Polyglycerol Esters of Fatty Acids. Emulsifiers in confectionery. Safe.',
    'polysorbate 20': 'Polysorbate 20 (E432/INS 432) is a non-ionic emulsifier in food and cosmetics. Ethoxylation may introduce trace 1,4-dioxane (IARC Group 2B). Safe within approved limits.',
    'e432': 'E432 is the EU/INS code for Polysorbate 20. Non-ionic emulsifier; trace 1,4-dioxane possible from ethoxylation. Safe within limits.',
    'polysorbate 80': 'Polysorbate 80 (E433/INS 433) is a widely used non-ionic emulsifier in food, vaccines and cosmetics. Ethoxylation may introduce trace 1,4-dioxane. Safe within approved limits.',
    'e433': 'E433 is the EU/INS code for Polysorbate 80. Widely used emulsifier; trace 1,4-dioxane possible. Safe within limits.',
    'polysorbate 60': 'Polysorbate 60 (E435/INS 435) is a non-ionic emulsifier in baked goods and whipped toppings. Safe within approved limits.',
    'e435': 'E435 is the EU/INS code for Polysorbate 60. Emulsifier in baked goods. Safe within limits.',
    'polysorbate 65': 'Polysorbate 65 (E436/INS 436) is an emulsifier in ice cream and chocolate coatings. Safe within approved limits.',
    'e436': 'E436 is the EU/INS code for Polysorbate 65. Emulsifier. Safe within limits.',
    'e460': 'E460 is the EU/INS code for Microcrystalline Cellulose. Insoluble dietary fibre; anti-caking agent. Safe.',
    'e461': 'E461 is the EU/INS code for Methyl Cellulose. Heat-set modified cellulose in plant-based burgers. Safe.',
    'e464': 'E464 is the EU/INS code for Hydroxypropyl Methyl Cellulose (HPMC). Used in vegetarian capsules and gluten-free baking. Safe.',
    'datem': 'DATEM (E472e/INS 472e) is a highly effective bread dough emulsifier. Key ingredient in industrial baking. Safe.',
    'e472e': 'E472e is the EU/INS code for DATEM. Key bread dough emulsifier. Safe.',
    'sodium stearoyl lactylate': 'Sodium Stearoyl Lactylate (SSL/E481/INS 481) is a bread emulsifier that strengthens gluten and extends shelf life. Safe.',
    'e481': 'E481 is the EU/INS code for Sodium Stearoyl Lactylate (SSL). Key bread emulsifier. Safe.',
    'calcium stearoyl lactylate': 'Calcium Stearoyl Lactylate (CSL/E482/INS 482) is a bread emulsifier and dough conditioner. Safe.',
    'e482': 'E482 is the EU/INS code for Calcium Stearoyl Lactylate (CSL). Bread emulsifier. Safe.',
    'e491': 'E491 is the EU/INS code for Sorbitan Monostearate (Span 60). Emulsifier. Safe.',
    'e492': 'E492 is the EU/INS code for Sorbitan Tristearate. Emulsifier. Safe.',
    'e493': 'E493 is the EU/INS code for Sorbitan Monolaurate (Span 20). Emulsifier. Safe.',
    'e494': 'E494 is the EU/INS code for Sorbitan Monooleate. Emulsifier. Safe.',
    'e495': 'E495 is the EU/INS code for Sorbitan Monopalmitate. Emulsifier. Safe.',
    'diphosphates': 'Diphosphates (E450/INS 450, Pyrophosphates) are emulsifying salts in processed cheese and leavening agents in baking. Safe at approved levels.',
    'e450': 'E450 is the EU/INS code for Diphosphates (Pyrophosphates). Emulsifying salts in processed cheese. Safe at approved levels.',
    'e451': 'E451 is the EU/INS code for Triphosphates. Moisture-retaining agent in processed meats. Safe.',
    'e452': 'E452 is the EU/INS code for Polyphosphates. Emulsifying salts. Safe.',

    # ── Raising agents / minerals (E500-E599) ────────────────────────────
    'e500': 'E500 is the EU/INS code for Sodium Carbonates (including Baking Soda). Most widely used raising agent. Safe.',
    'sodium bicarbonate': 'Sodium Bicarbonate (Baking Soda/E500ii) is the most widely used leavening agent. Reacts with acids to release CO2 for rising. Safe.',
    'e501': 'E501 is the EU/INS code for Potassium Carbonates. Raising agent in cocoa and noodles. Safe.',
    'ammonium carbonate': 'Ammonium Carbonate (E503/INS 503, Bakers\' Ammonia) is a traditional raising agent for thin biscuits. Ammonia fully evaporates during baking. Safe.',
    'e503': 'E503 is the EU/INS code for Ammonium Carbonates. Traditional raising agent. Ammonia bakes out. Safe.',
    'magnesium carbonate': 'Magnesium Carbonate (E504/INS 504) is used as an anti-caking agent. Provides dietary magnesium. Safe.',
    'e504': 'E504 is the EU/INS code for Magnesium Carbonates. Anti-caking agent; provides magnesium. Safe.',
    'potassium chloride food': 'Potassium Chloride (E508/INS 508) is a low-sodium salt substitute and firming agent in tofu and vegetables. Provides dietary potassium. Safe.',
    'e508': 'E508 is the EU/INS code for Potassium Chloride. Low-sodium salt substitute. Safe.',
    'calcium chloride food': 'Calcium Chloride (E509/INS 509) is a firming agent in tofu, canned vegetables and cheese. Provides dietary calcium. Safe.',
    'e509': 'E509 is the EU/INS code for Calcium Chloride. Firming agent in tofu and vegetables. Safe.',
    'magnesium chloride food': 'Magnesium Chloride (E511/INS 511, Nigari) is the traditional Japanese tofu coagulant. Provides dietary magnesium. Safe.',
    'e511': 'E511 is the EU/INS code for Magnesium Chloride (Nigari). Traditional tofu coagulant. Safe.',
    'calcium sulphate food': 'Calcium Sulphate (E516/INS 516, food-grade gypsum) is a tofu coagulant and firming agent. Provides dietary calcium. Safe.',
    'e516': 'E516 is the EU/INS code for Calcium Sulphate (food-grade gypsum). Tofu coagulant. Safe.',
    'e524': 'E524 is the EU/INS code for Sodium Hydroxide (Lye). Processing aid for pretzels and olives; neutralised in final product. Safe.',
    'e525': 'E525 is the EU/INS code for Potassium Hydroxide. Processing aid in cocoa; neutralised in final product. Safe.',
    'e526': 'E526 is the EU/INS code for Calcium Hydroxide (Slaked Lime). Used in traditional nixtamalisation of corn; provides calcium. Safe.',
    'e530': 'E530 is the EU/INS code for Magnesium Oxide. Anti-caking agent; provides magnesium. Safe.',
    'silicon dioxide food': 'Silicon Dioxide (E551/INS 551, Amorphous Silica) is the most widely used anti-caking agent in powdered foods, salt and spices. Not absorbed by the body. Safe.',
    'e551': 'E551 is the EU/INS code for Silicon Dioxide (Amorphous Silica). Most widely used anti-caking agent. Not absorbed; safe.',
    'e552': 'E552 is the EU/INS code for Calcium Silicate. Anti-caking agent. Safe.',
    'e553a': 'E553a is the EU/INS code for Magnesium Silicates. Anti-caking agent. Safe.',
    'e572': 'E572 is the EU/INS code for Magnesium Stearate. Anti-caking agent in supplements. Safe.',
    'sodium ferrocyanide': 'Sodium Ferrocyanide (E535/INS 535) prevents table salt from clumping. Despite the name, the cyanide is firmly bound to iron and not released at food-use conditions. Safe in the tiny concentrations used in salt.',
    'e535': 'E535 is the EU/INS code for Sodium Ferrocyanide. Anti-caking agent in salt. Cyanide firmly bound -- safe at approved levels.',
    'e536': 'E536 is the EU/INS code for Potassium Ferrocyanide. Anti-caking agent in salt. Stable; safe.',
    'e558': 'E558 is the EU/INS code for Bentonite. Natural clay used to clarify wine; filtered out. Safe.',
    'e559': 'E559 is the EU/INS code for Kaolin (China Clay). Anti-caking agent. Safe.',

    # ── Flavour enhancers (E620-E650) ────────────────────────────────────
    'glutamic acid food': 'Glutamic Acid (E620/INS 620) is the naturally occurring amino acid responsible for umami taste in meat, cheese, tomatoes and mushrooms. Safe -- one of the most abundant amino acids in the diet.',
    'e620': 'E620 is the EU/INS code for Glutamic Acid. Natural amino acid responsible for umami taste. Safe.',
    'e622': 'E622 is the EU/INS code for Monopotassium Glutamate. Umami flavour enhancer. Safe.',
    'e623': 'E623 is the EU/INS code for Calcium Diglutamate. Umami flavour enhancer and calcium source. Safe.',
    'e624': 'E624 is the EU/INS code for Monoammonium Glutamate. Umami flavour enhancer. Safe.',
    'e625': 'E625 is the EU/INS code for Magnesium Diglutamate. Umami flavour enhancer. Safe.',
    'guanylic acid': 'Guanylic Acid (E626/INS 626) is a nucleotide from dried mushrooms and fish that amplifies umami. High purine content -- avoid with gout. Safe for most.',
    'e626': 'E626 is the EU/INS code for Guanylic Acid. Nucleotide umami enhancer; high purine -- avoid with gout.',
    'e628': 'E628 is the EU/INS code for Dipotassium Guanylate. Nucleotide flavour enhancer; avoid with gout.',
    'e629': 'E629 is the EU/INS code for Calcium Guanylate. Nucleotide flavour enhancer; avoid with gout.',
    'inosinic acid': 'Inosinic Acid (E630/INS 630) is a nucleotide from meat and fish. Umami taste enhancer. High purine -- avoid with gout. Safe for most.',
    'e630': 'E630 is the EU/INS code for Inosinic Acid. Nucleotide umami enhancer; avoid with gout.',
    'e632': 'E632 is the EU/INS code for Dipotassium Inosinate. Nucleotide flavour enhancer; avoid with gout.',
    'e633': 'E633 is the EU/INS code for Calcium Inosinate. Nucleotide flavour enhancer; avoid with gout.',
    'glycine food': 'Glycine (E640/INS 640) is the simplest amino acid, used as a mild sweetener and bitter masker. Naturally in gelatin and bone broth. Safe.',
    'e640': 'E640 is the EU/INS code for Glycine and its Sodium Salt. Amino acid flavour enhancer. Safe.',

    # ── Glazing agents / waxes / gases (E900-E999) ───────────────────────
    'dimethyl polysiloxane': 'Dimethyl Polysiloxane (PDMS/E900/INS 900) is a silicone polymer anti-foaming agent in frying oils and beverages. Not absorbed by the body. Safe.',
    'e900': 'E900 is the EU/INS code for Dimethyl Polysiloxane. Silicone anti-foaming agent. Safe.',
    'beeswax food': 'Beeswax (E901/INS 901) is natural wax from honeybees. Used as a glazing agent on confectionery and fruit. Safe; not vegan.',
    'e901': 'E901 is the EU/INS code for Beeswax. Natural glazing agent. Safe; not vegan.',
    'candelilla wax': 'Candelilla Wax (E902/INS 902) is a plant-based wax from the candelilla shrub. Vegan alternative to beeswax. Safe.',
    'e902': 'E902 is the EU/INS code for Candelilla Wax. Plant-based vegan glazing agent. Safe.',
    'carnauba wax food': 'Carnauba Wax (E903/INS 903) is the hardest natural wax from Brazilian carnauba palms. Gives shine to hard-coated sweets. Safe.',
    'e903': 'E903 is the EU/INS code for Carnauba Wax. The shine on hard-coated confectionery. Safe.',
    'shellac food': 'Shellac (E904/INS 904) is a natural resin from lac insects. High-gloss coating on confectionery and pharmaceutical tablets. Safe; not vegan. India is the world\'s largest producer.',
    'e904': 'E904 is the EU/INS code for Shellac. Insect-derived glazing agent. Safe; not vegan.',
    'e920': 'E920 is the EU/INS code for L-Cysteine. Dough conditioner amino acid. Often from hair/feathers -- check vegan status. Safe.',
    'e941': 'E941 is the EU/INS code for Nitrogen. Inert packaging gas. Safe -- makes up 78% of air.',
    'e942': 'E942 is the EU/INS code for Nitrous Oxide. Whipped cream propellant. Safe in food; dangerous recreationally.',

    # ── Sweeteners (E950-E968) ───────────────────────────────────────────
    'steviol glycosides': 'Steviol Glycosides (Stevia/E960/INS 960) are naturally sweet compounds from the stevia plant -- 200-400 times sweeter than sugar. Zero calories. Approved by FSSAI, FDA, EU and Codex. Safe; suitable for diabetics.',
    'e960': 'E960 is the EU/INS code for Steviol Glycosides (Stevia). Natural zero-calorie sweetener. Safe; suitable for diabetics.',
    'thaumatin': 'Thaumatin (E957/INS 957) is a natural sweet protein from the katemfe fruit -- about 2,500 times sweeter than sugar. Zero calories at use levels. Safe.',
    'e957': 'E957 is the EU/INS code for Thaumatin. Natural sweet protein; ~2,500x sweeter than sugar. Safe.',
    'neotame': 'Neotame (E961/INS 961) is an ultra-intense sweetener (~8,000x sweeter than sugar). Unlike aspartame, safe for phenylketonurics. FDA and EU approved.',
    'e961': 'E961 is the EU/INS code for Neotame. Ultra-intense sweetener. Safe for phenylketonurics. FDA and EU approved.',
    'e953': 'E953 is the EU/INS code for Isomalt. Sugar alcohol from sucrose; laxative at high intake; label warning required.',
    'e965': 'E965 is the EU/INS code for Maltitol. Sugar alcohol sweetener; laxative at >40g/day; label warning required.',
    'e966': 'E966 is the EU/INS code for Lactitol. Sugar alcohol; laxative at high intake; not for lactose-intolerant individuals.',
    'e967': 'E967 is the EU/INS code for Xylitol. Natural sugar alcohol with dental benefits. CAUTION -- toxic to dogs. Laxative effects in humans at high doses.',
    'erythritol': 'Erythritol (E968/INS 968) is a naturally occurring sugar alcohol from fermented foods. Near-zero calories; minimal laxative effect. Used in zero-calorie products. Safe.',
    'e968': 'E968 is the EU/INS code for Erythritol. Natural sugar alcohol; near-zero calories; minimal laxative effect. Safe.',
    'cyclamate': 'Cyclamate (E952/INS 952) is an artificial sweetener. Banned in USA (1969) and UK due to bladder cancer in rat studies. Permitted in India and EU at specified limits.',
    'e952': 'E952 is the EU/INS code for Cyclamate. Banned in USA and UK; permitted in India and EU at limits.',
    'sodium cyclamate': 'Sodium Cyclamate is the sodium salt form of cyclamate. Banned in USA and UK; approved in EU and India at limits.',

    # ── Modified starches (E1400-E1599) ──────────────────────────────────
    'e1404': 'E1404 is the EU/INS code for Oxidised Starch. Modified starch for confectionery coatings. Safe.',
    'e1410': 'E1410 is the EU/INS code for Monostarch Phosphate. Modified starch thickener. Safe.',
    'e1412': 'E1412 is the EU/INS code for Distarch Phosphate. Cross-linked modified starch. Safe.',
    'e1420': 'E1420 is the EU/INS code for Acetylated Starch. Modified starch. Safe.',
    'e1422': 'E1422 is the EU/INS code for Acetylated Distarch Adipate. Modified starch in soups and frozen foods. Safe.',
    'e1440': 'E1440 is the EU/INS code for Hydroxypropyl Starch. Modified starch. Safe.',
    'e1442': 'E1442 is the EU/INS code for Hydroxypropyl Distarch Phosphate. Widely used modified starch in ketchup, mayo and baby food. Safe.',
    'e1450': 'E1450 is the EU/INS code for Starch Sodium Octenyl Succinate. Emulsifying modified starch for encapsulating flavours. Safe.',
    'hydroxypropyl distarch phosphate': 'Hydroxypropyl Distarch Phosphate (E1442/INS 1442) has superior heat, acid and freeze-thaw stability. Widely used in ketchup, mayonnaise, sauces and baby food. Safe.',

    # ── INS number lookup entries ─────────────────────────────────────────
    'ins 100': 'INS 100 / E100 -- Curcumin (Turmeric Yellow). Natural yellow colour. Safe.',
    'ins 101': 'INS 101 / E101 -- Riboflavin (Vitamin B2). Natural yellow colour and B-vitamin. Safe.',
    'ins 102': 'INS 102 / E102 -- Tartrazine. Synthetic yellow azo dye. EU warning label required. See tartrazine.',
    'ins 110': 'INS 110 / E110 -- Sunset Yellow FCF. Synthetic orange azo dye. EU warning label required.',
    'ins 129': 'INS 129 / E129 -- Allura Red AC (Red 40). Synthetic red azo dye. EU warning label required.',
    'ins 150d': 'INS 150d / E150d -- Sulphite Ammonia Caramel. Contains 4-MEI (IARC Group 2B). See e150d.',
    'ins 160a': 'INS 160a / E160a -- Beta-Carotene. Natural orange-yellow colour; Vitamin A precursor. Safe.',
    'ins 160b': 'INS 160b / E160b -- Annatto. Natural orange colour. Safe.',
    'ins 162': 'INS 162 / E162 -- Beetroot Red (Betanin). Natural red-purple colour. Safe.',
    'ins 171': 'INS 171 / E171 -- Titanium Dioxide. White colour. BANNED in EU food since 2022.',
    'ins 200': 'INS 200 / E200 -- Sorbic Acid. Natural mould inhibitor. Safe.',
    'ins 202': 'INS 202 / E202 -- Potassium Sorbate. Most widely used food preservative. Safe.',
    'ins 211': 'INS 211 / E211 -- Sodium Benzoate. Preservative; forms benzene with Vitamin C. See sodium benzoate.',
    'ins 220': 'INS 220 / E220 -- Sulfur Dioxide. Preservative; triggers asthma in sensitive individuals. See sulfur dioxide.',
    'ins 250': 'INS 250 / E250 -- Sodium Nitrite. Meat curing agent; forms nitrosamines when heated. See sodium nitrite.',
    'ins 260': 'INS 260 / E260 -- Acetic Acid (Vinegar acid). Safe acidity regulator.',
    'ins 270': 'INS 270 / E270 -- Lactic Acid. Natural fermentation acid. Safe.',
    'ins 296': 'INS 296 / E296 -- Malic Acid. Natural apple acid. Safe.',
    'ins 300': 'INS 300 / E300 -- Ascorbic Acid (Vitamin C). Essential vitamin and antioxidant. Safe.',
    'ins 306': 'INS 306 / E306 -- Tocopherol (Vitamin E). Natural antioxidant. Safe.',
    'ins 320': 'INS 320 / E320 -- BHA. Synthetic antioxidant; IARC Group 2B possible carcinogen.',
    'ins 321': 'INS 321 / E321 -- BHT. Synthetic antioxidant; IARC possible carcinogen.',
    'ins 330': 'INS 330 / E330 -- Citric Acid. Natural fruit acid. Safe.',
    'ins 338': 'INS 338 / E338 -- Phosphoric Acid. Gives cola drinks their tang; erodes tooth enamel with heavy use.',
    'ins 400': 'INS 400 / E400 -- Alginic Acid. Natural seaweed thickener. Safe.',
    'ins 401': 'INS 401 / E401 -- Sodium Alginate. Seaweed gelling agent. Safe.',
    'ins 406': 'INS 406 / E406 -- Agar. Natural red algae gelling agent. Vegetarian gelatin. Safe.',
    'ins 407': 'INS 407 / E407 -- Carrageenan. Seaweed stabiliser. Gut inflammation concerns; banned in EU infant formula.',
    'ins 410': 'INS 410 / E410 -- Locust Bean Gum (Carob Gum). Natural seed thickener. Safe.',
    'ins 412': 'INS 412 / E412 -- Guar Gum. Natural Indian seed gum. Safe.',
    'ins 414': 'INS 414 / E414 -- Gum Arabic (Acacia Gum). Natural food gum. Safe.',
    'ins 415': 'INS 415 / E415 -- Xanthan Gum. Microbial thickener; key to gluten-free baking. Safe.',
    'ins 420': 'INS 420 / E420 -- Sorbitol. Sugar alcohol; laxative at >50g/day.',
    'ins 422': 'INS 422 / E422 -- Glycerol (Glycerine). Natural humectant. Safe.',
    'ins 433': 'INS 433 / E433 -- Polysorbate 80. Emulsifier; trace 1,4-dioxane possible. Safe within limits.',
    'ins 440': 'INS 440 / E440 -- Pectin. Natural gelling agent from citrus peel. Safe.',
    'ins 450': 'INS 450 / E450 -- Diphosphates. Emulsifying salts. Safe.',
    'ins 471': 'INS 471 / E471 -- Mono- and Diglycerides of Fatty Acids. Most widely used food emulsifier. Safe.',
    'ins 476': 'INS 476 / E476 -- PGPR. Chocolate emulsifier. Safe.',
    'ins 481': 'INS 481 / E481 -- Sodium Stearoyl Lactylate (SSL). Key bread emulsifier. Safe.',
    'ins 500': 'INS 500 / E500 -- Sodium Carbonates (Baking Soda). Most widely used raising agent. Safe.',
    'ins 508': 'INS 508 / E508 -- Potassium Chloride. Low-sodium salt substitute. Safe.',
    'ins 509': 'INS 509 / E509 -- Calcium Chloride. Firming agent. Safe.',
    'ins 511': 'INS 511 / E511 -- Magnesium Chloride (Nigari). Tofu coagulant. Safe.',
    'ins 516': 'INS 516 / E516 -- Calcium Sulphate. Tofu coagulant. Safe.',
    'ins 551': 'INS 551 / E551 -- Silicon Dioxide. Most widely used anti-caking agent. Not absorbed; safe.',
    'ins 575': 'INS 575 / E575 -- Glucono Delta-Lactone (GDL). Natural mild acidifier. Safe.',
    'ins 621': 'INS 621 / E621 -- Monosodium Glutamate (MSG). Umami flavour enhancer. FDA GRAS. Safe.',
    'ins 627': 'INS 627 / E627 -- Disodium Guanylate. Nucleotide flavour enhancer; avoid with gout.',
    'ins 631': 'INS 631 / E631 -- Disodium Inosinate. Nucleotide flavour enhancer; avoid with gout.',
    'ins 635': "INS 635 / E635 -- Disodium 5'-Ribonucleotides (I+G). Nucleotide enhancer blend; avoid with gout.",
    'ins 900': 'INS 900 / E900 -- Dimethyl Polysiloxane. Silicone anti-foaming agent. Safe.',
    'ins 903': 'INS 903 / E903 -- Carnauba Wax. Natural glazing agent. Safe.',
    'ins 951': 'INS 951 / E951 -- Aspartame. Artificial sweetener (IARC Group 2B). See aspartame.',
    'ins 954': 'INS 954 / E954 -- Saccharin. Artificial sweetener. Bladder cancer concerns. See saccharin.',
    'ins 955': 'INS 955 / E955 -- Sucralose. Artificial sweetener. See sucralose.',
    'ins 960': 'INS 960 / E960 -- Steviol Glycosides (Stevia). Natural zero-calorie sweetener. Safe.',
    'ins 967': 'INS 967 / E967 -- Xylitol. Sugar alcohol. TOXIC TO DOGS. Dental benefits for humans.',
    'ins 968': 'INS 968 / E968 -- Erythritol. Natural sugar alcohol; near-zero calories. Safe.',
    'ins 1442': 'INS 1442 / E1442 -- Hydroxypropyl Distarch Phosphate. Modified starch in ketchup and baby food. Safe.',

    # ══ Soap Surfactants (Saponified Salts) ═══════════════════════════════════
    'sodium palmate': 'Sodium Palmate is the sodium salt of the fatty acids of palm oil, produced by saponification of palm oil with sodium hydroxide (lye). It is the primary cleansing and lathering ingredient in most commercial bar soaps. Chemically, it is a mixture of sodium palmitate (C16) and sodium stearate (C18) — the two dominant fatty acids in palm oil. While highly effective at removing oils, dirt and bacteria, its alkaline pH (~9–10) disrupts the skin\'s natural acid mantle (pH 4.5–5.5), which can cause transient barrier dysfunction, dryness and irritation particularly in individuals with eczema, sensitive skin or psoriasis. Environmental concern: palm oil is one of the most controversial agricultural products globally — large-scale palm cultivation is responsible for extensive tropical deforestation, peatland destruction, significant greenhouse gas emissions, and habitat loss for orangutans, pygmy elephants and Sumatran tigers. RSPO (Roundtable on Sustainable Palm Oil) certification is the primary standard for responsible sourcing, though compliance is inconsistent. For consumers with dry or sensitive skin, syndet (synthetic detergent) bars containing sodium cocoyl isethionate are a significantly milder alternative.',
    'sodium palm kernelate': 'Sodium Palm Kernelate is the sodium salt of palm kernel oil fatty acids, produced by saponification of palm kernel oil — the oil extracted from the seed (kernel) of the oil palm fruit, distinctly different from palm (fruit pulp) oil. Palm kernel oil has a significantly different fatty acid profile from palm oil: it is rich in lauric acid (C12, ~45–50%) and myristic acid (C14, ~15%), making its composition closer to coconut oil. Consequently, sodium palm kernelate produces a harder bar soap with denser, more stable, longer-lasting lather compared to sodium palmate — the lauric acid component is responsible for excellent foam generation. It is somewhat less drying than sodium palmate but still alkaline (pH ~9) and may cause barrier disruption in sensitive individuals. It carries the same environmental concerns as all palm-derived ingredients (deforestation, habitat loss, biodiversity impact). RSPO certification should be verified for palm kernel oil sourcing.',

    # ══ Natural Butters and Plant Oils ════════════════════════════════════════
    'kokum butter': 'Kokum Butter is a hard, white vegetable fat extracted from the seeds of Garcinia indica (the kokum tree), a plant native to the Western Ghats of India — particularly coastal Karnataka, Goa and Maharashtra. It is obtained by cold-pressing or solvent extraction of the dried kokum seeds. Fatty acid composition: exceptionally high in stearic acid (~55–60%) and oleic acid (~35–40%), with minimal polyunsaturated fats — making it one of the most oxidatively stable natural butters. Key properties: (1) Non-comedogenic — rated 0 on the comedogenic scale, uniquely suitable for oily and acne-prone skin unlike shea or cocoa butter; (2) deeply emollient without greasiness — melts at skin temperature and absorbs quickly without occlusive residue; (3) healing and regenerative — used traditionally in Ayurveda for cracked heels, chapped lips, dry scalp, sunburn and wound healing; (4) anti-inflammatory — Garcinia indica extracts have demonstrated anti-inflammatory activity in multiple in-vitro studies, attributed to garcinol and hydroxycitric acid; (5) antioxidant — garcinol, a polyisoprenylated benzophenone, shows significant free-radical scavenging activity; (6) promotes skin elasticity — stearic acid content supports skin lipid barrier integrity. In hair care, used to nourish dry, brittle hair and seal the cuticle. One of the most traditional and well-tolerated Indian cosmetic ingredients. Safe; no known allergenicity. An excellent choice for dry, very dry, or eczema-prone skin.',
    'oenocarpus bataua fruit oil': 'Oenocarpus Bataua Fruit Oil (patauá oil / patuá oil) is extracted from the fruits of the patauá palm (Oenocarpus bataua, syn. Jessenia bataua), a tall palm tree indigenous to the Amazon rainforest and Orinoco basin of South America, harvested by indigenous Amazonian communities using traditional extraction methods. Fatty acid composition: exceptionally high in oleic acid (C18:1, ~72–80% — rivalling and often exceeding argan and olive oils), with palmitic acid (~11%) and small amounts of linoleic acid (~3–5%). This makes patauá oil one of the richest natural sources of oleic acid available in cosmetics. Properties: (1) exceptional hair conditioning — oleic acid oils have a well-established affinity for the hair cortex; research has shown that C18:1-rich oils penetrate the hair fibre, reduce hygral fatigue (the swelling and shrinkage damage from repeated wetting) and restore the hair\'s natural lipid content after chemical or heat treatment; (2) emollient — quickly absorbed, non-greasy skin feel; (3) anti-inflammatory potential — patauá oil extracts have shown anti-inflammatory properties in studies by Brazilian and French research groups; (4) antioxidant — naturally rich in tocopherols (Vitamin E) and phytosterols; (5) sustainability credentials — patauá oil is harvested from wild-growing Amazonian palms, incentivising forest preservation over slash-and-burn agriculture; featured as a key ingredient in sustainable Amazonian bioeconomy initiatives. Safe; well-tolerated; no identified allergenicity at cosmetic use levels.',
    'hydrolyzed plukenetia volubilis seed extract': 'Hydrolyzed Plukenetia Volubilis Seed Extract is produced from the seeds of Plukenetia volubilis — the sacha inchi plant (Inca peanut, mountain peanut), a vine indigenous to the Peruvian and Brazilian Amazon, now cultivated in tropical regions for its exceptionally nutritious seeds. Sacha inchi seeds are among the richest known plant sources of polyunsaturated fatty acids: alpha-linolenic acid (omega-3, ~45–53%), linoleic acid (omega-6, ~33–38%), and oleic acid (omega-9, ~8%), with 25–30% of the seed being high-quality complete protein containing all essential amino acids. Hydrolysis (by enzymatic or mild acid treatment) breaks the seed protein into short peptides and free amino acids, and the oil fraction into smaller components — making the extract water-compatible and able to penetrate the hair fibre and skin surface. Properties in hair care: (1) conditioning and repair — peptides from sacha inchi protein temporarily fill structural gaps in the hair cuticle, reducing breakage and improving tensile strength; (2) hydration — amino acids act as natural moisturising factors (NMFs), attracting and retaining water in the hair cortex; (3) antioxidant protection — the polyphenol and tocopherol fraction protects hair from UV and oxidative damage; (4) scalp nourishment — the omega-3 component may reduce scalp inflammation and support healthy hair follicles. The extract\'s compatibility with rinse-off formulations (unlike the oil itself) makes it practical in shampoos and conditioners. Safe; no significant allergenicity identified in available literature. Well-tolerated; environmentally sustainable source.',

    # ══ Mild Surfactants / Cleansing Agents ══════════════════════════════════
    'sodium cocoyl isethionate': 'Sodium Cocoyl Isethionate (SCI) is a mild anionic surfactant produced by reacting coconut-derived fatty acids (primarily lauric acid, C12) with isethionic acid (2-hydroxyethanesulfonic acid), followed by sodium hydroxide neutralisation. It is the defining ingredient of "syndet bars" (synthetic detergent bars) — bar soap alternatives specifically formulated for sensitive, dry and eczema-prone skin. Key properties: (1) skin pH-compatible — SCI produces a lather with a pH of approximately 5.5–6.5, substantially closer to the skin\'s natural acid mantle (pH 4.5–5.5) than traditional soap (pH 9–10); this is clinically significant because maintaining acid mantle pH preserves barrier enzyme function and microbiome health; (2) exceptionally mild — multiple clinical studies comparing surfactant mildness consistently rank SCI among the lowest skin irritation scores, significantly below SLS, SLES and even cocamidopropyl betaine; (3) non-stripping — maintains stratum corneum lipid integrity better than conventional surfactants; (4) conditioning — leaves a slight conditioning feel; (5) rich, creamy, stable foam; (6) biodegradable; (7) compatible with ECOCERT/COSMOS natural cosmetics certification. Approved by FDA, EU Cosmetics Regulation, FSSAI and all major regulatory bodies. No significant allergenicity identified. The preferred surfactant for dermatologically-tested sensitive skin formulations endorsed by dermatology associations.',
    'sodium lauroyl sarcosinate': 'Sodium Lauroyl Sarcosinate (SLS — not to be confused with Sodium Lauryl Sulfate, also abbreviated SLS) is a mild anionic surfactant derived from sarcosine — a naturally occurring amino acid (N-methylglycine found in human muscle tissue, cranberry juice and starfish) — and coconut-derived lauric acid (C12 fatty acid). It produces excellent, creamy foam with good conditioning properties and is significantly milder on skin and mucous membranes than sodium lauryl sulfate. Used in facial cleansers, shampoos, body washes and toothpaste. Notable property in oral care: sodium lauroyl sarcosinate has demonstrated inhibition of Streptococcus mutans and other cariogenic bacteria in multiple in-vitro and clinical studies, contributing to anti-cavity and anti-plaque effects in toothpaste beyond mechanical cleaning. SCCS (EU Scientific Committee on Consumer Safety) review assessed sodium lauroyl sarcosinate as safe in cosmetics at typical use concentrations. The primary safety note in the scientific literature is the theoretical potential for N-nitrosoarcosine formation — a nitrosamine — if the ingredient contacts strong nitrosating agents (such as certain nitrogen-containing preservatives like sodium nitrite). Well-formulated products specifically avoid such combinations. No significant allergenicity; approved by FDA, EU Cosmetics Regulation, FSSAI.',
    'capryloyl/caproyl methyl glucamide': 'Capryloyl/Caproyl Methyl Glucamide is a mild, biodegradable amphoteric-like surfactant from the glucamide family, produced by the condensation reaction of N-methyl glucamine (from glucose) with a blend of caprylic acid (C8) and caproic acid (C6) — both fatty acids typically derived from coconut oil. It belongs to a category of "green chemistry" surfactants designed to be both highly effective and environmentally responsible. Properties: (1) mild and gentle — very low irritation potential; suitable for baby products, sensitive skin and atopic dermatitis formulations; (2) creamy, stable foam compatible with other mild surfactants; (3) rapidly biodegradable — the glucamide backbone degrades efficiently in wastewater treatment; (4) derived from renewable resources — glucose and coconut oil; (5) broad pH stability; (6) good compatibility with both anionic and amphoteric surfactants. Often used as the primary or co-surfactant in sulphate-free cleansing formulations. No significant allergenicity or regulatory concerns identified. Approved for cosmetic use globally.',
    'lauroyl/myristoyl methyl glucamide': 'Lauroyl/Myristoyl Methyl Glucamide is a mild surfactant from the glucamide family, made from N-methyl glucamine and a blend of lauric acid (C12) and myristic acid (C14) fatty acids from coconut and palm kernel oil. The longer carbon chain lengths (C12–C14) compared to capryloyl/caproyl methyl glucamide provide enhanced cleansing performance (better oil removal) alongside good conditioning properties, while maintaining the excellent skin tolerability characteristic of the glucamide family. Properties: (1) mild with excellent skin compatibility; (2) denser, more abundant foam than the C8/C6 variant — suitable for both facial and body cleansing; (3) conditioning after-feel — skin feels smooth and non-stripped after rinsing; (4) biodegradable; (5) compatible with natural cosmetic certification standards (ECOCERT-approved surfactant). Commonly paired with its C8/C6 counterpart (Capryloyl/Caproyl Methyl Glucamide) and Coco-Glucoside in sulphate-free "natural" formulations. Safe; no known allergenicity or regulatory concerns.',
    'coco-glucoside': 'Coco-Glucoside is a mild, non-ionic surfactant produced by condensation reaction of glucose (from corn starch or other starch sources) with coconut-derived fatty alcohols (primarily lauryl alcohol C12 and myristyl alcohol C14). It belongs to the alkyl glucoside (APG) surfactant family — a group recognised for being derived entirely from renewable plant-based raw materials and for having excellent biodegradability and skin tolerability. Properties: (1) exceptionally gentle — multiple clinical studies consistently show very low primary skin irritation scores; eye-safe; used in ophthalmologically and dermatologically tested baby products; (2) biodegradable — readily and rapidly biodegrades; one of the most environmentally favourable surfactant classes; (3) non-ionic — compatible with all other surfactant types (anionic, cationic, amphoteric); (4) skin-compatible pH ~11–12 as supplied, but in formulations buffered to normal cosmetic pH, excellent tolerability; (5) ECOCERT/COSMOS approved — frequently featured in certified natural cosmetics; (6) no ethoxylation — unlike SLES or PEG ingredients, alkyl glucosides do not carry 1,4-dioxane contamination risk; (7) good foam quality. Widely used in baby shampoos, sensitive skin cleansers, natural formulations and micellar waters. Approved globally. Safe.',
    'glycol distearate': 'Glycol Distearate (Ethylene Glycol Distearate / EGDS) is an ester produced by reacting ethylene glycol with two molecules of stearic acid (a saturated C18 fatty acid typically derived from vegetable or animal fat). It is the ingredient responsible for the distinctive pearl shimmer or "nacreous" appearance in shampoos, conditioners and body washes — the white, opalescent, light-reflecting quality of many liquid personal care products. Mechanism of pearlising action: glycol distearate forms microscopic crystalline platelets within the aqueous product matrix, which scatter incident light and produce the characteristic mother-of-pearl visual effect. Properties: (1) pearlising and opacifying — cosmetic aesthetic role; (2) mild emollient and skin-conditioning effect at the hair and skin surface; (3) mild thickener at higher concentrations. Safety: well-tolerated; patch test studies show low sensitisation potential; non-irritating to eyes at typical concentrations in rinse-off products; approved by EU Cosmetics Regulation, FDA and FSSAI. The ethylene glycol moiety in the molecule is part of the ester bond and is not the same as free ethylene glycol (which is toxic); the ester form is considered safe at cosmetic use levels. Safe.',
    'peg-150 distearate': 'PEG-150 Distearate is a high-molecular-weight polyethylene glycol (PEG) ester, produced by reacting polyethylene glycol with an average chain length of 150 ethylene oxide units (hence "PEG-150") with stearic acid. Used as a primary viscosity-building (thickening) agent in shampoos, conditioners and body washes — it is what gives these liquid products their characteristic thick, gel-like consistency without leaving a heavy or greasy feel. Properties: (1) efficient thickener at low concentrations; (2) the very high molecular weight (PEG-150 ≈ average MW ~6,600 Da) means essentially zero dermal penetration; (3) compatible with most surfactants and cosmetic ingredients. Safety concern: PEG-150 Distearate is manufactured via ethoxylation — a reaction of stearic acid with ethylene oxide that may generate 1,4-dioxane as a process by-product. The European Chemicals Agency (ECHA), FDA and Health Canada have all identified 1,4-dioxane as a potential carcinogen (IARC Group 2B — possibly carcinogenic to humans) and an environmental concern. The concern is a manufacturing quality and purity issue — the FDA recommends manufacturers minimise 1,4-dioxane content in cosmetic products to below 10 ppm; vacuum-stripping during production removes the vast majority of residual 1,4-dioxane to well below safety thresholds in quality-controlled manufacturing. Approved for cosmetic use; safe within applicable purity specifications.',
    'stearamidopropyl dimethylamine': 'Stearamidopropyl Dimethylamine (SAPDMA) is a fatty acid amide tertiary amine — a synthetic conditioning agent derived from stearic acid (C18 saturated fatty acid from vegetable or animal tallow) and 3-(dimethylamino)propylamine. In conditioner formulations maintained at slightly acidic pH (typically 4.5–5.5), SAPDMA undergoes protonation — its tertiary amine nitrogen gains a positive charge — which provides strong substantivity (adhesion) to the negatively charged surface of hair fibres. This electrostatic attraction is the basis for its conditioning efficacy. Physiological function: (1) detangling — significantly reduces hair-to-hair friction and improves wet and dry combability; (2) anti-static control — neutralises static charge that causes frizz and flyaways in low-humidity conditions; (3) smoothing — fills gaps in the hair cuticle; (4) improved hair feel. Safety: SCCS (EU Scientific Committee on Consumer Safety) reviewed stearamidopropyl dimethylamine and assessed it as safe for use in rinse-off hair care products at typical concentrations. A concern noted in the scientific literature: tertiary amines can theoretically form nitrosamines (N-nitroso compounds, which are IARC carcinogens) in the presence of nitrosating agents. EU Cosmetics Regulation Article 27 restricts amines from being formulated with nitrosating agents for this reason. Well-formulated products comply with this requirement, making the risk in compliant products very low. Approved by EU Cosmetics Regulation, FDA and FSSAI.',

    # ══ Optical Brightening Agent ═════════════════════════════════════════════
    'disodium distyrylbiphenyl disulfonate': 'Disodium Distyrylbiphenyl Disulfonate (CAS 27344-41-8; trade names Tinopal CBS, FWA-351, Fluorescent Brightening Agent 351) is a stilbene-type fluorescent whitening agent (FWA) or optical brightening agent (OBA). It works by absorbing ultraviolet radiation (UVA, 300–400 nm) and re-emitting it as visible blue-white light (emission peak ~430–440 nm), making white and pale-coloured products appear brighter, whiter and more visually appealing. In bar soaps, it deposits onto fabric and skin surfaces during washing, making clothing appear whiter — a purely cosmetic function with no therapeutic or hygiene benefit. Safety concerns: (1) photoallergy potential — fluorescent brighteners can cause photocontact allergic reactions in susceptible individuals (skin sensitisation followed by UV-triggered immune response); case reports of photoallergic contact dermatitis to Tinopal CBS have been documented in the dermatology literature; (2) environmental persistence — stilbene-type optical brighteners are poorly biodegradable under standard conditions and accumulate in aquatic environments; ECHA classifies some OBAs as potentially persistent, bioaccumulative and toxic (PBT); (3) aquatic toxicity — some studies report toxicity to aquatic organisms; (4) in-vitro genotoxicity concerns have been raised for stilbene OBAs under UV irradiation conditions in some studies, though in-vivo significance at cosmetic exposure levels remains unclear. Not approved in EU rinse-off products at certain concentrations. Added solely for aesthetic whitening of the product with no skin health benefit.',

    # ══ Conditioning / Quaternary Ammonium Polymers ════════════════════════════
    'polyquaternium-113': 'Polyquaternium-113 (PQ-113) is a high-molecular-weight cationic conditioning polymer based on a modified polysaccharide backbone (typically hydroxypropyl guar or similar natural biopolymer) that has been quaternized with trimethyl ammonium functional groups. It belongs to the polyquaternium family of hair conditioning polymers — a broad group of positively charged polymers used in shampoos and conditioners. Properties: (1) conditioning — the permanent positive charge (quaternary nitrogen) is electrostatically attracted to the negatively charged hair cuticle surface; adsorbs substantively from rinse-off products, providing detangling, smoothing and frizz control; (2) good film-forming on hair — reduces split ends, improves hair elasticity; (3) low build-up potential compared to many conditioning agents; (4) compatible with anionic surfactants — can be used directly in shampoo formulations; (5) the polysaccharide backbone confers improved biodegradability compared to fully synthetic polyquaterniums such as PQ-7 or PQ-11. Safety: no significant adverse effects at cosmetic use concentrations; well-tolerated. The primary concern for quaternary ammonium polymers as a class is environmental persistence — quats have antimicrobial activity that affects beneficial environmental microorganisms, and accumulate in water systems. PQ-113\'s natural polysaccharide backbone partially mitigates this environmental concern. Approved for cosmetic use.',
    'quaternium-98': 'Quaternium-98 is a quaternary ammonium salt conditioning agent — a member of the broad quaternary ammonium compound (quat) family used in personal care products, particularly in combined shampoo-conditioner formulations. Quaternary ammonium compounds carry a permanent positive charge on the nitrogen atom, enabling strong electrostatic adsorption to the negatively charged surface of wet hair fibres. This substantivity provides: (1) conditioning and detangling — reduces combing force on wet and dry hair; (2) anti-static control — neutralises charge build-up; (3) smooth, silky after-feel; (4) film formation on hair cuticle. Safety profile for quaternary ammonium compounds as a class: (1) contact allergy — quats are a recognised cause of contact allergic and irritant contact dermatitis, particularly in individuals with occupational exposure (hairdressers, healthcare workers) or pre-existing sensitive skin; (2) eye irritation — concentrated quat solutions are irritating to eyes; in rinse-off products at cosmetic concentrations, risk is low; (3) environmental concerns — quaternary ammonium compounds are generally poorly biodegradable, accumulate in wastewater treatment sludge and aquatic environments, exhibit aquatic toxicity, and have demonstrated disruption of beneficial environmental microbial communities at sub-lethal concentrations; (4) antimicrobial resistance — chronic sub-lethal exposure to quats in the environment may contribute to cross-resistance with antibiotics in some bacterial species. At cosmetic concentrations in rinse-off products, individual consumer risk is low. Environmental persistence is the more significant concern.',

    # ══ Mineral / Petrochemical Emollients ════════════════════════════════════
    'light liquid paraffin': 'Light Liquid Paraffin (also known as light mineral oil, light white oil, liquid paraffin light grade) is a highly refined, low-viscosity grade of mineral oil — a petroleum-derived mixture of saturated aliphatic (paraffin) and alicyclic hydrocarbon chains. The "light" designation refers to its lower density and viscosity (~20–30 cP) compared to heavy liquid paraffin. It is chemically equivalent to Paraffinum Liquidum (the INCI name used in cosmetic formulations). Highly refined to pharmaceutical or USP grade by processes including hydrotreatment, hydrocracking or acid-clay treatment to remove impurities. Properties: (1) excellent occlusive emollient — forms a physical barrier on skin surface that slows transepidermal water loss (TEWL); (2) inert — does not react with skin components; (3) hypoallergenic in pure form; (4) widely used in baby products, pharmaceutical preparations and cosmetics. Concerns: (1) Mineral Oil Aromatic Hydrocarbons (MOAH) — petrochemical refining can leave trace contamination with polycyclic aromatic hydrocarbons (PAH), some of which are classified IARC Group 1 carcinogens. EFSA has expressed concern about MOAH in food-contact applications; in cosmetics, EU requires safety data demonstrating MOAH levels below the threshold of concern (typically <2 ppm); (2) occlusive nature — while beneficial for xerosis, complete occlusion traps bacteria, sebum and heat, potentially aggravating acne-prone skin with regular use; (3) inhibits cell desquamation and skin breathing with heavy long-term use; (4) petroleum-derived; non-renewable origin; (5) environmental persistence. Approved for cosmetic use in EU, FDA and FSSAI jurisdictions at appropriate purity grades.',

    # ══ Synthetic Dyes / Colorants ════════════════════════════════════════════
    'ci 11680': 'CI 11680 (Colour Index Number 11680) is a synthetic monoazo dye known as Yellow AB (Aniline Yellow) or Fat Yellow 3. It produces a yellow to orange-yellow coloration and has been used in some personal care and cosmetic products. Regulatory status is highly restrictive: CI 11680 (Yellow AB) is NOT listed in Annex IV of the EU Cosmetics Regulation as an approved cosmetic colorant — its use in cosmetics is therefore not permitted in the European Union. In the USA, the FDA does not include CI 11680 in its list of approved cosmetic color additives for general use. Toxicology: as a monoazo dye, CI 11680 contains an azo group (-N=N-) that can be reductively cleaved by azo-reductase enzymes (present in intestinal bacteria and skin microflora under anaerobic conditions) to release aromatic amines. Several aromatic amines are classified as human carcinogens (IARC Group 1 or 2A). While the carcinogenic risk from azo dye reduction is primarily of concern with oral ingestion (food dyes) rather than topical application, the dermal absorption and metabolic activation potential of this specific compound warrants attention. The absence of regulatory approval in major cosmetic jurisdictions (EU, USA) is the primary concern. Its use in an Indian market product should be evaluated against FSSAI/BIS cosmetic colour regulations.',
    'ci 12120': 'CI 12120 (Colour Index Number 12120) is a synthetic monoazo dye — also referenced in some databases as Solvent Red 1 or related structures. It is used to impart red to orange-red coloration in personal care formulations. Regulatory status: CI 12120 is NOT listed in the EU Cosmetics Regulation Annex IV as an approved cosmetic colorant and is therefore not permitted for cosmetic use in the European Union. The FDA does not list CI 12120 as a permitted cosmetic color additive. Toxicological considerations: as a member of the azo dye class, CI 12120 contains an azo linkage susceptible to reductive cleavage by bacterial azo-reductases, potentially releasing aromatic amines — compounds for which various IARC carcinogenicity classifications exist depending on structure. The significance for topical rinse-off use (soap) is primarily the extent of dermal absorption, which is generally lower than for oral routes. However, the fundamental issue remains: this dye lacks regulatory approval for cosmetic use in major jurisdictions, meaning its safety has not been formally reviewed and established by the EU SCCS or FDA. Consumers have no assurance of independent safety evaluation. Its presence in a product sold in India should be verified against FSSAI Schedule IX cosmetic colorant regulations.',

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
    # PEG-modified silicone waxes — the PEG concern (1,4-dioxane) is a manufacturing
    # quality issue at trace levels; in cosmetics these are worth noting, not CQ
    'bis-peg-12 dimethicone beeswax': (
        'PEG-modified silicone wax emulsifier',
        'Contains a PEG moiety — ethoxylation may introduce trace 1,4-dioxane (IARC Group 2B possible carcinogen); reputable manufacturers control this via vacuum stripping; also contains a beeswax-derived component (not vegan); safe at cosmetic-use concentrations within approved limits'
    ),
    'bis-peg': (
        'PEG-modified silicone compound',
        'PEG-modified silicone; ethoxylation may introduce trace 1,4-dioxane; safe at approved cosmetic concentrations; manufacturers control 1,4-dioxane via vacuum stripping'
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
        'light liquid paraffin': ('Light mineral oil (petroleum-derived)', 'Petroleum-derived occlusive emollient; MOAH (Mineral Oil Aromatic Hydrocarbons) contamination risk from petrochemical refining — some PAHs are IARC Group 1 carcinogens; EU requires MOAH safety data; pharmaceutical-grade refining minimises but does not eliminate concern; occlusive — may aggravate acne-prone skin'),
        # Synthetic azo dyes not approved in EU/USA cosmetic colorant lists
        'ci 11680': ('Unapproved cosmetic colorant (Yellow AB / Fat Yellow 3)', 'NOT approved in EU Cosmetics Regulation Annex IV or USA FDA cosmetic colour additives list; monoazo dye — azo group can be reductively cleaved to aromatic amines, some of which are IARC carcinogens; no independent SCCS or FDA safety review; purely aesthetic colourant with no functional benefit'),
        'ci 12120': ('Unapproved cosmetic colorant (Solvent Red 1)', 'NOT approved in EU Cosmetics Regulation Annex IV or FDA cosmetic colour additives list; monoazo dye — azo reduction can produce aromatic amines of carcinogenicity concern; lacks regulatory safety review in major jurisdictions; purely aesthetic colourant'),
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

        # Potassium nitrite — curing salt, forms nitrosamines
        'potassium nitrite': ('Curing agent E249/INS 249', 'Curing salt in processed meats; can form N-nitrosamines (IARC Group 2A probable carcinogens) when heated to high temperatures, especially in combination with amines in meat; FSSAI and EU set strict maximum levels'),
        'e249': ('Potassium nitrite (E249)', 'Curing agent in processed meats; same nitrosamine formation risk as sodium nitrite (E250); FSSAI, EU and Codex permit at strict limits; avoid heavily cured meats in diet'),

        # Fragrance allergens — EU banned or mandatory declaration
        'butylphenyl methylpropional': ('Fragrance allergen (Lilial) — EU BANNED', 'BANNED across the EU since March 2022 (CMR 1B substance — reproductive toxicant); classified as toxic to reproduction in animal studies; still appears in many products sold outside Europe; avoid'),
        'lilial': ('Fragrance allergen (Butylphenyl Methylpropional) — EU BANNED', 'Same as Butylphenyl Methylpropional — banned in EU cosmetics since March 2022 due to reproductive toxicity; may persist on market in non-EU products and old stock; avoid'),

        # Chlorhexidine — antiseptic with allergy and ototoxicity risk
        'chlorhexidine digluconate': ('Antiseptic / disinfectant', 'Potent broad-spectrum antiseptic; EU Cosmetics Regulation restricts to 0.3% in mouthwash and 0.5% in other products; can cause severe allergic reactions including anaphylaxis (documented in medical settings); ototoxic — must not contact middle ear; not recommended for routine daily use'),
        'chlorhexidine': ('Antiseptic / disinfectant', 'Broad-spectrum antiseptic used in oral care and wound treatment; potential for severe contact allergy including anaphylaxis; ototoxic if enters middle ear; EU restricts concentration; suitable for therapeutic use, not daily cosmetic use'),
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

        # ── Soap Surfactants / Palm-derived ──────────────────────────────────
        'sodium palmate': ('Soap surfactant (saponified palm oil)', 'Alkaline pH (~9–10) disrupts skin acid mantle; potentially drying and irritating for sensitive/eczema skin; palm oil sourcing drives tropical deforestation, peatland destruction and endangered species habitat loss — RSPO certification needed'),
        'sodium palm kernelate': ('Soap surfactant (saponified palm kernel oil)', 'Milder than sodium palmate but same alkaline pH and potential barrier disruption for sensitive skin; carries palm oil environmental concerns — deforestation, biodiversity loss; RSPO certification of sourcing should be verified'),

        # ── Optical Brightener ────────────────────────────────────────────────
        'disodium distyrylbiphenyl disulfonate': ('Fluorescent optical brightener (Tinopal CBS / FWA-351)', 'Photoallergy risk — can cause UV-triggered photocontact allergic dermatitis in sensitised individuals; no therapeutic benefit, purely aesthetic; environmentally persistent — poorly biodegradable stilbene compound; aquatic toxicity; some in-vitro genotoxicity concerns under UV irradiation; deposited on skin and fabric from soap wash'),

        # ── Mild surfactants with nitrosamine potential ───────────────────────
        'sodium lauroyl sarcosinate': ('Mild amino acid-derived surfactant', 'Generally mild and well-tolerated; theoretical nitrosamine (N-nitrosoarcosine) formation potential when combined with nitrosating agents — EU Cosmetics Regulation restricts such combinations; compliant formulations present very low risk; approved for cosmetic use'),

        # ── PEG-based thickeners (1,4-dioxane concern) ───────────────────────
        'peg-150 distearate': ('PEG-based viscosity thickener', 'Ethoxylation manufacturing process may generate trace 1,4-dioxane — IARC Group 2B (possibly carcinogenic); FDA recommends <10 ppm limit in cosmetics; responsible manufacturers vacuum-strip to below safe thresholds; very high MW (PEG-150) means essentially no dermal penetration; safe within applicable purity specifications'),

        # ── Conditioning amines (nitrosamine potential) ───────────────────────
        'stearamidopropyl dimethylamine': ('Fatty acid amide tertiary amine conditioner', 'Tertiary amine — EU Cosmetics Regulation restricts from being combined with nitrosating agents (nitrosamine formation risk); SCCS assessed as safe in compliant rinse-off formulations; provides detangling, anti-static and conditioning on hair'),

        # ── Quaternary ammonium conditioning polymers ─────────────────────────
        'polyquaternium-113': ('Cationic polysaccharide conditioning polymer', 'A high-MW quat polymer with polysaccharide backbone — provides conditioning and frizz control; better environmental biodegradability than synthetic polyquaterniums; general class concern: quaternary ammonium compounds persist in aquatic environments and exhibit some antimicrobial toxicity to environmental microorganisms'),
        'quaternium-98': ('Quaternary ammonium salt conditioner', 'Cationic quat — provides conditioning, detangling and anti-static in hair care; class concerns: contact allergy in sensitised individuals (particularly hairdressers and healthcare workers); aquatic persistence — quats poorly biodegrade and accumulate in water systems; potential contribution to antimicrobial resistance at sub-lethal environmental concentrations; low consumer risk at rinse-off cosmetic concentrations'),

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
        
        # Mild acids (citric acid and lactic acid moved to generally_recognised — safe in food and cosmetics)

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
        
        # Acids (milder) — lactic acid and ascorbic acid moved to generally_recognised
        'malic acid': ('Acid E296', 'Tooth enamel erosion, mouth irritation, digestive upset in large amounts'),

        # Vitamins and minerals (when added) — ascorbic acid / tocopherol moved to generally_recognised
        'vitamin': ('Nutrient', 'Fortified — check if you need extra; excess of fat-soluble vitamins (A, D, E, K) can accumulate'),
        'mineral': ('Nutrient', 'Fortified — excess minerals can interfere with absorption of others'),
        
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
        'e402': ('Potassium alginate (E402)', 'Natural seaweed-derived thickener; CODEX and EU approved; generally safe'),
        'potassium alginate': ('Thickener E402/INS 402', 'Natural seaweed-derived gum; EU and CODEX approved; generally safe'),
        'e404': ('Calcium alginate (E404)', 'Natural seaweed-derived gelling agent; CODEX and EU approved; generally safe'),
        'calcium alginate': ('Thickener E404/INS 404', 'Natural seaweed-derived gelling agent; CODEX and EU approved; generally safe'),
        'locust bean gum': ('Thickener E410/INS 410', 'Natural carob seed gum; FSSAI, EU and CODEX approved; generally safe; high doses may cause flatulence'),
        'carob bean gum': ('Thickener E410/INS 410', 'Natural carob seed gum; EU and CODEX approved; generally safe'),
        'e410': ('Locust bean gum (E410)', 'Natural seed gum; FSSAI, EU and CODEX approved; generally safe; mild digestive effects at high doses'),
        'gum arabic': ('Emulsifier/thickener E414/INS 414', 'Natural acacia gum; FSSAI, EU and CODEX approved prebiotic fibre; generally safe; may cause bloating in sensitive individuals'),
        'acacia': ('Gum arabic (E414/INS 414)', 'Natural acacia gum; prebiotic fibre; FSSAI, EU and CODEX approved; generally safe'),
        'e414': ('Gum arabic (E414)', 'Natural acacia gum; FSSAI, EU and CODEX approved; prebiotic fibre with gut health benefits; may cause mild bloating'),
        'gellan gum': ('Thickener E418/INS 418', 'Fermentation-derived gelling agent; FSSAI, EU and FDA approved; generally safe; no significant adverse effects at food-use concentrations'),
        'e418': ('Gellan gum (E418)', 'Fermentation-derived gelling agent; FSSAI, EU and FDA approved; generally safe'),
        'pectin': ('Gelling agent E440/INS 440', 'Natural fruit-derived soluble fibre; FSSAI, EU and CODEX approved; excellent safety profile; minor digestive effects at very high doses'),
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

        # Sweeteners with considerations
        'mannitol': ('Sugar alcohol sweetener E421/INS 421', 'FSSAI, EU and CODEX approved; laxative effect when consumed above 20g/day; may cause gas and bloating'),
        'e421': ('Mannitol (E421)', 'Natural sugar alcohol; approved by FSSAI, EU and CODEX; laxative at >20g/day; may cause gas'),
        'isomalt': ('Sugar alcohol sweetener E953/INS 953', 'FSSAI, EU and CODEX approved; laxative effect above 25g/day; may cause flatulence and bloating'),
        'e953': ('Isomalt (E953)', 'Sugar-derived sweetener; FSSAI, EU and CODEX approved; laxative at high doses; mild digestive effects'),
        'xylitol': ('Sugar alcohol sweetener E967/INS 967', 'FSSAI, EU and FDA approved; dental health benefits; laxative above 40g/day; TOXIC TO DOGS — do not share products with pets'),
        'e967': ('Xylitol (E967)', 'FSSAI, EU and FDA approved sweetener; dental protective; laxative at high doses; TOXIC TO DOGS'),
        'stevia': ('Natural sweetener E960/INS 960', 'FSSAI, EU and FDA approved; zero-calorie natural sweetener; excellent safety record; some individuals report a slightly bitter aftertaste'),
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
        'e260': ('Acetic acid (E260)', 'FSSAI, EU and CODEX approved; safe at normal food use levels; minimal concerns'),
        'sodium acetate': ('Acidity regulator E262/INS 262', 'FSSAI, EU and CODEX approved; generally safe; watch sodium intake if on restricted diet'),
        'e262': ('Sodium acetate (E262)', 'FSSAI, EU and CODEX approved acidity regulator; generally safe'),
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

        # ── EU Mandatory Fragrance Allergens ─────────────────────────────────────
        # EU Cosmetics Regulation requires individual declaration of these 26 allergens above 0.001% (leave-on) / 0.01% (rinse-off)
        'limonene': ('Fragrance allergen — EU mandatory declaration', 'A citrus-derived terpene fragrance that is one of the most common causes of fragrance-related contact dermatitis; EU requires individual label declaration above 0.001% in leave-on products; also a common trigger for allergic reactions in sensitive individuals'),
        'linalool': ('Fragrance allergen — EU mandatory declaration', 'A naturally occurring floral terpene alcohol found in lavender, coriander and bergamot; one of the top causes of fragrance allergy; EU mandates individual declaration above threshold; linalool can oxidise on storage to form stronger sensitisers'),
        'benzyl salicylate': ('Fragrance allergen — EU mandatory declaration', 'A synthetic or naturally occurring fragrance ester with a floral balsamic scent; EU requires individual label declaration; associated with contact allergy and sensitization; used in perfumes, lotions and shampoos'),
        'hexyl cinnamal': ('Fragrance allergen — EU mandatory declaration', 'A synthetic jasmine-scented aldehyde fragrance; EU mandates individual declaration above threshold; can cause contact allergic dermatitis in sensitized individuals; common in hair care and personal care products'),
        'eugenol': ('Fragrance allergen — EU mandatory declaration', 'A natural phenol from clove oil; EU mandatory declaration allergen; common cause of contact dermatitis in dental and cosmetic products; also a fragrance used in personal care'),
        'geraniol': ('Fragrance allergen — EU mandatory declaration', 'A natural rose-scented terpene alcohol from geranium and palmarosa oil; EU mandatory allergen declaration; can oxidise on storage to form stronger skin sensitisers'),
        'citronellol': ('Fragrance allergen — EU mandatory declaration', 'A natural rose and citrus-scented terpene alcohol; EU mandatory declaration allergen; can cause contact allergy in sensitive individuals'),
        'coumarin': ('Fragrance allergen — EU mandatory declaration', 'A natural lactone from tonka beans and sweet clover with a sweet vanilla-hay scent; EU mandatory allergen declaration; some animal studies raised hepatotoxicity concerns at very high doses; restricted in food applications'),
        'isoeugenol': ('Fragrance allergen — EU mandatory declaration', 'A structural isomer of eugenol found in ylang-ylang and nutmeg essential oils; EU mandatory allergen declaration; strong sensitiser — has been banned in cosmetics in some jurisdictions'),
        'cinnamyl alcohol': ('Fragrance allergen — EU mandatory declaration', 'A cinnamon-scented alcohol that is an EU mandatory allergen; can cause contact allergy and is a known skin sensitiser at higher concentrations'),
        'cinnamal': ('Fragrance allergen — EU mandatory declaration', 'Cinnamic aldehyde, the primary aroma compound in cinnamon; EU mandatory allergen declaration; strong sensitiser in cosmetics; restricted in leave-on products'),
        'farnesol': ('Fragrance allergen — EU mandatory declaration', 'A natural sesquiterpene alcohol with a sweet floral scent; EU mandatory allergen declaration; can cause contact allergy in sensitive individuals'),
        'hydroxycitronellal': ('Fragrance allergen — EU mandatory declaration', 'A synthetic lily-of-the-valley scented aldehyde; EU mandatory declaration allergen; can cause contact sensitisation and allergic reactions'),
        'amyl cinnamal': ('Fragrance allergen — EU mandatory declaration', 'A synthetic jasmine-scented fragrance aldehyde; EU mandatory allergen declaration; contact allergy potential in sensitive individuals'),
        'benzyl cinnamate': ('Fragrance allergen — EU mandatory declaration', 'A fragrance ester with a sweet balsamic scent; EU mandatory declaration allergen; found in Peru balsam derivatives; sensitiser in some individuals'),
        'benzyl benzoate': ('Fragrance allergen — EU mandatory declaration', 'A fragrance ester also used as an antiparasitic agent (scabies, lice); EU mandatory declaration allergen; contact allergy potential; some reports of skin irritation'),
        'alpha-isomethyl ionone': ('Fragrance allergen — EU mandatory declaration', 'A synthetic violet-scented fragrance; EU mandatory allergen declaration; contact dermatitis potential in sensitised individuals'),
        'methyl 2-octynoate': ('Fragrance allergen — EU mandatory declaration', 'A powerful synthetic fruity fragrance chemical; EU mandatory declaration allergen; strong sensitiser at higher concentrations'),
        'anise alcohol': ('Fragrance allergen — EU mandatory declaration', 'Anisyl alcohol with sweet anise scent; EU mandatory declaration allergen; potential sensitiser'),

        # ── Quaternary Ammonium Conditioning Agents ───────────────────────────────
        'behentrimonium chloride': ('Quaternary ammonium conditioner', 'A positively charged (cationic) conditioning agent used in hair conditioners and treatments derived from rapeseed or coconut oil; EU restricts to 3% in rinse-off and 1% in leave-on products; may cause skin sensitisation and eye irritation at higher concentrations; environmental persistence concerns'),
        'behentrimonium methosulfate': ('Quaternary ammonium conditioner', 'A milder alternative to behentrimonium chloride; widely used in natural-oriented conditioners and hair masks; generally better tolerated than chloride salts of quaternary ammonium compounds'),
        'cetrimonium chloride': ('Quaternary ammonium conditioner', 'A cationic conditioning surfactant used to reduce hair frizz and static; EU restricts to 0.25% in rinse-off and is banned in leave-on products above 0.25%; can cause contact allergy, eye and skin irritation; toxic to aquatic organisms'),
        'cetrimonium bromide': ('Quaternary ammonium conditioner', 'A positively charged conditioning surfactant; similar profile to cetrimonium chloride; EU restricts concentration; antimicrobial activity at higher concentrations; potential irritant and sensitiser'),
        'quaternium-33': ('Quaternary ammonium conditioning agent', 'A conditioning polymeric quaternary ammonium compound used in hair products; generally safe at cosmetic use concentrations; some potential for skin sensitisation; provides anti-static and smoothing effects'),
        'quaternium-18': ('Quaternary ammonium compound', 'A conditioning quaternary ammonium compound used in hair care; provides conditioning and anti-static effects; may cause irritation at high concentrations'),
        'guar hydroxypropyltrimonium chloride': ('Cationic guar conditioner', 'A quaternized guar gum derivative used as a conditioning polymer in shampoos and conditioners; generally well tolerated; provides slip and detangling properties; biodegradable biopolymer base'),

        # ── Ethoxylated Compounds (1,4-Dioxane risk) ─────────────────────────────
        'trideceth-6': ('Ethoxylated surfactant/emulsifier', 'A non-ionic surfactant made by ethoxylating tridecanol; ethoxylation may introduce trace 1,4-dioxane contamination (IARC Group 2B possible carcinogen); generally mild surfactant at permitted levels; manufacturers can reduce dioxane via vacuum stripping'),
        'trideceth-': ('Ethoxylated surfactant (trideceth series)', 'Non-ionic emulsifier from the trideceth series; same ethoxylation-related 1,4-dioxane contamination risk as other ethoxylates; mild and effective surfactant'),
        'peg-100 stearate': ('PEG emulsifier (ethoxylated)', 'A PEG-based emulsifier from ethoxylation of stearic acid; potential trace 1,4-dioxane (IARC Group 2B) contamination from ethoxylation process; approved for cosmetic use'),
        'ceteareth-': ('Ethoxylated emulsifier (ceteareth series)', 'Non-ionic emulsifier from ethoxylation of cetearyl alcohol; potential 1,4-dioxane contamination from ethoxylation; widely used emulsifier at approved concentrations'),
        'laureth-': ('Ethoxylated lauryl alcohol surfactant series', 'Non-ionic surfactant from ethoxylation of lauryl alcohol; same 1,4-dioxane contamination risk as SLES; milder than SLS; widely used in cleansers'),
        'steareth-': ('Ethoxylated stearyl alcohol emulsifier series', 'Non-ionic emulsifier from ethoxylation of stearyl alcohol; potential 1,4-dioxane contamination; widely used cosmetic emulsifier'),

        # ── Solvents ──────────────────────────────────────────────────────────────
        'isopropyl alcohol': ('Solvent / antiseptic (IPA)', 'A petroleum-derived short-chain alcohol used as a solvent and antiseptic in cosmetics, hand sanitisers and pharmaceuticals; very drying to skin with repeated use; can disrupt the skin barrier and cause irritation, especially in sensitive or eczema-prone individuals; not for ingestion'),
        'isopropanol': ('Isopropyl alcohol / IPA', 'Same as isopropyl alcohol; drying to skin and scalp with repeated use; can compromise the skin barrier; used as a solvent and antiseptic in cosmetics'),

        # ── Cosmetic Emollients / Lipids ──────────────────────────────────────────
        'cetyl alcohol': ('Fatty alcohol emollient/emulsifier', 'A waxy fatty alcohol derived from coconut or palm oil; safe and well-tolerated; classified as an allergen only in rare cases; despite the word "alcohol" it is not drying and actually acts as a moisturiser'),
        'cetearyl alcohol': ('Fatty alcohol emollient/emulsifier', 'A blend of cetyl and stearyl alcohols; waxy emollient derived from coconut or palm oil; generally very well tolerated; occasional contact allergy reported in rare cases'),
        'stearyl alcohol': ('Fatty alcohol emollient/emulsifier', 'A naturally derived fatty alcohol used as an emollient and thickener in creams; generally very well tolerated; safe'),
        'behenyl alcohol': ('Fatty alcohol emollient/emulsifier', 'A long-chain fatty alcohol used as an emollient and thickener in hair and skin care; derived from rapeseed or coconut; generally very well tolerated'),
        'myristyl alcohol': ('Fatty alcohol emollient/emulsifier', 'A fatty alcohol derived from coconut oil; safe emollient and thickener; generally well tolerated'),
        'octyldodecanol': ('Fatty alcohol emollient', 'A branched-chain fatty alcohol used as an emollient and solubiliser in cosmetics; safe and non-comedogenic; well tolerated'),

        # ── Silicones (non-cyclic) ────────────────────────────────────────────────
        'phenyl trimethicone': ('Linear silicone (non-cyclic)', 'A phenyl-modified silicone used in hair and skin products for high-shine effects; environmental persistence but less restricted than cyclic silicones D4/D5; generally safe for topical use'),
        'trimethylsilylamodimethicone': ('Functional silicone (non-cyclic)', 'A trimethylsilyl-terminated amino silicone used in hair conditioning; provides long-lasting anti-frizz and shine; non-cyclic — less restricted than D4/D5; generally safe'),
        'bis-aminopropyl dimethicone': ('Amino silicone (non-cyclic)', 'A modified silicone with reactive amino groups for hair conditioning and repair; non-cyclic; generally safe'),
        # ── Ethoxylated emulsifiers (trace 1,4-dioxane concern) ────────────────
        'polysorbate 20': ('Emulsifier E432/INS 432', 'Non-ionic ethoxylated emulsifier; ethoxylation may introduce trace 1,4-dioxane (IARC Group 2B possible carcinogen); safe within approved limits'),
        'polysorbate 40': ('Emulsifier E434/INS 434', 'Non-ionic ethoxylated emulsifier; trace 1,4-dioxane possible; safe within approved limits'),
        'polysorbate 60': ('Emulsifier E435/INS 435', 'Non-ionic ethoxylated emulsifier in baked goods; trace 1,4-dioxane possible; safe within approved limits'),
        'polysorbate 65': ('Emulsifier E436/INS 436', 'Non-ionic ethoxylated emulsifier; safe within approved limits'),
        'polysorbate 80': ('Emulsifier E433/INS 433', 'Widely used non-ionic ethoxylated emulsifier in food, vaccines and cosmetics; trace 1,4-dioxane (IARC Group 2B) possible from ethoxylation; safe within approved limits'),
        'e432': ('Polysorbate 20 (E432)', 'Ethoxylated emulsifier; trace 1,4-dioxane possible; safe within approved limits'),
        'e433': ('Polysorbate 80 (E433)', 'Widely used ethoxylated emulsifier; trace 1,4-dioxane possible; safe within approved limits'),
        'e434': ('Polysorbate 40 (E434)', 'Ethoxylated emulsifier; safe within approved limits'),
        'e435': ('Polysorbate 60 (E435)', 'Ethoxylated emulsifier in baked goods; safe within approved limits'),
        'e436': ('Polysorbate 65 (E436)', 'Ethoxylated emulsifier; safe within approved limits'),

        # ── Animal/insect-derived — dietary restrictions ────────────────────────
        'gelatin': ('Animal-derived gelling protein E441/INS 441', 'Protein from animal collagen (bones/cartilage); used in gummies, jellies and capsules; NOT suitable for vegetarians, vegans or halal/kosher'),
        'e441': ('Gelatin (E441)', 'Animal collagen-derived gelling agent; not suitable for vegetarians, vegans or halal/kosher requirements'),
        'shellac': ('Insect-derived glazing agent E904/INS 904', 'Natural resin from lac insects; high-gloss coating on confectionery and tablets; not vegan; India is the world\'s largest producer; safe'),
        'beeswax': ('Natural glazing agent E901/INS 901', 'Wax from honeybees used to glaze confectionery and fruit; safe; not vegan'),

        # ── Nucleotide flavour enhancers (gout concern) ────────────────────────
        'guanylic acid': ('Nucleotide flavour enhancer E626/INS 626', 'Naturally from dried mushrooms and fish; amplifies umami taste; high purine content — avoid if you have gout or hyperuricaemia; safe for most people'),
        'e626': ('Guanylic Acid (E626)', 'Nucleotide umami enhancer; high purine — avoid with gout; safe for most'),
        'inosinic acid': ('Nucleotide flavour enhancer E630/INS 630', 'Natural nucleotide from meat and fish; high purine — avoid with gout; safe for most'),
        'e630': ('Inosinic Acid (E630)', 'Nucleotide umami enhancer; high purine — avoid with gout; safe for most'),

        # ── Sugar alcohols with laxative effects ──────────────────────────────
        'sorbitol': ('Sugar alcohol sweetener E420/INS 420', 'Naturally in apples, pears and other fruits; laxative effects at >50g/day — EU label warning required'),
        'mannitol': ('Sugar alcohol sweetener E421/INS 421', 'Natural sugar alcohol from mushrooms; more pronounced laxative effects than sorbitol; EU label warning required'),
        'maltitol': ('Sugar alcohol sweetener E965/INS 965', 'Sugar alcohol in sugar-free confectionery; laxative effects at >40g/day; EU label warning required'),
        'lactitol': ('Sugar alcohol sweetener E966/INS 966', 'Sugar alcohol from lactose; laxative at high intake; not for lactose-intolerant individuals'),
        'xylitol': ('Sugar alcohol sweetener E967/INS 967', 'Natural sugar alcohol with proven dental benefits; laxative at high intake; CAUTION — extremely toxic to dogs'),
        'isomalt': ('Sugar alcohol sweetener E953/INS 953', 'Sugar alcohol from sucrose; laxative at high intake; EU label warning required'),

        # ── Konjac (EU children restriction) ─────────────────────────────────
        'konjac': ('High-fibre gelling agent E425/INS 425', 'Polysaccharide from konjac plant; EU restricts certain firm jelly formats for children due to choking risk; otherwise safe'),
        'konjac flour': ('High-fibre gelling agent E425/INS 425', 'EU restricts certain firm jelly formats for children; safe in other uses'),
        'konjac gum': ('High-fibre thickener E425/INS 425', "EU restricts certain children's jelly formats; safe"),

        # ── Misc worth noting ─────────────────────────────────────────────────
        'nitrous oxide': ('Propellant E942/INS 942', 'Whipped cream canister propellant; safe in food; dangerous when misused recreationally as a drug'),
        'l-cysteine': ('Dough conditioner E920/INS 920', 'Amino acid used to reduce bread dough mixing time; often sourced from hair or feathers — check vegan/vegetarian compliance; safe'),
        'propylene glycol alginate': ('Modified seaweed gum E405/INS 405', 'Contains propylene glycol moiety; used in salad dressings and beer foam; safe at approved levels'),

        # ── UV Filters with mild concerns ─────────────────────────────────────
        'butyl methoxydibenzoylmethane': ('UVA sunscreen filter (Avobenzone)', 'Broad-spectrum UVA1 filter; photodegrades in sunlight when used alone — combine with photostabilisers; some skin penetration detected in studies but no confirmed safety risk at approved levels; FDA (3%) and EU (5%) approved'),
        'avobenzone': ('UVA sunscreen filter (Butyl Methoxydibenzoylmethane)', 'Same as Butyl Methoxydibenzoylmethane — the most widely used UVA filter; photounstable alone; safe within approved limits'),

        # ── PEG-modified silicone compounds ──────────────────────────────────
        'bis-peg-12 dimethicone beeswax': ('PEG-modified silicone wax emulsifier', 'PEG compound — ethoxylation may introduce trace 1,4-dioxane (IARC Group 2B possible carcinogen); also not vegan (contains beeswax derivative); safe at cosmetic-use concentrations within approved limits'),
        'bis-peg': ('PEG-modified silicone compound', 'PEG-modified silicone; ethoxylation may introduce trace 1,4-dioxane; generally safe at approved cosmetic concentrations'),

        # ── Cosmetic azo dye lakes (worth knowing in cosmetics) ───────────────
        'red 28 lake': ('Synthetic xanthene dye lake (D&C Red 28 / CI 45410)', 'Cosmetic colorant in lipsticks; FDA-approved; some photosensitisation concern at high concentrations; not permitted around eyes in the USA'),
        'red 28': ('Synthetic xanthene dye (D&C Red 28)', 'Cosmetic colorant; FDA-approved; some photosensitisation potential; not for eye area in USA'),

        # ── Quaternary ammonium conditioning agents ───────────────────────────
        'linoleamidopropyl pg-dimonium chloride phosphate': ('Cationic conditioning agent (quat)', 'Quaternary ammonium compound derived from linoleic acid; antistatic conditioner for hair and skin; safe at cosmetic concentrations; environmental persistence noted for quats'),
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
        'argania spinosa': ('Argan oil (Argania spinosa kernel oil)', 'Cold-pressed from Moroccan argan tree kernels; rich in oleic acid, linoleic acid and tocopherols; deeply nourishing for hair and skin; antioxidant; safe and well-tolerated'),
        'aqua': ('Water (purified)', 'Purified water — the universal solvent and base of most cosmetic and personal care formulations; safe'),
        'kokum butter': ('Natural Indian plant butter (Garcinia indica)', 'Non-comedogenic (0 rating), deeply emollient, anti-inflammatory; traditional Ayurvedic ingredient; excellent for dry, eczema-prone and acne-prone skin; rich in stearic and oleic acid; melts at skin temperature without greasy residue; safe and well-tolerated'),
        'oenocarpus bataua fruit oil': ('Amazonian patauá palm fruit oil', 'Exceptionally rich in oleic acid (72–80%) — one of the richest natural omega-9 sources; excellent hair conditioning and penetration; anti-inflammatory and antioxidant properties; sustainably harvested from Amazon rainforest; safe, well-tolerated, no known allergenicity'),
        'hydrolyzed plukenetia volubilis seed extract': ('Hydrolyzed sacha inchi seed extract (Amazonian)', 'Rich source of omega-3, omega-6 and amino acid peptides; conditions and repairs hair cuticle; retains moisture; antioxidant; sustainably sourced from Amazonian sacha inchi plant; safe and well-tolerated'),
        'sodium cocoyl isethionate': ('Mild coconut-derived syndet surfactant', 'pH-compatible with skin acid mantle (pH ~5.5–6.5); one of the mildest surfactants available; non-stripping; clinically proven lower irritation than SLS/SLES; biodegradable; preferred in dermatologically tested sensitive skin formulations; safe for all skin types'),
        'capryloyl/caproyl methyl glucamide': ('Mild sugar-derived surfactant (glucamide family)', 'Produced from glucose and coconut fatty acids; very low irritation; rapidly biodegradable; renewable raw material base; no ethoxylation so no 1,4-dioxane risk; ECOCERT-compatible; safe'),
        'lauroyl/myristoyl methyl glucamide': ('Mild sugar-derived surfactant (glucamide family)', 'From glucose and coconut C12–C14 fatty acids; gentle, creamy foam with conditioning properties; biodegradable; renewable; suitable for sensitive skin formulations; safe'),
        'coco-glucoside': ('Mild coconut and sugar-derived non-ionic surfactant', 'Alkyl glucoside from renewable sources; exceptionally mild — ophthalmologically and dermatologically tested; biodegradable; no ethoxylation contamination risk; ECOCERT/COSMOS approved; safe for baby products and sensitive skin'),
        'glycol distearate': ('Pearlising agent (stearic acid ester)', 'Responsible for pearl shimmer appearance in shampoos and body washes; mild emollient; well-tolerated; low sensitisation potential; approved by EU, FDA and FSSAI; safe at cosmetic use levels'),
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

        # ── Dual-use ingredients moved here from worth_knowing (safe in both food and cosmetics) ──
        'lactic acid': ('Natural fermentation acid (E270 / AHA)', 'Naturally produced by fermentation; found in yoghurt, sauerkraut and pickles; used as a preservative in food and as an alpha-hydroxy acid (AHA) exfoliant in skincare; safe and widely used in both contexts'),
        'citric acid': ('Natural fruit acid (E330)', 'The primary acid in citrus fruits; produced commercially by fermenting sugars; widely used as a pH adjuster, preservative and flavour agent in food, beverages and cosmetics; very safe and widely used'),
        'ascorbic acid': ('Vitamin C (E300)', 'Essential water-soluble vitamin naturally found in citrus fruits, berries and vegetables; used as a nutritional supplement, antioxidant preservative and skin-brightening agent; safe and nutritionally beneficial'),
        'tocopherol': ('Vitamin E (E306/E307)', 'Natural fat-soluble antioxidant found in nuts, seeds and vegetable oils; used as a natural preservative in food products and as a skin-conditioning antioxidant in cosmetics; safe and nutritionally beneficial'),
        'tocopheryl acetate': ('Vitamin E ester (tocopheryl acetate)', 'A stable ester form of Vitamin E widely used in cosmetics as an antioxidant and skin-conditioning agent; converts to vitamin E on the skin; safe'),

        # ── Cosmetic Actives — Generally Recognised (new additions) ──────────────
        'cetyl esters': ('Waxy emollient (synthetic jojoba substitute)', 'A mixture of long-chain fatty esters used as a skin and hair emollient; mimics the feel and function of spermaceti wax; biodegradable; CIR panel confirmed safe for cosmetic use; very well tolerated'),
        'hydroxypropyltrimonium hydrolyzed wheat protein': ('Cationic wheat protein conditioning agent', 'A quaternized hydrolyzed wheat protein that bonds to damaged hair via electrostatic attraction; repairs hair, reduces breakage and improves smoothness; safe at cosmetic use concentrations; contains quaternary ammonium group — environmental persistence noted'),
        'hydroxypropyltrimonium hydrolyzed': ('Cationic hydrolyzed protein conditioning agent', 'A quaternized hydrolyzed protein (wheat, rice, or corn source) for hair conditioning; bonds to hair and skin; safe at cosmetic concentrations'),
        'hydrolyzed wheat protein': ('Wheat-derived protein conditioning ingredient', 'Wheat protein broken down into smaller peptide fragments that can penetrate the hair shaft; strengthens and conditions hair; safe; wheat-allergic individuals should use caution with topical exposure'),
        'hydrolyzed keratin': ('Keratin protein hydrolysate for hair repair', 'Hydrolyzed keratin peptides from wool or hair; fill and temporarily repair gaps in the hair cuticle; strengthen and smooth the hair shaft; safe and effective for damaged hair'),
        'hydrolyzed collagen': ('Hydrolyzed collagen peptides (skin and hair conditioning)', 'Collagen broken into smaller peptides; used to add film-forming, moisturising and conditioning properties; safe; animal-derived unless labelled vegan'),
        'arginine': ('Natural amino acid (skin and hair conditioning)', 'An essential amino acid found naturally in the body; used in cosmetics to condition hair and support skin barrier function; helps repair damaged hair cuticles; safe; naturally present in foods like meat, dairy and nuts'),
        'serine': ('Natural amino acid (humectant and conditioner)', 'A non-essential amino acid naturally found in skin and hair; used as a humectant and skin-conditioning agent in cosmetics; safe and well-tolerated; part of the skin Natural Moisturising Factor (NMF)'),
        'glutamic acid': ('Natural amino acid (skin conditioning)', 'Naturally occurring amino acid found in proteins; used as a humectant and skin conditioner in cosmetics; safe; related to glutamate found in fermented foods'),
        'glycine': ('Natural amino acid (skin and hair conditioning)', 'The simplest amino acid; used in cosmetics for skin conditioning and buffering; safe; found naturally in collagen-rich foods'),
        'proline': ('Natural amino acid (collagen support)', 'Amino acid important in collagen synthesis; used in skincare to support skin elasticity; safe and naturally occurring in foods'),
        'threonine': ('Natural amino acid', 'Essential amino acid used in cosmetics for hair conditioning and moisturising; safe'),
        'alanine': ('Natural amino acid (skin conditioning)', 'Non-essential amino acid used as a humectant in cosmetics; safe and naturally occurring'),
        'leucine': ('Natural amino acid (skin conditioning)', 'Essential amino acid used in cosmetics for hair and skin conditioning; safe'),
        'isoleucine': ('Natural amino acid (skin conditioning)', 'Essential amino acid used in cosmetics; safe'),
        'valine': ('Natural amino acid (skin conditioning)', 'Essential amino acid used in cosmetics for hair strengthening; safe'),
        'lysine': ('Natural amino acid (skin and hair conditioning)', 'Essential amino acid used in hair care to strengthen hair protein structure; safe'),
        'cysteine': ('Natural amino acid (hair repair)', 'A sulfur-containing amino acid critical for keratin structure; used in hair treatments to improve strength; safe'),
        'cystine': ('Natural amino acid (hair strengthening)', 'The oxidised dimer of cysteine; contributes to the disulfide bonds in keratin; safe'),
        'histidine': ('Natural amino acid (skin conditioning)', 'Essential amino acid with antioxidant properties; used in skincare; safe'),
        'methionine': ('Natural amino acid (antioxidant)', 'Sulfur-containing essential amino acid; used as an antioxidant in cosmetics; safe'),
        'phenylalanine': ('Natural amino acid', 'Essential amino acid used in cosmetic conditioning; safe; individuals with PKU must monitor dietary phenylalanine'),
        'tryptophan': ('Natural amino acid', 'Essential amino acid; safe for cosmetic use'),
        'tyrosine': ('Natural amino acid (skin conditioning)', 'Non-essential amino acid; used in cosmetics; safe'),

        # ── Natural Glyceryl Fatty Acid Esters ───────────────────────────────────
        'glyceryl linoleate': ('Natural skin lipid (glyceryl ester of linoleic acid)', 'A naturally occurring glycerol ester of linoleic acid (omega-6); restores the skin lipid barrier; anti-inflammatory; safe and compatible with skin; found naturally in many plant oils'),
        'glyceryl oleate': ('Natural skin lipid (glyceryl ester of oleic acid)', 'A glycerol ester of oleic acid (omega-9); an emollient and emulsifier naturally present in olive and sunflower oil; safe and skin-compatible; moisturising'),
        'glyceryl linolenate': ('Natural skin lipid (glyceryl ester of linolenic acid)', 'A glycerol ester of alpha-linolenic acid (omega-3); skin barrier-restoring and anti-inflammatory lipid; safe and naturally found in flaxseed oil'),
        'glyceryl stearate': ('Natural emollient/emulsifier (glyceryl ester)', 'A widely used emulsifier and emollient derived from glycerol and stearic acid; occurs naturally in the human body; CIR confirmed safe; excellent tolerability in cosmetics'),
        'glyceryl behenate': ('Waxy emollient/emulsifier (glyceryl ester)', 'A glycerol ester of behenic acid used as a solid emollient and binder in cosmetics; safe; derived from rapeseed oil or coconut oil'),
        'glyceryl caprylate': ('Skin-compatible emollient and preservative booster', 'A glycerol ester of caprylic acid derived from coconut oil; used as an emollient and natural preservative booster (antimicrobial activity against gram-positive bacteria and Candida); safe; commonly used in natural formulations'),
        'glyceryl caprate': ('Skin-compatible emollient (glyceryl ester)', 'A glycerol ester of capric acid; emollient and mild preservative-boosting properties; safe; derived from coconut oil'),

        # ── Ceramide-like and Barrier Lipids ─────────────────────────────────────
        '2-oleamido-1,3-octadecanediol': ('Ceramide-like skin barrier lipid (oleamide diol)', 'A synthetic ceramide analogue that mimics the structure of natural skin ceramides; reinforces the skin lipid barrier, reduces transepidermal water loss and soothes dry skin; safe and well tolerated; used in high-performance barrier repair creams'),
        'ceramide np': ('Natural skin ceramide (type NP)', 'Ceramide NP (N-palmitoyl sphinganine) is the most abundant ceramide in human skin; restores the lamellar skin barrier; excellent tolerability; safe'),
        'ceramide ap': ('Natural skin ceramide (type AP)', 'Ceramide AP (N-palmitoyldihydrosphingosine) is a key skin barrier ceramide; barrier-restoring and moisturising; safe'),
        'ceramide eop': ('Natural skin ceramide (type EOP)', 'Ester-linked omega-hydroxy ceramide; forms the structural backbone of stratum corneum lamellar sheets; critical for skin barrier integrity; safe'),
        'phytosphingosine': ('Sphingoid base (natural ceramide precursor)', 'A sphingosine analog naturally found in skin; antimicrobial, anti-inflammatory and ceramide-building properties; safe'),
        'cholesterol': ('Natural skin lipid (barrier component)', 'One of the three essential stratum corneum lipids (with ceramides and fatty acids); restores the lamellar lipid barrier; bioidentical to skin lipids; safe'),

        # ── Cosmetic Polymers / Film-formers ─────────────────────────────────
        'polyethylene': ('Synthetic polymer wax (texture modifier)', 'High-molecular-weight polyethylene wax used in lipsticks and foundations; safe for topical use; different from microplastic PE beads (banned in rinse-offs)'),
        'polysilicone-11': ('Cross-linked silicone elastomer (film-former)', 'Silicone polymer used in long-wear makeup; film-former and suspension agent; not absorbed; safe'),
        'nylon-12': ('Synthetic polyamide polymer (texture agent)', 'Soft-focus texture agent and film-former in foundations and eyeshadows; not absorbed; safe for topical use'),
        'methyl methacrylate crosspolymer': ('Acrylic polymer (soft-focus agent)', 'Cross-linked acrylic polymer for mattifying and blurring effects in foundations; not absorbed; safe'),
        'acrylates/c10-30 alkyl acrylate crosspolymer': ('Synthetic thickener and emulsion stabiliser', 'Long-chain modified Carbomer analogue used in sunscreens and moisturisers; safe for topical use'),
        'acrylates': ('Acrylic polymer thickener/stabiliser', 'Cross-linked acrylic polymer used to thicken and stabilise cosmetic emulsions; safe'),

        # ── Cosmetic Emollients ───────────────────────────────────────────────
        'caprylic/capric triglyceride': ('Light coconut-derived emollient (CCT)', 'Hypoallergenic, non-comedogenic emollient from coconut oil; excellent skin tolerability; widely regarded as one of the best cosmetic emollients; safe'),
        'caprylic capric triglyceride': ('Light coconut-derived emollient (CCT)', 'Non-comedogenic coconut-derived emollient; hypoallergenic; safe and very well-tolerated'),
        'polyhydroxystearic acid': ('Emulsifier/dispersing agent for mineral UV filters', 'Used to stabilise zinc oxide and titanium dioxide in sunscreens; safe for topical use'),
        'pentaerythrityl tetra-di-t-butyl hydroxyhydrocinnamate': ('Hindered phenol antioxidant (formula stabiliser)', 'Trace-level antioxidant added to protect cosmetic oils and polymers from oxidation; not a skin active; safe'),
        'tocopheryl acetate': ('Vitamin E acetate (antioxidant and skin conditioner)', 'Stable esterified Vitamin E; antioxidant and emollient; converts to free tocopherol on skin; very safe and well-tolerated'),

        # ── Cosmetic Minerals / Clays ─────────────────────────────────────────
        'mica': ('Natural mineral pigment (shimmer/sparkle)', 'Phyllosilicate mineral used in makeup for light-reflective shimmer; safe topically; ethical sourcing concern in supply chain'),
        'dicalcium phosphate': ('Mineral abrasive / opacifier / calcium source', 'Used in toothpaste and cosmetics; provides dietary calcium in food; safe'),
        'stearalkonium bentonite': ('Organically-modified clay (rheology modifier)', 'Quat-modified bentonite clay; thickens and stabilises anhydrous cosmetic formulations; safe'),

        # ── UV Filters (generally safe) ───────────────────────────────────────
        'ethylhexyl salicylate': ('UVB sunscreen filter (Octyl Salicylate)', 'Approved UVB absorber; well-tolerated; safe within approved limits (up to 5% EU)'),
        'octyl salicylate': ('UVB sunscreen filter (Ethylhexyl Salicylate)', 'Same as ethylhexyl salicylate; EU and FDA approved UVB filter; safe'),
        'phenylbenzimidazole sulfonic acid': ('Water-soluble UVB sunscreen filter (Ensulizole)', 'Approved UVB filter (EU up to 8%, FDA up to 4%); water-soluble; safe and well-tolerated'),
        'ensulizole': ('UVB sunscreen filter (Phenylbenzimidazole Sulfonic Acid)', 'Water-soluble UVB filter; safe and approved'),

        # ── Hyaluronic Acid Variants ──────────────────────────────────────────
        'sodium acetylated hyaluronate': ('Acetylated hyaluronic acid (enhanced HA)', 'Lipophilic modified HA with longer-lasting skin surface retention; superior moisturisation to standard HA; safe'),
        'sodium hyaluronate crosspolymer': ('Cross-linked hyaluronic acid (film-forming HA)', 'High-molecular-weight cross-linked HA; forms a long-lasting moisture film on skin surface; safe'),
        'hydrolyzed sodium hyaluronate': ('Low molecular weight HA fragments (penetrating HA)', 'Small HA fragments that penetrate deeper into stratum corneum; deeper hydration than standard HA; safe'),
        'hydrolyzed hyaluronic acid': ('Low molecular weight HA (penetrating)', 'Enzymatically hydrolysed HA for deeper skin penetration; safe'),

        # ── Surfactants / Emulsifiers (safe) ──────────────────────────────────
        'sodium lauroyl lactylate': ('Mild biodegradable surfactant/emulsifier', 'Derived from coconut lauric acid and lactic acid; milder than SLS; excellent tolerability; safe'),

        # ── Misc safe cosmetic ingredients ────────────────────────────────────
        'propylene carbonate': ('Cosmetic solvent and plasticiser', 'Organic solvent used to dissolve and stabilise cosmetic ingredients; good skin tolerability; safe'),
        'red 7 lake': ('Cosmetic azo dye lake (D&C Red 7 / CI 15850)', 'EU and FDA approved cosmetic colorant in lipsticks and makeup; safe for external cosmetic use'),
        'red 7': ('Cosmetic azo dye (D&C Red 7 / CI 15850:1)', 'Approved cosmetic colorant; safe for external use'),
        'red 6': ('Cosmetic azo dye (D&C Red 6 / CI 15850)', 'FDA-approved cosmetic colorant in lipsticks; safe for external cosmetic application'),
        'ci 15850': ('Cosmetic azo dye colorant (Red 6 / Red 7)', 'Lithol Rubine family dye; EU and FDA approved for cosmetic use; safe'),
        'ci 77491': ('Red Iron Oxide mineral pigment', 'Natural inorganic mineral pigment; chemically inert; safe; approved globally for cosmetics and food'),
        'ci 77492': ('Yellow Iron Oxide mineral pigment', 'Natural inorganic mineral pigment; chemically inert; safe; approved globally'),
        'sphingosine': ('Natural ceramide component', 'A sphingoid base naturally present in human skin; precursor to ceramide synthesis; safe at cosmetic concentrations'),

        # ── Additional Cosmetic Waxes and Polymers ───────────────────────────────
        'polybutene': ('Synthetic polyolefin polymer (gloss and slip agent)', 'High-molecular-weight polyisobutylene used in lipsticks and balms to provide gloss, slip and adhesion; not absorbed through skin; no skin penetration; approved by FDA and EU Cosmetics Regulation; safe'),
        'cera microcristallina': ('Microcrystalline wax (refined petroleum wax)', 'A highly refined, odourless petroleum-derived wax used in lipsticks and creams as a thickener, binder and texture modifier; different from paraffin wax — has finer crystal structure; FDA GRAS; EU approved; safe'),
        'microcrystalline wax': ('Refined petroleum wax (thickener / binder)', 'Same as Cera Microcristallina; highly refined petroleum wax with no impurities; widely used in lip products and stick cosmetics; FDA GRAS and EU-approved; safe'),

        # ── Additional Cosmetic Natural Oils and Butters ─────────────────────────
        'theobroma grandiflorum seed butter': ('Cupuaçu butter (natural Amazonian seed butter)', 'Butter extracted from the seeds of Theobroma grandiflorum (cupuaçu fruit, related to cacao); rich in fatty acids (oleic, stearic, arachidic, palmitic); emollient and moisture-sealing; absorbs faster than shea butter; safe and well tolerated; sustainably sourced from Brazil'),
        'cupuacu butter': ('Cupuaçu butter (Theobroma grandiflorum)', 'Natural Amazonian seed butter; rich emollient with unique fatty acid profile; excellent moisturising and skin-conditioning properties; safe'),
        'helianthus annuus seed oil': ('Sunflower seed oil (emollient plant oil)', 'Cold-pressed oil from sunflower (Helianthus annuus) seeds; very high in linoleic acid (omega-6) and Vitamin E; non-comedogenic; helps restore skin barrier; safe and very well tolerated; one of the most skin-compatible plant oils'),
        'sunflower seed oil': ('Sunflower seed oil (Helianthus annuus)', 'Same as Helianthus Annuus Seed Oil; lightweight emollient; rich in linoleic acid; barrier-supportive; safe'),
        'carthamus tinctorius seed oil': ('Safflower seed oil (emollient plant oil)', 'Cold-pressed oil from safflower (Carthamus tinctorius) seeds; one of the highest natural sources of linoleic acid; lightweight, non-greasy emollient; non-comedogenic; safe'),
        'safflower seed oil': ('Safflower seed oil (Carthamus tinctorius)', 'Lightweight plant oil very high in linoleic acid; non-comedogenic and non-irritating; safe for all skin types'),

        # ── Additional Cosmetic Actives ───────────────────────────────────────────
        'sodium ascorbyl phosphate': ('Stable Vitamin C derivative (antioxidant / brightener)', 'A water-soluble, stable phosphate ester of ascorbic acid (Vitamin C); converted to active ascorbic acid by skin phosphatases; antioxidant, collagen-stimulating and skin-brightening; non-irritating even at higher concentrations unlike pure ascorbic acid; safe and well tolerated'),
        'magnesium aspartate': ('Magnesium amino acid chelate (skin conditioning mineral)', 'A chelated form of magnesium combined with aspartic acid; used in cosmetics as a skin conditioning agent and mineral active; supports skin enzyme activity; safe at cosmetic concentrations'),

        # ── Additional Cosmetic Minerals and Pigments ────────────────────────────
        'synthetic fluorphlogopite': ('Synthetic fluorine-mica (lab-created mica)', 'A laboratory-synthesised fluorophlogopite mica where hydroxyl groups in the crystal structure are replaced by fluorine; produces more uniform, brighter shimmer than mined natural mica; free of heavy-metal impurities common in natural mica; no child-labour mining concerns; approved by EU Cosmetics Regulation and FDA; safe'),
        'fluorphlogopite': ('Synthetic fluorine-mica (lab-created mica)', 'Same as Synthetic Fluorphlogopite; a fluorine-substituted synthetic mica; uniform optical properties; no natural mining concerns; safe'),
        'tin oxide': ('Tin(IV) oxide mineral pigment (luminosity agent)', 'An inorganic stannic oxide (SnO₂) used in colour cosmetics and nail products to produce a pearl-like, luminous shimmer effect; chemically inert; not absorbed through skin; approved by EU Cosmetics Regulation (Annex IV) and FDA for cosmetic use; safe'),
        'ci 77007': ('Ultramarine Blue / CI 77007 (inorganic pigment)', 'A complex inorganic sodium aluminium silicosulphate pigment; originally from lapis lazuli but cosmetic-grade is synthetically produced for purity; used in eyeshadows, eyeliners and nail products; approved by EU and FDA for cosmetic use including eye area; safe'),
        'ultramarines': ('Ultramarine pigments (CI 77007 / CI 77013)', 'Synthetic complex inorganic pigments used in colour cosmetics for blue/violet shades; chemically inert and stable; FDA and EU approved for eye-area use; safe'),
        'ci 77288': ('Chromium Oxide Greens / CI 77288 (inorganic pigment)', 'Chromium(III) oxide (Cr₂O₃) mineral pigment; an inorganic green pigment used in eyeshadows, eyeliners and colour cosmetics; highly stable, non-soluble and chemically inert; FDA and EU approved for use in eye-area cosmetics; safe — only trivalent chromium is used (not the toxic hexavalent form)'),
        'chromium oxide greens': ('Chromium Oxide Greens (Cr₂O₃) pigment', 'Same as CI 77288; inorganic green mineral pigment; approved for all cosmetic use including eye area by FDA and EU; safe'),

        # ── Additional Cosmetic Botanicals ───────────────────────────────────────
        'chamomilla recutita extract': ('German chamomile flower extract (soothing botanical)', 'Hydroalcoholic extract from Matricaria chamomilla (German chamomile) flowers; contains bisabolol, apigenin and chamazulene; clinically studied anti-inflammatory, soothing and skin-calming properties; safe for most skin types; patch test recommended for those with composite/daisy-family allergies'),
        'matricaria flower extract': ('German chamomile extract (Chamomilla recutita)', 'Same as Chamomilla Recutita Extract; rich in bisabolol and apigenin; anti-inflammatory and soothing for sensitive, irritated skin; safe; widely used in baby-friendly and sensitive-skin formulations'),

        # ── Silicones (additional safe/common types) ─────────────────────────────
        'caprylyl methicone': ('Volatile silicone (non-cyclic)', 'A lightweight volatile silicone used for smooth application and non-greasy feel; non-cyclic — does not share the D4/D5 environmental concerns; safe for cosmetic use'),
        'stearoxy dimethicone': ('Silicone emollient (non-cyclic)', 'A silicone wax used in conditioners and creams for smooth texture; non-cyclic silicone; safe'),
        'methicone': ('Low-viscosity silicone fluid (non-cyclic)', 'A monomethyl silicone fluid used in cosmetics for smooth texture; non-cyclic; safe for topical use'),
        'dimethicone/vinyl dimethicone crosspolymer': ('Cross-linked silicone elastomer', 'A silicone elastomer used to create a smooth, velvety skin feel; non-volatile; safe; used in primers and foundations'),
        'dimethicone crosspolymer': ('Cross-linked silicone polymer', 'A silicone elastomer that delivers a silky texture without leaving a greasy residue; safe for cosmetic use'),
        'silicone quaternium': ('Cationic silicone (quat-silicone hybrid)', 'A quaternized silicone that combines conditioning and silicone properties; provides excellent hair conditioning with some potential for buildup; safer than separate quaternary ammonium compounds alone'),

        # ── Hair and Skin Conditioning Polymers ───────────────────────────────────
        'polyquaternium-': ('Cationic conditioning polymer (polyquaternium series)', 'A group of quaternized polymers used in shampoos and conditioners to reduce static, improve combing and add conditioning; generally well tolerated at cosmetic concentrations; environmental persistence noted'),
        'polyquaternium-10': ('Cationic cellulose conditioning polymer', 'A quaternized hydroxyethylcellulose polymer used in shampoos; excellent safety profile; biodegradable biopolymer base; provides conditioning and anti-static effects; one of the safest cationic polymers'),
        'polyquaternium-11': ('Cationic vinyl/PVP conditioning polymer', 'A film-forming conditioning polymer used in hair styling and conditioning products; generally safe at cosmetic concentrations'),
        'polyquaternium-7': ('Acrylamide-based cationic polymer', 'A conditioning polymer; the acrylamide monomer is a potential contaminant — well-made grades have very low residual acrylamide; generally safe in finished cosmetics at permitted concentrations'),
        'hydroxypropyl guar': ('Modified guar gum conditioning agent', 'A non-ionic derivative of guar gum used in hair care to improve detangling and conditioning; biodegradable; safe and gentle'),

        # ── UV Filters (safe mineral) ─────────────────────────────────────────────
        'titanium dioxide': ('Mineral UV filter and white pigment (E171)', 'FDA Category I mineral UV filter in sunscreens; safe for topical use in cosmetics; EU banned as food additive in 2022 due to genotoxicity concerns — the topical safety profile is separate and generally accepted'),

        # ── Esters and Emollients ──────────────────────────────────────────────────
        'isopropyl myristate': ('Lightweight emollient ester', 'An ester of isopropyl alcohol and myristic acid used as a lightweight emollient; can be comedogenic (pore-clogging) — avoid in acne-prone skin; otherwise safe; widely used'),
        'isopropyl palmitate': ('Emollient ester', 'An ester of isopropyl alcohol and palmitic acid; lightweight emollient; some comedogenicity potential; safe for most skin types'),
        'caprylic/capric triglyceride': ('Natural plant-derived emollient', 'A light, non-greasy emollient made from glycerol and coconut/palm kernel-derived fatty acids; hypoallergenic; non-comedogenic; excellent tolerability; widely regarded as one of the best cosmetic emollients'),
        'cetyl octanoate': ('Emollient ester', 'An ester of cetyl alcohol and caprylic acid; lightweight skin emollient; safe and well tolerated'),
        'ethylhexyl palmitate': ('Emollient ester', 'An ester of 2-ethylhexanol and palmitic acid; lightweight dry-feel emollient; safe; mild comedogenicity in some individuals'),
        'diisopropyl sebacate': ('Lightweight emollient ester', 'An ester used as a non-greasy skin emollient; safe for cosmetic use'),
        'C12-15 alkyl benzoate': ('Dry-feel emollient ester', 'A synthetic emollient ester that provides a dry, silky skin feel; safe for cosmetic use; non-comedogenic; widely used'),

        # ── Humectants and Film-formers ───────────────────────────────────────────
        'betaine': ('Natural humectant from sugar beets', 'A naturally derived trimethylglycine (betaine) from sugar beet processing; excellent humectant and anti-irritant; very safe; used in hair and skin care for moisture retention and scalp soothing'),
        'glycereth-26': ('PEG-derived glycerol humectant', 'An ethoxylated glycerol used as a humectant; mild 1,4-dioxane contamination potential from ethoxylation; generally safe at permitted concentrations'),
        'propanediol': ('Natural glycol humectant/solvent', 'A 1,3-propanediol derived from corn fermentation; a gentler, more sustainable alternative to propylene glycol; excellent humectant with minimal irritation potential; GRAS status by FDA; very safe'),
        'caprylyl glycol': ('Multifunctional humectant and preservative booster', 'An 8-carbon diol used as a humectant and preservative-boosting agent; antimicrobial activity against gram-positive bacteria and yeast; safe and generally well tolerated'),
        'pentylene glycol': ('Natural-origin multifunctional glycol', 'A 1,5-pentanediol humectant with mild preservative-boosting and solvent properties; skin-compatible; generally well tolerated'),
        'butylene glycol': ('Short-chain diol humectant/solvent', 'A small synthetic diol used as a humectant, solvent and preservative booster in cosmetics; safe at cosmetic use concentrations; well tolerated'),
        'hexylene glycol': ('Glycol humectant/solvent', 'A short-chain diol used as a solvent and humectant in cosmetics; safe at cosmetic concentrations; high concentrations can cause skin irritation'),
        'fructooligosaccharides': ('Prebiotic fibre (FOS)', 'A natural prebiotic carbohydrate from chicory or agave; promotes beneficial gut bacteria; safe; minor bloating at high doses'),

        # ── Chelating agents (milder, cosmetic) ───────────────────────────────────
        'phytic acid': ('Natural chelating agent (from rice bran/corn)', 'A natural phytate chelating agent that binds metal ions to improve product stability; also used for its mild skin-brightening properties; safe for cosmetic use'),
        'sodium phytate': ('Natural chelating agent', 'Sodium salt of phytic acid; a plant-derived chelator for cosmetic preservation; safe alternative to EDTA'),

        # ── Botanical Extracts (cosmetic) ─────────────────────────────────────────
        'green tea extract': ('Polyphenol-rich botanical antioxidant', 'Rich in catechins (EGCG) with antioxidant and anti-inflammatory properties; safe for topical and dietary use; GRAS'),
        'chamomile extract': ('Soothing botanical (Matricaria chamomilla)', 'Contains bisabolol and apigenin; anti-inflammatory and soothing; safe and well tolerated; patch test for those with composite allergies'),
        'lavender extract': ('Botanical extract (Lavandula angustifolia)', 'Soothing and mildly antimicrobial; generally safe for topical use; lavender OIL (fragrance) is a declared EU allergen, but plant extracts at low levels are generally well tolerated'),
        'witch hazel': ('Astringent botanical (Hamamelis virginiana)', 'Natural astringent from witch hazel bark and leaves; contains tannins and gallic acid; safe; may be drying with very frequent use on sensitive skin'),
        'calendula extract': ('Anti-inflammatory botanical (Calendula officinalis)', 'Traditional wound-healing and anti-inflammatory herb; excellent tolerability; safe; very gentle — used in baby products'),
        'cucumber extract': ('Soothing botanical extract', 'Rich in antioxidants and silica; cooling and soothing; safe for topical use'),
        'licorice root extract': ('Skin-brightening botanical', 'Contains glabridin, a potent tyrosinase inhibitor; effective skin brightener; safe at cosmetic concentrations'),
        'licorice extract': ('Skin-brightening botanical (licorice root)', 'Contains skin-brightening glabridin and anti-inflammatory compounds; safe at cosmetic concentrations'),
        'willowbark extract': ('Natural BHA-containing botanical', 'Contains salicin (converts to salicylic acid); mild exfoliant; safe at cosmetic concentrations'),
        'bearberry extract': ('Skin-brightening botanical (contains arbutin)', 'Natural source of arbutin (alpha-arbutin) for skin brightening; safe at cosmetic concentrations'),
        'grapeseed extract': ('Antioxidant botanical (proanthocyanidins)', 'Rich in oligomeric proanthocyanidins (OPCs); potent antioxidant; safe for topical and dietary use'),
        'raspberry seed extract': ('Antioxidant botanical', 'Rich in antioxidants and omega-3; safe for topical use'),
        'blueberry extract': ('Antioxidant botanical', 'Rich in anthocyanins; potent antioxidant; safe for topical and dietary use'),
        'lotus extract': ('Botanical antioxidant', 'Traditional Ayurvedic and Asian medicine ingredient; antioxidant and skin-conditioning; safe for topical use'),
        'peony root extract': ('Botanical anti-inflammatory (Paeonia lactiflora)', 'Contains paeoniflorin; anti-inflammatory and brightening; safe at cosmetic concentrations'),
        'mulberry root extract': ('Skin-brightening botanical (Morus alba)', 'Contains oxyresveratrol and mulberroside F; potent tyrosinase inhibitors for skin brightening; safe at cosmetic concentrations'),
        'magnolia bark extract': ('Botanical anti-inflammatory (Magnolia officinalis)', 'Contains honokiol and magnolol; anti-inflammatory and antimicrobial; safe at cosmetic use levels'),
        'lotus flower extract': ('Botanical extract (Nelumbo nucifera)', 'Traditional Asian medicinal plant; antioxidant and skin-conditioning properties; safe'),
        'rice bran extract': ('Antioxidant botanical (oryzanol-rich)', 'Contains ferulic acid, oryzanol and tocopherols; antioxidant and brightening; safe'),
        'green coffee extract': ('Antioxidant botanical (caffeine-rich)', 'Rich in chlorogenic acids; antioxidant and mild skin-firming properties; safe'),
        'frankincense extract': ('Boswellia resin extract', 'Traditional anti-inflammatory ingredient; safe for topical use; used in luxury skincare for anti-ageing properties'),
        'bakuchiol': ('Plant-based retinol alternative (babchi plant)', 'Natural meroterpene with retinol-like effects; safe in pregnancy unlike retinol; well-tolerated with minimal irritation; clinically studied alternative to retinol'),

        # ── Functional Cosmetic Ingredients ──────────────────────────────────────
        'panthenol': ('Provitamin B5 (humectant and healing agent)', 'A skin and hair conditioning humectant that converts to pantothenic acid (Vitamin B5) in the body; promotes wound healing, reduces inflammation and deeply moisturises; safe and very well tolerated'),
        'niacinamide': ('Vitamin B3 (Nicotinamide) skincare active', 'One of the best-studied cosmetic actives; evidence for skin-brightening, barrier-strengthening and sebum-reducing effects; very safe and well tolerated; no purging effect unlike retinoids'),
        'biotin': ('Vitamin B7 / Vitamin H', 'B-vitamin used in hair care and cosmetics; safe; the evidence for topical biotin effectiveness in hair growth is limited'),
        'inositol': ('Vitamin B8 / polyol (hair conditioning)', 'A naturally occurring carbohydrate found in all cells; used in hair care for strengthening and smoothing; safe; food-grade ingredient'),
        'pyridoxine': ('Vitamin B6', 'Water-soluble B-vitamin used in cosmetics and food; safe at normal levels'),
        'riboflavin': ('Vitamin B2 (E101)', 'Essential B-vitamin that also acts as a natural yellow food colouring; safe and nutritionally beneficial'),
        'thiamine': ('Vitamin B1', 'Essential B-vitamin; safe at normal dietary and cosmetic levels'),
        'zinc gluconate': ('Zinc salt (anti-acne mineral)', 'Bioavailable zinc salt used in anti-acne cosmetics and food supplements; safe at recommended levels'),
        'zinc sulfate': ('Zinc salt (mineral supplement)', 'Bioavailable zinc salt; safe at approved levels in food and cosmetics'),
        'ferrous gluconate': ('Iron salt (mineral supplement / colorant)', 'An iron supplement with good bioavailability; also used as a food colouring (E579) in olives; safe at approved levels'),
        'copper gluconate': ('Copper salt (skin conditioning mineral)', 'Bioavailable copper salt; used in cosmetics for skin conditioning and as a dietary supplement; safe at low concentrations'),
        'ci 77510': ('Ferric Ferrocyanide / Prussian Blue (CI 77510) pigment', 'An inorganic iron-cyanide complex pigment (iron(III) hexacyanoferrate(II)) used as a blue or black colourant in makeup; the cyanide is firmly bound in a stable complex and is not bioavailable — it is chemically inert and non-toxic; EU Cosmetics Regulation permits it for all cosmetics including eye area; FDA however restricts it to external-use cosmetics only and does not permit it in cosmetics applied near the eye or mucous membranes — check formulation purpose; safe for external lip and skin use'),
        'ferric ferrocyanide': ('Prussian Blue pigment (CI 77510)', 'Same as CI 77510; inorganic iron-cyanide blue pigment; non-toxic at cosmetic concentrations despite containing cyanide (chemically bound, non-bioavailable); FDA-restricted from eye-area use; EU approved for all cosmetic applications; safe for external use'),
        'ci 77266': ('Carbon Black / Black 2 (CI 77266) pigment', 'A synthetic carbon black pigment used to produce deep black shades in eyeliners, mascaras and lip products; the EU Scientific Committee on Consumer Safety (SCCS) has found nano-form carbon black (particle size < 100nm) may penetrate damaged skin; EU restricts nano CI 77266 in spray cosmetics due to inhalation risk; permitted in non-spray formulations such as lipsticks and pencils; FDA permits it for cosmetic use; generally safe in solid and non-spray formats — nano status should be declared on EU labels'),
        'black 2': ('Carbon Black pigment (CI 77266)', 'Same as CI 77266 Carbon Black; deep black inorganic pigment; EU nano-form restrictions apply to spray formats; safe in solid cosmetics such as lip liners, eyeliners and pressed shadows'),
        'sodium pca': ('Natural humectant (Sodium 2-Pyrrolidone-5-Carboxylate)', 'Naturally present in human skin as part of the Natural Moisturising Factor (NMF); one of the most effective humectants; safe and very skin-compatible'),
        'urea': ('Natural humectant and keratolytic (at high levels)', 'Naturally present in the skin as part of NMF; at low concentrations (3–10%) acts as a humectant; at higher concentrations (20–40%) acts as a gentle keratolytic (softens thick skin); safe at cosmetic levels'),
        'urocanic acid': ('Natural NMF component (UV absorber)', 'Naturally present in skin and sweat; a UV-absorbing component of the skin Natural Moisturising Factor; safe'),
        'hydrolyzed silk': ('Silk protein hydrolysate (hair and skin conditioning)', 'Hydrolyzed silk fibroin peptides; conditioning and film-forming on hair and skin; safe; improves shine and smoothness'),
        'silk amino acids': ('Silk protein amino acids (hair conditioning)', 'Individual amino acids derived from silk; conditioning on hair and skin; safe'),
        'colloidal oatmeal': ('Finely milled oat extract (anti-inflammatory soothing agent)', 'FDA-approved OTC skin protectant at 0.5–2%; rich in avenanthramides (anti-inflammatory polyphenols); excellent tolerability including for eczema; safe'),
        'oat extract': ('Oat-derived soothing extract', 'Contains avenanthramides and beta-glucan; anti-inflammatory and barrier-supporting; safe; possible concern for those with severe oat/gluten sensitivity'),
        'beta-glucan': ('Natural polysaccharide (immune modulator and skin moisturiser)', 'A soluble fibre from oats, mushrooms or yeast cell walls; FDA heart health claim for oat beta-glucan; skin hydrating; safe and well-tolerated'),
        'saccharide isomerate': ('Natural carbohydrate skin hydrator (PENTAVITIN)', 'Carbohydrate complex from corn; claimed to bind to skin keratin for long-lasting hydration; safe and well-tolerated'),
        'trehalose': ('Natural disaccharide (cryoprotectant humectant)', 'A naturally occurring disaccharide found in mushrooms and desert plants; excellent humectant; safe for food and cosmetic use'),
        'gluconolactone': ('Polyhydroxy acid (PHA) exfoliant and antioxidant', 'A gentler exfoliating acid than AHAs; also acts as a chelating agent; safe; well tolerated even on sensitive skin; provides humectant benefits alongside exfoliation'),
        'lactobionic acid': ('Polyhydroxy acid (PHA) exfoliant', 'A PHA derived from lactose; gentler than glycolic acid with added humectant properties; safe; suitable for sensitive skin; provides antioxidant and chelating benefits'),
        'mandelic acid': ('Alpha hydroxy acid (AHA) from bitter almonds', 'A mild AHA with antibacterial properties; larger molecular size than glycolic acid means slower skin penetration and gentler action; safe; photosensitising — use SPF'),
        'tranexamic acid': ('Skin-brightening amino acid derivative', 'A lysine derivative clinically studied for skin brightening and melasma; safe for topical use; well tolerated; does not carry the procoagulant risks of systemic use at topical concentrations'),
        'kojic dipalmitate': ('Stable kojic acid ester (skin brightening)', 'A lipid-soluble, more stable form of kojic acid; tyrosinase inhibitor for skin brightening; safe for topical use; less irritating than kojic acid itself'),
        'diacetyl boldine': ('Alkaloid skin-brightening active', 'A derivative of boldine (from boldo plant); tyrosinase inhibitor for skin brightening; EU-reviewed; safe at specified concentrations'),
        'resveratrol': ('Polyphenol antioxidant (from grapes and berries)', 'Natural stilbenoid with antioxidant and anti-inflammatory properties; safe for topical and oral use; limited bioavailability orally — topical application delivers directly to skin'),
        'ferulic acid': ('Natural phenolic antioxidant (from bran)', 'Found in rice, wheat and oat bran; potent antioxidant that synergises with Vitamins C and E in skincare; safe; used as a food-grade antioxidant and cosmetic active'),
        'tetrahexyldecyl ascorbate': ('Oil-soluble stable Vitamin C ester', 'A lipid-soluble form of Vitamin C that penetrates the skin more effectively than ascorbic acid and is more stable; safe; no irritation at typical concentrations'),
        'ascorbyl glucoside': ('Water-soluble stable Vitamin C derivative', 'A glycoside of Vitamin C; stable and gentle; releases ascorbic acid on the skin; safe and well tolerated'),
        'ethyl ascorbic acid': ('Stable Vitamin C derivative', 'A direct, stable form of Vitamin C; well tolerated; more potent and stable than ascorbyl glucoside; safe'),
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

    # ── Generic undisclosed additive categories ──────────────────────────────
    # When a label says only "emulsifier", "acidity regulator", "sweetener" etc.
    # with no specific compound named, classify as worth_knowing — the consumer
    # cannot assess safety without knowing the exact ingredient used.
    _GENERIC_ADDITIVE_CATEGORIES = {
        'emulsifier':         ('Undisclosed emulsifier', 'Brand has not specified which emulsifier is used. Emulsifiers range from safe (soy lecithin, sunflower lecithin) to more concerning ones (carrageenan — EU-banned in infant formula; mono and diglycerides — trans fat risk). Without the specific compound, safety cannot be assessed.'),
        'emulsifiers':        ('Undisclosed emulsifier(s)', 'Brand has not specified which emulsifiers are used. Individual emulsifiers vary significantly in safety — some carry gut health concerns (carrageenan), trans fat risk (mono and diglycerides), or are poorly studied. Lack of disclosure prevents informed assessment.'),
        'acidity regulator':  ('Undisclosed acidity regulator', 'The specific acidity regulator is not named. Common options range from safe citric acid (E330) to phosphoric acid (E338 — tooth enamel erosion, mineral leaching) and acetylated derivatives. Without disclosure, consumers cannot identify what is present.'),
        'acidity regulators': ('Undisclosed acidity regulator(s)', 'The exact acidity regulators are not named. Safety varies widely — from benign citric acid to phosphoric acid (linked to bone mineral density concerns at high intake). Consumer cannot assess exposure without specifics.'),
        'sweetener':          ('Undisclosed sweetener', 'The specific sweetener is not named. Sweeteners range from stevia (clean safety profile) to aspartame (IARC Group 2B 2023), sucralose (genotoxicity signal 2023, J. Toxicology), and saccharin (animal carcinogen concerns). Undisclosed use prevents informed dietary choices.'),
        'sweeteners':         ('Undisclosed sweetener(s)', 'Specific sweeteners not named. Safety varies enormously — stevia and erythritol have relatively clean profiles; aspartame, sucralose, and saccharin each carry regulatory or research-based concerns. Without disclosure, consumers cannot assess their exposure.'),
        'stabilizer':         ('Undisclosed stabilizer', 'The specific stabilizer is not named. Stabilizers range from safe seed gums (locust bean gum, guar gum) to carrageenan (banned in EU infant formula; gut inflammation research). Cannot assess safety without knowing the compound.'),
        'stabilizers':        ('Undisclosed stabilizer(s)', 'Specific stabilizers not named. Safety varies by compound — carrageenan has gut health concerns while locust bean gum is benign. Cannot assess without disclosure.'),
        'stabiliser':         ('Undisclosed stabiliser', 'The specific stabiliser is not named. Ranges from safe seed gums to carrageenan (EU infant formula ban). Cannot assess without compound disclosure.'),
        'stabilisers':        ('Undisclosed stabiliser(s)', 'Specific stabilisers not named. Safety varies. Cannot assess without knowing which stabilisers are present.'),
        'thickener':          ('Undisclosed thickening agent', 'The specific thickener is not named. Most food thickeners are safe (guar gum, xanthan gum, modified starch) but carrageenan and certain modified starches warrant attention. Without the specific compound, full assessment is not possible.'),
        'thickeners':         ('Undisclosed thickening agent(s)', 'Specific thickeners not named. Safety varies. Cannot assess without knowing the exact compounds used.'),
        'preservative':       ('Undisclosed preservative', 'The specific preservative is not named. Preservatives range from safe rosemary extract and citric acid to concerning sodium benzoate (benzene precursor with Vitamin C), sodium nitrite (carcinogen precursor), and parabens (endocrine disruptors). Without disclosure, safety cannot be assessed.'),
        'preservatives':      ('Undisclosed preservative(s)', 'Specific preservatives not named. Safety varies enormously — from benign natural ones to synthetic preservatives with well-documented concerns (sodium benzoate, parabens, sulfites). Cannot assess without knowing which are used.'),
        'raising agent':      ('Undisclosed raising/leavening agent', 'The specific leavening agent is not named. Most are safe (sodium bicarbonate, cream of tartar) but aluminium-containing raising agents (sodium aluminium phosphate, sodium aluminium sulfate) are linked to neurotoxicity at chronic high intake. Disclosure allows consumers to identify these.'),
        'raising agents':     ('Undisclosed raising/leavening agent(s)', 'Specific leavening agents not named. Aluminium-containing variants (sodium aluminium phosphate, E541) warrant caution at high dietary intake. Cannot identify these without disclosure.'),
        'leavening agent':    ('Undisclosed leavening agent', 'The specific leavening agent is not named. Most are safe but aluminium-based variants (e.g., sodium aluminium phosphate) carry neurotoxicity concerns at chronic high dietary intake.'),
        'leavening agents':   ('Undisclosed leavening agent(s)', 'Specific leavening agents not named. Aluminium-containing variants warrant caution. Cannot assess without disclosure.'),
        'anti caking agent':  ('Undisclosed anti-caking agent', 'The specific anti-caking agent is not named. Options include safe silicon dioxide (E551) and calcium silicate but also aluminium silicates (neurotoxicity concern) and sodium ferrocyanide (E535). Disclosure allows consumers to identify higher-risk variants.'),
        'anticaking agent':   ('Undisclosed anti-caking agent', 'The specific anti-caking agent is not named. Cannot determine if aluminium-based or ferrocyanide variants are present without disclosure.'),
        'anti-caking agent':  ('Undisclosed anti-caking agent', 'The specific anti-caking agent is not named. Cannot identify aluminium silicates or sodium ferrocyanide without compound disclosure.'),
        'humectant':          ('Undisclosed humectant', 'The specific humectant is not named. Most are safe (glycerin, sorbitol) but propylene glycol (E1520) has penetration-enhancer concerns in cosmetics and high GI effect concerns in food. Cannot assess without knowing the specific compound.'),
        'humectants':         ('Undisclosed humectant(s)', 'Specific humectants not named. Cannot assess without knowing which compounds are present.'),
        'antioxidant':        ('Undisclosed antioxidant', 'The specific antioxidant is not named. Ranges from safe natural antioxidants (vitamin E, rosemary extract, ascorbic acid) to synthetic ones with regulatory concerns — BHA (E320, California Prop 65 carcinogen list), TBHQ (E319, banned in Japan), BHT (E321, possible carcinogen). Cannot assess without disclosure.'),
        'antioxidants':       ('Undisclosed antioxidant(s)', 'Specific antioxidants not named. Synthetic antioxidants BHA (E320) and TBHQ (E319) have significant safety concerns and are banned or restricted in several countries. Without disclosure, consumers cannot determine which are present.'),
        'flavouring':         ('Undisclosed flavouring', 'The specific flavouring compound(s) are not identified. "Flavouring" can refer to thousands of different natural or synthetic chemicals. Without specifics, allergenic potential and safety cannot be assessed.'),
        'flavourings':        ('Undisclosed flavouring(s)', 'Specific flavouring compounds not named. EU regulations require individual declaration of the 26 most common fragrance/flavour allergens; bare "flavourings" bypasses this transparency. Cannot assess without disclosure.'),
        'flavoring':          ('Undisclosed flavoring', 'The specific flavoring compound(s) are not named. Without specifics, allergenic potential and safety cannot be assessed.'),
        'flavorings':         ('Undisclosed flavoring(s)', 'Specific flavoring compounds not named. Cannot assess safety or allergen potential without knowing which compounds are present.'),
        'added flavour':      ('Undisclosed added flavouring', 'Flavouring is added but the compound(s) are not specified. "Added flavour" can represent hundreds of possible chemicals. Cannot assess safety or allergens without specific identification.'),
        'added flavor':       ('Undisclosed added flavoring', 'Flavoring is added but the compound(s) are not specified. Cannot assess safety or allergen content without knowing the specific compounds.'),
        'added flavouring':   ('Undisclosed added flavouring', 'Added flavouring with compound(s) unspecified. Cannot assess safety or allergen content without knowing the specific compounds used.'),
        'added flavoring':    ('Undisclosed added flavoring', 'Added flavoring with compound(s) unspecified. Cannot assess safety or allergen content without knowing the specific compounds used.'),
        'glazing agent':      ('Undisclosed glazing agent', 'The specific glazing agent is not named. Options range from safe natural waxes (carnauba E903, beeswax E901) to petroleum-derived mineral oil (E905) which carries potential MOAH (Mineral Oil Aromatic Hydrocarbons) carcinogen contamination risk. Cannot assess without disclosure.'),
        'glazing agents':     ('Undisclosed glazing agent(s)', 'Specific glazing agents not named. Cannot determine if petroleum-derived mineral oil (potential MOAH contamination) is present without disclosure.'),
        'bulking agent':      ('Undisclosed bulking agent', 'The specific bulking agent is not named. Most are safe but disclosure allows consumers to identify allergenic fillers or compounds that may affect nutrient absorption (e.g., polydextrose, inulin can cause digestive issues).'),
        'bulking agents':     ('Undisclosed bulking agent(s)', 'Specific bulking agents not named. Cannot fully assess without knowing which compounds are present.'),
        'firming agent':      ('Undisclosed firming agent', 'The specific firming agent is not named. Most common ones are calcium salts (generally safe) but without disclosure, consumers cannot assess potential interactions.'),
        'firming agents':     ('Undisclosed firming agent(s)', 'Specific firming agents not named. Cannot assess without knowing which compounds are present.'),
        'sequestrant':        ('Undisclosed sequestrant (chelating agent)', 'The specific sequestrant is not named. Some sequestrants like EDTA (E385) chelate essential minerals (calcium, zinc, iron) from the body at high dietary intake. Cannot assess without knowing the specific compound.'),
        'sequestrants':       ('Undisclosed sequestrant(s)', 'Specific sequestrants not named. EDTA and similar chelating agents can reduce absorption of essential minerals. Cannot assess without disclosure.'),
    }
    if ingredient_lower in _GENERIC_ADDITIVE_CATEGORIES:
        what_it_is, note = _GENERIC_ADDITIVE_CATEGORIES[ingredient_lower]
        return {
            'classification': 'worth_knowing',
            'what_it_is': what_it_is,
            'one_line_note': note,
            'regulatory_note': 'Specific compound not disclosed by brand — individual safety cannot be assessed without knowing the exact ingredient'
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
        # ── Colours ───────────────────────────────────────────────────────────
        'tartrazine':         'Permitted as food colour E102/INS 102 under FSSAI FSS (Food Products Standards and Food Additives) Regulations. Maximum limit: 100 mg/kg in soft drinks and confectionery. Must be declared by name on label per FSSAI labelling rules.',
        'e102':               'Tartrazine (E102/INS 102) is permitted under FSSAI with concentration limits. Must be declared by name.',
        'sunset yellow':      'Permitted as food colour E110/INS 110 under FSSAI. Quantity limits: up to 200 mg/kg depending on product category. Mandatory name declaration on label.',
        'e110':               'Sunset Yellow FCF (E110/INS 110) permitted under FSSAI with quantity limits and mandatory label declaration.',
        'allura red':         'Permitted as food colour E129/INS 129 under FSSAI with concentration limits. Mandatory name declaration on label.',
        'red 40':             'Allura Red AC (E129) permitted under FSSAI; concentration limits apply; must be declared by name.',
        'ponceau':            'Ponceau 4R (E124/INS 124) permitted as food colour under FSSAI with quantity limits and label declaration requirement.',
        'carmoisine':         'Carmoisine/Azorubine (E122/INS 122) permitted under FSSAI with limits. Mandatory name declaration.',
        'brilliant blue':     'Brilliant Blue FCF (E133/INS 133) permitted as food colour under FSSAI with concentration limits.',
        'erythrosine':        'Erythrosine (E127/INS 127) has restricted use under FSSAI — permitted only in specific products such as cocktail cherries.',
        'indigo carmine':     'Indigotine (E132/INS 132) permitted as food colour under FSSAI with concentration limits.',
        'quinoline yellow':   'Quinoline Yellow (E104/INS 104) permitted under FSSAI in limited applications with concentration limits.',
        'caramel colour':     'Caramel colour (E150a–E150d/INS 150a–150d) permitted under FSSAI. Class III (E150c) and Class IV (E150d) have restrictions in some beverage categories.',
        'caramel color':      'Caramel colour (E150 series) permitted under FSSAI; Class III/IV variants have beverage category restrictions.',
        'titanium dioxide':   'Titanium dioxide (E171/INS 171) is still permitted as a food additive under FSSAI (India has not adopted the EU 2022 ban). As a cosmetic ingredient, it remains approved. Situation under review.',
        'beta-carotene':      'Beta-carotene (E160a/INS 160a) is permitted as a natural food colour and nutritional supplement under FSSAI without restriction limits as it is a provitamin.',
        'curcumin':           'Curcumin (E100/INS 100) derived from turmeric is fully permitted under FSSAI as a natural food colour and flavouring agent.',
        # ── Preservatives ─────────────────────────────────────────────────────
        'sodium benzoate':    'Permitted as preservative E211/INS 211 under FSSAI FSS Regulations. Max limit: 150 mg/kg in soft drinks, 250 mg/kg in fruit products. Mandatory declaration on label.',
        'potassium sorbate':  'Permitted as preservative E202/INS 202 under FSSAI. Concentration limits apply depending on product category. Generally considered one of the safest preservatives.',
        'sorbic acid':        'Permitted as preservative E200/INS 200 under FSSAI with concentration limits. Safe and widely used in cheese and baked goods.',
        'sodium nitrite':     'Permitted under FSSAI in cured and processed meat products only (INS 250). Maximum limit: 125 mg/kg in cured meats. Strictly controlled due to nitrosamine formation risk.',
        'sodium nitrate':     'Permitted under FSSAI as a curing salt (INS 251) in processed meats. Maximum limit: 300 mg/kg. Acts as a slow-release nitrite source.',
        'sodium metabisulphite': 'Permitted as preservative/antioxidant E223/INS 223 under FSSAI. Mandatory declaration required on labels when sulphite content exceeds 10 mg/kg (ppm). Must declare "Contains sulphites".',
        'sulfur dioxide':     'Permitted as E220/INS 220 under FSSAI with concentration limits by product. Mandatory "contains sulphites" declaration. Sulphite-sensitive consumers (especially asthmatics) must be warned.',
        'sodium metabisulfite': 'Same as sodium metabisulphite (E223/INS 223). Permitted under FSSAI with sulphite declaration requirement.',
        'tbhq':               'TBHQ (Tert-Butylhydroquinone / E319/INS 319) is permitted as an antioxidant under FSSAI in edible oils at maximum 0.02% (200 mg/kg). Combined BHA+BHT+TBHQ limit is 0.02%.',
        'bha':                'BHA (Butylated Hydroxyanisole / E320/INS 320) permitted as antioxidant under FSSAI in edible oils and fats up to 0.02%. Combined limit with other antioxidants applies.',
        'butylated hydroxyanisole': 'BHA (E320/INS 320) permitted in edible oils under FSSAI up to 0.02%. Combined antioxidant limit applies.',
        'bht':                'BHT (Butylated Hydroxytoluene / E321/INS 321) permitted under FSSAI as antioxidant in edible oils up to 0.02%.',
        # ── Sweeteners ────────────────────────────────────────────────────────
        'aspartame':          'Aspartame (E951/INS 951) is permitted under FSSAI as a non-nutritive sweetener in specified food categories. Mandatory label warning required: "Contains Phenylalanine" for phenylketonuric (PKU) consumers. ADI: 40 mg/kg body weight/day.',
        'saccharin':          'Saccharin (E954/INS 954) is permitted under FSSAI in specified food categories with concentration limits and mandatory label declaration. Products must state "Not recommended for children" per Indian regulations.',
        'acesulfame':         'Acesulfame-K (E950/INS 950) is permitted as non-nutritive sweetener under FSSAI with ADI limits. Must be declared on label.',
        'sucralose':          'Sucralose (E955/INS 955) is permitted under FSSAI as a non-caloric sweetener. Must be declared on label with "contains sweetener" notation.',
        'stevia':             'Steviol glycosides (E960/INS 960) from stevia plant are permitted under FSSAI as natural non-caloric sweeteners. FSSAI has approved their use following global trend.',
        'xylitol':            'Xylitol (E967/INS 967) is permitted under FSSAI as a sugar alcohol in confectionery and diabetic foods. "Excessive consumption may have a laxative effect" declaration required above certain levels.',
        # ── Flavour Enhancers ─────────────────────────────────────────────────
        'monosodium glutamate': 'MSG (E621/INS 621) is permitted under FSSAI as a flavour enhancer. However, FSSAI prohibits MSG in foods intended for infants and young children. India also requires that products manufactured and sold in India declare MSG clearly on label.',
        'disodium guanylate':   'Disodium guanylate (E627/INS 627) is permitted under FSSAI as a flavour enhancer, typically used in combination with MSG. Not permitted in foods for infants.',
        'disodium inosinate':   'Disodium inosinate (E631/INS 631) is permitted under FSSAI as a flavour enhancer. Restricted in infant foods.',
        # ── Antioxidants ──────────────────────────────────────────────────────
        'ascorbic acid':      'Ascorbic acid/Vitamin C (E300/INS 300) is fully permitted under FSSAI as both an antioxidant and a nutritional supplement, with no concentration restrictions in most categories.',
        'tocopherol':         'Tocopherols (E306–E309/INS 306–309) are permitted under FSSAI as natural antioxidants in edible oils, fats and cosmetics. No ADI established by WHO/FAO due to safety.',
        'ascorbyl palmitate':  'Ascorbyl palmitate (E304/INS 304) permitted as antioxidant under FSSAI in fats, oils and fat-based products.',
        # ── Thickeners and Stabilisers ────────────────────────────────────────
        'carrageenan':        'Carrageenan (E407/INS 407) is permitted under FSSAI as a thickener and gelling agent. However, FSSAI prohibits carrageenan in infant formula. Degraded "poligeenan" is the form with health concerns — food-grade carrageenan is high molecular weight and different.',
        'xanthan gum':        'Xanthan gum (E415/INS 415) is permitted under FSSAI as a stabiliser and thickener. No ADI established due to safety; quantum satis (as needed) use permitted in most categories.',
        'guar gum':           'Guar gum (E412/INS 412) is permitted under FSSAI as a thickener and stabiliser. India is one of the world\'s largest guar producers. Quantum satis use permitted.',
        'lecithin':           'Lecithin (E322/INS 322) is permitted under FSSAI as an emulsifier in chocolate, margarine and other foods. No ADI established due to safety profile.',
        # ── Acidulants ────────────────────────────────────────────────────────
        'citric acid':        'Citric acid (E330/INS 330) is fully permitted under FSSAI as an acidulant, antioxidant and flavouring agent. No concentration limits in most categories. GRAS status.',
        'phosphoric acid':    'Phosphoric acid (E338/INS 338) is permitted under FSSAI as an acidulant in non-alcoholic beverages (e.g. colas). Concentration limits apply.',
        'lactic acid':        'Lactic acid (E270/INS 270) is fully permitted under FSSAI as an acidulant and flavouring agent. No concentration limits. Produced naturally in fermentation.',
        'acetic acid':        'Acetic acid (E260/INS 260) / vinegar is fully permitted under FSSAI as an acidulant and preservative. No concentration restrictions in normal food use.',
        'malic acid':         'Malic acid (E296/INS 296) is permitted under FSSAI as an acidulant and flavouring. No ADI established due to safety.',
        # ── Fats and Oils ─────────────────────────────────────────────────────
        'palm oil':           'Palm oil is regulated under FSSAI as an edible vegetable oil. FSSAI mandates that hydrogenated (vanaspati) versions must be labelled accordingly. Trans fat content in partially hydrogenated palm oil is restricted to max 2% under FSSAI 2022 amendment.',
        'hydrogenated vegetable oil': 'Hydrogenated vegetable oil (vanaspati) is regulated under FSSAI with strict trans fat limits. FSSAI has progressively reduced the maximum trans fat limit to 2% (2022). Products must declare trans fat content.',
        'brominated vegetable oil': 'Brominated Vegetable Oil (BVO/INS 443) is NOT permitted as a food additive under FSSAI. It has also been banned by the FDA (USA, 2024) and EU. Any product containing BVO should not be sold in India.',
        # ── Miscellaneous ──────────────────────────────────────────────────────
        'potassium bromate':  'Potassium bromate is BANNED as a food additive in India by FSSAI. It is prohibited in bread and bakery products under the Prevention of Food Adulteration Act. FSSAI enforces strict penalties for violation.',
        'azodicarbonamide':   'Azodicarbonamide (ADA/INS 927a) is NOT permitted as a food additive under FSSAI regulations. It is banned as a food additive in the EU and India.',
        'talc':               'Talc is listed as a food additive (INS 553iii) under FSSAI as an anti-caking agent in limited applications (e.g. rice polishing). FSSAI is reviewing its use in food in light of contamination concerns. As a cosmetic ingredient, it is regulated under CDSCO.',
        'sodium hyaluronate':  'Hyaluronic acid and its salts are not regulated as food additives under FSSAI but are permitted in cosmetics under CDSCO (Central Drugs Standard Control Organisation) guidelines.',
        # ── Cosmetic-specific ─────────────────────────────────────────────────
        'triclosan':          'Triclosan is permitted in cosmetics and personal care products under India\'s IS 4011 (BIS) cosmetic regulations. However, the Ministry of Health has not implemented restrictions matching EU/FDA bans. Usage concentration typically limited to 0.3% in rinse-off products.',
        'methylparaben':      'Parabens including methylparaben are permitted in cosmetics under India\'s IS 4011 (BIS/CDSCO) guidelines. Combined paraben limit is 0.8% total in cosmetics. India has not adopted the EU\'s ban on isobutylparaben and isopropylparaben.',
        'propylparaben':      'Propylparaben is permitted in cosmetics under India BIS/CDSCO guidelines. Maximum 0.4% for individual paraben or 0.8% for combinations.',
        'sodium lauryl sulfate': 'SLS is permitted in cosmetics and personal care products under Indian regulations. No specific concentration limit mandated, though industry guidelines recommend <1% in rinse-off products for sensitive skin.',
    }

    for key, pos in positions.items():
        if key in ingredient_lower:
            return pos

    if 'paraben' in ingredient_lower:
        return 'Parabens are permitted in cosmetics under India BIS/CDSCO guidelines. Combined paraben limit is 0.8% total. India has not adopted all EU paraben restrictions.'
    if 'sulphite' in ingredient_lower or 'sulfite' in ingredient_lower:
        return 'Sulphite preservatives are permitted under FSSAI. Mandatory "Contains sulphites" label declaration required when sulphite content exceeds 10 mg/kg (10 ppm).'
    if 'isothiazolinone' in ingredient_lower:
        return 'Methylisothiazolinone (MIT) and CMIT are permitted in cosmetics in India at low concentrations, though India has not matched the EU\'s near-ban on MIT in leave-on products.'
    if any(x in ingredient_lower for x in ['color', 'colour', 'dye', 'ci 1', 'ci 4', 'ci 7']):
        return 'Colouring agents in food must be declared by name under FSSAI labelling regulations. Cosmetic colorants are regulated under CDSCO and BIS standards.'
    if any(x in ingredient_lower for x in ['preservative', 'benzoate', 'sorbate', 'propionate']):
        return 'Permitted preservative under FSSAI Food Safety and Standards (Food Products Standards and Food Additives) Regulations with applicable quantity limits.'
    if any(x in ingredient_lower for x in ['vitamin', 'ascorbic', 'tocopherol', 'riboflavin', 'niacin', 'folic']):
        return 'Vitamins and their derivatives are permitted under FSSAI as nutritional supplements and functional food ingredients, subject to the FSS (Health Supplements, Nutraceuticals, Food for Special Dietary Uses, Functional Foods, Novel Food and Organic Foods) Regulations.'
    if any(x in ingredient_lower for x in ['oil', 'fat', 'butter', 'wax']):
        return 'Natural oils, fats and waxes are regulated under FSSAI Standards for Edible Oils (if used as food) or under CDSCO/BIS for cosmetic applications. No specific restrictions for most natural plant-derived oils and waxes.'
    if any(x in ingredient_lower for x in ['extract', 'powder', 'herb', 'botanical']):
        return 'Plant extracts used as food ingredients are regulated under FSSAI FSS (Food Products Standards) Regulations. Botanical extracts in cosmetics are regulated under CDSCO guidelines.'
    if any(x in ingredient_lower for x in ['silicone', 'dimethicone', 'methicone']):
        return 'Silicone polymers used in cosmetics are regulated under CDSCO (Central Drugs Standard Control Organisation) guidelines for cosmetics in India. They are not food additives and are not listed under FSSAI.'

    return 'Regulated under the Food Safety and Standards Act, 2006 (FSSAI) for food applications, and under the Drugs and Cosmetics Act, 1940 / CDSCO guidelines for cosmetic applications in India.'


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

    specific = {
        # ── Preservatives ─────────────────────────────────────────────────────
        'sodium benzoate':         'Soft drinks (Pepsi, Coca-Cola, fruit juices), pickles, ketchup, soy sauce, vinegar dressings, pharmaceutical syrups',
        'potassium sorbate':       'Cheese, baked goods, wine, dried fruits, fruit juices, margarine, yoghurt',
        'sodium nitrite':          'Bacon, ham, hot dogs, salami, pepperoni, canned meats, processed luncheon meats',
        'sodium nitrate':          'Cured and smoked meats, dry-cured ham, salami, hard cheese rinds',
        'sodium metabisulphite':   'Dried fruits (apricots, raisins), wine, beer, fresh seafood, packaged coconut water, fruit juices',
        'sulfur dioxide':          'Wine, dried fruits, fresh fruit salads, packaged fruit juice, lemon squash, beer',
        'tbhq':                    'Instant noodles, crackers, potato chips, fried snacks, edible oils, microwave popcorn, fast food',
        'bha':                     'Breakfast cereals, edible oils, potato chips, chewing gum, butter, lard, packaged snack foods',
        'bht':                     'Cereal, snack foods, edible oils, chewing gum, beer',
        # ── Colours ───────────────────────────────────────────────────────────
        'tartrazine':              'Yellow soft drinks (Mountain Dew, Mirinda Orange), lemon-flavoured candies, chips, pickles, instant noodles seasoning, medicines, fruit squash',
        'sunset yellow':           'Orange soft drinks (Fanta, Mirinda), Tang powder, orange-coloured sweets, marmalade, packaged snacks, ice lollies',
        'allura red':              'Red-coloured soft drinks, strawberry-flavoured sweets, lollipops, gelatine desserts, maraschino cherries, chewing gum, packaged fruit punch',
        'carmoisine':              'Red/pink-coloured sweets, jellies, jam, tinned fruits, medicines, raspberry-flavoured drinks',
        'brilliant blue':          'Blue-coloured sweets, ice cream, sports drinks, breakfast cereals, cake frosting, tinned peas',
        'quinoline yellow':        'Smoked fish, some drinks, sweets in EU; limited use in India',
        'indigo carmine':          'Some confectionery, ice cream, tablets, capsule coatings',
        'erythrosine':             'Cocktail and maraschino cherries, some fruit-flavoured products, medicines',
        'caramel colour':          'Cola drinks (Coca-Cola, Pepsi), dark soy sauce, beer, coffee, processed meats, bakery products, vinegar',
        'titanium dioxide':        'White-coated tablets, chewing gum, toothpaste, white icing, sunscreen, white cosmetics (foundation, concealer)',
        # ── Flavour Enhancers ─────────────────────────────────────────────────
        'monosodium glutamate':    'Instant noodles (Maggi), chips (Lay\'s, Kurkure), Chinese restaurant food, ready-to-eat meals, soups, savoury sauces, seasonings',
        'disodium guanylate':      'Chips, instant noodles, packaged soups, savoury snacks, flavour sachets — almost always alongside MSG',
        'disodium inosinate':      'Chips, instant noodles, savoury seasonings, processed meats — synergistic with MSG to amplify umami',
        # ── Sweeteners ────────────────────────────────────────────────────────
        'aspartame':               'Diet soft drinks (Diet Coke, Pepsi Max, Diet Pepsi), sugar-free chewing gum, low-calorie yoghurt, sugar-free sweets, medicines, tabletop sweeteners (Equal, NutraSweet)',
        'saccharin':               'Diet drinks, tabletop sweeteners (Sweet & Low), some toothpastes, medicines, pickle products',
        'acesulfame':              'Diet drinks, sugar-free chewing gum, sugar-free baked goods, protein shakes, tabletop sweeteners (Sunett, Sweet One)',
        'sucralose':               'Diet drinks, tabletop sweeteners (Splenda), sugar-free baked goods, protein bars, diet yoghurt',
        'stevia':                  'Stevia-sweetened drinks (Sprite Stevia), low-sugar dairy products, tabletop sweeteners, health food products',
        'xylitol':                 'Sugar-free chewing gum (Orbit, Extra), mints, dental care products, diabetic sweets',
        # ── Thickeners/Stabilisers ────────────────────────────────────────────
        'carrageenan':             'Chocolate milk, ice cream, infant formula (restricted), processed deli meats, canned pet food, almond milk, coconut milk',
        'xanthan gum':             'Salad dressings, sauces, gluten-free bread, ice cream, yoghurt, tomato sauces, cosmetic creams',
        'guar gum':                'Ice cream, sauces, instant oatmeal, gluten-free products, salad dressings, frozen desserts',
        'lecithin':                'Chocolate (almost all brands), margarine, baked goods, cooking sprays, protein supplements, baby formula',
        'gelatin':                 'Gummy sweets, marshmallows, jelly desserts (Jell-O), yoghurt, frosted cereals, pill capsules, aspic',
        # ── Cosmetic Surfactants ───────────────────────────────────────────────
        'sodium lauryl sulfate':   'Shampoos, toothpaste, body wash, bubble bath, hand soap, dishwashing liquids',
        'sodium laureth sulfate':  'Shampoos, conditioners, body wash, face wash, bubble bath, hair colour products',
        'cocamidopropyl betaine':  'Shampoos, conditioners, body wash, baby shampoo, facial cleansers',
        # ── Cosmetic Preservatives ────────────────────────────────────────────
        'methylparaben':           'Moisturisers, foundations, shampoos, conditioners, body lotion, pharmaceutical creams',
        'propylparaben':           'Moisturisers, body lotion, hair products, makeup, pharmaceutical ointments',
        'butylparaben':            'Cosmetics, hair care products, pharmaceutical preparations',
        'phenoxyethanol':          'Moisturisers, serums, baby wipes, face wash, sunscreen, makeup — one of the most common cosmetic preservatives',
        'triclosan':               'Antibacterial hand soaps (increasingly banned), toothpaste (e.g. Colgate Total), some deodorants, some mouthwashes',
        'methylisothiazolinone':   'Rinse-off products (shampoos, conditioners, body wash), household cleaning products, wipes',
        # ── Cosmetic Emollients ────────────────────────────────────────────────
        'dimethicone':             'Moisturisers, primers, foundations, sunscreen, hair serums, anti-frizz products, hand creams',
        'petrolatum':              'Lip balms (Vaseline), healing ointments, moisturisers, baby products, wound care',
        'glycerin':                'Almost all moisturisers, cleansers, toners, serums, soap, toothpaste, mouthwash, eye drops',
        'hyaluronic acid':         'Anti-ageing serums, moisturisers, eye creams, sheet masks, injectable fillers, wound care products',
        'sodium hyaluronate':      'Anti-ageing serums, moisturisers, eye creams, sheet masks, injectable dermal fillers',
        'niacinamide':             'Moisturisers, serums, toners, BB/CC creams, eye creams — one of the most popular skincare actives',
        'retinol':                 'Anti-ageing creams, serums, eye creams, prescription-strength tretinoin products',
        'salicylic acid':          'Acne treatments, exfoliating toners, anti-dandruff shampoos, medicated face washes',
        'benzoyl peroxide':        'Acne spot treatments, acne face washes, medicated cleansing bars',
        'zinc oxide':              'Mineral sunscreens, nappy rash cream, calamine lotion, anti-dandruff shampoo, wound care',
        'titanium dioxide cosmetic': 'Mineral sunscreens, BB creams, foundations, tinted moisturisers, setting powder',
        # ── Antimicrobials ────────────────────────────────────────────────────
        'benzalkonium chloride':   'Eye drops, nasal sprays, hand sanitisers, disinfectant wipes, some mouthwashes, preserved contact lens solutions',
        # ── Vitamins ──────────────────────────────────────────────────────────
        'ascorbic acid':           'Vitamin C supplements, fruit drinks, breakfast cereals, bread (as improver), fruit preserves, baby food',
        'tocopherol':              'Vitamin E supplements, cooking oils, bread, cereals, cosmetics (moisturisers, serums), sunscreen',
        'vitamin d':               'Fortified milk, breakfast cereals, vitamin D supplements, fortified orange juice',
        'folic acid':              'Fortified breakfast cereals, prenatal vitamins, bread, fortified flour, supplements',
        # ── Oils and Fats ─────────────────────────────────────────────────────
        'palm oil':                'Instant noodles (Maggi, Top Ramen), biscuits (Parle-G, Good Day), margarine, vanaspati, Nutella, most packaged snacks, chocolates, cooking oil blends',
        'hydrogenated vegetable oil': 'Vanaspati ghee, biscuits, pastries, fried fast food, shortenings, some margarines',
        'sunflower oil':           'Cooking oil, margarine, salad dressing, chips, crackers, cosmetic moisturisers',
        'coconut oil':             'Cooking (South Indian, Sri Lankan cuisines), hair oils (Parachute), cosmetics, chocolate fillings',
        'shea butter':             'Moisturisers, body butter, lip balm, hair conditioners, baby creams',
        'jojoba oil':              'Moisturisers, hair serums, cleansing oils, massage oils, lip products',
        # ── Minerals/Pigments ─────────────────────────────────────────────────
        'mica':                    'Eyeshadow, highlighter, blush, bronzer, nail polish, lip gloss, bath bombs',
        'iron oxides':             'Foundation, concealer, blush, eyeshadow, lip products, mineral makeup',
        'ci 77491':                'Foundation, concealer, blush, lip products — red iron oxide provides warm tones',
        'ci 77492':                'Foundation, concealer, bronzer — yellow iron oxide provides warm/golden tones',
        'ci 77499':                'Eyeliner, mascara, eyeshadow — black iron oxide',
        'ci 77891':                'Mineral sunscreen, foundation, white/light-coloured makeup',
        'ci 77007':                'Blue and violet eyeshadows, eyeliner',
        'ci 77288':                'Green eyeshadows, eye liners',
        # ── Fragrance/Allergens ───────────────────────────────────────────────
        'fragrance':               'Perfumes, deodorants, moisturisers, shampoos, fabric softener, cleaning products — found in 90%+ of rinse-off cosmetics',
        'parfum':                  'Perfumes, deodorants, moisturisers, shampoos — the EU INCI term for fragrance blend',
        'limonene':                'Citrus-scented perfumes, cleaning products, cosmetics, aromatherapy oils',
        'linalool':                'Lavender-scented cosmetics, shampoos, perfumes, fabric softeners',
        'eugenol':                 'Clove-based perfumes, dental products (clove oil), spice-scented cosmetics',
        'cinnamaldehyde':          'Cinnamon-flavoured products, perfumes, dental products',
        'geraniol':                'Rose-scented cosmetics, perfumes, insect repellents',
        # ── Waxes / Polymers ──────────────────────────────────────────────────
        'polyethylene glycol':     'Skin creams, laxatives (Movicol, MiraLax), toothpaste, wound care products, suppository bases, tablet coatings',
        'peg-':                    'Moisturisers, shampoos, conditioners, body wash — PEG series emulsifiers and solubilisers in almost all emulsion cosmetics',
        'propylene glycol':        'Moisturisers, foundations, hair dyes, deodorants, shaving cream, packaged baked goods, salad dressings, pharmaceutical oral syrups, asthma inhalers',
        'cyclomethicone':          'Hair serums, leave-on conditioners, facial primers, antiperspirants — used for its volatile, light, silky texture',
        'cyclopentasiloxane':      'Hair serums, styling products, skin primers, antiperspirants, sunscreens',
        'cyclohexasiloxane':       'Similar to cyclopentasiloxane — hair and skin leave-on products',
        'mineral oil':             'Baby oil, cold cream, makeup removers, laxatives (liquid paraffin), pharmaceutical preparations, industrial lubricants',
        'petrolatum':              'Vaseline/petroleum jelly, lip balms, wound ointments, heel balm, baby products (Johnsons), dry skin treatments',
        'paraffinum liquidum':     'Baby oil (Johnson\'s), cold creams, makeup removers, hair oil sprays',
        'polybutene':              'Lipsticks and lip glosses (provides gloss and body), mascara, eyeliner sticks',
        'microcrystalline wax':    'Lipsticks (structure and texture), lip balms, mascara, skin creams, paste products',
        'cera microcristallina':   'Lipsticks, lip pencils, eyebrow pencils, solid foundations, body butter sticks',
        # ── Retinoids ─────────────────────────────────────────────────────────
        'retinol':                 'Anti-ageing serums (L\'Oréal, Olay, RoC), retinol moisturisers, prescription tretinoin (Retin-A), anti-wrinkle eye creams',
        'retinyl palmitate':       'Anti-ageing creams, sunscreen lotions (in some formulas), vitamin A skin creams, multivitamin supplements',
        'tretinoin':               'Prescription acne treatment (Retin-A, Refissa), anti-ageing prescription creams — not available OTC',
        # ── Formaldehyde Releasers ────────────────────────────────────────────
        'dmdm hydantoin':          'Shampoos, conditioners, body wash, moisturisers, baby products — a very common preservative in rinse-off products',
        'imidazolidinyl urea':     'Moisturisers, sunscreens, hair care products, hand creams — common in leave-on cosmetics',
        'diazolidinyl urea':       'Moisturisers, sunscreens, hair products — second most common formaldehyde-releasing preservative in cosmetics',
        'quaternium-15':           'Shampoos, conditioners, body wash, baby products — a potent preservative and formaldehyde releaser',
        # ── Surfactants ───────────────────────────────────────────────────────
        'cocamide dea':            'Shampoos, bubble bath, body wash, car wash soaps — foam booster and thickener',
        'cocamide mea':            'Shampoos, conditioners, body wash — milder foam booster than DEA',
        # ── UV Filters ────────────────────────────────────────────────────────
        'oxybenzone':              'Chemical sunscreens (Coppertone, Banana Boat, La Roche-Posay Anthelios in older formulas), tinted moisturisers with SPF, daily moisturisers with SPF',
        'benzophenone-3':          'Chemical sunscreen products, SPF moisturisers — same chemical as oxybenzone (INCI name)',
        # ── Sweeteners ────────────────────────────────────────────────────_─────
        'cyclamate':               'Tabletop sweeteners, diet drinks (in EU, India and many other countries; banned in USA), sugar-free medicines, diabetic food products',
        'sodium cyclamate':        'Diet soft drinks, tabletop sweeteners (in India and EU), sugar-free sweets and baked goods',
        # ── Additives ─────────────────────────────────────────────────────────
        'maltodextrin':            'Protein powders, sports drinks, instant soups, infant formula, packaged baked goods, instant noodle flavour sachets, weight-gain supplements',
        'high fructose corn syrup': 'Soft drinks (especially in the USA), ketchup, salad dressing, bread, cereals, packaged sweets, flavoured yoghurt',
        'annatto':                 'Cheese (especially Cheddar and Red Leicester), butter, margarine, smoked fish, packaged rice dishes, cereals, ice cream',
        'potassium iodate':        'Iodised salt (India, many developing countries), some bread products (as dough improver in some countries)',
        'amaranth dye':            'Some jams, fruit-flavoured products, fish roe products — limited permitted use; banned in the USA and several countries',
        'carrageenan':             'Chocolate milk (Hershey\'s, Cadbury), deli meats, infant formula (now restricted in EU), almond/soy milk, ice cream, processed cheese',
        'carnauba wax':            'Confectionery coatings (M&Ms, Skittles), pharmaceutical tablet coatings, car wax, floor polish, shoe polish, candy glaze',
        'shellac':                 'Confectionery glaze (jelly beans, some chocolates), pharmaceutical tablet coatings, fruit coating (fresh produce shine), nail polish base',
        # ── Preservatives additional ──────────────────────────────────────────
        'benzyl alcohol':          'Cosmetic preservative in shampoos, hair dyes, creams; pharmaceutical injectable preservative; some baby product lines',
        'chlorhexidine':           'Surgical scrubs (Hibiscrub), antiseptic mouthwash (Corsodyl), wound wipes, medical device coatings, antibacterial hand wash, contact lens solutions',
        'chlorhexidine digluconate': 'Mouthwash (Corsodyl), wound antiseptics, surgical skin prep, hospital hand hygiene',
        # ── Emollients / Conditioners ─────────────────────────────────────────
        'lanolin':                 'Nipple cream (Lansinoh), lip balm, hand cream, hair conditioners, leather conditioners, pharmaceutical ointments',
        'polysorbate 80':          'Pharmaceutical injections (paclitaxel, erythropoietin), ice cream (as emulsifier), condiment sauces, pickles, cosmetic emulsifiers, oral care products',
        'polysorbate 20':          'Cosmetic emulsifiers, ice cream, dietary supplements, pharmaceutical preparations, shampoo and conditioner formulations',
        'gelatin':                 'Gummy bears and worms (Haribo), marshmallows, jelly desserts, yoghurt, pharmaceutical capsule shells, broths, cheesecake',
        'sorbitol':                'Sugar-free chewing gum, mints, toothpaste, diabetic sweets, diet foods, pharmaceutical oral syrups, dried fruit products',
        'maltodextrin':            'Protein powders, sports drinks, instant soups, infant formula, packaged baked goods, instant noodle seasoning',
        # ── Botanicals ────────────────────────────────────────────────────────
        'neem':                    'Neem soaps (Himalaya, Patanjali), neem face wash, neem oil for hair, Ayurvedic supplements, pesticide formulations, neem toothpaste',
        'tulsi':                   'Herbal teas (Organic India Tulsi tea), Ayurvedic supplements, tulsi face wash and toners, stress-relief capsules',
        'turmeric':                'Curries and Indian cooking (ubiquitous), turmeric latte (golden milk), Curcumin supplements, face masks (DIY and commercial), Himalaya and Patanjali skincare',
        'aloe vera':               'Aloe vera gel (Patanjali, Mamaearth, WOW), after-sun products, face wash, wound gels, Aloe Vera drinks, moisturisers (Cetaphil, Aveeno)',
        'ashwagandha':             'Ayurvedic supplements (Patanjali, Himalaya Ashvagandha), stress-relief capsules, protein powders with adaptogen blends, herbal teas',
        # ── Active cosmetic ingredients ───────────────────────────────────────
        'niacinamide':             'Ordinary Niacinamide 10% + Zinc, Minimalist Niacinamide, CeraVe PM, Olay Regenerist, The INKEY List Niacinamide — almost all modern skincare serums and moisturisers',
        'panthenol':               'Shampoos and conditioners (nearly all brands), body lotion, wound cream, baby products, Bepanthen antiseptic cream, hair masks',
        'squalane':                'The Ordinary Squalane, Biossance products, luxury face oils, lip products, hair serums — increasingly popular minimalist skincare',
        'bakuchiol':               'Bakuchiol serums (Herbivore Bakuchiol, The INKEY List), retinol-alternative night creams, pregnancy-safe anti-ageing products',
        'centella asiatica':       'Cicaplast Baume B5 (La Roche-Posay), Dr Jart+ Cicapair products, Korean skincare essentials, healing creams for eczema-prone skin',
        'allantoin':               'Aquaphor, healing creams, lip balm, baby products, shaving cream, post-procedure skin care, soothing face wash',
        'bisabolol':               'Sensitive skin moisturisers, anti-irritant serums, chamomile-based products, baby skincare, post-sun products, eye creams',
        'ferulic acid':            'SkinCeuticals CE Ferulic (iconic Vitamin C+E+Ferulic serum), anti-ageing serums with Vitamin C and E, sunscreens with antioxidant boosting',
        'resveratrol':             'Anti-ageing serums (SkinCeuticals Resveratrol BE), red wine-based cosmetics, grape-seed cosmetics, dietary supplements',
        'tranexamic acid':         'Melasma treatment serums (Murad Rapid Dark Spot Correcting Serum), skin brightening toners, hyperpigmentation creams',
        'mandelic acid':           'Exfoliating toners, anti-acne serums, AHA/BHA peel products, dark spot treatments — common in South Asian skincare for pigmentation',
        'kojic acid':              'Skin brightening creams and serums, fade creams, anti-pigmentation soaps (in some Indian markets), Kojic acid soap bars',
        'glycolic acid':           'Chemical exfoliant toners (Pixi Glow Tonic), AHA serums, peel pads, anti-ageing creams — one of the most widely used cosmetic acids',
        'azelaic acid':            'Prescription and OTC anti-acne/anti-rosacea treatments (Aziderm, Paula\'s Choice Azelaic Acid Booster), brightening serums',
        'zinc pyrithione':         'Anti-dandruff shampoos (Head & Shoulders, Nizoral), medicated body wash for seborrhoeic dermatitis, anti-fungal preparations',
        # ── Cosmetic pigments additional ──────────────────────────────────────
        'ci 77510':                'Eyeliner pencils, eye shadow palettes, lip liner, nail polish — blue/black cosmetic pigment',
        'ferric ferrocyanide':     'Eye and lip cosmetics requiring blue or grey shades — eyeliner, mascara, lip liner',
        'ci 77266':                'Eyeliner pencils, mascara, eyebrow products, black lipsticks — deep black carbon pigment',
        'carbon black':            'Eyeliner, mascara, eyeshadow, nail polish — jet-black pigment for colour cosmetics',
        'tin oxide':               'Highlighters, eyeshadow, loose mineral powder, BB creams — provides luminosity and shimmer',
        'synthetic fluorphlogopite': 'Eyeshadow palettes, highlighter powders, blush, lip gloss — synthetic mica for shimmer effects',
        'ci 77288':                'Green eyeshadows, eyeliners, nail polish — chromium oxide green pigment',
        'ci 77007':                'Blue and violet eyeshadows, eyeliner — ultramarine pigment',
        'sodium ascorbyl phosphate': 'Brightening serums (Paula\'s Choice, The Inkey List), vitamin C moisturisers, acne-fighting formulations',
        'theobroma grandiflorum':  'Luxury body butters, lip balms, moisturising creams, hair masks — high-end skincare ingredient',
        'helianthus annuus':       'Moisturisers, body oils, hair serums, facial oils, massage oils, baby products, salad dressings',
        'carthamus tinctorius':    'Lightweight face oils, hair oils, massage products, salad dressings, cosmetic emollient in serums',
        'chamomilla recutita':     'Soothing serums, sensitive-skin toners, baby skincare, anti-redness creams, chamomile tea products',
        'matricaria flower':       'Calming creams, sensitive skin serums, eye creams for puffiness, herbal face mists',

        # ── Additional entries ─────────────────────────────────────────────────
        'butylated hydroxytoluene': 'Breakfast cereals (Kellogg\'s), edible oils, chewing gum, beer, potato chips — antioxidant preservative',
        'bht':                     'Breakfast cereals, edible oils, chewing gum, beer, snack foods — antioxidant preservative to prevent rancidity',
        'propyl gallate':          'Edible oils, fat-containing products, chewing gum, dried meat products, margarine — antioxidant preservative',
        'e310':                    'Edible oils, fat-based products, chewing gum — propyl gallate antioxidant',
        'tetrasodium edta':        'Shampoos, conditioners, body wash, moisturisers, canned foods — chelating agent/preservative booster',
        'disodium edta':           'Canned beans (stabiliser), mayonnaise, salad dressings, personal care products, eye drops',
        'benzyl salicylate':       'Perfumes, floral-scented body lotions, deodorants, cosmetic fragrances — UV absorber and fragrance fixative',
        'benzyl benzoate':         'Perfumes, aftershave, anti-scabies cream (Scabisan), some insect repellents, cosmetic fragrances',
        'farnesol':                'Floral perfumes, deodorants, moisturisers, antiperspirants — rose/muguet fragrance note',
        'hydroxycitronellal':      'Lily and muguet-scented perfumes, floral fine fragrances, some cosmetic products',
        'isoeugenol':              'Rose and carnation perfumes, clove-based fragrances, cosmetic fragrance blends',
        'cinnamyl alcohol':        'Cinnamon and spice-themed perfumes, personal care fragrances, some food flavouring',
        'citronellol':             'Rose-scented perfumes, geranium-scented cosmetics, insect repellents, fabric softeners',
        'alpha-isomethyl ionone':  'Violet and iris-scented perfumes, cosmetic fragrances (Dior, Chanel and many luxury brands)',
        'amyl cinnamal':           'Jasmine-scented perfumes and cosmetics, floral fragrance blends',
        'benzyl cinnamate':        'Oriental and balsamic perfumes, perfume fixatives, cosmetic fragrance blends',
        'cetyl alcohol':           'Moisturisers (Cetaphil, CeraVe), hair conditioners, creams, body lotions — emollient and emulsifier',
        'cetearyl alcohol':        'Almost all emulsion-based moisturisers, hair conditioners, body creams, sunscreens — common emollient',
        'stearyl alcohol':         'Hair conditioners, moisturisers, skin creams — emollient, viscosity modifier',
        'behenyl alcohol':         'Hair conditioners, moisturisers, emollients — long-chain fatty alcohol',
        'behentrimonium chloride': 'Hair conditioners (Tresemmé, Pantene, Matrix), leave-in conditioners, detangling treatments',
        'behentrimonium methosulfate': 'Natural/organic hair conditioners, shea butter formulations, natural detangling products',
        'cetrimonium chloride':    'Hair conditioners, hair dyes, scalp treatments, quaternary ammonium antimicrobial',
        'cetrimonium bromide':     'Hair conditioners, antiseptic preparations, some shampoos',
        'isopropyl alcohol':       'Hand sanitisers, wound-cleaning wipes (IPA swabs), toners, astringents, hair sprays, nail polish removers',
        'polydextrose':            'Protein bars, sugar-free sweets, diet ice cream, low-calorie baked goods, meal replacement bars',
        'inulin':                  'Chicory root products, prebiotic supplements, high-fibre yoghurt (Yakult), protein bars, some fortified cereals',
        'avobenzone':              'Chemical sunscreens (Banana Boat, Neutrogena, Coppertone, La Roche-Posay), SPF moisturisers, tinted SPF products',
        'octinoxate':              'Chemical sunscreens, daily SPF moisturisers, BB creams with SPF — one of the most widely used UVB filters globally',
        'octocrylene':             'Sunscreens (alongside avobenzone as photostabiliser), SPF sprays, waterproof sunscreen, sport sunscreens',
        'ethylhexyl salicylate':   'UVB sunscreens, SPF moisturisers, sunscreen sprays — EU-approved UVB filter',
        'benzoyl peroxide':        'Clearasil, PanOxyl, Proactiv, Epiduo (with adapalene), anti-acne face wash and spot treatments, prescription acne creams',
        'zinc pyrithione':         'Head & Shoulders, Selsun, Nizoral shampoos, medicated scalp treatments, anti-dandruff conditioners',
        'alpha arbutin':           'Brightening serums (The Ordinary, Minimalist, COSRX), spot-correcting creams, hyperpigmentation treatments',
        'arbutin':                 'Skin brightening products, fade creams, Asian skincare brightening serums',
        'kojic acid':              'Skin brightening soaps (popular in South and South-East Asia), fade creams, hyperpigmentation serums, kojic acid soap bars',
        'glycolic acid':           'Pixi Glow Tonic, Paula\'s Choice AHA toners, NeoStrata glycolic acid, The Ordinary Glycolic Acid 7%, AHA exfoliant pads, chemical peels',
        'azelaic acid':            'Aziderm cream (Cipla), Finacea gel, Paula\'s Choice Azelaic Acid Booster, prescription and OTC rosacea treatments',
        'l-cysteine':              'Bread and bakery products (dough conditioner E920), some croissants and pastries, hair perm solutions',
        'potassium nitrite':       'Some cured and preserved meats, salamis, some pickled products',
        'charcoal':                'Charcoal face masks (Himalaya, Biotique), charcoal toothpaste, activated charcoal capsules (supplements), trendy charcoal-coloured foods and drinks',
        'green s':                 'Some canned peas, tinned vegetables with green colouring, some sweets — limited use; banned in many countries',
        'brilliant black':         'Some confectionery, blackcurrant products, some sauces and condiments — limited use; banned in many countries',
        'ceramide':                'CeraVe moisturisers, SkinCeuticals Triple Lipid Restore, Elizabeth Arden Ceramide Capsules, Kiehl\'s Ultra Facial Cream, barrier-repair moisturisers',
        'sodium pca':              'Moisturisers, hyaluronic acid serums, humectant-rich toners, NMF-based skincare products',
        'urea':                    'Eucerin Urea creams (5%, 10%), Flexitol heel balm, Ureadin (Isdin), diabetic foot care creams, psoriasis and eczema creams, nail softening treatments',
        'dimethiconol':            'Hair serums, conditioners, smoothing treatments — provides high-shine conditioning and detangling',
        'benzalkonium chloride':   'Mouthwash (Listerine antiseptic), nasal sprays, antiseptic throat lozenges, contact lens solutions, hospital disinfectants, skin antiseptic wipes',
        'hydrolyzed keratin':      'Hair strengthening shampoos and conditioners, salon bond treatments (Olaplex-like), hair masks for damaged hair, nail strengtheners',
        'hydrolyzed collagen':     'Anti-ageing serums, collagen supplements (Vital Proteins, HUM), joint supplements, hair masks, skin plumping creams',
        'hydrolyzed wheat protein': 'Hair strengthening shampoos, volumising conditioners, some skincare products — ingredient flagged in wheat allergy',
        'propylene glycol':        'Moisturisers, hair products, deodorant sticks, pharmaceutical oral syrups, hospital IV preparations, e-cigarette liquid, fog machine fluid',
        'isopropyl myristate':     'Moisturisers, sunscreens, foundations, massage oils, pharmaceutical creams — lightweight emollient',
        'cocamide dea':            'Shampoos, body wash, bubble bath, car wash soap — foam booster; less common now due to nitrosamine concerns',
        'potassium bromate':       'Bread and bakery products in countries where still permitted — banned in India, EU, UK, Canada; may still appear in imported products',
        'azodicarbonamide':        'Bread and baked goods where still permitted (some US manufacturers); banned in EU, UK, India — "yoga mat chemical"',

        # ── Packaged food / ice cream ─────────────────────────────────────────
        'mono and diglycerides':   'Ice cream (almost universal), bread, margarine, peanut butter, chocolate, instant mashed potato, chewing gum, packaged cakes — the most widely used food emulsifier globally',
        'e471':                    'Ice cream, bread, margarine, coffee whitener, chocolate, packaged baked goods — extremely common in ultra-processed foods',
        'datem':                   'Bread (Britannia, Harvest Gold), bakery products, croissants, pizza dough, Danish pastry — dough strengthener used in most commercial bread',
        'e472e':                   'Commercial bread, croissants, Danish pastries, pizza dough, bakery products',
        'sodium stearoyl lactylate': 'Bread (Britannia, Modern Bread), cake mixes, non-dairy coffee creamers, dehydrated potato products, packaged snack foods',
        'e481':                    'Commercial bread, cake mixes, coffee creamers — dough conditioner and emulsifier',
        'carboxymethyl cellulose': 'Ice cream (prevents ice crystal growth), jelly, cream cheese, canned fish, pharmaceuticals, diet foods, gluten-free products',
        'cmc':                     'Ice cream, cream cheese, jelly, pharmaceuticals — prevents ice crystal formation',
        'e466':                    'Ice cream, processed cheese, baked goods, salad dressings, gluten-free bread',
        'microcrystalline cellulose': 'Shredded cheese (anti-caking), protein powder, tablet coatings (pharmaceutical), low-fat ice cream, fibre-enriched products',
        'e460':                    'Shredded/grated cheese, protein bars, tablet coatings, low-fat dairy products',
        'locust bean gum':         'Ice cream (thickener and stabiliser with carrageenan), cream cheese, infant formula (anti-reflux), jelly, chocolate',
        'carob bean gum':          'Ice cream, cream cheese, infant anti-reflux formula, chocolate',
        'e410':                    'Ice cream, cream cheese, infant formula — natural carob gum stabiliser',
        'pectin':                  'Jam (almost all brands), jelly, marmalade, yoghurt, fruit preparations, confectionery, low-fat spreads',
        'e440':                    'Jam (Kissan, Mapro), jelly, marmalade, fruit juice drinks, confectionery',
        'gellan gum':              'Jelly desserts, low-acid beverages, some dairy products, structured plant-based foods, jam',
        'e418':                    'Dairy desserts, jelly, some plant-based beverages, jam',
        'hydroxypropyl methylcellulose': 'Gluten-free bread (replaces gluten structure), vegetarian capsules, ice cream (fat replacer), processed meat, fried foods (barrier coating)',
        'e464':                    'Gluten-free products, vegetarian capsules, ice cream, processed meat',
        'glycerol':                'Cake icing, marzipan, soft sweets (Turkish delight, marshmallow), chocolate fondant, baked goods (moisture retention), soap, cosmetics',
        'glycerin':                'Soft sweets, cake decoration, marzipan, chocolate coatings, bakery products, mouthwash, skin care',
        'e422':                    'Soft sweets, confectionery, icing, marzipan, cosmetics',
        'vanillin':                'Almost all vanilla-flavoured products: ice cream, biscuits (Bourbon, Nice), chocolate (Kit Kat, Dairy Milk), cake mixes, custard powder, flavoured milk — 99% of vanilla flavour in processed food is synthetic vanillin',
        'ethyl vanillin':          'Premium ice cream, chocolate, confectionery, bakery products — stronger vanilla flavour than vanillin',
        'vanilla':                 'Premium ice cream (Kwality Walls, Amul vanilla), baked goods, real vanilla extract in premium products',
        'natural flavour':         'Almost all packaged foods — chips, biscuits, instant noodles, flavoured milk, juices, snacks — covers thousands of possible compounds',
        'natural flavor':          'Packaged snacks, beverages, baked goods, ice cream, sauces — used in virtually all flavoured packaged foods',
        'artificial flavor':       'Most flavoured packaged foods, beverages, ice cream, sweets, instant powders — synthetic flavour compounds',
        'whey':                    'Protein powder supplements (Optimum Nutrition, MuscleBlaze), bread, biscuits, processed cheese, chocolate, protein bars, infant formula',
        'casein':                  'Protein supplements, coffee creamers, processed cheese (casein gives stretch and melt), infant formula, some protein bars',
        'lactose':                 'Tablets (pharmaceutical filler), instant coffee, confectionery, bread, processed foods as a mild sweetener',
        'skim milk':               'Ice cream (Kwality Walls, Amul, Baskin-Robbins), chocolate, biscuits, instant noodles, coffee whitener, protein drinks',
        'milk solids':             'Ice cream, chocolate (Cadbury Dairy Milk, KitKat), biscuits, instant coffee, bread, condensed milk, kheer mixes',
        'cocoa powder':            'Chocolate biscuits (Bourbon, Hide & Seek), cake mixes, hot chocolate drinks (Bournvita, Horlicks), chocolate ice cream, brownies, chocolate-flavoured snacks',
        'cocoa butter':            'Chocolate (Cadbury, Amul, Nestlé), premium ice cream, some cosmetics (lip balm, moisturisers)',
        'glucose syrup':           'Ice cream (prevents crystallisation), confectionery (boiled sweets, toffee), jams, soft drinks, baked goods, ketchup, energy drinks',
        'dextrose':                'Bread (browning agent), sausages and processed meats, sports drinks, confectionery, biscuits, packaged cereals',
        'maltitol':                'Sugar-free chocolates, sugar-free sweets, diet biscuits, diabetic confectionery, low-calorie ice cream',
        'e965':                    'Sugar-free chocolates, sugar-free sweets, diabetic confectionery — common in "no added sugar" products',
        'mannitol':                'Sugar-free chewing gum, sugar-free sweets, pharmaceutical tablet coatings, diabetic confectionery, medicated lozenges',
        'e421':                    'Sugar-free gum, medicated lozenges, pharmaceutical tablets, diabetic sweets',
        'lactitol':                'Sugar-free chocolates, sugar-free baked goods, diabetic confectionery, some laxative preparations (Importal)',
        'e966':                    'Sugar-free chocolate, sugar-free confectionery, laxative products',
        'sodium bicarbonate':      'Biscuits (Parle-G, Marie), baking powder, cake mixes, soda bread, self-raising flour, antacid tablets (Eno), fizzy drinks buffer',
        'e500':                    'Biscuits, baking powder, cake mixes, self-raising flour, soda bread, antacid preparations',
        'potassium bicarbonate':   'Low-sodium biscuits, baking powder blends, mineral water (added for taste), some fizzy drinks',
        'e501':                    'Low-sodium baking products, baking powder blends',
        'ammonium bicarbonate':    'Traditional biscuits (digestives, certain shortbreads), some flat breads — gives characteristic light texture without baking soda taste',
        'e503':                    'Digestive biscuits, gingerbread, traditional European biscuits, some Indian snacks',
        'diphosphate':             'Processed cheese (Amul, Britannia slices), instant potato powder, canned fish, sausages, some baking powders',
        'e450':                    'Processed cheese slices, instant mash, sausages, baking powder — phosphate salts',
        'triphosphate':            'Processed cheese, seafood products (water retention in prawns, fish fillets), processed meats, some canned goods',
        'e451':                    'Processed cheese, seafood, processed meats — tripolyphosphate',
        'polyphosphate':           'Seafood (prawns, fish fillets — water retention), deli meats, canned seafood, some processed meats',
        'e452':                    'Prawns, processed seafood, deli meats — polyphosphate water-retention agent',
        'beta carotene':           'Orange juice (for colour), margarine, butter (colour standardisation), cheese, ice cream (yellow colour), breakfast cereals, Vitamin A supplements',
        'e160a':                   'Margarine, orange juice, ice cream, breakfast cereals, cheese — orange/yellow colouring',
        'beetroot red':            'Red velvet products (some brands), strawberry-flavoured products, cranberry drinks, some yoghurts, red fruit confectionery',
        'e162':                    'Natural red-coloured foods, yoghurt, beverages, some confectionery',
        'anthocyanin':             'Natural red/purple/blue colour in berry beverages, grape juice, red cabbage products, some yoghurts and confectionery',
        'e163':                    'Berry-flavoured beverages, grape products, natural red/purple food colouring applications',
        'riboflavin':              'Fortified breakfast cereals (Kellogg\'s, Nestle), energy drinks, some pasta (fortified), multivitamin supplements, yellow food colouring in beverages',
        'e101':                    'Fortified cereals, energy drinks, some beverages — yellow vitamin B2 colouring',
        'tartaric acid':           'Wine (natural), cream of tartar (baking), grape-flavoured products, some carbonated drinks, jelly crystals',
        'e334':                    'Wine, cream of tartar, grape-flavoured confectionery, carbonated drinks',
        'sodium citrate':          'Processed cheese (fondue, cheese spreads), carbonated drinks (buffer), jelly, flavoured water, sports rehydration drinks (Gatorade)',
        'e331':                    'Processed cheese, carbonated drinks, sports drinks, jelly products',
        'calcium phosphate':       'Self-raising flour, baking powder, some cereals (calcium fortification), dental products (toothpaste), processed cheese',
        'e341':                    'Baking powder, self-raising flour, calcium-fortified cereals, processed cheese',
        'yeast extract':           'Marmite, Vegemite, Maggi seasoning, some instant noodle flavour sachets, savoury biscuits, crisps/chips, soups, stock cubes, ready meals',
        'hydrolysed':              'Instant noodle seasoning sachets, crisps flavouring (Lay\'s, Kurkure), savoury snacks, soy sauce substitutes, ready meals, soups',
        'gum arabic':              'Fizzy sweets (sugar coating), confectionery glazing, soft drink emulsifiers, wine (fining agent), some edible inks, pharmaceutical tablet coatings',
        'acacia':                  'Confectionery coatings, soft drink emulsification, pharmaceutical excipients, dietary fibre supplements',
        'modified starch':         'Instant soups, instant noodles (texture), ready meals, baby food, ketchup, sauces, mayonnaise, ice cream',
        'e1422':                   'Frozen desserts, canned foods, instant soups, sauce thickeners — heat-and-freeze-stable modified starch',
        'e1442':                   'Instant soups, sauces, frozen ready meals, canned baby food — stable to heating and freezing',
    }

    for key, found_in in specific.items():
        if key in ingredient_lower:
            return found_in

    # Smart fallbacks by ingredient type
    if any(x in ingredient_lower for x in ['benzoate', 'sorbate']):
        return 'Soft drinks, pickles, fruit juices, sauces, processed foods, pharmaceutical syrups'
    if any(x in ingredient_lower for x in ['sulphite', 'sulfite', 'metabisulph']):
        return 'Wine, beer, dried fruits, fresh seafood, packaged juices, preserved vegetables'
    if any(x in ingredient_lower for x in ['nitrite', 'nitrate']) and any(x in ingredient_lower for x in ['sodium', 'potassium']):
        return 'Bacon, ham, hot dogs, salami, canned meats, processed deli meats'
    if any(x in ingredient_lower for x in ['tartrazine', 'e102', 'ins 102']):
        return 'Yellow-coloured soft drinks, candies, pickles, instant noodle seasoning'
    if any(x in ingredient_lower for x in ['glutamate', 'guanylate', 'inosinate']):
        return 'Chips, instant noodles, savoury snacks, seasoning powders, fast food'
    if any(x in ingredient_lower for x in ['aspartame', 'sucralose', 'saccharin', 'acesulfame']):
        return 'Diet soft drinks, sugar-free chewing gum, tabletop sweeteners, diet dairy products'
    if any(x in ingredient_lower for x in ['paraben']):
        return 'Moisturisers, shampoos, conditioners, body lotion, foundations, pharmaceutical creams'
    if any(x in ingredient_lower for x in ['isothiazolinone']):
        return 'Shampoos, conditioners, body wash, household cleaning products, moist wipes'
    if any(x in ingredient_lower for x in ['sulfate', 'sulphate']) and any(x in ingredient_lower for x in ['lauryl', 'laureth']):
        return 'Shampoos, body wash, face wash, bubble bath, toothpaste, hand soap'
    if any(x in ingredient_lower for x in ['oil', 'seed oil', 'fruit oil', 'kernel oil']):
        return 'Cooking oils, moisturisers, hair oils, body serums, massage products, salad dressings'
    if any(x in ingredient_lower for x in ['extract', 'flower extract', 'leaf extract', 'root extract']):
        return 'Serums, toners, moisturisers, herbal supplements, natural skincare'
    if any(x in ingredient_lower for x in ['dimethicone', 'silicone', 'methicone']):
        return 'Hair serums, moisturisers, makeup primers, foundations, sunscreens'
    if any(x in ingredient_lower for x in ['acid']) and any(x in ingredient_lower for x in ['hyaluronic', 'glycolic', 'lactic', 'salicylic', 'ascorbic', 'citric']):
        return 'Skincare serums, toners, exfoliants, moisturisers, anti-ageing products'
    if any(x in ingredient_lower for x in ['gum', 'starch', 'cellulose', 'pectin']):
        return 'Sauces, dressings, ice cream, processed foods, gluten-free products'
    if any(x in ingredient_lower for x in ['color', 'colour', 'dye', 'pigment', 'ci 7']):
        return 'Colour cosmetics (eyeshadow, lipstick, foundation), food products (sweets, drinks)'
    if any(x in ingredient_lower for x in ['vitamin', 'ascorbic', 'tocopherol', 'retinol', 'niacin']):
        return 'Vitamin supplements, fortified foods, skincare serums, anti-ageing creams'
    if any(x in ingredient_lower for x in ['fragrance', 'parfum', 'perfume', 'scent']):
        return 'Perfumes, deodorants, moisturisers, shampoos, cleaning products, candles'
    if any(x in ingredient_lower for x in ['wax', 'cera']):
        return 'Lipsticks, lip balms, mascara, eyeliner, hair wax, body creams'

    return 'Various food and cosmetic products'


def get_health_effects(ingredient_name, classification):
    """Return health effects based on ingredient and classification"""
    ingredient_lower = ingredient_name.lower()

    # ── Specific entries (checked first regardless of classification) ─────────
    specific = {
        # Antimicrobials
        'triclosan': {
            'short_term': 'Skin and eye irritation, allergic contact dermatitis; may disrupt oral microbiome when used in toothpaste',
            'long_term': 'Endocrine disruption — acts as a weak oestrogen and thyroid hormone disrupter in animal studies; contributes to antibiotic-resistant bacteria (cross-resistance); possible thyroid function impairment with chronic exposure; accumulates in breast milk, plasma and urine',
            'vulnerable_groups': 'Pregnant and breastfeeding women, infants, children, people with thyroid conditions, healthcare workers with repeated hand-washing exposure'
        },
        'triclocarban': {
            'short_term': 'Skin sensitisation, contact dermatitis',
            'long_term': 'Hormone disruption (androgenic activity); bioaccumulation in fatty tissues; environmental persistence; potential development toxicity at high doses',
            'vulnerable_groups': 'Pregnant women, foetuses, infants, people with hormone-sensitive conditions'
        },
        # Preservatives
        'sodium benzoate': {
            'short_term': 'Urticaria (hives), angioedema, aggravation of asthma; when combined with Vitamin C forms benzene (a carcinogen)',
            'long_term': 'Benzene formation in acidic drinks containing Vitamin C is the primary long-term concern; hyperactivity link in the McCann et al. (2007) study (Southampton Study) when combined with artificial dyes',
            'vulnerable_groups': 'Asthmatics, children (hyperactivity), aspirin-sensitive individuals, people with urticaria'
        },
        'sodium nitrite': {
            'short_term': 'Methaemoglobinaemia at very high doses (rare with food levels); nausea and headache in sensitive individuals',
            'long_term': 'Reacts with amines in meat to form N-nitrosamines — several are classified IARC Group 1 carcinogens; associated with increased colorectal, stomach and oesophageal cancer risk in epidemiological studies (WHO/IARC 2015); preserving meats at high temperatures increases nitrosamine formation',
            'vulnerable_groups': 'Infants (methaemoglobinaemia risk), people who regularly consume processed meats, people with GERD'
        },
        'sodium nitrate': {
            'short_term': 'Minimal at food-level doses; excessive intake can cause methaemoglobinaemia',
            'long_term': 'Converted to nitrite in the body; same nitrosamine concerns as sodium nitrite; risk significantly elevated by high consumption of processed/cured meats',
            'vulnerable_groups': 'Infants under 6 months (highest risk for methaemoglobinaemia), regular processed meat consumers'
        },
        'sodium metabisulphite': {
            'short_term': 'Bronchospasm and asthma attacks (even trace amounts); hives, angioedema; anaphylaxis in highly sensitive individuals',
            'long_term': 'Destroys thiamine (Vitamin B1) in foods it contacts — a concern in thiamine-dependent diets; chronic sensitisation with repeated exposure',
            'vulnerable_groups': 'Asthmatics (15–20% are sulphite-sensitive), people on thiamine-restricted diets, people with sulphite allergy'
        },
        'sulfur dioxide': {
            'short_term': 'Triggers asthma attacks, coughing, wheezing and bronchoconstriction in asthmatics; skin, eye and mucous membrane irritation',
            'long_term': 'Destroys thiamine (Vitamin B1); chronic low-level exposure may sensitise the respiratory tract',
            'vulnerable_groups': 'Asthmatics, COPD patients, people with sulphite sensitivity, children'
        },
        'tbhq': {
            'short_term': 'Nausea, vomiting, ringing in ears at high doses; very rare at typical food-level exposure',
            'long_term': 'IARC classified TBHQ as "possibly carcinogenic" based on animal studies showing precancerous stomach lesions at high doses; may act as a tumour promoter at elevated doses; Japan has banned it due to carcinogenicity concerns',
            'vulnerable_groups': 'Heavy consumers of fried snacks and instant noodles; people with liver conditions'
        },
        'bha': {
            'short_term': 'Allergic reactions in sensitive individuals; skin irritation',
            'long_term': 'IARC Group 2B (possibly carcinogenic to humans); California Prop 65 listed; weak hormonal activity; some animal studies show thyroid effects; banned in Japan',
            'vulnerable_groups': 'Children with high snack food consumption, people with liver conditions, pregnant women'
        },
        # Synthetic dyes
        'tartrazine': {
            'short_term': 'Urticaria (hives), rhinitis, skin rash, asthma attacks; classic cross-reactivity with aspirin-sensitive individuals (aspirin-induced asthma/urticaria)',
            'long_term': 'Southampton Study (2007) linked tartrazine in combination with benzoate to increased hyperactivity in 3-year-olds and 8/9-year-olds; EU requires warning label "may have an adverse effect on activity and attention in children"',
            'vulnerable_groups': 'Children (hyperactivity), aspirin-sensitive individuals, asthmatics, people with atopic eczema'
        },
        'sunset yellow': {
            'short_term': 'Urticaria, nasal congestion, vomiting; hypersensitivity reactions in aspirin-sensitive individuals',
            'long_term': 'Included in the Southampton cocktail study showing hyperactivity effects; genotoxicity found in some in vitro studies; EU hyperactivity warning required',
            'vulnerable_groups': 'Children (hyperactivity/ADHD), aspirin-sensitive people, asthmatics'
        },
        'allura red': {
            'short_term': 'Allergic reactions, urticaria, hyperactivity in children; cross-reactivity with aspirin',
            'long_term': 'Part of the Southampton cocktail mixture linked to ADHD-like behaviour; some genotoxicity in vitro data; concerns about colon inflammation in animal studies',
            'vulnerable_groups': 'Children, asthmatics, aspirin-sensitive individuals'
        },
        'carmoisine': {
            'short_term': 'Urticaria, contact dermatitis, hypersensitivity reactions',
            'long_term': 'EU hyperactivity warning label required; aspirin cross-sensitivity noted',
            'vulnerable_groups': 'Children, aspirin-sensitive individuals, people with food colour sensitivities'
        },
        'brilliant blue': {
            'short_term': 'Rarely causes reactions; potential mild hypersensitivity in sensitive individuals',
            'long_term': 'Relatively less concerning than azo dyes; not part of the Southampton cocktail; limited long-term human data',
            'vulnerable_groups': 'People with known synthetic dye hypersensitivity'
        },
        'erythrosine': {
            'short_term': 'Photosensitivity reactions; rare allergic reactions',
            'long_term': 'Contains iodine (77% by weight); chronic intake may affect thyroid function; banned in cosmetics by FDA and in several countries due to carcinogenicity concerns in high-dose animal studies',
            'vulnerable_groups': 'People with thyroid conditions, iodine sensitivity, individuals on iodine-restricted diets'
        },
        # Phosphoric acid
        'phosphoric acid': {
            'short_term': 'Tooth enamel erosion on direct and repeated contact; mild gastric discomfort',
            'long_term': 'High intake from cola drinks associated with reduced bone mineral density (osteoporosis risk); impairs calcium absorption; kidney stone risk with very high intakes; can leach calcium from bones over time',
            'vulnerable_groups': 'Children (developing bones), adolescents, post-menopausal women, people with osteoporosis, individuals with kidney disease'
        },
        # Flavour enhancers
        'monosodium glutamate': {
            'short_term': '"Chinese Restaurant Syndrome" (CRS) — headache, flushing, sweating, pressure in the face — reported anecdotally but NOT confirmed in double-blind placebo-controlled trials; very large doses (>3g on empty stomach) may cause transient symptoms in a minority',
            'long_term': 'No confirmed long-term health effects in humans at normal dietary exposure; WHO, FDA and EU classify it as safe; some animal studies at extreme doses show hypothalamic damage — doses irrelevant to human food use',
            'vulnerable_groups': 'MSG-sensitive individuals (a small minority); some people report sensitivity to doses above 3g; asthmatic patients with possible bronchospasm at very high doses'
        },
        'disodium guanylate': {
            'short_term': 'Usually well tolerated; may trigger gout attacks in susceptible individuals (guanylate breaks down to purines)',
            'long_term': 'Purine content can elevate uric acid levels with very high consumption',
            'vulnerable_groups': 'People with gout, hyperuricaemia, or kidney disease; should not be used in foods for infants'
        },
        'disodium inosinate': {
            'short_term': 'Usually well tolerated; raises uric acid — may worsen gout',
            'long_term': 'Elevated uric acid at high intakes; same purine concerns as guanylate',
            'vulnerable_groups': 'People with gout, hyperuricaemia, kidney disease; infants'
        },
        # Sweeteners
        'aspartame': {
            'short_term': 'Headache, dizziness and GI discomfort reported anecdotally in sensitive individuals; phenylketonurics (PKU) cannot metabolise phenylalanine (one of its components) — mandatory label warning required',
            'long_term': 'IARC classified aspartame as Group 2B "possibly carcinogenic" in 2023 based on limited evidence from human studies on hepatocellular carcinoma — classified as inadequate evidence at normal intake levels; WHO JECFA maintained ADI of 40 mg/kg/day as still safe; conflicting studies on gut microbiome disruption; glucose intolerance in some studies',
            'vulnerable_groups': 'Phenylketonurics (PKU) — mandatory avoidance; pregnant women (precautionary); people with migraines'
        },
        'saccharin': {
            'short_term': 'Bitter metallic aftertaste; rare allergic reactions (cross-reactivity with sulfonamide antibiotics)',
            'long_term': 'Bladder cancer risk in rats at very high doses (not relevant to human dietary intake levels); removed from IARC carcinogen list in 1999; studies show potential gut microbiome disruption and impaired glucose tolerance at regular intake',
            'vulnerable_groups': 'People with sulfonamide drug allergy; pregnant women (precautionary; crosses placenta); infants'
        },
        'acesulfame': {
            'short_term': 'Generally well tolerated; rare hypersensitivity reactions',
            'long_term': 'Animal studies show potential effects on mitochondrial function and insulin signalling at high doses; some studies link to altered gut microbiome; limited long-term human data; considered safe within ADI (15 mg/kg/day)',
            'vulnerable_groups': 'Pregnant women (limited safety data in humans); infants'
        },
        # Parabens
        'methylparaben': {
            'short_term': 'Contact dermatitis and allergic sensitisation, especially in people with compromised skin barrier; immediate hypersensitivity reactions are rare',
            'long_term': 'Weak oestrogenic activity (100,000-fold less than oestradiol) — clinical significance at cosmetic exposure levels debated; found in breast tumour tissue (correlation, not causation established); accumulates in human adipose tissue; EU has banned propyl and butyl parabens in baby cosmetics',
            'vulnerable_groups': 'Infants and children (higher surface area to body weight; developing endocrine system), people with eczema or broken skin barrier, pregnant and breastfeeding women'
        },
        'propylparaben': {
            'short_term': 'Contact dermatitis, skin sensitisation',
            'long_term': 'Stronger oestrogenic activity than methylparaben; detected in human urine, blood and breast milk; EU restricts propylparaben in cosmetics to ≤0.14% and bans it in products for children under 3 on the nappy area',
            'vulnerable_groups': 'Infants under 3, pregnant women, people with hormone-sensitive conditions (e.g. oestrogen-receptor positive breast cancer)'
        },
        'butylparaben': {
            'short_term': 'Skin sensitisation, contact dermatitis',
            'long_term': 'Strongest oestrogenic activity among common parabens; EU has restricted butylparaben in leave-on face products for children under 3; studies show testicular toxicity and reduced sperm count in male rodents at high doses',
            'vulnerable_groups': 'Children, men and women with hormone-sensitive conditions, pregnant and breastfeeding women'
        },
        # Isothiazolinones
        'methylisothiazolinone': {
            'short_term': 'Severe allergic contact dermatitis — one of the top-10 contact allergens in the EU; cytotoxic at high concentrations; rare anaphylaxis',
            'long_term': 'Sensitisation is permanent — once sensitised, even trace amounts cause reactions; EU has banned MIT in leave-on products and restricted it to 0.0015% in rinse-off products; pandemic of contact dermatitis described in Europe due to its widespread adoption in the 2000s',
            'vulnerable_groups': 'People with eczema, atopic dermatitis, hand dermatitis, healthcare workers (glove-wearing); anyone who has been sensitised'
        },
        'methylchloroisothiazolinone': {
            'short_term': 'Severe contact dermatitis, chemical burns at high concentrations, extreme skin sensitiser',
            'long_term': 'Permanent sensitisation; EU banned in leave-on cosmetics; cross-reacts with methylisothiazolinone; one of the most potent skin sensitisers in cosmetics',
            'vulnerable_groups': 'People with existing skin conditions, all previously sensitised individuals'
        },
        # SLS / SLES
        'sodium lauryl sulfate': {
            'short_term': 'Disrupts skin barrier by denaturing epidermal proteins; causes irritation, redness, dryness and scaling with regular use; aggravates mouth ulcers (aphthous stomatitis) in toothpaste',
            'long_term': 'Chronic exposure damages the skin barrier leading to transepidermal water loss (TEWL); increases skin permeability, allowing other chemicals to penetrate more deeply; long-term scalp dryness and irritation',
            'vulnerable_groups': 'People with eczema, psoriasis, rosacea, sensitive skin; individuals prone to mouth ulcers; people with seborrhoeic dermatitis'
        },
        'sodium laureth sulfate': {
            'short_term': 'Milder than SLS; skin and scalp dryness in some users; mild irritation',
            'long_term': '1,4-dioxane contamination from ethoxylation process — 1,4-dioxane is a probable human carcinogen (IARC 2B); manufacturers should remove it via vacuum stripping (most do but it is not mandatory)',
            'vulnerable_groups': 'People with sensitive skin, dry scalp conditions; infants if used in baby products'
        },
        # Caramel
        'caramel colour': {
            'short_term': 'No significant immediate effects at typical food levels; Class III and IV caramel contains 4-methylimidazole (4-MEI)',
            'long_term': 'Class III (E150c) and Class IV (E150d) caramel contain 4-methylimidazole (4-MEI) as a by-product of manufacture; California Prop 65 lists 4-MEI as a possible carcinogen; Consumer Reports (2012) found elevated 4-MEI levels in major cola brands; EFSA re-evaluated caramel colours in 2011 and found no concern at current intakes',
            'vulnerable_groups': 'Heavy cola drinkers; people with inflammatory bowel disease (IBD) — animal studies show exacerbation; people sensitive to ammonia compounds'
        },
        # Titanium dioxide
        'titanium dioxide': {
            'short_term': 'Generally inert; nano-sized particles in spray or powder form may be inhaled — lung irritation possible with occupational exposure',
            'long_term': 'EU banned as food additive (E171) in 2022 — EFSA concluded genotoxicity cannot be ruled out based on particle studies; topical cosmetic use (sunscreen) is considered safe — particles do not penetrate intact skin; IARC classifies inhaled TiO₂ as Group 2B (possibly carcinogenic) — occupational inhalation risk',
            'vulnerable_groups': 'People who inhale nano-TiO₂ dust (occupational); concerns about food use particularly for children and pregnant women; intact skin exposure in cosmetics considered safe'
        },
        # Potassium bromate
        'potassium bromate': {
            'short_term': 'Acute toxicity: nausea, vomiting, abdominal pain at high doses; rare acute kidney failure',
            'long_term': 'IARC Group 2B (possibly carcinogenic to humans); causes DNA damage (genotoxic); linked to kidney tumours, thyroid cancer and mesothelioma in animal studies; bromate residues have been found in baked goods where it was not fully converted; BANNED in India, EU, UK, Canada, Brazil, China',
            'vulnerable_groups': 'Everyone — no safe level established; children and adolescents consuming large amounts of bread at highest exposure risk'
        },
        # Azodicarbonamide
        'azodicarbonamide': {
            'short_term': 'Occupational exposure causes asthma and skin sensitisation; WHO has classified workplace exposure as causing skin/respiratory problems',
            'long_term': 'Decomposes during baking to semicarbazide and urethane — both potential carcinogens; banned as food additive in EU, UK, Australia; the "yoga mat chemical" controversy (Subway, 2014)',
            'vulnerable_groups': 'Bakery workers (occupational asthma); children eating bread from countries where still permitted'
        },
        # BVO
        'brominated vegetable oil': {
            'short_term': 'Rare; very high consumption has caused bromoderma (skin lesions) and neurological symptoms (case reports)',
            'long_term': 'Bromine bioaccumulates in fatty tissues and competes with iodine; thyroid disruption with long-term high intake; FDA banned it in 2024; EU and India do not permit it',
            'vulnerable_groups': 'Heavy drinkers of BVO-containing citrus soft drinks; people with thyroid conditions; pregnant women'
        },
        # Aspartame components
        'phenylalanine': {
            'short_term': 'At normal dietary levels: no adverse effects; in phenylketonuria (PKU): immediate brain damage if dietary phenylalanine is not controlled',
            'long_term': 'In PKU: severe intellectual disability, seizures, behavioural problems if phenylalanine is not restricted from birth; for the general population: no adverse effects',
            'vulnerable_groups': 'People with phenylketonuria (PKU) — a genetic metabolic disorder; mandatory Aspartame warning "Contains Phenylalanine"'
        },
        # Carrageenan
        'carrageenan': {
            'short_term': 'Bloating, loose stools, increased intestinal permeability in some individuals',
            'long_term': 'Degraded carrageenan (poligeenan) — produced by acidic conditions and heating — is a proven carcinogen and proinflammatory agent; food-grade carrageenan is high-molecular-weight and different, but some researchers argue it partially degrades in the acidic stomach; animal studies show worsening of IBD and colon lesions; IARC classifies degraded carrageenan Group 2B',
            'vulnerable_groups': 'People with irritable bowel syndrome (IBS), Crohn\'s disease, ulcerative colitis, infants (removed from EU infant formula in 2018), people with gastrointestinal sensitivity'
        },
        # Talc
        'talc': {
            'short_term': 'Inhalation of loose powder: lung irritation, respiratory distress; topical use: generally well tolerated',
            'long_term': 'Talc contaminated with asbestos fibres poses a serious carcinogenic risk (mesothelioma, lung cancer); even "asbestos-free" talc is associated in multiple studies with ovarian cancer risk when applied to the genital area; Johnson & Johnson settled lawsuits worth billions; IARC classifies perineal talc use as "possibly carcinogenic" (Group 2B)',
            'vulnerable_groups': 'Women using talc in the perineal area (ovarian cancer risk); infants exposed to baby powder inhalation; people with asthma or respiratory conditions'
        },
        # Fragrance / Parfum
        'fragrance': {
            'short_term': 'Allergic contact dermatitis (fragrance is the #1 cause of cosmetic allergy); respiratory irritation in asthmatics; headaches, nausea in fragrance-sensitive individuals; aggravation of eczema',
            'long_term': 'Chronic sensitisation — once sensitised, cross-reactions to multiple fragrance ingredients; some fragrance components (musk ambrette, hydroxycitronellal) are endocrine disruptors; certain fragrance chemicals penetrate skin and accumulate in blood',
            'vulnerable_groups': 'People with eczema, asthma, contact dermatitis; people with fragrance allergy (estimated 1–4% of the population); chemically sensitive individuals; children'
        },
        'parfum': {
            'short_term': 'Same as fragrance — allergic contact dermatitis, respiratory irritation, asthma aggravation',
            'long_term': 'EU Cosmetics Regulation requires declaration of 26 known fragrance allergens on packaging when present above threshold; some fragrances are probable reproductive toxins',
            'vulnerable_groups': 'Eczema and asthma sufferers, fragrance-allergic individuals, pregnant women'
        },
        # Palm oil
        'palm oil': {
            'short_term': 'No acute effects; provides calorie-dense saturated fat',
            'long_term': 'High in saturated fat (palmitic acid at ~44%) which may raise LDL ("bad") cholesterol; processed at high temperatures produces glycidyl esters (a probable carcinogen — EFSA concern 2016); environmental issues (deforestation) — not a health concern but a sustainability one',
            'vulnerable_groups': 'People with hypercholesterolaemia (high cholesterol), cardiovascular disease risk; people relying heavily on ultra-processed foods using palm oil'
        },
        'hydrogenated vegetable oil': {
            'short_term': 'No immediate effects; very high calorie density',
            'long_term': 'Partially hydrogenated oils contain trans fats — strongly associated with increased LDL cholesterol, decreased HDL cholesterol, systemic inflammation, and a 2–3× increased risk of coronary heart disease (Harvard School of Public Health); WHO advocates eliminating trans fats globally by 2023',
            'vulnerable_groups': 'People with cardiovascular disease, high cholesterol, diabetes; children (developing cardiovascular system)'
        },
        # Carmine
        'carmine': {
            'short_term': 'Rare but severe allergic reactions including anaphylaxis; occupational asthma in carmine manufacturing workers; urticaria and angioedema in sensitised individuals',
            'long_term': 'Not a veganism/vegetarian concern from a health perspective; the main health concern is IgE-mediated hypersensitivity reactions which can intensify with repeated exposure; not linked to chronic toxicity',
            'vulnerable_groups': 'People with known carmine allergy; asthmatics (cross-reactivity); people allergic to cochineals; those with food-additive hypersensitivity'
        },
        'ci 75470': {
            'short_term': 'Rare IgE-mediated allergic reactions; anaphylaxis in highly sensitised individuals',
            'long_term': 'Same as carmine — allergy/sensitisation is the primary concern',
            'vulnerable_groups': 'People with carmine or cochineal allergy; asthmatics'
        },
        # CI 42090 / Blue 1
        'ci 42090': {
            'short_term': 'Rare hypersensitivity reactions; when injected intravenously as a marker dye: serious cardiovascular toxicity (FDA warning)',
            'long_term': 'Some evidence of absorption through damaged skin (wounds) and mucous membranes; metabolic acidosis and cardiovascular instability with IV use (not relevant to food use); some studies suggest possible carcinogenicity',
            'vulnerable_groups': 'People with known dye hypersensitivity; individuals with IBD or compromised gut integrity (potentially higher absorption)'
        },
        # Sodium Hyaluronate
        'sodium hyaluronate': {
            'short_term': 'Topical use: no known adverse effects — exceptionally well tolerated; injectable use: possible bruising, redness, swelling at injection site',
            'long_term': 'Topical: generally recognised as safe with no documented long-term concerns; injectable fillers: rare complications include granuloma formation, vascular occlusion (very rare), Tyndall effect (bluish discolouration)',
            'vulnerable_groups': 'Injectable HA: people with bleeding disorders, immunocompromised individuals, pregnant women (limited data); topical: safe for all skin types including sensitive and infant skin'
        },
        # Mica
        'mica': {
            'short_term': 'Topical application: safe and non-irritating; inhalation of mica dust (occupational): lung fibrosis (pneumoconiosis) at high concentrations',
            'long_term': 'Cosmetic-grade topical use is safe; occupational inhalation exposure causes muscovite pneumoconiosis; ethical concern: significant child labour in mica mining in India (Jharkhand, Rajasthan) — a supply chain issue, not a toxicological one',
            'vulnerable_groups': 'Workers in mica mining and processing (lung disease risk); spray cosmetics with mica particles may pose inhalation risk for those with respiratory conditions'
        },
        # Ascorbic acid / Vitamin C
        'ascorbic acid': {
            'short_term': 'Gastric discomfort, diarrhoea at high supplemental doses (>1g at once); acidic nature can worsen tooth enamel erosion if consumed in acidic drinks',
            'long_term': 'Generally one of the safest vitamins — water-soluble and any excess is excreted in urine; very high doses (>2g/day) may increase kidney stone risk (calcium oxalate) in predisposed individuals; no UL concerns at food additive levels',
            'vulnerable_groups': 'People with haemochromatosis (iron overload — Vitamin C enhances iron absorption); people prone to kidney stones; infants receiving formula (over-fortification risk)'
        },
        # Tocopherol
        'tocopherol': {
            'short_term': 'Topical: rare contact allergy; oral food-level intake: no known adverse effects',
            'long_term': 'Topical cosmetics: safe; supplemental Vitamin E at high doses (>400 IU/day) has been associated with increased all-cause mortality and haemorrhagic stroke risk in meta-analyses — not relevant to food additive use',
            'vulnerable_groups': 'People on anticoagulant therapy (Vitamin E potentiates blood thinning at supplemental doses); people with clotting disorders'
        },
        # Lecithin
        'lecithin': {
            'short_term': 'Topical or food use: generally well tolerated; very rare allergic reactions in individuals with soy or egg allergy (most lecithin is from soy)',
            'long_term': 'Phospholipid naturally found in every cell; generally recognised as safe; the compound phosphatidylcholine in lecithin is converted by gut bacteria to TMAO (trimethylamine N-oxide) — a compound linked to cardiovascular disease in large amounts; typical food-use quantities are far below concerning levels',
            'vulnerable_groups': 'People with severe soy allergy (soy-derived lecithin); egg-allergic individuals (egg lecithin); people with trimethylaminuria (fish odour syndrome)'
        },
        # Caffeine
        'caffeine': {
            'short_term': 'Jitteriness, anxiety, palpitations, insomnia, increased blood pressure, headache (withdrawal), stomach acid increase, diuresis',
            'long_term': 'Physical dependence (withdrawal: headaches, fatigue, irritability); no solid evidence for serious long-term health damage at moderate intake (≤400 mg/day); some cardiovascular benefit reported in moderate coffee consumption epidemiological studies',
            'vulnerable_groups': 'Pregnant women (>200mg/day linked to foetal growth restriction — NHS and ACOG guidance); infants and children (no safe level); people with anxiety disorders, arrhythmia, hypertension, GERD; people on MAOI medications'
        },
        # Sugar
        'sugar': {
            'short_term': 'Blood glucose spike and subsequent crash (reactive hypoglycaemia); dental caries with repeated exposure; energy rush followed by lethargy',
            'long_term': 'Weight gain and obesity at excess intake; Type 2 diabetes mellitus risk (strong epidemiological evidence); dental cavities (Streptococcus mutans feed on sucrose); non-alcoholic fatty liver disease; increased triglycerides and reduced HDL cholesterol',
            'vulnerable_groups': 'Diabetics and pre-diabetics, people with insulin resistance, obese individuals, children (dental caries, obesity), people with NAFLD (non-alcoholic fatty liver disease)'
        },
        # Retinol
        'retinol': {
            'short_term': 'Retinol reaction: skin redness, peeling, dryness and photosensitivity — especially in the first 2–4 weeks of use; purging breakouts',
            'long_term': 'Highly effective anti-ageing active with strong evidence for collagen production and cell turnover; teratogenic when used in high concentrations during pregnancy (Category C risk); high-dose oral Vitamin A is toxic to the liver; topical retinol at cosmetic concentrations has a good long-term safety record',
            'vulnerable_groups': 'Pregnant women (MUST avoid — even topical retinol is cautioned); breastfeeding women; people with rosacea or extremely sensitive skin; people on isotretinoin (Accutane)'
        },
        # Hyaluronic acid
        'hyaluronic acid': {
            'short_term': 'Topical: excellent tolerability — no known short-term adverse effects; injectable: bruising, swelling, redness at injection site (resolves in days)',
            'long_term': 'Topical use: excellent long-term safety profile; naturally occurring in human joints, eyes and skin — no systemic accumulation concerns; injectable filler: very rare complications include granuloma, vascular occlusion, migration over time',
            'vulnerable_groups': 'Injectable HA: pregnant and breastfeeding women (precautionary), immunocompromised individuals; topical: safe for all, including sensitive and baby skin'
        },
        # Salicylic acid
        'salicylic acid': {
            'short_term': 'Skin dryness, peeling, stinging and irritation at higher concentrations (>2%); very large body application areas may cause salicylate toxicity (rare)',
            'long_term': 'Extensive topical use over large body areas: salicylism (tinnitus, headache, nausea) — concern with systemic absorption; photosensitivity increases with regular use',
            'vulnerable_groups': 'Pregnant women (Category C — salicylates cross the placenta); infants and young children (higher surface area to body weight — risk of systemic absorption); people with aspirin sensitivity; individuals with kidney disease'
        },
        # Zinc oxide
        'zinc oxide': {
            'short_term': 'Topical: well tolerated; nano ZnO in sunscreens: minimal skin penetration on intact skin; slight white cast cosmetically',
            'long_term': 'Non-nano particles (used in most sunscreens): excellent safety record; nano-particle ZnO: some in vitro cytotoxicity shown but clinical significance on intact skin is low as nanoparticles do not penetrate beyond the stratum corneum in vivo according to TGA and SCCS reviews',
            'vulnerable_groups': 'People with zinc allergy (rare); concern about nano-ZnO inhalation from spray sunscreens; infants with damaged skin barrier (nappy rash applications)'
        },
        # Phenoxyethanol
        'phenoxyethanol': {
            'short_term': 'Mild skin and eye irritation at high concentrations; rare contact dermatitis; FDA warned against its use in nipple cream in 2008 (depression in nursing infants)',
            'long_term': 'Considered one of the safer preservatives at ≤1% in cosmetics; some rodent studies show reproductive and developmental toxicity at oral high doses — not relevant to cosmetic dermal exposure; EU permits up to 1%',
            'vulnerable_groups': 'Infants (avoid in nipple cream and products applied to infant skin); people with sensitive or eczema-prone skin; people with known phenoxyethanol allergy'
        },

        # ── PEGs / Polyethylene Glycols ───────────────────────────────────────
        'polyethylene glycol': {
            'short_term': 'Generally well tolerated topically; mild transient skin irritation in high concentrations; low-molecular-weight PEGs may irritate broken or damaged skin',
            'long_term': '1,4-dioxane — a probable human carcinogen (IARC Group 2B) — is a by-product of the ethoxylation manufacturing process; responsible manufacturers vacuum-strip it but the process is not mandatory; PEGs act as penetration enhancers, potentially increasing absorption of other ingredients through the skin; accumulate in wound tissue',
            'vulnerable_groups': 'People with damaged or broken skin barrier; people with eczema or wounds; infants (higher skin permeability); consumers seeking clean-label cosmetics'
        },
        'peg-': {
            'short_term': 'Topical application: generally well tolerated on intact skin; irritation on broken skin',
            'long_term': '1,4-dioxane contamination risk (IARC Group 2B probable carcinogen); PEGs increase dermal penetration of co-formulated ingredients; oral PEG used in laxatives and colonoscopy preps is safe due to non-absorption',
            'vulnerable_groups': 'People with compromised skin barrier; eczema, psoriasis, wound patients; infants and children; people seeking EWG "clean" cosmetics'
        },

        # ── Cyclosiloxanes (D4, D5, D6) ───────────────────────────────────────
        'cyclomethicone': {
            'short_term': 'Low immediate toxicity; minimal skin irritation',
            'long_term': 'D4 (cyclotetrasiloxane) classified as a persistent bioaccumulative and toxic (PBT) substance in the EU; D5 (cyclopentasiloxane) and D6 (cyclohexasiloxane) restricted in EU wash-off cosmetics (>0.1%) due to environmental persistence and aquatic toxicity; D4 shown to have uterotrophic (oestrogenic) activity in animals; FDA is reviewing cyclosiloxanes',
            'vulnerable_groups': 'Pregnant women (precautionary — endocrine activity in animal studies); people with regular occupational inhalation exposure to cyclosiloxane vapours; aquatic ecosystems (environmental concern)'
        },
        'cyclopentasiloxane': {
            'short_term': 'No significant short-term skin effects; inhalation of vapours at high concentrations causes respiratory irritation',
            'long_term': 'D5 is EU-restricted in wash-off cosmetics due to environmental PBT status; accumulates in aquatic organisms; some studies show endocrine disruption and liver effects in rodents; SCCS assessed D5 as safe in leave-on cosmetics at current use levels',
            'vulnerable_groups': 'Aquatic environment (PBT bioaccumulation); occupational inhalation workers; pregnant women (precautionary)'
        },
        'cyclohexasiloxane': {
            'short_term': 'Low acute toxicity; minimal skin irritation',
            'long_term': 'D6 is also EU-restricted in rinse-off cosmetics; similar environmental persistence concerns to D4/D5 though less studied; SCCS review ongoing',
            'vulnerable_groups': 'Environmental and occupational concerns primarily; precautionary avoidance in pregnancy'
        },

        # ── Mineral Oil / Petrolatum ──────────────────────────────────────────
        'mineral oil': {
            'short_term': 'Topical: occlusive barrier — may worsen acne in acne-prone individuals; generally well tolerated on intact skin; ingestion of food-grade mineral oil: minimal direct effects but inhibits fat-soluble vitamin absorption',
            'long_term': 'Highly refined (food and pharmaceutical grade) mineral oils are considered safe; inadequately refined mineral oils contain polycyclic aromatic hydrocarbons (PAHs) — IARC Group 1 carcinogens; EFSA raised concerns about mineral oil aromatic hydrocarbons (MOAH) migrating from packaging into food; occupational exposure to cutting/mist mineral oils is associated with bladder cancer',
            'vulnerable_groups': 'Acne-prone individuals (comedogenicity risk); people with fat-soluble vitamin deficiencies; workers exposed to untreated mineral oil mist; consumers of foods in mineral-oil-lined packaging'
        },
        'petrolatum': {
            'short_term': 'Topical: occlusive; may cause comedones in acne-prone skin; generally non-irritating',
            'long_term': 'Pharmaceutical/food-grade petrolatum (e.g. Vaseline) is fully refined and safe; EU requires petrolatum in cosmetics to have full refining history to show freedom from PAHs; PAH-contaminated petrolatum is carcinogenic; EU lists semi-solid petroleum-derived substances as restricted unless refining history establishes safety',
            'vulnerable_groups': 'Acne-prone individuals; people seeking petroleum-free cosmetics; workers exposed to unrefined petroleum products'
        },
        'paraffinum liquidum': {
            'short_term': 'Topical: well tolerated; occlusive; some comedogenicity',
            'long_term': 'Same PAH contamination concerns as mineral oil; liquid paraffin taken orally as a laxative can cause lipoid pneumonia if aspirated; impairs absorption of fat-soluble vitamins with prolonged oral use; EU cosmetic use requires refining certification',
            'vulnerable_groups': 'Acne-prone individuals; elderly patients using it as a laxative (aspiration risk); patients with swallowing difficulties'
        },

        # ── Retinoids ─────────────────────────────────────────────────────────
        'retinyl palmitate': {
            'short_term': 'Skin dryness, peeling, photosensitivity; milder than retinol',
            'long_term': 'The EWG and NTP (National Toxicology Program) flagged that retinyl palmitate may accelerate skin tumour development when applied to sun-exposed skin (animal study); the FDA has been reviewing it for use in sunscreens since 2010 — no conclusive human evidence of harm but precautionary concern exists; at non-sun-exposed sites, long-term topical use is generally accepted as safe',
            'vulnerable_groups': 'Pregnant women (all retinoids are teratogenic — caution with any form); people using it in sun-exposed areas (daytime use); people with sensitive skin'
        },
        'tretinoin': {
            'short_term': 'Significant skin irritation, dryness, peeling, photosensitivity, erythema — especially in the first 4–8 weeks; "retinoid reaction" is expected and part of the treatment',
            'long_term': 'FDA Category X in pregnancy — proven teratogen causing retinoic acid embryopathy (craniofacial, cardiac, thymic, CNS malformations); highly effective anti-acne and anti-ageing medication with 50+ years of clinical evidence; long-term use (years) well tolerated by most; increases susceptibility to UV damage so SPF use is mandatory',
            'vulnerable_groups': 'Pregnant women and those trying to conceive (MUST avoid — Category X); breastfeeding women; people with sensitive or rosacea skin; those without adequate sun protection'
        },

        # ── Benzyl Alcohol ────────────────────────────────────────────────────
        'benzyl alcohol': {
            'short_term': 'Skin and eye irritation; headache and dizziness from inhalation of vapours at high concentrations; "gasping syndrome" — metabolic acidosis and CNS depression in neonates given benzyl alcohol-preserved IV medications',
            'long_term': 'At cosmetic-use concentrations (≤1%), generally safe for adults; an EU fragrance allergen requiring declaration at >0.001% in leave-on and >0.01% in rinse-off products; the neonatal gasping syndrome was due to intravenous exposure, not topical cosmetic use',
            'vulnerable_groups': 'Newborns and premature infants (IV exposure causes gasping syndrome — cosmetic exposure is different but caution advised); people with benzyl alcohol contact allergy; people with fragrance sensitivity'
        },

        # ── DMDM Hydantoin and Formaldehyde Releasers ─────────────────────────
        'dmdm hydantoin': {
            'short_term': 'Releases formaldehyde — skin irritation, contact dermatitis, allergic sensitisation; formaldehyde odour at high concentrations',
            'long_term': 'Formaldehyde (IARC Group 1 carcinogen) is continuously released; at cosmetic use concentrations the release is low but contributes to cumulative formaldehyde exposure; sensitised individuals react to trace amounts; EU restricts formaldehyde releasers and requires "contains formaldehyde" label when released levels exceed 0.05%',
            'vulnerable_groups': 'People with formaldehyde allergy (an increasingly common contact allergen); eczema-prone individuals; salon and spa workers; people using multiple formaldehyde-releasing preservatives simultaneously'
        },
        'imidazolidinyl urea': {
            'short_term': 'Formaldehyde release causes skin irritation and contact dermatitis; among the more potent formaldehyde releasers',
            'long_term': 'Same formaldehyde-related carcinogenicity concerns; the highest formaldehyde-releasing preservative in common use; EU mandates formaldehyde label warning at defined release levels',
            'vulnerable_groups': 'People with formaldehyde allergy, eczema patients, salon workers, immunocompromised individuals'
        },
        'diazolidinyl urea': {
            'short_term': 'Contact dermatitis, sensitisation through formaldehyde release',
            'long_term': 'Significant formaldehyde releaser; cumulative formaldehyde exposure concern across multiple products; EU label warning required',
            'vulnerable_groups': 'Formaldehyde-allergic individuals, people with sensitive skin, eczema sufferers'
        },
        'quaternium-15': {
            'short_term': 'One of the most potent formaldehyde releasers — significant contact sensitiser; skin irritation, allergic dermatitis',
            'long_term': 'Classified as a known human contact allergen; EU has extremely restricted its use; persistent sensitisation once developed; cumulative formaldehyde release is highest among cosmetic preservatives',
            'vulnerable_groups': 'People with formaldehyde allergy, anyone with contact dermatitis history, eczema patients, salon workers'
        },

        # ── Cocamide DEA ──────────────────────────────────────────────────────
        'cocamide dea': {
            'short_term': 'Mild skin and scalp irritation at high concentrations; contact dermatitis in sensitised individuals',
            'long_term': 'Reacts with nitrites (often present as contaminants) to form diethanolamine nitrosamines (DEA-NO) — potent animal carcinogens; California Prop 65 lists cocamide DEA as a carcinogen based on this; IARC Group 2B for diethanolamine; the EU has restricted cocamide DEA in cosmetics as a precaution',
            'vulnerable_groups': 'All consumers — nitrosamine formation is a product quality issue; workers occupationally exposed to higher concentrations; people with scalp conditions using repeated high-concentration shampoos'
        },
        'cocamide mea': {
            'short_term': 'Milder than DEA; mild skin irritation',
            'long_term': 'Similar but lower nitrosamine formation potential than cocamide DEA; EU has also restricted it as part of the same concern',
            'vulnerable_groups': 'Same precautionary concerns as cocamide DEA; less acute risk but precautionary avoidance recommended'
        },

        # ── Oxybenzone / Chemical UV Filters ──────────────────────────────────
        'oxybenzone': {
            'short_term': 'Allergic contact dermatitis and photoallergic reactions (estimated 1–2% of users); skin sensitisation',
            'long_term': 'Significant dermal absorption — detected in blood, urine and breast milk; FDA classifies oxybenzone as "not generally recognised as safe" due to insufficient data; animal studies show oestrogenic and anti-androgenic activity; environmental toxicity — damages coral reefs (Hawaii and Palau have banned oxybenzone sunscreens); disrupts thyroid hormone in animal studies',
            'vulnerable_groups': 'Pregnant women and foetuses; infants (high surface area absorption); people with hormone-sensitive conditions; frequent whole-body sunscreen applicators; marine ecosystems'
        },
        'benzophenone-3': {
            'short_term': 'Photoallergic contact dermatitis; skin irritation in sensitised individuals',
            'long_term': 'Same as oxybenzone (benzophenone-3 is the INCI name); FDA "not generally recognised as safe" due to systemic absorption; EU allows up to 6% but recommends not using on large body surface areas in infants; coral reef toxicity',
            'vulnerable_groups': 'Pregnant women, infants, people with oestrogen-sensitive conditions, frequent sunscreen users, marine environments'
        },

        # ── Cyclamate ─────────────────────────────────────────────────────────
        'cyclamate': {
            'short_term': 'Generally well tolerated at low doses; some people metabolise it to cyclohexylamine — which can cause nausea',
            'long_term': 'Banned in the USA (FDA) in 1969 after animal studies linked it to bladder cancer (in combination with saccharin); the ban is under ongoing review — some scientific bodies consider current evidence insufficient for human risk; permitted in EU, India and 130+ countries; cyclohexylamine (gut metabolite in some individuals) has testicular atrophy effects in animals at high doses',
            'vulnerable_groups': 'People who are high metabolisers of cyclamate to cyclohexylamine (genetically variable); pregnant women (precautionary); people with bladder conditions'
        },
        'sodium cyclamate': {
            'short_term': 'Same as cyclamate — generally well tolerated; cyclohexylamine production varies by individual gut flora',
            'long_term': 'Same concerns as cyclamate; banned in USA, permitted in India and EU; ongoing FDA review',
            'vulnerable_groups': 'High cyclamate metabolisers, pregnant women, children'
        },

        # ── Propylene Glycol ──────────────────────────────────────────────────
        'propylene glycol': {
            'short_term': 'Skin irritation and contact dermatitis in sensitive individuals — particularly in leave-on products at concentrations >2%; eyes: irritation at high concentrations; ingestion: generally recognised as safe (FDA GRAS as a food additive)',
            'long_term': 'Accumulates in the body with very large oral doses (pharmaceutical IV use cases); topical cosmetic exposure: low systemic exposure; some individuals develop propylene glycol contact allergy — affects an estimated 2–4% of dermatology patients; metabolised to lactic acid and pyruvic acid (normal metabolic intermediates)',
            'vulnerable_groups': 'People with propylene glycol contact allergy; eczema-prone individuals; neonates and infants (limited liver metabolism capacity for high IV doses — not relevant to cosmetic use); people with kidney disease (impaired elimination at high doses)'
        },

        # ── Lilial / Butylphenyl Methylpropional ──────────────────────────────
        'lilial': {
            'short_term': 'Contact sensitisation and allergic dermatitis; a recognised fragrance allergen',
            'long_term': 'EU banned lilial (butylphenyl methylpropional) in cosmetics in March 2022 due to reproductive toxicity concerns — specifically classified as Category 1B reprotoxicant (may damage fertility); detected in human breast milk; endocrine disruption evidence',
            'vulnerable_groups': 'Pregnant women and those planning pregnancy (reproductive toxicity — EU banned); breastfeeding women; people with fragrance allergies'
        },
        'butylphenyl methylpropional': {
            'short_term': 'Fragrance allergen; skin sensitisation and contact dermatitis',
            'long_term': 'EU banned in cosmetics in 2022 due to Category 1B reproductive toxicity classification; detected in human breast milk; must not be present in cosmetics sold in the EU',
            'vulnerable_groups': 'All cosmetic users (now banned in EU cosmetics); pregnant women; breastfeeding women'
        },

        # ── Chlorhexidine ─────────────────────────────────────────────────────
        'chlorhexidine': {
            'short_term': 'Skin and mucous membrane irritation; bitter taste; rare but severe anaphylaxis (IgE-mediated) including fatal cases; brown staining of teeth and tongue with oral use; altered taste sensation',
            'long_term': 'Antimicrobial resistance — chlorhexidine tolerance in bacteria has been linked to cross-resistance to colistin (last-resort antibiotic) in some studies; ototoxicity if used in the ear canal; contact allergy develops in some individuals',
            'vulnerable_groups': 'People with known chlorhexidine allergy (anaphylaxis risk — allergy tests recommended before elective procedures); patients with perforated tympanic membranes (ear canal use prohibited); people with sensitive oral mucosa'
        },
        'chlorhexidine digluconate': {
            'short_term': 'Same as chlorhexidine — skin, eye and mucous membrane irritation; rare severe anaphylaxis',
            'long_term': 'Antimicrobial resistance cross-selection concerns; tooth staining with mouthwash use; contact sensitisation',
            'vulnerable_groups': 'Chlorhexidine-allergic individuals (severe anaphylaxis risk); patients with ear perforations; oral mucosa sensitivity'
        },

        # ── Annatto / E160b ───────────────────────────────────────────────────
        'annatto': {
            'short_term': 'Urticaria, hives and angioedema in sensitive individuals — annatto is one of the few "natural" food colourings associated with pseudoallergic reactions; very rare anaphylaxis reported',
            'long_term': 'Generally considered safe; no significant long-term toxicity established; the pseudoallergic reactions (not IgE-mediated) can still be severe and recurrent; WHO/FAO JECFA evaluates annatto as acceptable at current food-use levels',
            'vulnerable_groups': 'People with urticaria (hives), atopic individuals, people with aspirin or NSAID sensitivity (cross-reactivity pattern similar to other pseudoallergens)'
        },

        # ── Potassium Iodate ──────────────────────────────────────────────────
        'potassium iodate': {
            'short_term': 'Excess iodine causes hyperthyroidism symptoms: palpitations, tremor, weight loss, heat intolerance',
            'long_term': 'WHO recommends potassium iodide over potassium iodate for salt iodisation due to stability concerns; iodate is an oxidising agent — excess iodate intake (from high bread consumption in countries using it as a flour improver) may cause thyrotoxicosis in iodine-replete individuals; India uses potassium iodate for salt iodisation to combat iodine deficiency',
            'vulnerable_groups': 'People with thyroid conditions (hyperthyroidism, Graves\' disease, toxic nodular goitre); people on thyroid medications; iodine-replete individuals consuming high amounts of iodised bread'
        },

        # ── Amaranth Dye / E123 ───────────────────────────────────────────────
        'amaranth dye': {
            'short_term': 'Urticaria, skin rash, hyperactivity; aspirin cross-sensitivity',
            'long_term': 'BANNED in the USA (FDA) since 1976 due to carcinogenicity concerns (malignant tumours in animal studies); banned in several other countries; still permitted in EU and India in limited applications (e.g. fish roe); genotoxicity concerns in some studies',
            'vulnerable_groups': 'Children (hyperactivity), aspirin-sensitive individuals, asthmatics, people with food colour sensitivity'
        },
        'e123': {
            'short_term': 'Urticaria, hyperactivity in children; aspirin cross-reactivity',
            'long_term': 'Banned in USA since 1976; potential carcinogenicity; limited permitted use in EU and India',
            'vulnerable_groups': 'Children, aspirin-sensitive individuals, asthmatics'
        },

        # ── Cocamidopropyl Betaine ────────────────────────────────────────────
        'cocamidopropyl betaine': {
            'short_term': 'Contact dermatitis in sensitised individuals; mild skin and eye irritation in high concentrations; the American Contact Dermatitis Society named it "allergen of the year" in 2004',
            'long_term': 'Sensitisation is permanent; impurities in manufacturing (3-dimethylaminopropylamine and amidoamine) are the likely allergens rather than CAPB itself; considered one of the milder surfactants overall — reactions occur in a small but significant minority',
            'vulnerable_groups': 'People with existing contact dermatitis or eczema; hairdressers and cosmetologists (occupational sensitisation); people with known CAPB allergy — must avoid all products containing it once sensitised'
        },

        # ── Maltodextrin ──────────────────────────────────────────────────────
        'maltodextrin': {
            'short_term': 'Rapid blood glucose spike — very high glycaemic index (GI of 85–105, higher than table sugar); energy crash; potential bloating in large amounts',
            'long_term': 'Regular high intake contributes to the same metabolic risks as excess sugar (Type 2 diabetes, obesity, insulin resistance); some studies suggest maltodextrin may negatively alter the gut microbiome — promoting growth of E. coli strains associated with IBD; may mask the flavour of low-quality food by adding bulk',
            'vulnerable_groups': 'Diabetics and pre-diabetics (extreme blood glucose spike); people with IBD (gut microbiome disruption); people with coeliac disease if derived from wheat (though usually highly processed and gluten-free)'
        },

        # ── High Fructose Corn Syrup ──────────────────────────────────────────
        'high fructose corn syrup': {
            'short_term': 'Rapid blood glucose/fructose spike; fructose bypasses normal satiety signalling; may increase appetite',
            'long_term': 'Fructose is metabolised almost entirely in the liver — high intake causes non-alcoholic fatty liver disease (NAFLD), de novo lipogenesis (fat synthesis), elevated triglycerides and uric acid; epidemiological links to obesity, metabolic syndrome and Type 2 diabetes; does not stimulate insulin or leptin (satiety hormones) like glucose does',
            'vulnerable_groups': 'Obese individuals, people with NAFLD, diabetics, people with hyperuricaemia or gout (fructose raises uric acid), children and adolescents (high soft drink consumption)'
        },

        # ── Lanolin ───────────────────────────────────────────────────────────
        'lanolin': {
            'short_term': 'Contact dermatitis and lanolin allergy is one of the top 10 cosmetic contact allergens; affects an estimated 5% of eczema patients; skin rash, itching, redness',
            'long_term': 'Sensitisation is permanent; lanolin may be contaminated with pesticide residues (organochlorines) from sheep dip chemicals — highly purified pharmaceutical-grade lanolin is considered safe; environmental persistence of organochlorine contaminants is a concern with lower-grade lanolin',
            'vulnerable_groups': 'People with eczema (high sensitisation rate of ~5–10%); people with lanolin or wool allergy; consumers using lanolin-containing nipple creams while breastfeeding (infants ingest it)'
        },

        # ── Polysorbates ──────────────────────────────────────────────────────
        'polysorbate 80': {
            'short_term': 'Rare anaphylaxis and hypersensitivity reactions (particularly with IV pharmaceutical formulations); topical and oral food-use: generally well tolerated',
            'long_term': 'Animal studies (2015, Chassaing et al. in Nature) showed that polysorbate 80 and polysorbate 20 at concentrations found in food disrupted the intestinal mucosal barrier, promoted gut inflammation and triggered metabolic syndrome and colitis in mice; human evidence is limited but has raised concern about chronic dietary emulsifier exposure and gut permeability',
            'vulnerable_groups': 'People with IBD, Crohn\'s disease, or leaky gut; people with anaphylaxis to polysorbate 80 (documented rare but serious reactions especially with IV drugs like paclitaxel, erythropoietin); people with inflammatory gut conditions'
        },
        'polysorbate 20': {
            'short_term': 'Generally well tolerated; rare hypersensitivity reactions with IV use',
            'long_term': 'Same intestinal barrier disruption concerns as polysorbate 80 from the 2015 animal studies; human evidence lacking but precautionary concern for daily emulsifier intake across multiple food and cosmetic products',
            'vulnerable_groups': 'People with IBD, gut sensitivity, polysorbate hypersensitivity'
        },

        # ── Gelatin ───────────────────────────────────────────────────────────
        'gelatin': {
            'short_term': 'Generally well tolerated; not suitable for vegetarians, vegans, and people following halal/kosher diets (porcine gelatin); rare allergic reactions',
            'long_term': 'Food-grade gelatin is considered safe; historical concern about bovine spongiform encephalopathy (BSE/mad cow disease) transmission via bovine gelatin — risk managed by strict sourcing regulations; provides glycine and proline which are collagen precursors',
            'vulnerable_groups': 'People with allergy to source animal (bovine or porcine gelatin); people adhering to halal, kosher or vegetarian/vegan dietary restrictions; people with phenylketonuria (gelatin contains phenylalanine)'
        },

        # ── Sorbitol ──────────────────────────────────────────────────────────
        'sorbitol': {
            'short_term': 'Osmotic laxative effect at doses >10–50g — bloating, flatulence, abdominal cramping, diarrhoea; onset at doses lower than other sugar alcohols',
            'long_term': 'Safe at food additive use levels; diabetic-friendly sweetener as it has a lower glycaemic index than sucrose; products with >10g/100g sorbitol must carry "excessive consumption may have a laxative effect" warning (EU); no significant long-term concerns',
            'vulnerable_groups': 'People with IBS or functional gut disorders (sorbitol is a well-documented FODMAP trigger); people with fructose malabsorption; children eating large amounts of sugar-free sweets (higher risk of diarrhoea per kg body weight)'
        },

        # ── Fragrance EU Allergens ────────────────────────────────────────────
        'limonene': {
            'short_term': 'Skin sensitisation and contact dermatitis — particularly when oxidised (autooxidation products are the main allergens); slight mucosal irritation with undiluted application',
            'long_term': 'EU declared allergen — must be declared at >0.001% (leave-on) and >0.01% (rinse-off) on labels; sensitisation is permanent; autooxidised limonene is significantly more allergenic than fresh limonene; IFRA restricts its use in perfumery based on sensitisation potential',
            'vulnerable_groups': 'People with existing fragrance allergy; people with eczema; atopic individuals; those using citrus-scented products daily'
        },
        'linalool': {
            'short_term': 'Skin sensitisation — particularly the oxidised (linalool oxide) form is the primary allergen; mild skin irritation in undiluted form',
            'long_term': 'EU declared fragrance allergen requiring label declaration; sensitisation is permanent and cross-reacts with other fragrance components; IFRA guidelines restrict concentration in leave-on products',
            'vulnerable_groups': 'People with fragrance allergy; eczema and atopic dermatitis patients; consumers using lavender-scented products daily'
        },
        'eugenol': {
            'short_term': 'Mucous membrane irritation; skin sensitisation and contact dermatitis; dental pulp irritation when used in tooth care products at high concentrations',
            'long_term': 'EU declared allergen; cytotoxic to dental pulp cells at high concentrations (relevant to dental paste, clove oil); sensitisation is permanent; autooxidation products are more allergenic',
            'vulnerable_groups': 'People with clove or dental product allergy; dentistry patients; people with fragrance allergies; eczema sufferers'
        },
        'geraniol': {
            'short_term': 'Skin sensitisation and allergic contact dermatitis; eye irritant; oxidised geraniol is more allergenic',
            'long_term': 'EU declared fragrance allergen requiring declaration; sensitisation is permanent; IFRA restricts its maximum use in leave-on products',
            'vulnerable_groups': 'People with rose-fragrance allergy; fragrance-sensitive individuals; eczema patients'
        },
        'cinnamaldehyde': {
            'short_term': 'A potent skin sensitiser and contact allergen — one of the most common causes of contact dermatitis; oral mucosa reactions (perioral dermatitis, cheilitis) with cinnamon-flavoured products; can cause asthma exacerbation',
            'long_term': 'EU declared allergen; sensitisation to cinnamaldehyde is one of the most common fragrance allergies globally; permanent sensitisation; IFRA strictly limits its concentration in products',
            'vulnerable_groups': 'People with cinnamon allergy; those with oral mucosa sensitivity; asthmatics; eczema patients; people who use cinnamon-flavoured dental products'
        },
        'coumarin': {
            'short_term': 'Skin sensitisation and allergic contact dermatitis; photosensitisation',
            'long_term': 'EU declared allergen; large oral doses show hepatotoxicity in animal studies — not relevant to food-flavouring levels; EFSA raised concern about coumarin in cinnamon-flavoured products (cassia contains high coumarin); EU limits coumarin in food and cosmetics; IARC Group 3 (not classifiable as carcinogenic to humans)',
            'vulnerable_groups': 'People with cinnamon/cassia allergy; fragrance-sensitive individuals; people with liver disease; children eating large amounts of cinnamon-flavoured food (cassia cinnamon)'
        },
        'hexyl cinnamal': {
            'short_term': 'Skin sensitisation and allergic contact dermatitis; a jasmine-scented fragrance allergen',
            'long_term': 'EU declared fragrance allergen; permanent sensitisation; frequently found in combination with other fragrance allergens',
            'vulnerable_groups': 'People with fragrance allergy; eczema patients; people using jasmine/floral-scented cosmetics daily'
        },

        # ── Alcohol / Ethanol ─────────────────────────────────────────────────
        'alcohol denat': {
            'short_term': 'Skin dryness and irritation with regular use — disrupts the skin\'s lipid barrier; astringent feel; cold sensation on skin; aggravates eczema, rosacea and sensitive skin',
            'long_term': 'Chronic skin barrier disruption leading to increased transepidermal water loss (TEWL); decreases ceramide levels in skin with habitual use; scalp damage in high-alcohol hair products; denatured with bitter agents or methanol to prevent drinking — denaturing agents may be irritating',
            'vulnerable_groups': 'People with eczema, rosacea, dry or sensitive skin; people with alcohol sensitivity; individuals with seborrhoeic dermatitis'
        },
        'sd alcohol': {
            'short_term': 'Same as alcohol denat — skin dryness, irritation, barrier disruption; short-lived antimicrobial effect',
            'long_term': 'Same long-term barrier disruption as alcohol denat; the SD (specially denatured) designation refers to specific denaturing agent used',
            'vulnerable_groups': 'Same as alcohol denat — sensitive, dry and eczema-prone skin types'
        },

        # ── Niacinamide ───────────────────────────────────────────────────────
        'niacinamide': {
            'short_term': 'Occasional transient flushing, itching or redness, especially at high concentrations (>5%) — particularly in the first weeks of use; may cause irritation when combined with acidic Vitamin C (lowers skin pH); generally very well tolerated',
            'long_term': 'One of the best-studied and safest cosmetic actives; clinical evidence for skin brightening, pore minimisation, barrier strengthening and sebum reduction; no known long-term adverse effects at topical cosmetic concentrations',
            'vulnerable_groups': 'People with niacin allergy (rare); people prone to flushing who find initial application uncomfortable; people who combine it with high-concentration Vitamin C products simultaneously'
        },

        # ── Panthenol ─────────────────────────────────────────────────────────
        'panthenol': {
            'short_term': 'Exceptional tolerability; no known short-term adverse effects; rare contact allergy (extremely uncommon)',
            'long_term': 'Excellent long-term safety record; widely used in baby products; provitamin B5 converts to pantothenic acid (Vitamin B5) in the body; wound-healing, anti-inflammatory and moisturising properties are well evidenced',
            'vulnerable_groups': 'Safe for virtually all populations including infants; very rare hypersensitivity reactions are the only documented concern'
        },

        # ── Indian Botanicals ─────────────────────────────────────────────────
        'neem': {
            'short_term': 'Topical: well tolerated on skin; distinctive smell; occasional skin sensitisation; oral neem oil: TOXIC — severe metabolic acidosis, seizures and coma reported in infants given neem oil orally; should never be taken internally',
            'long_term': 'Topical use: generally safe; antimicrobial, anti-inflammatory and wound-healing properties; oral neem oil: documented cases of fatal toxicity in children — NOT safe for oral use; neem seed oil contains azadirachtin which can cause liver and kidney damage with oral ingestion',
            'vulnerable_groups': 'Infants and children (oral neem oil is dangerous — has caused deaths); pregnant women (abortifacient effects reported); people with plant/Meliaceae family allergy'
        },
        'tulsi': {
            'short_term': 'Topical and food use: generally well tolerated; mild anticoagulant properties',
            'long_term': 'Traditional Ayurvedic herb (holy basil / Ocimum sanctum); adaptogenic and antioxidant properties; long-term use as food is safe; very high supplemental doses may affect blood clotting and blood sugar; possible uterine contractions at medicinal doses',
            'vulnerable_groups': 'Pregnant women (avoid medicinal doses — may stimulate uterine contractions); people on anticoagulants (mild blood-thinning effect); people undergoing surgery (discontinue 2 weeks before)'
        },
        'turmeric': {
            'short_term': 'Generally safe; yellow staining of skin and surfaces; very high supplemental curcumin doses: nausea, diarrhoea, liver stress in sensitive individuals; gallbladder contraction with large doses',
            'long_term': 'Excellent safety profile as food spice and cosmetic ingredient; high-dose curcumin supplements may cause hepatotoxicity in rare cases (case reports); curcumin has very poor bioavailability unless combined with piperine (black pepper); potential drug interactions with anticoagulants and diabetes medications at medicinal doses',
            'vulnerable_groups': 'People with gallstones or bile duct obstruction (promotes bile secretion); people on anticoagulants or diabetes medication at high supplemental doses; people with oxalate kidney stones (turmeric is high in oxalates)'
        },
        'aloe vera': {
            'short_term': 'Topical gel: well tolerated; rare contact allergy; occasional skin irritation in sensitive individuals; oral aloe vera: may cause diarrhoea and cramping from anthraquinone laxatives (mainly from the latex, not gel)',
            'long_term': 'Topical use: excellent safety record; soothing, anti-inflammatory and wound-healing properties; IARC classified whole-leaf aloe vera extract (containing anthraquinones) as Group 2B (possibly carcinogenic) — this refers to oral non-decolourised whole-leaf extract, NOT the commonly used decolourised gel; FDA withdrew OTC laxative status for aloe in 2002',
            'vulnerable_groups': 'People with known aloe allergy; people taking diuretics or digoxin (electrolyte interaction with oral aloe); pregnant women (oral aloe latex has uterine stimulant properties — topical gel is safe); people with IBD (oral latex form)'
        },
        'ashwagandha': {
            'short_term': 'Generally well tolerated; mild GI discomfort, drowsiness at high doses; possible thyroid hormone increase',
            'long_term': 'Adaptogenic herb (Withania somnifera) with clinical evidence for stress reduction and cortisol lowering; rare but documented cases of hepatotoxicity at high supplemental doses (case reports, 2021–2023); potential thyroid stimulation — use caution in hyperthyroidism; may enhance thyroid medication effects',
            'vulnerable_groups': 'Pregnant women (avoid — may induce abortion at medicinal doses); people with thyroid conditions; people with autoimmune diseases (immunostimulant effects); people with liver disease; people on immunosuppressants'
        },

        # ── Key Emulsifiers ───────────────────────────────────────────────────
        'polyglycerol polyricinoleate': {
            'short_term': 'Generally well tolerated; rarely associated with adverse effects at food-additive concentrations',
            'long_term': 'PGPR (E476) is used in chocolate to reduce fat content and improve flow; JECFA and EFSA have evaluated it as safe at food-additive use levels; ADI established by JECFA at 7.5 mg/kg/day; no significant long-term concerns established',
            'vulnerable_groups': 'People with known castor oil hypersensitivity (PGPR is derived from ricinoleic acid from castor oil); people with multiple food emulsifier sensitivities'
        },
        'carnauba wax': {
            'short_term': 'Generally well tolerated; food-grade and cosmetic-grade are considered safe; potential rare allergy in hypersensitive individuals',
            'long_term': 'Natural wax from Copernicia prunifera palm leaves; no significant long-term toxicity established; GRAS status (FDA); EU approved as E903; widely used in tablet coatings, sweets and cosmetics',
            'vulnerable_groups': 'People with palm or wax allergy (very rare); generally safe for all populations'
        },
        'shellac': {
            'short_term': 'Generally well tolerated; not suitable for vegans (insect-derived); rare allergic reactions',
            'long_term': 'Natural resin secreted by lac insects (Laccifer lacca); approved as food glaze E904; generally recognised as safe; no significant long-term toxicity concerns',
            'vulnerable_groups': 'Vegans and some religious groups (insect-derived); people with insect-product allergy'
        },

        # ── Key Vitamins and Minerals ─────────────────────────────────────────
        'zinc gluconate': {
            'short_term': 'Mild nausea at higher doses; metallic taste; generally well tolerated at food/cosmetic concentrations',
            'long_term': 'Anti-acne mineral with good evidence at concentrations used in cosmetics; safe within food ADI; excessive supplemental zinc (>40mg/day) causes copper deficiency, impairs immune function and reduces HDL cholesterol; topical use at cosmetic levels is safe',
            'vulnerable_groups': 'People taking zinc supplements above UL (40 mg/day); people with Wilson\'s disease (copper accumulation); kidney disease patients'
        },
        'zinc sulfate': {
            'short_term': 'Nausea and gastric irritation in higher oral doses; eye irritation if used in eye drops without proper dilution',
            'long_term': 'Same long-term concerns as excess zinc supplementation; used as a nutritional supplement; copper deficiency with chronic excess intake',
            'vulnerable_groups': 'People already taking zinc supplements; Wilson\'s disease patients; kidney disease patients'
        },
        'copper gluconate': {
            'short_term': 'Generally well tolerated at food and cosmetic concentrations; excess oral copper causes nausea, vomiting, liver pain',
            'long_term': 'Copper is an essential trace mineral but toxic in excess — liver cirrhosis and neurological damage with chronic copper overload (Wilson\'s disease genetic model); cosmetic use is safe at typical concentrations; copper peptides in skincare are well-researched wound-healing agents',
            'vulnerable_groups': 'People with Wilson\'s disease (impaired copper excretion); people with liver disease; infants under 12 months (immature copper excretion mechanisms)'
        },
        'magnesium aspartate': {
            'short_term': 'Generally well tolerated; high oral magnesium doses cause diarrhoea (osmotic effect) — not relevant to cosmetic use',
            'long_term': 'Magnesium is an essential mineral; deficiency is common in modern diets; supplemental magnesium at high doses (>350mg/day from supplements) may cause loose stools; topical cosmetic use is safe and may support skin enzyme function',
            'vulnerable_groups': 'People with kidney disease (impaired magnesium excretion — risk of hypermagnesaemia with high doses); people on medications that interact with magnesium (antibiotics, muscle relaxants)'
        },
        'ferulic acid': {
            'short_term': 'Generally well tolerated topically and orally; very rare allergic reactions; mild photosensitisation possible',
            'long_term': 'Potent antioxidant with strong evidence for synergistic activity with Vitamins C and E in sunscreens; stabilises Vitamin C formulations; anti-cancer properties shown in cell studies; excellent long-term safety profile both as food antioxidant and cosmetic ingredient',
            'vulnerable_groups': 'People with bran (wheat, rice, oat) allergy — ferulic acid is found in bran; generally safe for all populations'
        },
        'resveratrol': {
            'short_term': 'Topical: generally well tolerated; oral supplements: mild GI side effects at high doses; blood-thinning effect at high doses (antiplatelet activity)',
            'long_term': 'Potent polyphenol antioxidant; oral supplements have poor bioavailability (rapid metabolism); topical application delivers directly to skin — good anti-ageing evidence; very high supplemental doses (>1g/day) may interfere with oestrogen metabolism; anti-inflammatory, anti-carcinogenic properties in cell studies',
            'vulnerable_groups': 'People on anticoagulants (antiplatelet activity); people on oestrogen therapy or with oestrogen-sensitive conditions at high supplemental doses; people scheduled for surgery (blood-thinning effect)'
        },
        'bakuchiol': {
            'short_term': 'Excellent tolerability — much milder than retinol; minimal irritation, dryness or photosensitivity; rare contact sensitisation',
            'long_term': 'Plant-based retinol alternative from babchi (Psoralea corylifolia) seeds; clinical studies show comparable anti-ageing efficacy to 0.5% retinol with significantly less irritation; considered safe in pregnancy as a retinol substitute (though human data is limited); good long-term skin tolerability',
            'vulnerable_groups': 'Pregnant women (considered a retinol alternative but human pregnancy safety data is still limited); people with Psoralea/legume allergy (very rare)'
        },
        'squalane': {
            'short_term': 'Exceptional tolerability — non-comedogenic, non-irritating, non-sensitising; one of the most universally tolerated cosmetic emollients',
            'long_term': 'Naturally found in human sebum; stable, plant-derived (typically from olive, sugarcane or amaranth) or shark-liver-derived squalane (avoid shark-sourced for ethical reasons); excellent long-term safety record; antioxidant and emollient properties; no significant concerns established',
            'vulnerable_groups': 'Shark-liver-derived squalane raises ethical concerns; olive-derived squalane is safe for all; virtually no adverse effects reported'
        },
        'sodium ascorbyl phosphate': {
            'short_term': 'Excellent tolerability — significantly less irritating than L-ascorbic acid; rare contact dermatitis; stable in formulations',
            'long_term': 'Well-studied stable Vitamin C derivative; antioxidant, collagen-stimulating and antimicrobial properties; converts to active ascorbic acid in the skin; good long-term safety record; anti-acne properties shown in several studies',
            'vulnerable_groups': 'People with ascorbic acid or ascorbyl derivative allergy (very rare); generally safe for all skin types including sensitive'
        },
        'centella asiatica': {
            'short_term': 'Generally well tolerated; rare contact allergy; mild photosensitisation possible',
            'long_term': 'Traditional medicinal plant (gotu kola); strong evidence for wound healing, collagen synthesis stimulation and anti-inflammatory effects; madecassoside (a key active) has good safety data; long-term safety well established in traditional use',
            'vulnerable_groups': 'People with allergy to Centella asiatica or Apiaceae plant family; people on sedative medications (mild sedative properties with oral use)'
        },
        'allantoin': {
            'short_term': 'Exceptional tolerability — widely used in products for sensitive and damaged skin; no known short-term adverse effects at cosmetic concentrations',
            'long_term': 'Naturally occurring metabolite of uric acid; excellent wound-healing, anti-irritant and cell-proliferating properties; long history of safe use in dermatology; no significant long-term concerns',
            'vulnerable_groups': 'Safe for virtually all populations including infants; people with allantoin hypersensitivity (extremely rare)'
        },
        'bisabolol': {
            'short_term': 'Exceptional tolerability — anti-inflammatory and soothing properties reduce, rather than cause, irritation; very rare allergy in people with composite (daisy) family hypersensitivity',
            'long_term': 'Naturally derived from chamomile or synthetically produced; potent anti-irritant and anti-inflammatory; clinical evidence for reducing skin sensitivity and enhancing wound healing; excellent long-term safety record',
            'vulnerable_groups': 'People with chamomile or daisy family allergy (Asteraceae/Compositae) — rare but documented cross-reactivity'
        },

        # ── BHT ───────────────────────────────────────────────────────────────
        'butylated hydroxytoluene': {
            'short_term': 'Skin and eye irritation at high concentrations; rare contact dermatitis; very low acute toxicity at food-additive levels',
            'long_term': 'IARC Group 3 (not classifiable as carcinogenic to humans — insufficient evidence); animal studies at high doses show liver enlargement, thyroid tumour promotion and hormonal disruption; Japan has banned it in food; California Prop 65 does not list it (unlike BHA) but regulatory reviews are ongoing; at food-additive levels human risk is considered low',
            'vulnerable_groups': 'People with thyroid conditions (thyroid promoter effects in animal studies); heavy consumers of highly processed foods containing multiple antioxidant preservatives; people with known BHT contact allergy'
        },
        'bht': {
            'short_term': 'Generally well tolerated at food-additive concentrations; rare contact allergy',
            'long_term': 'Liver and thyroid effects in high-dose animal studies; hormonal disruption debate; banned in Japan; IARC Group 3; combined BHA+BHT intake should be within ADI limits',
            'vulnerable_groups': 'People with thyroid conditions; people with liver disease; those consuming high amounts of preserved processed foods daily'
        },

        # ── Propyl Gallate ────────────────────────────────────────────────────
        'propyl gallate': {
            'short_term': 'Skin and mucous membrane irritation; gastric irritation; occasional allergic reactions; contact dermatitis in sensitive individuals',
            'long_term': 'Weak oestrogenic activity in some in vitro studies; IARC Group 3 (not classifiable); banned in Japan; EU has placed it on the "Substances of Very High Concern" watch list; some animal studies show thyroid and reproductive effects at high doses; suspected endocrine disruptor at higher concentrations',
            'vulnerable_groups': 'People with known gallate hypersensitivity; people with aspirin/salicylate sensitivity (cross-reactivity possible); people with hormone-sensitive conditions; pregnant women (precautionary)'
        },
        'e310': {
            'short_term': 'Skin irritation; rare allergic reactions; gastric discomfort at high doses',
            'long_term': 'Same as propyl gallate — weak endocrine disruption in vitro; banned Japan; EU watch list; animal thyroid effects at high doses',
            'vulnerable_groups': 'Aspirin-sensitive individuals, people with hormone-sensitive conditions'
        },

        # ── EDTA ──────────────────────────────────────────────────────────────
        'tetrasodium edta': {
            'short_term': 'Topical: generally well tolerated; skin irritation at high concentrations; IV use in chelation therapy: hypocalcaemia (dangerously low calcium — fatal cases reported)',
            'long_term': 'Acts as a penetration enhancer — increases skin absorption of other cosmetic ingredients including potentially harmful ones; strips essential trace minerals (calcium, zinc, iron, magnesium) with prolonged oral or IV use; environmental persistence — not biodegradable, accumulates in water systems and mobilises heavy metals from sediment',
            'vulnerable_groups': 'People with mineral deficiencies; people with cardiovascular disease (calcium depletion risk with IV use); pregnant women; aquatic ecosystems (environmental concern); patients receiving chelation therapy (IV EDTA has caused deaths from hypocalcaemia)'
        },
        'disodium edta': {
            'short_term': 'Topical: similar to tetrasodium EDTA — mild irritant at high concentrations; enhances penetration of co-formulated ingredients',
            'long_term': 'Same penetration-enhancing and mineral-stripping concerns as tetrasodium EDTA; environmental persistence and heavy metal mobilisation; oral/IV use causes calcium depletion; approved as food additive (E385) at low concentrations with ADI',
            'vulnerable_groups': 'People with mineral deficiencies; pregnant women; anyone using multiple products containing EDTA simultaneously; aquatic ecosystems'
        },

        # ── Fragrance EU 26 Allergens (remaining) ────────────────────────────
        'benzyl salicylate': {
            'short_term': 'Allergic contact dermatitis and photoallergic reactions (sun activates the allergen); skin rash and sensitisation',
            'long_term': 'EU declared fragrance allergen — must be declared at >0.001% (leave-on) and >0.01% (rinse-off); photoallergic reactions (UV-triggered) are particularly problematic as they occur every time the sensitised person uses a UV-containing product; permanent sensitisation once acquired',
            'vulnerable_groups': 'People with fragrance allergy; people who spend time in the sun after applying products containing it; people with atopic dermatitis or eczema'
        },
        'benzyl benzoate': {
            'short_term': 'Skin irritation and contact sensitisation; a known topical irritant at higher concentrations; used as a scabicide/pediculicide at pharmaceutical doses which cause burning and itching',
            'long_term': 'EU declared fragrance allergen; toxic to cats (important if pets lick treated skin); permanent sensitisation; at pharmaceutical scabicide doses (25% cream) — CNS toxicity if massaged into broken skin in large amounts',
            'vulnerable_groups': 'Fragrance-allergic individuals; people with eczema or broken skin; households with cats (benzyl benzoate is highly toxic to cats even in cosmetic concentrations); children treated for scabies'
        },
        'farnesol': {
            'short_term': 'Allergic contact dermatitis; skin sensitisation — one of the more potent fragrance sensitisers; floral/muguet aroma',
            'long_term': 'EU declared fragrance allergen requiring declaration; animal studies show anti-androgenic activity at high doses; sensitisation is permanent; IFRA restricts maximum concentration',
            'vulnerable_groups': 'People with fragrance allergy; men with hormone-sensitive conditions (anti-androgenic at high doses — not relevant to cosmetic use but noted); eczema patients'
        },
        'hydroxycitronellal': {
            'short_term': 'Allergic contact dermatitis; skin sensitisation; photosensitisation possible',
            'long_term': 'EU declared fragrance allergen; IFRA classification restricts use due to sensitisation potential; some endocrine disruption evidence in vitro at high concentrations; permanent sensitisation',
            'vulnerable_groups': 'Fragrance-allergic individuals; people with eczema; people with hormone-sensitive conditions (precautionary at high exposures)'
        },
        'isoeugenol': {
            'short_term': 'One of the most potent fragrance sensitisers — causes significant allergic contact dermatitis; skin and mucous membrane irritation; clove-like aroma',
            'long_term': 'EU declared allergen and one of the most common causes of fragrance contact allergy globally; IFRA severely restricts its use due to high sensitisation potential; permanent sensitisation — cross-reacts with eugenol and other phenylpropanoids',
            'vulnerable_groups': 'Anyone using fragrance products regularly — sensitisation rate is significant; people with eczema or atopic dermatitis; people with clove allergy'
        },
        'cinnamyl alcohol': {
            'short_term': 'Allergic contact dermatitis; skin sensitisation; oxidises to cinnamaldehyde (an even stronger sensitiser) on skin',
            'long_term': 'EU declared allergen; oxidation products on skin and in formulations are more allergenic than the parent compound; permanent sensitisation; cross-reacts with cinnamaldehyde and other cinnamic derivatives',
            'vulnerable_groups': 'Fragrance-allergic individuals; people using cinnamon-scented products; eczema and atopic dermatitis patients'
        },
        'citronellol': {
            'short_term': 'Skin sensitisation and allergic contact dermatitis — milder than most other EU declared allergens but still significant; rose-citrus aroma',
            'long_term': 'EU declared fragrance allergen requiring label declaration; sensitisation is permanent; IFRA guidelines restrict concentration in leave-on products',
            'vulnerable_groups': 'People with fragrance allergy; eczema sufferers; consumers using rose or citrus-scented cosmetics daily'
        },
        'alpha-isomethyl ionone': {
            'short_term': 'Allergic contact dermatitis; skin sensitisation; violet/floral aroma',
            'long_term': 'EU declared fragrance allergen; sensitisation permanent; IFRA restricts use concentration; sometimes causes cross-reactivity with other ionones',
            'vulnerable_groups': 'Fragrance-allergic individuals; people with eczema; consumers using violet or iris-scented products'
        },
        'amyl cinnamal': {
            'short_term': 'Allergic contact dermatitis; skin and eye sensitisation; jasmine-like fragrance',
            'long_term': 'EU declared fragrance allergen; sensitisation permanent; IFRA restricts maximum use level in leave-on products; cross-reacts with cinnamaldehyde derivatives',
            'vulnerable_groups': 'Fragrance-allergic individuals; people with eczema; eczema-prone individuals using jasmine-scented products'
        },
        'benzyl cinnamate': {
            'short_term': 'Allergic contact dermatitis; mild skin sensitiser',
            'long_term': 'EU declared fragrance allergen; one of the less potent of the 26 declared allergens; permanent sensitisation; found in balsam of Peru and related natural fragrance materials',
            'vulnerable_groups': 'People with fragrance allergy; people with Peru balsam allergy (cross-reactivity is significant)'
        },

        # ── Fatty Alcohols ────────────────────────────────────────────────────
        'cetyl alcohol': {
            'short_term': 'Very well tolerated topically; rare contact dermatitis in sensitive individuals; despite the name "alcohol" it is a fatty alcohol (waxy solid), not a drying alcohol',
            'long_term': 'Excellent long-term safety record; naturally derived from palm or coconut oil; emollient and emulsifier; no significant long-term concerns; the rare contact dermatitis cases are usually from impurities rather than the pure compound',
            'vulnerable_groups': 'People with documented cetyl alcohol contact allergy; people with eczema using products containing it for the first time (patch test recommended for sensitive skin)'
        },
        'cetearyl alcohol': {
            'short_term': 'Same as cetyl alcohol — well tolerated fatty wax; rare contact allergy; emollient and stabiliser',
            'long_term': 'One of the most commonly used and well-tolerated cosmetic emollients; excellent safety record; naturally derived; very rare cases of contact allergy documented',
            'vulnerable_groups': 'People with documented fatty alcohol sensitivity; eczema patients who have previously reacted to fatty alcohols (uncommon but documented)'
        },
        'stearyl alcohol': {
            'short_term': 'Well tolerated; non-drying waxy emollient; very rare contact allergy',
            'long_term': 'Excellent long-term safety record; derived from natural sources; emollient and viscosity modifier; rare documented contact allergy cases',
            'vulnerable_groups': 'People with known fatty alcohol allergy (very rare); those with multiple cosmetic ingredient sensitivities'
        },
        'behenyl alcohol': {
            'short_term': 'Excellent tolerability — one of the most inert fatty alcohols used in cosmetics; rare contact allergy',
            'long_term': 'C22 fatty alcohol with no significant safety concerns; good hair-conditioning properties; no long-term toxicity concerns established',
            'vulnerable_groups': 'Same precautionary note as other fatty alcohols — very rare allergy possible; safe for general use'
        },

        # ── Quaternary Ammonium Compounds ─────────────────────────────────────
        'behentrimonium chloride': {
            'short_term': 'Well tolerated in rinse-off hair conditioners at typical use concentrations; eye irritation if product enters eyes; skin irritation at high concentrations',
            'long_term': 'A cationic quat (C22) used as a hair conditioner; lower irritation potential than shorter-chain quats; environmental concern — quats are persistent in water systems and have some antimicrobial toxicity to aquatic organisms; very rare contact allergy',
            'vulnerable_groups': 'People with quat sensitivity; people with scalp conditions (occupational hairdresser exposure); sensitive eyes if conditioner not fully rinsed'
        },
        'behentrimonium methosulfate': {
            'short_term': 'Well tolerated; milder than the chloride counterpart; conditioning agent for hair',
            'long_term': 'Same environmental persistence concerns as other quats; generally good safety profile in rinse-off hair care; no significant long-term human health concerns at cosmetic concentrations',
            'vulnerable_groups': 'People with quat allergy (rare); environmental concern for aquatic organisms'
        },
        'cetrimonium chloride': {
            'short_term': 'Eye and skin irritation at higher concentrations; contact sensitisation in some individuals; cytotoxic at high concentrations',
            'long_term': 'Strong quat preservative and conditioning agent; can disrupt skin and mucous membrane barrier at high concentrations; environmental persistence; moderate contact allergy potential; studies show cytotoxicity to hair follicle cells at high concentrations',
            'vulnerable_groups': 'People with quat allergy; people using multiple quat-containing products; aquatic ecosystems; people with sensitive scalp'
        },
        'cetrimonium bromide': {
            'short_term': 'More irritating than chloride counterpart; contact sensitisation; skin and eye irritant',
            'long_term': 'Potent quat with antimicrobial and cytotoxic activity; environmental persistence; same concerns as cetrimonium chloride but generally higher irritation potential',
            'vulnerable_groups': 'People with quat allergy; individuals with sensitive skin or scalp'
        },

        # ── Isopropyl Alcohol ──────────────────────────────────────────────────
        'isopropyl alcohol': {
            'short_term': 'Skin dryness and barrier disruption with regular topical use; burning sensation on broken skin; inhalation of high concentrations causes headache, dizziness, CNS depression; eye irritant',
            'long_term': 'Chronic topical exposure damages the skin lipid barrier; repeated application leads to xerosis (skin dryness), increased skin permeability and potential for secondary infection; unlike ethanol, isopropyl alcohol is metabolised to acetone — not to toxic acetaldehyde; no significant long-term carcinogenicity concerns at cosmetic use levels',
            'vulnerable_groups': 'People with eczema, psoriasis, dry skin; infants (higher skin permeability, limited metabolic capacity); people using it as a wound-cleaning agent on large areas (absorption concern); people with isopropanol inhalation exposure'
        },

        # ── Polydextrose / Inulin ─────────────────────────────────────────────
        'polydextrose': {
            'short_term': 'Osmotic laxative effect at high doses (>50g) — bloating, flatulence, loose stools; better tolerated than sorbitol or lactulose',
            'long_term': 'Soluble dietary fibre with prebiotic properties; promotes beneficial gut bacteria; no significant long-term toxicity; EU and FDA approved; "excessive consumption may have a laxative effect" label required above certain doses',
            'vulnerable_groups': 'People with IBS (may worsen symptoms at high doses); people with short bowel syndrome; children eating large amounts of fibre-enriched products'
        },
        'inulin': {
            'short_term': 'Bloating, flatulence, abdominal cramping — particularly during first week of use as gut microbiome adapts; dose-dependent (typically >10g/day causes symptoms)',
            'long_term': 'Highly beneficial prebiotic fibre — selectively feeds beneficial Bifidobacterium and Lactobacillus; reduces appetite hormones (ghrelin), increases satiety hormones (PYY); positive cardiovascular effects; safe with long-term use when dose is titrated gradually',
            'vulnerable_groups': 'People with IBS or SIBO (small intestinal bacterial overgrowth) — inulin is a major FODMAP; people with fructan intolerance; people with Crohn\'s disease (during flares)'
        },
        'maltodextrin': {
            'short_term': 'Very high glycaemic index (GI 85–105, exceeding table sugar) — causes rapid blood glucose spike; energy crash; bloating in some individuals',
            'long_term': 'Regular high intake contributes to same metabolic risks as excess sugar; Chassaing et al. (2015, Nature) showed dietary emulsifiers including maltodextrin disrupted the gut mucosal barrier and promoted metabolic syndrome and colitis in mice — human implications under investigation; may promote adherent-invasive E. coli (associated with Crohn\'s disease)',
            'vulnerable_groups': 'Diabetics and pre-diabetics (extreme glucose spike); people with IBD particularly Crohn\'s disease; people on low-FODMAP diets; people seeking "clean label" foods'
        },

        # ── UV Filters ────────────────────────────────────────────────────────
        'avobenzone': {
            'short_term': 'Generally well tolerated; rare allergic contact dermatitis and photoallergic reactions; mild skin sensitisation in some individuals',
            'long_term': 'Photolabile — degrades rapidly (within 30 min) in sunlight to potentially harmful breakdown products; photodegradation products may be allergenic and more toxic than the parent compound; requires photostabilisers (Tinosorb S/M or octocrylene) to maintain efficacy; detected in blood, urine and breast milk with regular use; FDA classifies as "not generally recognised as safe" due to insufficient systemic absorption data',
            'vulnerable_groups': 'Pregnant women and infants (systemic absorption/breast milk concern); people with sunscreen allergy; people with history of photoallergic reactions; people using sunscreen without photostabilisers'
        },
        'octinoxate': {
            'short_term': 'Skin sensitisation and contact/photoallergic dermatitis in some users; mild hormonal activity',
            'long_term': 'One of the most widely studied chemical sunscreens — significant dermal absorption detected; acts as a weak oestrogen and anti-androgen in animal and in vitro studies; FDA classifies as "not generally recognised as safe" due to systemic absorption and potential endocrine effects; Hawaii and Palau have banned it (coral reef toxicity); detected in human blood, urine and breast milk',
            'vulnerable_groups': 'Pregnant women and foetuses (systemic absorption); infants (high surface area to body ratio); people with hormone-sensitive conditions; coral reef ecosystems; people with photoallergy history'
        },
        'octocrylene': {
            'short_term': 'Allergic and photoallergic contact dermatitis; increasingly recognised as a significant allergen; skin sensitisation',
            'long_term': 'A UV stabiliser for avobenzone as well as a UV absorber itself; accumulates in coral tissue (coral reef toxicity); degrades in sunscreen products to benzophenone — a potential carcinogen (FDA 2021 study found benzophenone contamination in products with octocrylene); FDA classifies as "not generally recognised as safe"; cross-reacts with ketoprofen (NSAID) causing severe photoallergic reactions in sensitised individuals',
            'vulnerable_groups': 'People taking ketoprofen or other benzophenone-related medications (cross-photoallergy); people with photodermatitis; pregnant women; infants; coral reef ecosystems'
        },
        'ethylhexyl salicylate': {
            'short_term': 'Generally well tolerated; mild skin sensitisation in some individuals; rare photoallergic reactions',
            'long_term': 'EU-approved UVB filter; weak oestrogenic activity in some in vitro studies — clinical significance at cosmetic use levels not established; detected in human blood at low levels with regular use; considered safer than oxybenzone but under review',
            'vulnerable_groups': 'Pregnant women (precautionary — weak oestrogenic activity); people with aspirin/salicylate sensitivity (may cross-react); infants'
        },

        # ── Anti-acne and Brightening Actives ────────────────────────────────
        'benzoyl peroxide': {
            'short_term': 'Skin dryness, peeling, redness and burning — especially in the first 2–4 weeks; significant skin bleaching effect (bleaches fabrics, hair, eyebrows); rare contact dermatitis; eye, nose and throat irritation if aerosolised',
            'long_term': 'Highly effective acne treatment with 40+ years of evidence; free radical generator — theoretical oxidative stress concerns but no established carcinogenicity in topical use at approved concentrations; FDA-approved OTC at 2.5–10%; long-term use is well-tolerated; photosensitising — SPF use recommended',
            'vulnerable_groups': 'Pregnant women (Category C — limited safety data, use under medical supervision); people with eczema or rosacea; people with sensitive skin; anyone wearing coloured clothing or fabrics (bleaching damage)'
        },
        'zinc pyrithione': {
            'short_term': 'Generally well tolerated in anti-dandruff shampoos; scalp irritation in some users; eye irritation if product enters eyes; toxic to cats and fish',
            'long_term': 'Effective anti-fungal (Malassezia) and anti-bacterial agent for seborrhoeic dermatitis and dandruff; systemic absorption is very low from rinse-off products; EU restricted in leave-on cosmetics (concern about aquatic toxicity and potential developmental toxicity); highly toxic to aquatic organisms — not biodegradable; some reproductive toxicity at high doses in animal studies',
            'vulnerable_groups': 'Pregnant and breastfeeding women (use leave-on products with caution); people with sensitive scalp; households with fish or cats (never dispose of ZPT-containing products in aquatic environments)'
        },
        'alpha arbutin': {
            'short_term': 'Very well tolerated — significantly gentler than hydroquinone; rare contact allergy; no significant short-term adverse effects at cosmetic concentrations',
            'long_term': 'Alpha-arbutin inhibits tyrosinase but does not itself degrade to hydroquinone to the same extent as beta-arbutin; at very high concentrations some hydrolysis to hydroquinone is theoretically possible — EU limits alpha-arbutin to 2% in face products and 0.5% in body products; hydroquinone is a known skin depigmenting agent with ochronosis (skin darkening paradox) and carcinogenicity concerns at high doses',
            'vulnerable_groups': 'Pregnant women (EU restricts use — hydroquinone concerns); people with known hydroquinone sensitivity; people using high-concentration arbutin products beyond EU limits'
        },
        'arbutin': {
            'short_term': 'Beta-arbutin: slightly more irritating than alpha-arbutin; can hydrolyse to hydroquinone more readily than alpha form',
            'long_term': 'Beta-arbutin more readily degrades to hydroquinone than alpha form; EU restricts beta-arbutin in body lotions and facial products to lower concentrations; hydroquinone at high topical concentrations can cause ochronosis (paradoxical skin darkening), a permanent condition',
            'vulnerable_groups': 'Pregnant women; people using high-concentration beta-arbutin; people with sensitive skin; those who previously reacted to hydroquinone'
        },
        'kojic acid': {
            'short_term': 'Skin irritation, contact dermatitis, and sensitisation — a more irritating brightener than niacinamide or arbutin; redness and stinging are common, especially >1%',
            'long_term': 'Tyrosinase inhibitor for skin brightening; some animal studies show thyroid effects at very high oral doses — not relevant to topical cosmetic use; EU restricts kojic acid to 1% in face products; potential skin sensitisation with prolonged use; some in vitro mutagenicity data — EFSA found insufficient evidence of carcinogenicity in humans at cosmetic levels',
            'vulnerable_groups': 'People with sensitive skin or eczema; people with known kojic acid hypersensitivity; pregnant women (precautionary — limited data); people using concentrations above EU limit (1%)'
        },
        'glycolic acid': {
            'short_term': 'Stinging, burning, erythema and peeling proportional to concentration and pH; 10%+ concentrations can cause chemical burns; significant photosensitisation — must use SPF',
            'long_term': 'Most well-studied AHA with excellent clinical evidence for exfoliation, anti-ageing and hyperpigmentation treatment; chronic sun exposure without SPF use can negate benefits and increase photo-ageing and skin cancer risk; FDA requires a "use sunscreen" warning on AHA-containing products; long-term use at appropriate concentrations has good safety record',
            'vulnerable_groups': 'Pregnant women (use with caution — glycolic acid is largely safe but high-strength peels should be avoided); people with rosacea or eczema; people who cannot commit to daily SPF use; people with melanin-rich skin (higher risk of post-inflammatory hyperpigmentation from chemical burns)'
        },
        'azelaic acid': {
            'short_term': 'Initial tingling, itching or mild burning — common in first 2–4 weeks; generally much less irritating than glycolic acid or retinol; rare contact allergy',
            'long_term': 'Anti-acne (inhibits P. acnes), anti-rosacea (anti-inflammatory) and skin-brightening (tyrosinase inhibitor) with strong clinical evidence; FDA-approved OTC (15% for rosacea, 20% prescription); considered safe in pregnancy (Category B); excellent long-term tolerance; no established serious long-term concerns',
            'vulnerable_groups': 'People with known azelaic acid allergy (rare); people with severe eczema (transient irritation at initiation); otherwise one of the safest brightening and anti-acne actives available'
        },

        # ── Food Additives (miscellaneous) ────────────────────────────────────
        'l-cysteine': {
            'short_term': 'Generally well tolerated at food additive levels; high oral supplemental doses (>7g/day) may cause CNS toxicity',
            'long_term': 'Used as a dough conditioner (E920) in bread; sourced from human hair, duck feathers, hog hair or synthesised — raises religious, ethical and dietary (vegan/halal/kosher) concerns; the cysteine itself is a natural amino acid with no significant toxicity at food-additive use levels; at very high supplemental doses, promotes cystine kidney stone formation',
            'vulnerable_groups': 'Vegans and vegetarians (non-synthetic L-cysteine is animal-derived); people adhering to halal or kosher dietary requirements (source matters); people prone to cystine kidney stones'
        },
        'potassium nitrite': {
            'short_term': 'Same as sodium nitrite — methaemoglobinaemia risk at high doses; acute nausea and hypotension',
            'long_term': 'Converts to nitrite in the body with same nitrosamine-forming and colorectal cancer concerns as sodium nitrite; used in some cured meats as an alternative curing salt; IARC classifies processed meat consumption (partly attributable to nitrites/nitrates) as Group 1 carcinogenic',
            'vulnerable_groups': 'Infants under 6 months (methaemoglobinaemia), regular processed meat consumers, people with GERD'
        },
        'charcoal': {
            'short_term': 'Topical use in skincare: generally well tolerated; theoretical adsorption of some beneficial topical actives; oral activated charcoal: binds medications and reduces their effectiveness; temporary black stools; nausea',
            'long_term': 'Activated charcoal in food and beverages: FDA has not approved it as a food additive — trend in charcoal-coloured foods/drinks is unregulated; may adsorb nutrients and medications if consumed regularly; topical activated charcoal in cleansers has limited evidence for deep pore cleansing; potential for skin dryness with overuse',
            'vulnerable_groups': 'People on any medications (activated charcoal binds and neutralises drugs — take medications 2 hours apart from activated charcoal); pregnant women; people with constipation or bowel obstruction'
        },
        'green s': {
            'short_term': 'Urticaria, rhinitis, hypersensitivity reactions; cross-sensitivity with aspirin; skin rash',
            'long_term': 'E142 — banned in USA, Canada, Australia, Norway, Japan; some evidence of hyperactivity in children like other azo dyes; limited long-term human data; IARC has not specifically evaluated it',
            'vulnerable_groups': 'Children (hyperactivity risk), aspirin-sensitive individuals, asthmatics, people with food colour sensitivity'
        },
        'e142': {
            'short_term': 'Urticaria, asthma, hypersensitivity reactions; aspirin cross-reactivity',
            'long_term': 'Banned in USA, Canada, Australia, Norway, Japan — safety concerns; limited long-term data',
            'vulnerable_groups': 'Children, aspirin-sensitive individuals, asthmatics'
        },
        'brilliant black': {
            'short_term': 'Hypersensitivity reactions; urticaria; asthma attacks; aspirin cross-reactivity',
            'long_term': 'E151 — banned in USA, Canada, Australia, Belgium, Denmark, France, Germany, Switzerland, Sweden — safety concerns; azo dye with hyperactivity concerns; limited long-term human safety data',
            'vulnerable_groups': 'Children (hyperactivity), aspirin-sensitive individuals, asthmatics, people with azo dye intolerance'
        },
        'e151': {
            'short_term': 'Urticaria, asthma, hypersensitivity; aspirin cross-reactivity',
            'long_term': 'Brilliant Black BN — banned in multiple countries including USA, Canada, Australia; safety concerns; hyperactivity link',
            'vulnerable_groups': 'Children, aspirin-sensitive individuals, asthmatics'
        },

        # ── Ceramides and Skin Barrier Ingredients ────────────────────────────
        'ceramide': {
            'short_term': 'Excellent tolerability — ceramides are naturally found in human skin and are essentially hypoallergenic; rare allergy to vehicle ingredients but not ceramide itself',
            'long_term': 'Ceramides are essential structural lipids in the stratum corneum (skin barrier); depleted in eczema, ageing and barrier-damaged skin; topical ceramide supplementation has strong clinical evidence for barrier repair in atopic dermatitis; excellent long-term safety — CeraVe and other ceramide-rich products are widely recommended by dermatologists',
            'vulnerable_groups': 'Safe for all populations including infants and people with eczema; one of the most universally tolerated skincare ingredients'
        },
        'sodium pca': {
            'short_term': 'Exceptional tolerability — naturally present in human skin as part of the Natural Moisturising Factor (NMF); no known adverse effects at any cosmetic concentration',
            'long_term': 'One of the most effective humectants available; identical to the body\'s own NMF component; draws moisture from the air and deeper skin layers to the stratum corneum; no long-term toxicity concerns; excellent compatibility with all skin types',
            'vulnerable_groups': 'Safe for all populations including sensitive skin and infants; no restrictions'
        },
        'urea': {
            'short_term': 'At cosmetic concentrations (3–10%): effective humectant with no adverse effects; at higher concentrations (>20%): mild initial stinging on application to cracked or eczematous skin; very rare contact allergy',
            'long_term': 'Naturally found in human skin as an NMF component; at 3–10%: pure humectant; at 10–20%: mild exfoliating and anti-pruritic (anti-itch) properties; at 20–40%: keratolytic (dissolves thickened skin on calluses and nail conditions); excellent long-term safety record — well-documented in dermatology for decades; no established systemic concerns with topical use',
            'vulnerable_groups': 'People with very sensitive skin (initial stinging at high concentrations); infants (use low concentrations only); people with formaldehyde allergy (rare cases of urea decomposition to formaldehyde — theoretical at very high temperatures)'
        },
        'dimethiconol': {
            'short_term': 'Excellent tolerability — a non-volatile silicone polymer; no known short-term adverse effects; non-comedogenic; non-sensitising',
            'long_term': 'A high-molecular-weight silicone used for hair conditioning and skin smoothing; does not penetrate skin due to large molecular size; no established long-term health concerns; not cyclic (unlike D4/D5) so no EU PBT restrictions; minimal environmental persistence compared to cyclosiloxanes',
            'vulnerable_groups': 'No specific vulnerable groups for this ingredient; safe for all populations'
        },
        'benzalkonium chloride': {
            'short_term': 'Skin and mucous membrane irritation — concentration dependent; eye irritation (avoid in eye drops without proper dilution); rare severe anaphylactic reactions; damages the nasal mucosal barrier in nasal sprays (paradoxical worsening of nasal symptoms)',
            'long_term': 'One of the most used antiseptic preservatives; increasingly associated with contact allergy; contributes to antimicrobial resistance (quat resistance in bacteria linked to cross-resistance to antibiotics); long-term use in nasal sprays damages cilia and mucosal barrier; environmental persistence',
            'vulnerable_groups': 'People with known benzalkonium chloride allergy; people using nasal sprays long-term (mucosal damage); contact lens wearers (not compatible — absorbed by soft lenses); people with reactive airway disease'
        },

        # ── Common Amino Acids and Proteins ────────────────────────────────────
        'hydrolyzed keratin': {
            'short_term': 'Excellent tolerability; very rare allergy to keratin protein; sometimes formulated with formaldehyde-based cross-linkers in salon keratin treatments — the cross-linker is the hazard, not keratin itself',
            'long_term': 'Hydrolysed keratin (small peptides and amino acids from keratin) coats the hair shaft and reduces breakage; no significant long-term safety concerns for the ingredient itself; salon "keratin straightening treatments" may use formaldehyde as cross-linker — an entirely separate hazard',
            'vulnerable_groups': 'People with keratin or egg/wool allergy (rare); salon workers using formaldehyde-based keratin straightening systems (not the hydrolysed keratin ingredient)'
        },
        'hydrolyzed collagen': {
            'short_term': 'Generally very well tolerated topically; rare allergy in people with fish, bovine or porcine sensitivity (source-dependent); no known short-term adverse effects',
            'long_term': 'Hydrolysed collagen (collagen peptides) form a film on skin and hair for temporary smoothing; oral collagen peptide supplements have clinical evidence for joint and skin benefits; no significant long-term safety concerns at cosmetic use levels; marine collagen allergy is more common than bovine in fish-allergic individuals',
            'vulnerable_groups': 'People with fish or shellfish allergy (marine-derived collagen); people with bovine/porcine allergy (animal-derived collagen); vegans (all collagen is animal-derived)'
        },
        'hydrolyzed wheat protein': {
            'short_term': 'Rare but documented severe allergic reactions in wheat/gluten-intolerant individuals — particularly hydrolysed wheat protein in shampoos has been linked to wheat allergy induction in Japan (major outbreak, 2011)',
            'long_term': 'The Japanese "Cha no Shizuku" soap incident (2011) demonstrated that topically applied hydrolysed wheat protein induced wheat allergy in thousands of people who then suffered anaphylaxis upon eating wheat — this led to WHO review of hydrolysed protein safety; currently EU requires specific labelling; the degree of hydrolysis affects allergenicity — smaller peptides are more likely to sensitise',
            'vulnerable_groups': 'People with coeliac disease or wheat/gluten allergy — AVOID; people who consume wheat regularly and use hydrolysed wheat protein topically (sensitisation risk); people with multiple food allergies'
        },

        # ════════════════════════════════════════════════════════════════════
        # PACKAGED FOOD AND ICE CREAM INGREDIENTS
        # ════════════════════════════════════════════════════════════════════

        # ── Emulsifiers ───────────────────────────────────────────────────────
        'mono and diglycerides': {
            'short_term': 'Generally well tolerated at food-additive levels; no significant immediate effects in most people; some individuals report mild GI discomfort with high intake',
            'long_term': 'Mono and diglycerides of fatty acids (E471) are partial glycerides — the body treats them like dietary fats; the critical concern is their SOURCE: if derived from partially hydrogenated oils, they may contain trans fats which are NOT required to be declared on the trans fat label (a regulatory loophole in the USA and many countries); trans fat-derived E471 raises LDL cholesterol and increases cardiovascular disease risk; animal studies suggest that, like other emulsifiers, they may alter gut microbiome composition with chronic high intake; most modern food-grade E471 is derived from palm or sunflower oil (not hydrogenated)',
            'vulnerable_groups': 'People with cardiovascular disease or high cholesterol (if trans-fat-derived); people seeking to avoid trans fats (labelling loophole means hidden trans fats are possible); people with inflammatory bowel disease (chronic emulsifier intake concern)'
        },
        'e471': {
            'short_term': 'Generally well tolerated; no significant short-term effects at food-additive concentrations',
            'long_term': 'Same as mono and diglycerides — trans fat labelling loophole concern; chronic emulsifier gut microbiome alteration; safe from non-hydrogenated sources',
            'vulnerable_groups': 'People with cardiovascular disease; people avoiding trans fats; people with IBD'
        },
        'datem': {
            'short_term': 'Generally well tolerated; no significant short-term adverse effects at food-additive levels',
            'long_term': 'DATEM (Diacetyl Tartaric Acid Ester of Mono/Diglycerides, E472e) is a bread dough emulsifier; breaks down in the body to diacetyl, tartaric acid and fatty acids; diacetyl at high occupational INHALATION exposure causes bronchiolitis obliterans ("popcorn lung") — at food ingestion levels this concern is not applicable; FDA GRAS; EFSA found it safe at current food use levels; chronic high intake studies in animals show liver effects at extremely high doses not achievable through normal diet',
            'vulnerable_groups': 'Bakery workers (occupational diacetyl inhalation — not the food additive itself); people with tartrate kidney stones (precautionary); otherwise safe for general population'
        },
        'e472e': {
            'short_term': 'No significant short-term effects; well tolerated at food-additive levels',
            'long_term': 'Same as DATEM — diacetyl inhalation concern for bakery workers (occupational only); FDA GRAS and EFSA approved for food use; liver effects only at extreme doses in animals',
            'vulnerable_groups': 'Bakery workers (occupational diacetyl); people with tartrate sensitivity'
        },
        'sodium stearoyl lactylate': {
            'short_term': 'Excellent tolerability — one of the most widely studied and safest food emulsifiers; no known short-term adverse effects',
            'long_term': 'SSL (E481) is derived from stearic acid (saturated fatty acid) and lactic acid — both naturally present in food; FDA GRAS with long use history; JECFA established ADI of 0–20 mg/kg body weight; no significant carcinogenicity, teratogenicity or reproductive toxicity in studies; breaks down to stearic acid and lactic acid which are normal metabolic intermediates',
            'vulnerable_groups': 'People with milk allergy (lactic acid is not dairy-derived but check formulation); people with very strict low-fat diets; generally safe for all populations including children'
        },
        'e481': {
            'short_term': 'No known adverse effects at food-additive concentrations; excellent tolerability',
            'long_term': 'Same as sodium stearoyl lactylate — FDA GRAS, JECFA ADI established; metabolised to stearic acid and lactic acid; no significant long-term concerns',
            'vulnerable_groups': 'Safe for general population; see sodium stearoyl lactylate'
        },
        'calcium stearoyl lactylate': {
            'short_term': 'Well tolerated at food-additive levels; no significant short-term adverse effects',
            'long_term': 'E482 — same profile as SSL (E481); metabolised to calcium, stearic acid and lactic acid; FDA GRAS; JECFA approved; no significant long-term concerns at food-additive intake',
            'vulnerable_groups': 'Safe for general population; same precautions as E481'
        },
        'carboxymethyl cellulose': {
            'short_term': 'Mild GI effects (bloating, altered stool consistency) with high intake; generally well tolerated at typical food concentrations',
            'long_term': 'CMC (E466) was one of two emulsifiers in the landmark Chassaing et al. (2015, Nature) mouse study showing dietary emulsifiers disrupted the intestinal mucosal barrier, altered gut microbiome composition and promoted metabolic syndrome, obesity and colitis — at concentrations "relevant to human food use"; a subsequent FRESH Cohort human study (2022) found positive association between CMC intake and increased Crohn\'s disease risk; EFSA reviewed the evidence (2020) and found it insufficient to change ADI but noted uncertainty; ongoing human studies; the traditional safety record is long but recent microbiome evidence has raised concern',
            'vulnerable_groups': 'People with Crohn\'s disease and ulcerative colitis — strongest concern; people with IBS; people with gut dysbiosis; infants and children (developing gut microbiome); people consuming large amounts of ultra-processed foods with multiple emulsifiers'
        },
        'cmc': {
            'short_term': 'Bloating, altered stool consistency at high intake; generally tolerated at food concentrations',
            'long_term': 'Same as carboxymethyl cellulose (E466) — Chassaing 2015 gut barrier disruption study; FRESH Cohort 2022 Crohn\'s association; ongoing human studies; EFSA uncertainty noted',
            'vulnerable_groups': 'People with IBD (Crohn\'s, ulcerative colitis), IBS, gut dysbiosis'
        },
        'e466': {
            'short_term': 'Mild GI bloating and altered stool consistency at high doses',
            'long_term': 'Carboxymethyl cellulose — Chassaing 2015 mouse study (gut barrier disruption); 2022 human cohort Crohn\'s disease association; EFSA review noted uncertainty; further human studies underway',
            'vulnerable_groups': 'People with Crohn\'s disease, ulcerative colitis, IBS, gut dysbiosis'
        },
        'microcrystalline cellulose': {
            'short_term': 'No significant short-term effects; insoluble fibre — adds bulk; safe',
            'long_term': 'MCC (E460) is highly purified, partially depolymerised cellulose derived from plant pulp; chemically inert and not digested or absorbed; passes through the gut unchanged; FDA GRAS with extensive use history; no bioaccumulation; no significant long-term health concerns established in humans or animals at food-additive levels',
            'vulnerable_groups': 'People with swallowing difficulties (MCC in tablet form can cause obstruction — not relevant to food use); safe for all populations at food-additive levels'
        },
        'e460': {
            'short_term': 'No adverse effects; inert bulking agent',
            'long_term': 'Microcrystalline cellulose — chemically inert, not absorbed; FDA GRAS; no long-term concerns',
            'vulnerable_groups': 'Safe for general population'
        },
        'locust bean gum': {
            'short_term': 'Generally well tolerated; mild bloating or flatulence at very high intake as undigested fibre',
            'long_term': 'Carob bean gum (E410) is a natural galactomannan polysaccharide from carob tree seeds; prebiotic — selectively feeds beneficial Bifidobacterium species; FDA GRAS; JECFA found no ADI necessary (safe at any food-use level); lowers LDL cholesterol and improves glycaemic control; used as infant formula thickener for reflux management — safe at appropriate doses',
            'vulnerable_groups': 'People with carob allergy (rare — cross-reactivity with legumes possible); people with very severe IBS (any dietary fibre may worsen symptoms during flares); generally very safe'
        },
        'carob bean gum': {
            'short_term': 'Well tolerated; mild flatulence at high intake',
            'long_term': 'Same as locust bean gum (E410) — prebiotic galactomannan; FDA GRAS; lowers cholesterol; safe in infant formula',
            'vulnerable_groups': 'People with carob or legume allergy (rare)'
        },
        'e410': {
            'short_term': 'Mild bloating at very high intake; otherwise well tolerated',
            'long_term': 'Locust bean gum — prebiotic, cholesterol-lowering; FDA GRAS; no ADI necessary',
            'vulnerable_groups': 'People with carob allergy (rare)'
        },
        'pectin': {
            'short_term': 'Very well tolerated; mild GI effects (increased stool bulk, mild flatulence) at high intake due to fibre content',
            'long_term': 'Natural polysaccharide found in cell walls of all fruits and vegetables; excellent safety profile; FDA GRAS; no ADI necessary according to JECFA; lowers LDL cholesterol (soluble fibre binding bile acids); improves glycaemic control; prebiotic for gut microbiome; fruit-derived pectin reduces post-meal blood glucose spikes; no significant long-term concerns',
            'vulnerable_groups': 'People with very severe GI sensitivity (excess fibre); people with latex allergy (very rare cross-reactivity with fruit pectin); generally one of the safest food additives'
        },
        'e440': {
            'short_term': 'Well tolerated; mild fibre effects at high intake',
            'long_term': 'Pectin — natural fruit fibre; FDA GRAS; cholesterol and glucose control benefits; prebiotic; no long-term concerns',
            'vulnerable_groups': 'People with latex allergy (rare cross-reactivity); very safe generally'
        },
        'gellan gum': {
            'short_term': 'Generally well tolerated; bloating and flatulence at high intake; very small amounts used in food',
            'long_term': 'E418 — fermentation-derived polysaccharide from Sphingomonas elodea bacteria; FDA GRAS; JECFA approved; not digested or absorbed; passes through gut unchanged; no established carcinogenicity, teratogenicity or toxicity in long-term animal studies at relevant food-use doses',
            'vulnerable_groups': 'Safe for general population; mild fibre-related GI effects at high intake only'
        },
        'e418': {
            'short_term': 'Well tolerated; minimal GI effects at food concentrations',
            'long_term': 'Gellan gum — fermentation-derived; FDA GRAS; JECFA approved; not absorbed; no long-term concerns',
            'vulnerable_groups': 'Safe for general population'
        },
        'hydroxypropyl methylcellulose': {
            'short_term': 'Well tolerated; mild laxative effect at high oral doses; used as a pharmaceutical film coating',
            'long_term': 'HPMC (E464) is a semi-synthetic cellulose derivative; not digested or absorbed; FDA GRAS; used as a viscosity modifier, fat replacer and in capsule shells (veggie capsules); no significant long-term toxicity established; inert and excreted unchanged',
            'vulnerable_groups': 'Safe for general population; celiac patients note: HPMC is gluten-free despite wheat-like coating appearance'
        },
        'e464': {
            'short_term': 'Well tolerated at food-additive concentrations; mild laxative at high doses',
            'long_term': 'Hydroxypropyl methylcellulose — not absorbed; FDA GRAS; inert; no long-term concerns',
            'vulnerable_groups': 'Safe for general population'
        },

        # ── Glycerol / Glycerin ───────────────────────────────────────────────
        'glycerol': {
            'short_term': 'Very well tolerated; safe as food additive and cosmetic ingredient; very high oral intake (>1g/kg body weight) causes headache and nausea — not achievable through food additive levels; very mild osmotic laxative at very high doses',
            'long_term': 'E422 — a natural trihydric alcohol and metabolic intermediate in the human body; formed from triglyceride (fat) metabolism; FDA GRAS; JECFA found no ADI necessary; used as sweetener, humectant, solvent and preservative; metabolised to glucose and glycerol-3-phosphate (normal metabolic intermediates); no long-term concerns at food-additive levels',
            'vulnerable_groups': 'Diabetics at very high supplemental doses (converted to glucose); people with very rare glycerol intolerance; safe for general population at food-additive levels'
        },
        'glycerin': {
            'short_term': 'Same as glycerol — excellent tolerability in food and cosmetics; no known short-term adverse effects at use concentrations',
            'long_term': 'Same as glycerol (E422) — natural metabolic intermediate; FDA GRAS; JECFA no ADI necessary; no long-term concerns',
            'vulnerable_groups': 'Diabetics at high supplemental intake; safe for general population'
        },
        'e422': {
            'short_term': 'No adverse effects at food-additive levels; excellent tolerability',
            'long_term': 'Glycerol/glycerin — natural metabolic intermediate; FDA GRAS; no ADI necessary',
            'vulnerable_groups': 'Diabetics at high doses; safe generally'
        },

        # ── Flavourings ───────────────────────────────────────────────────────
        'vanillin': {
            'short_term': 'Well tolerated at food flavouring levels; rare contact dermatitis and skin sensitisation; migraine trigger in sensitive individuals (contains phenolic compounds); very rare allergic reactions',
            'long_term': 'Synthetic vanillin (4-hydroxy-3-methoxybenzaldehyde) is the most widely used flavour compound in the world; 99% of vanillin used in food is synthetic (petroleum or wood lignin-derived) rather than from vanilla beans; FDA GRAS; no established carcinogenicity or serious long-term toxicity at food-use levels; animal studies at very high doses show liver effects — not relevant to food additive use; some animal studies suggest vanillin may have protective antioxidant properties',
            'vulnerable_groups': 'People with vanilla or phenolic compound allergy; migraine sufferers (phenolic trigger); people with contact dermatitis to fragrances (cross-reactivity with vanilla fragrance)'
        },
        'ethyl vanillin': {
            'short_term': 'Well tolerated at food-flavouring levels; 2–4× stronger flavour than vanillin; rare allergic reactions; migraine trigger possibility',
            'long_term': 'Ethyl vanillin is entirely synthetic — not found naturally; FDA GRAS at food-use levels; some studies suggest higher acute toxicity than vanillin in animals — but at doses far exceeding any food exposure; no established long-term concern in humans at flavouring levels; EU permits its use with concentration limits in certain baby foods',
            'vulnerable_groups': 'Infants and young children (EU restricts in baby food); people with vanilla/phenolic allergy; migraine sufferers'
        },
        'vanilla': {
            'short_term': 'Genuine vanilla extract: very well tolerated; contains vanillin plus 200+ other flavour compounds; rare contact allergy to vanilla oleoresin',
            'long_term': 'Natural vanilla from Vanilla planifolia bean has excellent safety record; contains antioxidants; FDA GRAS for vanilla extract; vanillin and other phenolics provide antioxidant properties; very low toxicity profile with centuries of safe food use; no significant long-term health concerns',
            'vulnerable_groups': 'People with vanilla bean allergy (rare); people with sensitivity to phenolic compounds; people purchasing products labelled "vanilla flavour" — this is likely synthetic vanillin, not real vanilla bean extract'
        },
        'natural flavour': {
            'short_term': 'Reactions vary widely — "natural flavour" is a legally defined term covering thousands of compounds derived from natural sources; allergens (including the 14 major EU allergens) can be hidden within natural flavour declarations',
            'long_term': 'The major concern is lack of transparency: "natural flavours" and "natural flavoring" require NO disclosure of the specific compound used; a "natural flavour" derived from shellfish is not required to be declared as such in all jurisdictions; monosodium glutamate, yeast extract and other flavour-active compounds are sometimes listed as "natural flavour"; processing aids and carrier solvents (propylene glycol, glycerol, benzyl alcohol) do not need to be declared; people with specific food allergies cannot make informed decisions',
            'vulnerable_groups': 'People with any food allergy — natural flavours can hide allergens; people avoiding specific ingredients (MSG-sensitive, vegans, halal/kosher consumers); people with migraine triggered by phenolic compounds or glutamates'
        },
        'natural flavor': {
            'short_term': 'Same as natural flavour — allergens can be hidden; no way to assess without full disclosure',
            'long_term': 'Same concerns as natural flavour — lack of transparency; potential for hidden MSG, allergens, or solvents',
            'vulnerable_groups': 'People with food allergies; people avoiding MSG; vegans; halal/kosher consumers'
        },
        'artificial flavor': {
            'short_term': 'Reactions vary by specific compound; most artificial flavours are FDA GRAS at use concentrations; rare hypersensitivity reactions',
            'long_term': 'Artificial flavours are synthetic compounds; FDA requires each compound to be individually GRAS-approved before use; the term "artificial flavour" on a label covers thousands of possible compounds without disclosure; animal studies are conducted on each compound but cumulative effects of multiple synthetic flavours together are rarely studied; some artificial flavours (diacetyl in butter flavouring) have been linked to serious health problems in occupational settings',
            'vulnerable_groups': 'People with chemical sensitivities; people who react to specific artificial flavouring compounds; children (precautionary — some artificial flavours not studied in developing populations); people who prefer transparency in food labelling'
        },

        # ── Dairy and Protein Ingredients ────────────────────────────────────
        'whey': {
            'short_term': 'Well tolerated in most people; milk allergy (IgE-mediated) can cause severe reactions including anaphylaxis; lactose intolerance can cause bloating, gas, diarrhoea from residual lactose in whey concentrate (whey isolate is mostly lactose-free)',
            'long_term': 'Whey protein is a high-quality complete protein (all essential amino acids); excellent digestibility; strongly supported by clinical evidence for muscle protein synthesis; high leucine content triggers maximal muscle protein synthesis; no significant long-term health concerns in healthy adults at supplemental levels; very high protein intake (>2.2g/kg/day from all sources combined) may increase kidney workload in those with existing kidney disease',
            'vulnerable_groups': 'People with cow\'s milk allergy (IgE-mediated — AVOID; anaphylaxis risk); people with lactose intolerance (whey concentrate only — whey isolate is largely lactose-free); people with pre-existing kidney disease (monitor total protein intake)'
        },
        'casein': {
            'short_term': 'Well tolerated in most people; milk allergy causes reactions including anaphylaxis; lactose-free but still a milk protein',
            'long_term': 'Casein is the dominant milk protein (80% of total); slow-digesting due to gel formation in stomach (compared to fast-digesting whey); provides sustained amino acid release over 5–7 hours; complete protein; no significant long-term health concerns at normal dietary levels; some observational studies link high casein intake to increased IGF-1 (insulin-like growth factor) levels — clinical significance debated; casein allergy is distinct from lactose intolerance',
            'vulnerable_groups': 'People with cow\'s milk allergy (casein is the primary allergen in milk — AVOID); infants with cow\'s milk protein intolerance; people on dairy-free diets (casein is dairy-derived)'
        },
        'lactose': {
            'short_term': 'Bloating, flatulence, abdominal cramping, diarrhoea in lactose-intolerant individuals; severity depends on dose and degree of intolerance; symptoms onset 30–120 minutes after ingestion; well tolerated in lactase-sufficient individuals',
            'long_term': 'Lactose (milk sugar) is digested by lactase (small intestinal enzyme) to glucose and galactose; 65–70% of the global adult population has some degree of lactase deficiency post-weaning (primary lactase deficiency); higher prevalence in East Asian, African, Middle Eastern populations; secondary lactase deficiency can occur after gastroenteritis; no direct long-term toxicity — it is the fermentation by colonic bacteria causing the GI symptoms',
            'vulnerable_groups': 'Lactose-intolerant individuals (most of the global adult population to some degree); infants with congenital lactase deficiency (rare but severe); people with irritable bowel syndrome (FODMAP trigger); people after gastroenteritis or chemotherapy (secondary lactase deficiency)'
        },
        'skim milk': {
            'short_term': 'Well tolerated in those without milk allergy or lactose intolerance; same allergy concerns as whole milk',
            'long_term': 'Skim milk powder / non-fat dry milk provides milk proteins (casein and whey), lactose, and minerals; nutritious and well-studied; contains all milk allergens (casein, whey, lactalbumin, lactoferrin); used extensively in packaged foods, ice cream, and chocolates as a cost-effective dairy ingredient',
            'vulnerable_groups': 'People with cow\'s milk allergy (all milk proteins present); people with lactose intolerance (lactose content is significant in skim milk); vegans'
        },
        'milk solids': {
            'short_term': 'Same as skim milk — well tolerated except in milk allergy and lactose intolerance',
            'long_term': 'Concentrated dairy ingredient containing milk proteins, lactose and minerals; same nutritional and allergen profile as dairy; used extensively in ice cream, chocolates and baked goods for flavour and texture',
            'vulnerable_groups': 'People with cow\'s milk allergy; people with lactose intolerance; vegans; people on dairy-restricted diets'
        },

        # ── Cocoa Products ────────────────────────────────────────────────────
        'cocoa powder': {
            'short_term': 'Generally well tolerated; cocoa contains caffeine and theobromine — mild stimulant effects at high intake; migraine trigger for some (tyramine, phenylethylamine content); rare cocoa allergy; heartburn/GERD aggravation',
            'long_term': 'Rich source of flavanols (epicatechin, catechin) — strong antioxidant activity; multiple RCTs show cocoa flavanols improve endothelial function, lower blood pressure and improve insulin sensitivity; EFSA approved health claim for cocoa flavanols and normal blood flow; however, processed cocoa powder has highly variable flavanol content (Dutch/alkali processing destroys 60–90% of flavanols); contains oxalates (kidney stone concern at very high intake); small amount of cadmium naturally present in cocoa — WHO and EU have limits',
            'vulnerable_groups': 'Migraine sufferers (phenylethylamine, tyramine triggers); people with GERD (relaxes lower oesophageal sphincter); people prone to kidney stones (high oxalate); pregnant women (caffeine + theobromine — limit total caffeine intake); people with cocoa allergy (rare); dogs and cats (theobromine is toxic to pets)'
        },
        'cocoa butter': {
            'short_term': 'Excellent tolerability in topical cosmetic use; well tolerated orally; no significant short-term adverse effects',
            'long_term': 'Primarily stearic acid (35%) and oleic acid (35%) with palmitic acid (25%); stearic acid is unusual among saturated fats — it does not raise LDL cholesterol (converted to oleic acid in the liver); neutral effect on cardiovascular risk unlike other saturated fats; solid fat at room temperature (melts at body temperature — characteristic chocolate melt); excellent cosmetic moisturiser; no significant long-term concerns',
            'vulnerable_groups': 'People with cocoa allergy (very rare but documented); people with very high saturated fat intake already; acne-prone individuals using topical cocoa butter (comedogenic in some people)'
        },

        # ── Sugars and Sugar Syrups ───────────────────────────────────────────
        'glucose syrup': {
            'short_term': 'Rapid blood glucose spike — high glycaemic index; energy rush followed by crash; no direct short-term effects beyond elevated blood glucose in most people',
            'long_term': 'Glucose syrup is a highly refined starch hydrolysate consisting of glucose oligomers and maltose; very high GI (similar to pure glucose); regular high intake contributes to insulin resistance, obesity, Type 2 diabetes and dental caries; used extensively in confectionery, ice cream, beverages and processed foods; less concerning than high-fructose corn syrup for liver fat accumulation (glucose is distributed to all tissues unlike fructose which is predominantly hepatic)',
            'vulnerable_groups': 'Diabetics and pre-diabetics (extreme glucose spike); children (obesity and dental caries risk); people with hypoglycaemia (rebound sugar crash); people with insulin resistance'
        },
        'dextrose': {
            'short_term': 'Pure glucose — most rapid blood glucose spike of any sugar; immediate energy; can cause reactive hypoglycaemia (blood sugar crash) after initial spike',
            'long_term': 'Dextrose is pharmaceutical-grade glucose; at food-additive levels in packaged products, same metabolic concerns as glucose syrup; used for sweetening, browning (Maillard reaction) and as a fermentation substrate; excessive intake contributes to weight gain, diabetes risk and dental cavities',
            'vulnerable_groups': 'Diabetics and pre-diabetics (highest glycaemic response of all sugars); children; people with reactive hypoglycaemia'
        },

        # ── Sugar Alcohols ────────────────────────────────────────────────────
        'maltitol': {
            'short_term': 'Osmotic laxative effect at lower doses than most other sugar alcohols — bloating, flatulence and diarrhoea onset from approximately 25–30g in adults (varies individually); products must carry "excessive consumption may have laxative effects" warning in EU',
            'long_term': 'Maltitol has a glycaemic index of 35 (vs 65 for sucrose) — still significantly raises blood glucose and insulin, making it less suitable for diabetics than other sugar alcohols like erythritol or xylitol; the marketing of "sugar-free" products containing maltitol as "diabetic-friendly" is misleading; no significant long-term toxicity; dental-friendly (not fermented by Streptococcus mutans); prebiotic-like effects on gut bacteria',
            'vulnerable_groups': 'Diabetics — maltitol still raises blood glucose significantly (GI of 35); people with IBS or functional gut disorders (laxative threshold is low); children (lower body weight means lower laxative threshold per unit consumed)'
        },
        'e965': {
            'short_term': 'Osmotic diarrhoea and bloating onset at ~25g; laxative threshold lower than for sorbitol in some individuals',
            'long_term': 'Maltitol — GI of 35 (not truly "diabetic safe"); EU laxative warning required; dental-friendly; no significant long-term toxicity',
            'vulnerable_groups': 'Diabetics, people with IBS, children'
        },
        'mannitol': {
            'short_term': 'Strong osmotic laxative effect at low doses (10–20g) — bloating, flatulence, abdominal pain, diarrhoea; IV mannitol is used as an osmotic diuretic and brain oedema treatment — at those doses causes dangerous electrolyte disturbances',
            'long_term': 'Very poorly absorbed from the gut (compared to sorbitol which is partially absorbed); almost completely reaches the colon where bacteria ferment it; very dental-friendly; very low glycaemic index; FDA GRAS with "laxative effect" warning; no significant long-term toxicity from food additive use; commonly used as a pharmaceutical excipient',
            'vulnerable_groups': 'People with IBS or functional gut disorders (very strong laxative effect at low dose); children (low laxative threshold); people with kidney disease (renal excretion of absorbed mannitol); diabetics (safe sugar alcohol — very low GI)'
        },
        'e421': {
            'short_term': 'Strong osmotic laxative at low doses (10–20g); significant GI symptoms',
            'long_term': 'Mannitol — very low GI, dental-friendly; strong laxative action; FDA GRAS with warning',
            'vulnerable_groups': 'IBS sufferers, children, people with kidney disease'
        },
        'lactitol': {
            'short_term': 'Osmotic laxative effect similar to lactulose (used medically as laxative); bloating, flatulence; bowel movements increased',
            'long_term': 'E966 — disaccharide sugar alcohol derived from lactose; poorly absorbed, fermented by colonic bacteria to produce beneficial SCFAs (short-chain fatty acids); prebiotic effects; very low GI (<5); dental-friendly; clinically used as a laxative for constipation; long-term safety excellent; EU-approved with laxative effect warning',
            'vulnerable_groups': 'People with lactose intolerance (some residual lactose sensitivity possible); people with IBS who are sensitive to polyols; people taking other laxatives'
        },
        'e966': {
            'short_term': 'Osmotic laxative effects — used as a prescription laxative; bloating and flatulence',
            'long_term': 'Lactitol — prebiotic, very low GI, dental-friendly; long-term safety excellent',
            'vulnerable_groups': 'Lactose-sensitive individuals, IBS sufferers'
        },

        # ── Leavening / Raising Agents ────────────────────────────────────────
        'sodium bicarbonate': {
            'short_term': 'Well tolerated at baking use levels; as an antacid: rapid CO₂ gas release causes belching; alkaline nature can temporarily neutralise stomach acid; excessive intake (as antacid) causes milk-alkali syndrome',
            'long_term': 'E500 — common baking soda; reacts with acids to produce CO₂ (leavening action); at baking residue levels, the sodium content contributes to dietary sodium intake (concerns for hypertension); no direct long-term toxicity at food-additive amounts; excessive use as a DIY antacid causes metabolic alkalosis and milk-alkali syndrome (hypercalcaemia, renal failure)',
            'vulnerable_groups': 'People on sodium-restricted diets (hypertension, heart failure, kidney disease) — significant sodium contribution at high baking use; people self-treating with large amounts as antacid (milk-alkali syndrome risk)'
        },
        'e500': {
            'short_term': 'Well tolerated at baking levels; excess causes alkalosis',
            'long_term': 'Sodium bicarbonate — contributes dietary sodium; no direct toxicity at food-additive levels',
            'vulnerable_groups': 'People on low-sodium diets (hypertension, heart/kidney disease)'
        },
        'potassium bicarbonate': {
            'short_term': 'Well tolerated at food-additive levels; same CO₂-generating leavening mechanism as sodium bicarbonate; less sodium than equivalent sodium bicarbonate',
            'long_term': 'E501 — used in low-sodium baking products; provides potassium (beneficial for blood pressure); at food-additive levels no significant concerns; excessive supplemental potassium intake can cause hyperkalaemia in people with kidney disease',
            'vulnerable_groups': 'People with kidney disease (potassium accumulation — hyperkalaemia risk with large amounts); otherwise safe and beneficial (potassium vs sodium)'
        },
        'e501': {
            'short_term': 'Well tolerated at baking levels; same mechanism as baking soda',
            'long_term': 'Potassium bicarbonate — beneficial potassium source; low-sodium alternative to E500',
            'vulnerable_groups': 'People with kidney disease (potassium restriction needed)'
        },
        'ammonium bicarbonate': {
            'short_term': 'Strong ammoniacal odour during baking that dissipates with heat; if improperly baked, residual ammonia can cause irritation; well tolerated in properly baked products',
            'long_term': 'E503 — decomposes completely to NH₃, CO₂ and H₂O at baking temperatures; if completely decomposed, no residual compound remains in the baked product; formerly called "hartshorn" or "baker\'s ammonia"; concern only if product not properly baked and ammonia residue remains; FDA GRAS for appropriate baking use',
            'vulnerable_groups': 'People with ammonia metabolism disorders (urea cycle disorders — extremely rare); otherwise safe in properly baked products; concern if under-baked (raw dough consumption)'
        },
        'e503': {
            'short_term': 'Ammonia odour if under-baked; well tolerated in fully baked products',
            'long_term': 'Ammonium bicarbonate — completely decomposes during baking; no residue if properly baked',
            'vulnerable_groups': 'People with urea cycle disorders (rare); ensure product is properly baked'
        },
        'diphosphate': {
            'short_term': 'Well tolerated at food-additive levels; no significant short-term adverse effects',
            'long_term': 'E450 (pyrophosphates) — used as leavening agents, emulsifying salts in processed cheese, and meat binders; contributes to dietary phosphate intake; high total dietary phosphate intake associated with increased cardiovascular mortality in people with chronic kidney disease (CKD); phosphate from food additives has higher bioavailability (~80–100%) than organic phosphate from natural foods (~40–60%); WHO/IARC note that vascular calcification worsens with excess phosphate in CKD patients',
            'vulnerable_groups': 'People with chronic kidney disease (impaired phosphate excretion — hyperphosphataemia risk); people with hyperparathyroidism; people with cardiovascular disease (vascular calcification concern); people consuming large amounts of ultra-processed food containing multiple phosphate additives'
        },
        'e450': {
            'short_term': 'Well tolerated at food-additive levels; no immediate adverse effects',
            'long_term': 'Diphosphates — high bioavailability phosphate additive; cardiovascular and kidney concerns with high total intake; CKD patients most vulnerable',
            'vulnerable_groups': 'CKD patients, people with hyperparathyroidism, people with cardiovascular disease'
        },
        'triphosphate': {
            'short_term': 'Well tolerated at food-additive levels; same profile as diphosphates',
            'long_term': 'E451 (triphosphates/sodium tripolyphosphate) — same high-bioavailability phosphate concerns as E450; used in meat, seafood and processed cheese; EFSA has raised concern about cumulative phosphate intake from multiple food additives in the modern diet',
            'vulnerable_groups': 'CKD patients, people on phosphate-restricted diets, people with cardiovascular disease'
        },
        'e451': {
            'short_term': 'Well tolerated at food-additive levels',
            'long_term': 'Triphosphates — same phosphate overload concerns as E450 for CKD patients; EFSA cumulative intake concern',
            'vulnerable_groups': 'CKD patients, people with cardiovascular disease'
        },
        'polyphosphate': {
            'short_term': 'Well tolerated; no significant short-term effects',
            'long_term': 'E452 (polyphosphates) — used as stabilisers, water-retention agents in seafood and meat; contributes to dietary phosphate load; same kidney/cardiovascular concerns as other phosphate additives at high cumulative intake; EFSA reviewed and found current use safe but noted inadequate data on cumulative phosphate intake from all food additives',
            'vulnerable_groups': 'CKD patients, people with hyperparathyroidism, people with CVD'
        },
        'e452': {
            'short_term': 'Well tolerated at food-additive levels',
            'long_term': 'Polyphosphates — cumulative phosphate intake concern; EFSA note on inadequate data',
            'vulnerable_groups': 'CKD patients, people on phosphate-restricted diets'
        },

        # ── Natural Colours ───────────────────────────────────────────────────
        'beta carotene': {
            'short_term': 'Well tolerated; very high intake causes carotenodermia (harmless yellow-orange skin colouration — fully reversible); no acute toxicity',
            'long_term': 'E160a — provitamin A (converts to Vitamin A as needed); powerful antioxidant; major clinical trial (CARET, ATBC) found that high-dose beta-carotene SUPPLEMENTS (20–30mg/day — far above food colouring levels) INCREASED lung cancer risk and overall mortality in smokers and asbestos workers; this finding applies to synthetic supplements, NOT to dietary beta-carotene from food or food colouring amounts; at food-additive concentrations (typically 1–25mg/day), beta-carotene is safe and beneficial; FDA approved for food colouring',
            'vulnerable_groups': 'Current and former smokers — DO NOT take high-dose beta-carotene supplements (CARET trial evidence); asbestos workers; people with liver disease (impaired Vitamin A conversion); at FOOD levels, safe for all populations including pregnant women'
        },
        'e160a': {
            'short_term': 'Well tolerated; carotenodermia at very high intake (harmless)',
            'long_term': 'Beta-carotene — safe at food levels; high-dose supplement risk in smokers (CARET trial); antioxidant at food concentrations',
            'vulnerable_groups': 'Smokers taking supplements (increased lung cancer risk in trials); safe at food colouring levels'
        },
        'beetroot red': {
            'short_term': 'Harmless reddish-pink urine and stools (beeturia) in sensitive individuals — alarming appearance but completely safe; very rare allergic reactions',
            'long_term': 'E162 (betanin) — natural pigment from red beetroot; FDA GRAS; excellent safety profile; some studies show antioxidant and anti-inflammatory properties; betalain pigments may have cancer-protective properties in cell studies; no significant long-term health concerns; instability to heat and light means it may degrade in stored products',
            'vulnerable_groups': 'People with beeturia (benign — up to 14% of population excrete red urine after beetroot — alarming but harmless); very rare allergic reactions to beetroot; people with kidney stones (beetroot is high in oxalates — relevant only to very large beetroot consumption, not food colouring levels)'
        },
        'e162': {
            'short_term': 'Possible harmless beeturia (red urine/stools); very rare allergy',
            'long_term': 'Betanin — natural beetroot pigment; FDA GRAS; antioxidant; excellent safety',
            'vulnerable_groups': 'Safe; beeturia is harmless; very rare allergy to beetroot'
        },
        'anthocyanin': {
            'short_term': 'Excellent tolerability; natural pigments from berries, red cabbage, purple sweet potato; very rare allergy; stools may show slight colour change at high intake',
            'long_term': 'E163 — water-soluble flavonoid pigments with potent antioxidant activity; extensive research shows cardiovascular protection, anti-inflammatory, anti-cancer and neuroprotective properties in epidemiological and cell studies; FDA approved natural food colouring; no ADI necessary (JECFA); one of the most beneficial food additives with positive health associations',
            'vulnerable_groups': 'Very rare allergy to specific anthocyanin sources (berries, red cabbage etc); safe for all populations; one of the healthiest food colourants available'
        },
        'e163': {
            'short_term': 'Excellent tolerability; natural berry/vegetable pigment',
            'long_term': 'Anthocyanins — potent antioxidant; cardiovascular and anti-cancer associations; FDA approved; no ADI necessary',
            'vulnerable_groups': 'Very rare allergy to source ingredient; otherwise very safe and beneficial'
        },
        'riboflavin': {
            'short_term': 'Excellent tolerability; harmless bright yellow urine from excess riboflavin excretion (water-soluble B vitamin); very rare photosensitivity',
            'long_term': 'E101 — Vitamin B2; essential nutrient; used as both a nutrient and a yellow food colouring; water-soluble — excess excreted in urine (gives characteristic bright yellow colour); no toxicity from food or moderate supplemental amounts; extensive research confirms safety; FDA GRAS; beneficial as a nutrient source in fortified foods',
            'vulnerable_groups': 'Safe for all populations; higher doses may cause photosensitivity in rare individuals; bright yellow urine is harmless and expected'
        },
        'e101': {
            'short_term': 'Harmless bright yellow urine from riboflavin excretion; excellent tolerability',
            'long_term': 'Riboflavin/Vitamin B2 — essential nutrient colouring; FDA GRAS; water-soluble; no toxicity',
            'vulnerable_groups': 'Safe for general population; very rare photosensitivity'
        },

        # ── Acidity Regulators ────────────────────────────────────────────────
        'tartaric acid': {
            'short_term': 'Well tolerated at food-use levels; very high intake (rare) causes GI irritation, muscle weakness and kidney damage (tartrate toxicity documented only at extreme doses)',
            'long_term': 'E334 — natural acid found in grapes, tamarind and bananas; used as an acidulant and leavening acid (cream of tartar); FDA GRAS; JECFA no ADI necessary; metabolised to tartrate, CO₂ and water; no significant long-term health concerns at food-additive intake; cream of tartar (potassium bitartrate) is widely used in baking',
            'vulnerable_groups': 'People with kidney disease (tartrate is renally excreted — risk of accumulation at very high intake); people with hyperoxaluria (tartrate can complex with calcium); safe for general population at food-additive levels'
        },
        'e334': {
            'short_term': 'Well tolerated at food levels; extreme intake causes kidney issues (not relevant to food additive use)',
            'long_term': 'Tartaric acid — natural grape/tamarind acid; FDA GRAS; no ADI necessary; no long-term concerns',
            'vulnerable_groups': 'People with kidney disease at very high intake'
        },
        'sodium citrate': {
            'short_term': 'Well tolerated; used as an acidity regulator and flavour modifier; large oral doses can cause GI discomfort (alkalising effect); IV sodium citrate used as anticoagulant in blood transfusions',
            'long_term': 'E331 — sodium salt of citric acid; FDA GRAS; metabolised to bicarbonate (alkalising); contributes to dietary sodium intake; no direct long-term toxicity at food-additive levels; used in sports drinks for rapid rehydration and as a buffer in pharmaceutical preparations',
            'vulnerable_groups': 'People on sodium-restricted diets; people with kidney disease (citrate can increase urinary calcium oxalate stone formation at very high intake, though it also has stone-preventing properties at moderate intake)'
        },
        'e331': {
            'short_term': 'Well tolerated; contributes dietary sodium at food-additive levels',
            'long_term': 'Sodium citrates — FDA GRAS; metabolised to bicarbonate; no long-term concerns at food levels',
            'vulnerable_groups': 'People on low-sodium diets; people with kidney stone history'
        },
        'calcium phosphate': {
            'short_term': 'Well tolerated at food-additive levels; provides calcium and phosphorus; no significant short-term adverse effects',
            'long_term': 'E341 (mono/di/tricalcium phosphate) — used as raising agents, anti-caking agents, nutrient supplements and mineral salts; provides highly bioavailable calcium; same phosphate additive concerns apply (see E450/451/452) for people with CKD — high bioavailability phosphate can worsen hyperphosphataemia; calcium supplement benefit must be weighed against phosphate load in CKD',
            'vulnerable_groups': 'CKD patients (hyperphosphataemia risk from highly bioavailable phosphate); people with hypercalcaemia (milk-alkali syndrome risk); otherwise beneficial calcium source for general population'
        },
        'e341': {
            'short_term': 'Well tolerated; provides calcium and phosphorus',
            'long_term': 'Calcium phosphates — beneficial calcium source; high-bioavailability phosphate CKD concern',
            'vulnerable_groups': 'CKD patients (phosphate restriction); people with hypercalcaemia'
        },

        # ── Yeast Extract / HVP ───────────────────────────────────────────────
        'yeast extract': {
            'short_term': 'Well tolerated in most people; naturally contains high levels of free glutamates (approximately 5% by weight) — people sensitive to MSG may react; contains tyramine — migraine trigger; high sodium content in some formulations',
            'long_term': 'Yeast extract (Marmite, Vegemite, Maggi seasoning) provides B vitamins (especially B12 and folate), zinc, selenium; the glutamate content (technically "naturally occurring") gives it deep umami flavour; used to label products as "no added MSG" while achieving the same flavour — the free glutamate is physiologically identical to MSG; high purine content raises uric acid — concern for gout sufferers; no established long-term toxicity',
            'vulnerable_groups': 'People sensitive to MSG/glutamate; migraine sufferers (tyramine content); people with gout or hyperuricaemia (high purines); people on low-sodium diets; people with Crohn\'s disease (some intolerance reported)'
        },
        'hydrolysed': {
            'short_term': 'Hydrolysed vegetable/plant/wheat protein (HVP/HWP/HPP) is high in free glutamates — same MSG-like reactions possible; may contain residual allergens from source protein (soy, wheat, milk)',
            'long_term': 'Acid or enzyme hydrolysis of proteins creates free amino acids including glutamate; used to label products as "no added MSG" while providing equivalent flavour-enhancing effect; HVP may contain 3-MCPD (3-monochloropropane-1,2-diol — a probable carcinogen) as a by-product of acid hydrolysis at elevated temperatures; EU has strict limits on 3-MCPD in HVP; enzymatically produced HVP has much lower 3-MCPD levels',
            'vulnerable_groups': 'People with MSG sensitivity; people with allergies to source protein (soy HVP for soy allergic, wheat HVP for coeliac); people avoiding MSG-like compounds'
        },
        'gum arabic': {
            'short_term': 'Generally well tolerated; occasional GI effects (bloating, flatulence) at high intake as it is a dietary fibre; rare occupational allergy in pharmaceutical manufacturing',
            'long_term': 'E414 (Acacia) — natural exudate from Acacia senegal and Acacia seyal trees; one of the safest food additives; FDA GRAS with no ADI necessary; prebiotic fibre selectively feeding Bifidobacterium and Lactobacillus; clinical studies show it lowers total cholesterol and reduces abdominal fat at high doses; safe in pregnancy and childhood; no carcinogenicity, mutagenicity or reproductive toxicity in extensive animal studies',
            'vulnerable_groups': 'People with gum arabic occupational allergy (pharmaceutical/food industry workers); people with very sensitive gut (high-fibre effects); otherwise one of the safest food additives'
        },
        'acacia': {
            'short_term': 'Same as gum arabic — well tolerated; mild fibre-related GI effects at high intake',
            'long_term': 'Same as gum arabic (E414) — FDA GRAS; prebiotic; cholesterol-lowering; no ADI necessary',
            'vulnerable_groups': 'Occupational allergy risk; generally very safe'
        },
        'modified starch': {
            'short_term': 'Generally well tolerated; some individuals with IBS report sensitivity; provides glucose rapidly on digestion (higher GI than unmodified starch)',
            'long_term': 'Modified food starches (E1400–E1450 series) are physically, enzymatically or chemically treated starches; most are safe and FDA GRAS; however, octenyl succinic anhydride-modified starch (E1450) is restricted in infant formula in EU; acetylated distarch adipate (E1422) and hydroxypropyl distarch phosphate (E1442) are the most common; phosphate-modified starches add to total dietary phosphate (CKD concern); chemical treatments are minimal and mostly removed in processing',
            'vulnerable_groups': 'CKD patients (phosphate-modified starches); infants (EU restricts some modified starches in infant formula); people with coeliac disease (if wheat-starch derived — gluten-free modified starches are available)'
        },
        'e1422': {
            'short_term': 'Well tolerated at food-additive levels; same as other modified starches',
            'long_term': 'Acetylated distarch adipate — a chemically modified corn/tapioca starch; FDA GRAS; EU permitted; no significant long-term health concerns at food-additive levels; widely used in frozen foods for freeze-thaw stability',
            'vulnerable_groups': 'CKD patients (phosphate content); people with corn or tapioca allergy (rare)'
        },
        'e1442': {
            'short_term': 'Well tolerated; same as modified starch general profile',
            'long_term': 'Hydroxypropyl distarch phosphate — stable under heat, acid and freezing; FDA GRAS; EU permitted; phosphate content is a concern for CKD patients at high cumulative intake from multiple modified starch additives',
            'vulnerable_groups': 'CKD patients; people with corn or potato allergy (rare, source-dependent)'
        },
    }

    for key, effects in specific.items():
        if key in ingredient_lower:
            return effects

    # ── Classification-based fallbacks ────────────────────────────────────────
    if classification == 'commonly_questioned':
        if 'paraben' in ingredient_lower:
            return {
                'short_term': 'Contact dermatitis, skin sensitisation, allergic reactions with prolonged use',
                'long_term': 'Weak oestrogenic and androgenic activity; detected in human breast tissue, blood, urine and adipose tissue; potential endocrine disruption with chronic exposure; bioaccumulation concern',
                'vulnerable_groups': 'Pregnant and breastfeeding women, infants, children, people with hormone-sensitive conditions (ER+ breast cancer), people with damaged skin barrier'
            }
        if 'isothiazolinone' in ingredient_lower:
            return {
                'short_term': 'Severe allergic contact dermatitis, skin and scalp eczema, cytotoxic at high concentrations',
                'long_term': 'Permanent sensitisation; cross-reactivity between MIT and CMIT; pandemic of contact allergy in Europe in the 2010s traced to their widespread adoption in cosmetics',
                'vulnerable_groups': 'Anyone with eczema or atopic dermatitis; people previously sensitised; healthcare workers; all individuals — sensitisation risk is significant'
            }
        if any(x in ingredient_lower for x in ['nitrite', 'nitrate']):
            return {
                'short_term': 'Methaemoglobinaemia risk at high doses (especially in infants under 6 months)',
                'long_term': 'N-nitrosamine formation linked to colorectal, stomach and oesophageal cancer; IARC classifies processed meat consumption as Group 1 carcinogenic (partly attributed to nitrite/nitrate)',
                'vulnerable_groups': 'Infants under 6 months (highest methaemoglobinaemia risk), regular processed meat consumers, people with GERD'
            }
        if any(x in ingredient_lower for x in ['color', 'colour', 'dye', 'red', 'yellow', 'blue', 'green']) and any(x in ingredient_lower for x in ['artificial', 'synthetic', 'azo', 'allura', 'sunset', 'tartrazine']):
            return {
                'short_term': 'Urticaria, rhinitis, asthma attacks, hyperactivity in children; aspirin cross-sensitivity for azo dyes',
                'long_term': 'EU mandatory hyperactivity warning label; possible carcinogenicity of some derivatives in animal studies; genotoxicity concerns in some in vitro data',
                'vulnerable_groups': 'Children (hyperactivity/ADHD), asthmatics, aspirin-sensitive individuals, people with food colour hypersensitivity'
            }
        if 'formaldehyde' in ingredient_lower or 'dmdm' in ingredient_lower or 'imidazolidinyl' in ingredient_lower or 'diazolidinyl' in ingredient_lower or 'quaternium-15' in ingredient_lower:
            return {
                'short_term': 'Skin irritation, contact dermatitis, sensitisation; formaldehyde is a potent skin and mucous membrane irritant',
                'long_term': 'Formaldehyde is IARC Group 1 (carcinogenic to humans — nasopharyngeal cancer, leukaemia at high occupational exposure); at cosmetic release levels, carcinogenicity evidence is limited but sensitisation is a confirmed concern',
                'vulnerable_groups': 'People with formaldehyde or preservative allergy; eczema-prone individuals; salon workers (professional exposure to higher concentrations in keratin treatments)'
            }
        if any(x in ingredient_lower for x in ['phthalate', 'dibutyl', 'diethyl', 'dimethyl phthalate']):
            return {
                'short_term': 'Skin, eye and respiratory irritation; headache with heavy inhalation',
                'long_term': 'Anti-androgenic endocrine disruptors; DEP, DBP and DEHP linked to reproductive toxicity in animal studies; DBP and DEHP banned in cosmetics in EU; detected in human urine, blood and amniotic fluid; possible contributors to male reproductive decline (reduced sperm count, testicular dysgenesis)',
                'vulnerable_groups': 'Pregnant women and foetuses (reproductive development), infants, men of reproductive age, people with hormone-sensitive conditions'
            }
        return {
            'short_term': 'Possible allergic reactions, skin or digestive sensitivity in some individuals',
            'long_term': 'Regulatory restrictions or safety concerns documented; may have endocrine-disrupting, carcinogenic or toxic properties at relevant exposure levels',
            'vulnerable_groups': 'Pregnant women, infants, children, people with allergies or sensitivities, immunocompromised individuals'
        }

    elif classification == 'worth_knowing':
        if 'sugar' in ingredient_lower or 'syrup' in ingredient_lower or 'fructose' in ingredient_lower or 'glucose' in ingredient_lower:
            return {
                'short_term': 'Blood glucose spike and crash; dental caries with repeated oral exposure; rapid energy followed by lethargy',
                'long_term': 'Obesity, Type 2 diabetes, cardiovascular disease risk at excess intake; non-alcoholic fatty liver disease (especially fructose); dental cavities',
                'vulnerable_groups': 'Diabetics and pre-diabetics, children (dental cavities, obesity risk), people with metabolic syndrome, individuals with insulin resistance'
            }
        if 'palm oil' in ingredient_lower or 'palmolein' in ingredient_lower:
            return {
                'short_term': 'High calorie density — contributes to excess caloric intake',
                'long_term': 'High palmitic acid (saturated fat) raises LDL cholesterol; processing-induced glycidyl esters are a carcinogenicity concern (EFSA); environmental impact from deforestation',
                'vulnerable_groups': 'People with dyslipidaemia (high cholesterol), cardiovascular disease, those with high intake of ultra-processed foods containing palm oil'
            }
        if 'sodium lauryl' in ingredient_lower or 'sodium laureth' in ingredient_lower or ('sulfate' in ingredient_lower and 'lauryl' in ingredient_lower):
            return {
                'short_term': 'Skin barrier disruption, dryness, redness, scalp irritation; aggravates mouth ulcers in toothpaste',
                'long_term': 'Chronic barrier disruption leading to transepidermal water loss and increased skin permeability; SLES has 1,4-dioxane contamination risk from ethoxylation',
                'vulnerable_groups': 'People with eczema, psoriasis, rosacea, dry skin; individuals with recurrent aphthous ulcers (avoid SLS in toothpaste)'
            }
        if 'caffeine' in ingredient_lower:
            return {
                'short_term': 'Increased heart rate, jitteriness, anxiety, insomnia, headache on withdrawal, GERD aggravation',
                'long_term': 'Physical dependence (caffeine use disorder); no established serious long-term toxicity at moderate doses; potential cardiovascular benefits in moderate coffee consumption',
                'vulnerable_groups': 'Pregnant women (limit to <200 mg/day), infants and children (no safe limit), people with anxiety, arrhythmia, hypertension, GERD'
            }
        if 'carrageenan' in ingredient_lower:
            return {
                'short_term': 'Bloating, diarrhoea, increased gut permeability in sensitive individuals',
                'long_term': 'Degraded carrageenan (poligeenan) is carcinogenic and proinflammatory; some studies suggest partial degradation in the stomach; animal studies show worsening of colitis',
                'vulnerable_groups': 'People with IBS, Crohn\'s disease, ulcerative colitis, infants (removed from EU infant formula 2018)'
            }
        if 'mica' in ingredient_lower:
            return {
                'short_term': 'Topical use: safe and non-irritating; inhalation of loose powder: respiratory irritation',
                'long_term': 'Occupational inhalation causes mica pneumoconiosis; spray products with mica pose inhalation risk; child labour in supply chain is an ethical issue',
                'vulnerable_groups': 'People with respiratory conditions (avoid spray cosmetics with mica); workers in mica processing'
            }
        if any(x in ingredient_lower for x in ['zinc', 'copper', 'magnesium', 'iron', 'calcium']):
            return {
                'short_term': 'Generally well tolerated at food and cosmetic concentrations; high supplemental doses of zinc (>40 mg/day) can cause nausea and copper deficiency',
                'long_term': 'At normal dietary and cosmetic concentrations: safe and beneficial; supplemental zinc at excessive doses reduces HDL cholesterol and impairs immune function over time',
                'vulnerable_groups': 'People taking zinc supplements above tolerable upper intake level (40 mg/day); people with Wilson\'s disease (copper accumulation); kidney disease patients (impaired mineral excretion)'
            }
        if 'lecithin' in ingredient_lower:
            return {
                'short_term': 'Well tolerated; rare allergic reaction in people with severe soy allergy',
                'long_term': 'Gut bacteria convert phosphatidylcholine to TMAO — high TMAO linked to cardiovascular disease risk; typically safe at food additive levels; provides beneficial phospholipids',
                'vulnerable_groups': 'People with severe soy or egg allergy; people with trimethylaminuria (fish odour syndrome); people with very high dietary choline intake already'
            }
        return {
            'short_term': 'Generally well tolerated at typical food or cosmetic concentrations; individual sensitivity may cause mild reactions',
            'long_term': 'Safe in normal quantities; consider cumulative daily exposure from multiple products; some specific concerns at high or prolonged intake may apply',
            'vulnerable_groups': 'Sensitive individuals, children, pregnant or breastfeeding women, people with specific food intolerances or allergies'
        }

    else:  # generally_recognised
        if 'hyaluronic' in ingredient_lower or 'hyaluronate' in ingredient_lower:
            return {
                'short_term': 'Exceptional tolerability; no known short-term adverse effects for topical use',
                'long_term': 'No long-term safety concerns; naturally occurring in the human body; injectable HA fillers have rare serious complications',
                'vulnerable_groups': 'Injectable HA: pregnant women and immunocompromised individuals (precautionary); topical: safe for all skin types'
            }
        if 'tocopherol' in ingredient_lower or 'vitamin e' in ingredient_lower:
            return {
                'short_term': 'Topical: rarely causes contact sensitisation; food-level intake: no adverse effects',
                'long_term': 'Food-additive and cosmetic levels are safe; high-dose supplementation (>400 IU/day) may increase haemorrhagic stroke risk — not relevant to food additive use',
                'vulnerable_groups': 'People on blood thinners (Vitamin E potentiates anticoagulants at supplemental doses)'
            }
        if 'ascorbic' in ingredient_lower or 'vitamin c' in ingredient_lower:
            return {
                'short_term': 'Gastric discomfort and diarrhoea at high supplemental doses; food-level intake is well tolerated',
                'long_term': 'One of the safest vitamins — water-soluble, excess excreted; very high doses (>2 g/day) increase kidney stone risk in predisposed individuals',
                'vulnerable_groups': 'People with haemochromatosis (iron absorption is enhanced); people prone to calcium oxalate kidney stones; infants (over-fortification risk)'
            }
        return {
            'short_term': 'No known adverse effects at typical use concentrations',
            'long_term': 'Approved by major regulatory bodies (FDA, EU, WHO, FSSAI) as safe for intended use; long-term safety well established',
            'vulnerable_groups': 'Safe for the general population; individuals with specific ingredient allergies should check labels as always'
        }
