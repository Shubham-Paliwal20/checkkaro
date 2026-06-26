"""
Add 30 Shesha Ayurveda products to ai_extracted_products.
"""
import sys, os, re
sys.path.insert(0, 'backend')
from dotenv import load_dotenv
load_dotenv('backend/.env')
from supabase import create_client
from routes.ingredient_database import classify_ingredient, INGREDIENT_DESCRIPTIONS

SUPABASE_URL = os.environ['SUPABASE_URL']
SERVICE_KEY  = os.environ['SUPABASE_SERVICE_ROLE_KEY']
sb = create_client(SUPABASE_URL, SERVICE_KEY)

CDN = "https://sheshaayurveda.com/cdn/shop/files/"

# ── helpers ───────────────────────────────────────────────────────────────────

def parse_ingredients(raw: str):
    parts, depth, cur = [], 0, ""
    for ch in raw:
        if ch == '(': depth += 1; cur += ch
        elif ch == ')': depth -= 1; cur += ch
        elif ch == ',' and depth == 0:
            p = cur.strip().rstrip('.')
            if p: parts.append(p)
            cur = ""
        else: cur += ch
    if cur.strip(): parts.append(cur.strip().rstrip('.'))
    return parts

def classify_one(name: str) -> dict:
    try:
        cls = classify_ingredient(name)
        if not isinstance(cls, str):
            cls = cls.get('classification', 'generally_recognised')
    except Exception:
        cls = 'generally_recognised'
    key = name.lower().strip()
    raw_desc = (INGREDIENT_DESCRIPTIONS.get(key) or
                INGREDIENT_DESCRIPTIONS.get(re.sub(r'\s*\(.*?\)', '', key).strip()))
    desc = raw_desc if isinstance(raw_desc, dict) else {}
    return {
        "name": name, "aliases": desc.get('aliases', ''), "classification": cls,
        "one_line_note": desc.get('one_line_note', ''), "regulatory_note": desc.get('regulatory_note', ''),
        "commonly_found_in": desc.get('commonly_found_in'), "health_effects": desc.get('health_effects'),
        "countries_restricted": desc.get('countries_restricted', []),
        "fssai_position": desc.get('fssai_position'), "recommendation": desc.get('recommendation'),
    }

def compute_grade(classified):
    if not classified: return "B"
    total = len(classified)
    q = sum(1 for i in classified if i['classification'] == 'commonly_questioned')
    w = sum(1 for i in classified if i['classification'] == 'worth_knowing')
    if q > 0: return "D"
    if w == 0: return "A"
    return "B" if w / total <= 0.30 else "C"

def make_static_key(name: str) -> str:
    return re.sub(r'[^a-z0-9]', '', name.lower())

def make_summary(name, brand, grade, q, w, total):
    if grade == "A":
        return f"{name} by {brand} scores Grade A. All {total} ingredients are generally recognised as safe."
    elif grade == "B":
        return f"{name} by {brand} scores Grade B. {total} ingredients analysed; {w} worth knowing about, no restricted additives."
    elif grade == "C":
        return f"{name} by {brand} scores Grade C. Contains {w} worth-knowing ingredients (>30% of total). Use with awareness."
    else:
        return f"{name} by {brand} scores Grade D. Contains {q} commonly questioned ingredient(s) flagged in some countries."

FSSAI_MAP = {
    "Haircare":        "Hair care products regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
    "Hair Colour":     "Hair colour products regulated under Cosmetics Rules 2020. Patch test recommended.",
    "Skincare":        "Cosmetics regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
    "Ayurvedic Oil":   "Ayurvedic formulations licensed under Drugs and Cosmetics Act 1940 (Schedule E). GMP compliant.",
    "Lip Care":        "Lip care products regulated as cosmetics under Cosmetics Rules 2020.",
    "Body Care":       "Body care products regulated under Cosmetics Rules 2020. Ingredient labelling mandatory.",
    "Wellness":        "Ayurvedic therapeutic oils licensed under Drugs and Cosmetics Act 1940.",
}

# ── product catalogue ─────────────────────────────────────────────────────────
# (name, brand, category, ingredients_raw, image_url)

PRODUCTS = [
    # ── HAIR CARE ──
    (
        "Shesha Ayurveda Neeli Bringadi Hair Oil", "Shesha Ayurveda", "Haircare",
        "Indigofera Tinctoria, Eclipta Alba, Cardiospermum Halicacabum, Emblica Officinalis, "
        "Cocos Nucifera Milk, Cow's Milk, Goat's Milk, Buffalo's Milk, "
        "Glycyrrhiza Glabra, Abrus Precatorius, Berberis Species Extract, "
        "Cocos Nucifera Virgin Coconut Oil",
        CDN + "Ayurvedic_Neelibringadi_hair_oil_for_reducing_hair_fall_and_promoting_new_hair_growth.png?v=1770449339",
    ),
    (
        "Shesha Ayurveda Bhringa Thali Ayurvedic Shampoo", "Shesha Ayurveda", "Haircare",
        "Eclipta Alba Hassk, Hibiscus Rosa Sinensis, Acacia Concinna, Lawsonia Inermis, "
        "Aloe Barbadensis, Piper Betle, Ocimum Sanctum, Nigella Sativa, "
        "Terminalia Chebula, Terminalia Belerica, Emblica Officinalis, "
        "Coco-Glucoside, Galguard Trident",
        CDN + "Ayurvedic_shampoo_with_Reetha_Amla_and_Hibiscus_for_deep_cleansing_and_volume.jpg?v=1775215268",
    ),
    (
        "Shesha Ayurveda Bhringa Thali Hair Conditioner", "Shesha Ayurveda", "Haircare",
        "Cocos Nucifera Oil, Eclipta Alba Hassk, Glycerin, Aloe Barbadensis, "
        "Olea Europaea Olive Oil, Hibiscus Rosa Sinensis, Crocus Sativus, "
        "Aqua, Cetearyl Alcohol, Behentriamonium Chloride, Tocopherol, "
        "Cetrimonium Chloride, D-Panthenol, Plant Keratin, Capryl Capric Triglyceride, "
        "Olea Europaea Oil, Disodium EDTA, Glyceryl Monostearate, "
        "Sodium Benzoate, Potassium Sorbate",
        CDN + "BhringaThaliHairConditionersulphatefreeparabenfreesiliconefreegentleAyurvedicconditioner.png?v=1775043152",
    ),
    (
        "Shesha Ayurveda Root Touch Up Hair Powder", "Shesha Ayurveda", "Haircare",
        "Talc, Iron Oxide Black, Zinc Stearate, Magnesium Stearate, "
        "Caprylic/Capric Triglyceride, Dimethicone/Vinyl Dimethicone Crosspolymer, "
        "Sodium Hyaluronate",
        CDN + "SheshaAyurvedaroottouchuphairpowdernaturalblack4gwithapplicator.jpg?v=1767453771",
    ),
    # ── HAIR COLOUR ──
    (
        "Shesha Ayurveda Nilini Hair Color Natural Black", "Shesha Ayurveda", "Hair Colour",
        "Indigofera Tinctoria, Lawsonia Inermis, Cocos Nucifera, Centella Asiatica, "
        "Aloe Barbadensis, Emblica Officinalis, Eclipta Alba, Hibiscus Rosa-Sinensis, "
        "Himalayan Pink Salt, Musa Paradisica, Camellia Sinensis, Nigella Sativa, "
        "Punica Granatum, Terminalia Belerica, Moringa Oleifera, Nelumbo Nucifera, "
        "Acacia Concinna, Vetiveria Zizanioides, Abrus Precatorius, Piper Betle, "
        "Azadirachta Indica, Sesamum Indicum Nigrum, Vitex Negundo, "
        "Murraya Koenigii, Ocimum Tenuiflorum",
        CDN + "NILINI_hair_color_-_best_natural_black_hair_color-min.jpg?v=1763450002",
    ),
    (
        "Shesha Ayurveda Beard Colour Natural Black", "Shesha Ayurveda", "Hair Colour",
        "Indigofera Tinctoria, Lawsonia Inermis, Cocos Nucifera, Centella Asiatica, "
        "Aloe Barbadensis, Emblica Officinalis, Eclipta Alba, Hibiscus Rosa-Sinensis, "
        "Acacia Concinna, Vetiveria Zizanioides, Abrus Precatorius, Ocimum Tenuiflorum, "
        "Camellia Sinensis, Himalayan Pink Salt, Musa Paradisica, Nigella Sativa, "
        "Punica Granatum, Terminalia Belerica, Moringa Oleifera, Azadirachta Indica, "
        "Sesamum Indicum Nigrum, Vitex Negundo",
        CDN + "shesha-ayurveda-beard-color-indias-best-beard-color.jpg?v=1740811993",
    ),
    # ── AYURVEDIC SKIN OILS ──
    (
        "Shesha Ayurveda Kumkumadi Thailam", "Shesha Ayurveda", "Skincare",
        "Vetiveria Zizanioides, Coscinium Fenestratum, Lacca Laccifera, "
        "Glycyrrhiza Glabra, Santalum Album, Ficus Bengalensis, Prunus Cerasoides, "
        "Nelumbo Nucifera, Monochoria Vaginalis, Rubia Cordifolia, Lacca Laccifera, "
        "Caesalpinia Sappan, Glycyrrhiza Glabra, Crocus Sativus, "
        "Goat's Milk, Sesamum Indicum Seed Oil",
        CDN + "shesha_ayurveda_skin_brightening_saffron_oil.jpg?v=1775239746",
    ),
    (
        "Shesha Ayurveda Nalpamaradi Thailam", "Shesha Ayurveda", "Skincare",
        "Curcuma Longa, Fumaria Parviflora, Sesamum Indicum Seed Oil, "
        "Ficus Bengalensis Bark, Ficus Racemosa Bark, Ficus Religiosa Bark, "
        "Ficus Lacor Bark, Terminalia Chebula, Emblica Officinalis, "
        "Terminalia Bellerica, Pterocarpus Santalinus, Vetiveria Zizanioides, "
        "Inula Racemosa, Rubia Cordifolia, Kaempferia Galanga, Aquilaria Agallocha",
        CDN + "nalpamaradi_thailam_50_ml.png?v=1719138343",
    ),
    (
        "Shesha Ayurveda Eladi Thailam", "Shesha Ayurveda", "Ayurvedic Oil",
        "Pterocarpus Marsupium, Aegle Marmelos, Sida Cordifolia, Tinospora Cordifolia, "
        "Elettaria Cardamomum, Amomum Subulatum, Boswellia Serrata, Inula Racemosa, "
        "Callicarpa Macrophylla, Coleus Vettiveroides, Actiniopteris Radiata, "
        "Cymbopogon Martini, Curcuma Zedoaria, Cinnamomum Zeylanicum, "
        "Cinnamomum Tamala, Valeriana Wallichii, Taxus Baccata, Myristica Fragrans, "
        "Commiphora Myrrha, Ostrea Edulis, Martynia Annua, Cedrus Deodara, "
        "Ventilago Maderaspatana, Pinus Longifolia, Costus Speciosus, "
        "Commiphora Wightii, Shorea Robusta, Acacia Catechu, Celastrus Paniculatus, "
        "Mesua Ferrea, Nardostachys Jatamansi, Coconut Milk, "
        "Sesamum Indicum Seed Oil, Crocus Sativus, Cinnamomum Camphora",
        CDN + "Eladi-thailam-dry-skin-massage-oil-02.png?v=1768293171",
    ),
    # ── WELLNESS OILS ──
    (
        "Shesha Ayurveda Dhanwantaram Thailam", "Shesha Ayurveda", "Wellness",
        "Sida Cordifolia, Desmodium Gangeticum, Pseudarthria Viscida, Aerva Lanata, "
        "Solanum Indicum, Gmelina Arborea, Aegle Marmelos, Stereospermum Suaveolens, "
        "Oroxylum Indicum, Premna Mucronata, Tribulus Terrestris, Hordeum Vulgare, "
        "Ziziphus Jujuba, Dolichos Biflorus, Polygonatum Cirrhifolium, "
        "Polygonatum Verticillatum, Cedrus Deodara, Rubia Cordifolia, "
        "Lilium Polyphyllum, Asparagus Adscendens, Santalum Album, "
        "Hemidesmus Indicus, Inula Racemosa, Valeriana Wallichii, "
        "Microstylis Wallichii, Microstylis Muscifera, Rock Salt, Milk, "
        "Trigonella Foenum-Graecum, Withania Somnifera, Asparagus Racemosus, "
        "Ipomoea Paniculata, Glycyrrhiza Glabra, Terminalia Chebula, "
        "Emblica Officinalis, Terminalia Bellerica, Commiphora Myrrha, "
        "Peucedanum Graveolens, Teramnus Labialis, Phaseolus Trilobus, "
        "Elettaria Cardamomum, Cinnamomum Zeylanicum, Cinnamomum Tamala, "
        "Sesamum Indicum Seed Oil",
        CDN + "Dhanwantaram_Post-Partum-massage-oil-01.png?v=1719574669",
    ),
    (
        "Shesha Ayurveda Karpooradi Thailam", "Shesha Ayurveda", "Wellness",
        "Cinnamomum Camphora, Sesamum Indicum Seed Oil",
        CDN + "karpooradi-thailam-pain-relief-massage-oil-01.png?v=1719575159",
    ),
    (
        "Shesha Ayurveda Balaswagandhadi Thailam", "Shesha Ayurveda", "Wellness",
        "Sida Cordifolia, Withania Somnifera, Laccifer Lacca, Curd, "
        "Sesamum Indicum Seed Oil, Alpinia Galanga, Santalum Album, "
        "Rubia Cordifolia, Cynodon Dactylon, Glycyrrhiza Glabra, "
        "Hedychium Spicatum, Hemidesmus Indicus, Vetiveria Zizanioides, "
        "Cyperus Rotundus, Inula Racemosa, Aquilaria Agallocha, Cedrus Deodara, "
        "Berberis Aristata, Nymphaea Alba, Vitex Negundo, "
        "Anethum Sowa, Nelumbo Nucifera",
        CDN + "Balaswagandhadi__001.png?v=1719574426",
    ),
    (
        "Shesha Ayurveda Kottamchukkadi Pain Relief Thailam", "Shesha Ayurveda", "Wellness",
        "Tamarindus Indica, Inula Racemosa, Zingiber Officinale, Acorus Calamus, "
        "Moringa Oleifera, Allium Sativum, Hugonia Mystax, Cedrus Deodara, "
        "Brassica Campestris, Alpinia Galanga, Azadirachta Indica Oil, "
        "Ricinus Communis Oil, Sesamum Indicum Oil",
        CDN + "kottamchukkadi-pain-relief-thailam-01.png?v=1719576712",
    ),
    (
        "Shesha Ayurveda Murivenna Pain Relief Oil", "Shesha Ayurveda", "Wellness",
        "Pongamia Pinnata, Aloe Barbadensis, Piper Betle, Moringa Oleifera, "
        "Erythrina Indica, Allium Oschaninii, Spermacoce Articularis, "
        "Asparagus Racemosus, Cocos Nucifera Oil",
        CDN + "murivenna-pain-relief-oil-01.png?v=1719578068",
    ),
    (
        "Shesha Ayurveda Lakshadi Baby Massage Oil", "Shesha Ayurveda", "Wellness",
        "Lacca Laccifera, Sesamum Indicum Seed Oil, Withania Somnifera, "
        "Curcuma Longa, Cedrus Deodara, Vitex Negundo, Inula Racemosa, "
        "Curd, Cyperus Rotundus, Santalum Album, Marsdenia Tenacissima, "
        "Picrorhiza Kurroa, Pluchea Lanceolata, Anethum Sowa, Glycyrrhiza Glabra",
        CDN + "lakshadi_thailam_skin_brightening_and_muscle_recovery_and_body_toning_oil_shesha_ayurveda.jpg?v=1774775701",
    ),
    # ── SKINCARE ──
    (
        "Shesha Ayurveda Red Sandalwood Face Wash", "Shesha Ayurveda", "Skincare",
        "Pterocarpus Santalinus, Citrus Aurantifolia, Rosa Damascena, "
        "Azadirachta Indica, Crocus Sativus, Camellia Sinensis, Tamarindus Indica, "
        "Bakuchiol, Niacinamide, Sodium Hyaluronate, Aqua, "
        "Sodium Lauroyl Sarcosinate, Acrylates Copolymer, Cocamidopropyl Betaine, "
        "Decyl Glucoside, Xylitylglucoside, Allantoin, Sodium Hydroxide, "
        "Sodium PCA, Phenoxyethanol, Pentylene Glycol, Coco Monoethanolamide",
        CDN + "Red_Sandalwood_Skin_Brightening_face_wash_3.png?v=1719126793",
    ),
    (
        "Shesha Ayurveda Red Sandalwood Night Repair Cream", "Shesha Ayurveda", "Skincare",
        "Pterocarpus Santalinus, Kumkumadi Thailam, Cocos Nucifera Virgin Coconut Oil, "
        "Prunus Dulcis Almond Oil, Simmondsia Chinensis Jojoba Oil, "
        "Hydnocarpus Wightianus Chaulmoogra Oil, Vitis Vinifera Grapeseed Oil, "
        "Azadirachta Indica Neem Oil, Lavandula Lavender Oil, "
        "Chrysopogon Zizanioides Vetiver Oil, Curcuma Longa Turmeric Extract, "
        "Alpinia Galanga Oil, Acorus Calamus Oil, Pelargonium Graveolens Geranium Oil, "
        "DM Water, Glyceryl Monostearate, Emulsifying Wax, Glycerin, "
        "Stearic Acid, Citric Acid, Phenoxyethanol, Tocopherol",
        CDN + "red_sandalwood_cream_shesha_ayurveda_1.png?v=1778162538",
    ),
    (
        "Shesha Ayurveda Kumkumadi Brightening Day Cream", "Shesha Ayurveda", "Skincare",
        "Aloe Barbadensis Leaf Extract, Kumkumadi Thailam, Ricinus Communis Castor Oil, "
        "Glycerin, 2-Hydroxyethyl Methacrylate, Coco-Glucoside, Polysorbate 80, "
        "Sodium Benzoate, Potassium Sorbate, Phenoxyethanol, Citric Acid, Deionized Water",
        CDN + "shesha_ayurveda_skin_brightening_day_cream_texture.webp?v=1778389680",
    ),
    (
        "Shesha Ayurveda Kumkumadi Suvarna Ubtan", "Shesha Ayurveda", "Skincare",
        "Crocus Sativus, Hibiscus Rosa-Sinensis, Nelumbo Nucifera, "
        "Pterocarpus Santalinus, Rosa Damascena, Aloe Barbadensis Dried, "
        "Prunus Dulcis, Myristica Fragrans, Cassia Auriculata, "
        "Ocimum Tenuiflorum, Vigna Radiata, Cicer Arietinum, "
        "Curcuma Zedoaria, Emblica Officinalis, Azadirachta Indica, "
        "Cyperus Rotundus, Curcuma Aromatica",
        CDN + "kumkumadi-suvarna-ubtan-skin-brightening-face-pack-03.png?v=1774515643",
    ),
    (
        "Shesha Ayurveda Yellow Kasturi Manjal Face Pack", "Shesha Ayurveda", "Skincare",
        "Curcuma Zedoaria, Curcuma Aromatica, Orange Peel Powder, "
        "Lemon Peel Powder, Ocimum Tenuiflorum",
        CDN + "wild_turmeric_or_yellow_skin_brightening_kasturi_manjal_shesha_ayurveda.jpg?v=1747207111",
    ),
    (
        "Shesha Ayurveda Kasturi Manjal Musk Turmeric Powder", "Shesha Ayurveda", "Skincare",
        "Curcuma Aromatica",
        CDN + "ALTMF-SHSA-SUM-AD-KMYL-WHT-01-min.jpg?v=1747207234",
    ),
    (
        "Shesha Ayurveda Multani Mitti Facial Ubtan", "Shesha Ayurveda", "Skincare",
        "Solum Fullonum",
        CDN + "multani-mitti-square-1_1.png?v=1766909232",
    ),
    # ── LIP CARE ──
    (
        "Shesha Ayurveda Kumkumadi Lip Balm", "Shesha Ayurveda", "Lip Care",
        "Kumkumadi Thailam, Theobroma Cacao Cocoa Butter, Mangifera Indica Mango Butter, "
        "Helianthus Annuus Sunflower Oil, Prunus Dulcis Almond Oil, "
        "Cocos Nucifera Virgin Coconut Oil, Ricinus Communis Castor Oil, "
        "Rubia Cordifolia Manjistha, Glycyrrhiza Glabra Licorice Extract, "
        "Psoralea Corylifolia Babchi Seed Extract, Tocopherol, "
        "Crocus Sativus Saffron Essential Oil, Pterocarpus Santalinus, Cera Alba",
        CDN + "kumkumadi_lipbalm_shesha_ayurveda.jpg?v=1754641748",
    ),
    # ── BODY & PERSONAL CARE ──
    (
        "Shesha Ayurveda Pure Aloe Vera Gel", "Shesha Ayurveda", "Body Care",
        "Aloe Barbadensis Leaf Juice, Xanthan Gum, Guar Gum, "
        "Benzyl Alcohol, Salicylic Acid, Glycerin, Sorbic Acid",
        CDN + "pure-aloe-vera-gel_0002_Layer203.jpg?v=1712786485",
    ),
    (
        "Shesha Ayurveda Pure Rose Water", "Shesha Ayurveda", "Body Care",
        "Rosa Damascena Flower Water",
        CDN + "shesha_ayurveda_pure_rose_water.png?v=1750929241",
    ),
    (
        "Shesha Ayurveda Kasturi Turmeric Vetiver Shower Gel", "Shesha Ayurveda", "Body Care",
        "Aloe Barbadensis Leaf Extract, Chrysopogon Zizanioides Vetiver Oil, "
        "Curcuma Aromatica, Curcuma Zedoaria, Curcuma Longa, Glycerine, Citric Acid, "
        "DM Water, CI 15985, Capryl Glucoside, Coco-Glucoside, "
        "Cocamidopropyl Betaine, Sodium Methyl Cocoyl Taurate, "
        "Methylchloroisothiazolinone, Methylisothiazolinone",
        CDN + "kasturi_vetiver_shower_gel.webp?v=1778268284",
    ),
    (
        "Shesha Ayurveda Mud with Nalpamaradi Soap", "Shesha Ayurveda", "Body Care",
        "Solum Fullonum Multani Mitti, Cocos Nucifera Oil, Curcuma Longa, "
        "Aloe Barbadensis, Nigella Sativa, Cynodon Dactylon, Ficus Lacor, "
        "Ficus Racemosa, Punica Granatum, Ficus Bengalensis, Ficus Religiosa, "
        "Piper Betle, Cymbopogon Citratus, Sodium Hydroxide",
        CDN + "shesha_ayurveda_mud_skin_brightening_soap.jpg?v=1750919913",
    ),
    (
        "Shesha Ayurveda Extra Virgin Coconut Oil", "Shesha Ayurveda", "Body Care",
        "Cocos Nucifera Extra Virgin Coconut Oil",
        CDN + "co2001_1.jpg?v=1715779030",
    ),
    (
        "Shesha Ayurveda Nargis Deodorant Body Mist", "Shesha Ayurveda", "Body Care",
        "DM Water, Aloe Barbadensis Leaf Extract, Narcissus Poeticus Flower Oil, "
        "Butyrospermum Parkii Shea Butter, Denatured Ethanol, Tocopherol, Menthol",
        CDN + "sheshaayurvedanargisdeodorantbodymist3.png?v=1761375536",
    ),
    (
        "Shesha Ayurveda Parijatham Deodorant Body Mist", "Shesha Ayurveda", "Body Care",
        "DM Water, Aloe Barbadensis Leaf Extract, Nyctanthes Arbor-Tristis Flower Extract, "
        "Butyrospermum Parkii Shea Butter, Denatured Ethanol, Tocopherol, Menthol",
        CDN + "shesha_ayurveda_body_mist_parijat.jpg?v=1734160568",
    ),
]

# ── insertion ─────────────────────────────────────────────────────────────────

def already_exists(name: str) -> bool:
    res = sb.table('ai_extracted_products').select('id').ilike('name', name).limit(1).execute()
    return bool(res.data)

def insert_product(name, brand, category, ingredients_raw, image_url):
    print(f"\n[{name}]")
    if already_exists(name):
        print("  SKIP — already in database")
        return False

    ing_names  = parse_ingredients(ingredients_raw)
    classified = [classify_one(n) for n in ing_names]
    grade      = compute_grade(classified)
    q = sum(1 for i in classified if i['classification'] == 'commonly_questioned')
    w = sum(1 for i in classified if i['classification'] == 'worth_knowing')
    total = len(classified)
    print(f"  Grade={grade}  questioned={q}  worth={w}  total={total}")

    fssai_note = FSSAI_MAP.get(category, "Regulated under Cosmetics Rules 2020.")
    verdict = (f"Contains {q} restricted/flagged ingredient(s)." if q else
               f"Contains {w} ingredient(s) worth monitoring." if w else
               "All ingredients are generally safe.")
    recommendation = ("Avoid or use sparingly — contains commonly questioned ingredients." if q else
                      "Use with awareness — some additives worth monitoring." if w else
                      "Safe to use — no concerning ingredients detected.")
    awareness_score = max(0, 100 - (q * 25) - (w * 8))

    record = {
        "name":            name,
        "brand":           brand,
        "category":        category,
        "grade":           grade,
        "ingredients_raw": ingredients_raw,
        "ingredients":     classified,
        "image_url":       image_url,
        "static_key":      make_static_key(name),
        "summary":         make_summary(name, brand, grade, q, w, total),
        "fssai_note":      fssai_note,
        "verdict":         verdict,
        "recommendation":  recommendation,
        "awareness_score": awareness_score,
        "status":          "approved",
    }
    try:
        res = sb.table('ai_extracted_products').insert(record).execute()
        print(f"  INSERTED (id: {res.data[0]['id'][:8]}...)")
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return None

def main():
    print(f"Inserting {len(PRODUCTS)} Shesha Ayurveda products...\n")
    added = skipped = failed = 0
    for p in PRODUCTS:
        r = insert_product(*p)
        if r is True:    added += 1
        elif r is False: skipped += 1
        else:            failed += 1
    print(f"\n{'='*60}")
    print(f"Done.  Added: {added}  |  Skipped: {skipped}  |  Failed: {failed}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
