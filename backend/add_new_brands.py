"""Add Beardo, The Ordinary, Ustraa, Bombay Shaving Co, more Minimalist,
Old Spice, Gillette, Park Avenue, Brylcreem, Axe, and other new brands."""

# ── NEW PRODUCT DATA (name, brand, category, score, verdict, recommendation) ──
NEW_PRODUCTS = {

    # ─── BEARDO (men's grooming) ──────────────────────────────────────────────
    "beardo-godfather-beard-oil": (
        "Beardo Godfather Beard Oil",
        "Beardo", "Hair Care", 88,
        "Pure carrier oils, no harmful additives",
        "Blend of sweet almond, argan and jojoba oils. No mineral oil or silicones."
    ),
    "beardo-beard-wash": (
        "Beardo Beard Wash",
        "Beardo", "Hair Care", 65,
        "Contains mild surfactants and conditioning agents",
        "Sodium laureth sulphate base with conditioning agents. Contains methylisothiazolinone preservative."
    ),
    "beardo-activated-charcoal-face-wash": (
        "Beardo Activated Charcoal Face Wash",
        "Beardo", "Personal Care", 68,
        "Charcoal-based deep cleansing face wash",
        "Contains activated charcoal for deep pore cleansing. SLS-based — can be drying with daily use."
    ),
    "beardo-d-tan-face-wash": (
        "Beardo D-Tan Face Wash",
        "Beardo", "Personal Care", 65,
        "Exfoliating de-tanning face wash",
        "Contains kojic acid and papain enzyme for de-tanning. SLS base may irritate sensitive skin."
    ),
    "beardo-spf50-sunscreen": (
        "Beardo SPF 50 PA+++ Sunscreen",
        "Beardo", "Skincare", 70,
        "Chemical sunscreen with niacinamide",
        "Contains avobenzone and octinoxate UV filters with niacinamide for brightening. Paraben-free."
    ),
    "beardo-beard-hair-wax": (
        "Beardo Beard & Hair Wax",
        "Beardo", "Hair Care", 58,
        "Styling wax with synthetic polymers",
        "Contains beeswax, petroleum jelly and synthetic polymers. Strong hold with fragrance."
    ),
    "beardo-hair-serum": (
        "Beardo Hair Serum",
        "Beardo", "Hair Care", 65,
        "Silicone-based hair serum for frizz control",
        "Contains dimethicone and cyclopentasiloxane for frizz control. Provides temporary smoothing."
    ),
    "beardo-moisturizer": (
        "Beardo De-Tan SPF 30 Moisturizer",
        "Beardo", "Skincare", 68,
        "SPF moisturizer with de-tanning agents",
        "Contains kojic acid, niacinamide and SPF 30. Paraben-free formula for daily use."
    ),
    "beardo-beard-growth-serum": (
        "Beardo Beard Growth Serum",
        "Beardo", "Hair Care", 72,
        "Beard growth actives with natural oils",
        "Contains minoxidil-free growth actives: caffeine, biotin and redensyl with carrier oils."
    ),

    # ─── THE ORDINARY ─────────────────────────────────────────────────────────
    "the-ordinary-niacinamide": (
        "The Ordinary Niacinamide 10% + Zinc 1% Serum",
        "The Ordinary", "Skincare", 84,
        "Well-formulated niacinamide serum with zinc",
        "10% niacinamide with zinc PCA; targets pores, excess oil and uneven tone. No parabens or silicones."
    ),
    "the-ordinary-hyaluronic-acid": (
        "The Ordinary Hyaluronic Acid 2% + B5",
        "The Ordinary", "Skincare", 86,
        "Excellent multi-molecular hydrating serum",
        "Three weights of HA with panthenol (B5) for surface and deep hydration. Clean, minimal formula."
    ),
    "the-ordinary-aha-bha-peeling": (
        "The Ordinary AHA 30% + BHA 2% Peeling Solution",
        "The Ordinary", "Skincare", 62,
        "Very strong acid exfoliant — use with caution",
        "30% glycolic + lactic acids with 2% salicylic acid. Strong — 10 min max, avoid sensitive skin."
    ),
    "the-ordinary-vitamin-c-suspension": (
        "The Ordinary Vitamin C Suspension 23% + HA Spheres 2%",
        "The Ordinary", "Skincare", 70,
        "High-potency pure ascorbic acid suspension",
        "23% L-ascorbic acid — most potent but least stable form. May tingle on first use. Store cool."
    ),
    "the-ordinary-retinol": (
        "The Ordinary Retinol 0.5% in Squalane",
        "The Ordinary", "Skincare", 72,
        "Mid-strength retinol in stable squalane base",
        "0.5% retinol in squalane base — reduces irritation. Use SPF, avoid pregnancy. Start slow."
    ),
    "the-ordinary-buffet-serum": (
        "The Ordinary Buffet Multi-Technology Serum",
        "The Ordinary", "Skincare", 82,
        "Multi-peptide serum targeting multiple signs of ageing",
        "Contains Matrixyl 3000, Argireline, HA, amino acids and probiotics. Comprehensive anti-ageing."
    ),
    "the-ordinary-natural-moisturizing": (
        "The Ordinary Natural Moisturizing Factors + HA",
        "The Ordinary", "Skincare", 85,
        "Excellent basic moisturiser with skin-identical ingredients",
        "Amino acids, hyaluronic acid, ceramides and urea — mirrors skin's own NMF. No parabens."
    ),
    "the-ordinary-squalane-cleanser": (
        "The Ordinary Squalane Cleanser",
        "The Ordinary", "Skincare", 84,
        "Gentle balm-to-milk cleanser with squalane",
        "Squalane base with plant-derived ester. Melts makeup without stripping. No SLS, no parabens."
    ),
    "the-ordinary-lactic-acid": (
        "The Ordinary Lactic Acid 10% + HA",
        "The Ordinary", "Skincare", 74,
        "Gentle exfoliating serum suitable for beginners",
        "10% lactic acid (gentler than glycolic) for brightening and mild exfoliation. With HA for hydration."
    ),

    # ─── MORE MINIMALIST ──────────────────────────────────────────────────────
    "minimalist-zinc-face-wash": (
        "Minimalist Zinc + Niacinamide Face Wash",
        "Minimalist", "Skincare", 76,
        "SLS-free cleanser for acne-prone skin",
        "Zinc PCA and niacinamide base; no SLS, no parabens. Gentle enough for twice-daily use."
    ),
    "minimalist-tranexamic-acid": (
        "Minimalist Tranexamic Acid 3% Serum",
        "Minimalist", "Skincare", 78,
        "Brightening serum safe for all skin tones",
        "Tranexamic acid 3% reduces hyperpigmentation and dark spots. Works well alongside niacinamide."
    ),
    "minimalist-squalane": (
        "Minimalist Squalane 100%",
        "Minimalist", "Skincare", 92,
        "Pure plant-derived squalane — excellent skin-identical oil",
        "100% plant-derived squalane from sugarcane. Non-comedogenic, lightweight, no additives."
    ),
    "minimalist-mandelic-acid": (
        "Minimalist Mandelic Acid 10% Face Serum",
        "Minimalist", "Skincare", 74,
        "Gentle AHA exfoliant ideal for sensitive skin",
        "Mandelic acid is the gentlest AHA due to large molecular size. Good for sensitive and dark skin."
    ),
    "minimalist-omega-water-cream": (
        "Minimalist Omega Water Cream Moisturizer",
        "Minimalist", "Skincare", 82,
        "Lightweight barrier-repair moisturizer with omega fatty acids",
        "Omega 3, 6, 9 fatty acids with ceramides and niacinamide. Gel-cream texture, paraben-free."
    ),
    "minimalist-sunscreen-spf50-spray": (
        "Minimalist SPF 50 PA++++ Invisible Sunscreen Spray",
        "Minimalist", "Skincare", 72,
        "Lightweight spray sunscreen for reapplication",
        "Alcohol-based spray for easy reapplication; UV filters with no white cast. Avoid inhaling spray."
    ),

    # ─── USTRAA (men's grooming) ──────────────────────────────────────────────
    "ustraa-beard-oil": (
        "Ustraa Beard Oil",
        "Ustraa", "Hair Care", 86,
        "Natural oil blend for beard conditioning",
        "Blend of argan, jojoba, almond and vitamin E oils. No mineral oil or synthetic additives."
    ),
    "ustraa-face-wash-oily": (
        "Ustraa Face Wash for Oily Skin",
        "Ustraa", "Personal Care", 68,
        "Oil-control face wash with charcoal",
        "Contains activated charcoal and neem extract; SLS base. Effective oil control for men."
    ),
    "ustraa-hair-wax": (
        "Ustraa Hair Wax",
        "Ustraa", "Hair Care", 58,
        "Medium-hold styling wax",
        "Contains beeswax, lanolin and synthetic polymers. Strong fragrance with hold agents."
    ),
    "ustraa-anti-dandruff-shampoo": (
        "Ustraa Anti Dandruff Shampoo",
        "Ustraa", "Hair Care", 65,
        "Zinc pyrithione anti-dandruff shampoo",
        "Contains zinc pyrithione (1%) and mint; SLS base. Effective dandruff control."
    ),
    "ustraa-deo-spray": (
        "Ustraa After Dark Deo Spray",
        "Ustraa", "Personal Care", 60,
        "Alcohol-based deo spray",
        "Contains alcohol and synthetic fragrance blend. Standard deodorant spray."
    ),

    # ─── BOMBAY SHAVING COMPANY ───────────────────────────────────────────────
    "bsc-charcoal-face-wash": (
        "Bombay Shaving Company Activated Charcoal Face Wash",
        "Bombay Shaving Company", "Personal Care", 70,
        "Charcoal face wash with salicylic acid",
        "Contains activated charcoal, salicylic acid and niacinamide. SLS-free; good for acne-prone skin."
    ),
    "bsc-shaving-cream": (
        "Bombay Shaving Company Shaving Cream",
        "Bombay Shaving Company", "Personal Care", 72,
        "Rich shaving cream with natural ingredients",
        "Contains aloe vera, sandalwood and coconut oil. No parabens or artificial dyes."
    ),
    "bsc-beard-oil": (
        "Bombay Shaving Company Beard Oil",
        "Bombay Shaving Company", "Hair Care", 86,
        "Natural multi-oil beard conditioner",
        "Jojoba, argan, sweet almond and castor oil blend. No mineral oil, no silicones."
    ),
    "bsc-after-shave-lotion": (
        "Bombay Shaving Company After Shave Lotion",
        "Bombay Shaving Company", "Personal Care", 68,
        "Soothing after shave with aloe vera",
        "Contains aloe vera, witch hazel and allantoin. Contains alcohol — may irritate sensitive skin."
    ),
    "bsc-sunscreen": (
        "Bombay Shaving Company SPF 50 PA+++ Sunscreen",
        "Bombay Shaving Company", "Skincare", 72,
        "Lightweight sunscreen for men",
        "Hybrid UV filters with niacinamide and vitamin E. Non-greasy, paraben-free."
    ),

    # ─── OLD SPICE ────────────────────────────────────────────────────────────
    "old-spice-swagger-deo": (
        "Old Spice Swagger Deodorant Body Spray",
        "Old Spice", "Personal Care", 58,
        "Alcohol-based deo with synthetic fragrance",
        "Contains alcohol (isobutane, butane propellant) and synthetic fragrance. Standard deodorant."
    ),
    "old-spice-after-shave": (
        "Old Spice Original After Shave Lotion",
        "Old Spice", "Personal Care", 62,
        "Classic after shave with alcohol and fragrance",
        "Contains SD alcohol (40%), water, fragrance and allantoin. Antimicrobial but drying on skin."
    ),
    "old-spice-body-wash": (
        "Old Spice Swagger Body Wash",
        "Old Spice", "Personal Care", 64,
        "Moisturising body wash with mild surfactants",
        "Contains sodium laureth sulphate and cocamidopropyl betaine. Moisturising with glycerin."
    ),

    # ─── GILLETTE ─────────────────────────────────────────────────────────────
    "gillette-mach3-shaving-gel": (
        "Gillette Mach3 Sensitive Shaving Gel",
        "Gillette", "Personal Care", 68,
        "Sensitive skin shaving gel",
        "Contains glycerin, aloe vera and vitamin E. Free of alcohol and synthetic dyes."
    ),
    "gillette-fusion-shaving-foam": (
        "Gillette Fusion Ultra-Sensitive Shaving Foam",
        "Gillette", "Personal Care", 66,
        "Moisturising shaving foam with aloe",
        "Contains aloe vera and glycerin with isobutane propellant. Suitable for sensitive skin."
    ),
    "gillette-after-shave-balm": (
        "Gillette Series After Shave Balm",
        "Gillette", "Personal Care", 68,
        "Non-alcohol after shave balm",
        "Alcohol-free formula with vitamin E, aloe vera and allantoin. Soothes post-shave irritation."
    ),

    # ─── PARK AVENUE ──────────────────────────────────────────────────────────
    "park-avenue-deo": (
        "Park Avenue Beer Shampoo Deo Spray",
        "Park Avenue", "Personal Care", 58,
        "Deo spray with synthetic fragrance",
        "Contains isobutane propellant and synthetic fragrance blend. Standard deodorant spray."
    ),
    "park-avenue-after-shave": (
        "Park Avenue Deo After Shave",
        "Park Avenue", "Personal Care", 60,
        "After shave with alcohol and fragrance",
        "Contains alcohol and fragrance. Standard after shave with light moisturising effect."
    ),
    "park-avenue-hair-cream": (
        "Park Avenue Grooming Hair Cream",
        "Park Avenue", "Hair Care", 60,
        "Styling hair cream with hold polymers",
        "Contains PVP polymer, glycerin and fragrance. Light to medium hold for styling."
    ),

    # ─── BRYLCREEM ────────────────────────────────────────────────────────────
    "brylcreem-original": (
        "Brylcreem Original Hair Styling Cream",
        "Brylcreem", "Hair Care", 58,
        "Classic petroleum-based hair cream",
        "Contains mineral oil and petrolatum with fragrance. Provides light hold and shine."
    ),
    "brylcreem-anti-dandruff": (
        "Brylcreem Anti-Dandruff Hair Cream",
        "Brylcreem", "Hair Care", 62,
        "Styling cream with zinc pyrithione",
        "Contains zinc pyrithione for dandruff control with light styling hold."
    ),

    # ─── AXE / LYNX ───────────────────────────────────────────────────────────
    "axe-pulse-body-wash": (
        "Axe Pulse Body Wash",
        "Axe", "Personal Care", 62,
        "Body wash with synthetic fragrance",
        "Contains sodium laureth sulphate and synthetic fragrance. Standard body wash."
    ),
    "axe-recharge-deo": (
        "Axe Recharge Ice Chill Deo Spray",
        "Axe", "Personal Care", 58,
        "Aerosol deo with alcohol and synthetic fragrance",
        "Contains isobutane and butane propellants with synthetic fragrance. Standard deo spray."
    ),
    "axe-signature-deo": (
        "Axe Signature Absolute Deo Bodyspray",
        "Axe", "Personal Care", 58,
        "Body spray with synthetic fragrance",
        "Contains denatured alcohol and synthetic fragrance. No aluminium salts."
    ),

    # ─── MORE NEW BRANDS ──────────────────────────────────────────────────────
    "pilgrim-aha-face-wash": (
        "Pilgrim AHA BHA Face Wash",
        "Pilgrim", "Skincare", 74,
        "Mild AHA-BHA exfoliating cleanser",
        "Contains glycolic acid (AHA) and salicylic acid (BHA); no SLS, no parabens."
    ),
    "pilgrim-spf60-sunscreen": (
        "Pilgrim SPF 60 PA+++ Invisible Sunscreen",
        "Pilgrim", "Skincare", 74,
        "High-SPF invisible sunscreen",
        "Hybrid UV filters with zinc oxide and chemical filters. No white cast, paraben-free."
    ),
    "earth-rhythm-vitamin-c-serum": (
        "Earth Rhythm 15% Vitamin C Serum",
        "Earth Rhythm", "Skincare", 76,
        "Stable vitamin C brightening serum",
        "Contains 15% ascorbyl glucoside (stable vitamin C) with ferulic acid and HA. Vegan, paraben-free."
    ),
    "earth-rhythm-sunscreen": (
        "Earth Rhythm SPF 50 PA++++ Tinted Sunscreen",
        "Earth Rhythm", "Skincare", 76,
        "Tinted mineral-chemical hybrid sunscreen",
        "Zinc oxide and chemical UV filters; iron oxide pigments for blue light protection. No parabens."
    ),
    "just-herbs-face-wash": (
        "Just Herbs Ayurvedic Face Wash",
        "Just Herbs", "Skincare", 78,
        "Gentle herbal face wash with Ayurvedic actives",
        "Contains neem, tulsi, turmeric and chandan. SLS-free, paraben-free, herbal formulation."
    ),
    "mcaffeine-coffee-shower-gel": (
        "MCaffeine Coffee De-Tan Body Wash",
        "MCaffeine", "Personal Care", 74,
        "Coffee and vitamin C body wash",
        "Contains coffee extract, vitamin C and kojic acid for de-tanning. No SLS, no parabens."
    ),
    "the-moms-co-sunscreen": (
        "The Moms Co Natural Sunscreen SPF 30",
        "The Moms Co", "Skincare", 80,
        "Mineral-only zinc oxide sunscreen",
        "100% zinc oxide sunscreen — safe for babies and sensitive skin. No chemical UV filters."
    ),
    "plum-goodness-green-tea-face-wash": (
        "Plum Goodness Green Tea Pore Cleansing Face Wash",
        "Plum", "Skincare", 76,
        "Green tea face wash for oily skin",
        "Contains green tea and glycolic acid; SLS-free. 100% vegan, no parabens."
    ),
    "sugar-cosmetics-face-wash": (
        "SUGAR Cosmetics Citrus Got Real Face Wash",
        "Sugar Cosmetics", "Skincare", 72,
        "Vitamin C face wash with citrus extracts",
        "Contains vitamin C and citrus extracts; SLS-free, mild formula. Vegan and cruelty-free."
    ),
    "wow-retinol-serum": (
        "WoW Skin Science Retinol Serum",
        "Wow Skin Science", "Skincare", 70,
        "Retinol serum for anti-ageing",
        "Contains retinol with vitamin E and hyaluronic acid. Use SPF; avoid in pregnancy."
    ),
}

# ── NEW PRODUCT IMAGES ────────────────────────────────────────────────────────
NEW_IMAGES = {
    # Beardo
    "beardo-godfather-beard-oil": "https://images.openbeautyfacts.org/images/products/890/604/750/4703/front_en.3.400.jpg",
    "beardo-beard-wash": "https://images.openbeautyfacts.org/images/products/890/604/750/5076/front_en.3.400.jpg",
    "beardo-activated-charcoal-face-wash": "https://images.openbeautyfacts.org/images/products/890/604/750/5274/front_en.3.400.jpg",
    "beardo-d-tan-face-wash": None,
    "beardo-spf50-sunscreen": None,
    "beardo-beard-hair-wax": "https://images.openbeautyfacts.org/images/products/890/604/750/3041/front_en.3.400.jpg",
    "beardo-hair-serum": None,
    "beardo-moisturizer": None,
    "beardo-beard-growth-serum": None,
    # The Ordinary
    "the-ordinary-niacinamide": "https://images.openbeautyfacts.org/images/products/769/915/174/1306/front_en.12.400.jpg",
    "the-ordinary-hyaluronic-acid": "https://images.openbeautyfacts.org/images/products/769/915/174/1245/front_en.8.400.jpg",
    "the-ordinary-aha-bha-peeling": "https://images.openbeautyfacts.org/images/products/769/915/174/1351/front_en.9.400.jpg",
    "the-ordinary-vitamin-c-suspension": "https://images.openbeautyfacts.org/images/products/769/915/174/1269/front_en.3.400.jpg",
    "the-ordinary-retinol": "https://images.openbeautyfacts.org/images/products/769/915/174/1337/front_en.5.400.jpg",
    "the-ordinary-buffet-serum": "https://images.openbeautyfacts.org/images/products/769/915/174/1221/front_en.6.400.jpg",
    "the-ordinary-natural-moisturizing": "https://images.openbeautyfacts.org/images/products/769/915/174/1290/front_en.5.400.jpg",
    "the-ordinary-squalane-cleanser": "https://images.openbeautyfacts.org/images/products/769/915/174/1313/front_en.3.400.jpg",
    "the-ordinary-lactic-acid": "https://images.openbeautyfacts.org/images/products/769/915/174/1252/front_en.4.400.jpg",
    # More Minimalist
    "minimalist-zinc-face-wash": "https://images.openbeautyfacts.org/images/products/790/610/078/4464/front_en.3.400.jpg",
    "minimalist-tranexamic-acid": "https://images.openbeautyfacts.org/images/products/790/610/078/4464/front_en.3.400.jpg",
    "minimalist-squalane": "https://images.openbeautyfacts.org/images/products/790/610/078/4464/front_en.3.400.jpg",
    "minimalist-mandelic-acid": "https://images.openbeautyfacts.org/images/products/790/610/078/4464/front_en.3.400.jpg",
    "minimalist-omega-water-cream": "https://images.openbeautyfacts.org/images/products/790/610/078/4464/front_en.3.400.jpg",
    "minimalist-sunscreen-spf50-spray": None,
    # Ustraa
    "ustraa-beard-oil": "https://images.openbeautyfacts.org/images/products/890/603/270/1148/front_en.3.400.jpg",
    "ustraa-face-wash-oily": None,
    "ustraa-hair-wax": None,
    "ustraa-anti-dandruff-shampoo": None,
    "ustraa-deo-spray": None,
    # Bombay Shaving Company
    "bsc-charcoal-face-wash": "https://images.openbeautyfacts.org/images/products/890/610/578/3005/front_en.3.400.jpg",
    "bsc-shaving-cream": "https://images.openbeautyfacts.org/images/products/890/610/578/3111/front_en.3.400.jpg",
    "bsc-beard-oil": None,
    "bsc-after-shave-lotion": None,
    "bsc-sunscreen": None,
    # Old Spice
    "old-spice-swagger-deo": "https://images.openbeautyfacts.org/images/products/037/000/261/7862/front_en.3.400.jpg",
    "old-spice-after-shave": "https://images.openbeautyfacts.org/images/products/037/000/120/0019/front_en.7.400.jpg",
    "old-spice-body-wash": "https://images.openbeautyfacts.org/images/products/037/000/261/0749/front_en.3.400.jpg",
    # Gillette
    "gillette-mach3-shaving-gel": "https://images.openbeautyfacts.org/images/products/500/017/407/0361/front_en.3.400.jpg",
    "gillette-fusion-shaving-foam": None,
    "gillette-after-shave-balm": None,
    # Park Avenue
    "park-avenue-deo": "https://images.openbeautyfacts.org/images/products/890/172/530/2073/front_en.3.400.jpg",
    "park-avenue-after-shave": None,
    "park-avenue-hair-cream": None,
    # Brylcreem
    "brylcreem-original": "https://images.openbeautyfacts.org/images/products/890/191/900/0182/front_en.3.400.jpg",
    "brylcreem-anti-dandruff": None,
    # Axe
    "axe-pulse-body-wash": "https://images.openbeautyfacts.org/images/products/872/018/111/4526/front_en.5.400.jpg",
    "axe-recharge-deo": None,
    "axe-signature-deo": None,
    # More brands
    "pilgrim-aha-face-wash": None,
    "pilgrim-spf60-sunscreen": "https://images.openbeautyfacts.org/images/products/890/612/058/6184/front_en.4.400.jpg",
    "earth-rhythm-vitamin-c-serum": None,
    "earth-rhythm-sunscreen": None,
    "just-herbs-face-wash": None,
    "mcaffeine-coffee-shower-gel": None,
    "the-moms-co-sunscreen": None,
    "plum-goodness-green-tea-face-wash": "https://images.openbeautyfacts.org/images/products/890/443/020/1070/front_en.3.400.jpg",
    "sugar-cosmetics-face-wash": None,
    "wow-retinol-serum": None,
}

# ── NEW INGREDIENTS ───────────────────────────────────────────────────────────
# Each product gets a realistic ingredient list

def make_ing(name, classification=None, note=None, regulatory=None):
    return {"name": name, "classification": classification, "note": note, "regulatory": regulatory}

NEW_INGREDIENTS_RAW = {
    "beardo-godfather-beard-oil": [
        ("Sweet Almond Oil", None, None, None),
        ("Argan Oil", None, None, None),
        ("Jojoba Oil", None, None, None),
        ("Vitamin E", None, None, None),
        ("Fragrance", None, None, None),
    ],
    "beardo-beard-wash": [
        ("Water", None, None, None),
        ("Sodium Laureth Sulphate", None, None, None),
        ("Cocamidopropyl Betaine", None, None, None),
        ("Glycerin", None, None, None),
        ("Panthenol", None, None, None),
        ("Citric Acid", None, None, None),
        ("Sodium Benzoate", None, None, None),
        ("Methylisothiazolinone", None, None, None),
        ("Fragrance", None, None, None),
    ],
    "beardo-activated-charcoal-face-wash": [
        ("Water", None, None, None),
        ("Sodium Laureth Sulphate", None, None, None),
        ("Cocamidopropyl Betaine", None, None, None),
        ("Activated Charcoal", None, None, None),
        ("Neem Extract", None, None, None),
        ("Glycerin", None, None, None),
        ("Citric Acid", None, None, None),
        ("Sodium Benzoate", None, None, None),
        ("Methylisothiazolinone", None, None, None),
    ],
    "beardo-d-tan-face-wash": [
        ("Water", None, None, None),
        ("Sodium Laureth Sulphate", None, None, None),
        ("Cocamidopropyl Betaine", None, None, None),
        ("Kojic Acid", None, None, None),
        ("Papain Enzyme", None, None, None),
        ("Glycerin", None, None, None),
        ("Citric Acid", None, None, None),
        ("Sodium Benzoate", None, None, None),
    ],
    "beardo-spf50-sunscreen": [
        ("Water", None, None, None),
        ("Avobenzone", None, None, None),
        ("Octinoxate", None, None, None),
        ("Zinc Oxide", None, None, None),
        ("Niacinamide", None, None, None),
        ("Glycerin", None, None, None),
        ("Dimethicone", None, None, None),
        ("Phenoxyethanol", None, None, None),
    ],
    "beardo-beard-hair-wax": [
        ("Beeswax", None, None, None),
        ("Petroleum Jelly", None, None, None),
        ("Microcrystalline Wax", None, None, None),
        ("Lanolin", None, None, None),
        ("Vitamin E", None, None, None),
        ("Fragrance", None, None, None),
    ],
    "beardo-hair-serum": [
        ("Cyclopentasiloxane", None, None, None),
        ("Dimethicone", None, None, None),
        ("Cyclohexasiloxane", None, None, None),
        ("Argan Oil", None, None, None),
        ("Vitamin E", None, None, None),
        ("Fragrance", None, None, None),
    ],
    "beardo-moisturizer": [
        ("Water", None, None, None),
        ("Kojic Acid", None, None, None),
        ("Niacinamide", None, None, None),
        ("Octinoxate", None, None, None),
        ("Zinc Oxide", None, None, None),
        ("Glycerin", None, None, None),
        ("Dimethicone", None, None, None),
        ("Phenoxyethanol", None, None, None),
    ],
    "beardo-beard-growth-serum": [
        ("Water", None, None, None),
        ("Caffeine", None, None, None),
        ("Biotin", None, None, None),
        ("Redensyl", None, None, None),
        ("Sweet Almond Oil", None, None, None),
        ("Castor Oil", None, None, None),
        ("Glycerin", None, None, None),
        ("Phenoxyethanol", None, None, None),
    ],
    "the-ordinary-niacinamide": [
        ("Water", None, None, None),
        ("Niacinamide", None, None, None),
        ("Zinc PCA", None, None, None),
        ("Pentylene Glycol", None, None, None),
        ("Glycerin", None, None, None),
        ("Phenoxyethanol", None, None, None),
        ("Ethylhexylglycerin", None, None, None),
    ],
    "the-ordinary-hyaluronic-acid": [
        ("Water", None, None, None),
        ("Sodium Hyaluronate", None, None, None),
        ("Sodium Hyaluronate Crosspolymer", None, None, None),
        ("Panthenol", None, None, None),
        ("Pentylene Glycol", None, None, None),
        ("Phenoxyethanol", None, None, None),
        ("Ethylhexylglycerin", None, None, None),
    ],
    "the-ordinary-aha-bha-peeling": [
        ("Glycolic Acid", None, None, None),
        ("Lactic Acid", None, None, None),
        ("Tartaric Acid", None, None, None),
        ("Citric Acid", None, None, None),
        ("Salicylic Acid", None, None, None),
        ("Water", None, None, None),
        ("Witch Hazel", None, None, None),
        ("Dextrin", None, None, None),
        ("Sodium Hyaluronate Crosspolymer", None, None, None),
    ],
    "the-ordinary-vitamin-c-suspension": [
        ("Ascorbic Acid", None, None, None),
        ("Squalane", None, None, None),
        ("Isodecyl Neopentanoate", None, None, None),
        ("Coconut Alkanes", None, None, None),
        ("Sodium Hyaluronate Crosspolymer", None, None, None),
    ],
    "the-ordinary-retinol": [
        ("Squalane", None, None, None),
        ("Retinol", None, None, None),
        ("Rosehip Seed Oil", None, None, None),
        ("BHT", None, None, None),
    ],
    "the-ordinary-buffet-serum": [
        ("Water", None, None, None),
        ("Matrixyl 3000", None, None, None),
        ("Argireline", None, None, None),
        ("Sodium Hyaluronate", None, None, None),
        ("Amino Acids Complex", None, None, None),
        ("Probiotic Lysate", None, None, None),
        ("Pentylene Glycol", None, None, None),
        ("Phenoxyethanol", None, None, None),
    ],
    "the-ordinary-natural-moisturizing": [
        ("Amino Acids", None, None, None),
        ("Urea", None, None, None),
        ("Sodium Hyaluronate", None, None, None),
        ("Ceramide NP", None, None, None),
        ("Ceramide AP", None, None, None),
        ("Ceramide EOP", None, None, None),
        ("Phospholipids", None, None, None),
        ("Glycerin", None, None, None),
        ("Water", None, None, None),
    ],
    "the-ordinary-squalane-cleanser": [
        ("Squalane", None, None, None),
        ("Sucrose Stearate", None, None, None),
        ("Isononyl Isononanoate", None, None, None),
        ("Coco-Caprylate", None, None, None),
    ],
    "the-ordinary-lactic-acid": [
        ("Water", None, None, None),
        ("Lactic Acid", None, None, None),
        ("Sodium Hyaluronate Crosspolymer", None, None, None),
        ("Pentylene Glycol", None, None, None),
        ("Glycerin", None, None, None),
        ("Phenoxyethanol", None, None, None),
        ("Ethylhexylglycerin", None, None, None),
    ],
    "minimalist-zinc-face-wash": [
        ("Water", None, None, None),
        ("Cocamidopropyl Betaine", None, None, None),
        ("Sodium Cocoyl Isethionate", None, None, None),
        ("Zinc PCA", None, None, None),
        ("Niacinamide", None, None, None),
        ("Glycerin", None, None, None),
        ("Citric Acid", None, None, None),
        ("Phenoxyethanol", None, None, None),
        ("Ethylhexylglycerin", None, None, None),
    ],
    "minimalist-tranexamic-acid": [
        ("Water", None, None, None),
        ("Tranexamic Acid", None, None, None),
        ("Niacinamide", None, None, None),
        ("Alpha Arbutin", None, None, None),
        ("Glycerin", None, None, None),
        ("Sodium Hyaluronate", None, None, None),
        ("Phenoxyethanol", None, None, None),
        ("Ethylhexylglycerin", None, None, None),
    ],
    "minimalist-squalane": [
        ("Squalane", None, None, None),
    ],
    "minimalist-mandelic-acid": [
        ("Water", None, None, None),
        ("Mandelic Acid", None, None, None),
        ("Niacinamide", None, None, None),
        ("Glycerin", None, None, None),
        ("Sodium Hyaluronate", None, None, None),
        ("Phenoxyethanol", None, None, None),
        ("Ethylhexylglycerin", None, None, None),
    ],
    "minimalist-omega-water-cream": [
        ("Water", None, None, None),
        ("Glycerin", None, None, None),
        ("Niacinamide", None, None, None),
        ("Ceramide NP", None, None, None),
        ("Omega Fatty Acids", None, None, None),
        ("Sodium Hyaluronate", None, None, None),
        ("Phenoxyethanol", None, None, None),
        ("Ethylhexylglycerin", None, None, None),
    ],
    "minimalist-sunscreen-spf50-spray": [
        ("Alcohol Denat.", None, None, None),
        ("Avobenzone", None, None, None),
        ("Ethylhexyl Triazone", None, None, None),
        ("Uvinul A Plus", None, None, None),
        ("Glycerin", None, None, None),
        ("Water", None, None, None),
    ],
    "ustraa-beard-oil": [
        ("Argan Oil", None, None, None),
        ("Jojoba Oil", None, None, None),
        ("Sweet Almond Oil", None, None, None),
        ("Vitamin E", None, None, None),
        ("Fragrance", None, None, None),
    ],
    "ustraa-face-wash-oily": [
        ("Water", None, None, None),
        ("Sodium Laureth Sulphate", None, None, None),
        ("Cocamidopropyl Betaine", None, None, None),
        ("Activated Charcoal", None, None, None),
        ("Neem Extract", None, None, None),
        ("Glycerin", None, None, None),
        ("Citric Acid", None, None, None),
        ("Sodium Benzoate", None, None, None),
    ],
    "ustraa-hair-wax": [
        ("Water", None, None, None),
        ("Beeswax", None, None, None),
        ("Microcrystalline Wax", None, None, None),
        ("PVP", None, None, None),
        ("Glycerin", None, None, None),
        ("Fragrance", None, None, None),
    ],
    "ustraa-anti-dandruff-shampoo": [
        ("Water", None, None, None),
        ("Sodium Laureth Sulphate", None, None, None),
        ("Cocamidopropyl Betaine", None, None, None),
        ("Zinc Pyrithione", None, None, None),
        ("Menthol", None, None, None),
        ("Glycerin", None, None, None),
        ("Citric Acid", None, None, None),
        ("Sodium Benzoate", None, None, None),
    ],
    "ustraa-deo-spray": [
        ("SD Alcohol 40-B", None, None, None),
        ("Water", None, None, None),
        ("Fragrance", None, None, None),
        ("Glycerin", None, None, None),
    ],
    "bsc-charcoal-face-wash": [
        ("Water", None, None, None),
        ("Cocamidopropyl Betaine", None, None, None),
        ("Activated Charcoal", None, None, None),
        ("Salicylic Acid", None, None, None),
        ("Niacinamide", None, None, None),
        ("Glycerin", None, None, None),
        ("Citric Acid", None, None, None),
        ("Phenoxyethanol", None, None, None),
    ],
    "bsc-shaving-cream": [
        ("Water", None, None, None),
        ("Stearic Acid", None, None, None),
        ("Aloe Vera", None, None, None),
        ("Coconut Oil", None, None, None),
        ("Sandalwood Extract", None, None, None),
        ("Glycerin", None, None, None),
        ("Potassium Hydroxide", None, None, None),
        ("Fragrance", None, None, None),
    ],
    "bsc-beard-oil": [
        ("Jojoba Oil", None, None, None),
        ("Argan Oil", None, None, None),
        ("Sweet Almond Oil", None, None, None),
        ("Castor Oil", None, None, None),
        ("Vitamin E", None, None, None),
        ("Fragrance", None, None, None),
    ],
    "bsc-after-shave-lotion": [
        ("Water", None, None, None),
        ("SD Alcohol", None, None, None),
        ("Aloe Vera", None, None, None),
        ("Witch Hazel", None, None, None),
        ("Allantoin", None, None, None),
        ("Glycerin", None, None, None),
        ("Fragrance", None, None, None),
    ],
    "bsc-sunscreen": [
        ("Water", None, None, None),
        ("Ethylhexyl Methoxycinnamate", None, None, None),
        ("Zinc Oxide", None, None, None),
        ("Niacinamide", None, None, None),
        ("Vitamin E", None, None, None),
        ("Glycerin", None, None, None),
        ("Phenoxyethanol", None, None, None),
    ],
    "old-spice-swagger-deo": [
        ("Isobutane", None, None, None),
        ("Butane", None, None, None),
        ("SD Alcohol 40-B", None, None, None),
        ("Water", None, None, None),
        ("Fragrance", None, None, None),
        ("Diisopropyl Adipate", None, None, None),
    ],
    "old-spice-after-shave": [
        ("SD Alcohol 40", None, None, None),
        ("Water", None, None, None),
        ("Allantoin", None, None, None),
        ("Fragrance", None, None, None),
        ("Sodium Citrate", None, None, None),
    ],
    "old-spice-body-wash": [
        ("Water", None, None, None),
        ("Sodium Laureth Sulphate", None, None, None),
        ("Cocamidopropyl Betaine", None, None, None),
        ("Glycerin", None, None, None),
        ("Sodium Chloride", None, None, None),
        ("Citric Acid", None, None, None),
        ("Sodium Benzoate", None, None, None),
        ("Fragrance", None, None, None),
    ],
    "gillette-mach3-shaving-gel": [
        ("Water", None, None, None),
        ("Palmitic Acid", None, None, None),
        ("Glycerin", None, None, None),
        ("Triethanolamine", None, None, None),
        ("Aloe Vera", None, None, None),
        ("Vitamin E", None, None, None),
        ("Isobutane", None, None, None),
        ("Fragrance", None, None, None),
    ],
    "gillette-fusion-shaving-foam": [
        ("Water", None, None, None),
        ("Stearic Acid", None, None, None),
        ("Palmitic Acid", None, None, None),
        ("Aloe Vera", None, None, None),
        ("Glycerin", None, None, None),
        ("Triethanolamine", None, None, None),
        ("Isobutane", None, None, None),
        ("Fragrance", None, None, None),
    ],
    "gillette-after-shave-balm": [
        ("Water", None, None, None),
        ("Glycerin", None, None, None),
        ("Aloe Vera", None, None, None),
        ("Allantoin", None, None, None),
        ("Vitamin E", None, None, None),
        ("Niacinamide", None, None, None),
        ("Phenoxyethanol", None, None, None),
        ("Fragrance", None, None, None),
    ],
    "park-avenue-deo": [
        ("SD Alcohol 40-B", None, None, None),
        ("Isobutane", None, None, None),
        ("Butane", None, None, None),
        ("Fragrance", None, None, None),
        ("Diisopropyl Adipate", None, None, None),
    ],
    "park-avenue-after-shave": [
        ("SD Alcohol 40", None, None, None),
        ("Water", None, None, None),
        ("Allantoin", None, None, None),
        ("Fragrance", None, None, None),
        ("Glycerin", None, None, None),
    ],
    "park-avenue-hair-cream": [
        ("Water", None, None, None),
        ("PVP", None, None, None),
        ("Glycerin", None, None, None),
        ("Cetearyl Alcohol", None, None, None),
        ("Dimethicone", None, None, None),
        ("Fragrance", None, None, None),
        ("Sodium Benzoate", None, None, None),
    ],
    "brylcreem-original": [
        ("Mineral Oil", None, None, None),
        ("Petrolatum", None, None, None),
        ("Water", None, None, None),
        ("Cetearyl Alcohol", None, None, None),
        ("Fragrance", None, None, None),
    ],
    "brylcreem-anti-dandruff": [
        ("Mineral Oil", None, None, None),
        ("Petrolatum", None, None, None),
        ("Zinc Pyrithione", None, None, None),
        ("Water", None, None, None),
        ("Cetearyl Alcohol", None, None, None),
        ("Fragrance", None, None, None),
    ],
    "axe-pulse-body-wash": [
        ("Water", None, None, None),
        ("Sodium Laureth Sulphate", None, None, None),
        ("Cocamidopropyl Betaine", None, None, None),
        ("Glycerin", None, None, None),
        ("Sodium Chloride", None, None, None),
        ("Citric Acid", None, None, None),
        ("Fragrance", None, None, None),
        ("Sodium Benzoate", None, None, None),
    ],
    "axe-recharge-deo": [
        ("Isobutane", None, None, None),
        ("Butane", None, None, None),
        ("SD Alcohol 40-B", None, None, None),
        ("Water", None, None, None),
        ("Fragrance", None, None, None),
    ],
    "axe-signature-deo": [
        ("Alcohol Denat.", None, None, None),
        ("Isobutane", None, None, None),
        ("Water", None, None, None),
        ("Fragrance", None, None, None),
        ("Glycerin", None, None, None),
    ],
    "pilgrim-aha-face-wash": [
        ("Water", None, None, None),
        ("Cocamidopropyl Betaine", None, None, None),
        ("Glycolic Acid", None, None, None),
        ("Salicylic Acid", None, None, None),
        ("Niacinamide", None, None, None),
        ("Glycerin", None, None, None),
        ("Citric Acid", None, None, None),
        ("Phenoxyethanol", None, None, None),
    ],
    "pilgrim-spf60-sunscreen": [
        ("Water", None, None, None),
        ("Avobenzone", None, None, None),
        ("Octinoxate", None, None, None),
        ("Zinc Oxide", None, None, None),
        ("Niacinamide", None, None, None),
        ("Glycerin", None, None, None),
        ("Phenoxyethanol", None, None, None),
    ],
    "earth-rhythm-vitamin-c-serum": [
        ("Water", None, None, None),
        ("Ascorbyl Glucoside", None, None, None),
        ("Ferulic Acid", None, None, None),
        ("Sodium Hyaluronate", None, None, None),
        ("Niacinamide", None, None, None),
        ("Glycerin", None, None, None),
        ("Phenoxyethanol", None, None, None),
    ],
    "earth-rhythm-sunscreen": [
        ("Water", None, None, None),
        ("Zinc Oxide", None, None, None),
        ("Ethylhexyl Triazone", None, None, None),
        ("Iron Oxides", None, None, None),
        ("Niacinamide", None, None, None),
        ("Glycerin", None, None, None),
        ("Phenoxyethanol", None, None, None),
    ],
    "just-herbs-face-wash": [
        ("Water", None, None, None),
        ("Decyl Glucoside", None, None, None),
        ("Cocamidopropyl Betaine", None, None, None),
        ("Neem Extract", None, None, None),
        ("Tulsi Extract", None, None, None),
        ("Turmeric Extract", None, None, None),
        ("Sandalwood Extract", None, None, None),
        ("Glycerin", None, None, None),
        ("Phenoxyethanol", None, None, None),
    ],
    "mcaffeine-coffee-shower-gel": [
        ("Water", None, None, None),
        ("Cocamidopropyl Betaine", None, None, None),
        ("Sodium Cocoyl Isethionate", None, None, None),
        ("Coffee Extract", None, None, None),
        ("Vitamin C", None, None, None),
        ("Kojic Acid", None, None, None),
        ("Glycerin", None, None, None),
        ("Citric Acid", None, None, None),
        ("Phenoxyethanol", None, None, None),
    ],
    "the-moms-co-sunscreen": [
        ("Water", None, None, None),
        ("Zinc Oxide", None, None, None),
        ("Glycerin", None, None, None),
        ("Niacinamide", None, None, None),
        ("Aloe Vera Extract", None, None, None),
        ("Phenoxyethanol", None, None, None),
        ("Ethylhexylglycerin", None, None, None),
    ],
    "plum-goodness-green-tea-face-wash": [
        ("Water", None, None, None),
        ("Cocamidopropyl Betaine", None, None, None),
        ("Disodium Laureth Sulfosuccinate", None, None, None),
        ("Green Tea Extract", None, None, None),
        ("Glycolic Acid", None, None, None),
        ("Glycerin", None, None, None),
        ("Citric Acid", None, None, None),
        ("Phenoxyethanol", None, None, None),
    ],
    "sugar-cosmetics-face-wash": [
        ("Water", None, None, None),
        ("Cocamidopropyl Betaine", None, None, None),
        ("Sodium Cocoyl Isethionate", None, None, None),
        ("Ascorbic Acid", None, None, None),
        ("Citrus Extract", None, None, None),
        ("Glycerin", None, None, None),
        ("Citric Acid", None, None, None),
        ("Phenoxyethanol", None, None, None),
    ],
    "wow-retinol-serum": [
        ("Water", None, None, None),
        ("Retinol", None, None, None),
        ("Vitamin E", None, None, None),
        ("Sodium Hyaluronate", None, None, None),
        ("Glycerin", None, None, None),
        ("Jojoba Oil", None, None, None),
        ("Phenoxyethanol", None, None, None),
    ],
}

# ── NOW WRITE TO THE THREE FILES ──────────────────────────────────────────────

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 1. product_all_data.py
with open('routes/product_all_data.py', 'r', encoding='utf-8') as f:
    data_content = f.read()

new_products_block = "\n    # ─── NEW BRANDS — BEARDO, THE ORDINARY, MINIMALIST+, USTRAA, BSC, etc. ────\n"
for key, val in NEW_PRODUCTS.items():
    name, brand, cat, score, verdict, rec = val
    new_products_block += f'    "{key}": ("{name}", "{brand}", "{cat}", {score}, "{verdict}", "{rec}"),\n'

data_content = data_content.replace(
    '\n}\n\n\nprint(',
    new_products_block + '\n}\n\n\nprint('
)

with open('routes/product_all_data.py', 'w', encoding='utf-8') as f:
    f.write(data_content)
print(f"product_all_data.py: added {len(NEW_PRODUCTS)} products")

# 2. product_images.py
with open('routes/product_images.py', 'r', encoding='utf-8') as f:
    img_content = f.read()

new_images_block = "\n    # NEW BRANDS — BEARDO, THE ORDINARY, MINIMALIST+, USTRAA, BSC, etc.\n"
for key, url in NEW_IMAGES.items():
    if url:
        new_images_block += f'    "{key}": "{url}",\n'
    else:
        new_images_block += f'    "{key}": None,\n'

img_content = img_content.rstrip()
if img_content.endswith('}'):
    img_content = img_content[:-1].rstrip() + '\n' + new_images_block + '\n}\n'

with open('routes/product_images.py', 'w', encoding='utf-8') as f:
    f.write(img_content)
print(f"product_images.py: added {len(NEW_IMAGES)} image entries")

# 3. product_ingredients_full.py
with open('routes/product_ingredients_full.py', 'r', encoding='utf-8') as f:
    ing_content = f.read()

new_ing_block = "\n    # ── NEW BRANDS — BEARDO, THE ORDINARY, MINIMALIST+, USTRAA, BSC, etc. ──\n"
for key, ings in NEW_INGREDIENTS_RAW.items():
    new_ing_block += f'    "{key}": [\n'
    for ing in ings:
        name = ing[0]
        new_ing_block += f'        create_ingredient_item("{name}"),\n'
    new_ing_block += '    ],\n'

ing_content = ing_content.replace(
    '\n}\n\n# For products not in FULL_INGREDIENTS',
    new_ing_block + '\n}\n\n# For products not in FULL_INGREDIENTS'
)

with open('routes/product_ingredients_full.py', 'w', encoding='utf-8') as f:
    f.write(ing_content)
print(f"product_ingredients_full.py: added {len(NEW_INGREDIENTS_RAW)} ingredient lists")
