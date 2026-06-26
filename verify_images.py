"""Check which image URLs actually load in the database."""
import sys, os, requests
sys.path.insert(0, 'backend')
from dotenv import load_dotenv
load_dotenv('backend/.env')
from supabase import create_client

SUPABASE_URL = os.environ['SUPABASE_URL']
SERVICE_KEY  = os.environ['SUPABASE_SERVICE_ROLE_KEY']
sb = create_client(SUPABASE_URL, SERVICE_KEY)

BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.bigbasket.com/",
}

# Get newly inserted products (those we just added)
target_names = [
    "Nestle KitKat 4 Finger", "Parle Monaco Classic", "Parle Krackjack",
    "Paper Boat Frooti Mango Drink", "Sting Energy Drink Berry Blast",
    "Quaker Oats Original", "Kellogg's Corn Flakes", "Kellogg's Chocos",
    "Sunfeast Yippee Magic Masala Noodles", "Knorr Classic Tomato Soup",
    "Yoga Bar Oats And Berries Bar", "Too Yumm Multigrain Chips",
    "Himalaya Anti-Dandruff Shampoo", "St. Ives Apricot Scrub",
    "Re'equil Oxi-Moist Moisturizer SPF 15", "Fixderma Shadow SPF 30 Sunscreen",
    "Pilgrim Salicylic Acid Face Wash", "Pilgrim Red Vine Anti-Aging Serum",
    "The Derma Co 1% Hyaluronic Acid Serum", "The Derma Co 0.3% Retinol Night Serum",
    "Kama Ayurveda Kumkumadi Oil", "Mars by GHC 5% Minoxidil Hair Serum",
    "Plum Green Tea Pore-Cleansing Face Wash", "Aqualogica Glow+ Dewy Sunscreen SPF 50",
    "Fixderma Shadow SPF 50+ Sunscreen Gel", "Wild Stone Ultra Sensual Body Spray",
    "Fogg Xpression Deodorant For Men", "Engage W1 Perfume Spray For Women",
    "Sugar Cosmetics Aquaholic Sunscreen",
]

working, broken = [], []

for name in target_names:
    res = sb.table('ai_extracted_products').select('id,image_url').ilike('name', name).limit(1).execute()
    if not res.data:
        print(f"  NOT FOUND: {name}")
        continue

    row = res.data[0]
    url = row.get('image_url') or ''

    if not url:
        print(f"  NO IMAGE: {name}")
        broken.append(name)
        continue

    try:
        r = requests.get(url, headers=BROWSER_HEADERS, timeout=8, stream=True)
        ct = r.headers.get('content-type', '')
        r.close()
        if r.status_code == 200 and ('image' in ct or url.endswith(('.jpg', '.png', '.webp', '.svg'))):
            print(f"  OK  [{r.status_code}] {name}")
            working.append(name)
        else:
            print(f"  BAD [{r.status_code}] {name} -- {url[:60]}")
            broken.append(name)
    except Exception as e:
        print(f"  ERR {name}: {e}")
        broken.append(name)

print(f"\nWorking: {len(working)}/{len(target_names)}")
print(f"Broken/missing: {len(broken)}")
if broken:
    print("Need fixing:")
    for n in broken:
        print(f"  - {n}")
