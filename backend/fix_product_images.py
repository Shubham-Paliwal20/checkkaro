"""
Fix wrong images (non-English labels, duplicates) and add missing images.
Runs selectively — only touches products flagged as problematic or missing.
python fix_product_images.py
"""

import time
import json
import urllib.request
import urllib.parse
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from routes.product_all_data import ALL_PRODUCTS
from routes.product_images import PRODUCT_IMAGES

OFT  = "https://world.openfoodfacts.org/cgi/search.pl"
OBF  = "https://world.openbeautyfacts.org/cgi/search.pl"
HEADERS = {"User-Agent": "CheckKaro/1.0 (educational project)"}

BAD_LANG = ['_fr.', '_ar.', '_es.', '_de.', '_it.', '_pt.', '_nl.', '_pl.', '_ru.']

COSMETIC_CATEGORIES = {
    "Skincare", "Hair Care", "Cosmetics", "Personal Care",
    "Baby Care", "Oral Care", "Household"
}

# Manually verified correct image URLs for products that search keeps getting wrong
MANUAL_OVERRIDES = {
    # These have wrong-language labels — clear them so re-search picks up English version
    "pepsi": None,
    "sprite": None,
    "maaza": None,
    "haldiram-sev": None,
    "doritos": None,
    "knorr-soupy": None,
    "patanjali-atta-noodles": None,
    "nestle-milkybar": None,
    "junior-horlicks": None,
    "head-shoulders": None,
    "patanjali-atta": None,
    "b-natural-mango": None,
    "nescafe-classic": None,
    "axe-deo": None,
    "daawat-basmati": None,
    "happilo-cashews": None,
    "monster-energy": None,
    "tulsi-green-tea": None,
    "vahdam-tea": None,
    "mcvities-digestive": None,
    "mdh-dal-makhani-masala": None,
    "pepsodent-whitening-toothpaste": None,
    # Duplicates — clear one of each pair so it gets re-searched
    "amul-milk-chocolate": None,    # duplicate of amul-dark-chocolate
    "lipton-honey-lemon-green-tea": None,  # duplicate of green-tea-lipton
}


def is_good_url(url):
    if not url:
        return False
    if not url.startswith("https://images.openfoodfacts.org") and \
       not url.startswith("https://images.openbeautyfacts.org"):
        return False
    for bad in BAD_LANG:
        if bad in url:
            return False
    return True


def search_api(base_url, query, img_domain, retries=2, page_size=8):
    params = urllib.parse.urlencode({
        "search_terms": query,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "fields": "product_name,brands,image_front_url",
        "page_size": page_size,
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
                if img and img.startswith(img_domain) and is_good_url(img):
                    return img
        except Exception:
            if attempt < retries - 1:
                time.sleep(1)
    return None


def fetch_best_image(name, brand, category):
    is_cosmetic = category in COSMETIC_CATEGORIES
    query = f"{name} {brand}"

    if is_cosmetic:
        url = search_api(OBF, query, "https://images.openbeautyfacts.org")
        if not url:
            # Try with just brand
            url = search_api(OBF, f"{brand} {name.split()[0]}", "https://images.openbeautyfacts.org")
        if not url:
            url = search_api(OFT, query, "https://images.openfoodfacts.org")
    else:
        url = search_api(OFT, query, "https://images.openfoodfacts.org")
        if not url:
            url = search_api(OFT, f"{name} India", "https://images.openfoodfacts.org")
        if not url:
            url = search_api(OBF, query, "https://images.openbeautyfacts.org")
    return url


def main():
    results = dict(PRODUCT_IMAGES)

    # 1. Build list of products to fix: wrong language, duplicates, missing
    to_fix = set()

    # Wrong language
    for k, v in results.items():
        if v and any(bad in v for bad in BAD_LANG):
            to_fix.add(k)

    # Duplicates — fix the second occurrence
    seen_urls = {}
    for k, v in results.items():
        if v:
            if v in seen_urls:
                to_fix.add(k)   # fix the duplicate
            else:
                seen_urls[v] = k

    # Missing images
    for k in ALL_PRODUCTS:
        if not results.get(k):
            to_fix.add(k)

    # Apply manual overrides immediately (no network call)
    for k, v in MANUAL_OVERRIDES.items():
        if v is not None:
            results[k] = v
            to_fix.discard(k)
            print(f"[manual] {k} -> OK")

    total = len(to_fix)
    print(f"\nProducts to fix/fill: {total}")
    fixed = 0

    for idx, key in enumerate(sorted(to_fix)):
        val = ALL_PRODUCTS.get(key)
        if not val:
            continue
        name, brand, category = val[0], val[1], val[2]
        old = results.get(key)
        print(f"[{idx+1}/{total}] {name} ({brand}) [{category}] ... ", end="", flush=True)

        url = fetch_best_image(name, brand, category)
        if url:
            results[key] = url
            fixed += 1
            print("OK")
        else:
            results[key] = old if (old and is_good_url(old)) else None
            print("not found" if not results[key] else "kept existing")
        time.sleep(0.4)

    # Write
    with open("routes/product_images.py", "w", encoding="utf-8") as f:
        f.write('"""\nProduct image URLs -- Open Food Facts + Open Beauty Facts.\nAuto-generated.\n"""\n\n')
        f.write("PRODUCT_IMAGES = {\n")
        for k, v in results.items():
            if v:
                f.write(f'    "{k}": "{v}",\n')
            else:
                f.write(f'    "{k}": None,\n')
        f.write("}\n")

    total_imgs = sum(1 for v in results.values() if v)
    print(f"\nDone. {total_imgs}/464 images total. Fixed/filled {fixed} products.")


if __name__ == "__main__":
    main()
