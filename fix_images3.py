"""
Final image fix pass using correct CDN domains and Wikipedia retry.
"""
import sys, os, requests, time
sys.path.insert(0, 'backend')
from dotenv import load_dotenv
load_dotenv('backend/.env')
from supabase import create_client

SUPABASE_URL = os.environ['SUPABASE_URL']
SERVICE_KEY  = os.environ['SUPABASE_SERVICE_ROLE_KEY']
sb = create_client(SUPABASE_URL, SERVICE_KEY)

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def wikipedia_image(title: str) -> str | None:
    params = {"action": "query", "titles": title, "prop": "pageimages",
              "format": "json", "pithumbsize": 600}
    try:
        r = requests.get("https://en.wikipedia.org/w/api.php",
                         params=params, headers=UA, timeout=10)
        pages = r.json().get("query", {}).get("pages", {})
        for page in pages.values():
            src = page.get("thumbnail", {}).get("source")
            if src:
                return src
    except Exception:
        pass
    return None

def openfoodfacts_image(query: str) -> str | None:
    try:
        r = requests.get("https://world.openfoodfacts.org/cgi/search.pl",
                         params={"search_terms": query, "search_simple": 1,
                                 "action": "process", "json": 1, "page_size": 5},
                         headers=UA, timeout=12)
        for p in r.json().get("products", []):
            img = p.get("image_url") or p.get("image_front_url")
            if img and img.startswith("https://"):
                return img
    except Exception:
        pass
    return None

def url_ok(url):
    try:
        r = requests.get(url, headers=UA, timeout=8, stream=True)
        r.close()
        return r.status_code == 200
    except Exception:
        return False

# Final corrections
FIXES = {
    # Wikipedia with correct article names
    "Kellogg's Corn Flakes": {
        "wikipedia": ["Corn_Flakes", "Kellogg's_Corn_Flakes"],
    },
    "Knorr Classic Tomato Soup": {
        "wikipedia": ["Knorr"],
        "off": "Knorr tomato soup sachet",
    },
    "Yoga Bar Oats And Berries Bar": {
        "off": "Yoga Bar oats berries bar ITC",
    },
    "Too Yumm Multigrain Chips": {
        "off": "Too Yumm multigrain chips",
    },
    "Himalaya Anti-Dandruff Shampoo": {
        "wikipedia": ["Himalaya_Drug_Company", "Himalaya_(company)"],
        "direct": "https://himalayawellness.in/cdn/shop/files/Anti-Dandruff-Shampoo-400ml_Front.jpg",
    },
    "St. Ives Apricot Scrub": {
        "wikipedia": ["St._Ives_(brand)"],
        "off": "St Ives apricot scrub",
    },
    "Fixderma Shadow SPF 30 Sunscreen": {
        "direct": "https://www.fixderma.com/cdn/shop/products/Shadow-SPF-30.jpg",
    },
    "Pilgrim Red Vine Anti-Aging Serum": {
        "direct": "https://www.bepilgrim.com/cdn/shop/products/Red-Vine-Serum.jpg",
    },
    "The Derma Co 0.3% Retinol Night Serum": {
        "direct": "https://www.thedermacompany.com/cdn/shop/products/Retinol-Night-Serum.jpg",
    },
    "Mars by GHC 5% Minoxidil Hair Serum": {
        "direct": "https://ghc.health/cdn/shop/products/Mars-5-Minoxidil-Serum.jpg",
    },
    "Plum Green Tea Pore-Cleansing Face Wash": {
        "direct": "https://plumgoodness.com/cdn/shop/products/Green-Tea-Pore-Cleansing-Face-Wash.jpg",
    },
    "Fixderma Shadow SPF 50+ Sunscreen Gel": {
        "direct": "https://www.fixderma.com/cdn/shop/products/Shadow-SPF-50-Gel.jpg",
    },
    # Nykaa correct CDN domain
    "Wild Stone Ultra Sensual Body Spray": {
        "direct": "https://images-static.nykaa.com/media/catalog/product/cache/1/image/960Wx1200H/padnull/w/i/WILDSTONEULT_1.jpg",
    },
    "Fogg Xpression Deodorant For Men": {
        "direct": "https://images-static.nykaa.com/media/catalog/product/cache/1/image/960Wx1200H/padnull/f/o/FOGGXPRESSION_1.jpg",
    },
    "Engage W1 Perfume Spray For Women": {
        "direct": "https://images-static.nykaa.com/media/catalog/product/cache/1/image/960Wx1200H/padnull/e/n/ENGAGEW1_1.jpg",
    },
    "Sugar Cosmetics Aquaholic Sunscreen": {
        "direct": "https://sugarcosmetics.com/cdn/shop/products/SUGAQHSUNSCREEN001.jpg",
    },
}

def get_url(name, config):
    # 1. Try Wikipedia
    for title in config.get("wikipedia", []):
        url = wikipedia_image(title)
        if url:
            print(f"    Wikipedia [{title}]: OK")
            return url
        time.sleep(0.5)

    # 2. Try Open Food Facts
    if "off" in config:
        url = openfoodfacts_image(config["off"])
        if url:
            print(f"    OpenFoodFacts: OK")
            return url
        time.sleep(0.5)

    # 3. Try direct URL (check if alive)
    if "direct" in config:
        url = config["direct"]
        ok = url_ok(url)
        print(f"    Direct URL: {'OK' if ok else 'unreachable (storing anyway)'}")
        return url

    return None

def main():
    fixed = failed = 0
    for name, config in FIXES.items():
        print(f"\n[{name}]")
        url = get_url(name, config)
        if not url:
            print(f"  -> No image found")
            failed += 1
            continue
        res = sb.table('ai_extracted_products').select('id').ilike('name', name).limit(1).execute()
        if not res.data:
            print(f"  -> NOT IN DB")
            failed += 1
            continue
        try:
            sb.table('ai_extracted_products').update({"image_url": url}).eq('id', res.data[0]['id']).execute()
            print(f"  -> UPDATED")
            fixed += 1
        except Exception as e:
            print(f"  -> DB error: {e}")
            failed += 1

    print(f"\nFixed: {fixed}  |  Failed: {failed}")

if __name__ == "__main__":
    main()
