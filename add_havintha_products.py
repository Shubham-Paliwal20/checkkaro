"""
Add 41 Havintha products to ai_extracted_products.
"""
import sys, os, re
sys.path.insert(0, 'backend')
from dotenv import load_dotenv
load_dotenv('backend/.env')
from supabase import create_client
from routes.ingredient_database import classify_ingredient, INGREDIENT_DESCRIPTIONS

SUPABASE_URL = os.environ['SUPABASE_URL']
SERVICE_KEY  = os.environ['SUPABASE_SERVICE_ROLE_KEY']
sb = create_client(SUPABASE_URL, SERVICE_KEY)

CDN = "https://havintha.in/cdn/shop/files/"

# ── helpers ───────────────────────────────────────────────────────────────────

def parse_ingredients(raw: str):
    parts, depth, cur = [], 0, ""
    for ch in raw:
        if ch == '(': depth += 1; cur += ch
        elif ch == ')': depth -= 1; cur += ch
        elif ch == ',' and depth == 0:
            p = cur.strip().rstrip('.')
            if p: parts.append(p)
            cur = ""
        else: cur += ch
    if cur.strip(): parts.append(cur.strip().rstrip('.'))
    return parts

def classify_one(name: str) -> dict:
    try:
        cls = classify_ingredient(name)
        if not isinstance(cls, str):
            cls = cls.get('classification', 'generally_recognised')
    except Exception:
        cls = 'generally_recognised'
    key = name.lower().strip()
    raw_desc = (INGREDIENT_DESCRIPTIONS.get(key) or
                INGREDIENT_DESCRIPTIONS.get(re.sub(r'\s*\(.*?\)', '', key).strip()))
    desc = raw_desc if isinstance(raw_desc, dict) else {}
    return {
        "name": name, "aliases": desc.get('aliases', ''), "classification": cls,
        "one_line_note": desc.get('one_line_note', ''), "regulatory_note": desc.get('regulatory_note', ''),
        "commonly_found_in": desc.get('commonly_found_in'), "health_effects": desc.get('health_effects'),
        "countries_restricted": desc.get('countries_restricted', []),
        "fssai_position": desc.get('fssai_position'), "recommendation": desc.get('recommendation'),
    }

def compute_grade(classified):
    if not classified: return "B"
    total = len(classified)
    q = sum(1 for i in classified if i['classification'] == 'commonly_questioned')
    w = sum(1 for i in classified if i['classification'] == 'worth_knowing')
    if q > 0: return "D"
    if w == 0: return "A"
    return "B" if w / total <= 0.30 else "C"

def make_static_key(name: str) -> str:
    return re.sub(r'[^a-z0-9]', '', name.lower())

def make_summary(name, brand, grade, q, w, total):
    if grade == "A":
        return f"{name} by {brand} scores Grade A. All {total} ingredients are generally recognised as safe."
    elif grade == "B":
        return f"{name} by {brand} scores Grade B. {total} ingredients analysed; {w} worth knowing about, no restricted additives."
    elif grade == "C":
        return f"{name} by {brand} scores Grade C. Contains {w} worth-knowing ingredients (>30% of total). Use with awareness."
    else:
        return f"{name} by {brand} scores Grade D. Contains {q} commonly questioned ingredient(s) flagged in some countries."

FSSAI_MAP = {
    "Haircare":     "Hair care products regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
    "Hair Colour":  "Hair colour products regulated under Cosmetics Rules 2020. Patch test recommended before use.",
    "Skincare":     "Cosmetics regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
    "Essential Oil":"Essential oils sold as cosmetics regulated under Cosmetics Rules 2020. Must be diluted before skin use.",
}

# ── catalogue: (name, brand, category, ingredients_raw, image_url) ─────────

PRODUCTS = [
    # ── POWDER SHAMPOOS ──
    (
        "Havintha Natural Hair Shampoo Amla Reetha Shikakai Methi Dana",
        "Havintha", "Haircare",
        "Sapindus Mukorossi, Trigonella Foenum-Graecum, Acacia Concinna, Phyllanthus Emblica",
        CDN + "4_in_1_3e0f3c7a-751f-4ae6-9ca1-e305fc1b3309.png?v=1778912932",
    ),
    (
        "Havintha Natural Bhringraj Brahmi Powder Shampoo",
        "Havintha", "Haircare",
        "Acacia Concinna, Sapindus Mukorossi, Hibiscus Rosa-Sinensis, "
        "Trigonella Foenum-Graecum, Eclipta Prostrata, Linum Usitatissimum, "
        "Bacopa Monnieri, Phyllanthus Emblica",
        CDN + "Website_front_page_27.png?v=1780662354",
    ),
    (
        "Havintha Natural Hibiscus Powder Shampoo",
        "Havintha", "Haircare",
        "Sapindus Mukorossi, Acacia Concinna, Trigonella Foenum-Graecum, "
        "Hibiscus Rosa-Sinensis, Phyllanthus Emblica",
        CDN + "Website_front_page_26.png?v=1779882549",
    ),
    (
        "Havintha Natural Aloevera Powder Shampoo",
        "Havintha", "Haircare",
        "Sapindus Mukorossi, Acacia Concinna, Trigonella Foenum-Graecum, "
        "Aloe Barbadensis",
        CDN + "Face_BOdy_wash_6.png?v=1779192535",
    ),
    # ── HAIR OILS & SPRAYS ──
    (
        "Havintha Jata Amrit Hair Oil",
        "Havintha", "Haircare",
        "Cocos Nucifera Oil, Olea Europaea Oil, Sesamum Indicum Oil, "
        "Aloe Barbadensis, Eclipta Prostrata, Rosmarinus Officinalis, "
        "Phyllanthus Emblica, Acacia Concinna, Bacopa Monnieri, "
        "Trigonella Foenum-Graecum, Hibiscus Rosa-Sinensis, Nigella Sativa, "
        "Nardostachys Jatamansi, Luffa Cylindrica, Azadirachta Indica, "
        "Murraya Koenigii, Cinnamomum Camphora, Ricinus Communis Oil, "
        "Prunus Dulcis Oil, Alkanna Tinctoria, Olea Europaea Raw, "
        "Tocopherol, Melaleuca Alternifolia Oil, Simmondsia Chinensis Oil, "
        "Argania Spinosa Oil, Rosmarinus Officinalis Essential Oil, "
        "Lavandula Angustifolia Oil",
        CDN + "jata_amrit_5371d524-05f8-4427-8e80-3c591ad62d4d.png?v=1778913400",
    ),
    (
        "Havintha Organic Rosemary Hair Oil",
        "Havintha", "Haircare",
        "Fractionated Cocos Nucifera Oil, Ricinus Communis Oil, "
        "Olea Europaea Oil, Rosmarinus Officinalis Raw, "
        "Rosmarinus Officinalis Essential Oil, Tocopherol, "
        "Lavandula Angustifolia Essential Oil",
        CDN + "Website_front_page_9.png?v=1779098566",
    ),
    (
        "Havintha Natural Rosemary Water Spray",
        "Havintha", "Haircare",
        "Rosmarinus Officinalis Hydrosol",
        CDN + "1_24a3e9ab-3ab3-46f9-bdf4-69a777655f26.png?v=1776860240",
    ),
    # ── HAIR COLOUR ──
    (
        "Havintha Natural Indigo Powder",
        "Havintha", "Hair Colour",
        "Indigofera Tinctoria",
        CDN + "Website_front_page_19.png?v=1779796422",
    ),
    (
        "Havintha Natural Henna Powder",
        "Havintha", "Hair Colour",
        "Lawsonia Inermis",
        CDN + "Website_front_page_20.png?v=1779798530",
    ),
    (
        "Havintha Natural Herbal Henna Hair Pack",
        "Havintha", "Hair Colour",
        "Lawsonia Inermis, Trigonella Foenum-Graecum, Acacia Concinna, "
        "Phyllanthus Emblica, Hibiscus Rosa-Sinensis, Senegalia Catechu, "
        "Eclipta Prostrata, Azadirachta Indica, Bacopa Monnieri, "
        "Camellia Sinensis, Indigofera Tinctoria",
        CDN + "herbal_henna.png?v=1779097500",
    ),
    # ── HAIR HERB POWDERS (single ingredient) ──
    (
        "Havintha Natural Amla Powder",
        "Havintha", "Haircare",
        "Phyllanthus Emblica",
        CDN + "47_240a12ce-6fbb-4c6b-8bf5-863bcffae339.png?v=1775197821",
    ),
    (
        "Havintha Organic Shikakai Powder",
        "Havintha", "Haircare",
        "Acacia Concinna",
        CDN + "Shikakaipowder_8c9aa40c-b760-44b9-9373-f8520e77ca9b.png?v=1749459457",
    ),
    (
        "Havintha Natural Reetha Powder",
        "Havintha", "Haircare",
        "Sapindus Mukorossi",
        CDN + "Reethapowder.png?v=1749126990",
    ),
    (
        "Havintha Natural Bhringraj Powder",
        "Havintha", "Haircare",
        "Eclipta Prostrata",
        CDN + "38_5c3271e9-72a1-41a5-8951-f0eba9da604b.png?v=1775197131",
    ),
    (
        "Havintha Natural Brahmi Powder",
        "Havintha", "Haircare",
        "Bacopa Monnieri",
        CDN + "101.png?v=1775199706",
    ),
    (
        "Havintha Natural Methidana Powder",
        "Havintha", "Haircare",
        "Trigonella Foenum-Graecum",
        CDN + "83_176c9184-2f99-4701-bee2-a460b098fd10.png?v=1775198237",
    ),
    (
        "Havintha Natural Hibiscus Powder",
        "Havintha", "Haircare",
        "Hibiscus Rosa-Sinensis",
        "https://havintha.com/cdn/shop/files/Hibiscuspowderfront_c5f4487c-8298-44ac-a07f-cb0093c2edb5.png?v=1750161080",
    ),
    (
        "Havintha Natural Jatamansi Powder",
        "Havintha", "Haircare",
        "Nardostachys Jatamansi",
        CDN + "56_ac0c4a1e-7e94-4161-82de-0df555d9426e.png?v=1775197979",
    ),
    (
        "Havintha Natural Ratanjot Powder",
        "Havintha", "Haircare",
        "Alkanna Tinctoria",
        CDN + "92.png?v=1775199082",
    ),
    (
        "Havintha Natural Curry Leaves Powder",
        "Havintha", "Haircare",
        "Murraya Koenigii",
        CDN + "Hair_Powder_Sub-images_6.png?v=1775201818",
    ),
    (
        "Havintha Natural Neem Leaf Powder",
        "Havintha", "Haircare",
        "Azadirachta Indica",
        CDN + "74_60274161-9344-4d7f-83cb-f7db2eff06fd.png?v=1775198149",
    ),
    (
        "Havintha Natural Tulsi Powder",
        "Havintha", "Haircare",
        "Ocimum Tenuiflorum",
        CDN + "110.png?v=1776244534",
    ),
    (
        "Havintha Natural Mulethi Powder",
        "Havintha", "Haircare",
        "Glycyrrhiza Glabra",
        CDN + "94_aaebd7c7-02d7-4b10-ae75-262d8ebc4cda.jpg?v=1776504973",
    ),
    (
        "Havintha Natural Kalonji Powder",
        "Havintha", "Haircare",
        "Nigella Sativa",
        CDN + "250.jpg?v=1775219201",
    ),
    (
        "Havintha Natural Rosemary Powder",
        "Havintha", "Haircare",
        "Rosmarinus Officinalis",
        CDN + "119.png?v=1775199871",
    ),
    # ── FACE PACKS & SKIN POWDERS ──
    (
        "Havintha Natural Face and Body Ubtan Powder",
        "Havintha", "Skincare",
        "Cicer Arietinum Flour, Solum Fullonum, Curcuma Amada, "
        "Santalum Album, Milk Powder, Lens Culinaris, Rosa Damascena, "
        "Aloe Barbadensis Extract, Glycyrrhiza Glabra, Oryza Sativa, "
        "Prunus Dulcis Oil",
        CDN + "Face_BOdy_wash_5.png?v=1779086438",
    ),
    (
        "Havintha Natural Orange Peel Powder",
        "Havintha", "Skincare",
        "Citrus Aurantium",
        CDN + "Website_front_page_14.png?v=1779366588",
    ),
    (
        "Havintha Natural Sandalwood Powder",
        "Havintha", "Skincare",
        "Santalum Album",
        CDN + "Website_front_page_15.png?v=1779704489",
    ),
    (
        "Havintha Natural Multani Mitti Powder",
        "Havintha", "Skincare",
        "Solum Fullonum",
        CDN + "47.jpg?v=1775215616",
    ),
    (
        "Havintha Natural Activated Charcoal Powder",
        "Havintha", "Skincare",
        "Activated Charcoal",
        CDN + "Website_front_page_18.png?v=1779790977",
    ),
    (
        "Havintha Natural Rose Petals Powder",
        "Havintha", "Skincare",
        "Rosa Damascena",
        CDN + "29.jpg?v=1775215189",
    ),
    (
        "Havintha Natural Amba Haldi Powder",
        "Havintha", "Skincare",
        "Curcuma Amada",
        CDN + "20_c4f4285d-0768-40aa-827f-a6de2443bb71.jpg?v=1776416995",
    ),
    (
        "Havintha Natural Masoor Dal Powder",
        "Havintha", "Skincare",
        "Lens Culinaris",
        CDN + "241.jpg?v=1775219488",
    ),
    (
        "Havintha Natural Lemon Peel Powder",
        "Havintha", "Skincare",
        "Citrus Limon",
        CDN + "2_ad7a6c95-3480-4930-bf17-8f6384d5fefa.jpg?v=1775214922",
    ),
    (
        "Havintha Natural Anar Peel Powder",
        "Havintha", "Skincare",
        "Punica Granatum",
        CDN + "184_987dfb0e-b650-41b5-a12d-3acab7d5cbe9.jpg?v=1776425584",
    ),
    (
        "Havintha Natural Beet Root Powder",
        "Havintha", "Skincare",
        "Beta Vulgaris",
        CDN + "67_d0e87972-ae0d-4c75-824b-ef4cc7d01ec4.jpg?v=1775215797",
    ),
    (
        "Havintha Natural Rice Powder Mask",
        "Havintha", "Skincare",
        "Oryza Sativa",
        CDN + "103.png?v=1774526692",
    ),
    (
        "Havintha Natural Aloevera Powder",
        "Havintha", "Skincare",
        "Aloe Barbadensis",
        CDN + "130.jpg?v=1775217297",
    ),
    # ── ESSENTIAL OILS ──
    (
        "Havintha Natural Rosemary Essential Oil",
        "Havintha", "Essential Oil",
        "Rosmarinus Officinalis Essential Oil",
        CDN + "9_e2ea45be-fb64-4a00-8179-a6c4ca8cb5a6.png?v=1775300965",
    ),
    (
        "Havintha Tea Tree Essential Oil",
        "Havintha", "Essential Oil",
        "Melaleuca Alternifolia Essential Oil",
        CDN + "9_b21fc3b4-e916-4ded-baa1-484a6c0f84a4.png?v=1775298404",
    ),
    (
        "Havintha Lavender Essential Oil",
        "Havintha", "Essential Oil",
        "Lavandula Angustifolia Essential Oil",
        CDN + "49_c9b20e14-1ab3-4495-a33f-ede8afc543b0.png?v=1775298685",
    ),
]

# ── insertion ─────────────────────────────────────────────────────────────────

def already_exists(name: str) -> bool:
    res = sb.table('ai_extracted_products').select('id').ilike('name', name).limit(1).execute()
    return bool(res.data)

def insert_product(name, brand, category, ingredients_raw, image_url):
    print(f"\n[{name}]")
    if already_exists(name):
        print("  SKIP — already in database")
        return False

    ing_names  = parse_ingredients(ingredients_raw)
    classified = [classify_one(n) for n in ing_names]
    grade      = compute_grade(classified)
    q = sum(1 for i in classified if i['classification'] == 'commonly_questioned')
    w = sum(1 for i in classified if i['classification'] == 'worth_knowing')
    total = len(classified)
    print(f"  Grade={grade}  questioned={q}  worth={w}  total={total}")

    fssai_note = FSSAI_MAP.get(category, "Regulated under Cosmetics Rules 2020.")
    verdict = (f"Contains {q} restricted/flagged ingredient(s)." if q else
               f"Contains {w} ingredient(s) worth monitoring." if w else
               "All ingredients are generally safe.")
    recommendation = ("Avoid or use sparingly — contains commonly questioned ingredients." if q else
                      "Use with awareness — some additives worth monitoring." if w else
                      "Safe to use — no concerning ingredients detected.")
    awareness_score = max(0, 100 - (q * 25) - (w * 8))

    record = {
        "name":            name,
        "brand":           brand,
        "category":        category,
        "grade":           grade,
        "ingredients_raw": ingredients_raw,
        "ingredients":     classified,
        "image_url":       image_url,
        "static_key":      make_static_key(name),
        "summary":         make_summary(name, brand, grade, q, w, total),
        "fssai_note":      fssai_note,
        "verdict":         verdict,
        "recommendation":  recommendation,
        "awareness_score": awareness_score,
        "status":          "approved",
    }
    try:
        res = sb.table('ai_extracted_products').insert(record).execute()
        print(f"  INSERTED (id: {res.data[0]['id'][:8]}...)")
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return None

def main():
    print(f"Inserting {len(PRODUCTS)} Havintha products...\n")
    added = skipped = failed = 0
    for p in PRODUCTS:
        r = insert_product(*p)
        if r is True:    added += 1
        elif r is False: skipped += 1
        else:            failed += 1
    print(f"\n{'='*60}")
    print(f"Done.  Added: {added}  |  Skipped: {skipped}  |  Failed: {failed}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
