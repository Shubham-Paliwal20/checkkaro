"""
Update image_url for all newly inserted products using DuckDuckGo image search.
"""
import sys, os, time
sys.path.insert(0, 'backend')
from dotenv import load_dotenv
load_dotenv('backend/.env')
from supabase import create_client
from duckduckgo_search import DDGS

SUPABASE_URL = os.environ['SUPABASE_URL']
SERVICE_KEY  = os.environ['SUPABASE_SERVICE_ROLE_KEY']
sb = create_client(SUPABASE_URL, SERVICE_KEY)

# Products inserted in this batch (those with image_url = NULL)
PRODUCT_QUERIES = {
    "Nestle KitKat 4 Finger":              "Nestle KitKat 4 Finger chocolate bar pack",
    "Parle Monaco Classic":                "Parle Monaco Classic salted biscuit pack India",
    "Parle Krackjack":                     "Parle Krackjack sweet salty biscuit pack India",
    "Paper Boat Frooti Mango Drink":       "Paper Boat Frooti mango drink 200ml tetra pack",
    "Sting Energy Drink Berry Blast":      "Sting Energy Drink Berry Blast 250ml can",
    "Quaker Oats Original":                "Quaker Oats original 500g pouch India",
    "Kellogg's Corn Flakes":               "Kellogg's Corn Flakes original 250g box India",
    "Kellogg's Chocos":                    "Kellogg's Chocos choco fills cereal box India",
    "Sunfeast Yippee Magic Masala Noodles": "Sunfeast Yippee Magic Masala instant noodles packet",
    "Knorr Classic Tomato Soup":           "Knorr Classic Tomato Soup sachet India",
    "Yoga Bar Oats And Berries Bar":       "Yoga Bar Oats Berries energy bar wrapper India",
    "Too Yumm Multigrain Chips":           "Too Yumm Multigrain Chips original packet",
    "Himalaya Anti-Dandruff Shampoo":      "Himalaya Anti-Dandruff shampoo green bottle 400ml",
    "St. Ives Apricot Scrub":             "St Ives Fresh Skin Apricot Scrub face scrub tube",
    "Re'equil Oxi-Moist Moisturizer SPF 15": "Requil Oxi Moist moisturiser sunscreen SPF 15 tube",
    "Fixderma Shadow SPF 30 Sunscreen":   "Fixderma Shadow SPF 30 sunscreen tube India",
    "Pilgrim Salicylic Acid Face Wash":   "Pilgrim Salicylic Acid 2% Green Tea face wash tube",
    "Pilgrim Red Vine Anti-Aging Serum":  "Pilgrim Red Vine hyaluronic acid anti aging serum",
    "The Derma Co 1% Hyaluronic Acid Serum": "The Derma Co Hyaluronic Acid serum dropper bottle",
    "The Derma Co 0.3% Retinol Night Serum": "Derma Co 0.3% Retinol Peptide night serum",
    "Kama Ayurveda Kumkumadi Oil":        "Kama Ayurveda Kumkumadi Miraculous Beauty Fluid oil",
    "Mars by GHC 5% Minoxidil Hair Serum": "Mars by GHC 5% Minoxidil hair serum scalp",
    "Plum Green Tea Pore-Cleansing Face Wash": "Plum Green Tea pore cleansing face wash tube",
    "Aqualogica Glow+ Dewy Sunscreen SPF 50": "Aqualogica Glow Dewy Sunscreen SPF 50 PA++++ tube",
    "Fixderma Shadow SPF 50+ Sunscreen Gel": "Fixderma Shadow SPF 50+ sunscreen gel tube India",
    "Wild Stone Ultra Sensual Body Spray": "Wild Stone Ultra Sensual deodorant body spray can",
    "Fogg Xpression Deodorant For Men":   "Fogg Xpression perfume body spray men 150ml",
    "Engage W1 Perfume Spray For Women":  "Engage W1 perfume spray women 150ml bottle",
    "Sugar Cosmetics Aquaholic Sunscreen": "Sugar Cosmetics Aquaholic Sunscreen SPF 50 matte",
}

def get_image(query: str, retries: int = 3) -> str | None:
    """Search DuckDuckGo Images and return the first result URL."""
    for attempt in range(retries):
        try:
            with DDGS() as ddgs:
                results = list(ddgs.images(
                    query,
                    region="in-en",
                    safesearch="off",
                    max_results=5,
                ))
            for r in results:
                url = r.get("image") or r.get("thumbnail")
                if url:
                    return url
        except Exception as e:
            msg = str(e)
            if "Ratelimit" in msg or "403" in msg:
                wait = 12 * (attempt + 1)
                print(f"    Rate-limited. Waiting {wait}s before retry {attempt+1}/{retries}...")
                time.sleep(wait)
            else:
                print(f"    DDG error: {e}")
                break
    return None

def main():
    updated, failed = 0, 0

    for name, query in PRODUCT_QUERIES.items():
        # Check if already has an image
        res = sb.table('ai_extracted_products').select('id,image_url').ilike('name', name).limit(1).execute()
        if not res.data:
            print(f"  [{name}] NOT FOUND in DB -- skipping")
            continue

        row = res.data[0]
        if row.get('image_url'):
            print(f"  [{name}] already has image -- skipping")
            updated += 1
            continue

        print(f"  [{name}] Searching: {query[:60]}...")
        url = get_image(query)
        if url:
            print(f"    Found: {url[:80]}...")
            try:
                sb.table('ai_extracted_products').update({"image_url": url}).eq('id', row['id']).execute()
                print(f"    Updated!")
                updated += 1
            except Exception as e:
                print(f"    DB error: {e}")
                failed += 1
        else:
            print(f"    No image found")
            failed += 1

        time.sleep(8)  # long delay to avoid DuckDuckGo rate limit

    print(f"\nDone! Updated: {updated}  |  Failed: {failed}")

if __name__ == "__main__":
    main()
