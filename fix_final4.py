"""Fix the last 4 products without any image URL."""
import sys, os, requests, time
sys.path.insert(0, 'backend')
from dotenv import load_dotenv
load_dotenv('backend/.env')
from supabase import create_client

SUPABASE_URL = os.environ['SUPABASE_URL']
SERVICE_KEY  = os.environ['SUPABASE_SERVICE_ROLE_KEY']
sb = create_client(SUPABASE_URL, SERVICE_KEY)

UA = {"User-Agent": "Mozilla/5.0 (compatible; ParkhoApp/1.0)"}

def wikipedia_image(title):
    try:
        r = requests.get("https://en.wikipedia.org/w/api.php",
                         params={"action": "query", "titles": title, "prop": "pageimages",
                                 "format": "json", "pithumbsize": 600},
                         headers=UA, timeout=12)
        pages = r.json().get("query", {}).get("pages", {})
        for page in pages.values():
            src = page.get("thumbnail", {}).get("source")
            if src:
                return src
    except Exception as e:
        print(f"  Wiki error: {e}")
    return None

def openfoodfacts_image(query):
    try:
        r = requests.get("https://world.openfoodfacts.org/cgi/search.pl",
                         params={"search_terms": query, "action": "process",
                                 "json": 1, "page_size": 5},
                         headers=UA, timeout=15)
        for p in r.json().get("products", []):
            img = p.get("image_url") or p.get("image_front_url")
            if img and img.startswith("https://images.openfoodfacts.org"):
                return img
    except Exception:
        pass
    return None

LAST4 = {
    "Kellogg's Corn Flakes": [
        ("wiki", "Corn_Flakes"),
        ("off",  "Kellogg Corn Flakes 250g"),
        ("direct", "https://upload.wikimedia.org/wikipedia/commons/b/bf/Corn_Flakes_in_bowl_with_milk.jpg"),
    ],
    "Knorr Classic Tomato Soup": [
        ("off",  "Knorr tomato soup India"),
        ("wiki", "Knorr"),
        ("direct", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Knorr_logo.svg/500px-Knorr_logo.svg.png"),
    ],
    "Yoga Bar Oats And Berries Bar": [
        ("off",  "Yoga Bar oats berries ITC bar"),
        ("direct", "https://itcstore.in/media/catalog/product/y/b/yb_oats_berries.jpg"),
    ],
    "St. Ives Apricot Scrub": [
        ("off",  "St Ives apricot fresh skin exfoliating"),
        ("wiki", "St._Ives_(brand)"),
        ("direct", "https://upload.wikimedia.org/wikipedia/en/thumb/d/d0/St_Ives_logo.svg/500px-St_Ives_logo.svg.png"),
    ],
}

def resolve(steps):
    for kind, val in steps:
        if kind == "wiki":
            url = wikipedia_image(val)
            if url:
                print(f"    Wikipedia OK: {url[:70]}")
                return url
            time.sleep(1)
        elif kind == "off":
            url = openfoodfacts_image(val)
            if url:
                print(f"    OpenFoodFacts OK: {url[:70]}")
                return url
            time.sleep(0.5)
        elif kind == "direct":
            print(f"    Using direct URL: {val[:70]}")
            return val
    return None

def main():
    for name, steps in LAST4.items():
        print(f"\n[{name}]")
        url = resolve(steps)
        if not url:
            print(f"  No image found")
            continue
        res = sb.table('ai_extracted_products').select('id').ilike('name', name).limit(1).execute()
        if not res.data:
            continue
        sb.table('ai_extracted_products').update({"image_url": url}).eq('id', res.data[0]['id']).execute()
        print(f"  Updated in DB")

if __name__ == "__main__":
    main()
