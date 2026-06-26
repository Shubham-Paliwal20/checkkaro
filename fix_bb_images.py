"""
Search BigBasket's product API to find correct image URLs for broken products.
BigBasket returns JSON from their product search endpoint.
"""
import sys, os, requests, time, re
sys.path.insert(0, 'backend')
from dotenv import load_dotenv
load_dotenv('backend/.env')
from supabase import create_client

SUPABASE_URL = os.environ['SUPABASE_URL']
SERVICE_KEY  = os.environ['SUPABASE_SERVICE_ROLE_KEY']
sb = create_client(SUPABASE_URL, SERVICE_KEY)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-IN,en;q=0.9",
    "Referer": "https://www.bigbasket.com/",
    "x-channel": "BB-WEB",
}

BB_SEARCH = "https://www.bigbasket.com/product/get-products/"

def bigbasket_image(query: str) -> str | None:
    """Search BigBasket and return the first product image URL."""
    try:
        params = {
            "slug": query,
            "tab_type": '["prd"]',
            "sub_cat_id": "",
            "brand": "",
            "sort": "",
            "desc": "",
            "per_page": "5",
            "page": "1",
        }
        r = requests.get(BB_SEARCH, params=params, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            return None
        data = r.json()
        prods = (
            data.get("tab", {}).get("prd", {}).get("prod", []) or
            data.get("products", []) or
            []
        )
        for p in prods:
            img = (
                p.get("w") or          # web image
                p.get("wi") or         # web image alternate key
                p.get("image") or
                p.get("imgs", {}).get("w") if isinstance(p.get("imgs"), dict) else None
            )
            if img:
                # BigBasket sometimes gives relative paths
                if img.startswith("//"):
                    img = "https:" + img
                elif img.startswith("/media"):
                    img = "https://www.bigbasket.com" + img
                return img
    except Exception as e:
        print(f"    BB error: {e}")
    return None

def wikipedia_image(title: str) -> str | None:
    """Get product image thumbnail from Wikipedia."""
    api = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query", "titles": title,
        "prop": "pageimages", "format": "json",
        "pithumbsize": 500,
    }
    try:
        r = requests.get(api, params=params, timeout=8,
                         headers={"User-Agent": "Mozilla/5.0"})
        pages = r.json().get("query", {}).get("pages", {})
        for page in pages.values():
            src = page.get("thumbnail", {}).get("source")
            if src:
                return src
    except Exception:
        pass
    return None

# Products to fix and their search queries
BROKEN = {
    "Parle Monaco Classic":            ("Parle Monaco Classic biscuits", "Parle Monaco"),
    "Parle Krackjack":                 ("Parle KrackJack biscuits", "Parle KrackJack"),
    "Paper Boat Frooti Mango Drink":   ("Frooti mango drink", "Frooti"),
    "Sting Energy Drink Berry Blast":  ("Sting energy drink berry blast", "Sting Energy"),
    "Kellogg's Corn Flakes":           ("Kellogg's Corn Flakes", "Corn_Flakes"),
    "Kellogg's Chocos":                ("Kellogg Chocos", "Kellogg's_Chocos"),
    "Sunfeast Yippee Magic Masala Noodles": ("Yippee Magic Masala noodles", "Sunfeast_Yippee"),
    "Knorr Classic Tomato Soup":       ("Knorr tomato soup", "Knorr"),
    "Yoga Bar Oats And Berries Bar":   ("Yoga Bar oats berries", None),
    "Too Yumm Multigrain Chips":       ("Too Yumm multigrain chips", None),
    "Himalaya Anti-Dandruff Shampoo":  ("Himalaya anti dandruff shampoo", "Himalaya_Drug_Company"),
    "St. Ives Apricot Scrub":          ("St Ives apricot scrub", "St._Ives_(brand)"),
    "Fixderma Shadow SPF 30 Sunscreen":("Fixderma Shadow SPF 30 sunscreen", None),
    "Pilgrim Red Vine Anti-Aging Serum":("Pilgrim red vine serum", None),
    "Mars by GHC 5% Minoxidil Hair Serum": ("Mars GHC minoxidil hair serum", None),
    "Plum Green Tea Pore-Cleansing Face Wash": ("Plum green tea face wash", None),
    "Fixderma Shadow SPF 50+ Sunscreen Gel": ("Fixderma Shadow SPF 50 sunscreen gel", None),
    "Wild Stone Ultra Sensual Body Spray": ("Wild Stone Ultra Sensual body spray", "Wild_Stone_(brand)"),
    "Fogg Xpression Deodorant For Men": ("Fogg Xpression deodorant men", None),
    "Engage W1 Perfume Spray For Women": ("Engage W1 perfume spray women", None),
    "Sugar Cosmetics Aquaholic Sunscreen": ("Sugar cosmetics aquaholic sunscreen", None),
}

def main():
    fixed, failed = 0, 0

    for name, (bb_query, wiki_title) in BROKEN.items():
        print(f"\n  [{name}]")

        img_url = None

        # 1. Try Wikipedia first (very reliable for global brands)
        if wiki_title:
            img_url = wikipedia_image(wiki_title)
            if img_url:
                print(f"    Wikipedia: {img_url[:80]}")
            time.sleep(0.2)

        # 2. Try BigBasket search
        if not img_url:
            img_url = bigbasket_image(bb_query)
            if img_url:
                print(f"    BigBasket: {img_url[:80]}")
            time.sleep(1)

        if not img_url:
            print(f"    No image found")
            failed += 1
            continue

        # Update DB
        res = sb.table('ai_extracted_products').select('id').ilike('name', name).limit(1).execute()
        if not res.data:
            print(f"    NOT IN DB")
            failed += 1
            continue

        try:
            sb.table('ai_extracted_products').update({"image_url": img_url}).eq('id', res.data[0]['id']).execute()
            print(f"    UPDATED")
            fixed += 1
        except Exception as e:
            print(f"    DB error: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Fixed: {fixed}  |  Failed: {failed}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
