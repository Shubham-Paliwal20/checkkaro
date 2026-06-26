"""
Add 23 The Moms Co. products to ai_extracted_products.
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

IMG = "https://incidecoder-content.storage.googleapis.com"

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
    "Skincare":  "Cosmetics regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
    "Haircare":  "Hair care products regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
    "Sunscreen": "Sunscreens regulated under Schedule Q of Drugs and Cosmetics Act 1940. SPF claims must be substantiated.",
    "Baby Care": "Baby cosmetics regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020. Stricter safety norms apply.",
}

# ── catalogue ─────────────────────────────────────────────────────────────────

PRODUCTS = [
    # ── FACE WASHES ──
    (
        "The Moms Co. Natural Vitamin C Face Wash",
        "The Moms Co.", "Skincare",
        "Purified Water, Decyl Glucoside, Aloe Vera Leaf Juice, Glycerin, "
        "Sodium Cocoamphoacetate, Lauryl Glucoside, Sodium Cocoyl Glutamate, "
        "Sodium Lauryl Glucose Carboxylate, Heptyl Glucoside, Sodium PCA, "
        "Xylitylglucoside, Anhydroxylitol, Xylitol, Dehydroxanthan Gum, "
        "3-O-Ethyl Ascorbic Acid, Orange Peel Powder, "
        "Epilobium Angustifolium Flower/Leaf/Stem Extract, Panthenol, "
        "Orange Oil, Litsea Cubeba Oil, Lemon Oil, "
        "PCA Ethyl Cocoyl Arginate, Sodium Gluconate",
        IMG + "/647f45a3-3296-4dea-bd58-8bb5ad61424f/products/"
              "the-moms-co-natural-vitamin-c-face-wash/"
              "the-moms-co-natural-vitamin-c-face-wash_front_photo_original.jpeg",
    ),
    (
        "The Moms Co. Natural Clay Face Wash",
        "The Moms Co.", "Skincare",
        "Aqua, Alanine, Allantoin, Aloe Vera Juice, Arginine, Arachidyl Alcohol, "
        "Arachidyl Glucoside, Charcoal Powder, Erythritol, Solum Fullonum, "
        "Glutamic Acid, Glycerin, Glycine, Glycyrrhiza Glabra Extract, "
        "Hydroxyethyl Cellulose, Kaolin, Lauryl Glucoside, Lysine Hydrochloride, "
        "Moroccan Ghassoul Lava Clay, Niacinamide, Orchid Essential Oil, "
        "Patchouli Essential Oil, PCA, Peppermint Oil, Proline, Propanediol, "
        "Saccharide Isomerate, Serine, Silica, Sodium Citrate, "
        "Sodium Cocoamphoacetate, Sodium Cocoyl Glutamate, "
        "Sodium Cocoyl Isethionate, Sodium Lactate, "
        "Sodium Lauryl Glucose Carboxylate, Sodium PCA, Sorbitol, "
        "Sugar Maple Extract, Sugarcane Extract, Threonine, Titanium Dioxide, "
        "Tocopherol, Vaccinium Myrtillus Fruit Extract, Xanthan Gum, Zinc Oxide",
        IMG + "/00ad6e71-c5e2-42a2-9333-ac686bb6cfa5/products/"
              "the-moms-co-the-moms-co-natural-clay-face-wash-with-moroccan-lava-clay-activated-charcoal-l-purifies-detoxes-brightens-l-normal-to-oily-skin/"
              "the-moms-co-the-moms-co-natural-clay-face-wash-with-moroccan-lava-clay-activated-charcoal-l-purifies-detoxes-brightens-l-normal-to-oily-skin_front_photo_original.jpeg",
    ),
    (
        "The Moms Co. Natural Vita Rich Face Wash",
        "The Moms Co.", "Skincare",
        "Purified Water, Glycerin, Sodium Cocoamphoacetate, Lauryl Glucoside, "
        "Sodium Cocoyl Glutamate, Sodium Lauryl Glucose Carboxylate, "
        "Rose Flower Water, Sodium Cocoyl/Olivoyl Hydrolyzed Oat Protein, "
        "Fructosyl Cocoate/Olivate, Fructose, Xylitylglucoside, Anhydroxylitol, "
        "Xylitol, Saccharide Isomerate, Citric Acid, Sodium Citrate, "
        "Caprylhydroxamic Acid, Caprylyl Glycol, Sodium PCA, Wheat Amino Acids, "
        "Panthenol, Sodium Hyaluronate, Hydroxyproline, Xanthan Gum, Niacinamide, "
        "Betaine, Bergamot Essential Oil, Mandarin Essential Oil, "
        "Patchouli Essential Oil, Lemon Essential Oil, Organic Neem Leaf Extract, "
        "Witch Hazel Extract, Sodium Gluconate, 3-O-Ethyl Ascorbic Acid",
        IMG + "/8a56df8c-b451-4731-8178-f9d65baa5da7/products/"
              "the-moms-co-natural-vita-rich-face-wash/"
              "the-moms-co-natural-vita-rich-face-wash_front_photo_original.jpeg",
    ),
    # ── FACE SERUMS ──
    (
        "The Moms Co. Natural 10% Vitamin C Face Serum",
        "The Moms Co.", "Skincare",
        "Purified Water, 3-O-Ethyl Ascorbic Acid, Pentylene Glycol, Niacinamide, "
        "Sodium Levulinate, Sodium Sorbate, Xylitylglucoside, Anhydroxylitol, "
        "Xylitol, Glycerin, Panax Ginseng Root Extract, Ferulic Acid, "
        "Glycyrrhiza Glabra Root Extract, Citrus Reticulata Peel Oil, Pinene, "
        "Citrus Sinensis Peel Oil, Dehydroxanthan Gum, Citric Acid",
        IMG + "/62be037e-a13d-4ba6-aa63-35641f9668ad/products/"
              "the-moms-co-natural-10-vitamin-c-face-serum/"
              "the-moms-co-natural-10-vitamin-c-face-serum_front_photo_original.jpeg",
    ),
    (
        "The Moms Co. Natural Vita Rich Face Serum",
        "The Moms Co.", "Skincare",
        "Purified Water, C12-15 Alkyl Benzoate, Xanthan Gum, Lecithin, "
        "Sclerotium Gum, Pullulan, Isoamyl Laurate, Argania Spinosa Kernel Oil, "
        "Methylpropanediol, Saccharide Isomerate, Citric Acid, Sodium Citrate, "
        "Propanediol, Caprylyl Glycol, Niacinamide, "
        "Phytosteryl Octyldodecyl Lauroyl Glutamate, Salvia Hispanica Seed Oil, "
        "Tocopherol, Oenothera Biennis Oil, Glycerin, "
        "Terminalia Ferdinandiana Fruit Extract, Panthenol, Orange Essential Oil, "
        "Ethylhexylglycerin, Allantoin, Sodium Gluconate, Sodium Hyaluronate",
        IMG + "/c380fdaa-8111-448c-bf0a-ca37097cb58d/products/"
              "the-moms-co-natural-vita-rich-face-serum/"
              "the-moms-co-natural-vita-rich-face-serum_front_photo_original.jpeg",
    ),
    (
        "The Moms Co. Natural Age Control Face Serum",
        "The Moms Co.", "Skincare",
        "Purified Water, Aloe Barbadensis Leaf Juice, Squalane, Niacinamide, "
        "Pentylene Glycol, Isoamyl Laurate, Sodium Levulinate, Potassium Sorbate, "
        "Xanthan Gum, Lecithin, Sclerotium Gum, Pullulan, Xylitylglucoside, "
        "Anhydroxylitol, Xylitol, Glycerin, Heptyl Glucoside, "
        "Epilobium Angustifolium Flower/Leaf/Stem Extract, Bakuchiol, "
        "Sodium Hyaluronate, Hydroxyapatite, Cysteine, Glutathione, "
        "Tocopherol, Lemon Oil, Allantoin, Sodium Gluconate",
        IMG + "/679a431c-904c-4959-8491-92d46cd9ec6c/products/"
              "the-moms-co-natural-age-control-face-serum/"
              "the-moms-co-natural-age-control-face-serum_front_photo_original.jpeg",
    ),
    (
        "The Moms Co. Natural Ceramide Face Serum",
        "The Moms Co.", "Skincare",
        "Purified Water, Pentylene Glycol, Squalane, Glycerin, Ceramide NP, "
        "Rice Water, Xylitylglucoside, Anhydroxylitol, Xylitol, "
        "Aloe Barbadensis Leaf Juice, Sodium Levulinate, Potassium Sorbate, "
        "Sodium Hyaluronate, Niacinamide, Hydroxyapatite, Cysteine, Glutathione, "
        "Isoamyl Laurate, Heptyl Glucoside, Tocopherol, Xanthan Gum, Lecithin, "
        "Sclerotium Gum, Pullulan, Allantoin, Sodium Gluconate",
        IMG + "/b8319b6e-6e42-4d33-865b-461c880ae2d1/products/"
              "the-moms-co-natural-ceramide-face-serum/"
              "the-moms-co-natural-ceramide-face-serum_front_photo_original.jpeg",
    ),
    # ── FACE CREAMS ──
    (
        "The Moms Co. Natural Vitamin C Face Cream",
        "The Moms Co.", "Skincare",
        "Purified Water, Aloe Barbadensis Leaf Juice, Dicaprylyl Carbonate, "
        "Caprylic/Capric Triglyceride, Glycerin, Squalane, Betaine, "
        "Glyceryl Monostearate, Polyglyceryl-2 Stearate, Stearyl Alcohol, "
        "Heptyl Undecylenate, Cetyl Alcohol, Cetostearyl Alcohol, "
        "Hydrogenated Lecithin, C12-16 Alcohols, Palmitic Acid, "
        "Ribes Nigrum Seed Oil, Octyldodecanol, Octyldodecyl Oleate, "
        "Octyldodecyl Stearoyl Stearate, Paeonia Suffruticosa Root Extract, "
        "Rosmarinus Officinalis Leaf Extract, Hydroxyapatite, Cysteine, "
        "Glutathione, Xylitylglucoside, Anhydroxylitol, Xylitol, Sodium PCA, "
        "PCA Ethyl Cocoyl Arginate, Isoamyl Laurate, Saccharide Isomerate, "
        "3-O-Ethyl Ascorbic Acid, Ferulic Acid, "
        "Epilobium Angustifolium Flower/Leaf/Stem Extract, "
        "Aluminium Starch Octenylsuccinate, "
        "Glyceryl Citrate/Lactate/Linoleate/Oleate, "
        "Passiflora Edulis Seed Oil, Tocopherol, Allantoin, "
        "Citrus Reticulata Peel Oil, Pinene, Citrus Sinensis Peel Oil, "
        "Sodium Gluconate",
        IMG + "/789cf560-0b47-46a1-b335-68a3182d9a82/products/"
              "the-moms-co-natural-vitamin-c-face-cream/"
              "the-moms-co-natural-vitamin-c-face-cream_front_photo_original.jpeg",
    ),
    (
        "The Moms Co. Natural Vita Rich Face Cream",
        "The Moms Co.", "Skincare",
        "Aqua, Acetyl Tyrosine, Allantoin, Alpha-Arbutin, "
        "Aminopropyl Ascorbyl Phosphate, Anhydroxylitol, Arbutin, "
        "Argania Spinosa Kernel Oil, C14-22 Alcohols, C12-20 Alkyl Glucoside, "
        "Calophyllum Inophyllum Seed Oil, Caprylhydroxamic Acid, "
        "Caprylic/Capric Triglyceride, Capryloyl Glycerin/Sebacic Acid Copolymer, "
        "Caprylyl Glycol, Cetearyl Alcohol, Cetearyl Glucoside, Citric Acid, "
        "Diheptyl Succinate, Ethylhexylglycerin, Glutathione, Glycerin, "
        "Camellia Sinensis Seed Oil, Isoamyl Laurate, Myristyl Myristate, "
        "Niacinamide, Citrus Sinensis Essential Oil, Citrus Reticulata Essential Oil, "
        "Paeonia Suffruticosa Root Extract, Panthenol, Propanediol, "
        "Rumex Occidentalis Extract, Saccharide Isomerate, Salvia Hispanica Seed Oil, "
        "Saxifraga Sarmentosa Extract, Scutellaria Baicalensis Extract, "
        "Sodium Citrate, Sodium Gluconate, Sodium Hyaluronate, Sorbitan Stearate, "
        "Terminalia Ferdinandiana Fruit Extract, Tocopherol, Xanthan Gum, "
        "Xylitol, Xylitylglucoside",
        IMG + "/62dc7cf3-dd81-4a84-bcb4-02e0adf9a435/products/"
              "the-moms-co-natural-vita-rich-face-cream/"
              "the-moms-co-natural-vita-rich-face-cream_front_photo_original.jpeg",
    ),
    (
        "The Moms Co. Natural Age Control Night Cream",
        "The Moms Co.", "Skincare",
        "Aqua, Sodium Gluconate, Glycerin, Xanthan Gum, Allantoin, "
        "Aloe Barbadensis Leaf Juice, Caprylhydroxamic Acid, Caprylyl Glycol, "
        "Dicaprylyl Carbonate, Caprylic/Capric Triglyceride, Cetostearyl Alcohol, "
        "Glyceryl Monostearate, Heptyl Undecylenate, Hydrogenated Lecithin, "
        "C12-16 Alcohols, Palmitic Acid, Bakuchiol, "
        "Psoralea Corylifolia Seed Extract, Tocopherol, Isoamyl Laurate, "
        "Glyceryl Citrate/Lactate/Linoleate/Oleate, Cucumis Sativus Fruit Extract, "
        "Niacinamide, Hamamelis Virginiana Extract, Hydroxyapatite, Cysteine, "
        "Glutathione, Propylene Glycol, Hesperidin Methyl Chalcone, "
        "Malva Sylvestris Extract, Aesculus Hippocastanum Seed Extract, "
        "Hamamelis Virginiana Leaf Extract, Ruscus Aculeatus Root Extract, "
        "Arnica Montana Flower Extract, Saccharide Isomerate, Sodium Hyaluronate, "
        "Hyaluronic Acid, Prunus Persica Fruit Extract, "
        "Prunus Serrulata Flower Extract, Jasminum Officinale Flower Extract",
        IMG + "/9d8d2438-a2f9-470e-b3fb-11e510cbd6c1/products/"
              "the-moms-co-natural-age-control-night-cream/"
              "the-moms-co-natural-age-control-night-cream_front_photo_original.jpeg",
    ),
    # ── EYE CREAM ──
    (
        "The Moms Co. Natural Vita Rich Under Eye Cream",
        "The Moms Co.", "Skincare",
        "Water, Organic Aloe Barbadensis Leaf Gel, Arachidyl Alcohol, "
        "Arachidyl Glucoside, Organic Butyrospermum Parkii Butter, Behenyl Alcohol, "
        "Caprylhydroxamic Acid, Caprylyl Glycol, Cetostearyl Alcohol, "
        "Caprylic/Capric Triglyceride, Cetearyl Olivate, Coffea Arabica Seed Oil, "
        "Citric Acid, Glycerin, Glyceryl Monostearate, Camellia Sinensis Seed Oil, "
        "Heptyl Undecylenate, Isopropyl Myristate, Citrus Reticulata Essential Oil, "
        "Niacinamide, Citrus Sinensis Essential Oil, Organic Chamomilla Recutita Oil, "
        "Prunus Amygdalus Dulcis Oil, Persea Gratissima Oil, Sodium Gluconate, "
        "Sodium Hyaluronate, Sorbitan Olivate, Organic Simmondsia Chinensis Seed Oil, "
        "Spilanthes Acmella Flower Extract, Salvia Hispanica Seed Oil, Sodium PCA, "
        "Saccharide Isomerate, Sodium Citrate, Tocopherol, Xanthan Gum",
        IMG + "/67bb88f4-2562-405a-8ed5-1bb461e890c0/products/"
              "the-moms-co-natural-vita-rich-under-eye-cream/"
              "the-moms-co-natural-vita-rich-under-eye-cream_front_photo_original.jpeg",
    ),
    # ── TONER ──
    (
        "The Moms Co. Natural Vitamin C Face Toner",
        "The Moms Co.", "Skincare",
        "Ascorbic Acid, Purified Water, Aloe Barbadensis Leaf Juice, Niacinamide, "
        "Citrus Limon Peel Extract, Camellia Sinensis Leaf Extract, "
        "Hamamelis Virginiana Extract, Caprylyl Glycol, "
        "Cupressus Sempervirens Leaf Oil, Glycerin, 3-O-Ethyl Ascorbic Acid, "
        "Vaccinium Myrtillus Fruit Extract, Citrus Aurantium Dulcis Peel Oil, "
        "Saccharum Officinarum Extract, Rosa Damascena Flower Water, "
        "Caprylhydroxamic Acid, Citrus Limon Peel Oil, "
        "Citrus Aurantium Dulcis Extract, Pyrus Malus Fruit Extract, "
        "Jasminum Officinale Extract, Acer Saccharum Extract",
        IMG + "/a8c66ac9-0266-4fba-a0a5-2b1f05d3cd45/products/"
              "the-moms-co-natural-vitamin-c-face-toner/"
              "the-moms-co-natural-vitamin-c-face-toner_front_photo_original.jpeg",
    ),
    # ── ALOE VERA GEL ──
    (
        "The Moms Co. Aloe Vera Gel",
        "The Moms Co.", "Skincare",
        "Purified Water, Aloe Barbadensis Leaf Juice, Sodium PCA, "
        "Sodium Polyglutamate, Xylitylglucoside, Anhydroxylitol, Xylitol, "
        "Trehalose, Pentylene Glycol, Phenethyl Alcohol, Caprylyl Glycol, "
        "Dehydroxanthan Gum, Panthenol, Tocopherol, Glycerin, "
        "Hydroxypropyl Starch Phosphate, Cupressus Sempervirens Leaf Oil, "
        "Citrus Limon Oil, Citrus Sinensis Oil",
        IMG + "/9898d63c-c5c1-43b0-8e43-dc9a9c6fb0e1/products/"
              "the-moms-co-aloe-vera-gel/"
              "the-moms-co-aloe-vera-gel_front_photo_original.jpeg",
    ),
    # ── SUNSCREEN ──
    (
        "The Moms Co. Natural Daily Sunscreen SPF 45+",
        "The Moms Co.", "Sunscreen",
        "Purified Water, Titanium Dioxide, Zinc Oxide, "
        "Caprylic/Capric Triglycerides, Isopropyl Myristate, Undecane, Tridecane, "
        "Polyglyceryl-2 Dipolyhydroxystearate, Glycerin, Coco-Caprylate/Caprate, "
        "Sorbitan Olivate, Pongamia Glabra Seed Oil, Heptyl Undecylenate, "
        "Caprylhydroxamic Acid, Caprylyl Glycol, Organic Olea Europaea Oil, "
        "Vanilla Planifolia Extract, Organic Butyrospermum Parkii Butter, "
        "Lactic Acid, Sodium Gluconate, Tocopherol, "
        "Rubus Idaeus Seed Oil, Organic Daucus Carota Sativa Seed Oil",
        IMG + "/040e77c8-d7ca-4755-b572-20f792382ee0/products/"
              "the-moms-co-natural-daily-sunscreen-spf-45/"
              "the-moms-co-natural-daily-sunscreen-spf-45_front_photo_original.jpeg",
    ),
    # ── HAIR CARE ──
    (
        "The Moms Co. Natural Protein Shampoo",
        "The Moms Co.", "Haircare",
        "Aqua, Sodium Cocoamphoacetate, Glycerin, Lauryl Glucoside, "
        "Sodium Cocoyl Glutamate, Sodium Lauryl Glucose Carboxylate, Coco-Betaine, "
        "Sodium Methyl Oleoyl Taurate, Decyl Glucoside, "
        "Cocodimonium Hydroxypropyl Hydrolyzed Wheat Protein, Citric Acid, "
        "Hydrolyzed Silk, Coco-Glucoside, Glyceryl Oleate, Caprylyl Glycol, "
        "Caprylyl/Capryl Glucoside, Glyceryl Caprylate, Polyglyceryl-6 Oleate, "
        "Sodium Surfactin, Hydrolyzed Corn Starch, Beta Vulgaris Root Extract, "
        "Citrus Aurantium Dulcis Peel Oil, Citrus Aurantium Bergamia Peel Oil, "
        "Panthenol, Xylitylglucoside, Anhydroxylitol, Xylitol, "
        "Saccharide Isomerate, Sodium Citrate, Sodium Gluconate, Potassium Sorbate",
        IMG + "/6268ed12-1a07-4a0f-ae27-999504cf331e/products/"
              "the-moms-co-natural-protein-shampoo/"
              "the-moms-co-natural-protein-shampoo_front_photo_original.jpeg",
    ),
    (
        "The Moms Co. Natural Ka+ Damage Repair Shampoo",
        "The Moms Co.", "Haircare",
        "Purified Water, Sodium Lauroyl Methyl Isethionate, "
        "Sodium Methyl Oleoyl Taurate, Decyl Glucoside, C12-15 Alkyl Benzoate, "
        "Hydrolyzed Keratin, Betaine, Coco-Glucoside, Glyceryl Oleate, "
        "Sorbitan Stearate, Cetearyl Alcohol, Cetearyl Glucoside, Erythritol, "
        "Sodium PCA, Xylitylglucoside, Anhydroxylitol, Maltitol, Xylitol, "
        "Pelvetia Canaliculata Extract, Caprylhydroxamic Acid, Caprylyl Glycol, "
        "Glycerin, Citrus Aurantium Dulcis Peel Oil, "
        "Citrus Aurantium Bergamia Peel Oil, "
        "Trisodium Ethylenediamine Disuccinate, Argania Spinosa Kernel Oil, "
        "Cetyl Alcohol, Saccharide Isomerate, Citric Acid, Sodium Citrate, "
        "Moringa Oleifera Seed Oil, Xanthan Gum",
        IMG + "/7628ad37-4e84-4dd3-9152-d33af902f1c3/products/"
              "the-moms-co-natural-ka-damage-repair-shampoo/"
              "the-moms-co-natural-ka-damage-repair-shampoo_front_photo_original.jpeg",
    ),
    (
        "The Moms Co. Natural Protein Conditioner",
        "The Moms Co.", "Haircare",
        "Aqua, Cetostearyl Alcohol, Cetyl Alcohol, Heptyl Undecylenate, Glycerin, "
        "Stearamidopropyl Dimethylamine, Orbignya Speciosa Kernel Oil, "
        "Astrocaryum Murumuru Seed Butter, Diheptyl Succinate, "
        "Capryloyl Glycerin/Sebacic Acid Copolymer, Sodium Lactate, "
        "Caprylhydroxamic Acid, Caprylyl Glycol, Hydrolyzed Silk, "
        "Cocodimonium Hydroxypropyl Hydrolyzed Wheat Protein, Argania Spinosa Kernel Oil, "
        "Panthenol, Sodium PCA, Citrus Sinensis Peel Oil, "
        "Citrus Aurantium Bergamia Peel Oil, Lactic Acid, Xylitylglucoside, "
        "Anhydroxylitol, Xylitol, Saccharide Isomerate, Citric Acid, Sodium Citrate, "
        "Hydrolyzed Corn Starch, Beta Vulgaris Root Extract, Tocopherol, "
        "Guar Hydroxypropyltrimonium Chloride, Sodium Gluconate",
        IMG + "/abfe39aa-2f65-43d9-aab9-e108538cfd11/products/"
              "the-moms-co-natural-protein-conditioner/"
              "the-moms-co-natural-protein-conditioner_front_photo_original.jpeg",
    ),
    (
        "The Moms Co. Natural Ka+ Damage Repair Hair Conditioner",
        "The Moms Co.", "Haircare",
        "Purified Water, Aloe Vera Extract, Ricinus Communis Seed Oil, "
        "Cetostearyl Alcohol, Cocos Nucifera Oil, Heptyl Undecylenate, "
        "Diheptyl Succinate, Capryloyl Glycerin/Sebacic Acid Copolymer, "
        "Arachidyl Alcohol, Behenyl Alcohol, Arachidyl Glucoside, Glycerin, "
        "Stearamidopropyl Dimethylamine, Hydrolyzed Keratin, Sodium Lactate, "
        "Caprylhydroxamic Acid, Caprylyl Glycol, Butyrospermum Parkii Butter, "
        "Citrus Sinensis Peel Oil, Citrus Aurantium Bergamia Peel Oil, "
        "Argania Spinosa Kernel Oil, Orbignya Speciosa Kernel Oil, "
        "Astrocaryum Murumuru Seed Butter, Panthenol, Xylitylglucoside, "
        "Anhydroxylitol, Xylitol, Lactic Acid, Tocopherol, "
        "Guar Hydroxypropyltrimonium Chloride, Saccharide Isomerate, "
        "Citric Acid, Sodium Citrate, Trisodium Ethylenediamine Disuccinate, "
        "Potassium Sorbate",
        IMG + "/92389c75-fea7-46a6-a863-dd8f40f859ed/products/"
              "the-moms-co-natural-ka-damage-repair-hair-conditioner/"
              "the-moms-co-natural-ka-damage-repair-hair-conditioner_front_photo_original.jpeg",
    ),
    (
        "The Moms Co. Natural Protein Hair Serum",
        "The Moms Co.", "Haircare",
        "Aqua, Diheptyl Succinate, Capryloyl Glycerin/Sebacic Acid Copolymer, "
        "Glycerin, Sodium PCA, Sodium Lactate, Arginine, Aspartic Acid, PCA, "
        "Glycine, Alanine, Serine, Valine, Proline, Threonine, Isoleucine, "
        "Histidine, Phenylalanine, Xanthan Gum, Lecithin, Sclerotium Gum, "
        "Pullulan, Sweet Almond Protein, Sodium Stearate, Sodium Chloride, "
        "Caprylyl Glycol, Sclerocarya Birrea Seed Oil, Argania Spinosa Kernel Oil, "
        "Phytosteryl Octyldodecyl Lauroyl Glutamate, Orange Essential Oil, "
        "Bergamot Essential Oil, Ethylhexylglycerin, "
        "Guar Hydroxypropyltrimonium Chloride, Sodium Gluconate",
        IMG + "/72e45657-cca6-466b-b27e-736837bc832c/products/"
              "the-moms-co-hair-serum/"
              "the-moms-co-hair-serum_front_photo_original.jpeg",
    ),
    # ── BABY CARE ──
    (
        "The Moms Co. Natural Baby Shampoo",
        "The Moms Co.", "Baby Care",
        "Purified Water, Decyl Glucoside, Sodium Cocoamphoacetate, Glycerin, "
        "Betaine, Lauryl Glucoside, Sodium Methyl Cocoyl Taurate, Sodium Chloride, "
        "Sodium Cocoyl Glutamate, Sodium Lauryl Glucose Carboxylate, Caprylyl Glycol, "
        "Citric Acid, Panthenol, Panthenyl Hydroxypropyl Steardimonium Chloride, "
        "Citrus Nobilis Essential Oil, Citrus Grandis Essential Oil, "
        "Citrus Aurantium Dulcis Essential Oil, Coco-Glucoside, Glyceryl Oleate, "
        "Sodium Gluconate, Caprylhydroxamic Acid, Argania Spinosa Kernel Oil",
        IMG + "/646565ac-c302-4bf0-9022-2aba189a66b1/products/"
              "the-moms-co-natural-baby-shampoo/"
              "the-moms-co-natural-baby-shampoo_front_photo_original.jpeg",
    ),
    (
        "The Moms Co. Natural Baby Wash",
        "The Moms Co.", "Baby Care",
        "Purified Water, Decyl Glucoside, Sodium Cocoamphoacetate, Glycerin, "
        "Lauryl Glucoside, Sodium Methyl Cocoyl Taurate, Xylitylglucoside, "
        "Sodium Cocoyl Glutamate, Sodium Lauryl Glucose Carboxylate, Sodium Chloride, "
        "Caprylyl Glycol, Panthenol, Citric Acid, Citrus Nobilis Essential Oil, "
        "Citrus Grandis Essential Oil, Citrus Aurantium Dulcis Essential Oil, "
        "Coco-Glucoside, Glyceryl Oleate, Sodium Gluconate, Caprylhydroxamic Acid, "
        "Calendula Officinalis Oil, Persea Gratissima Oil, Aloe Barbadensis Extract, "
        "Argania Spinosa Kernel Oil, Chamomilla Recutita Flower Oil",
        IMG + "/a57cb2da-26bb-4dcd-9289-9432bb51228b/products/"
              "the-moms-co-natural-baby-wash/"
              "the-moms-co-natural-baby-wash_front_photo_original.jpeg",
    ),
    (
        "The Moms Co. Natural Baby Lotion",
        "The Moms Co.", "Baby Care",
        "Purified Water, Caprylic/Capric Triglyceride, Glycerin, "
        "Glyceryl Monostearate, Cetostearyl Alcohol, Cetyl Alcohol, "
        "Organic Butyrospermum Parkii Butter, Coco-Caprylate/Caprate, "
        "Aloe Barbadensis Extract, Cera Alba, Heptyl Undecylenate, "
        "Ethylhexyl Olivate, Caprylyl Glycol, Organic Prunus Armeniaca Kernel Oil, "
        "Vanilla Planifolia Fruit Extract, Theobroma Cacao Seed Butter, "
        "Cocos Nucifera Oil, Organic Simmondsia Chinensis Seed Oil, "
        "Organic Oryza Sativa Bran Oil, Sodium PCA, Xanthan Gum, "
        "Sodium Stearoyl Glutamate, Sodium Gluconate, Tocopherol, "
        "Caprylhydroxamic Acid, Persea Gratissima Seed Oil, Citric Acid",
        IMG + "/7ac0659d-b611-4b5a-9826-0a17dd932943/products/"
              "the-moms-co-natural-baby-lotion/"
              "the-moms-co-natural-baby-lotion_front_photo_original.jpeg",
    ),
    (
        "The Moms Co. Natural Talc-Free Baby Powder",
        "The Moms Co.", "Baby Care",
        "Zea Mays Starch, Tricalcium Phosphate, Organic Simmondsia Chinensis Oil, "
        "Calendula Officinalis Oil, Vanilla Planifolia Extract, "
        "Organic Matricaria Recutita Flower Oil",
        IMG + "/d5d814a0-5dab-4284-a276-9e744712d539/products/"
              "the-moms-co-natural-baby-powder/"
              "the-moms-co-natural-baby-powder_front_photo_original.jpeg",
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
    print(f"Inserting {len(PRODUCTS)} The Moms Co. products...\n")
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
