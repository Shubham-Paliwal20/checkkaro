"""Generate CheckKaro Ingredient Database PDF — 500 entries, authentic data"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.chdir(os.path.join(os.path.dirname(__file__), 'backend'))

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT

OUTPUT = os.path.join(os.path.dirname(__file__), 'CheckKaro_Ingredient_Database.pdf')

# Format: (Ingredient Name, Type / Function, Key Health Concern, [Countries Banned/Restricted])
# All data sourced from: FSSAI, EFSA, FDA, WHO, IARC, EU Cosmetics Regulation 1223/2009,
# EU Food Additives Regulation 1333/2008, Codex Alimentarius

INGREDIENTS = {

# ─── COMMONLY QUESTIONED ────────────────────────────────────────────────────
# Ingredients with significant regulatory bans, restrictions, or well-documented health risks
'commonly_questioned': [

    # ── Preservatives & Antimicrobials ──
    ('Triclosan', 'Antimicrobial preservative', 'Hormone (thyroid/estrogen) disruption; promotes antibiotic resistance; bioaccumulates', ['EU (cosmetics ban since 2017)', 'USA (FDA banned in hand soaps 2016)', 'Canada (restricted)']),
    ('Sodium Benzoate (E211)', 'Preservative', 'Reacts with vitamin C to form benzene (IARC Group 1 carcinogen); linked to ADHD in children', ['EU (mandatory warning if combined with vitamin C)', 'California Prop 65 (carcinogen list)']),
    ('Sodium Metabisulphite (E223)', 'Sulphite preservative', 'Triggers severe asthma attacks; destroys vitamin B1; anaphylaxis in sensitive people', ['EU (must declare on label)', 'Australia (mandatory declaration above 10ppm)']),
    ('Sulfur Dioxide (E220)', 'Sulphite preservative', 'Destroys thiamine (B1); triggers asthma attacks; severe allergic reactions', ['EU (must declare)', 'Australia (declaration required)']),
    ('Potassium Metabisulphite (E224)', 'Sulphite preservative', 'Asthma trigger; allergic reactions; destroys vitamin B1', ['EU (must declare)', 'Australia (declaration required)']),
    ('Sodium Nitrite (E250)', 'Curing agent in meat', 'Forms carcinogenic nitrosamines at high heat (cooking); linked to colorectal cancer (IARC Group 1)', ['EU (strict concentration limits)', 'UK (restricted since 2022)', 'Nordic countries (restricted)']),
    ('Sodium Nitrate (E251)', 'Curing / preservative in meat', 'Converts to nitrite in the body; associated with colorectal cancer (IARC Group 1)', ['EU (restricted concentration)', 'Nordic countries (restricted)']),
    ('Potassium Nitrite (E249)', 'Curing agent in meat', 'Converts to nitrosamines; carcinogenic at high heat', ['EU (strict concentration limits)']),
    ('Potassium Nitrate (E252)', 'Curing / preservative in meat', 'Converts to nitrite; colorectal cancer risk (IARC Group 1)', ['EU (restricted concentration)']),
    ('Methylparaben (E218)', 'Paraben preservative', 'Weak estrogen mimic; accumulates in breast tissue; disrupts endocrine system', ["Denmark (banned in children's products)", 'EU (concentration restricted)']),
    ('Propylparaben (E216)', 'Paraben preservative', 'Endocrine disruptor; reduces sperm count; reproductive toxicity in animals', ["Denmark (banned children's products)", 'EU (banned in products for children under 3)']),
    ('Butylparaben (E214)', 'Paraben preservative', 'Strongest endocrine disruptor among parabens; bioaccumulates; reproductive harm', ['Denmark', 'EU (banned in products for children under 3)', 'Japan (restricted)']),
    ('Isobutylparaben', 'Paraben preservative', 'Endocrine disruption; hormone mimicry; reproductive toxicity', ['EU (banned in cosmetics since 2015)']),
    ('Isopropylparaben', 'Paraben preservative', 'Endocrine disruption; hormone interference', ['EU (banned in cosmetics since 2015)']),
    ('Phenylparaben', 'Paraben preservative', 'Hormone disruption; insufficient safety data', ['EU (banned in cosmetics)']),
    ('Benzylparaben', 'Paraben preservative', 'Hormone disruption; skin sensitization', ['EU (banned in cosmetics)']),
    ('Methylisothiazolinone (MIT)', 'Preservative', 'Powerful skin allergen; severe contact dermatitis; neurotoxic in vitro', ['EU (banned in leave-on cosmetics)', 'Canada (restricted)']),
    ('Methylchloroisothiazolinone (CMIT)', 'Preservative', 'Severe contact dermatitis; neurotoxic; respiratory sensitizer', ['EU (restricted rinse-off, banned leave-on)', 'Japan (restricted)']),
    ('Formaldehyde (E240)', 'Preservative / crosslinker', 'IARC Group 1 carcinogen; sensitizer; causes allergic contact dermatitis', ['EU (banned in cosmetics above 0.001% in leave-on)', 'Japan (banned in some uses)', 'Sweden']),
    ('DMDM Hydantoin', 'Formaldehyde-releasing preservative', 'Releases formaldehyde (IARC Group 1 carcinogen); strong skin sensitizer', ['EU (restricted - must declare formaldehyde release)', 'Japan (restricted)']),
    ('Quaternium-15', 'Formaldehyde-releasing preservative', 'Releases formaldehyde; most common cause of cosmetic contact dermatitis', ['EU (restricted)', 'Japan (restricted)']),
    ('Imidazolidinyl Urea', 'Formaldehyde-releasing preservative', 'Releases formaldehyde; contact allergen; skin sensitizer', ['EU (must declare if formaldehyde released)', 'Japan']),
    ('Diazolidinyl Urea', 'Formaldehyde-releasing preservative', 'Releases formaldehyde; contact dermatitis; sensitizer', ['EU (must declare formaldehyde release)']),

    # ── Artificial Synthetic Colors ──
    ('Tartrazine (E102 / Yellow 5)', 'Synthetic azo dye', 'Hyperactivity and ADHD in children (McCann study); asthma attacks; cross-reacts with aspirin', ['Austria', 'Norway', 'EU (mandatory warning on label)']),
    ('Sunset Yellow FCF (E110 / Yellow 6)', 'Synthetic azo dye', 'Hyperactivity in children; hives; asthma; possible carcinogenicity at high doses', ['Norway', 'Finland', 'EU (mandatory warning on label)']),
    ('Allura Red AC (E129 / Red 40)', 'Synthetic azo dye', 'Hyperactivity in children; immune system tumors in mice; allergic reactions', ['Denmark', 'Belgium', 'France', 'Germany', 'Switzerland', 'Sweden', 'Austria', 'Norway', 'EU (warning label)']),
    ('Ponceau 4R (E124)', 'Synthetic azo dye', 'Hyperactivity; thyroid problems in animal studies; asthma attacks', ['USA', 'Norway', 'Finland', 'EU (warning label)']),
    ('Carmoisine (E122 / Red 3)', 'Synthetic azo dye', 'Hyperactivity; asthma attacks; allergic urticaria (hives)', ['USA', 'Canada', 'Japan', 'Austria', 'Norway', 'Sweden']),
    ('Quinoline Yellow (E104)', 'Synthetic coal-tar dye', 'Hyperactivity in children; contact dermatitis; eczema', ['USA', 'Canada', 'Japan', 'Australia', 'Norway']),
    ('Brown HT (E155)', 'Synthetic azo dye', 'Hyperactivity; asthma; skin rashes', ['USA', 'Canada', 'Australia', 'Belgium', 'France', 'Switzerland']),
    ('Brilliant Blue FCF (E133 / Blue 1)', 'Synthetic coal-tar dye', 'Crosses blood-brain barrier; chromosomal damage; neurotoxicity in high doses', ['Belgium', 'France', 'Germany', 'Greece', 'Italy', 'Spain', 'Switzerland']),
    ('Indigo Carmine (E132 / Blue 2)', 'Synthetic indigoid dye', 'Brain tumors in animal studies; skin rashes; nausea', ['Norway', 'UK (restricted)']),
    ('Erythrosine (E127 / Red 3)', 'Synthetic xanthene dye', 'Thyroid tumors in male rats (high dose); thyroid hormone disruption', ['Norway', 'USA (banned in cosmetics 1990)', 'EU (restricted use)']),
    ('Green S (E142)', 'Synthetic triarylmethane dye', 'Hyperactivity; limited safety data; asthma trigger', ['USA', 'Canada', 'Japan', 'Norway']),
    ('Fast Green FCF (E143)', 'Synthetic triphenylmethane dye', 'Bladder tumors in animal studies; genotoxicity concerns', ['EU', 'Austria', 'Norway', 'Sweden', 'UK', 'Belgium', 'France', 'Germany', 'Switzerland']),
    ('Amaranth (E123)', 'Synthetic azo dye', 'Suspected carcinogen in animal studies; birth defects in animal studies', ['USA (banned since 1976)', 'Russia', 'Austria', 'Norway']),
    ('Azorubine / Carmoisine (E122)', 'Synthetic azo dye', 'Hyperactivity; asthma; hypersensitivity reactions', ['USA', 'Canada', 'Japan', 'Norway', 'Sweden']),
    ('Red 2G (E128)', 'Synthetic azo dye', 'Converted to aniline (carcinogen) in the body', ['EU (suspended 2007)', 'USA', 'Australia', 'Canada']),

    # ── Flavor Enhancers ──
    ('Monosodium Glutamate / MSG (E621)', 'Umami flavor enhancer', 'Chinese Restaurant Syndrome; headaches, flushing, sweating; neurotoxicity at high repeated doses', []),
    ('Disodium Guanylate (E627)', 'Flavor synergist with MSG', 'Headaches, numbness, flushing; unsafe for gout patients; MSG-like effects', ['Restricted for use in infant foods globally']),
    ('Disodium Inosinate (E631)', 'Flavor synergist with MSG', 'Sweating, chest pain, nausea in sensitive individuals; gout risk (purine compound)', ['Restricted for use in infant foods globally']),
    ('Disodium Succinate (E626)', 'Flavor enhancer', 'MSG-like reactions in sensitive individuals; headaches', []),
    ('Calcium Glutamate (E623)', 'Flavor enhancer', 'Same concerns as MSG; headaches; nausea in sensitive people', []),

    # ── Synthetic Antioxidants ──
    ('TBHQ — Tert-Butylhydroquinone (E319)', 'Synthetic antioxidant', 'Stomach tumors in animal studies at high doses; DNA damage in vitro; liver tumors in rats', ['Japan (banned)', 'EU (restricted max 100mg/kg in fat)', 'Australia (concentration limits)']),
    ('BHA — Butylated Hydroxyanisole (E320)', 'Synthetic antioxidant', 'IARC Group 2B (possible human carcinogen); mimics estrogen; disrupts thyroid', ['Japan (banned from fats/oils)', 'EU (restricted)', 'California Prop 65 (carcinogen list)']),
    ('BHT — Butylated Hydroxytoluene (E321)', 'Synthetic antioxidant', 'Liver/kidney tumors in animal studies; mimics estrogen; suspected carcinogen', ['Japan (restricted)', 'EU (restricted usage levels)']),
    ('Propyl Gallate (E310)', 'Synthetic antioxidant', 'Allergic reactions; asthma; may have estrogenic activity; thyroid disruption', ['Australia (restricted)', 'EU (concentration limits)']),
    ('Octyl Gallate (E311)', 'Synthetic antioxidant', 'Gastrointestinal irritation; allergic reactions; limited safety data', ['Australia (banned as food additive)', 'UK']),
    ('Dodecyl Gallate (E312)', 'Synthetic antioxidant', 'Contact dermatitis; allergic reactions; insufficient safety data', ['Australia (banned as food additive)']),

    # ── Flour Treatment / Bleaching Agents ──
    ('Potassium Bromate (E924)', 'Flour improver / oxidizer', 'IARC Group 2B carcinogen; kidney and thyroid tumors; genotoxic', ['European Union', 'United Kingdom', 'Canada', 'Brazil', 'China', 'Sri Lanka', 'Nigeria', 'Peru', 'Australia', 'India (partially banned)']),
    ('Azodicarbonamide (E927a)', 'Flour improver / dough conditioner', 'Breaks down to semicarbazide (carcinogen) during baking; respiratory sensitizer', ['European Union', 'United Kingdom', 'Australia', 'Singapore', 'Most of Asia']),
    ('Benzoyl Peroxide (E928)', 'Flour bleaching agent', 'Destroys vitamins in flour (B1, B2, folic acid); respiratory irritant', ['EU (banned as flour treatment)', 'Australia (restricted)']),
    ('Chlorine (E925)', 'Flour bleaching agent', 'Reacts with organic matter to form chlorinated compounds; destroys vitamins', ['EU (banned as flour treatment)', 'UK']),
    ('Chlorine Dioxide (E926)', 'Flour bleaching agent', 'Destroys vitamins; forms toxic chlorinated by-products', ['EU (banned as flour treatment)']),

    # ── Other Food Additives with Significant Concerns ──
    ('Brominated Vegetable Oil (BVO)', 'Emulsifier in citrus beverages', 'Contains bromine; accumulates in fatty tissue and brain; neurological effects', ['European Union', 'Japan', 'India', 'UK (banned 2023)']),
    ('Cyclamate (E952)', 'Artificial sweetener', 'Bladder cancer in animal studies; converted to cyclohexylamine (toxic) by gut bacteria', ['USA (banned since 1969)', 'Japan (banned)']),
    ('Phosphoric Acid (E338)', 'Acidulant in soft drinks', 'Erodes tooth enamel; reduces bone mineral density; kidney stone formation; calcium depletion', ['EU (labelling required)', 'Some countries restrict in children\'s drinks']),
    ('Caramel Colour E150c (Ammonia Process)', 'Brown color additive', 'Contains carcinogenic 4-methylimidazole (4-MEI); IARC Group 2B (animal carcinogen)', ['California Prop 65 (warning required in beverages)', 'EU (usage limits under review)']),
    ('Caramel Colour E150d (Ammonia-Sulphite Process)', 'Brown color additive', 'Highest levels of 4-MEI (carcinogen); also contains 2-MEI; linked to cancer in animal studies', ['California Prop 65 (above 29mcg/day requires cancer warning)', 'EU (under review)']),
    ('Aspartame (E951)', 'Artificial sweetener', 'IARC classified as "possibly carcinogenic" (Group 2B) in 2023; headaches; seizures in PKU patients', ['EU (mandatory PKU warning)', 'Must declare on all labels globally']),
    ('Saccharin (E954)', 'Artificial sweetener', 'Bladder cancer in male rats at very high doses; FDA requires warning label history', ['Canada (restricted)', 'EU (must declare on label)']),
    ('Cyclamate / Sodium Cyclamate (E952)', 'Artificial sweetener', 'Bladder tumors in animal studies; converted to cyclohexylamine by gut bacteria', ['USA (banned 1969)', 'Japan', 'UK (banned)']),

    # ── Harmful Cosmetic Ingredients ──
    ('Hydroquinone', 'Skin-lightening agent', 'Ochronosis (blue-black skin discolouration with long use); cytotoxic; possible carcinogen', ['EU (banned in cosmetics)', 'Japan (restricted)', 'Australia (prescription only)', 'Several African countries (banned)']),
    ('Mercury (Mercurous Chloride / Thiomersal)', 'Skin-lightening / preservative', 'Neurotoxic; accumulates in brain, kidneys, liver; causes tremors and memory loss', ['Globally banned in cosmetics (Minamata Convention)', 'EU', 'USA', 'India', 'Canada']),
    ('Lead Acetate', 'Hair color (progressive)', 'Neurotoxin; accumulates in bones; developmental harm in children', ['EU (banned in cosmetics)', 'Canada', 'Japan', 'Australia']),
    ('Toluene', 'Nail polish solvent', 'Neurotoxin; reproductive toxin; developmental harm to fetuses', ['EU (banned in cosmetics)', 'Japan (restricted)', 'California (listed reproductive toxin)']),
    ('Dibutyl Phthalate (DBP)', 'Plasticizer in nail polish', 'Endocrine disruptor; reproductive toxin; developmental toxin (Category 1B)', ['EU (banned in cosmetics)', 'Canada', 'Japan (restricted)']),
    ('Diethylhexyl Phthalate (DEHP)', 'Plasticizer', 'Endocrine disruptor; reproductive toxin; IARC Group 2B carcinogen', ['EU (banned in many applications)', 'USA (CPSC restricted in toys)', 'Canada']),
    ('Coal Tar Dyes (general)', 'Synthetic hair / cosmetic color', 'Contains carcinogenic polycyclic aromatic hydrocarbons (PAHs); skin sensitizer', ['EU (restricted)', 'Canada (banned in cosmetics)', 'USA (restricted)']),
    ('Resorcinol', 'Hair dye / skin exfoliant', 'Thyroid disruptor; skin sensitizer; toxic to aquatic life', ['EU (restricted in cosmetics)', 'Japan (restricted)']),
    ('p-Phenylenediamine (PPD)', 'Oxidative hair dye', 'Strong skin sensitizer; cross-reacts with many medicines; associated with bladder cancer in long-term use', ['EU (concentration restricted)', 'Japan (restricted)']),
    ('Oxybenzone (Benzophenone-3)', 'Chemical UV filter in sunscreen', 'Endocrine disruptor (estrogen mimic); detected in blood and breast milk; coral reef damage', ['Hawaii (banned to protect coral reefs)', 'Palau (banned)', 'US Virgin Islands', 'Key West Florida']),
    ('Octinoxate (Ethylhexyl Methoxycinnamate)', 'Chemical UV filter', 'Endocrine disruption (thyroid and estrogen); coral bleaching; detected in human milk', ['Hawaii (banned)', 'Palau (banned)', 'US Virgin Islands']),
    ('Homosalate', 'Chemical UV filter', 'Penetrates skin; weak endocrine disruptor; EU lowered limit to 0.5% in 2021', ['EU (concentration restricted to 0.5% from 2021)']),
    ('Octocrylene', 'UV filter / photoprotector', 'Converts to benzophenone (potential carcinogen) over time; accumulates in coral', ['EU (under review)', 'Hawaii (banned)']),
    ('Aluminium Chlorohydrate', 'Antiperspirant active', 'Linked to breast cancer (near armpit application); aluminium neurotoxicity concerns', ['EU (concentration restricted)', 'France (recommended limits)']),
    ('Aluminium Zirconium Tetrachlorohydrex', 'Antiperspirant active', 'Aluminium accumulation concerns; possible breast cancer and Alzheimer\'s link', ['EU (concentration limits)']),
    ('Sodium Lauryl Sulphate (SLS as irritant grade)', 'Surfactant used in oral care tests', 'Oral ulcer trigger (canker sores); mucosal irritation; damages taste buds temporarily', ['EU (restricted concentration in toothpaste)']),
    ('Mineral Oil (heavy / technical grade)', 'Occlusive / cheap filler', 'Untreated/mildly treated mineral oil is IARC Group 1 carcinogen; may contain PAHs', ['EU (untreated/mildly treated mineral oil banned in cosmetics)']),
    ('Formaldehyde in Nail Products', 'Nail hardener', 'IARC Group 1 carcinogen; causes allergic contact dermatitis; respiratory sensitizer', ['EU (banned in cosmetics above 0.001% leave-on)', 'California (Prop 65)']),
    ('Acetaldehyde', 'Flavor / processing contaminant', 'IARC Group 1 carcinogen (in alcoholic beverages); respiratory irritant; mutagen', ['EU (restricted as flavouring)', 'WHO advises elimination']),
    ('Acrylamide', 'Process contaminant in starchy fried/baked foods', 'IARC Group 2A (probable human carcinogen); forms when starchy foods cooked above 120°C', ['EU (benchmark levels 2017)', 'California Prop 65 (warning required)']),
    ('Bisphenol A (BPA)', 'Plasticizer / can lining', 'Endocrine disruptor (estrogen mimic); developmental neurotoxin; linked to breast cancer', ['EU (banned in baby bottles, food packaging under review)', 'Canada (declared toxic)', 'France (banned in food contact materials)']),
    ('Styrene', 'Plastic packaging contaminant', 'IARC Group 2B possible carcinogen; neurotoxic; may leach from polystyrene containers', ['EU (restricted in food contact materials)', 'California Prop 65']),

    # ── Banned Contaminants / Illegal Adulterants ──
    ('Sudan Dyes (I, II, III, IV)', 'Illegal synthetic azo dyes used to adulterate food', 'Genotoxic and carcinogenic (IARC); Sudan I is Group 3 — found illegally in chilli powder, paprika, palm oil', ['Globally banned as food additives', 'EU (zero tolerance since 2003)', 'India (FSSAI banned)', 'USA']),
    ('Malachite Green', 'Banned synthetic dye used in aquaculture', 'Carcinogenic; genotoxic; teratogenic; accumulates in fish tissue', ['Globally banned in food-producing fish', 'EU', 'USA', 'India (FSSAI banned)', 'Canada']),
    ('Chloramphenicol', 'Banned antibiotic (food animals)', 'Aplastic anaemia in humans even at trace levels; carcinogenic potential; no safe threshold', ['Globally banned for use in food animals', 'EU', 'USA', 'India', 'Canada', 'Australia']),
    ('Melamine (food adulteration)', 'Industrial chemical illegally added to food/milk to fake protein content', 'Kidney stones and kidney failure; especially fatal in infants (2008 China scandal)', ['Globally banned as food ingredient', 'EU (zero tolerance)', 'USA', 'India']),

    # ── Toxic Process Contaminants ──
    ('1,4-Dioxane', 'Carcinogenic contaminant in ethoxylated cosmetics (SLES, PEG, polysorbates)', 'IARC Group 2B possible carcinogen; forms as by-product of ethoxylation; not disclosed on labels', ['EU (trace limits set for cosmetics)', 'USA (FDA monitoring programme)', 'California Prop 65']),
    ('Nitrosamines (N-nitrosamines)', 'Carcinogenic contaminants formed in nitrite-preserved food or certain cosmetics', 'IARC multiple members are Group 1/2A carcinogens; DNA alkylation; liver and stomach cancer', ['EU (maximum limits in food)', 'Germany (restricted in cosmetics)', 'USA (FDA monitoring)']),
    ('Polycyclic Aromatic Hydrocarbons (PAH)', 'Carcinogenic contaminants in smoked, grilled, charred foods', 'Benzo[a]pyrene is IARC Group 1 carcinogen; mutagen; DNA damage; forms in charred meat/fish', ['EU (maximum levels for benzo[a]pyrene in smoked fish, meat)', 'WHO (limits recommended)']),
    ('Heterocyclic Amines (HCA)', 'Carcinogens formed when meat is cooked at very high temperature (grilling, pan-frying)', 'IARC Group 2A probable human carcinogens; DNA mutations; linked to colorectal and breast cancer', ['WHO recommends limiting consumption', 'IARC monitoring']),
    ('Acrolein', 'Toxic aldehyde formed when cooking oils overheat (deep frying)', 'Highly reactive; lung irritant; DNA damage; mutagenic; associated with cardiovascular disease', ['EU (occupational exposure limits set)', 'California Prop 65 (listed carcinogen)']),

    # ── Banned Cosmetic Actives ──
    ('Dihydroxyacetone (DHA) — spray-on tanning', 'Self-tanning active (safe topically, concerns with spray)', 'Safe in creams/lotions; spray-on DHA inhalation causes potential lung DNA damage; absorbed via lungs', ['EU/USA (FDA warns against inhaling spray-on DHA)', 'Australia (TGA advisory for spray form)']),
    ('Polyacrylamide (cosmetic grade)', 'Film-forming polymer (releases acrylamide)', 'Acrylamide monomer residue is IARC Group 2A probable carcinogen; reproductive toxin; neurotoxin', ['EU (max 0.1 ppm acrylamide residue)', 'Canada (restricted)']),
    ('Nonylphenol Ethoxylates (NPE)', 'Surfactant / emulsifier', 'Strong endocrine disruptor; degrades to nonylphenol in environment (persistent xenoestrogen); fish reproductive toxicity', ['EU (banned in household/personal care products)', 'Canada (restricted)', 'Norway']),
    ('Bronopol (2-Bromo-2-nitropropane-1,3-diol)', 'Formaldehyde-releasing preservative', 'Releases formaldehyde and bromine; forms carcinogenic nitrosamines; strong sensitizer', ['EU (restricted — must declare formaldehyde release)', 'Japan (restricted)']),
],

# ─── WORTH KNOWING ─────────────────────────────────────────────────────────
# Permitted ingredients with considerations — safe for most at normal levels,
# but worth being aware of due to specific effects or sensitivities
'worth_knowing': [

    # ── Artificial Sweeteners (approved, some concerns) ──
    ('Acesulfame Potassium / Acesulfame K (E950)', 'Artificial sweetener', 'Some studies suggest disruption of gut microbiome; insulin response changes; headaches', []),
    ('Sucralose (E955)', 'Artificial sweetener', 'Alters gut bacteria composition; may affect insulin response; bakes into toxic compounds above 120°C', []),
    ('Neotame (E961)', 'Artificial sweetener', 'Limited long-term human data; metabolizes to formaldehyde and aspartic acid', ['EU (labelling required)']),
    ('Advantame (E969)', 'Artificial sweetener', 'Very limited human data; very new approval; metabolizes to phenylalanine', ['EU (labelling required for PKU)']),
    ('Stevia / Steviol Glycosides (E960)', 'Natural-derived sweetener', 'May lower blood pressure significantly; interacts with diabetes/hypertension medications', []),
    ('Monk Fruit Extract (Luo Han Guo)', 'Natural-derived sweetener', 'Limited long-term human data; may cause digestive issues in large amounts', []),
    ('Erythritol (E968)', 'Sugar alcohol sweetener', 'New 2023 study links high blood levels to cardiovascular risk; laxative in large amounts', []),
    ('Xylitol (E967)', 'Sugar alcohol sweetener', 'Laxative at doses above 50g/day; toxic to dogs (veterinary emergency); mild digestive issues', []),
    ('Mannitol (E421)', 'Sugar alcohol sweetener', 'Strong laxative effect; diarrhoea; bloating; should not be given to infants', ['EU (labelling: "excessive consumption may produce laxative effects")']),
    ('Sorbitol (E420)', 'Sugar alcohol / humectant', 'Laxative effect above 10g; diarrhoea; bloating; malabsorption in some', ['EU (labelling: "excessive consumption may produce laxative effects")']),

    # ── Sugars (excess concerns) ──
    ('Sugar (Sucrose)', 'Sweetener', 'Obesity; type 2 diabetes; tooth decay; non-alcoholic fatty liver disease; inflammation', []),
    ('High Fructose Corn Syrup (HFCS)', 'Sweetener', 'Directly metabolized to fat in liver; linked to NAFLD; obesity; insulin resistance', ['Several countries restrict in beverages (Hungary tax)']),
    ('Glucose Syrup (E440-type)', 'Sweetener / bulking agent', 'High glycaemic index; rapid blood sugar spikes; weight gain with regular consumption', []),
    ('Invert Sugar / Invert Syrup', 'Sweetener / humectant', 'High calorie; rapid blood sugar spikes; tooth decay; same metabolic concerns as HFCS', []),
    ('Fructose (crystalline)', 'Sweetener', 'Metabolized by liver into fat; linked to gout, fatty liver disease with excess consumption', []),
    ('Corn Syrup (light/dark)', 'Sweetener / humectant', 'High glycaemic; linked to weight gain; tooth decay; insulin spikes', []),
    ('Maltodextrin (E1400)', 'Carbohydrate bulking agent', 'Glycaemic index higher than sugar (GI ~110-136); disrupts gut microbiome; rapid blood sugar rise', []),
    ('Dextrose (D-Glucose)', 'Sweetener / fermentation substrate', 'High glycaemic index; rapid blood sugar elevation; weight gain with regular use', []),
    ('Agave Nectar / Agave Syrup', 'Sweetener', 'Very high fructose content (70-90%); same liver-fat concerns as HFCS despite "natural" label', []),
    ('Brown Rice Syrup', 'Sweetener', 'High GI (98); arsenic contamination risk from rice source', []),

    # ── Fats & Oils ──
    ('Palm Oil', 'Vegetable oil', 'High saturated fat ~50%; raises LDL cholesterol; 3-MCPD esters (potential carcinogen) in refined oil', []),
    ('Palm Kernel Oil', 'Vegetable oil (highly saturated)', 'Higher saturated fat than palm oil (~82%); strongly raises LDL cholesterol', []),
    ('Palmolein', 'Fractionated palm oil', 'High saturated fat; may raise LDL; 3-MCPD and glycidol ester contamination in refined forms', []),
    ('Hydrogenated Vegetable Oil', 'Modified fat', 'May contain residual trans fats (<0.5g threshold allows "0g trans fat" labelling); cardiovascular risk', []),
    ('Partially Hydrogenated Oil (PHO)', 'Trans fat source', 'WHO estimates trans fats cause 500,000 cardiovascular deaths per year; increases LDL, decreases HDL', ['USA (FDA banned 2020)', 'EU (maximum 2g per 100g of fat since 2021)', 'Canada (banned 2018)', 'Denmark (pioneer ban 2003)']),
    ('Interesterified Fat', 'Modified fat for margarine', 'Increases blood glucose and insulin response; displaces phospholipids; limited human data', []),
    ('Cottonseed Oil', 'Vegetable oil', 'Naturally contains gossypol (toxic to male fertility); usually refined out but contamination risk exists', []),
    ('Refined Vegetable Oil (generic)', 'Cooking oil', '3-MCPD esters and glycidol esters form during high-temperature refining — possible carcinogens', ['EU (maximum levels for 3-MCPD set in 2020)']),

    # ── Emulsifiers ──
    ('Soy Lecithin (E322)', 'Emulsifier', 'Soy allergen (must declare); processed from hexane-extracted soy; digestive issues in sensitive', []),
    ('Mono- and Diglycerides of Fatty Acids (E471)', 'Emulsifier', 'May contain trace trans fats; source fat often unclear (palm, hydrogenated); digestive issues', []),
    ('Polyglycerol Polyricinoleate / PGPR (E476)', 'Emulsifier in chocolate', 'Liver and kidney enlargement in animal studies at high doses; often used to replace cocoa butter cheaply', []),
    ('Ammonium Phosphatides (E442)', 'Emulsifier in chocolate', 'Synthetic; limited long-term human data; may affect mineral absorption', []),
    ('Carrageenan (E407)', 'Thickener / gelling agent', 'Degraded carrageenan causes intestinal inflammation; linked to IBD; triggers immune response in gut cells', ['EU (banned in infant formula)', 'USA (National Organic Program debating removal)']),
    ('Polysorbate 80 (E433)', 'Emulsifier / solubilizer', 'Increases gut permeability; alters gut microbiome composition; may promote metabolic syndrome', []),
    ('Polysorbate 60 (E435)', 'Emulsifier', 'Similar gut microbiome disruption as Polysorbate 80; limited long-term human data', []),
    ('Polysorbate 20 (E432)', 'Emulsifier / solubilizer', 'Gut barrier disruption in animal studies; may promote low-grade intestinal inflammation', []),
    ('DATEM — Diacetyl Tartaric Acid Esters (E472e)', 'Emulsifier in bread', 'Generally safe; may cause digestive upset in some; fat source often palm oil', []),
    ('Sodium Stearoyl Lactylate (E481)', 'Emulsifier / dough conditioner', 'Generally safe; milk derivative — dairy allergen for sensitive individuals', []),
    ('Acetylated Monoglycerides (E472a)', 'Emulsifier', 'Usually safe; fat source often from palm oil or hydrogenated fat', []),
    ('Stearoyl Lactylate (E482)', 'Emulsifier', 'Milk-derived; dairy allergen; digestive issues in sensitive', []),

    # ── Thickeners, Stabilizers, Gelling Agents ──
    ('Carboxymethylcellulose / CMC (E466)', 'Thickener / stabilizer', 'Disrupts gut microbiome; promotes intestinal inflammation; linked to IBD and colorectal cancer in mice', []),
    ('Modified Starch (various E1400s)', 'Thickener / binder', 'Chemically modified with reagents (octenyl succinic acid, acetate, phosphate); high GI; digestive issues', []),
    ('Guar Gum (E412)', 'Thickener / stabilizer', 'Digestive bloating; gas; diarrhoea; inhibits absorption of some medications', []),
    ('Xanthan Gum (E415)', 'Thickener / stabilizer', 'Digestive issues (gas, bloating) in large amounts; may worsen IBS symptoms', []),
    ('Konjac Gum / Glucomannan (E425)', 'Thickener / gelling agent', 'Choking hazard in jelly form (banned in EU/USA for mini cups); diarrhoea; bloating', ['EU (banned in mini cups / jelly products)', 'USA (banned in similar forms)', 'Australia']),
    ('Cellulose Gum (E466 synonym)', 'Thickener', 'Same gut microbiome disruption concerns as CMC', []),
    ('Methyl Cellulose (E461)', 'Thickener / bulking agent', 'Diarrhoea; bloating; may interfere with mineral absorption', []),
    ('Hydroxypropyl Methylcellulose (E464)', 'Thickener / coating agent', 'Digestive laxative effect in large amounts; bloating; gas', []),
    ('Pectin (E440) — high dose', 'Gelling agent', 'Generally safe; large doses may reduce absorption of nutrients (iron, zinc)', []),
    ('Locust Bean Gum (E410)', 'Thickener / stabilizer', 'May cause digestive issues; flatulence; usually safe at normal levels', []),
    ('Agar (E406)', 'Gelling agent', 'May cause digestive discomfort; loose stools in large amounts', []),
    ('Tara Gum (E417)', 'Thickener', 'Limited long-term human data; may cause digestive issues', []),
    ('Sodium Alginate (E401)', 'Thickener / gel', 'Generally safe; large amounts may cause digestive issues', []),

    # ── Preservatives (approved, mild concerns) ──
    ('Potassium Sorbate (E202)', 'Preservative', 'Allergic reactions; contact dermatitis; migraines in sensitive people; DNA damage concerns in vitro', []),
    ('Sorbic Acid (E200)', 'Preservative', 'Skin and mucous membrane irritant; allergic reactions in sensitive people', []),
    ('Calcium Propionate (E282)', 'Bread preservative', 'Linked to irritability, restlessness, and sleep disturbance in children', []),
    ('Sodium Propionate (E281)', 'Preservative in bread', 'May cause migraines; digestive discomfort; limited data on long-term effects', []),
    ('Natamycin (E235)', 'Antifungal preservative', 'Gastrointestinal irritation; nausea; allergic reactions; antibiotic resistance concerns', ['Several countries restrict topical use']),
    ('Benzoic Acid (E210)', 'Preservative', 'Reacts with vitamin C to form benzene; asthma trigger; hives in sensitive people', ['EU (concentration limits)', 'Several countries require labelling']),
    ('Citric Acid (E330) — cosmetic grade high %', 'Acid / preservative / chelator', 'High-concentration cosmetic use causes enamel erosion, skin irritation, photosensitivity', []),
    ('Phenoxyethanol', 'Preservative in cosmetics', 'EU restricts to 1%; toxic to infants (affects CNS); skin irritant; allergic reactions', ['EU (restricted 1% max; banned in products for nappy area of children)']),
    ('Benzyl Alcohol', 'Preservative / solvent', 'Skin sensitizer; toxic to neonates in IV use; contact dermatitis', ['EU (must declare as fragrance allergen above 0.001%)']),
    ('Chlorphenesin', 'Preservative in cosmetics', 'Limited safety data; muscle relaxant (toxic at high levels); irritant', ['EU (concentration restricted)']),
    ('Benzalkonium Chloride', 'Preservative / antimicrobial', 'Asthma aggravation from inhalers; skin sensitizer; eye irritant; antimicrobial resistance', ['EU (restricted in cosmetics)', 'Replaced in many inhaler formulations']),

    # ── Surfactants / Cleansing Agents ──
    ('Sodium Lauryl Sulphate (SLS)', 'Anionic surfactant', 'Strips skin barrier lipids; dries and irritates skin/scalp; triggers aphthous ulcers (canker sores)', ['EU (restricted in oral care products)']),
    ('Sodium Laureth Sulphate (SLES)', 'Anionic surfactant', 'Less irritating than SLS but potential 1,4-dioxane contamination (carcinogen) from ethoxylation process', []),
    ('Ammonium Lauryl Sulphate (ALS)', 'Anionic surfactant', 'Similar irritation profile to SLS; scalp sensitivity; dry skin', []),
    ('Ammonium Laureth Sulphate', 'Anionic surfactant', 'Skin irritation; potential 1,4-dioxane contamination from manufacturing', []),
    ('Cocamidopropyl Betaine (CAPB)', 'Amphoteric surfactant', 'Allergic contact dermatitis; impurities from manufacturing (DMABA) are stronger allergens', []),
    ('Sodium Coco Sulphate', 'Anionic surfactant', 'Irritating at high concentration; similar to SLS in irritation profile', []),
    ('Decyl Glucoside', 'Non-ionic surfactant', 'Very mild; rare contact allergy possible; generally among safest surfactants', []),
    ('TEA Lauryl Sulphate', 'Anionic surfactant', 'Irritating; TEA can form carcinogenic nitrosamines with certain other ingredients', ['EU (TEA-nitrosamine formation restricted)']),

    # ── Silicones ──
    ('Dimethicone', 'Silicone conditioner / skin smoother', 'Occlusive; traps bacteria under skin leading to breakouts; environmental persistence (not biodegradable)', []),
    ('Dimethiconol', 'Silicone for hair', 'Builds up on hair shaft; weighs hair down; requires sulfates to remove; environmental persistence', []),
    ('Cyclopentasiloxane (D5)', 'Volatile silicone', 'Persistent in aquatic environment; potential endocrine disruption; fish reproductive toxicity', ['EU (banned in rinse-off cosmetics above 0.1% since 2020)', 'Canada (considered toxic to environment)']),
    ('Cyclotetrasiloxane (D4)', 'Volatile silicone', 'Endocrine disruptor; reproductive toxin (Category 2); very persistent in environment', ['EU (banned in cosmetics above 0.1%)', 'Canada (toxic substance list)']),
    ('Cyclohexasiloxane (D6)', 'Volatile silicone', 'Persistent bioaccumulative; under review for toxicity and environmental harm', ['EU (under restriction review)']),

    # ── PEG (Polyethylene Glycol) Compounds ──
    ('PEG-100 Stearate', 'Emulsifier / thickener', 'Potential 1,4-dioxane contamination from ethoxylation; penetration enhancer', []),
    ('PEG-40 Hydrogenated Castor Oil', 'Solubilizer / emulsifier', 'Potential 1,4-dioxane contamination; skin sensitizer if impure', []),
    ('PEG-7 Glyceryl Cocoate', 'Emulsifier', 'Penetration enhancer — may increase absorption of other (potentially harmful) ingredients', []),
    ('Ceteareth-20', 'Emulsifier', 'Potential 1,4-dioxane contamination; skin irritant at high concentrations', []),
    ('Laureth-7', 'Surfactant / emulsifier', '1,4-dioxane contamination possible; skin sensitizer', []),

    # ── Chelating Agents ──
    ('Disodium EDTA', 'Chelating agent', 'Removes beneficial calcium and magnesium; environmental pollutant (does not biodegrade easily); penetration enhancer', []),
    ('Tetrasodium EDTA', 'Chelating agent', 'Binds calcium and zinc; may increase penetration of other chemicals; poor biodegradability', []),
    ('Tetrasodium Etidronate', 'Chelating agent', 'May interfere with bone mineralisation with long-term use; poorly biodegradable', []),

    # ── Humectants & Solvents ──
    ('Propylene Glycol (E1520)', 'Humectant / solvent', 'Skin irritation at high concentrations; neurotoxicity at very high IV doses; contact dermatitis', []),
    ('Butylene Glycol', 'Humectant / solvent', 'Skin irritation; mild sensitizer; large amounts potentially toxic', []),
    ('Hexylene Glycol', 'Humectant / solvent', 'Skin and eye irritant at concentration; relatively limited safety data', []),
    ('Isopropyl Alcohol (IPA)', 'Solvent / astringent', 'Dries and strips skin barrier; central nervous system depression at high skin absorption', []),
    ('Ethyl Alcohol / Denatured Alcohol (SD Alcohol)', 'Solvent / astringent', 'Dries skin; disrupts skin barrier with frequent use; worsens rosacea and eczema', []),

    # ── Food Colorants (natural but with considerations) ──
    ('Titanium Dioxide (E171) — food use', 'White colorant / opacity agent', 'Nanoparticle form causes DNA damage; banned in EU as food additive since 2022; still used in India', ['EU (banned as food additive since 2022)', 'UK (under review)']),
    ('Beta-Carotene (E160a) — high dose supplements', 'Orange-yellow colour / pro-vitamin A', 'High dose beta-carotene supplements increase lung cancer risk in smokers by 18% (CARET study, IARC)', []),
    ('Caramel (E150a — plain)', 'Brown colour from sugar heating', 'Generally safest caramel type; high amounts may cause digestive issues', []),
    ('Iron Oxides (E172)', 'Brown/red/yellow colour', 'Generally safe; nanoparticle forms under study for potential toxicity', []),
    ('Annatto (E160b)', 'Yellow-orange natural colour', 'Rare but well-documented allergic reactions; hives; IBS aggravation in sensitive', []),
    ('Paprika Extract (E160c)', 'Red natural colour', 'May cause allergic reactions; skin sensitivity; generally mild concern', []),
    ('Carmine / Cochineal (E120)', 'Natural red colour from insects', 'Severe allergic reactions including anaphylaxis; not vegetarian/vegan; must declare on label', ['EU (mandatory declaration)']),

    # ── Raising Agents / Processing Aids ──
    ('Ammonium Bicarbonate (E503)', 'Leavening agent', 'Generally safe; residual ammonia if not fully baked out; irritant in raw state', []),
    ('Sodium Aluminosilicate (E554)', 'Anticaking agent', 'Aluminium compound; potential aluminium accumulation with high consumption', []),
    ('Aluminium Sodium Silicate (E559)', 'Anticaking agent', 'Aluminium exposure concerns; nausea and digestive issues at high doses', []),
    ('Aluminium Silicate / Kaolin (food grade)', 'Anticaking / processing aid', 'Aluminium compound; potential neurotoxicity with excess cumulative consumption', ['EU (usage limits set)']),
    ('Silicon Dioxide / Silica (E551)', 'Anticaking agent', 'Nanoparticle form possibly affects gut health; inhalation causes silicosis (industrial exposure)', []),
    ('Calcium Silicate (E552)', 'Anticaking agent', 'Generally safe; large amounts may cause digestive issues', []),
    ('Magnesium Carbonate (E504)', 'Anticaking / colour retention', 'Large doses may cause digestive issues; laxative effect', []),
    ('Microcrystalline Cellulose (E460)', 'Bulking agent / anticaking', 'Generally safe; may cause digestive discomfort in large amounts', []),

    # ── Caffeine and Related Stimulants ──
    ('Caffeine', 'Stimulant / flavour', 'Anxiety; insomnia; palpitations; dependency/withdrawal; miscarriage risk above 200mg/day in pregnancy', []),
    ('Guarana Extract', 'Natural caffeine source', 'Same effects as caffeine but often unlabelled; high caffeine content per gram; palpitations', []),
    ('Kola Nut Extract', 'Natural caffeine source', 'High caffeine; tannins irritate gut lining; interacts with blood-thinning medications', []),
    ('Taurine (in energy drinks)', 'Amino acid added to energy drinks', 'Concern about synergistic effects with caffeine and alcohol in energy drinks; limited long-term data', []),
    ('Inositol (in energy drinks)', 'B-vitamin related compound', 'Generally safe at normal doses; laxative effect at high doses', []),
    ('Niacin (added high dose)', 'B3 vitamin — added to fortified foods', 'High dose (above 35mg/day) causes flushing, liver damage; only an issue with supplement doses', []),

    # ── Misc Food Additives ──
    ('Yeast Extract (natural glutamate)', 'Flavour enhancer', 'Natural source of free glutamates; triggers MSG-like reactions in highly sensitive individuals', []),
    ('Hydrolysed Vegetable Protein (HVP)', 'Flavour enhancer', 'Contains free glutamates; headaches in MSG-sensitive people; may contain trace 3-MCPD (carcinogen)', ['EU (3-MCPD limits set)']),
    ('Autolysed Yeast', 'Flavour enhancer', 'Free glutamates similar to MSG; headache, flushing in sensitive people', []),
    ('Natural Flavours (complex mixtures)', 'Flavouring', 'FDA "natural" category is broad; may still contain allergens; no full disclosure required in India', []),
    ('Artificial Flavours', 'Synthetic flavouring', 'Some contain allergens; certain compounds (e.g., diacetyl in butter flavour) linked to lung disease at occupational exposure', []),
    ('Salt / Sodium Chloride (excess)', 'Flavour / preservative', 'Hypertension; cardiovascular disease; kidney disease; stroke with chronic high intake', ['WHO recommends below 5g/day; most Indians consume 10-12g/day']),
    ('Phosphates (food additives E338-342)', 'Acidulant / leavening / preservative', 'Accelerates ageing of kidneys with high intake; decreases bone density; cardiovascular calcification', ['EU (labelling required in children\'s food)']),

    # ── Cosmetic Ingredients — Worth Knowing ──
    ('Petrolatum (Petroleum Jelly — cosmetic grade)', 'Occlusive moisturiser', 'Pharmaceutical/cosmetic grade is safe; but non-pharmaceutical grade may contain carcinogenic PAH impurities', ['EU (only highly refined cosmetic grade permitted)']),
    ('Lanolin', 'Emollient from sheep wool', 'Common allergen in people with wool sensitivity; pesticide residue concerns in non-purified grades', []),
    ('Mineral Oil (cosmetic grade)', 'Occlusive / emollient', 'Highly refined cosmetic grade is safe; petroleum-derived; non-comedogenic light grades safe; heavy grades comedogenic', ['EU (highly refined grade only)']),
    ('Sodium Lauryl Sulphate (oral care)', 'Surfactant in toothpaste', 'Causes canker sores / aphthous ulcers; irritates oral mucosa; may worsen dry mouth', ['EU (restricted concentration in oral care)']),
    ('Oat Extract — Avenanthramides', 'Skin-soothing', 'Rare oat allergy possible; generally very safe for eczema and sensitive skin', []),
    ('Lactic Acid (skin >5%)', 'Alpha-hydroxy acid / exfoliant', 'Sun sensitivity (photosensitization); irritation on broken skin; stinging', ['FDA requires SPF warning for OTC AHA products']),
    ('Glycolic Acid', 'Alpha-hydroxy acid / exfoliant', 'Strong photosensitization; barrier disruption; burns on sensitive skin above 10%', ['EU (concentration and pH limits set)']),
    ('Acetone', 'Nail polish remover / solvent', 'Drying to nails and cuticles; central nervous system effects at high inhalation', []),
    ('Butyl Acetate', 'Nail polish solvent', 'Skin and eye irritant; mild CNS effects at high inhalation; flammable', []),
    ('Nitrocellulose', 'Nail polish film-former', 'Flammable; may cause irritation; historically derived from cotton — generally safe in nails', []),
    ('Parabens (general / mixed)', 'Preservative system', 'Cumulative estrogen-mimicking load from multiple paraben-containing products used daily', ['EU (prohibited combinations of propyl, butyl, isopropyl, isobutyl parabens in leave-on products for children under 3)']),
    ('Retinyl Palmitate (Vitamin A ester) — sunscreen', 'Antioxidant / anti-aging', 'When combined with UV radiation may speed development of skin tumours (animal data)', ['EU (concentration restricted in products used in sun)']),
    ('Nanoparticles (general — cosmetics)', 'Delivery system / filter', 'Very small particles (<100nm) may penetrate intact skin or inhaled nanosprays; under ongoing review', ['EU (mandatory nano labelling on cosmetics)']),

    # ── Chemical UV Filters (approved but considerations) ──
    ('Avobenzone (Butyl Methoxydibenzoylmethane)', 'Chemical UVA filter', 'Photodegraded rapidly by UV — becomes ineffective within 30 min unless stabilised with octocrylene', []),
    ('Octisalate (Ethylhexyl Salicylate)', 'Chemical UVB filter', 'Weak endocrine activity in some studies; skin sensitizer in sensitive individuals; photostable', []),
    ('Benzophenone-4 / Sulisobenzone', 'Chemical UV filter', 'Higher sensitization potential than other UV filters; photo-allergy possible', ['EU (restricted concentration)']),
    ('Bemotrizinol (Tinosorb S)', 'Broad-spectrum UV filter', 'Appears safe; limited long-term data; detected in breast milk in one study', ['Not yet approved in USA (FDA)']),
    ('Bisoctrizole (Tinosorb M)', 'Mineral-organic hybrid UV filter', 'Limited long-term human data; EU-approved but not FDA-approved', ['Not yet approved in USA']),

    # ── Preservatives with considerations ──
    ('Sodium Fluoride (in toothpaste)', 'Fluoride source / caries prevention', 'Dental fluorosis in children with excess swallowing; skeletal fluorosis at very high long-term intake', ['EU (max 0.15% for children\'s toothpaste)', 'WHO (recommends fluoride monitoring in water)']),
    ('Chlorhexidine Digluconate', 'Antimicrobial / oral antiseptic', 'Stains teeth brown with extended use; alters taste; rare anaphylaxis; disrupts oral microbiome', ['EU (restricted in some cosmetics)']),
    ('Cetrimonium Bromide', 'Quaternary ammonium antimicrobial / conditioner', 'Skin and eye irritant at higher concentrations; environmental toxicity to aquatic organisms', ['EU (concentration restricted in cosmetics)']),
    ('Behentrimonium Methosulfate (BTMS)', 'Conditioning emulsifier', 'Generally mild; rare contact sensitization; derived from rapeseed; safer than older quats', []),
    ('Benzethonium Chloride', 'Quaternary ammonium preservative / antimicrobial', 'Skin and eye irritant; absorbed through skin; toxicity at high systemic doses', ['EU (restricted in cosmetics)']),

    # ── Carbohydrate-based Additives ──
    ('Hydroxypropyl Cellulose (E463)', 'Thickener / binder', 'Digestive discomfort in large amounts; poorly digested; may interfere with drug absorption timing', []),
    ('Sucrose Esters of Fatty Acids (E473)', 'Emulsifier', 'Generally safe; high amounts may have laxative effect; fat source often palm', []),
    ('Polyglycerol Esters of Fatty Acids (E475)', 'Emulsifier', 'Generally safe at food levels; limited long-term data at high doses', []),
    ('Lactic Acid Esters of Mono- and Diglycerides (E472b)', 'Emulsifier in baked goods', 'Generally safe; milk derivatives possible — allergen consideration', []),
    ('Acetylated Distarch Phosphate (E1414)', 'Modified starch thickener', 'Chemically modified; high GI; digestive issues with large amounts', []),
    ('Octenyl Succinic Anhydride Starch (E1450)', 'Modified starch emulsifier', 'Chemical modification with OSA; residual OSA concerns; generally approved', []),

    # ── Polymer / Film-forming Ingredients ──
    ('Carbomer (Carbopol)', 'Thickening polymer in skincare', 'Generally safe; trace benzene contamination found in some batches (2020 recalls); neutralising agent irritation', ['FDA (benzene contamination recall 2020)']),
    ('Acrylates Copolymer', 'Film-forming polymer', 'Generally safe topically; potential for skin sensitization in some formulations; environmental persistence', []),
    ('Hydroxyethylcellulose', 'Thickener / film-former', 'Generally safe; may cause mild digestive effects if ingested in large amounts; well-tolerated topically', []),
    ('Polyisobutene', 'Film-forming occlusive polymer', 'Petroleum-derived; comedogenic at high concentrations; environmental persistence concern', []),

    # ── Minerals (concerns at high intake) ──
    ('Sodium Bicarbonate (baking soda, excess)', 'Leavening / antacid', 'Alkalosis with excess ingestion; gas; bloating; interferes with stomach acid (digestion)', []),
    ('Potassium Sorbate + Sodium Benzoate (combination)', 'Dual preservative system', 'Combination may be more allergenic; each alone is safer; interaction with vitamin C (benzene risk)', []),
    ('Glycyrrhizin / Licorice Sweetener (high dose)', 'Natural sweetener from licorice root', 'Raises blood pressure; causes potassium loss; hormonal effects; WHO advises <100mg/day', ['Several countries restrict high licorice consumption in pregnancy']),
    ('Dioctyl Sodium Sulfosuccinate / Docusate (E480)', 'Surfactant / stool softener used as food wetting agent', 'Used medically as laxative; as food additive — limited human data; digestive effects', ['EU (restricted to specific uses)']),
],

# ─── GENERALLY RECOGNISED ──────────────────────────────────────────────────
# Ingredients with no significant regulatory flags at normal levels of use
'generally_recognised': [

    # ── Water & Base ──
    ('Water (Aqua / Purified Water)', 'Base/solvent for all formulations', 'No concerns at all', []),
    ('Rose Water', 'Natural hydrosol from rose petals', 'Toning, anti-inflammatory; safe for all skin types', []),
    ('Thermal Water', 'Mineral-rich spring water', 'Soothing; rich in selenium and silica; safe', []),

    # ── Vitamins ──
    ('Ascorbic Acid (Vitamin C)', 'Antioxidant / skin brightener (E300)', 'Large oral doses may cause diarrhea or kidney stones; topically safe', []),
    ('Tocopherol / Vitamin E (E306-E309)', 'Antioxidant / skin conditioner', 'Safe at normal levels; blood thinning at very high supplement doses', []),
    ('Niacinamide (Vitamin B3)', 'Brightening / barrier repair / anti-aging', 'Safe; flushing only with oral doses >35mg; topically universally safe', []),
    ('Panthenol (Pro-Vitamin B5)', 'Moisturiser / wound healer', 'Deeply moisturising; non-sensitizing; widely safe across all skin types', []),
    ('Pyridoxine Hydrochloride (Vitamin B6)', 'Nutrient / scalp health', 'Safe at normal dietary levels; peripheral neuropathy only at extreme supplement mega-doses', []),
    ('Biotin (Vitamin B7)', 'Hair/nail growth supplement', 'Safe at normal levels; may interfere with thyroid and hormone blood test results', []),
    ('Riboflavin (Vitamin B2 / E101)', 'Nutrient / natural yellow color', 'Safe at normal levels; turns urine bright yellow (harmless)', []),
    ('Thiamine (Vitamin B1)', 'Nutrient', 'Safe at normal dietary levels; very rare allergic reactions with IV administration', []),
    ('Folic Acid (Vitamin B9)', 'Nutrient (critical in pregnancy)', 'Safe at recommended doses; very high doses may mask vitamin B12 deficiency', []),
    ('Vitamin D3 (Cholecalciferol)', 'Fat-soluble nutrient', 'Safe at recommended doses; toxicity (hypercalcemia) only at extreme supplement doses', []),
    ('Vitamin K1 (Phylloquinone)', 'Nutrient / clotting', 'Safe at dietary levels; may interact with warfarin anticoagulant', []),
    ('Retinol (Vitamin A) — low cosmetic %', 'Anti-aging skin ingredient', 'Safe in cosmetics at <0.3% (EU); avoid in pregnancy at higher concentrations', ['EU (max 0.05% in face products, 0.3% in body)']),
    ('Ascorbyl Glucoside', 'Stable vitamin C derivative', 'Gentle, non-irritating vitamin C; safe for sensitive skin', []),
    ('Sodium Ascorbyl Phosphate', 'Stable vitamin C derivative', 'Non-irritating; stable; safe for all skin types', []),
    ('Tocopheryl Acetate (Vitamin E ester)', 'Antioxidant / skin conditioner', 'Stable vitamin E; safe; rare contact allergy possible', []),

    # ── Skin-Identical & Biocompatible Ingredients ──
    ('Hyaluronic Acid (HA / Sodium Hyaluronate)', 'Humectant / skin hydrator', 'Natural skin component; safe for all skin types and ages', []),
    ('Ceramide NP', 'Skin barrier lipid', 'Identical to skin-produced ceramide; restores barrier; safe for all skin', []),
    ('Ceramide AP', 'Skin barrier lipid', 'Skin-identical; supports barrier function; safe', []),
    ('Ceramide EOP', 'Skin barrier lipid', 'Skin-identical long-chain ceramide; safe and beneficial', []),
    ('Squalane (plant-derived)', 'Lightweight emollient', 'Skin-identical; non-comedogenic; stable; safe for all skin types', []),
    ('Cholesterol', 'Emollient / barrier repair', 'Skin-identical lipid; supports barrier; safe', []),
    ('Sodium PCA', 'Natural moisturising factor', 'Natural skin component; safe humectant; no concerns', []),
    ('Amino Acids (Serine, Glycine, etc.)', 'Moisturising / protein building blocks', 'Natural skin components; safe; no concerns', []),
    ('Urea (5-10% in skincare)', 'Keratolytic / humectant', 'Safe at 5-40%; higher concentrations treat skin conditions; natural skin component', []),
    ('Allantoin', 'Soothing / healing agent', 'Well-documented safety; calming; wound-healing; safe for sensitive skin', []),
    ('Beta-Glucan (oat-derived)', 'Immunomodulating / soothing', 'Highly effective soothing agent; safe for all skin types', []),
    ('Colloidal Oatmeal', 'Soothing for eczema/sensitive skin', 'FDA approved OTC skin protectant; safe; highly effective for eczema', []),
    ('Bisabolol (from chamomile)', 'Skin-soothing / anti-inflammatory', 'Gentle; anti-irritant; safe for sensitive skin', []),
    ('Collagen Hydrolysate', 'Film-forming / moisturising', 'Safe topically; too large to penetrate skin but safe; oral supplements also generally safe', []),
    ('Elastin Hydrolysate', 'Skin conditioner', 'Safe topically; moisturising film-former', []),
    ('Silk Amino Acids', 'Moisturising / film-forming', 'Safe; adds shine and softness; mild allergen rarely', []),

    # ── Active Skin Ingredients ──
    ('Salicylic Acid (0.5-2%)', 'BHA exfoliant / anti-acne', 'Safe at cosmetic concentrations; avoid in pregnancy at higher concentrations', []),
    ('Niacinamide (4-10%)', 'Multi-functional active', 'Brightening, pore-minimizing, anti-inflammatory; safe even for sensitive skin', []),
    ('Azelaic Acid (up to 10%)', 'Anti-acne / brightening / anti-rosacea', 'Safe for use in pregnancy; rare stinging; well-tolerated', []),
    ('Alpha-Arbutin', 'Skin brightener (enzymatic precursor to hydroquinone)', 'Safe at cosmetic concentrations (up to 2%); degrades slowly', []),
    ('Kojic Acid (below 1%)', 'Skin brightener from fermentation', 'Safe at low concentrations; may cause temporary sensitisation at high %', []),
    ('Ferulic Acid', 'Antioxidant / enhances Vitamin C', 'Safe; no known adverse effects at cosmetic concentrations', []),
    ('Mandelic Acid', 'Gentle AHA exfoliant', 'Large molecule — less irritating than glycolic; safe for darker skin tones', []),
    ('Phytic Acid', 'Antioxidant / mild brightener', 'Safe at cosmetic concentrations; naturally from rice bran', []),
    ('Tranexamic Acid', 'Brightener / anti-melasma', 'Safe topically; oral form used medically; well-tolerated', []),
    ('Adenosine', 'Anti-aging / wrinkle-smoothing', 'Naturally occurring in all cells; safe for all skin types', []),
    ('Copper Peptide GHK-Cu', 'Wound healing / anti-aging', 'Well-studied; collagen stimulating; safe', []),
    ('Palmitoyl Tripeptide-1', 'Anti-aging peptide', 'Synthetic collagen-stimulating peptide; safe', []),
    ('Palmitoyl Tetrapeptide-7', 'Anti-inflammatory peptide', 'Reduces inflammation; safe', []),
    ('Acetyl Hexapeptide-3 (Argireline)', 'Anti-wrinkle peptide', 'Safe; works on muscle relaxation at skin surface; no systemic effect', []),
    ('Zinc PCA', 'Sebum-regulating mineral complex', 'Safe; reduces excess sebum; anti-bacterial for acne', []),

    # ── Natural Oils & Butters ──
    ('Coconut Oil (Virgin)', 'Emollient / antimicrobial', 'Antimicrobial properties; safe; may be comedogenic on acne-prone skin', []),
    ('Argan Oil', 'Emollient / hair conditioner', 'Rich in vitamin E and fatty acids; safe for all skin and hair types', []),
    ('Jojoba Oil / Jojoba Wax', 'Non-comedogenic emollient', 'Actually a liquid wax; closely mimics sebum; non-comedogenic; safe', []),
    ('Shea Butter', 'Rich emollient / anti-inflammatory', 'Safe for all skin types; rare latex/tree nut allergy possible', []),
    ('Sweet Almond Oil', 'Emollient / massage oil', 'Rich in oleic acid; safe; tree nut allergy caution', []),
    ('Avocado Oil', 'Nourishing emollient', 'Rich in oleic acid and vitamins; safe; non-comedogenic', []),
    ('Rosehip Seed Oil', 'Regenerative oil (anti-aging)', 'Rich in trans-retinoic acid (natural retinol) and linoleic acid; safe', []),
    ('Sunflower Seed Oil', 'Lightweight emollient', 'Rich in linoleic acid; safe; good for sensitive/eczema skin', []),
    ('Castor Oil', 'Occlusive / lash growth', 'Safe; may cause stickiness; rare allergic reactions', []),
    ('Sesame Oil', 'Ayurvedic emollient', 'Natural antioxidants; anti-inflammatory; safe; sesame allergy rare', []),
    ('Sea Buckthorn Oil', 'Nutrient-rich skin oil', 'Rich in vitamins C and E; anti-inflammatory; safe', []),
    ('Marula Oil', 'Lightweight emollient', 'High in oleic acid; antioxidant; safe for all skin types', []),
    ('Bakuchiol', 'Natural retinol alternative (from Psoralea corylifolia)', 'Clinically proven retinol-like effects; safe in pregnancy unlike retinol', []),
    ('Cocoa Butter', 'Rich emollient', 'Safe; antioxidant; suitable for dry skin; may be comedogenic for some', []),
    ('Mango Butter', 'Rich emollient', 'Moisturising; safe; rich in stearic acid', []),
    ('Neem Oil', 'Ayurvedic antimicrobial oil', 'Strong antimicrobial and antifungal; safe in diluted cosmetic use', []),

    # ── Herbal / Plant Extracts ──
    ('Aloe Vera Gel / Extract', 'Soothing / moisturising botanical', 'Widely documented safety; anti-inflammatory; safe for all skin types', []),
    ('Neem Extract (leaf)', 'Antibacterial / antifungal botanical', 'Ayurvedic tradition; safe topically; not for internal use in concentrated form', []),
    ('Tulsi (Holy Basil) Extract', 'Adaptogenic / antimicrobial botanical', 'Antioxidant; adaptogenic; safe at normal use', []),
    ('Ashwagandha Extract (Withania somnifera)', 'Adaptogenic herb', 'Stress reduction; safe at recommended doses; limited data in pregnancy', []),
    ('Turmeric / Curcumin', 'Anti-inflammatory / antioxidant spice', 'Strong anti-inflammatory; safe at dietary levels; may interact with blood thinners at high supplement doses', []),
    ('Ginger Extract (Zingiber officinale)', 'Anti-nausea / anti-inflammatory botanical', 'Safe at normal levels; may interact with blood thinners at very high doses', []),
    ('Chamomile Extract (Matricaria)', 'Soothing / anti-inflammatory', 'Well-documented safety; calming for skin; rare ragweed cross-allergy', []),
    ('Calendula Extract (Marigold)', 'Wound-healing / anti-inflammatory', 'Safe; soothing for sensitive skin; mild allergen in those sensitive to Asteraceae family', []),
    ('Green Tea Extract (EGCG)', 'Antioxidant / anti-inflammatory', 'Well-studied safety; potent antioxidant; safe topically and as food', []),
    ('White Tea Extract', 'Antioxidant botanical', 'Strong antioxidant; safe', []),
    ('Rosemary Extract', 'Natural antioxidant preservative (E392)', 'Safe as natural preservative; antioxidant; anti-inflammatory', []),
    ('Lavender Extract / Oil', 'Calming / antimicrobial botanical', 'Safe at low concentrations; lavender oil above 10% can be irritating; EU listed fragrance allergen at high doses', []),
    ('Hibiscus Extract', 'Antioxidant / gentle AHA source', 'Natural AHA; safe; antioxidant', []),
    ('Rose Extract / Rose Hip', 'Antioxidant / astringent', 'Safe; anti-inflammatory; antioxidant', []),
    ('Pomegranate Extract', 'Potent antioxidant', 'Rich in ellagic acid and punicalagins; anti-inflammatory; safe', []),
    ('Centella Asiatica (Gotu Kola)', 'Wound healing / anti-inflammatory botanical', 'Madecassoside and asiaticoside accelerate wound healing; safe; recommended for sensitive skin', []),
    ('Licorice Root Extract (Glycyrrhiza)', 'Skin brightener / anti-inflammatory', 'Safe at cosmetic concentrations; brightening via glabridin mechanism', []),
    ('Cucumber Extract', 'Soothing / toning', 'Safe; cooling and anti-puffiness; mild antioxidant', []),
    ('Papaya Extract / Papain', 'Gentle enzymatic exfoliant', 'Safe at cosmetic concentrations; dissolves dead skin cells; safe for sensitive skin', []),
    ('Amla / Indian Gooseberry Extract', 'Antioxidant / hair strengthener', 'Very high Vitamin C; safe; traditional Ayurvedic use', []),
    ('Moringa Extract (Moringa oleifera)', 'Nutrient-rich botanical', 'Rich in oleic acid and antioxidants; safe', []),
    ('Brahmi (Bacopa monnieri) Extract', 'Cognitive adaptogen', 'Safe at normal Ayurvedic doses; neuroprotective', []),
    ('Neem Bark / Babool Extract', 'Oral care antimicrobial', 'Traditional oral care; antibacterial; safe in oral care products', []),
    ('Tea Tree Oil (diluted 1-5%)', 'Antimicrobial / antifungal essential oil', 'Safe at 1-5% in cosmetics; undiluted form toxic if ingested; mild skin irritant at high concentrations', []),
    ('Sandalwood Extract', 'Soothing / anti-inflammatory', 'Safe; anti-inflammatory; antioxidant', []),
    ('Vetiver Root Extract', 'Soothing / grounding', 'Safe in cosmetics; mild astringent', []),
    ('Triphala Extract', 'Ayurvedic antioxidant blend', 'Safe at normal Ayurvedic doses; digestive health', []),
    ('Giloy / Guduchi Extract (Tinospora cordifolia)', 'Immunomodulatory Ayurvedic herb', 'Generally safe; immune support; note WHO CAMH advises caution in autoimmune diseases', []),
    ('Shatavari Extract (Asparagus racemosus)', 'Ayurvedic adaptogen', 'Safe at normal doses; women\'s health herb', []),

    # ── Minerals & Clays ──
    ('Zinc Oxide (cosmetic / sunscreen grade)', 'Mineral sunscreen / anti-inflammatory', 'Safest UV filter; safe even for babies; FDA category I (Generally Recognised as Safe)', []),
    ('Kaolin Clay', 'Absorbent / mattifying clay', 'Very gentle clay; safe for sensitive skin; no concerns', []),
    ('Bentonite Clay', 'Detoxifying / absorbent clay', 'Safe topically; internally FDA has concerns about lead content in some products', []),
    ('French Green Clay', 'Purifying / mineral-rich clay', 'Safe for topical use; mineral-rich; no concerns', []),
    ('Calcium Carbonate (E170)', 'Chalky white mineral / calcium supplement', 'Safe at dietary levels; gas/bloating only with very high doses', []),
    ('Magnesium Sulphate (Epsom Salt)', 'Muscle-relaxing mineral soak', 'Safe topically; oral: laxative; safe', []),
    ('Zinc (as gluconate/sulphate)', 'Essential mineral supplement', 'Safe at RDA levels; nausea at high supplement doses; excess impairs copper absorption', []),
    ('Iron (as ferrous sulphate)', 'Essential mineral supplement', 'Safe at RDA; constipation, dark stools at supplement doses; overdose toxic', []),
    ('Calcium', 'Essential mineral supplement', 'Safe at RDA; kidney stones only with very high supplement use', []),
    ('Selenium', 'Essential trace mineral', 'Safe at RDA (55mcg/day); toxicity (selenosis) above 400mcg/day', []),

    # ── Waxes & Natural Fixers ──
    ('Beeswax (E901)', 'Natural wax emulsifier / protective', 'Safe; rare allergy in bee-pollen sensitive; moisturising and protective', []),
    ('Carnauba Wax (E903)', 'Plant wax (from palm leaves)', 'Safe glazing agent; indigestible but harmless; non-toxic', []),
    ('Candelilla Wax', 'Vegan wax from Euphorbia plant', 'Safe vegan alternative to beeswax; no concerns', []),
    ('Rice Bran Wax', 'Natural plant wax', 'Safe emollient; natural; no concerns', []),
    ('Shellac (E904)', 'Resin from lac insect', 'Safe; rare allergy; natural glazing agent', []),

    # ── Common Food Ingredients ──
    ('Whole Wheat Flour', 'Whole grain flour', 'Rich in fibre; safe; gluten-containing (celiac/gluten sensitivity note)', []),
    ('Wheat Flour (Maida)', 'Refined white flour', 'Lower fibre than whole wheat; high GI; safe at normal levels', []),
    ('Rice Flour', 'Grain flour (gluten-free)', 'Safe; gluten-free; good for sensitive digestive systems', []),
    ('Oat Flour / Rolled Oats', 'Whole grain (high fibre)', 'Rich in beta-glucan; cholesterol-lowering; safe; oat protein cross-reacts in some celiacs', []),
    ('Gram Flour (Besan)', 'Legume flour (chickpea)', 'High protein; gluten-free; safe', []),
    ('Maize / Corn Flour', 'Grain flour (gluten-free)', 'Safe; gluten-free; common in Indian cooking', []),
    ('Semolina (Rava / Sooji)', 'Coarse-ground wheat', 'Safe; contains gluten; good source of B vitamins', []),
    ('Milk / Full-fat Milk', 'Dairy — calcium and protein source', 'Safe for lactose-tolerant individuals; dairy allergen (must declare)', []),
    ('Skimmed Milk Powder', 'Low-fat dairy ingredient', 'Safe; good protein source; dairy allergen', []),
    ('Whey Protein', 'Dairy protein concentrate', 'Safe and well-studied; dairy allergen; acne trigger in some individuals', []),
    ('Casein / Milk Protein', 'Slow-release dairy protein', 'Safe; dairy allergen; digestive issues in lactose-intolerant', []),
    ('Butter', 'Dairy fat', 'Natural saturated fat; safe at normal dietary levels', []),
    ('Ghee (Clarified Butter)', 'Traditional Indian cooking fat', 'Rich in fat-soluble vitamins; anti-inflammatory short-chain fatty acids; safe', []),
    ('Cream', 'Dairy fat', 'Natural; safe; high saturated fat', []),
    ('Eggs / Whole Egg Powder', 'Complete protein source', 'Excellent nutrition; egg allergen (must declare); safe', []),
    ('Honey', 'Natural sweetener / antimicrobial', 'Safe for adults; NOT suitable for infants under 1 year (botulism risk)', []),
    ('Pure Apple Cider Vinegar', 'Fermented fruit vinegar', 'Safe at diluted concentrations; undiluted erodes tooth enamel', []),
    ('Lemon Juice / Citric Juice', 'Natural acidulant', 'Safe at normal use; enamel erosion if very frequent undiluted contact', []),
    ('Tamarind Extract', 'Souring agent / natural flavour', 'Safe; traditional use; may interact with some medications (blood thinners) at very high amounts', []),
    ('Mango Pulp / Puree', 'Natural fruit ingredient', 'Safe; good source of vitamins A and C', []),
    ('Tomato Puree / Paste', 'Natural vegetable ingredient', 'Safe; rich in lycopene; antioxidant', []),
    ('Cocoa Powder (unsweetened)', 'Natural chocolate flavour', 'Rich in antioxidants (flavanols); safe; stimulant effect from theobromine', []),
    ('Dark Chocolate (above 70%)', 'Flavour / ingredient', 'Rich in beneficial flavanols; safe; stimulant theobromine; safe at normal amounts', []),
    ('Coconut Milk / Coconut Water', 'Plant-based dairy alternative', 'Safe; naturally electrolyte-rich; high fat in milk form', []),
    ('Soya Milk / Soy Protein', 'Plant-based protein', 'Safe; soy allergen (must declare); phytoestrogens — generally fine at normal food amounts', []),
    ('Lactic Acid Culture / Lactobacillus', 'Probiotic bacteria', 'Beneficial; promotes gut health; safe; used in yogurt and fermented foods', []),
    ('Bifidobacterium strains', 'Probiotic bacteria', 'Well-studied beneficial bacteria; safe; promotes gut and immune health', []),
    ('Inulin (prebiotic fibre)', 'Prebiotic / dietary fibre', 'Feeds beneficial gut bacteria; gas and bloating in large amounts; generally safe', []),
    ('Psyllium Husk', 'Soluble dietary fibre', 'Highly effective for cholesterol and constipation; safe; must take with water', []),
    ('Oat Bran', 'Soluble fibre (beta-glucan source)', 'Cholesterol-lowering; safe; excellent source of soluble fibre', []),

    # ── Indian Spices (commonly used) ──
    ('Turmeric (Haldi)', 'Spice / anti-inflammatory', 'Potent anti-inflammatory curcumin; antioxidant; safe at dietary levels', []),
    ('Cumin (Jeera)', 'Spice / digestive aid', 'Carminative; digestive aid; safe', []),
    ('Coriander (Dhania)', 'Spice', 'Digestive; antioxidant; safe', []),
    ('Cardamom (Elaichi)', 'Spice / digestive aid', 'Carminative; anti-inflammatory; safe', []),
    ('Cloves (Laung)', 'Spice / oral antimicrobial', 'Potent antimicrobial eugenol; antioxidant; safe at normal use', []),
    ('Cinnamon (Dalchini)', 'Spice / blood sugar moderator', 'Safe at normal dietary levels; cassia variety high coumarin — avoid excess supplement doses', []),
    ('Black Pepper (Kali Mirch)', 'Spice / bioavailability enhancer', 'Piperine enhances absorption of nutrients and drugs; safe at dietary levels', []),
    ('Ginger (Adrak)', 'Spice / anti-nausea', 'Well-documented safety; anti-nausea; anti-inflammatory; safe', []),
    ('Garlic (Lahsun)', 'Spice / antimicrobial', 'Potent allicin antimicrobial; cardiovascular benefits; safe', []),
    ('Mustard Seeds (Sarson)', 'Spice', 'Antioxidant; safe at dietary levels; mustard allergen (must declare in EU)', []),
    ('Fenugreek Seeds (Methi)', 'Spice / blood sugar support', 'May lower blood sugar; safe at dietary levels; uterine stimulant at very high amounts', []),
    ('Fennel Seeds (Saunf)', 'Spice / digestive carminative', 'Safe; carminative; digestive', []),
    ('Asafoetida / Hing', 'Digestive spice', 'Carminative; anti-flatulent; safe at normal use', []),
    ('Star Anise', 'Spice / flavour', 'Safe; digestive; antioxidant', []),
    ('Nutmeg (Jaiphal)', 'Spice', 'Safe at culinary levels; toxic (hallucinations, tachycardia) only at very high doses above 5g', []),
    ('Ajwain (Carom Seeds)', 'Spice / digestive aid', 'Thymol antimicrobial; carminative; safe at dietary levels', []),
    ('Bay Leaves', 'Herb / flavour', 'Safe; antioxidant; antimicrobial', []),
    ('Saffron (Kesar)', 'Spice / colorant / mood-enhancing', 'Safe at culinary levels (up to 1.5g/day); antidepressant properties; expensive — often adulterated', []),
    ('Poppy Seeds (Khus Khus)', 'Seed ingredient', 'Culinary use is safe; trace morphine compounds present but not pharmacologically significant at food amounts', []),
    ('Sesame Seeds (Til)', 'Seed ingredient', 'Safe; rich in calcium and antioxidants; sesame allergen (now must declare in EU/USA)', []),
    ('Curry Leaves', 'Herb / antioxidant', 'Rich in vitamins; antioxidant; safe', []),

    # ── Nuts & Seeds (as food ingredients) ──
    ('Almonds', 'Tree nut', 'Rich in vitamin E and monounsaturated fat; tree nut allergen; safe', []),
    ('Cashews', 'Tree nut', 'Rich in minerals; tree nut allergen; safe', []),
    ('Walnuts', 'Tree nut (omega-3 rich)', 'Rich in ALA omega-3; anti-inflammatory; tree nut allergen; safe', []),
    ('Pistachios', 'Tree nut', 'Rich in antioxidants; tree nut allergen; safe', []),
    ('Peanuts (Groundnuts)', 'Legume (commonly called nut)', 'Rich in protein; peanut allergy is common and can be severe — must declare', []),
    ('Flaxseeds (Alsi)', 'Omega-3 rich seed', 'Rich in ALA and fibre; safe; grind for better absorption', []),
    ('Chia Seeds', 'Omega-3 rich seed', 'Rich in fibre, omega-3; safe; drink with water to avoid choking', []),
    ('Sunflower Seeds', 'Seed', 'Rich in vitamin E; safe', []),
    ('Pumpkin Seeds', 'Seed (rich in zinc)', 'Rich in zinc and magnesium; safe', []),

    # ── Fermented / Probiotic ──
    ('Natural Yogurt / Curd (Dahi)', 'Fermented dairy', 'Rich in probiotics; calcium; safe', []),
    ('Cheese Culture', 'Probiotic for cheese making', 'Beneficial bacteria; safe', []),
    ('Apple Cider Vinegar (raw, with mother)', 'Fermented raw vinegar', 'Prebiotic; antimicrobial; safe diluted; enamel erosion undiluted', []),
    ('Kimchi / Fermented Vegetables', 'Probiotic food', 'Rich in beneficial Lactobacillus; safe; sodium content to note', []),
    ('Miso', 'Fermented soy paste', 'Probiotic; safe; high sodium', []),
    ('Kefir', 'Fermented dairy drink', 'Rich in diverse probiotic strains; safe; dairy allergen', []),

    # ── Grains & Pulses ──
    ('Brown Rice', 'Whole grain (high fibre)', 'More nutritious than white rice; safe; arsenic levels in soil — normal consumption safe', []),
    ('Quinoa', 'Complete protein grain', 'Complete protein; gluten-free; safe; saponin coating should be rinsed', []),
    ('Lentils (Dal — Masoor, Moong, Toor)', 'Legume protein source', 'Rich in protein and fibre; safe; phytic acid reduces mineral absorption — soaking helps', []),
    ('Chickpeas (Chana)', 'Legume protein source', 'High protein and fibre; safe; gas-producing — soak and cook thoroughly', []),
    ('Mung Beans (Moong)', 'Legume protein source', 'High protein; easily digestible; safe', []),
    ('Kidney Beans (Rajma)', 'Legume', 'High protein; MUST cook thoroughly — raw beans contain phytohaemagglutinin (lectin) which causes food poisoning; cooked form safe', []),
    ('Soybean', 'Legume protein source', 'Complete protein; soy allergen (must declare); phytoestrogens safe at normal food amounts', []),

    # ── Natural Gums & Fibres (food grade safe) ──
    ('Gum Arabic / Acacia Gum (E414)', 'Prebiotic fibre / emulsifier', 'Prebiotic; well-tolerated at normal food amounts; safe', []),
    ('Agar (E406)', 'Gelling agent from seaweed', 'Vegan gelatin alternative; safe', []),
    ('Pectin (E440) — normal food levels', 'Natural gelling agent from citrus/apple', 'Natural fibre; cholesterol-lowering; safe at food amounts', []),

    # ── Natural Colorants ──
    ('Beetroot Red (E162)', 'Natural red colour', 'Safe; causes red urine/stools (harmless); antioxidant', []),
    ('Chlorophyll / Chlorophyllin (E140/E141)', 'Natural green colour', 'Safe; antioxidant', []),
    ('Turmeric / Curcumin (E100)', 'Natural yellow colour', 'Anti-inflammatory; antioxidant; safe', []),
    ('Saffron (E164 equivalent)', 'Natural yellow-red colour', 'Safe; anti-inflammatory; mood-enhancing', []),
    ('Carotenes from natural sources (E160)', 'Natural orange color from vegetables', 'Pro-vitamin A; safe from food sources (not high-dose supplements)', []),

    # ── Acid / pH Adjusters (safe levels) ──
    ('Acetic Acid (E260) — food grade dilute', 'Mild acidulant / vinegar acid', 'Safe at food grade concentrations; antimicrobial', []),
    ('Lactic Acid (E270) — food/low cosmetic', 'Fermentation acid / AHA', 'Safe in food; mild AHA in cosmetics at low concentrations', []),
    ('Malic Acid (E296) — food grade', 'Fruit acid / flavour enhancer', 'Safe at food levels; slight enamel erosion risk with very high amounts', []),
    ('Tartaric Acid (E334)', 'Fruit acid from grapes', 'Safe at normal food levels', []),
    ('Fumaric Acid (E297)', 'Acidulant', 'Safe at approved food levels', []),

    # ── Safe Cosmetic Fatty Alcohols & Esters ──
    ('Cetyl Alcohol', 'Fatty alcohol emollient/emulsifier', 'Not an intoxicating alcohol; skin conditioner; safe; non-irritating', []),
    ('Cetearyl Alcohol', 'Fatty alcohol emollient', 'Safe; moisturising; non-irritating; well-tolerated', []),
    ('Stearyl Alcohol', 'Fatty alcohol emollient', 'Safe emollient; skin-softening; no concerns', []),
    ('Behenyl Alcohol', 'Fatty alcohol conditioner', 'Safe; smoothing; used in hair care', []),
    ('Stearic Acid', 'Fatty acid emollient', 'Skin-identical; safe; solidifying agent', []),
    ('Palmitic Acid', 'Fatty acid emollient', 'Naturally abundant in skin; safe', []),
    ('Caprylic / Capric Triglyceride (MCT)', 'Lightweight emollient from coconut', 'Non-comedogenic; safe; derived from coconut/palm kernel', []),
    ('Isopropyl Myristate', 'Lightweight emollient', 'Safe; some reports of comedogenicity in susceptible skin', []),
    ('Cetyl Esters', 'Emollient', 'Plant-derived wax ester; safe', []),

    # ── Sunscreen Actives (safe mineral) ──
    ('Zinc Oxide (micronised, non-nano)', 'Mineral broad-spectrum sunscreen', 'Safest UV filter; FDA Category I (GRAS); non-toxic; good for sensitive skin', []),
    ('Titanium Dioxide (micronised, non-nano)', 'Mineral UVB sunscreen', 'Safe in non-nano form; FDA Category I (GRAS); does not penetrate intact skin', []),

    # ── Safe Miscellaneous Ingredients ──
    ('Glycerin / Glycerol (E422)', 'Humectant / solvent', 'Safe; moisturising; non-irritating; natural by-product of soap making', []),
    ('Sodium Hyaluronate (salt of HA)', 'Humectant / hydrator', 'Smaller than HA — penetrates slightly better; safe; skin-identical', []),
    ('Betaine (from sugar beet)', 'Humectant / hair conditioner', 'Safe; naturally derived; moisturising; gentle', []),
    ('Trehalose', 'Natural stabilizer / humectant', 'Safe; naturally occurring in many organisms; moisturising', []),
    ('Inositol', 'B-vitamin related compound', 'Naturally occurring; safe at normal food and cosmetic doses', []),
    ('Lactic Acid Culture / Bifidus', 'Probiotic bacteria', 'Beneficial; safe', []),
    ('Natural Vanilla Extract', 'Flavouring', 'Safe; antioxidant; natural', []),
    ('Natural Fruit Extracts (general)', 'Flavour / antioxidant', 'Generally safe from natural fruit sources', []),
    ('Rice Bran Extract', 'Antioxidant / moisturising', 'Rich in gamma-oryzanol; safe; antioxidant', []),
    ('Zinc Gluconate', 'Zinc supplement / anti-acne', 'Safe at normal doses; anti-inflammatory for acne', []),
    ('Boswellia / Frankincense Extract', 'Anti-inflammatory Ayurvedic resin', 'Well-studied; safe at normal doses; anti-inflammatory', []),
    ('Peppermint Oil (diluted)', 'Cooling / antimicrobial essential oil', 'Safe at 1-5%; cooling sensation; unsafe undiluted or near infants\' faces', []),
    ('Clove Oil (diluted)', 'Antimicrobial / analgesic essential oil', 'Safe diluted in oral care (eugenol); antimicrobial', []),
    ('Eucalyptus Oil (diluted)', 'Decongestant / antimicrobial', 'Safe diluted; unsafe near infants under 2; avoid ingestion', []),
    ('Activated Charcoal (food grade)', 'Detoxifying / cleansing', 'Safe topically; orally may absorb medications — separate by 2 hours', []),
    ('Aquaxyl (Xylitylglucoside)', 'Novel moisturising active', 'Derived from xylitol and glucose; safe; well-tolerated', []),
    ('Phytosphingosine', 'Skin-identical ceramide precursor', 'Natural skin component; safe; anti-bacterial and anti-inflammatory', []),
    ('Madecassoside (from Centella Asiatica)', 'Wound healing / anti-inflammatory', 'Well-studied; safe; particularly good for sensitive/redness-prone skin', []),
    ('Asiaticoside (from Centella Asiatica)', 'Collagen synthesis / wound healing', 'Well-studied safety; promotes collagen production', []),
    ('Bakuchiol', 'Natural retinol alternative', 'Safe in pregnancy; clinically comparable to retinol for wrinkles; non-irritating', []),

    # ── Superfoods & Nutraceuticals ──
    ('Spirulina (Arthrospira platensis)', 'Blue-green algae superfood supplement', 'Excellent protein and B12 source; safe at recommended doses; avoid if on blood thinners or immunosuppressants', []),
    ('Chlorella', 'Green algae detox supplement', 'Rich in chlorophyll; safe; may bind to heavy metals and medications — separate from medications', []),
    ('Omega-3 Fatty Acids (EPA/DHA from fish oil)', 'Essential fatty acid supplement', 'Cardioprotective; anti-inflammatory; safe; high doses may increase bleeding time — monitor with anticoagulants', []),
    ('CoQ10 (Ubiquinone / Ubiquinol)', 'Mitochondrial antioxidant / anti-aging', 'Safe and well-studied; may reduce effectiveness of warfarin at high doses; beneficial for heart health', []),
    ('Resveratrol (from red grapes/berries)', 'Polyphenol antioxidant', 'Anti-aging; anti-inflammatory; safe at food levels; very high supplement doses interact with blood thinners', []),
    ('Quercetin', 'Flavonoid antioxidant (found in onions, apples)', 'Potent anti-inflammatory; antihistamine properties; safe at food levels; high supplements may interact with medications', []),
    ('Vitamin B12 (Cyanocobalamin)', 'Essential vitamin for nerve function', 'Safe at all recommended doses; critically important for vegetarians/vegans; no known toxicity', []),
    ('Grape Seed Extract (OPC)', 'Oligomeric proanthocyanidins antioxidant', 'Potent antioxidant; anti-inflammatory; safe; may interact with blood thinners at high doses', []),
    ('Blueberry Extract / Anthocyanins', 'Polyphenol antioxidant', 'Antioxidant-rich; anti-inflammatory; safe; beneficial for cognitive health', []),

    # ── Safe Food Starches & Thickeners ──
    ('Tapioca Starch (native)', 'Gluten-free starch from cassava', 'Safe; gluten-free; digestible; widely used in Indian snacks (sabudana)', []),
    ('Corn Starch (native / unmodified)', 'Natural food starch', 'Safe; gluten-free; common thickener; high GI but fine at normal amounts', []),
    ('Arrowroot Starch', 'Natural starch from Maranta arundinacea', 'Easily digestible; safe; traditional use; gentle on the stomach', []),
    ('Potato Starch', 'Natural starch', 'Safe; resistant starch (when cooled) feeds beneficial gut bacteria', []),
    ('Sodium Bicarbonate (baking soda, cooking use)', 'Leavening agent', 'Safe at baking amounts; neutralises acids; no concerns at culinary levels', []),
    ('Potassium Chloride (E508)', 'Salt substitute / mineral', 'Safe at dietary levels; useful low-sodium salt substitute; metallic taste at high amounts', []),

    # ── Safe Botanical Extracts ──
    ('Sea Kelp / Brown Seaweed Extract', 'Iodine-rich marine botanical', 'Rich in iodine and minerals; safe at normal use; excess iodine can affect thyroid', []),
    ('Bamboo Extract / Bamboo Silica', 'Silica-rich plant extract', 'High natural silica; supports hair and nail strength; safe', []),
    ('Sunflower Lecithin', 'Non-GMO emulsifier from sunflower', 'Soy-free emulsifier; safe for soy-sensitive individuals; no concerns', []),
    ('Oat Kernel Oil', 'Emollient from oats', 'Rich in beta-glucan and fatty acids; safe for eczema-prone and sensitive skin; non-comedogenic', []),
    ('Glutathione', 'Master antioxidant / skin brightener', 'Safe topically and in food supplements at recommended doses; powerful cellular antioxidant; safe', []),
    ('Piperine (from Black Pepper)', 'Bioavailability enhancer (Bioperine)', 'Significantly enhances absorption of curcumin, vitamins, and medications; safe at normal use', []),
    ('Melatonin (in functional foods / supplements)', 'Sleep hormone / antioxidant', 'Safe at low doses (0.5-3mg); regulates sleep; powerful antioxidant; avoid high chronic doses', []),
],
}

# Verify counts
total = sum(len(v) for v in INGREDIENTS.values())
print(f"Total ingredients in database: {total}")
cq = len(INGREDIENTS['commonly_questioned'])
wk = len(INGREDIENTS['worth_knowing'])
gr = len(INGREDIENTS['generally_recognised'])
print(f"  Commonly Questioned: {cq}")
print(f"  Worth Knowing: {wk}")
print(f"  Generally Recognised: {gr}")

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=1.3*cm, rightMargin=1.3*cm,
    topMargin=2*cm, bottomMargin=2*cm
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle('title', fontSize=20, fontName='Helvetica-Bold',
    textColor=colors.HexColor('#FF9933'), alignment=TA_CENTER, spaceAfter=4)
subtitle_style = ParagraphStyle('subtitle', fontSize=10, fontName='Helvetica',
    textColor=colors.HexColor('#555555'), alignment=TA_CENTER, spaceAfter=2)
date_style = ParagraphStyle('date', fontSize=9, fontName='Helvetica',
    textColor=colors.HexColor('#888888'), alignment=TA_CENTER, spaceAfter=14)
cat_style = ParagraphStyle('cat', fontSize=12, fontName='Helvetica-Bold',
    textColor=colors.white, alignment=TA_LEFT)
footer_style = ParagraphStyle('footer', fontSize=8, fontName='Helvetica',
    textColor=colors.HexColor('#999999'), alignment=TA_CENTER)

CAT_CONFIG = {
    'commonly_questioned': ('#dc2626', f'COMMONLY QUESTIONED — {cq} Ingredients (Red Flag)'),
    'worth_knowing': ('#b45309', f'WORTH KNOWING — {wk} Ingredients (Caution)'),
    'generally_recognised': ('#16a34a', f'GENERALLY RECOGNISED — {gr} Ingredients (Safe)'),
}

story = []

story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("CheckKaro", title_style))
story.append(Paragraph(f"Complete Ingredient Classification Database — {total} Ingredients", subtitle_style))
story.append(Paragraph("Food | Cosmetics | Personal Care | Nutraceuticals", subtitle_style))
story.append(Paragraph("Sources: FSSAI · EFSA · FDA · WHO/IARC · EU Regulations · Codex Alimentarius | checkkaro.in", date_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#FF9933'), spaceAfter=16))

# Legend
legend_data = [
    [Paragraph('<b>CLASSIFICATION KEY</b>', ParagraphStyle('lh', fontSize=9, fontName='Helvetica-Bold', textColor=colors.HexColor('#333333'))),
     Paragraph('<font color="#dc2626"><b>COMMONLY QUESTIONED</b></font> — Regulatory bans/restrictions or well-documented health risks in scientific literature',
               ParagraphStyle('lc', fontSize=8, fontName='Helvetica')),
     Paragraph('<font color="#b45309"><b>WORTH KNOWING</b></font> — Permitted but with considerations at high intake or for sensitive individuals',
               ParagraphStyle('lc', fontSize=8, fontName='Helvetica')),
     Paragraph('<font color="#16a34a"><b>GENERALLY RECOGNISED</b></font> — No notable regulatory concerns at normal use levels',
               ParagraphStyle('lc', fontSize=8, fontName='Helvetica')),
    ]
]
leg_tbl = Table([legend_data[0]], colWidths=[3*cm, 5.6*cm, 5.2*cm, 4.6*cm])
leg_tbl.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f9f9f9')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e5e7eb')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story.append(leg_tbl)
story.append(Spacer(1, 14))

sno = 1
for cat_key in ['commonly_questioned', 'worth_knowing', 'generally_recognised']:
    items = INGREDIENTS[cat_key]
    header_color, cat_label = CAT_CONFIG[cat_key]

    cat_table = Table(
        [[Paragraph(f"  {cat_label}", cat_style)]],
        colWidths=[17.4*cm]
    )
    cat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0D1B2A')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(cat_table)
    story.append(Spacer(1, 3))

    header = [
        Paragraph('<b>#</b>', ParagraphStyle('th', fontSize=7.5, fontName='Helvetica-Bold', textColor=colors.white)),
        Paragraph('<b>Ingredient Name</b>', ParagraphStyle('th', fontSize=7.5, fontName='Helvetica-Bold', textColor=colors.white)),
        Paragraph('<b>Type / Function</b>', ParagraphStyle('th', fontSize=7.5, fontName='Helvetica-Bold', textColor=colors.white)),
        Paragraph('<b>Key Health Concern</b>', ParagraphStyle('th', fontSize=7.5, fontName='Helvetica-Bold', textColor=colors.white)),
        Paragraph('<b>Banned / Restricted In</b>', ParagraphStyle('th', fontSize=7.5, fontName='Helvetica-Bold', textColor=colors.white)),
    ]

    rows = [header]
    for i, (name, type_, concern, countries) in enumerate(items):
        country_text = ', '.join(countries) if countries else '—'
        rows.append([
            Paragraph(str(sno), ParagraphStyle('cell', fontSize=7, fontName='Helvetica', textColor=colors.HexColor('#888888'))),
            Paragraph(f'<b>{name}</b>', ParagraphStyle('cell', fontSize=7.5, fontName='Helvetica-Bold')),
            Paragraph(type_, ParagraphStyle('cell', fontSize=7, fontName='Helvetica', textColor=colors.HexColor('#444444'))),
            Paragraph(concern, ParagraphStyle('cell', fontSize=7, fontName='Helvetica')),
            Paragraph(country_text, ParagraphStyle('cell', fontSize=6.5, fontName='Helvetica',
                textColor=colors.HexColor('#dc2626') if countries else colors.HexColor('#999999'))),
        ])
        sno += 1

    tbl = Table(rows, colWidths=[0.6*cm, 3.7*cm, 2.9*cm, 5.5*cm, 4.7*cm])
    style_cmds = [
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(header_color)),
        ('GRID', (0,0), (-1,-1), 0.25, colors.HexColor('#e5e7eb')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]
    for i in range(1, len(rows)):
        bg = colors.HexColor('#fafafa') if i % 2 == 1 else colors.white
        style_cmds.append(('BACKGROUND', (0,i), (-1,i), bg))

    tbl.setStyle(TableStyle(style_cmds))
    story.append(tbl)
    story.append(Spacer(1, 14))

story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e5e7eb'), spaceBefore=8))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "CheckKaro Ingredient Database | Data sourced from FSSAI (India), EFSA (EU), FDA (USA), WHO/IARC, "
    "EU Cosmetics Regulation 1223/2009, EU Food Additives Regulation 1333/2008, Codex Alimentarius. "
    "For general awareness only — not medical advice. Regulatory status may change. | checkkaro.in",
    footer_style
))

doc.build(story)
print(f"\nPDF saved: {OUTPUT}")
print(f"Total ingredients in PDF: {sno - 1}")
