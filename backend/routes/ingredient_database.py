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
    'disodium ribonucleotides': 'A commercially prepared blend of disodium guanylate (E627) and disodium inosinate (E631) in a 1:1 ratio (E635/INS 635). Used in snack foods, instant noodles and savoury seasonings to intensify umami flavour synergistically with MSG.',
    'e635': 'E635/INS 635 is disodium 5-ribonucleotides, a combined flavour enhancer (E627 + E631) used in crisps, instant noodles and processed savoury foods. Approved by FSSAI, EU and CODEX. Avoid if MSG-sensitive.',
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
    "disodium 5'-ribonucleotides": 'Disodium 5\'-ribonucleotides (E635/INS 635) is a combined nucleotide flavour enhancer — a 1:1 blend of disodium guanylate (E627) and disodium inosinate (E631). Used in instant noodles, crisps, savoury seasonings and processed foods to synergistically intensify umami flavour with MSG. Approved by FSSAI, EU and CODEX. Avoid if MSG-sensitive.',
    "disodium 5' ribonucleotides": 'Disodium 5\'-ribonucleotides (E635/INS 635), a combined nucleotide flavour enhancer used in savoury processed foods to boost umami flavour. Approved by FSSAI, EU and CODEX.',

    # ── Hydrolysed Proteins ───────────────────────────────────────────────────
    'hydrolysed groundnut protein': 'Hydrolysed groundnut (peanut) protein is produced by breaking down peanut protein into amino acids and short peptides using acid, base or enzymatic hydrolysis. Used as a natural umami flavour enhancer in instant noodles, seasonings and soups. Contains free glutamates which contribute to savoury taste. Peanut allergen — must be declared on packaging.',
    'hydrolysed vegetable protein': 'Hydrolysed vegetable protein (HVP) is produced by breaking down plant proteins (soy, wheat, corn, groundnut) into amino acids and peptides. Rich in free glutamates, used as a natural umami flavour enhancer in soups, sauces, seasonings and instant noodles. May contain MSG-like amounts of glutamate.',
    'hydrolysed soy protein': 'Hydrolysed soy protein (HSP) is produced by enzymatic or acid hydrolysis of soy protein. Used as a flavour enhancer in savoury foods. Soy allergen — must be declared on packaging.',

    # ── Caramel Colour variants ────────────────────────────────────────────────
    'caramel iv': 'Caramel Colour Class IV (E150d/INS 150d), produced by heating carbohydrates with ammonium sulfite compounds. The most widely used caramel colour globally — in cola drinks, soy sauce and some noodle seasonings. Contains 4-methylimidazole (4-MEI), listed as a possible carcinogen (IARC Group 2B) in animal studies; California Prop 65 listed.',
    'caramel colour iv': 'Caramel Colour Class IV (E150d), the sulphite-ammonia process caramel colour. Contains 4-MEI, a possible carcinogen in animal studies; listed under California Prop 65. Widely used in cola drinks and savoury seasonings.',
    'e150d': 'E150d/INS 150d is Class IV caramel colour (sulphite-ammonia process). Contains 4-MEI, a possible carcinogen in animal studies. California Prop 65 listed. EU restricts use in certain beverage categories.',
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
    """Convert 'INS 200', 'INS200', 'ins-200' → 'e200' so it matches E-number keys."""
    import re
    s = name.strip().lower()
    m = re.match(r'^ins[\s\-]*(\d+)', s)
    if m:
        return 'e' + m.group(1)
    return s


def classify_ingredient(ingredient_name, category=None):
    """Classify ingredients based on regulatory and health concerns - SINGLE SOURCE OF TRUTH"""
    # Normalize INS numbers first: "INS 200" → "e200"
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
        'disodium ribonucleotides': ('Flavour enhancer E635/INS 635', 'Combined flavour enhancer (E627 + E631); FSSAI, EU and CODEX approved; MSG-like reactions possible in sensitive individuals'),
        'e635': ('Disodium 5-ribonucleotides (E635)', 'FSSAI, EU and CODEX approved; combined nucleotide flavour enhancer; MSG-sensitive individuals may react'),

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
