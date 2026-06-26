"""
Script to add comprehensive INS/E-number entries to ingredient_database.py
and update _normalize_ins to handle bare numbers, sub-types (i/ii/iii), E-prefix.
Run once from the backend directory.
"""

import re

DB_FILE = "routes/ingredient_database.py"

# ─── NEW INGREDIENT_DESCRIPTIONS ENTRIES ─────────────────────────────────────
NEW_DESCRIPTIONS = """
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
    'e503i': 'E503(i) / INS 503(i) — Ammonium Carbonate (baker\'s ammonia). Traditional leavening agent for crisp baked goods. Fully decomposes during baking; no ammonia residue in finished product.',
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
    'e635': 'E635 / INS 635 — Disodium 5\\'\\'-Ribonucleotides. A blend of disodium inosinate (E631) and disodium guanylate (E627) in an optimised ratio for maximum umami enhancement. Used in chips, instant noodles and savoury snacks. Safe at permitted levels. Not suitable for gout sufferers (high purine content).',

    # --- Modified Starches (additional E-numbers) ---
    'e1410': 'E1410 / INS 1410 — Monostarch Phosphate. A modified starch with a small degree of phosphate cross-linking. Used as a thickener with improved acid and heat stability in sauces, soups and ready meals. Safe.',
    'e1420': 'E1420 / INS 1420 — Acetylated Starch. Starch modified by reaction with acetic anhydride to reduce retrogradation (staling). Used in sauces, dressings and dairy products. Safe.',
    'e1422': 'E1422 / INS 1422 — Acetylated Distarch Adipate. A more extensively modified starch with excellent freeze-thaw stability. Used in frozen sauces, soups and ready meals. Safe.',
    'e1440': 'E1440 / INS 1440 — Hydroxypropyl Starch. Starch modified with propylene oxide for improved freeze-thaw stability. Used in frozen foods and dairy products. Safe.',
    'e1442': 'E1442 / INS 1442 — Hydroxypropyl Distarch Phosphate. Combines cross-linking (phosphate) and substitution (hydroxypropyl) for maximum stability under heat, acid and freezing. Used in sauces, soups and canned foods. Safe.',
    'e1201': 'E1201 / INS 1201 — Polyvinylpyrrolidone (PVP / Povidone). A synthetic polymer used as a clarifying agent in beer and wine, and as a binder in pharmaceutical tablets. Safe at food-use levels.',
"""

# ─── NEW classify_ingredient ENTRIES ─────────────────────────────────────────

# These go in commonly_questioned_patterns
NEW_COMMONLY_QUESTIONED = """
        # E-number aliases for existing commonly_questioned ingredients
        'e142': ('Synthetic green dye E142 (Green S)', 'Banned in USA, Canada, Japan, Australia — hyperactivity concerns and lack of comprehensive safety data'),
        'e150c': ('Ammonia Caramel (E150c / Caramel III)', '4-MEI by-product is IARC Group 2B possible carcinogen; California Prop 65 cancer warning required; used in beer and soy sauce'),
        'e150d': ('Sulfite Ammonia Caramel (E150d / Caramel IV)', '4-MEI by-product is IARC Group 2B possible carcinogen; used in colas — Coca-Cola reformulated in some markets; California Prop 65 warning required'),
        'e151': ('Brilliant Black BN (E151)', 'Banned in USA, Canada, Japan, Australia; hyperactivity warning required in EU; azo dye with cancer and hyperactivity concerns'),
        'e218': ('Methylparaben as E218', 'Same as methylparaben — estrogen mimic, accumulates in breast tissue, endocrine disruptor; EU restricts concentration'),
        'e219': ('Sodium Methylparaben (E219)', 'Sodium salt of methylparaben; same hormone disruption concerns; EU restricts concentration'),
        'e471': ('Mono- and Diglycerides of Fatty Acids (E471)', 'May contain residual trans-fatty acids; glycidol fatty acid esters (probable carcinogen IARC Group 2A) found as contaminant; EFSA reviewed and set limits; widely used in bread and margarine'),
"""

# These go in worth_knowing_patterns
NEW_WORTH_KNOWING = """
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
"""

# These go in generally_recognised_patterns
NEW_GENERALLY_RECOGNISED = """
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
"""

NEW_NORMALIZE_INS = '''def _normalize_ins(name: str) -> str:
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
        r'^(?:ins[\s\-]?|e[\s]?)(\d+)\s*[\(\s\-]*(i{1,3}v?|iv|v)\s*\)?\s*$',
        s, re.IGNORECASE
    )
    if m:
        return 'e' + m.group(1) + m.group(2).lower()
    # Just a number (bare, or with INS/E prefix, no sub-type)
    m2 = re.match(r'^(?:ins[\s\-]?|e[\s]?)?(\d+)\b', s, re.IGNORECASE)
    if m2:
        return 'e' + m2.group(1)
    # Old behaviour: 'INS 200' → 'e200'
    m3 = re.match(r'^ins[\s\-]*(\d+)', s, re.IGNORECASE)
    if m3:
        return 'e' + m3.group(1)
    return s.lower()
'''

NEW_FALLBACK_LOGIC = '''    # Sub-type fallback: if 'e500ii' not found in any pattern, retry with parent 'e500'
    if re.match(r'^e\\d+(i{1,3}v?|iv|v)$', ingredient_lower):
        parent = re.sub(r'(i{1,3}v?|iv|v)$', '', ingredient_lower)
        if parent != ingredient_lower:
            return classify_ingredient(parent, category)
'''

# ─── APPLY CHANGES ────────────────────────────────────────────────────────────
with open(DB_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add new INGREDIENT_DESCRIPTIONS entries before the closing } of the dict
DESCRIPTIONS_CLOSE = "    'e1412': 'E1412/INS 1412 is Distarch Phosphate, a cross-linked modified starch thickener with high stability. Used in soups and canned foods.',\n}"
if DESCRIPTIONS_CLOSE not in content:
    print("ERROR: Could not find INGREDIENT_DESCRIPTIONS closing marker")
else:
    content = content.replace(
        DESCRIPTIONS_CLOSE,
        DESCRIPTIONS_CLOSE.rstrip('}') + '\n' + NEW_DESCRIPTIONS + '\n}'
    )
    print("✓ Added INGREDIENT_DESCRIPTIONS entries")

# 2. Replace _normalize_ins function
OLD_NORMALIZE = """def _normalize_ins(name: str) -> str:
    \"\"\"Convert 'INS 200', 'INS200', 'ins-200' → 'e200' so it matches E-number keys.\"\"\"
    import re
    s = name.strip().lower()
    m = re.match(r'^ins[\\s\\-]*(\\d+)', s)
    if m:
        return 'e' + m.group(1)
    return s"""
if OLD_NORMALIZE not in content:
    print("ERROR: Could not find _normalize_ins function")
else:
    content = content.replace(OLD_NORMALIZE, NEW_NORMALIZE_INS)
    print("✓ Updated _normalize_ins")

# 3. Add sub-type fallback logic in classify_ingredient (after the COSMETIC_SAFE_OVERRIDES block)
FALLBACK_ANCHOR = "    # Check commonly questioned first (highest priority — serious concerns)"
if FALLBACK_ANCHOR not in content:
    print("ERROR: Could not find fallback anchor")
else:
    content = content.replace(
        FALLBACK_ANCHOR,
        NEW_FALLBACK_LOGIC + '\n    ' + FALLBACK_ANCHOR
    )
    print("✓ Added sub-type fallback logic")

# 4. Add new commonly_questioned entries before the closing of commonly_questioned_patterns
CQ_CLOSE = "        # Potassium nitrite — curing salt, forms nitrosamines\n        'potassium nitrite':"
if CQ_CLOSE not in content:
    print("ERROR: Could not find commonly_questioned closing anchor")
else:
    content = content.replace(
        CQ_CLOSE,
        NEW_COMMONLY_QUESTIONED + '\n        # Potassium nitrite — curing salt, forms nitrosamines\n        \'potassium nitrite\':'
    )
    print("✓ Added commonly_questioned entries")

# 5. Add new worth_knowing entries after the polysorbate / emulsifier section
WK_CLOSE = "        'e955': ('Sucralose (E955)', 'Alters gut microbiome; may impair insulin response; glucose intolerance in some studies'),\n        # e954 / saccharin → moved to commonly_questioned"
if WK_CLOSE not in content:
    print("ERROR: Could not find worth_knowing closing anchor")
else:
    content = content.replace(
        WK_CLOSE,
        WK_CLOSE + '\n' + NEW_WORTH_KNOWING
    )
    print("✓ Added worth_knowing entries")

# 6. Add generally_recognised entries before the IFRA fragrance override
GR_CLOSE = "    # IFRA certified / allergen-free fragrance → worth_knowing"
if GR_CLOSE not in content:
    print("ERROR: Could not find generally_recognised closing anchor")
else:
    content = content.replace(
        GR_CLOSE,
        "    # Additional generally recognised E-number entries\n    generally_recognised_patterns.update({\n" + NEW_GENERALLY_RECOGNISED + "\n    })\n\n    " + GR_CLOSE.lstrip()
    )
    print("✓ Added generally_recognised entries")

# Write the modified file
with open(DB_FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✓ ingredient_database.py updated successfully")
print("Run the backend to verify: uvicorn main:app --reload")
