"""
Fetch genuine product images from Open Food Facts (food) + Open Beauty Facts (cosmetics).
Run once: python fetch_product_images.py
Outputs: product_images.py with image_url per product key.
Skips products that already have a URL in the existing file.
"""

import time
import json
import urllib.request
import urllib.parse
import os
import sys

# Force UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from routes.product_all_data import ALL_PRODUCTS

OFT_SEARCH  = "https://world.openfoodfacts.org/cgi/search.pl"
OBF_SEARCH  = "https://world.openbeautyfacts.org/cgi/search.pl"

COSMETIC_CATEGORIES = {
    "Skincare", "Hair Care", "Cosmetics", "Personal Care",
    "Baby Care", "Oral Care", "Household"
}

HEADERS = {"User-Agent": "CheckKaro/1.0 (educational project)"}


def search_api(base_url, product_name, brand, img_domain, retries=2):
    query = f"{product_name} {brand}"
    params = urllib.parse.urlencode({
        "search_terms": query,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "fields": "product_name,brands,image_front_url",
        "page_size": 5,
        "lc": "en",
    })
    url = f"{base_url}?{params}"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
            for p in data.get("products", []):
                img = p.get("image_front_url", "")
                if img and img.startswith(img_domain):
                    return img
        except Exception:
            if attempt < retries - 1:
                time.sleep(1)
    return None


def fetch_image(product_name, brand, category):
    """Try the best database first based on category, fall back to the other."""
    is_cosmetic = category in COSMETIC_CATEGORIES

    if is_cosmetic:
        # Beauty Facts first, Food Facts as fallback
        url = search_api(OBF_SEARCH, product_name, brand, "https://images.openbeautyfacts.org")
        if not url:
            url = search_api(OFT_SEARCH, product_name, brand, "https://images.openfoodfacts.org")
    else:
        # Food Facts first, Beauty Facts as fallback
        url = search_api(OFT_SEARCH, product_name, brand, "https://images.openfoodfacts.org")
        if not url:
            url = search_api(OBF_SEARCH, product_name, brand, "https://images.openbeautyfacts.org")
    return url


def load_existing():
    """Load already-fetched URLs so we can skip them."""
    existing = {}
    path = "routes/product_images.py"
    if not os.path.exists(path):
        return existing
    try:
        ns = {}
        with open(path, encoding="utf-8") as f:
            exec(f.read(), ns)
        existing = ns.get("PRODUCT_IMAGES", {})
    except Exception:
        pass
    return existing


def main():
    existing = load_existing()
    results = dict(existing)  # start from what we have
    total = len(ALL_PRODUCTS)
    found = sum(1 for v in existing.values() if v)
    new_found = 0
    skipped = 0

    print(f"Loaded {len(existing)} existing entries ({found} with images). Fetching missing...")

    for idx, (key, val) in enumerate(ALL_PRODUCTS.items()):
        name, brand, category = val[0], val[1], val[2]

        # Skip if already has a real URL
        if existing.get(key):
            skipped += 1
            continue

        print(f"[{idx+1}/{total}] {name} ({brand}) [{category}] ... ", end="", flush=True)
        url = fetch_image(name, brand, category)
        if url:
            results[key] = url
            found += 1
            new_found += 1
            print("OK")
        else:
            results[key] = None
            print("not found")
        time.sleep(0.4)  # respect rate limits

    # Write output file
    with open("routes/product_images.py", "w", encoding="utf-8") as f:
        f.write('"""\nProduct image URLs — Open Food Facts + Open Beauty Facts.\nAuto-generated.\n"""\n\n')
        f.write("PRODUCT_IMAGES = {\n")
        for key, url in results.items():
            if url:
                f.write(f'    "{key}": "{url}",\n')
            else:
                f.write(f'    "{key}": None,\n')
        f.write("}\n")

    print(f"\nDone. {found}/{total} total images ({new_found} newly found, {skipped} already had images).")


if __name__ == "__main__":
    main()
