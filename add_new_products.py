"""
Add 41 new products to Parkho database.
Images fetched from Google Images search.
Ingredients classified using the backend engine.
"""
import sys, os, re, time, json, urllib.parse, requests
sys.path.insert(0, 'backend')

from dotenv import load_dotenv
load_dotenv('backend/.env')
from supabase import create_client

# Backend imports
from routes.ingredient_database import (
    classify_ingredient, INGREDIENT_DESCRIPTIONS
)

# Supabase admin client (bypasses RLS)
SUPABASE_URL  = os.environ['SUPABASE_URL']
SERVICE_KEY   = os.environ['SUPABASE_SERVICE_ROLE_KEY']
sb = create_client(SUPABASE_URL, SERVICE_KEY)

# ── Google Image Search ───────────────────────────────────────────────────────

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml',
}

def duckduckgo_image(query) -> str | None:
    """Search DuckDuckGo Images and return the first product image URL."""
    session = requests.Session()
    session.headers.update(HEADERS)
    try:
        # Step 1: get vqd token (required for image API)
        enc = urllib.parse.quote_plus(query)
        r = session.get(f"https://duckduckgo.com/?q={enc}&ia=images", timeout=10)
        vqd_match = re.search(r'vqd=(["\'])([^"\']+)\1', r.text)
        if not vqd_match:
            # Try alternate pattern
            vqd_match = re.search(r'"vqd":"([^"]+)"', r.text)
            vqd = vqd_match.group(1) if vqd_match else None
        else:
            vqd = vqd_match.group(2)

        if not vqd:
            return None

        time.sleep(0.5)

        # Step 2: image JSON API
        api = (
            f"https://duckduckgo.com/i.js"
            f"?l=wt-wt&o=json&q={enc}&vqd={vqd}&f=,,,,,&p=1"
        )
        r2 = session.get(api, timeout=10,
                         headers={**HEADERS, "Referer": "https://duckduckgo.com/"})
        data = r2.json()
        results = data.get("results", [])
        for item in results:
            u = item.get("image") or item.get("thumbnail")
            if u and re.search(r'\.(jpg|jpeg|png|webp)', u, re.I):
                return u
    except Exception as e:
        print(f"    DuckDuckGo error: {e}")
    return None

# ── Ingredient Helpers ────────────────────────────────────────────────────────

def parse_ingredients(raw: str):
    """Split comma-separated ingredient string, respecting parentheses."""
    parts, depth, cur = [], 0, ""
    for ch in raw:
        if ch == '(':
            depth += 1; cur += ch
        elif ch == ')':
            depth -= 1; cur += ch
        elif ch == ',' and depth == 0:
            p = cur.strip().rstrip('.')
            if p:
                parts.append(p)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur.strip().rstrip('.'))
    return parts

def classify_one(name: str) -> dict:
    """Classify a single ingredient and return a structured dict."""
    try:
        cls = classify_ingredient(name)
        if not isinstance(cls, str):
            cls = cls.get('classification', 'generally_recognised')
    except Exception:
        cls = 'generally_recognised'

    key = name.lower().strip()
    # Try direct lookup and a few normalizations
    raw_desc = (
        INGREDIENT_DESCRIPTIONS.get(key) or
        INGREDIENT_DESCRIPTIONS.get(re.sub(r'\s*\(.*?\)', '', key).strip())
    )
    # Values can be strings or dicts depending on ingredient_database version
    desc = raw_desc if isinstance(raw_desc, dict) else {}
    return {
        "name": name,
        "aliases": desc.get('aliases', ''),
        "classification": cls,
        "one_line_note": desc.get('one_line_note', ''),
        "regulatory_note": desc.get('regulatory_note', ''),
        "commonly_found_in": desc.get('commonly_found_in'),
        "health_effects": desc.get('health_effects'),
        "countries_restricted": desc.get('countries_restricted', []),
        "fssai_position": desc.get('fssai_position'),
        "recommendation": desc.get('recommendation'),
    }

def compute_grade(classified: list) -> str:
    if not classified:
        return "B"
    total = len(classified)
    questioned = sum(1 for i in classified if i['classification'] == 'commonly_questioned')
    worth     = sum(1 for i in classified if i['classification'] == 'worth_knowing')
    if questioned > 0:
        return "D"
    if worth == 0:
        return "A"
    return "B" if worth / total <= 0.30 else "C"

def make_static_key(name: str) -> str:
    return re.sub(r'[^a-z0-9]', '', name.lower())

def make_summary(name, brand, grade, questioned, worth, total) -> str:
    safe_pct = round((total - questioned - worth) / max(total, 1) * 100)
    concern  = "commonly questioned" if questioned else ("worth knowing" if worth else "")
    if grade == "A":
        return (f"{name} by {brand} scores Grade A. All {total} ingredients are "
                f"generally recognised as safe with no concerning additives detected.")
    elif grade == "B":
        return (f"{name} by {brand} scores Grade B. {total} ingredients analysed; "
                f"{worth} are worth knowing about but no restricted additives found.")
    elif grade == "C":
        return (f"{name} by {brand} scores Grade C. Contains {worth} worth-knowing "
                f"ingredients (>{30}% of total). Use with awareness.")
    else:
        return (f"{name} by {brand} scores Grade D. Contains {questioned} "
                f"{concern} ingredient(s) that are restricted or flagged in some countries.")

# ── Product Catalogue ─────────────────────────────────────────────────────────
# (name, brand, category, variant, net_wt, ingredients_raw, image_hint)
# image_hint = extra keyword for Google image search

PRODUCTS = [
    # ── FOOD ──────────────────────────────────────────────────────────────────
    (
        "Nestle KitKat 4 Finger", "Nestle", "Chocolates", "4 Finger Bar", "41.5 g",
        "Sugar, Cocoa Butter, Skimmed Milk Powder, Cocoa Mass, Wheat Flour, Vegetable Fat (Palm), "
        "Lactose, Whole Milk Powder, Whey Powder, Raising Agents (Sodium Bicarbonate, Ammonium Bicarbonate), "
        "Emulsifiers (Soy Lecithin, INS 476), Salt, Flavour (Vanillin).",
        "Nestle KitKat 4 Finger chocolate bar India"
    ),
    (
        "Nestle Munch", "Nestle", "Chocolates", "Original", "18 g",
        "Sugar, Glucose, Hydrogenated Vegetable Fat, Wheat Flour, Cocoa Solids, Milk Solids, "
        "Invert Sugar, Emulsifiers (INS 322, INS 476), Salt, Raising Agents (INS 500(ii), INS 503(ii)), "
        "Colour (INS 150a), Flavours.",
        "Nestle Munch chocolate bar India"
    ),
    (
        "Nestle Milkybar", "Nestle", "Chocolates", "Original White Chocolate", "13 g",
        "Sugar, Whole Milk Powder, Cocoa Butter, Skimmed Milk Powder, Wheat Flour, Lactose, "
        "Emulsifiers (Soy Lecithin, INS 476), Raising Agents (Sodium Bicarbonate, Ammonium Bicarbonate), "
        "Salt, Flavour (Vanillin).",
        "Nestle Milkybar white chocolate India"
    ),
    (
        "Cadbury Gems", "Cadbury", "Chocolates", "Button Chocolate", "24 g",
        "Sugar, Cocoa Butter, Skimmed Milk Powder, Cocoa Mass, Lactose, Vegetable Fats (Palm, Shea), "
        "Whey Permeate Powder, Emulsifier (Soy Lecithin), Glucose Syrup, Starch (Rice, Potato, Maize), "
        "Colours (INS 110, INS 124, INS 102, INS 133, INS 132), Glazing Agent (Carnauba Wax, Shellac), Flavour.",
        "Cadbury Gems chocolate India"
    ),
    (
        "Parle Monaco Classic", "Parle", "Biscuits", "Classic Salted", "150 g",
        "Refined Wheat Flour (Maida), Edible Vegetable Oil (Palm Oil), Sugar, Invert Sugar Syrup, "
        "Salt, Raising Agents (INS 503(ii), INS 500(ii)), Emulsifier (INS 322), "
        "Acidity Regulator (INS 330), Yeast, Dough Conditioner (INS 920).",
        "Parle Monaco biscuits India"
    ),
    (
        "Parle Krackjack", "Parle", "Biscuits", "Sweet & Salty", "300 g",
        "Refined Wheat Flour (Maida), Edible Vegetable Oil (Palm Oil), Sugar, Liquid Glucose, "
        "Invert Sugar Syrup, Salt, Raising Agents (INS 503(ii), INS 500(ii)), Emulsifier (INS 322), "
        "Dough Conditioner (INS 920), Acidity Regulator (INS 270), Yeast.",
        "Parle Krackjack sweet salty biscuit India"
    ),
    (
        "Britannia Marie Gold", "Britannia", "Biscuits", "Classic", "250 g",
        "Refined Wheat Flour (Maida), Sugar, Edible Vegetable Oil (Palm Oil), Invert Sugar Syrup, "
        "Wheat Bran, Raising Agents (Ammonium Bicarbonate, Sodium Bicarbonate), Salt, "
        "Emulsifier (Soy Lecithin INS 322), Flavour (Vanilla).",
        "Britannia Marie Gold biscuit India"
    ),
    (
        "Britannia Good Day Butter Cookies", "Britannia", "Biscuits", "Butter", "150 g",
        "Refined Wheat Flour (Maida), Sugar, Edible Vegetable Oil (Palm Olein), Liquid Glucose, "
        "Invert Sugar Syrup, Milk Solids, Butter (3%), Salt, Raising Agents (INS 500(ii), INS 503(ii)), "
        "Emulsifier (INS 322), Flavour (Artificial Butter).",
        "Britannia Good Day Butter Cookies India"
    ),
    (
        "Tropicana 100% Orange Juice", "PepsiCo", "Beverages", "100% Orange", "1 L",
        "100% Orange Juice from Concentrate (Water, Orange Juice Concentrate), Vitamin C (Ascorbic Acid).",
        "Tropicana 100% orange juice 1 litre India"
    ),
    (
        "Paper Boat Frooti Mango Drink", "Hector Beverages", "Beverages", "Mango Fruit Drink", "200 mL",
        "Water, Mango Pulp (27%), Sugar, Citric Acid (INS 330), Antioxidant (Ascorbic Acid INS 300), "
        "Salt, Guar Gum (INS 412), Colour (Beta-Carotene INS 160a), Preservative (Potassium Sorbate INS 202).",
        "Paper Boat frooti mango drink India"
    ),
    (
        "Minute Maid Pulpy Orange", "Coca-Cola India", "Beverages", "Orange Drink", "400 mL",
        "Water, Sugar, Orange Pulp (3%), Orange Juice Concentrate (1.5%), Citric Acid (INS 330), "
        "Stabilisers (Cellulose Gum INS 466, Pectin INS 440), Colour (INS 110 Sunset Yellow), "
        "Flavour (Natural Orange).",
        "Minute Maid Pulpy Orange drink India"
    ),
    (
        "Red Bull Energy Drink", "Red Bull GmbH", "Beverages", "Original 250 mL", "250 mL",
        "Water, Sucrose, Glucose, Citric Acid (INS 330), Taurine (0.4%), Sodium Citrate (INS 331), "
        "Magnesium Carbonate (INS 504), Caffeine (0.03%), Niacinamide (Vitamin B3), "
        "Calcium Pantothenate (Vitamin B5), Pyridoxine HCl (Vitamin B6), Cyanocobalamin (Vitamin B12), "
        "Colour (INS 150a Caramel), Flavours.",
        "Red Bull energy drink 250ml can India"
    ),
    (
        "Sting Energy Drink Berry Blast", "PepsiCo", "Beverages", "Berry Blast", "250 mL",
        "Carbonated Water, Sugar, Glucose, Citric Acid (INS 330), Taurine, Caffeine, "
        "Sodium Citrate (INS 331), Inositol, Colour (INS 122, INS 124), "
        "Acesulfame Potassium (INS 950), Sucralose (INS 955), Flavours, Vitamins (B3, B6, B12).",
        "Sting energy drink Berry Blast can India"
    ),
    (
        "Quaker Oats Original", "PepsiCo", "Breakfast Cereals", "Original Rolled Oats", "500 g",
        "Whole Grain Rolled Oats (100%).",
        "Quaker Oats original 500g pouch India"
    ),
    (
        "Kellogg's Corn Flakes", "Kellogg's", "Breakfast Cereals", "Original", "250 g",
        "Milled Corn (Corn Grits 91%), Sugar, Salt, Malt Flavour (from Barley), "
        "Niacinamide, Vitamin A, Vitamin B6, Vitamin B2, Folic Acid, Vitamin B12, Iron, "
        "Colour (INS 150a).",
        "Kellogg's Corn Flakes 250g box India"
    ),
    (
        "Kellogg's Chocos", "Kellogg's", "Breakfast Cereals", "Choco Fills", "375 g",
        "Whole Grain Wheat (59%), Sugar, Cocoa Powder (4%), Wheat Starch, Salt, "
        "Colour (INS 150d), Emulsifier (Soy Lecithin INS 322), Niacinamide, Iron, Zinc, "
        "Vitamin B6, Riboflavin, Vitamin B12, Folic Acid, Vitamin A, Vitamin D3, Flavour.",
        "Kellogg's Chocos cereal box India"
    ),
    (
        "Sunfeast Yippee Magic Masala Noodles", "ITC", "Instant Noodles", "Magic Masala", "65 g",
        "Refined Wheat Flour (Maida 92%), Refined Palm Oil, Salt, Minerals (INS 451(i), INS 500(i)), "
        "Colour (INS 101ii), Iodised Salt, Sugar, Spices and Condiments (Coriander, Chilli, Turmeric, Cumin), "
        "Dehydrated Vegetables (Onion, Tomato), Flavour Enhancer (INS 621, INS 627, INS 631), "
        "Acidity Regulator (INS 330), Colour (INS 110, INS 100ii), "
        "Anticaking Agent (INS 551), Hydrogenated Vegetable Fat.",
        "Sunfeast Yippee Magic Masala noodles India"
    ),
    (
        "Knorr Classic Tomato Soup", "HUL", "Instant Soups", "Classic Tomato", "46 g",
        "Wheat Flour, Sugar, Tomato Powder (10%), Salt, Corn Starch, Edible Vegetable Oil (Palm), "
        "Maltodextrin, Skimmed Milk Powder, Tomato Flakes (1%), Tomato Puree Powder, "
        "Flavour Enhancers (INS 621, INS 627, INS 631), Flavour (Tomato), "
        "Acidity Regulator (INS 330), Spices, Anticaking Agent (INS 551).",
        "Knorr Classic Tomato Soup sachet India"
    ),
    (
        "Kissan Mixed Fruit Jam", "HUL", "Spreads", "Mixed Fruit", "500 g",
        "Sugar, Mixed Fruit Pulp and Juice (Mango, Papaya, Pineapple, Banana) (45%), "
        "Citric Acid (INS 330), Pectin (INS 440), Preservative (Sodium Benzoate INS 211), "
        "Colour (INS 110 Sunset Yellow, INS 129 Allura Red).",
        "Kissan Mixed Fruit Jam 500g jar India"
    ),
    (
        "Yoga Bar Oats And Berries Bar", "ITC Yoga Bar", "Health Bars", "Oats & Berries", "38 g",
        "Oats (55%), Mixed Berries (Cranberry, Raisin, Blueberry 14%), Brown Rice Crisps, "
        "Rice Syrup, Honey, Sunflower Seeds, Flax Seeds, Pumpkin Seeds, Rolled Wheat, "
        "Soy Crisps (Soy Protein Isolate), Dark Chocolate (Cocoa Mass, Sugar, Cocoa Butter, Soy Lecithin), Salt.",
        "Yoga Bar Oats Berries energy bar India"
    ),
    (
        "Too Yumm Multigrain Chips", "RP-Sanjiv Goenka Group", "Snacks", "Multigrain Original", "42 g",
        "Multigrain Mix (Corn, Rice, Oats, Soya, Wheat 70%), Edible Vegetable Oil (Rice Bran Oil), "
        "Iodised Salt, Sugar, Maltodextrin, Acidity Regulator (INS 330), "
        "Hydrolysed Corn Protein, Spices, Anticaking Agent (INS 551).",
        "Too Yumm Multigrain Chips packet India"
    ),

    # ── COSMETICS ─────────────────────────────────────────────────────────────
    (
        "Himalaya Nourishing Skin Cream", "Himalaya", "Skincare", "Original", "50 mL",
        "Aqua, Aloe Barbadensis Leaf Extract, Glycerin, Cetearyl Alcohol, Mineral Oil, "
        "Stearic Acid, Vitis Vinifera Seed Oil, Glyceryl Stearate, Sodium Stearoyl Lactylate, "
        "Prunus Amygdalus Dulcis Oil, Butyrospermum Parkii (Shea Butter), Carbomer, "
        "Triethanolamine, Allantoin, Sodium PCA, Diazolidinyl Urea, Iodopropynyl Butylcarbamate, Parfum.",
        "Himalaya Nourishing Skin Cream tube India"
    ),
    (
        "Himalaya Aloe Vera Face Wash", "Himalaya", "Face Wash", "Moisturizing", "100 mL",
        "Aqua, Aloe Barbadensis Leaf Extract, Cocamidopropyl Betaine, Sodium Laureth Sulfate, "
        "Glycerin, Propylene Glycol, PEG-7 Glyceryl Cocoate, Citric Acid, Disodium EDTA, "
        "Benzophenone-4, Methylparaben, Propylparaben, Parfum.",
        "Himalaya Aloe Vera moisturizing face wash India"
    ),
    (
        "Himalaya Anti-Dandruff Shampoo", "Himalaya", "Haircare", "Anti-Dandruff", "400 mL",
        "Aqua, Sodium Laureth Sulfate, Cocamidopropyl Betaine, Glycol Distearate, Sodium Chloride, "
        "Glycerin, Zinc Pyrithione (1%), Selenium Disulfide (0.1%), Tea Tree Leaf Oil, "
        "Neem Leaf Extract, Aloe Barbadensis Extract, Dimethicone, Carbomer, Citric Acid, "
        "Sodium Benzoate, DMDM Hydantoin, Parfum.",
        "Himalaya Anti-Dandruff shampoo bottle India"
    ),
    (
        "St. Ives Apricot Scrub", "Unilever", "Skincare", "Exfoliate & Unclog Pores", "150 mL",
        "Water, Walnut Shell Powder, Glycerin, Sodium C14-16 Olefin Sulfonate, "
        "Cocamidopropyl Betaine, Propylene Glycol, Acrylates C10-30 Alkyl Acrylate Crosspolymer, "
        "Sodium Hydroxide, Prunus Armeniaca Kernel Oil, Citric Acid, "
        "DMDM Hydantoin, Methylisothiazolinone, Parfum.",
        "St Ives Apricot Scrub exfoliating face scrub India"
    ),
    (
        "Re'equil Oxi-Moist Moisturizer SPF 15", "Re'equil", "Sunscreen", "SPF 15 PA++", "50 g",
        "Aqua, Ethylhexyl Methoxycinnamate, Glycerin, Ethylhexyl Salicylate, Dimethicone, "
        "Cyclomethicone, Niacinamide, Cetyl Alcohol, Stearyl Alcohol, Polyacrylate-13, "
        "Vitamin E (Tocopheryl Acetate), Allantoin, Aloe Barbadensis Extract, "
        "Disodium EDTA, Phenoxyethanol, Ethylhexylglycerin, Parfum.",
        "Re'equil Oxi-Moist moisturizer SPF 15 India"
    ),
    (
        "Fixderma Shadow SPF 30 Sunscreen", "Fixderma", "Sunscreen", "Shadow SPF 30 PA+++", "75 g",
        "Avobenzone (3%), Octinoxate (7.5%), Oxybenzone (2%), Aqua, Glycerin, Niacinamide, "
        "Dimethicone, Cyclomethicone, Cetearyl Alcohol, Ceteareth-20, Titanium Dioxide, Zinc Oxide, "
        "Aloe Vera Extract, Vitamin C (Ascorbic Acid), Vitamin E (Tocopheryl Acetate), "
        "Phenoxyethanol, Methylparaben, Parfum.",
        "Fixderma Shadow SPF 30 sunscreen India"
    ),
    (
        "Pilgrim Salicylic Acid Face Wash", "Pilgrim", "Face Wash", "Salicylic Acid 2% + Green Tea", "100 mL",
        "Aqua, Cocamidopropyl Betaine, Sodium Cocoyl Isethionate, Glycerin, Salicylic Acid (2%), "
        "Camellia Sinensis Leaf Extract, Niacinamide, Willow Bark Extract, Panthenol, Allantoin, "
        "Zinc PCA, Sodium Benzoate, Citric Acid, Disodium EDTA, Phenoxyethanol.",
        "Pilgrim Salicylic Acid 2% face wash tube India"
    ),
    (
        "Pilgrim Red Vine Anti-Aging Serum", "Pilgrim", "Serums", "Red Vine + Hyaluronic Acid", "30 mL",
        "Aqua, Niacinamide (5%), Hyaluronic Acid (Sodium Hyaluronate), "
        "Vitis Vinifera Seed Extract (Resveratrol), Panthenol (Vitamin B5), Glycerin, "
        "Propylene Glycol, Carbomer, Triethanolamine, Allantoin, Disodium EDTA, "
        "Phenoxyethanol, Ethylhexylglycerin.",
        "Pilgrim Red Vine anti-aging serum dropper India"
    ),
    (
        "The Derma Co 1% Hyaluronic Acid Serum", "The Derma Co", "Serums", "1% Hyaluronic Acid", "30 mL",
        "Aqua, Glycerin, Sodium Hyaluronate, Hyaluronic Acid, Hydrolyzed Hyaluronic Acid, "
        "Sodium Acetylated Hyaluronate, Hydroxypropyltrimonium Hyaluronate, Panthenol, "
        "Allantoin, Niacinamide, Betaine, Phenoxyethanol, Ethylhexylglycerin, "
        "Disodium EDTA, Xanthan Gum.",
        "The Derma Co Hyaluronic Acid serum India"
    ),
    (
        "The Derma Co 0.3% Retinol Night Serum", "The Derma Co", "Serums", "0.3% Retinol + Peptide", "30 mL",
        "Aqua, Cyclopentasiloxane, Dimethicone Vinyl Dimethicone Crosspolymer, Glycerin, "
        "Retinol (0.3%), Palmitoyl Tripeptide-5, Tocopheryl Acetate, Sodium Hyaluronate, "
        "Niacinamide, Bakuchiol, Simmondsia Chinensis Seed Oil, Phenoxyethanol, "
        "Ethylhexylglycerin, BHT.",
        "Derma Co 0.3% Retinol night serum India"
    ),
    (
        "Kama Ayurveda Kumkumadi Oil", "Kama Ayurveda", "Skincare", "Miraculous Beauty Fluid", "12 mL",
        "Sesamum Indicum Seed Oil, Crocus Sativus Stigma Extract, Rubia Cordifolia Root Extract, "
        "Vetiveria Zizanioides Root Extract, Glycyrrhiza Glabra Root Extract, "
        "Nelumbo Nucifera Petal Extract, Santalum Album Heartwood Oil, Rosa Damascena Essential Oil, "
        "Boerhavia Diffusa Root Extract.",
        "Kama Ayurveda Kumkumadi Miraculous Beauty Oil India"
    ),
    (
        "Beardo Beard Growth Oil", "Beardo", "Haircare", "Beard & Hair Growth Oil", "50 mL",
        "Argania Spinosa Kernel Oil, Simmondsia Chinensis Seed Oil, Ricinus Communis Seed Oil, "
        "Vitis Vinifera Seed Oil, Tocopherol (Vitamin E), Redensyl (Larix Europaea Wood Extract, "
        "Glycine, Zinc Chloride), Procapil (Biotinyl GHK Tripeptide-3, Apigenin, Oleanolic Acid), "
        "Eclipta Prostrata Extract, Rosmarinus Officinalis Leaf Oil.",
        "Beardo beard growth oil 50ml India"
    ),
    (
        "Mars by GHC 5% Minoxidil Hair Serum", "The Good Health Company", "Haircare", "5% Minoxidil Scalp Serum", "60 mL",
        "Minoxidil (5%), Propylene Glycol, Ethanol, Redensyl (Larix Europaea Wood Extract), "
        "Capilia Longa (Curcuma Longa Callus Extract), Anagain (Pisum Sativum Sprout Extract), "
        "Procapil (Biotinyl GHK Tripeptide-3, Apigenin, Oleanolic Acid), Biotin, Aqua.",
        "Mars by GHC 5% Minoxidil hair serum India"
    ),
    (
        "Plum Green Tea Pore-Cleansing Face Wash", "Plum", "Face Wash", "Green Tea Pore-Cleansing", "100 mL",
        "Aqua, Decyl Glucoside, Cocamidopropyl Betaine, Camellia Sinensis Leaf Extract, Glycerin, "
        "Niacinamide, Willow Bark Extract (Salicylic Acid 0.5%), Allantoin, Panthenol, "
        "Disodium Cocoamphodiacetate, Citric Acid, Sodium Benzoate, Potassium Sorbate, Xanthan Gum.",
        "Plum Green Tea Pore Cleansing Face Wash India"
    ),
    (
        "Aqualogica Glow+ Dewy Sunscreen SPF 50", "Aqualogica", "Sunscreen", "SPF 50 PA++++", "50 g",
        "Ethylhexyl Methoxycinnamate (7.5%), Ethylhexyl Salicylate (5%), "
        "Butyl Methoxydibenzoylmethane (3%), Aqua, Dimethicone, Glycerin, Niacinamide, "
        "Watermelon Fruit Extract, Hyaluronic Acid (Sodium Hyaluronate), "
        "Vitamin E (Tocopheryl Acetate), Pentylene Glycol, Phenoxyethanol, "
        "Carbomer, Triethanolamine.",
        "Aqualogica Glow+ Dewy Sunscreen SPF 50 India"
    ),
    (
        "Fixderma Shadow SPF 50+ Sunscreen Gel", "Fixderma", "Sunscreen", "SPF 50+ PA++++", "50 g",
        "Ethylhexyl Methoxycinnamate (7.5%), Butyl Methoxydibenzoylmethane (3.5%), "
        "Ethylhexyl Triazone (3%), Aqua, Glycerin, Niacinamide, Aloe Vera Leaf Juice, "
        "Vitamin E (Tocopheryl Acetate), Hydroxypropyl Cellulose, Carbomer, "
        "Sodium Hydroxide, Disodium EDTA, Phenoxyethanol, Ethylhexylglycerin.",
        "Fixderma Shadow SPF 50+ sunscreen gel tube India"
    ),
    (
        "Wild Stone Ultra Sensual Body Spray", "JK Helene Curtis", "Deodorants", "Ultra Sensual Men", "150 mL",
        "Alcohol Denat., Aqua, Parfum, Butane, Propane, Isobutane, Dimethyl Ether, "
        "Cyclopentasiloxane, Isopropyl Myristate, Benzyl Salicylate, Linalool, Limonene, "
        "Geraniol, Hexyl Cinnamal, Coumarin, Benzyl Benzoate, Citronellol, "
        "Alpha-Isomethyl Ionone, Eugenol, Hydroxycitronellal, Amyl Cinnamal.",
        "Wild Stone Ultra Sensual body spray deodorant India"
    ),
    (
        "Fogg Xpression Deodorant For Men", "Vini Cosmetics", "Deodorants", "Xpression Men", "150 mL",
        "Alcohol (SD Alcohol 40-B), Parfum, Dimethyl Ether, Cyclopentasiloxane, "
        "Isopropyl Myristate, Butylphenyl Methylpropional, Linalool, Limonene, Citronellol, "
        "Geraniol, Benzyl Salicylate, Amyl Cinnamal, Hexyl Cinnamal, Coumarin, "
        "Butane, Propane, Isobutane.",
        "Fogg Xpression deodorant body spray men India"
    ),
    (
        "Engage W1 Perfume Spray For Women", "ITC", "Deodorants", "W1 Women", "150 mL",
        "Alcohol Denat., Aqua, Parfum, Dimethyl Ether, Benzyl Salicylate, Linalool, Limonene, "
        "Hexyl Cinnamal, Alpha-Isomethyl Ionone, Citronellol, Geraniol, "
        "Hydroxyisohexyl 3-Cyclohexene Carboxaldehyde, Coumarin, Butylphenyl Methylpropional, "
        "Amyl Cinnamal, Butane, Propane, Isobutane.",
        "Engage W1 perfume spray women India"
    ),
    (
        "Sugar Cosmetics Aquaholic Sunscreen", "Sugar Cosmetics", "Sunscreen", "SPF 50 PA++++ Aquaholic Matte", "50 g",
        "Ethylhexyl Methoxycinnamate (7%), Bis-Ethylhexyloxyphenol Methoxyphenyl Triazine (3%), "
        "Ethylhexyl Triazone (3%), Aqua, Glycerin, Niacinamide, Cucumber Fruit Extract, "
        "Menthol, Hyaluronic Acid (Sodium Hyaluronate), Silica, Dimethicone, Carbomer, "
        "Sodium Hydroxide, Disodium EDTA, Phenoxyethanol, Ethylhexylglycerin.",
        "Sugar Cosmetics Aquaholic Sunscreen SPF 50 India"
    ),
]

# ── Main Insertion Loop ───────────────────────────────────────────────────────

def already_exists(name: str) -> bool:
    res = sb.table('ai_extracted_products').select('id').ilike('name', name).limit(1).execute()
    return bool(res.data)

def insert_product(name, brand, category, variant, net_wt, ingredients_raw, image_hint):
    print(f"\n[{name}]")

    # Skip if already in DB
    if already_exists(name):
        print(f"  SKIP -- already in database")
        return False

    # 1. Fetch image via DuckDuckGo (no API key needed)
    print(f"  Searching image: {image_hint[:55]}...")
    image_url = duckduckgo_image(image_hint)
    if image_url:
        print(f"  Image: {image_url[:80]}...")
    else:
        print(f"  No image found")
    time.sleep(1.0)

    # 2. Parse and classify ingredients
    ing_names = parse_ingredients(ingredients_raw)
    classified = [classify_one(n) for n in ing_names]
    print(f"  Classified {len(classified)} ingredients")

    # 3. Compute grade
    grade = compute_grade(classified)
    questioned = sum(1 for i in classified if i['classification'] == 'commonly_questioned')
    worth      = sum(1 for i in classified if i['classification'] == 'worth_knowing')
    print(f"  Grade: {grade}  ({questioned} questioned, {worth} worth-knowing, {len(classified)-questioned-worth} safe)")

    # 4. Build summary
    summary = make_summary(name, brand, grade, questioned, worth, len(classified))

    # 5. FSSAI note
    fssai_map = {
        "Beverages": "This product falls under beverages. FSSAI regulates maximum caffeine, colour, and preservative limits under FSS (Food Products Standards and Food Additives) Regulations 2011.",
        "Chocolates": "Chocolate products are regulated under FSSAI standards for cocoa, milk solids, and vegetable fat. Artificial colours must be listed on label.",
        "Biscuits": "Biscuits and cookies are regulated under FSSAI Schedule I. Palm oil usage and trans-fat limits apply under FSS Regulations.",
        "Instant Noodles": "Instant noodles are regulated under FSSAI. MSG (INS 621) is permitted. Trans-fat from hydrogenated fat must be below 2% of total fat.",
        "Breakfast Cereals": "Breakfast cereals are regulated under Food Safety and Standards Act. Added vitamins must meet FSSAI fortification standards.",
        "Skincare": "Cosmetics are regulated under the Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020. Ingredient labelling is mandatory.",
        "Face Wash": "Regulated under Cosmetics Rules 2020. SLES and SLS are permitted. Preservative concentrations must meet BIS standards.",
        "Sunscreen": "Sunscreens are classified as cosmetics under Drugs & Cosmetics Act. SPF values must be validated per ISO 24444.",
        "Serums": "Face serums are regulated as cosmetics under Cosmetics Rules 2020. Active ingredient concentrations should match label claims.",
        "Haircare": "Hair care products regulated under Cosmetics Rules 2020. Zinc Pyrithione concentrations for anti-dandruff products regulated separately.",
        "Deodorants": "Regulated as cosmetics. Alcohol-based sprays must meet IS 9834. Fragrance allergens must be disclosed on label.",
        "Health Bars": "Regulated as processed food under FSSAI. Energy and nutrition claims must comply with FSSAI Food Labelling Regulations 2019.",
        "Instant Soups": "Regulated under FSSAI processed food standards. MSG and artificial colours must be declared on label.",
        "Spreads": "Regulated under FSSAI Jam, Jellies and Marmalade standards. Preservatives like Sodium Benzoate are permitted at regulated levels.",
        "Snacks": "Regulated under FSSAI snack food standards. Trans-fat must be less than 2% of total fat. Colour and flavour additives must be from permitted list.",
    }
    fssai_note = fssai_map.get(category, "Regulated under the Food Safety and Standards Authority of India (FSSAI) or Cosmetics Rules 2020.")

    # 6. Build record — only columns that exist in the table
    # Actual columns: id, name, brand, category, image_url, awareness_score,
    #   summary, fssai_note, verdict, recommendation, ingredients,
    #   ingredients_raw, submission_id, status, created_at, images, grade, static_key
    safe_count = len(classified) - questioned - worth
    verdict = (
        f"Contains {questioned} restricted/flagged ingredient(s)." if questioned else
        f"Contains {worth} ingredient(s) worth monitoring." if worth else
        "All ingredients are generally safe."
    )
    recommendation = (
        "Avoid or use sparingly — contains commonly questioned ingredients." if questioned else
        "Use with awareness — some additives worth monitoring." if worth else
        "Safe to use — no concerning ingredients detected."
    )
    awareness_score = max(0, 100 - (questioned * 25) - (worth * 8))

    record = {
        "name":            name,
        "brand":           brand,
        "category":        category,
        "grade":           grade,
        "ingredients_raw": ingredients_raw,
        "ingredients":     classified,
        "image_url":       image_url,
        "static_key":      make_static_key(name),
        "summary":         summary,
        "fssai_note":      fssai_note,
        "verdict":         verdict,
        "recommendation":  recommendation,
        "awareness_score": awareness_score,
        "status":          "approved",
    }

    # 7. Insert into Supabase
    try:
        res = sb.table('ai_extracted_products').insert(record).execute()
        print(f"  INSERTED (id: {res.data[0]['id'][:8]}...)")
        return True
    except Exception as e:
        print(f"  ERROR inserting: {e}")
        return None  # None = failed (False = skipped)


def main():
    print(f"Starting insertion of {len(PRODUCTS)} products...\n")
    added, skipped, failed = 0, 0, 0

    for p in PRODUCTS:
        result = insert_product(*p)
        if result is True:
            added += 1
        elif result is False:
            skipped += 1
        else:
            failed += 1

    print(f"\n{'='*50}")
    print(f"Done!  Added: {added}  |  Skipped (already in DB): {skipped}  |  Failed: {failed}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
