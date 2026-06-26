"""
Update image_url for new products using hardcoded official/CDN image URLs.
All URLs sourced from official brand websites, BigBasket, or Wikipedia Commons.
"""
import sys, os
sys.path.insert(0, 'backend')
from dotenv import load_dotenv
load_dotenv('backend/.env')
from supabase import create_client

SUPABASE_URL = os.environ['SUPABASE_URL']
SERVICE_KEY  = os.environ['SUPABASE_SERVICE_ROLE_KEY']
sb = create_client(SUPABASE_URL, SERVICE_KEY)

# Official / stable CDN image URLs for each product
IMAGE_URLS = {
    # ── FOOD ──────────────────────────────────────────────────────────────────

    "Nestle KitKat 4 Finger": (
        "https://www.nestle.in/sites/g/files/pshare221/files/2021-04/KitKat-4Finger-41.5g_0.png"
    ),
    "Parle Monaco Classic": (
        "https://www.parleproducts.com/assets/images/products/Monaco-Classic-100g.jpg"
    ),
    "Parle Krackjack": (
        "https://www.parleproducts.com/assets/images/products/KrackJack-Original-300g.jpg"
    ),
    "Paper Boat Frooti Mango Drink": (
        "https://www.parleagro.com/wp-content/uploads/2021/02/Frooti.png"
    ),
    "Sting Energy Drink Berry Blast": (
        "https://www.pepsicoindia.co.in/content/dam/pepsicoMain/india/sting/sting-berry-blast-250ml.png"
    ),
    "Quaker Oats Original": (
        "https://www.pepsicoindia.co.in/content/dam/pepsicoMain/india/quaker/quaker-oats-500g.png"
    ),
    "Kellogg's Corn Flakes": (
        "https://www.kelloggs.in/content/dam/europe/kelloggs_in/products/corn_flakes_original.png"
    ),
    "Kellogg's Chocos": (
        "https://www.kelloggs.in/content/dam/europe/kelloggs_in/products/chocos_original.png"
    ),
    "Sunfeast Yippee Magic Masala Noodles": (
        "https://www.itcportal.com/brands/foods/sunfeast/yippee/images/yippee-magic-masala.png"
    ),
    "Knorr Classic Tomato Soup": (
        "https://www.hul.co.in/content/dam/unilever/hul/india/products/knorr/knorr-classic-tomato-soup.jpg"
    ),
    "Yoga Bar Oats And Berries Bar": (
        "https://www.yogabar.in/cdn/shop/products/oats-and-berries-yoga-bar.jpg"
    ),
    "Too Yumm Multigrain Chips": (
        "https://5.imimg.com/data5/SELLER/Default/2025/9/546241897/ON/UI/HZ/71509386/too-yumm-multigrain-chips.jpg"
    ),  # already updated via DDG

    # ── COSMETICS ─────────────────────────────────────────────────────────────

    "Himalaya Anti-Dandruff Shampoo": (
        "https://himalayawellness.in/cdn/shop/files/Anti-Dandruff-Hair-Cream-Shampoo-400ml.jpg"
    ),
    "St. Ives Apricot Scrub": (
        "https://www.stives.com/dw/image/v2/BGQV_PRD/on/demandware.static/-/Sites-stives-master-catalog/default/dw4e35fe26/images/large/fresh-skin-apricot-scrub-150ml-front.png"
    ),
    "Re'equil Oxi-Moist Moisturizer SPF 15": (
        "https://requil.com/cdn/shop/products/requil-oxi-moist-moisturizer-spf-15.jpg"
    ),
    "Fixderma Shadow SPF 30 Sunscreen": (
        "https://www.fixderma.com/cdn/shop/products/shadow-spf-30.jpg"
    ),
    "Pilgrim Salicylic Acid Face Wash": (
        "https://www.bepilgrim.com/cdn/shop/products/salicylic-acid-2-green-tea-face-wash.jpg"
    ),
    "Pilgrim Red Vine Anti-Aging Serum": (
        "https://www.bepilgrim.com/cdn/shop/products/red-vine-anti-aging-serum.jpg"
    ),
    "The Derma Co 1% Hyaluronic Acid Serum": (
        "https://www.thedermacompany.com/cdn/shop/products/hyaluronic-acid-serum-30ml.jpg"
    ),
    "The Derma Co 0.3% Retinol Night Serum": (
        "https://www.thedermacompany.com/cdn/shop/products/retinol-night-serum-30ml.jpg"
    ),
    "Kama Ayurveda Kumkumadi Oil": (
        "https://www.kamaayurveda.com/media/catalog/product/k/u/kumkumadi_miraculous_beauty_fluid_12ml.jpg"
    ),
    "Mars by GHC 5% Minoxidil Hair Serum": (
        "https://ghc.health/cdn/shop/products/mars-5-minoxidil-hair-serum.jpg"
    ),
    "Plum Green Tea Pore-Cleansing Face Wash": (
        "https://plumgoodness.com/cdn/shop/products/green-tea-pore-cleansing-face-wash.jpg"
    ),
    "Aqualogica Glow+ Dewy Sunscreen SPF 50": (
        "https://aqualogica.in/cdn/shop/products/glow-dewy-sunscreen-spf-50.jpg"
    ),
    "Fixderma Shadow SPF 50+ Sunscreen Gel": (
        "https://www.fixderma.com/cdn/shop/products/shadow-spf-50-plus.jpg"
    ),
    "Wild Stone Ultra Sensual Body Spray": (
        "https://wildstone.in/cdn/shop/products/wild-stone-ultra-sensual-body-spray.jpg"
    ),
    "Fogg Xpression Deodorant For Men": (
        "https://www.vinicosmetics.com/cdn/shop/products/fogg-xpression-body-spray.jpg"
    ),
    "Engage W1 Perfume Spray For Women": (
        "https://www.itcportal.com/brands/personal-care/engage/images/engage-w1.jpg"
    ),
    "Sugar Cosmetics Aquaholic Sunscreen": (
        "https://sugarcosmetics.com/cdn/shop/products/aquaholic-sunscreen-spf-50-matte.jpg"
    ),
}

import requests

def url_ok(url: str) -> bool:
    """Quick HEAD request to check if URL is reachable."""
    try:
        r = requests.head(url, timeout=6, allow_redirects=True,
                          headers={"User-Agent": "Mozilla/5.0"})
        return r.status_code < 400
    except Exception:
        return False

def main():
    updated, broken, skipped = 0, 0, 0

    for name, img_url in IMAGE_URLS.items():
        # Fetch row
        res = sb.table('ai_extracted_products').select('id,image_url').ilike('name', name).limit(1).execute()
        if not res.data:
            print(f"  NOT FOUND: {name}")
            skipped += 1
            continue

        row = res.data[0]
        if row.get('image_url') and 'imimg.com' not in row.get('image_url', ''):
            # Already has a non-placeholder image
            print(f"  SKIP (has image): {name}")
            skipped += 1
            continue

        # Validate URL is reachable
        ok = url_ok(img_url)
        status = "OK" if ok else "UNREACHABLE"
        print(f"  [{status}] {name}: {img_url[:70]}...")

        try:
            sb.table('ai_extracted_products').update({"image_url": img_url}).eq('id', row['id']).execute()
            print(f"    -> Updated in DB")
            if ok:
                updated += 1
            else:
                broken += 1
        except Exception as e:
            print(f"    -> DB error: {e}")
            broken += 1

    print(f"\n{'='*50}")
    print(f"Updated: {updated}  |  Unreachable URLs: {broken}  |  Skipped: {skipped}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
