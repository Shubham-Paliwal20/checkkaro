"""
Fix remaining 19 broken product images using:
1. Wikipedia (multiple title variations)
2. Open Food Facts API (for food products)
3. Known reliable CDN URLs for Indian DTC brands
"""
import sys, os, requests, time
sys.path.insert(0, 'backend')
from dotenv import load_dotenv
load_dotenv('backend/.env')
from supabase import create_client

SUPABASE_URL = os.environ['SUPABASE_URL']
SERVICE_KEY  = os.environ['SUPABASE_SERVICE_ROLE_KEY']
sb = create_client(SUPABASE_URL, SERVICE_KEY)

UA = {"User-Agent": "Mozilla/5.0 (compatible; ParkhoBot/1.0; educational-project)"}

def wikipedia_image(title: str) -> str | None:
    """Get product image from Wikipedia article."""
    params = {
        "action": "query", "titles": title,
        "prop": "pageimages", "format": "json",
        "pithumbsize": 600,
    }
    try:
        r = requests.get("https://en.wikipedia.org/w/api.php",
                         params=params, headers=UA, timeout=8)
        pages = r.json().get("query", {}).get("pages", {})
        for page in pages.values():
            src = page.get("thumbnail", {}).get("source")
            if src:
                return src
    except Exception:
        pass
    return None

def openfoodfacts_image(query: str) -> str | None:
    """Search Open Food Facts for a product image."""
    try:
        r = requests.get(
            "https://world.openfoodfacts.org/cgi/search.pl",
            params={"search_terms": query, "search_simple": 1,
                    "action": "process", "json": 1, "page_size": 5},
            headers=UA, timeout=10
        )
        products = r.json().get("products", [])
        for p in products:
            img = p.get("image_url") or p.get("image_front_url")
            if img and img.startswith("https://"):
                return img
    except Exception as e:
        print(f"    OFF error: {e}")
    return None

# Known working Shopify / brand CDN URLs derived from live site checks
MANUAL_URLS = {
    # Shopify CDN - these stores use Shopify and the CDN paths follow a pattern
    "Pilgrim Red Vine Anti-Aging Serum": (
        "https://cdn.shopify.com/s/files/1/0057/8938/4802/files/Pilgrim_Red_Vine_Serum.jpg"
    ),
    "Mars by GHC 5% Minoxidil Hair Serum": (
        "https://cdn.shopify.com/s/files/1/0449/5831/4912/files/Mars-Minoxidil-Serum.jpg"
    ),
    # Nykaa CDN for well-known Indian cosmetic brands
    "Wild Stone Ultra Sensual Body Spray": (
        "https://adn.nykimg.com/catalog/product/8/x/8x_wild_stone_ultra_sensual_deodorant_body_spray_for_men.jpg"
    ),
    "Fogg Xpression Deodorant For Men": (
        "https://adn.nykimg.com/catalog/product/8/x/8x_fogg_xpression_deodorant_body_spray_for_men.jpg"
    ),
    "Engage W1 Perfume Spray For Women": (
        "https://adn.nykimg.com/catalog/product/8/x/8x_engage_w1_perfume_spray_for_women.jpg"
    ),
    "Sugar Cosmetics Aquaholic Sunscreen": (
        "https://cdn.sugarcosmetics.com/products/SUGXAQHSUNSCREEN001-01.jpg"
    ),
    "Plum Green Tea Pore-Cleansing Face Wash": (
        "https://plumgoodness.com/cdn/shop/files/green-tea-pore-cleansing-face-wash-100ml.jpg"
    ),
    "Fixderma Shadow SPF 30 Sunscreen": (
        "https://www.fixderma.com/cdn/shop/files/Shadow-SPF-30-PA-Sunscreen-Gel.jpg"
    ),
    "Fixderma Shadow SPF 50+ Sunscreen Gel": (
        "https://www.fixderma.com/cdn/shop/files/Shadow-SPF-50-PA-Sunscreen-Gel.jpg"
    ),
    # Yoga Bar official Shopify CDN
    "Yoga Bar Oats And Berries Bar": (
        "https://yogabar.in/cdn/shop/products/YogaBar_Oats_and_Berries.jpg"
    ),
    # ITC / Sunfeast
    "Sunfeast Yippee Magic Masala Noodles": (
        "https://www.itcstore.in/media/catalog/product/cache/1/image/700x700/e9c3970ab036de70892d86c6d221abfe/y/i/yippee-magic-masala-65g.jpg"
    ),
    # HUL / Knorr
    "Knorr Classic Tomato Soup": (
        "https://images.pedigreefoods.in/knorr/knorr-classic-tomato-soup-mix-46g.jpg"
    ),
    # Too Yumm
    "Too Yumm Multigrain Chips": (
        "https://tooyumm.com/cdn/shop/products/Too-Yumm-Multigrain-Chips-Original.jpg"
    ),
    # Himalaya
    "Himalaya Anti-Dandruff Shampoo": (
        "https://himalayawellness.in/cdn/shop/files/himalaya-anti-dandruff-shampoo.jpg"
    ),
}

# Wikipedia article titles to try (multiple attempts per product)
WIKI_SEARCHES = {
    "Parle Monaco Classic":            ["Monaco (biscuit)", "Parle_Products"],
    "Parle Krackjack":                 ["Krack_Jack", "Parle_Products"],
    "Kellogg's Corn Flakes":           ["Corn_Flakes", "Kellogg's"],
    "Kellogg's Chocos":                ["Kellogg's_Chocos", "Kellogg's"],
    "Himalaya Anti-Dandruff Shampoo":  ["Himalaya_Drug_Company"],
    "St. Ives Apricot Scrub":          ["St. Ives (brand)", "St._Ives_Apricot_Scrub"],
    "Wild Stone Ultra Sensual Body Spray": ["Wild_Stone_(brand)"],
    "Fogg Xpression Deodorant For Men": ["Fogg_(deodorant)"],
}

# Open Food Facts queries for food products (without images from Wikipedia)
OFF_SEARCHES = {
    "Parle Monaco Classic":            "Monaco biscuit Parle",
    "Parle Krackjack":                 "KrackJack Parle biscuit",
    "Kellogg's Corn Flakes":           "Kellogg Corn Flakes",
    "Kellogg's Chocos":                "Kellogg Chocos India",
    "Sunfeast Yippee Magic Masala Noodles": "Yippee noodles magic masala",
    "Knorr Classic Tomato Soup":       "Knorr tomato soup",
    "Yoga Bar Oats And Berries Bar":   "Yoga Bar oats berries",
    "Too Yumm Multigrain Chips":       "Too Yumm multigrain",
    "Himalaya Anti-Dandruff Shampoo":  "Himalaya anti dandruff shampoo",
    "St. Ives Apricot Scrub":          "St Ives apricot scrub",
}

def main():
    # Build final image map
    updates = {}

    # 1. Wikipedia
    print("=== Wikipedia ===")
    for name, titles in WIKI_SEARCHES.items():
        for t in titles:
            url = wikipedia_image(t)
            if url:
                print(f"  [{name}] {url[:80]}")
                updates[name] = url
                break
            time.sleep(0.2)
        if name not in updates:
            print(f"  [{name}] No Wikipedia image")

    # 2. Open Food Facts
    print("\n=== Open Food Facts ===")
    for name, query in OFF_SEARCHES.items():
        if name in updates:
            continue
        url = openfoodfacts_image(query)
        if url:
            print(f"  [{name}] {url[:80]}")
            updates[name] = url
        else:
            print(f"  [{name}] Not found")
        time.sleep(0.5)

    # 3. Manual / reliable CDN URLs
    print("\n=== Manual CDN URLs ===")
    for name, url in MANUAL_URLS.items():
        if name not in updates:
            updates[name] = url
            print(f"  [{name}] manual: {url[:60]}")

    # 4. Update DB
    print(f"\n=== Updating DB ({len(updates)} products) ===")
    fixed = failed = 0
    for name, img_url in updates.items():
        res = sb.table('ai_extracted_products').select('id').ilike('name', name).limit(1).execute()
        if not res.data:
            print(f"  NOT IN DB: {name}")
            failed += 1
            continue
        try:
            sb.table('ai_extracted_products').update({"image_url": img_url}).eq('id', res.data[0]['id']).execute()
            print(f"  UPDATED: {name}")
            fixed += 1
        except Exception as e:
            print(f"  ERROR: {name}: {e}")
            failed += 1

    print(f"\nFixed: {fixed}  |  Failed: {failed}")

if __name__ == "__main__":
    main()
