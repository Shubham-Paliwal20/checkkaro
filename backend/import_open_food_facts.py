"""
Import Indian products from Open Food Facts into product_submissions for admin review.

Usage:
  python import_open_food_facts.py            # Preview only (no DB changes)
  python import_open_food_facts.py --save     # Preview + save to product_submissions

Products go into product_submissions with status='pending' and source='open_food_facts'.
Review and approve them in the website admin panel, then click 'Save to Database'.
"""

import os, sys, time, re, json
import httpx
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

SAVE_MODE = "--save" in sys.argv

# OFF search URL — Indian products, with ingredients, EAN-13 barcodes
OFF_SEARCH = "https://world.openfoodfacts.org/cgi/search.pl"

CATEGORY_MAP = {
    "beverages": "Beverages", "drinks": "Beverages", "juices": "Beverages",
    "dairy": "Dairy", "milk": "Dairy", "cheese": "Dairy", "yogurt": "Dairy",
    "snacks": "Snacks", "chips": "Snacks", "biscuits": "Snacks", "cookies": "Snacks",
    "chocolates": "Snacks", "candies": "Snacks",
    "cereals": "Breakfast Cereal", "breakfast": "Breakfast Cereal",
    "oils": "Cooking Oil", "cooking": "Cooking Oil",
    "sauces": "Food", "condiments": "Food", "spices": "Food",
    "noodles": "Food", "pasta": "Food", "rice": "Food",
    "ice cream": "Ice Cream", "frozen": "Ice Cream",
    "health": "Health Supplement", "protein": "Health Supplement",
    "beauty": "Skincare", "skin": "Skincare", "hair": "Hair Care",
    "oral": "Personal Care", "toothpaste": "Personal Care", "soap": "Personal Care",
    "baby": "Personal Care",
}

def _guess_category(tags: list) -> str:
    tag_str = " ".join(tags).lower()
    for kw, cat in CATEGORY_MAP.items():
        if kw in tag_str:
            return cat
    return "Food"

def _clean(text: str) -> str:
    return re.sub(r'\s+', ' ', (text or "").strip())

def fetch_off_page(page: int, page_size: int = 50) -> list:
    params = {
        "action":       "process",
        "tagtype_0":    "countries",
        "tag_contains_0": "contains",
        "tag_0":        "india",
        "fields":       "code,product_name,brands,categories_tags,ingredients_text,image_front_url",
        "json":         1,
        "page_size":    page_size,
        "page":         page,
    }
    try:
        r = httpx.get(OFF_SEARCH, params=params, timeout=20)
        data = r.json()
        return data.get("products", [])
    except Exception as e:
        print(f"  [OFF] Fetch error page {page}: {e}")
        return []

def process_products(max_pages: int = 10) -> list:
    results = []
    print(f"\n{'='*60}")
    print("Fetching Indian products from Open Food Facts...")
    print(f"{'='*60}\n")

    for page in range(1, max_pages + 1):
        print(f"Page {page}/{max_pages}...", end=" ", flush=True)
        products = fetch_off_page(page)
        if not products:
            print("no results, stopping.")
            break

        count = 0
        for p in products:
            barcode   = (p.get("code") or "").strip()
            name      = _clean(p.get("product_name") or "")
            brand     = _clean(p.get("brands") or "")
            ings_raw  = _clean(p.get("ingredients_text") or "")
            image_url = p.get("image_front_url") or None
            cats      = p.get("categories_tags") or []

            # Skip if missing key fields
            if not barcode or len(barcode) < 8: continue
            if not name or len(name) < 3:        continue
            if not ings_raw or len(ings_raw) < 10: continue

            category = _guess_category(cats)

            results.append({
                "barcode":               barcode,
                "product_name_searched": name[:200],
                "brand":                 brand[:100] if brand else None,
                "category":              category,
                "ingredients_raw":       ings_raw[:5000],
                "image_url":             image_url,
                "images":                [image_url] if image_url else [],
            })
            count += 1

        print(f"found {count} valid products (total so far: {len(results)})")
        time.sleep(0.5)  # be polite to OFF servers

    return results

def preview(products: list):
    print(f"\n{'='*60}")
    print(f"PREVIEW — {len(products)} products found")
    print(f"{'='*60}")
    for i, p in enumerate(products[:30], 1):
        ing_preview = p['ingredients_raw'][:60].replace('\n', ' ')
        print(f"\n{i:3}. [{p['barcode']}] {p['product_name_searched']}")
        print(f"     Brand: {p.get('brand') or '—'}  |  Category: {p['category']}")
        print(f"     Ingredients: {ing_preview}...")
    if len(products) > 30:
        print(f"\n     ... and {len(products)-30} more products not shown")

def save_to_supabase(products: list):
    if not SUPABASE_KEY:
        print("\n[ERROR] SUPABASE_SERVICE_ROLE_KEY not set in .env")
        return

    headers = {
        "apikey":        SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type":  "application/json",
        "Prefer":        "return=minimal",
    }
    url = f"{SUPABASE_URL}/rest/v1/product_submissions"

    print(f"\nSaving {len(products)} products to product_submissions...")
    saved = skipped = 0

    for p in products:
        row = {
            "product_name_searched": p["product_name_searched"],
            "ingredients_raw":       p["ingredients_raw"],
            "images":                p["images"],
            "contact":               p.get("brand") or "Open Food Facts",
            "email":                 "import@openfoodfacts.org",
            "barcode":               p["barcode"],
            "source":                "open_food_facts",
            "status":                "pending",
            "user_id":               None,
        }
        try:
            r = httpx.post(url, json=row, headers=headers, timeout=10)
            if r.status_code in (200, 201):
                saved += 1
            elif r.status_code == 409:  # duplicate
                skipped += 1
            else:
                print(f"  [WARN] {p['barcode']} — {r.status_code}: {r.text[:80]}")
        except Exception as e:
            print(f"  [ERROR] {p['barcode']}: {e}")
        time.sleep(0.05)

    print(f"\n✓ Done: {saved} saved, {skipped} skipped (duplicates)")
    print("\nGo to the website admin panel → Submissions tab to review and approve.")

if __name__ == "__main__":
    products = process_products(max_pages=10)

    if not products:
        print("\nNo products found.")
        sys.exit(0)

    preview(products)

    if SAVE_MODE:
        print(f"\n[--save mode] Saving to Supabase...")
        save_to_supabase(products)
    else:
        print(f"\n{'='*60}")
        print(f"Preview complete. {len(products)} products ready to import.")
        print("Run with --save flag to import them to product_submissions:")
        print("  python import_open_food_facts.py --save")
        print(f"{'='*60}\n")
