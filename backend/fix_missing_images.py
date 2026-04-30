"""
Fetch images for the 122 products still missing them.
Uses multiple search strategies and keeps only English-label images.
Run from the backend/ directory:  python fix_missing_images.py
"""

import requests, re, time, json

# Products that need special/shorter search terms instead of using the key
SEARCH_OVERRIDES = {
    "britannia-bourbon":        "Britannia Bourbon biscuit",
    "parle-hide-seek":          "Parle Hide Seek biscuit",
    "sunfeast-moms-magic":      "Sunfeast Moms Magic biscuit",
    "parle-krackjack":          "Parle Krackjack cracker",
    "kurkure-masala":           "Kurkure Masala Munch",
    "bikano-aloo-lachha":       "Bikano Aloo Lachha",
    "balaji-wafers":            "Balaji Wafers potato chips",
    "too-yumm":                 "Too Yumm snack",
    "doritos":                  "Doritos nacho chips",
    "bingo-salted":             "Bingo Mad Angles",
    "sunfeast-yippee-atta":     "Sunfeast Yippee Atta noodles",
    "knorr-soupy":              "Knorr Soupy noodles",
    "patanjali-atta-noodles":   "Patanjali Atta noodles",
    "perk":                     "Cadbury Perk chocolate",
    "cadbury-gems":             "Cadbury Gems",
    "bournvita":                "Cadbury Bournvita",
    "complan":                  "Complan health drink",
    "patanjali-nutrela":        "Nutrela soya chunks",
    "patanjali-mustard-oil":    "Patanjali Mustard oil kachi ghani",
    "everest-garam-masala":     "Everest Garam Masala",
    "everest-chana-masala":     "Everest Chana Masala",
    "mdh-rajma-masala":         "MDH Rajma Masala",
    "everest-kitchen-king":     "Everest Kitchen King Masala",
    "patanjali-haldi":          "Patanjali haldi turmeric powder",
    "mtr-paneer-butter-masala": "MTR Paneer Butter Masala ready",
    "mtr-dal-makhani":          "MTR Dal Makhani ready meal",
    "mtr-palak-paneer":         "MTR Palak Paneer ready",
    "haldiram-ready-to-eat":    "Haldiram ready to eat",
    "real-apple":               "Real Apple juice",
    "paper-boat-aamras":        "Paper Boat Aamras mango",
    "b-natural-mango":          "B Natural mango juice ITC",
    "patanjali-mango-pickle":   "Patanjali mango pickle",
    "rin-detergent":            "Rin Advanced detergent powder",
    "sattu-patanjali":          "Patanjali sattu",
    "forest-essentials-serum":  "Forest Essentials serum",
    "kama-ayurveda-kumkumadi":  "Kama Ayurveda Kumkumadi oil",
    "re-equil-sunscreen":       "Re equil sunscreen",
    "forest-essentials-face-mask": "Forest Essentials face mask",
    "forest-essentials-hair-oil":  "Forest Essentials hair oil",
    "khadi-hair-oil":           "Khadi Natural hair oil",
    "colorbar-bb-cream":        "Colorbar BB cream",
    "colorbar-kajal":           "Colorbar kajal",
    "colorbar-nail-polish":     "Colorbar nail polish",
    "mccain-fries":             "McCain French Fries",
    "tata-sampann-poha":        "Tata Sampann Poha",
    "happydent-gum":            "Happydent White chewing gum",
    "milkybar-choclairs":       "Milkybar Choclairs candy",
    "sunbites-whole-grain":     "Sunbites whole grain snack",
    "tiger-biscuits":           "Tiger biscuit",
    "fortune-basmati-rice":     "Fortune Basmati Rice",
    "daawat-basmati":           "Daawat Basmati Rice",
    "patanjali-besan":          "Patanjali Besan gram flour",
    "id-idli-batter":           "iD Fresh idli batter",
    "id-dosa-batter":           "iD Fresh dosa batter",
    "mtr-rava-idli-mix":        "MTR Rava Idli Mix",
    "mtr-kheer-mix":            "MTR Kheer Mix",
    "eastern-fish-curry-masala":"Eastern Fish Curry Masala",
    "amul-peanut-butter":       "Amul Peanut Butter",
    "myfitness-peanut-butter":  "MyFitness Peanut Butter",
    "sleepy-owl-granola":       "Sleepy Owl Granola",
    "onelife-protein-bar":      "One Life protein bar",
    "yoga-bar-protein":         "Yoga Bar protein bar",
    "true-elements-seeds":      "True Elements seeds mix",
    "farmley-almonds":          "Farmley almonds",
    "happilo-cashews":          "Happilo cashews",
    "hell-energy":              "Hell Energy Drink",
    "tetley-green-tea":         "Tetley Green Tea",
    "tulsi-green-tea":          "Organic India Tulsi Green Tea",
    "patanjali-honey-lemon-tea":"Patanjali Honey Lemon Ginger Tea",
    "chaayos-masala-chai":      "Chaayos Masala Chai",
    "dabur-chyawanprash":       "Dabur Chyawanprash",
    "himalaya-ashwagandha":     "Himalaya Ashwagandha tablet",
    "dabur-amla-juice":         "Dabur Amla juice",
    "vestige-noni-juice":       "Vestige Noni juice",
    "nimbooz":                  "Pepsi Nimbooz lemon drink",
    "glucon-d-original":        "Glucon D orange glucose",
    "gatorade-lemon":           "Gatorade Lemon Lime",
    "amul-kool-chocolate-milk": "Amul Kool chocolate milk",
    "go-cheese-spread":         "Go Cheese Spread",
    "parle-cheeselings":        "Parle Cheeselings",
    "sunfeast-bounce-chocolate":"Sunfeast Bounce chocolate cream biscuit",
    "toblerone-milk-chocolate": "Toblerone milk chocolate",
    "halls-mentho-lyptus":      "Halls Mentho Lyptus",
    "pulse-raw-mango-candy":    "Pass Pass Pulse raw mango candy",
    "center-fresh-spearmint-gum":"Center Fresh spearmint gum",
    "alpenliebe-caramel-candy": "Alpenliebe caramel candy",
    "mango-bite-candy":         "Mango Bite candy Parle",
    "lifebuoy-total-handwash":  "Lifebuoy Total handwash",
    "indulekha-bringha-shampoo":"Indulekha Bringha shampoo",
    "captain-cook-salt":        "Captain Cook iodised salt",
    "saffola-masala-oats-tomato":"Saffola Masala Oats tomato",
    "maggi-pazzta-masala":      "Maggi Pazzta pasta masala",
    "aashirvaad-sambhar-masala":"Aashirvaad Sambhar Masala",
    "amul-mithai-mate":         "Amul Mithai Mate condensed milk",
    "revital-h-multivitamin":   "Revital H multivitamin",
    "baidyanath-chyawanprash":  "Baidyanath Chyawanprash",
    "himalaya-triphala":        "Himalaya Triphala tablet",
    "patanjali-ashwagandha-churna":"Patanjali Ashwagandha churna",
    "himalaya-liv52-syrup":     "Himalaya Liv 52 syrup",
    "haldiram-navrattan-mixture":"Haldiram Navrattan mixture",
    "too-yumm-multigrain":      "Too Yumm multigrain chips",
    "britannia-cheese-croissant":"Britannia Cheese Croissant",
    "domex-toilet-cleaner":     "Domex toilet cleaner",
    "horlicks-lite-health-drink":"Horlicks Lite health drink",
    "bru-gold-coffee":          "Bru Gold instant coffee",
    "knorr-hot-sour-soup":      "Knorr Hot Sour soup",
    "amrutanjan-balm":          "Amrutanjan pain balm",
    "boost-health-drink":       "Boost health drink chocolate",
    "boroline-cream":           "Boroline antiseptic cream",
    "complan-chocolate":        "Complan chocolate health drink",
    "dalda-vanaspati-ghee":     "Dalda vanaspati",
    "haldiram-namkeen-mix":     "Haldiram Namkeen",
    "iodex-fast-relief":        "Iodex Fast Relief",
    "kinley-water":             "Kinley drinking water",
    "kurkure-triangles":        "Kurkure Triangles",
    "maggi-hot-sweet-sauce":    "Maggi Hot Sweet Tomato Chilli Sauce",
    "margo-neem-soap":          "Margo neem soap",
    "odomos-mosquito-repellent":"Odomos mosquito repellent cream",
    "saffola-gold-oil":         "Saffola Gold cooking oil",
    "sunfeast-dream-cream":     "Sunfeast Dream Cream biscuit",
    "thums-up-charged":         "Thums Up Charged",
    "vicks-vaporub":            "Vicks VapoRub",
}

BAD_LANG = re.compile(r'_(fr|ar|es|de|it|pt|nl|pl|ru|zh|ja|ko|tr|uk|ro|bg)\.')

def is_good_url(url: str) -> bool:
    if not url:
        return False
    if BAD_LANG.search(url):
        return False
    if '/front_en' in url or '/front.' in url:
        return True
    # accept if no language suffix present (neutral URL)
    return True

HEADERS = {"User-Agent": "CheckKaro/1.0 (shubhampaliwal5@gmail.com) educational product-awareness app"}

def search_off(query: str, max_results: int = 8, endpoint: str = "in") -> list:
    """Search Open Food Facts (India first, then world) and return image URLs."""
    try:
        url = f"https://{endpoint}.openfoodfacts.org/cgi/search.pl"
        params = {
            "search_terms": query,
            "search_simple": 1,
            "action": "process",
            "json": 1,
            "page_size": max_results,
            "fields": "id,product_name,brands,image_front_url,image_url",
        }
        r = requests.get(url, params=params, headers=HEADERS, timeout=14)
        if r.status_code != 200:
            return []
        data = r.json()
        results = []
        for p in data.get("products", []):
            for field in ("image_front_url", "image_url"):
                img = p.get(field, "")
                if img and is_good_url(img):
                    results.append(img)
                    break
        return results
    except Exception as e:
        print(f"    [ERROR] {e}")
        return []

def try_find_image(key: str) -> str | None:
    query = SEARCH_OVERRIDES.get(key)
    if not query:
        query = key.replace("-", " ")

    # 1. India endpoint
    print(f"  IN '{query}' ...", end="", flush=True)
    urls = search_off(query, endpoint="in")
    if urls:
        print(f" OK {urls[0][:65]}...")
        return urls[0]

    # 2. World endpoint
    print(f" | WORLD ...", end="", flush=True)
    urls = search_off(query, endpoint="world")
    if urls:
        print(f" OK {urls[0][:65]}...")
        return urls[0]

    # 3. Shorter query on India
    words = query.split()
    if len(words) > 2:
        short = " ".join(words[:3])
        print(f" | short '{short}' ...", end="", flush=True)
        urls = search_off(short, endpoint="in")
        if urls:
            print(f" OK {urls[0][:65]}...")
            return urls[0]

    print(" MISS")
    return None


def main():
    # Load current PRODUCT_IMAGES
    images_path = "routes/product_images.py"
    with open(images_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find all keys with None
    none_keys = re.findall(r'"([^"]+)":\s*None,', content)
    print(f"Found {len(none_keys)} products with missing images\n")

    updates = {}
    for key in none_keys:
        print(f"[{key}]")
        img = try_find_image(key)
        if img:
            updates[key] = img
        time.sleep(0.4)

    print(f"\n{'='*60}")
    print(f"Found images for {len(updates)} / {len(none_keys)} products")
    print("Updating product_images.py ...")

    new_content = content
    for key, url in updates.items():
        old = f'"{key}": None,'
        new = f'"{key}": "{url}",'
        new_content = new_content.replace(old, new, 1)

    with open(images_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("Done! Restart the backend to pick up the new images.")
    print("\nProducts still missing images:")
    still_none = [k for k in none_keys if k not in updates]
    for k in still_none:
        print(f"  {k}")


if __name__ == "__main__":
    main()
