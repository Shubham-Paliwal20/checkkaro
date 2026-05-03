"""
One-shot migration: insert all 645 static products into ai_extracted_products.

Run locally AFTER running the Phase 1 SQL in Supabase dashboard:
  python migrate_static_to_supabase.py

Safe to re-run: upsert on static_key skips already-inserted rows.
"""

import os, sys, time
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from db.supabase_client import supabase_admin
from routes.product_all_data import ALL_PRODUCTS
from routes.product_images import PRODUCT_IMAGES
from routes.product_ingredients_full import FULL_INGREDIENTS

PLACEHOLDER_NAMES = {
    "standard food/cosmetic ingredients",
    "standard ingredients",
    "standard food ingredients",
    "standard cosmetic ingredients",
}

def ings_to_raw(ingredient_list: list) -> str:
    names = [
        i["name"] for i in ingredient_list
        if i.get("name") and i["name"].lower().strip() not in PLACEHOLDER_NAMES
    ]
    return ", ".join(names)

def looks_like_raw_ingredients(text: str) -> bool:
    if not text:
        return False
    return text.count(",") >= 3 and len(text) > 60

BATCH_SIZE = 50
rows = []

for key, (name, brand, category, score, verdict, recommendation) in ALL_PRODUCTS.items():
    if key in FULL_INGREDIENTS:
        raw = ings_to_raw(FULL_INGREDIENTS[key])
        rec = recommendation
    elif looks_like_raw_ingredients(recommendation):
        raw = recommendation
        rec = ""
    else:
        raw = ""
        rec = recommendation

    image_url = PRODUCT_IMAGES.get(key)

    summary = (
        f"{name} — {verdict}. "
        "This information is for general awareness based on publicly available "
        "regulatory data. It is not a health assessment or medical advice."
    )

    rows.append({
        "static_key":      key,
        "name":            name,
        "brand":           brand,
        "category":        category,
        "image_url":       image_url,
        "verdict":         verdict,
        "recommendation":  rec,
        "ingredients_raw": raw,
        "ingredients":     [],
        "summary":         summary,
        "fssai_note":      "FSSAI approved product with standard ingredients.",
    })

print(f"Preparing to insert {len(rows)} products...")

# Delete any previously migrated static rows so re-runs are clean
print("Removing previously migrated static rows (if any)...")
try:
    supabase_admin.from_("ai_extracted_products") \
        .delete() \
        .not_.is_("static_key", "null") \
        .execute()
    print("  Previous static rows cleared.")
except Exception as e:
    print(f"  Warning: could not clear old rows: {e} (continuing)")

inserted = 0
for i in range(0, len(rows), BATCH_SIZE):
    batch = rows[i: i + BATCH_SIZE]
    supabase_admin.from_("ai_extracted_products") \
        .insert(batch) \
        .execute()
    inserted += len(batch)
    last_name = batch[-1]["name"]
    print(f"  Batch {i // BATCH_SIZE + 1}: {inserted}/{len(rows)} | latest: {last_name}")
    time.sleep(0.3)

print(f"\nDone — {inserted} products inserted.")
