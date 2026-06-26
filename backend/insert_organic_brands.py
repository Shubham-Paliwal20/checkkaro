"""
Insert organic brand products from Organic_Brands_Ingredients_Dataset.pdf
Brands: Rustic Art, Juicy Chemistry, Vilvah Store, The Tribe Concepts,
        Kama Ayurveda, Forest Essentials, Mamaearth
"""
import os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from dotenv import load_dotenv
load_dotenv()

from db.supabase_client import supabase_admin
from routes.product_new import _classify, _parse_raw
from grading import calculate_grade

def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

def static_key(name):
    return re.sub(r'\s+', '-', name.lower().strip())

def make_key(name):
    return re.sub(r'[^a-z0-9-]', '', static_key(name))

def compute_grade(ingredients_raw):
    names = _parse_raw(ingredients_raw)
    classified = [{"name": n, "classification": _classify(n)} for n in names if n]
    return calculate_grade(classified) if classified else "C"

PRODUCTS = [
    {
        "name": "Rustic Art Organic Neem Basil Face Wash",
        "brand": "Rustic Art",
        "category": "Skincare",
        "ingredients_raw": "Water (Aqua), Potassium Cocoate (Saponified Coconut Oil), Potassium Ricinoleate (Saponified Castor Oil), Potassium Olivate (Saponified Olive Oil), Organic Neem Oil, Organic Basil Oil, Organic Lemon Oil, Vegetable Glycerin",
    },
    {
        "name": "Rustic Art Biodegradable Laundry Powder",
        "brand": "Rustic Art",
        "category": "Household",
        "ingredients_raw": "Saponified Coconut Oil, Saponified Neem Oil, Saponified Karanja Oil, Lemon Extract, Neem Extract, Sodium Carbonate (Washing Soda), Sodium Bicarbonate (Baking Soda)",
    },
    {
        "name": "Rustic Art Organic Virgin Coconut Oil",
        "brand": "Rustic Art",
        "category": "Hair Care",
        "ingredients_raw": "100% Organic Virgin Cold Pressed Coconut Oil",
    },
    {
        "name": "Juicy Chemistry Chilli Horsetail Black Seed Hair Oil",
        "brand": "Juicy Chemistry",
        "category": "Hair Care",
        "ingredients_raw": "Nigella Sativa (Black Seed) Oil, Capsicum Annuum (Chilli) Seed Oil, Helianthus Annuus (Sunflower) Seed Oil, Equisetum Arvense (Horsetail) Extract, Arctium Lappa (Burdock Root) Extract, Salvia Sclarea (Clary Sage) Essential Oil, Rosmarinus Officinalis (Rosemary) Essential Oil, Pelargonium Graveolens (Geranium) Essential Oil",
    },
    {
        "name": "Juicy Chemistry Kakadu Plum Vitamin C Face Mask",
        "brand": "Juicy Chemistry",
        "category": "Skincare",
        "ingredients_raw": "Terminalia Ferdinandiana (Kakadu Plum) Powder, Bentonite Clay, Rosa Damascena (Rose) Powder, Pelargonium Graveolens (Geranium) Essential Oil, Citrus Sinensis (Orange) Essential Oil",
    },
    {
        "name": "Vilvah Store Goat Milk Shampoo",
        "brand": "Vilvah Store",
        "category": "Hair Care",
        "ingredients_raw": "Fresh Goat Milk, Saponified Oils of Olive, Coconut, and Castor, Jasmine Essential Oil, Patchouli Essential Oil, Guar Gum, Vegetable Glycerin",
    },
    {
        "name": "The Tribe Concepts Face Brightening Daily Cleanser",
        "brand": "The Tribe Concepts",
        "category": "Skincare",
        "ingredients_raw": "Organic Sandalwood, Organic Saffron, Organic Rose Petals, Organic Neem, Organic Turmeric, Organic Vetiver, Organic Fenugreek, Organic Green Gram",
    },
    {
        "name": "Kama Ayurveda Kumkumadi Miraculous Beauty Fluid",
        "brand": "Kama Ayurveda",
        "category": "Skincare",
        "ingredients_raw": "Saffron (Crocus Sativus), Sandalwood (Santalum Album), Madder (Rubia Cordifolia), Licorice (Glycyrrhiza Glabra), Indian Banyan (Ficus Benghalensis), Vetiver (Vetiveria Zizanioides), Blue Lotus (Nymphaea Caerulea), Sesame Oil (Sesamum Indicum), Goat Milk",
    },
    {
        "name": "Forest Essentials Soundarya Radiance Cream",
        "brand": "Forest Essentials",
        "category": "Skincare",
        "ingredients_raw": "24K Gold Bhasma, Cow's Milk, Saffron Extract, Cold Pressed Virgin Sesame Oil, Sweet Almond Oil, Shea Butter, Aloe Vera Juice, Licorice Root Extract, Turmeric Extract, Cetearyl Olivate",
    },
    {
        "name": "Mamaearth Onion Hair Oil",
        "brand": "Mamaearth",
        "category": "Hair Care",
        "ingredients_raw": "Sunflower Oil, Onion Seed Oil, Almond Oil, Amla Oil, Castor Oil, Hibiscus Oil, Bhringraj Oil, Vitamin E, Redensyl, IFRA Certified Allergen Free Fragrance",
    },
]

inserted = 0
skipped = 0

for p in PRODUCTS:
    key = make_key(p["name"])
    grade = compute_grade(p["ingredients_raw"])

    # Skip if already exists (match by static_key or exact name)
    existing = supabase_admin.from_("ai_extracted_products") \
        .select("id") \
        .or_(f"static_key.eq.{key},name.ilike.{p['name']}") \
        .limit(1).execute()

    if existing.data:
        print(f"  SKIP  {p['name']} (already exists)")
        skipped += 1
        continue

    row = {
        "name":            p["name"],
        "brand":           p["brand"],
        "category":        p["category"],
        "ingredients_raw": p["ingredients_raw"],
        "ingredients":     [],
        "grade":           grade,
        "static_key":      key,
        "summary":         f"{p['name']} by {p['brand']}. Ingredient Grade: {grade}.",
        "fssai_note":      "Product subject to FSSAI/BIS regulations.",
        "verdict":         "",
        "recommendation":  "",
    }

    result = supabase_admin.from_("ai_extracted_products").insert(row).execute()
    if result.data:
        print(f"  OK    {p['name']}  Grade {grade}")
        inserted += 1
    else:
        print(f"  FAIL  {p['name']}")

print(f"\nDone — {inserted} inserted, {skipped} skipped.")
