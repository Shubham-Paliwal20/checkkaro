"""
Add 27 Avimee Herbal products to ai_extracted_products.
Images use official Avimee CDN URLs (no scraping needed).
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
        return f"{name} by {brand} scores Grade A. All {total} ingredients are generally recognised as safe with no concerning additives detected."
    elif grade == "B":
        return f"{name} by {brand} scores Grade B. {total} ingredients analysed; {w} are worth knowing about but no restricted additives found."
    elif grade == "C":
        return f"{name} by {brand} scores Grade C. Contains {w} worth-knowing ingredients (>30% of total). Use with awareness."
    else:
        return f"{name} by {brand} scores Grade D. Contains {q} commonly questioned ingredient(s) that are restricted or flagged in some countries."

FSSAI_MAP = {
    "Haircare":           "Hair care products are regulated under the Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020. Ingredient labelling is mandatory. Active claims must be substantiated.",
    "Face Wash":          "Regulated under Cosmetics Rules 2020. Surfactants like SLS and SLES are permitted. Preservative concentrations must meet BIS standards.",
    "Skincare":           "Cosmetics are regulated under the Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020. Ingredient labelling is mandatory.",
    "Serums":             "Face serums are regulated as cosmetics under Cosmetics Rules 2020. Active ingredient concentrations should match label claims.",
    "Sunscreen":          "Sunscreens are classified as cosmetics under Drugs & Cosmetics Act. SPF values must be validated per ISO 24444.",
    "Health Supplements": "Health supplements are regulated under the Food Safety and Standards (Health Supplements, Nutraceuticals, Food for Special Dietary Use, Food for Special Medical Purpose, Functional Food and Novel Food) Regulations, 2022 by FSSAI.",
}

# ── product catalogue ─────────────────────────────────────────────────────────
# (name, brand, category, variant, net_wt, ingredients_raw, image_url)

CDN = "https://avimeeherbal.com/cdn/shop/files/"

PRODUCTS = [
    # ── HAIR OILS ──────────────────────────────────────────────────────────────
    (
        "Avimee Herbal Keshpallav Hair Oil", "Avimee Herbal", "Haircare", "Hair Growth Oil", "100 ml",
        "Nansyl, Sunflower Seed Oil, Pumpkin Seed Oil, Coconut MCT Oil, Black Sesame Seed Oil, "
        "Flax Seed Oil, Amla Oil, Bhringraj Oil, Brahmi Oil, Hibiscus Oil, Curry Leaf Oil, "
        "Saw Palmetto Oil, Camellia Seed Oil, Pecan Nut Oil, Soyabean Oil, Macadamia Nut Oil, "
        "Marula Oil, Walnut Oil, Mustard Seed Oil, Castor Oil, Arnica Oil, Almond Oil, "
        "Apricot Kernel Oil, Cucumber Oil, Pomegranate Seed Oil, Shea Oil, Malkangni Oil, "
        "Karanja Oil, Wheat Grass Oil, Bergamot Oil, Cedarwood Oil, Stinging Nettle Oil, "
        "Bottle Gourd Oil, Borage Seed Oil, Bakuchi Oil, Bamboo Oil, Wheat Germ Oil, Halim Oil, "
        "Plum Kernel Oil, Avocado Oil, Carrot Oil, Grapeseed Oil, Hazel Nut Oil, Passion Fruit Oil, "
        "Clary Sage Oil, Tea Tree Oil, Birch Oil, Argan Oil, Clove Oil, Rosemary Oil, Jojoba Oil, "
        "Tamanu Oil, Lemongrass Oil, Lavender Oil, Eucalyptus Oil, Helichrysum Oil, Myrrh Oil, "
        "Nutmeg Oil, Ylang Ylang Oil, Kalonji Oil",
        CDN + "1_ea13a123-3a1c-4e51-9c67-b4b015e1390b.png?v=1776662994&width=1000",
    ),
    (
        "Avimee Herbal Keshpallav Plus Daily Hair Oil", "Avimee Herbal", "Haircare", "Daily Hair Oil", "100 ml",
        "Coconut MCT Oil, Sunflower Seed Oil, Pumpkin Seed Oil, Cold Pressed Coconut Oil, "
        "Black Sesame Seed Oil, Flax Seed Oil, Amla Oil, Bhringraj Oil, Brahmi Oil, Hibiscus Oil, "
        "Curry Leaf Oil, Saw Palmetto Oil, Camellia Seed Oil, Pecan Nut Oil, Soybean Oil, "
        "Macadamia Nut Oil, Marula Oil, Walnut Oil, Mustard Seed Oil, Castor Oil, Arnica Oil, "
        "Almond Oil, Apricot Kernel Oil, Cucumber Oil, Pomegranate Seed Oil, Shea Oil, "
        "Malkangni Oil, Karanja Oil, Wheat Grass Oil, Bergamot Oil, Cedarwood Oil, Stinging Nettle Oil, "
        "Bottle Gourd Oil, Borage Seed Oil, Bakuchi Oil, Bamboo Oil, Wheat Germ Oil, Halim Oil, "
        "Plum Kernel Oil, Avocado Oil, Carrot Oil, Grapeseed Oil, Hazel Nut Oil, Passion Fruit Oil, "
        "Clary Sage Oil, Tea Tree Oil, Birch Oil, Argan Oil, Clove Oil, Rosemary Oil, Jojoba Oil, "
        "Tamanu Oil, Lemongrass Oil, Lavender Oil, Eucalyptus Oil, Helichrysum Oil, Myrrh Oil, "
        "Nutmeg Oil, Ylang Ylang Oil, Kalonji Oil",
        CDN + "1_53008127-fc08-44d6-9d6a-5d2a694d9bb7.png?v=1781776488&width=1000",
    ),
    (
        "Avimee Herbal Keshkrishna Grey Hair Oil", "Avimee Herbal", "Haircare", "Anti-Grey Hair Oil", "100 ml",
        "Melaina, Henna Oil, Cassia Obovata Oil, Indigo Oil, Amla Oil, Catechu Oil, "
        "Curry Leaves Oil, Manjistha Oil, Hibiscus Oil, Black Tea Oil, Spinach Oil, Shikakai, "
        "Amaranthus Oil, Black Coffee Oil, Dalchini Oil, Jatamansi Oil, Bhringraj Oil, "
        "Wheatgrass Oil, Pineapple Oil, Watermelon Oil, Sweet Potato Oil, Pomegranate Peel Oil, "
        "Carrot Oil, Beet Root Oil, Kalonji Oil, BHT",
        CDN + "fran_faf185ea-c5c7-4e09-a081-bc07b385db36.png?v=1743850444&width=1000",
    ),
    (
        "Avimee Herbal Rosemary Hair Oil", "Avimee Herbal", "Haircare", "Rosemary Hair Growth Oil", "100 ml",
        "Rosemary Oil Extract, Rosemary Essential Oil, Pumpkin Seed Oil, Chia Seed Oil, "
        "Flax Seed Oil, Jatamansi Oil, Pomegranate Seed Oil, Neem Oil Extract, Amla Oil Extract, "
        "Curry Leaves Oil Extract, Methidana Oil Extract, Bhringraj Oil Extract, Brahmi Oil Extract, "
        "Punarnava Oil Extract, Onion Oil Extract, Coconut Oil, Mushroom Oil Extract, "
        "Clove Oil, Sandal Oil, Tempus, Grapeseed Oil, BHT",
        CDN + "1_602faf76-ef48-4fc3-aaf4-2fa257c2b7de.png?v=1776683771&width=1000",
    ),
    (
        "Avimee Herbal Maha Bhringraj Hair Oil", "Avimee Herbal", "Haircare", "Bhringraj Hair Oil", "100 ml",
        "Shweta Bhringraj Oil, Neel Bhringraj Oil, Peet Bhringraj Oil, Brahmi Oil, Mandukparni Oil, "
        "Coconut Oil, BHT",
        CDN + "1_07a8a5e1-27e1-48dc-946d-83caa37be3bb.png?v=1777019118&width=1000",
    ),
    (
        "Avimee Herbal Javakusum Hibiscus Hair Oil", "Avimee Herbal", "Haircare", "Hibiscus Hair Oil", "100 ml",
        "Hibiscus Flower Oil Soluble Extract, Hibiscus Leaves Oil Soluble Extract, Coconut Oil, "
        "Hibiscus Flower Essential Oil, Grape Seed Oil, Pomegranate Seed Oil, Lotus Seeds Oil, "
        "Jatamansi Seeds Oil, Saw Palmetto Oil, Curry Leaves Oil, Amla Oil, Green Tea Oil, "
        "Lotus Petal Oil, Pumpkin Seeds Oil, Nettle Leaves Oil, Spinach Oil, Vitamin E, Vitamin B12",
        CDN + "1_b66a73bc-e40e-4602-a6f6-499d0b5f5596.png?v=1781777676&width=1000",
    ),
    (
        "Avimee Herbal Pure Amla Hair Oil", "Avimee Herbal", "Haircare", "Pure Amla Oil", "100 ml",
        "Amla Fruit Oil, Amla Seed Oil, Acerola Fruit Oil, Kakadu Plum Oil, Orange Peel Oil, "
        "Vitamin E, BHT",
        CDN + "1_18cfb30e-1f66-446a-b3e0-f94b2ac9f200.png?v=1777019013&width=1000",
    ),
    (
        "Avimee Herbal Cold Pressed Castor Oil", "Avimee Herbal", "Haircare", "Cold Pressed Castor Oil", "200 ml",
        "Castor Oil, Vitamin E",
        CDN + "1_c83907ba-4c38-44c5-ada9-72350466e0d4.png?v=1777018935&width=1000",
    ),
    (
        "Avimee Herbal Extra Virgin Coconut Oil", "Avimee Herbal", "Haircare", "Extra Virgin Coconut Oil", "200 ml",
        "Extra Virgin Coconut Oil, Vitamin E",
        CDN + "1_8_ba503cbd-21dd-4370-ac74-4c620bd8fc20.png",
    ),

    # ── HAIR SERUMS & SPRAY ────────────────────────────────────────────────────
    (
        "Avimee Herbal Scalptone Hair Growth Serum", "Avimee Herbal", "Haircare", "Hair Growth Serum 5% Nansyl", "25 ml",
        "Nansyl, Aloe Vera Juice, Pomegranate Extract, Green Tea Extract, Grapeseed Extract, "
        "Ashwagandha Extract, Jatamansi Extract, Bala Extract, Pea Sprout Extract, "
        "Olive Leaf Extract, Sodium Gluconate, 2-Phenoxyethanol, Ethylhexylglycerin, DM Water",
        CDN + "1_3d8c7e36-d2e9-4b06-b0a5-3367733b0a09.png?v=1775636150&width=1000",
    ),
    (
        "Avimee Herbal Scalptone Dandruff Serum", "Avimee Herbal", "Haircare", "Anti-Dandruff Scalp Serum", "25 ml",
        "Nilscurf, Aloe Vera Juice, Caffeine, Black Tea Extract, Zinc PCA, Niacinamide, "
        "Hyaluronic Acid, Piperine, Eugenol, Cinnamaldehyde, Bacoside, Asiaticoside, "
        "Sodium Hydroxide, Sodium Gluconate, Fragrance, 2-Phenoxyethanol, Ethylhexyl Glycerin, DM Water",
        CDN + "1_08e59c36-fc46-4753-9b87-9d975ec9d827.png?v=1781774701&width=1000",
    ),
    (
        "Avimee Herbal Scalptone Grey Hair Serum", "Avimee Herbal", "Haircare", "Anti-Grey Hair Serum", "25 ml",
        "Melaina, Aloe Vera Juice, Acetyl Tyrosine, Hyaluronic Acid, Catalase, Melanin, "
        "Epigallocatechin-3-Gallate, Caffeine, Apple Cider Vinegar, Sodium Gluconate, "
        "2-Phenoxyethanol, Ethylhexyl Glycerin, Fragrance, DM Water",
        CDN + "1_ba653fb2-cdcb-40df-badf-063c7b17ad88.png?v=1781774971&width=1000",
    ),
    (
        "Avimee Herbal Hair Tonic PV1 Scalp Spray", "Avimee Herbal", "Haircare", "DHT Blocker Scalp Spray", "100 ml",
        "Coiffure, Tempus, Arnica Extract, Jaborandi Extract, Saw Palmetto Extract, "
        "Amla Extract, Bhringraj Extract, Methi Daana Extract, Harad Extract, Baheda Extract",
        CDN + "1_85a1bbc0-1390-419c-95f6-286f3644d19d.png?v=1761578224&width=1000",
    ),

    # ── SHAMPOOS & CONDITIONER ─────────────────────────────────────────────────
    (
        "Avimee Herbal Shakuntala Daily Use Hair Cleanser", "Avimee Herbal", "Haircare", "Daily Hair Cleanser Shampoo", "200 ml",
        "Coconut Water, Sodium Lauryl Sarcosinate, Decyl Glucoside, Aloe Vera Juice, "
        "Tempus, Sodium PCA, Polyquaternium-7, Cetrimonium Chloride, PEG-150 Distearate, "
        "Betaine, Glycolic Acid, Dipropylene Glycol, Polysilicone-29, D-Panthenol, "
        "Ethylene Glycol Monostearate, IFRA Certified Fragrance, 2-Phenoxyethanol, "
        "Ethyl Hexyl Glycerin, Polyquaternium-10, Guar Hydroxy Trimonium Chloride, "
        "Clove Oil, Argan Oil, Hydrolyzed Keratin Protein, Onion Oil, Tea Tree Oil, Sodium Gluconate",
        CDN + "1_b92d688f-2ec3-49c9-8a1f-bfcb1f614686.png?v=1781773834&width=1000",
    ),
    (
        "Avimee Herbal Sakshi Hair Shampoo", "Avimee Herbal", "Haircare", "Deep Cleansing Shampoo", "200 ml",
        "Decyl Glucoside, Coco Glucoside, Aloe Vera Juice, Almond Oil, Coconut Water, "
        "Apple Cider Vinegar, SLS, Keratin Protein, Natural Fragrance, Aloe Vera Powder 200x, "
        "Guar Gum, EGMS, PQ 10, Saw Palmetto Extract, Soapnut Extract, Neem Oil, "
        "Sodium Benzoate, Rice Protein, Vitamin E, Green Coffee Derivative, Argan Oil, "
        "Tea Tree Oil, DM Water",
        CDN + "frantimage_1f93b20d-80f2-43a3-88cf-b513238f2c11.png?v=1733213651&width=1000",
    ),
    (
        "Avimee Herbal Radha Hair Conditioner", "Avimee Herbal", "Haircare", "Keratin Repair Conditioner", "200 ml",
        "Aloe Vera Juice, Curd, Milk, Corn Starch, Castor Oil, Almond Oil, "
        "Sodium Lauryl Sarcosinate, Keratin Powder, Veg Glycerine, Rice Maad, Coconut Water, "
        "Emulsifying Wax, Cetyl Alcohol, Rice Protein, Hibiscus Water, Green Tea Water, "
        "Guar Gum, Polyquaternium 10, Apple Cider Vinegar, D-Panthenol, Tea Tree Oil, "
        "Whey Protein, Argan Oil, Merquat 3330, Fragrance, Red Onion Seed Powder, "
        "Sandal Water, Aloe Vera Powder 200x, Potassium Sorbate, Potato Juice, Apple Juice, "
        "Papaya Juice, Carrot Juice, Tomato Juice, Vitamin E, DM Water",
        CDN + "1_9b986cd2-399e-4e46-8d2f-b68ad52134d4.png?v=1781787830&width=1000",
    ),

    # ── SKINCARE ───────────────────────────────────────────────────────────────
    (
        "Avimee Herbal Pure Aloe Vera Gel", "Avimee Herbal", "Skincare", "Pure Aloe Vera Gel", "100 ml",
        "Aloe Vera Juice, Aloe Vera Powder 200X, Sodium Benzoate, Potassium Sorbate",
        CDN + "frantimage_b71fe5ff-bb30-4e66-80e7-53e0177d088f.png?v=1708752599&width=1000",
    ),
    (
        "Avimee Herbal Gulabo Pure Rose Water", "Avimee Herbal", "Skincare", "Pure Rose Water Hydrosol", "110 ml",
        "Rose Distillate, Rose Oil, Glucan P 20 Humectant",
        CDN + "01_a16fc329-1313-4936-801e-27ce6c7b336c.png?v=1740064605&width=1000",
    ),

    # ── FACE WASHES ────────────────────────────────────────────────────────────
    (
        "Avimee Herbal Kunwar Charcoal Face Wash", "Avimee Herbal", "Face Wash", "Activated Charcoal Face Wash", "50 ml",
        "Decyl Glucoside, Aloe Vera Juice, Coco Glucoside, Sodium Lauryl Sarcosinate, "
        "Pomegranate Extract, Carrot Extract, Propolis Extract, Lemon Extract, Apple Extract, "
        "Dragon Fruit Extract, Coconut Water, Beet Root Extract, PEG 150 Distearate, "
        "Carbomer 940, Triethanolamine, Spinach Extract, Neem Extract, Aloe Vera Powder 200x, "
        "Activated Charcoal, Curcumin Extract, Citric Acid, Tea Tree Oil, "
        "Sodium Benzoate, Potassium Sorbate, DM Water",
        CDN + "1_9fec05f1-8529-4482-87b3-2ad099bee014.png?v=1740645873&width=1000",
    ),
    (
        "Avimee Herbal Vitamin C Face Wash", "Avimee Herbal", "Face Wash", "Vitamin C Brightening Face Wash", "100 ml",
        "Coco Apple Amino Acid, Ascorbic Acid, Disodium Cocoamphoacetate, Coco Amino Propyl Betaine, "
        "Aloe Vera Juice, Acerola Fruit Extract, Kakadu Plum Extract, Kiwi Extract, "
        "Orange Peel Extract, Amla Extract, Pineapple Extract, Rose Water, Red Sandal Extract, "
        "Niacinamide, Hyaluronic Acid, Beet Root Extract, Cucumber Extract, Manjistha Extract, "
        "Green Tea Extract, Neem Water, Red Sandal Water, Tween 80, Fragrance, "
        "Potassium Sorbate, DM Water",
        CDN + "1_17605c5c-0285-40ca-8bfa-8529dd67f804.png?v=1713160901&width=1000",
    ),
    (
        "Avimee Herbal Salicylic Acid Face Wash", "Avimee Herbal", "Face Wash", "Salicylic Acid Acne Face Wash", "100 ml",
        "Coco Apple Amino Acid, Disodium Cocoamphoacetate, Coco Amino Propyl Betaine, "
        "Salix Alba Extract, Filipendula Ulmaria Extract, Betula Lenta Extract, "
        "Gaultheria Procumbens Extract, Spirea Extract, Watermelon Extract, Cucurbita Pepo Extract, "
        "Salicylic Acid, Aloe Vera Juice, Hyaluronic Acid, PEG 7 Glyceryl Cocoate, Rose Water, "
        "Allantoin, Glycolic Acid, 2-Phenoxyethanol, Ethylhexyl Glycerin, Polysorbate 80, "
        "PEG-40 Hydrogenated Castor Oil, Glycerin, 1,3-Propanediol, Sodium Gluconate, "
        "Fragrance, DM Water",
        CDN + "1_a34ac65b-a24b-419f-8a29-fc7ac85dd595.png?v=1713161609&width=1000",
    ),
    (
        "Avimee Herbal Niacinamide Face Wash", "Avimee Herbal", "Face Wash", "Niacinamide Pore Control Face Wash", "100 ml",
        "Coco Apple Amino Acid, Niacinamide, Aloe Vera Juice, Disodium Cocoamphoacetate, "
        "Coco Amino Propyl Betaine, Sodium PCA, Zinc PCA, PEG 7 Glyceryl Cocoate, "
        "Seabuckthorn Extract, Cinnamon Extract, Rosemary Extract, Tomato Extract, "
        "Tea Tree Extract, Eucalyptus Extract, Lemongrass Extract, Neem Extract, Honey, "
        "Ascorbic Acid, Tween 80, Perfume, Potassium Sorbate, Vitamin E, "
        "Sodium Gluconate, Fragrance, DM Water",
        CDN + "1_32f04551-3238-4799-9809-fa2e4e8d07d6.jpg",
    ),

    # ── FACE SERUMS ────────────────────────────────────────────────────────────
    (
        "Avimee Herbal Vitamin C Face Serum", "Avimee Herbal", "Serums", "Vitamin C Brightening Face Serum", "25 ml",
        "Ascorbic Acid, Aloe Vera Juice, Acerola Fruit Extract, Kakadu Plum Extract, "
        "Kiwi Extract, Orange Peel Extract, Amla Extract, Sodium PCA, Pineapple Extract, "
        "Rose Water, Niacinamide, Hyaluronic Acid, Beet Root Extract, Cucumber Extract, "
        "Manjistha Extract, Green Tea Extract, Neem Water, Red Sandal Water, "
        "Tween 80, Fragrance, Potassium Sorbate, DM Water",
        CDN + "1_103e0c1c-6f25-49b6-b7a9-65db8dc268b9.png?v=1781775079&width=1000",
    ),
    (
        "Avimee Herbal Salicylic Acid Face Serum", "Avimee Herbal", "Serums", "Salicylic Acid Blemish Serum", "25 ml",
        "Salix Alba Extract, Filipendula Ulmaria Extract, Betula Lenta Extract, "
        "Gaultheria Procumbens Extract, Spirea Extract, Watermelon Extract, Cucurbita Pepo Extract, "
        "Salicylic Acid, Aloe Vera Juice, Hyaluronic Acid, Hydroxyethyl Cellulose, Rose Water, "
        "Allantoin, Glycolic Acid, 2-Phenoxyethanol, Ethylhexyl Glycerin, Polysorbate 80, "
        "PEG-40 Hydrogenated Castor Oil, Glycerin, 1,3-Propanediol, Sodium Gluconate, "
        "Fragrance, DM Water",
        CDN + "1_a7b871e0-9013-4ebe-ad32-86b0039e39e7.png?v=1781775626&width=1000",
    ),
    (
        "Avimee Herbal Niacinamide Face Serum", "Avimee Herbal", "Serums", "Niacinamide Glow Serum", "25 ml",
        "DM Water, Aloe Vera Juice, Niacinamide, Haldi Extract, Sea Buckthorn Extract, "
        "Cinnamon Extract, Rosemary Extract, Tomato Extract, Tea Tree Extract, Matmarine, "
        "Eucalyptus Extract, Lemongrass Extract, Neem Extract, Honey, Ascorbic Acid, "
        "Tween 80, Perfume, Potassium Sorbate, Hyaluronic Acid",
        CDN + "1_2c4cb5bc-4c70-4d7c-a038-16ac051e5dfa.png?v=1781775320&width=1000",
    ),

    # ── SUNSCREEN ──────────────────────────────────────────────────────────────
    (
        "Avimee Herbal Soorya Kawach SPF 50 Sunscreen", "Avimee Herbal", "Sunscreen", "SPF 50 PA++++ Sunscreen", "50 ml",
        "DM Water, Octocrylene, Octyl Methoxy Cinnamate, Aloe Vera Juice, Octyl Salicylate, "
        "Zinc Oxide, De-tan Extract, Isopropyl Myristate, Polyglyceryl-2 Stearate, "
        "Glyceryl Stearate, Stearyl Alcohol, Cetostearyl Alcohol, Emulsifying Wax, Betaine, "
        "Hyaluronic Acid, Allantoin, IFRA Certified Fragrance, Sapt Beej Oil, "
        "Vitamin E, 2-Phenoxyethanol, Potassium Sorbate, Sodium Gluconate",
        CDN + "1_f6577cbf-72d1-4cae-b7a8-a629e54c73fe.png?v=1715593416&width=1000",
    ),

    # ── HEALTH ─────────────────────────────────────────────────────────────────
    (
        "Avimee Herbal Keshmadhu Hair Growth Capsule", "Avimee Herbal", "Health Supplements", "Biotin Hair Growth Capsule", "60 Capsules",
        "Sesbania Extract, Curry Leaves Extract, Indrajaw Extract, Basil Extract, "
        "Lemon Peel Extract, Amla Extract, Hadjod Extract, Moringa Extract, Bamboo Extract, "
        "Shilajit Extract, Bhringraj Extract, Mandukparni Extract, Brahmi Extract, "
        "Jatamansi Extract, Black Sesame Seed Powder, Sweet Potato Extract, Grapeseed Extract, "
        "Ashwagandha Extract, Soya Extract, Lichen Extract, Chlorella Extract, Vanslochan, "
        "Guava Extract, Sage Leaves Extract, Stinging Nettle Leaves Extract, "
        "Spirulina Extract, Saw Palmetto Extract, Ginseng Extract",
        CDN + "2_e9303c6d-a051-4418-82ad-42c9237ce3cc.png?v=1741611221&width=1000",
    ),
]

# ── insertion ─────────────────────────────────────────────────────────────────

def already_exists(name: str) -> bool:
    res = sb.table('ai_extracted_products').select('id').ilike('name', name).limit(1).execute()
    return bool(res.data)

def insert_product(name, brand, category, variant, net_wt, ingredients_raw, image_url):
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

    fssai_note = FSSAI_MAP.get(category, "Regulated under the Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.")
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
    print(f"Inserting {len(PRODUCTS)} Avimee Herbal products...\n")
    added = skipped = failed = 0
    for p in PRODUCTS:
        r = insert_product(*p)
        if r is True:   added += 1
        elif r is False: skipped += 1
        else:            failed += 1
    print(f"\n{'='*55}")
    print(f"Done.  Added: {added}  |  Skipped: {skipped}  |  Failed: {failed}")
    print(f"{'='*55}")

if __name__ == "__main__":
    main()
