"""
New Products Catalog PDF — Food & Cosmetics NOT in Parkho database.
For review before adding to DB.
"""
from fpdf import FPDF

OUT = "Parkho_New_Products_Catalog.pdf"

# ── Palette ───────────────────────────────────────────────────────────────────
NAVY      = (26,  43,  74)
NAVY_MED  = (30,  58,  138)
ORANGE    = (234, 88,  12)
WHITE     = (255, 255, 255)
GRAY_900  = (17,  24,  39)
GRAY_700  = (55,  65,  81)
GRAY_500  = (107, 114, 128)
GRAY_200  = (229, 231, 235)
GRAY_50   = (249, 250, 251)
GREEN_BG  = (220, 252, 231)
GREEN_FG  = (21,  128, 61)
PINK_BG   = (252, 231, 243)
PINK_FG   = (157, 23,  77)
AMBER_BG  = (254, 243, 199)
AMBER_FG  = (180, 83,  9)
BLUE_BG   = (219, 234, 254)
BLUE_FG   = (29,  78,  216)
RED_BG    = (254, 226, 226)
RED_FG    = (185, 28,  28)

def safe(t):
    subs = {
        '—':'--','–':'-','→':'->','←':'<-',''': "'", ''': "'",
        '"': '"', '"': '"', '…': '...', '°': 'deg', '•': '*',
        '₹': 'Rs.', 'é': 'e', '×': 'x', '≥': '>=', '≤': '<=',
        '®': '(R)', '™': '(TM)', '±': '+/-',
        '°': 'deg', '’': "'",
    }
    for k, v in subs.items():
        t = t.replace(k, v)
    return t.encode('latin-1', 'replace').decode('latin-1')


class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 8, 'F')
        self.set_text_color(*WHITE)
        self.set_font('Helvetica', 'B', 6.5)
        self.set_xy(10, 1)
        self.cell(0, 6, "Parkho -- New Products Catalog (For Review Only -- Not Yet in Database)", align='L')
        self.set_text_color(0, 0, 0)
        self.set_y(11)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-11)
        self.set_draw_color(*GRAY_200)
        self.set_line_width(0.2)
        self.line(10, self.get_y(), 200, self.get_y())
        self.set_font('Helvetica', '', 7)
        self.set_text_color(*GRAY_500)
        self.set_x(10)
        self.cell(0, 6, f"Page {self.page_no()}  |  Parkho New Products Review List  |  June 2026", align='C')
        self.set_text_color(0, 0, 0)
        self.set_draw_color(0, 0, 0)


def cover(pdf):
    pdf.add_page()
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 0, 210, 297, 'F')

    # badge
    badge = "PRODUCT REVIEW CATALOG"
    pdf.set_font('Helvetica', 'B', 7)
    bw = pdf.get_string_width(badge) + 10
    pdf.set_fill_color(*ORANGE)
    pdf.rect((210-bw)/2, 42, bw, 7, 'F')
    pdf.set_text_color(*WHITE)
    pdf.set_xy((210-bw)/2, 42)
    pdf.cell(bw, 7, badge, align='C')

    pdf.set_font('Helvetica', 'B', 40)
    pdf.set_text_color(*ORANGE)
    pdf.set_xy(0, 56)
    pdf.cell(210, 16, "Parkho", align='C', ln=True)

    pdf.set_font('Helvetica', '', 13)
    pdf.set_text_color(180, 195, 215)
    pdf.set_x(0)
    pdf.cell(210, 7, "New Products -- Food & Cosmetics", align='C', ln=True)
    pdf.set_font('Helvetica', '', 10)
    pdf.set_x(0)
    pdf.cell(210, 6, "Full Ingredient Lists for Review Before Adding to Database", align='C', ln=True)

    # info boxes
    stats = [
        ("FOOD PRODUCTS", "21 Products"),
        ("COSMETIC PRODUCTS", "20 Products"),
        ("TOTAL", "41 Products"),
    ]
    total_w = 160
    box_w = total_w / len(stats)
    x0 = (210 - total_w) / 2
    y0 = 105
    for label, val in stats:
        pdf.set_fill_color(40, 65, 100)
        pdf.rect(x0, y0, box_w - 3, 22, 'F')
        pdf.set_text_color(180, 200, 230)
        pdf.set_font('Helvetica', '', 6.5)
        pdf.set_xy(x0, y0 + 3)
        pdf.cell(box_w - 3, 5, label, align='C')
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(*WHITE)
        pdf.set_xy(x0, y0 + 9)
        pdf.cell(box_w - 3, 8, val, align='C')
        x0 += box_w

    notice_y = 140
    pdf.set_fill_color(255, 240, 200)
    pdf.rect(20, notice_y, 170, 20, 'F')
    pdf.set_text_color(120, 60, 0)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_xy(22, notice_y + 3)
    pdf.cell(0, 5, "IMPORTANT NOTICE", ln=True)
    pdf.set_font('Helvetica', '', 7.5)
    pdf.set_xy(22, notice_y + 9)
    pdf.cell(0, 5, "These products are NOT yet in the Parkho database. Review and confirm before adding.", ln=True)

    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(100, 130, 170)
    pdf.set_xy(0, 170)
    pdf.cell(210, 6, "June 2026  |  www.parkho.in", align='C')

    pdf.set_fill_color(20, 35, 60)
    pdf.rect(0, 277, 210, 20, 'F')
    pdf.set_text_color(120, 150, 190)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_xy(0, 282)
    pdf.cell(210, 6, "Page 1", align='C')
    pdf.set_text_color(0, 0, 0)


def section_banner(pdf, title, subtitle, bg, fg):
    pdf.ln(4)
    pdf.set_fill_color(*bg)
    pdf.rect(10, pdf.get_y(), 190, 14, 'F')
    pdf.set_text_color(*fg)
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_xy(14, pdf.get_y() + 1.5)
    pdf.cell(0, 7, safe(title), ln=True)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_xy(14, pdf.get_y() - 1)
    pdf.cell(0, 6, safe(subtitle))
    pdf.set_y(pdf.get_y() + 7)
    pdf.set_text_color(0, 0, 0)


def product_card(pdf, num, name, brand, category, variant, net_wt, ingredients, note=None):
    # Card background
    y0 = pdf.get_y()
    # Estimate height
    ing_text = "Ingredients: " + ingredients
    char_w = 2.0
    w_available = 170
    lines_needed = max(3, len(safe(ing_text)) // int(w_available / char_w) + 1)
    note_lines = max(2, len(safe(note)) // int(w_available / char_w) + 1) if note else 0
    estimated_h = 24 + lines_needed * 4.8 + note_lines * 4.8 + 4

    # Check page break
    if y0 + estimated_h > 270:
        pdf.add_page()
        y0 = pdf.get_y()

    # Card fill
    pdf.set_fill_color(*GRAY_50)
    pdf.set_draw_color(*GRAY_200)
    pdf.set_line_width(0.3)
    pdf.rect(10, y0, 190, estimated_h, 'FD')

    # Number badge
    pdf.set_fill_color(*NAVY_MED)
    pdf.rect(10, y0, 10, 10, 'F')
    pdf.set_text_color(*WHITE)
    pdf.set_font('Helvetica', 'B', 7)
    pdf.set_xy(10, y0 + 1.5)
    pdf.cell(10, 7, str(num), align='C')

    # Product name
    pdf.set_text_color(*GRAY_900)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_xy(22, y0 + 1.5)
    pdf.cell(0, 5, safe(name), ln=True)

    # Brand | Category | Variant | Net Wt row
    meta_y = y0 + 7.5
    pdf.set_font('Helvetica', '', 7.5)
    pdf.set_text_color(*GRAY_500)
    pdf.set_xy(22, meta_y)
    pdf.cell(35, 5, safe(f"Brand: {brand}"))
    pdf.cell(50, 5, safe(f"Category: {category}"))
    pdf.cell(50, 5, safe(f"Variant: {variant}"))
    pdf.cell(0, 5, safe(f"Net Wt: {net_wt}"))
    pdf.ln(6)

    # Divider
    pdf.set_draw_color(*GRAY_200)
    pdf.line(12, pdf.get_y(), 198, pdf.get_y())
    pdf.ln(2)

    # Ingredients
    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.set_text_color(*NAVY_MED)
    pdf.set_x(13)
    pdf.cell(22, 5, "Ingredients:", ln=False)
    pdf.set_font('Helvetica', '', 7.5)
    pdf.set_text_color(*GRAY_700)
    pdf.multi_cell(165, 4.8, safe(ingredients), align='L')

    # Note
    if note:
        pdf.set_x(13)
        pdf.set_font('Helvetica', 'I', 7)
        pdf.set_text_color(*AMBER_FG)
        pdf.cell(20, 4.5, "Note:", ln=False)
        pdf.set_text_color(*GRAY_500)
        pdf.multi_cell(165, 4.5, safe(note), align='L')

    pdf.set_y(y0 + estimated_h + 2)
    pdf.set_text_color(0, 0, 0)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.2)


# ── Product Data ──────────────────────────────────────────────────────────────

FOOD_PRODUCTS = [

    ("Nestle KitKat 4 Finger", "Nestle", "Chocolates & Candy", "4 Finger Bar", "41.5 g",
     "Sugar, Cocoa Butter, Skimmed Milk Powder, Cocoa Mass, Wheat Flour, Vegetable Fat (Palm), Lactose, Whole Milk Powder, Whey Powder (from Milk), Raising Agents (Sodium Bicarbonate, Ammonium Bicarbonate), Emulsifiers (Soy Lecithin, INS 476), Salt, Flavour (Vanillin).",
     "Contains: Milk, Soy, Wheat, Gluten. May contain traces of Peanuts and Tree Nuts."),

    ("Nestle Munch", "Nestle", "Chocolates & Candy", "Original", "18 g",
     "Sugar, Glucose, Hydrogenated Vegetable Fat, Wheat Flour, Cocoa Solids, Milk Solids, Invert Sugar, Emulsifiers (INS 322, INS 476), Salt, Raising Agents (INS 500(ii), INS 503(ii)), Colour (INS 150a), Flavours.",
     "Contains Milk, Wheat, Gluten and Soy derivatives."),

    ("Nestle Milkybar", "Nestle", "Chocolates & Candy", "Original White Chocolate", "13 g",
     "Sugar, Whole Milk Powder, Cocoa Butter, Skimmed Milk Powder, Wheat Flour, Lactose (Milk), Emulsifiers (Soy Lecithin, INS 476), Raising Agents (Sodium Bicarbonate, Ammonium Bicarbonate), Salt, Flavour (Vanillin).",
     "Contains Milk, Wheat, Gluten, Soy. May contain traces of Peanuts."),

    ("Cadbury Gems", "Cadbury (Mondelez)", "Chocolates & Candy", "Original", "24 g",
     "Sugar, Cocoa Butter, Skimmed Milk Powder, Cocoa Mass, Lactose, Vegetable Fats (Palm, Shea), Whey Permeate Powder, Emulsifier (Soy Lecithin), Glucose Syrup, Starch (Rice, Potato, Maize), Colours (INS 110, INS 124, INS 102, INS 133, INS 132), Glazing Agent (Carnauba Wax, Shellac), Flavour.",
     "Contains Milk, Soy. Colours INS 110, 124, 102 are artificial food colours."),

    ("Parle Monaco Classic", "Parle", "Biscuits", "Classic Salted", "150 g",
     "Refined Wheat Flour (Maida), Edible Vegetable Oil (Palm Oil), Sugar, Invert Sugar Syrup, Salt, Raising Agents (INS 503(ii), INS 500(ii)), Emulsifier (INS 322), Acidity Regulator (INS 330), Yeast, Dough Conditioner (INS 920).",
     None),

    ("Parle Krackjack", "Parle", "Biscuits", "Sweet & Salty", "300 g",
     "Refined Wheat Flour (Maida), Edible Vegetable Oil (Palm Oil), Sugar, Liquid Glucose, Invert Sugar Syrup, Salt, Raising Agents (INS 503(ii), INS 500(ii)), Emulsifier (INS 322), Dough Conditioner (INS 920), Acidity Regulator (INS 270), Yeast.",
     None),

    ("Britannia Marie Gold", "Britannia", "Biscuits", "Classic", "250 g",
     "Refined Wheat Flour (Maida), Sugar, Edible Vegetable Oil (Palm Oil), Invert Sugar Syrup, Wheat Bran, Raising Agents (Ammonium Bicarbonate, Sodium Bicarbonate), Salt, Emulsifier (Soy Lecithin INS 322), Flavour (Vanilla).",
     None),

    ("Britannia Good Day Butter Cookies", "Britannia", "Biscuits", "Butter", "150 g",
     "Refined Wheat Flour (Maida), Sugar, Edible Vegetable Oil (Palm Olein), Liquid Glucose, Invert Sugar Syrup, Milk Solids, Butter (3%), Salt, Raising Agents (INS 500(ii), INS 503(ii)), Emulsifier (INS 322), Flavour (Artificial Butter).",
     None),

    ("Tropicana 100% Orange Juice", "PepsiCo (Tropicana)", "Beverages", "100% Orange", "1 L",
     "100% Orange Juice from Concentrate (Water, Orange Juice Concentrate), Vitamin C (Ascorbic Acid).",
     "No added sugar. No artificial flavours or preservatives. Reconstituted from concentrate."),

    ("Paper Boat Frooti Mango Drink", "Hector Beverages", "Beverages", "Mango Fruit Drink", "200 mL",
     "Water, Mango Pulp (27%), Sugar, Citric Acid (INS 330), Antioxidant (Ascorbic Acid INS 300), Salt, Guar Gum (INS 412), Colour (Beta-Carotene INS 160a), Preservative (Potassium Sorbate INS 202).",
     None),

    ("Minute Maid Pulpy Orange", "Coca-Cola India", "Beverages", "Orange Drink", "400 mL",
     "Water, Sugar, Orange Pulp (3%), Orange Juice Concentrate (1.5%), Acidity Regulator (Citric Acid INS 330), Stabilisers (Cellulose Gum INS 466, Pectin INS 440), Colour (INS 110 Sunset Yellow), Flavour (Natural Orange).",
     "Contains artificial colour INS 110 (Sunset Yellow) -- may affect activity in children."),

    ("Red Bull Energy Drink", "Red Bull", "Beverages", "Original (Blue-Silver)", "250 mL",
     "Water, Sucrose, Glucose, Citric Acid (INS 330), Taurine (0.4%), Sodium Citrate (INS 331), Magnesium Carbonate (INS 504), Caffeine (0.03%), Niacinamide (Vitamin B3), Calcium Pantothenate (Vitamin B5), Pyridoxine HCl (Vitamin B6), Cyanocobalamin (Vitamin B12), Colour (INS 150a Caramel), Flavours.",
     "Contains 80 mg caffeine per 250 mL. Not recommended for children, pregnant women, or persons sensitive to caffeine."),

    ("Sting Energy Drink", "PepsiCo", "Beverages", "Berry Blast", "250 mL",
     "Carbonated Water, Sugar, Glucose, Citric Acid (INS 330), Taurine, Caffeine, Sodium Citrate (INS 331), Inositol, Colour (INS 122, INS 124), Acesulfame Potassium (INS 950), Sucralose (INS 955), Flavours, Vitamins (B3, B6, B12).",
     "Contains caffeine (32 mg/100 mL) and artificial colours INS 122 and 124. Not for children."),

    ("Quaker Oats Original", "PepsiCo (Quaker)", "Breakfast Cereals", "Original Oats", "500 g",
     "Whole Grain Rolled Oats (100%). No added sugar, salt or preservatives.",
     "Rich in Beta-Glucan dietary fibre. Contains Gluten."),

    ("Kellogg's Corn Flakes", "Kellogg's", "Breakfast Cereals", "Original", "250 g",
     "Milled Corn (Corn Grits 91%), Sugar, Salt, Malt Flavour (from Barley), Vitamins & Iron (Niacinamide, Vitamin A, Vitamin B6, Vitamin B2, Folic Acid, Vitamin B12, Iron), Colour (INS 150a).",
     "Contains Maize and Barley (Gluten). May contain traces of Wheat, Soy and Milk."),

    ("Kellogg's Chocos", "Kellogg's", "Breakfast Cereals", "Choco Fills", "375 g",
     "Whole Grain Wheat (59%), Sugar, Cocoa Powder (4%), Wheat Starch, Salt, Colour (INS 150d), Emulsifier (Soy Lecithin INS 322), Vitamins & Minerals (Niacinamide, Iron, Zinc, Vitamin B6, Riboflavin, Vitamin B12, Folic Acid, Vitamin A, Vitamin D3), Flavour.",
     "High in sugar (33g per 100g). Contains Wheat, Soy."),

    ("Yippee Noodles Magic Masala", "ITC Sunfeast", "Instant Noodles", "Magic Masala", "65 g",
     "Noodle Cake: Refined Wheat Flour (Maida 92%), Refined Palm Oil, Salt, Minerals (INS 451(i), INS 500(i)), Colour (INS 101ii). Taste Maker: Iodised Salt, Sugar, Spices and Condiments (Coriander, Chilli, Turmeric, Cumin, Garam Masala), Dehydrated Vegetables (Onion, Tomato), Flavour Enhancer (INS 621 MSG, INS 627, INS 631), Acidity Regulator (INS 330), Colour (INS 110, INS 100ii), Anticaking Agent (INS 551), Hydrogenated Vegetable Fat.",
     "Contains MSG (INS 621) and artificial colour INS 110 (Sunset Yellow). Contains Gluten (Wheat)."),

    ("Knorr Classic Tomato Soup", "HUL (Knorr)", "Instant Soups", "Classic Tomato", "46 g",
     "Wheat Flour, Sugar, Tomato Powder (10%), Salt, Corn Starch, Edible Vegetable Oil (Palm), Maltodextrin, Skimmed Milk Powder, Tomato Flakes (1%), Tomato Puree Powder, Flavour Enhancers (INS 621, INS 627, INS 631), Flavour (Tomato), Acidity Regulator (INS 330), Spices, Anticaking Agent (INS 551).",
     "Contains Wheat (Gluten), Milk, Soy. Contains MSG (INS 621)."),

    ("Kissan Mixed Fruit Jam", "HUL (Kissan)", "Spreads & Jams", "Mixed Fruit", "500 g",
     "Sugar, Mixed Fruit Pulp & Juice (Mango, Papaya, Pineapple, Banana) (45%), Acidity Regulator (INS 330 Citric Acid), Pectin (INS 440), Preservative (Sodium Benzoate INS 211), Colour (INS 110 Sunset Yellow, INS 129 Allura Red).",
     "Contains preservative Sodium Benzoate (INS 211) and artificial colours INS 110 and 129."),

    ("Yoga Bar Oats & Berries Bar", "Yoga Bar (ITC)", "Health Bars", "Oats & Berries", "38 g",
     "Oats (55%), Mixed Berries (Cranberry, Raisin, Blueberry 14%), Brown Rice Crisps, Rice Syrup, Honey, Sunflower Seeds, Flax Seeds, Pumpkin Seeds, Rolled Wheat, Soy Crisps (Soy Protein Isolate), Dark Chocolate (Cocoa Mass, Sugar, Cocoa Butter, Soy Lecithin), Salt.",
     "Contains Gluten (Oats, Wheat), Soy, Milk traces. No artificial flavours or preservatives."),

    ("Too Yumm Multigrain Chips", "Guiltfree Industries (RP-Sanjiv Goenka)", "Chips & Crisps", "Multigrain Original", "42 g",
     "Multigrain Mix (Corn, Rice, Oats, Soya, Wheat 70%), Edible Vegetable Oil (Rice Bran Oil), Iodised Salt, Sugar, Maltodextrin, Acidity Regulator (INS 330), Hydrolysed Corn Protein, Spices, Anticaking Agent (INS 551).",
     "Baked, not fried. Contains Wheat, Soy, Oat (Gluten). 30% less fat than regular potato chips."),

]

COSMETIC_PRODUCTS = [

    ("Himalaya Nourishing Skin Cream", "Himalaya", "Skincare / Moisturizer", "Original", "50 mL",
     "Aqua, Aloe Barbadensis (Aloe Vera) Leaf Extract, Glycerin, Cetearyl Alcohol, Mineral Oil, Stearic Acid, Vitis Vinifera (Grape) Seed Oil, Glyceryl Stearate, Sodium Stearoyl Lactylate, Prunus Amygdalus Dulcis (Sweet Almond) Oil, Butyrospermum Parkii (Shea Butter), Carbomer, Triethanolamine, Allantoin, Sodium PCA, Diazolidinyl Urea, Iodopropynyl Butylcarbamate, Parfum.",
     "Contains Diazolidinyl Urea (formaldehyde releaser, rated 5 on EWG) and Triethanolamine."),

    ("Himalaya Aloe Vera Face Wash", "Himalaya", "Skincare / Face Wash", "Moisturizing", "100 mL",
     "Aqua, Aloe Barbadensis (Aloe Vera) Leaf Extract, Cocamidopropyl Betaine, Sodium Laureth Sulfate, Glycerin, Propylene Glycol, PEG-7 Glyceryl Cocoate, Citric Acid, Disodium EDTA, Benzophenone-4, Methylparaben, Propylparaben, Parfum.",
     "Contains SLES (surfactant), Parabens (Methylparaben, Propylparaben) and Benzophenone-4."),

    ("Himalaya Anti-Dandruff Shampoo", "Himalaya", "Haircare / Shampoo", "Anti-Dandruff", "400 mL",
     "Aqua, Sodium Laureth Sulfate, Cocamidopropyl Betaine, Glycol Distearate, Sodium Chloride, Glycerin, Zinc Pyrithione (1%), Selenium Disulfide (0.1%), Tea Tree Leaf Oil (Melaleuca Alternifolia), Neem (Azadirachta Indica) Leaf Extract, Aloe Barbadensis Extract, Dimethicone, Carbomer, Citric Acid, Sodium Benzoate, DMDM Hydantoin, Parfum.",
     "Contains Zinc Pyrithione (anti-dandruff active), DMDM Hydantoin (formaldehyde releaser) and SLES."),

    ("St. Ives Apricot Scrub", "Unilever (St. Ives)", "Skincare / Face Scrub", "Exfoliate & Unclog Pores", "150 mL",
     "Water, Walnut Shell Powder, Glycerin, Sodium C14-16 Olefin Sulfonate, Cocamidopropyl Betaine, Propylene Glycol, Acrylates/C10-30 Alkyl Acrylate Crosspolymer, Sodium Hydroxide, Prunus Armeniaca (Apricot) Kernel Oil, Citric Acid, DMDM Hydantoin, Methylisothiazolinone, Parfum.",
     "Physical scrub with walnut shell powder. Contains DMDM Hydantoin (formaldehyde releaser) and Methylisothiazolinone (skin sensitizer at rinse-off concentration per EU Scientific Committee)."),

    ("Re'equil Oxi-Moist Moisturizer", "Re'equil", "Skincare / Moisturizer", "SPF 15 PA++", "50 g",
     "Aqua, Ethylhexyl Methoxycinnamate, Glycerin, Ethylhexyl Salicylate, Dimethicone, Cyclomethicone, Niacinamide, Cetyl Alcohol, Stearyl Alcohol, Polyacrylate-13, Vitamin E (Tocopheryl Acetate), Allantoin, Aloe Barbadensis Extract, Disodium EDTA, Phenoxyethanol, Ethylhexylglycerin, Parfum.",
     "Contains chemical sunscreen filters Ethylhexyl Methoxycinnamate and Ethylhexyl Salicylate. Fragrance-free options available."),

    ("Fixderma Sunscreen SPF 30", "Fixderma", "Skincare / Sunscreen", "Shadow SPF 30 PA+++", "75 g",
     "Avobenzone (3%), Octinoxate (7.5%), Oxybenzone (2%), Aqua, Glycerin, Niacinamide, Dimethicone, Cyclomethicone, Cetearyl Alcohol, Ceteareth-20, Titanium Dioxide, Zinc Oxide, Aloe Vera Extract, Vitamin C (Ascorbic Acid), Vitamin E (Tocopheryl Acetate), Phenoxyethanol, Methylparaben, Parfum.",
     "Contains Oxybenzone -- avoid use on large body areas or by children under 6 months. Also contains Methylparaben."),

    ("Pilgrim Salicylic Acid 2% Face Wash", "Pilgrim", "Skincare / Face Wash", "Salicylic Acid + Green Tea", "100 mL",
     "Aqua, Cocamidopropyl Betaine, Sodium Cocoyl Isethionate, Glycerin, Salicylic Acid (2%), Camellia Sinensis (Green Tea) Leaf Extract, Niacinamide, Willow Bark Extract (Salix Alba), Panthenol, Allantoin, Zinc PCA, Sodium Benzoate, Citric Acid, Disodium EDTA, Phenoxyethanol.",
     "Salicylic acid 2% is BHA -- use with sun protection as it increases photosensitivity."),

    ("Pilgrim Red Vine Anti-Aging Serum", "Pilgrim", "Skincare / Serum", "Red Vine + Hyaluronic Acid", "30 mL",
     "Aqua, Niacinamide (5%), Hyaluronic Acid (Sodium Hyaluronate), Vitis Vinifera (Red Grape) Seed Extract (Resveratrol), Panthenol (Vitamin B5), Glycerin, Propylene Glycol, Carbomer, Triethanolamine, Allantoin, Disodium EDTA, Phenoxyethanol, Ethylhexylglycerin.",
     "Contains Triethanolamine (can form nitrosamines with certain preservatives at high concentration). Generally safe at cosmetic use levels."),

    ("Derma Co 1% Hyaluronic Acid Serum", "The Derma Co (Honasa)", "Skincare / Serum", "1% Hyaluronic Acid + 5 Molecular Weights", "30 mL",
     "Aqua, Glycerin, Sodium Hyaluronate, Hyaluronic Acid, Hydrolyzed Hyaluronic Acid, Sodium Acetylated Hyaluronate, Hydroxypropyltrimonium Hyaluronate, Panthenol, Allantoin, Niacinamide, Betaine, Phenoxyethanol, Ethylhexylglycerin, Disodium EDTA, Xanthan Gum.",
     "Contains 5 forms of Hyaluronic Acid at different molecular weights for deep and surface hydration."),

    ("Derma Co 0.3% Retinol Night Serum", "The Derma Co (Honasa)", "Skincare / Serum", "0.3% Retinol + Peptide", "30 mL",
     "Aqua, Cyclopentasiloxane, Dimethicone/Vinyl Dimethicone Crosspolymer, Glycerin, Retinol (0.3%), Palmitoyl Tripeptide-5, Tocopheryl Acetate (Vitamin E), Hyaluronic Acid (Sodium Hyaluronate), Niacinamide, Bakuchiol, Jojoba Oil (Simmondsia Chinensis), Phenoxyethanol, Ethylhexylglycerin, BHT.",
     "Retinol 0.3% -- start with 2x per week use. Avoid during pregnancy. Always use SPF during day when using retinol."),

    ("Kama Ayurveda Kumkumadi Miracle Youth Oil", "Kama Ayurveda", "Skincare / Face Oil", "Miraculous Beauty Fluid", "12 mL",
     "Sesamum Indicum (Sesame) Seed Oil, Crocus Sativus (Saffron) Stigma Extract, Rubia Cordifolia (Manjistha) Root Extract, Vetiveria Zizanioides (Vetiver) Root Extract, Glycyrrhiza Glabra (Liquorice) Root Extract, Nelumbo Nucifera (Lotus) Petal Extract, Santalum Album (Sandalwood) Heartwood Oil, Rosa Damascena (Rose) Essential Oil, Boerhavia Diffusa (Punarnava) Root Extract.",
     "No preservatives, parabens, or artificial fragrance. Pure botanical oil formula. Patch test recommended -- Sesame oil allergy possible."),

    ("Beardo Beard & Hair Growth Oil", "Beardo", "Haircare / Beard Oil", "Beard & Hair Growth", "50 mL",
     "Argania Spinosa (Argan) Kernel Oil, Simmondsia Chinensis (Jojoba) Seed Oil, Ricinus Communis (Castor) Seed Oil, Vitis Vinifera (Grape) Seed Oil, Tocopherol (Vitamin E), Redensyl (Larix Europaea Wood Extract, Glycine, Zinc Chloride), Procapil (Biotinyl GHK Tripeptide-3, Apigenin, Oleanolic Acid), Bhringraj (Eclipta Prostrata) Extract, Rosmarinus Officinalis (Rosemary) Leaf Oil.",
     "Contains Redensyl and Procapil -- clinically studied hair growth peptides. Castor oil is thick; use sparingly."),

    ("Mars by GHC Hair Growth Serum", "The Good Health Company (GHC)", "Haircare / Scalp Serum", "5% Minoxidil Scalp Serum", "60 mL",
     "Minoxidil (5%), Propylene Glycol, Ethanol, Redensyl (Larix Europaea Wood Extract), Capilia Longa (Curcuma Longa Callus Extract), Anagain (Pisum Sativum Sprout Extract), Procapil (Biotinyl GHK Tripeptide-3, Apigenin, Oleanolic Acid), Biotin, Aqua.",
     "PRESCRIPTION / OTC DRUG: Contains 5% Minoxidil -- FDA approved for male pattern baldness. Not for women or under 18. Side effects possible including scalp irritation, unwanted facial hair growth. Consult doctor before use."),

    ("Plum Green Tea Face Wash", "Plum", "Skincare / Face Wash", "Pore-Cleansing", "100 mL",
     "Aqua, Decyl Glucoside, Cocamidopropyl Betaine, Camellia Sinensis (Green Tea) Leaf Extract, Glycerin, Niacinamide, Willow Bark Extract (Salicylic Acid 0.5%), Allantoin, Panthenol, Disodium Cocoamphodiacetate, Citric Acid, Sodium Benzoate, Potassium Sorbate, Xanthan Gum.",
     "Free from SLS, SLES, Parabens, Artificial Fragrance and Silicones. Preservatives Sodium Benzoate and Potassium Sorbate."),

    ("Aqualogica Glow+ Dewy Sunscreen", "Aqualogica", "Skincare / Sunscreen", "SPF 50 PA++++", "50 g",
     "Ethylhexyl Methoxycinnamate (7.5%), Ethylhexyl Salicylate (5%), Butyl Methoxydibenzoylmethane (3%), Aqua, Dimethicone, Glycerin, Niacinamide, Watermelon Fruit Extract (Citrullus Lanatus), Hyaluronic Acid (Sodium Hyaluronate), Vitamin E (Tocopheryl Acetate), Pentylene Glycol, Phenoxyethanol, Carbomer, Triethanolamine.",
     "Chemical sunscreen with 3 UV filters. Dewy finish. Suitable for normal to dry skin."),

    ("Fixderma Shadow SPF 50+ Sunscreen Gel", "Fixderma", "Skincare / Sunscreen", "SPF 50+ PA++++", "50 g",
     "Ethylhexyl Methoxycinnamate (7.5%), Uvinul A Plus (Butyl Methoxydibenzoylmethane 3.5%), Uvinul T 150 (Ethylhexyl Triazone 3%), Aqua, Glycerin, Niacinamide, Aloe Vera (Aloe Barbadensis) Leaf Juice, Vitamin E (Tocopheryl Acetate), Hydroxypropyl Cellulose, Carbomer, Sodium Hydroxide, Disodium EDTA, Phenoxyethanol, Ethylhexylglycerin.",
     "Broad spectrum with 3 chemical UV filters. Lightweight gel formula. No white cast."),

    ("Wild Stone Ultra Sensual Body Spray", "JK Helene Curtis", "Fragrance / Deodorant", "Ultra Sensual for Men", "150 mL",
     "Alcohol Denat., Aqua, Parfum, Butane, Propane, Isobutane, Dimethyl Ether, Cyclopentasiloxane, Isopropyl Myristate, Benzyl Salicylate, Linalool, Limonene, Geraniol, Hexyl Cinnamal, Coumarin, Benzyl Benzoate, Citronellol, Alpha-Isomethyl Ionone, Eugenol, Hydroxycitronellal, Amyl Cinnamal.",
     "Contains multiple EU fragrance allergens: Linalool, Limonene, Geraniol, Hexyl Cinnamal, Coumarin, Benzyl Benzoate, Citronellol, Eugenol. Spray deodorant with propellant gases."),

    ("Fogg Scent Xpression Deodorant", "Vini Cosmetics", "Fragrance / Deodorant", "Xpression for Men", "150 mL",
     "Alcohol (SD Alcohol 40-B), Parfum, Dimethyl Ether, Cyclopentasiloxane, Isopropyl Myristate, Butylphenyl Methylpropional (Lilial), Linalool, Limonene, Citronellol, Geraniol, Benzyl Salicylate, Amyl Cinnamal, Hexyl Cinnamal, Coumarin, Butane, Propane, Isobutane.",
     "Contains Butylphenyl Methylpropional (Lilial) -- banned in EU since March 2022 as suspected endocrine disruptor. Also contains multiple fragrance allergens. Check for updated formula without Lilial."),

    ("Engage W1 Perfume Spray (Women)", "ITC", "Fragrance / Perfume", "W1 for Women", "150 mL",
     "Alcohol Denat., Aqua, Parfum, Dimethyl Ether, Benzyl Salicylate, Linalool, Limonene, Hexyl Cinnamal, Alpha-Isomethyl Ionone, Citronellol, Geraniol, Hydroxyisohexyl 3-Cyclohexene Carboxaldehyde (HICC), Coumarin, Butylphenyl Methylpropional, Amyl Cinnamal, Butane, Propane, Isobutane.",
     "Contains HICC (Hydroxyisohexyl 3-Cyclohexene Carboxaldehyde) -- banned in EU due to high sensitization risk. Also contains Butylphenyl Methylpropional (EU banned). Verify formula version before adding."),

    ("Sugar Cosmetics Aquaholic Sunscreen", "Sugar Cosmetics", "Skincare / Sunscreen", "SPF 50 PA++++ Aquaholic Cooling Matte", "50 g",
     "Ethylhexyl Methoxycinnamate (7%), Bis-Ethylhexyloxyphenol Methoxyphenyl Triazine (Tinosorb S 3%), Ethylhexyl Triazone (3%), Aqua, Glycerin, Niacinamide, Cucumber Fruit Extract (Cucumis Sativus), Menthol, Hyaluronic Acid (Sodium Hyaluronate), Silica, Dimethicone, Carbomer, Sodium Hydroxide, Disodium EDTA, Phenoxyethanol, Ethylhexylglycerin.",
     "Contains Tinosorb S (Bis-Ethylhexyloxyphenol Methoxyphenyl Triazine) -- next-gen broad spectrum filter approved in EU/India but not yet FDA approved for USA. Cooling effect from Menthol."),

]


# ── Build PDF ─────────────────────────────────────────────────────────────────

def build(pdf):
    cover(pdf)

    # ── Food Products ─────────────────────────────────────────────────────────
    pdf.add_page()
    section_banner(pdf,
        "[FOOD PRODUCTS]  -- 21 Products",
        "Chocolates, Biscuits, Beverages, Breakfast Cereals, Instant Foods, Health Bars",
        GREEN_BG, GREEN_FG)

    for i, p in enumerate(FOOD_PRODUCTS, 1):
        product_card(pdf, i, *p)

    # ── Cosmetic Products ─────────────────────────────────────────────────────
    pdf.add_page()
    section_banner(pdf,
        "[COSMETIC PRODUCTS]  -- 20 Products",
        "Skincare, Sunscreens, Haircare, Face Washes, Serums, Deodorants & Perfumes",
        PINK_BG, PINK_FG)

    for i, p in enumerate(COSMETIC_PRODUCTS, 1):
        product_card(pdf, i, *p)

    # ── Summary Table ─────────────────────────────────────────────────────────
    pdf.add_page()
    section_banner(pdf, "[QUICK REFERENCE]  -- All Products at a Glance", "", BLUE_BG, BLUE_FG)

    # Header row
    pdf.set_fill_color(*NAVY_MED)
    pdf.set_text_color(*WHITE)
    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.set_x(10)
    for col, w in [("#", 8), ("Product Name", 80), ("Brand", 35), ("Category", 40), ("Net Wt", 27)]:
        pdf.cell(w, 7, col, border=1, fill=True)
    pdf.ln(7)

    all_products = [("FOOD", p) for p in FOOD_PRODUCTS] + [("COSMETIC", p) for p in COSMETIC_PRODUCTS]
    for idx, (ptype, p) in enumerate(all_products, 1):
        fill = idx % 2 == 0
        pdf.set_fill_color(*(GRAY_50 if fill else WHITE))
        pdf.set_text_color(*GRAY_900)
        pdf.set_font('Helvetica', '', 7.5)
        pdf.set_x(10)
        name, brand, category, variant, net_wt = p[0], p[1], p[2], p[3], p[4]
        pdf.cell(8,  6, str(idx),        border=1, fill=fill)
        pdf.cell(80, 6, safe(name[:45] + ('...' if len(name) > 45 else '')), border=1, fill=fill)
        pdf.cell(35, 6, safe(brand[:20]),     border=1, fill=fill)
        pdf.cell(40, 6, safe(category[:25]),  border=1, fill=fill)
        pdf.cell(27, 6, safe(net_wt),         border=1, fill=fill)
        pdf.ln(6)

    # Legend
    pdf.ln(6)
    pdf.set_draw_color(*GRAY_200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(*ORANGE)
    pdf.set_x(10)
    pdf.cell(0, 5, "Ingredients flagged with notes marked in amber -- verify classification before adding to database.", ln=True)
    pdf.set_font('Helvetica', '', 7.5)
    pdf.set_text_color(*GRAY_500)
    pdf.set_x(10)
    pdf.cell(0, 5, "Ingredient lists are based on publicly available label information. Verify with actual product packaging before database entry.", ln=True)
    pdf.set_x(10)
    pdf.cell(0, 5, "Some products (Mars GHC 5% Minoxidil, Fogg Xpression, Engage W1) may require special classification -- see notes.", ln=True)
    pdf.set_text_color(0, 0, 0)


def main():
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.set_margins(10, 12, 10)
    build(pdf)
    pdf.output(OUT)
    print(f"Done: {OUT}  ({pdf.page} pages)")

if __name__ == "__main__":
    main()
