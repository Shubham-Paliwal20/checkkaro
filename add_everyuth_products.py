"""
Add 10 Everyuth Naturals products to ai_extracted_products.
Full INCI sourced from INCIDecoder for 4 products; partial/key-only for remaining 6.
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

BASE = "https://www.everyuth.com/uploads/product/"

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
        return f"{name} by {brand} scores Grade C. Contains {w} worth-knowing ingredients (>30% of total)."
    else:
        return f"{name} by {brand} scores Grade D. Contains {q} commonly questioned ingredient(s) — parabens and/or MIT detected."

FSSAI_MAP = {
    "Face Wash": "Regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
    "Face Scrub": "Regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
    "Peel-Off Mask": "Regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
    "Face Pack": "Regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
    "Gel": "Regulated under Drugs and Cosmetics Act 1940 and Cosmetics Rules 2020.",
}

# ── catalogue ─────────────────────────────────────────────────────────────────

PRODUCTS = [
    # ── FACE WASH (Full INCI) ──
    (
        "Everyuth Naturals Tulsi Turmeric Advanced Face Wash",
        "Everyuth Naturals", "Face Wash",
        "Purified Water, Sodium Lauryl Ether Sulphate, Cocamidopropyl Betaine, "
        "Sodium Lactate, Niacinamide, Aloe Barbadensis Leaf Juice, "
        "Olea Europaea Fruit Oil, Glyceryl Laurate, Sodium Polyacrylate, "
        "Dimethicone, Cyclopentasiloxane, Trideceth-6, PEG/PPG-18/18 Dimethicone, "
        "Zinc Monomethionine, Zingiber Officinale Extract, "
        "Ammonium Acryloyldimethyltaurate/VP Copolymer, Mandelic Acid, "
        "Saccharum Officinarum Extract, Coleus Forskohlii Oil, "
        "Phenoxyethanol, Caprylyl Glycol, Decylene Glycol, "
        "Octadecyl Di-T-Butyl-4-Hydroxyhydrocinnamate, Propylene Glycol, "
        "Poly Glutamic Acid, Decyl Glucoside, Triethanolamine, "
        "Acrylates/C10-30 Alkyl Acrylate Crosspolymer, Salicylic Acid, "
        "Fragrance, PEG-40 Hydrogenated Castor Oil, Methylparaben, "
        "PEG 6000 Distearate, Disodium EDTA, Methylisothiazolinone, "
        "Ocimum Sanctum Extract, Curcuma Longa Extract, Emblica Officinalis Extract, "
        "Carica Papaya Extract, Bacopa Monnieri Extract, Sodium Benzoate, "
        "Methylpropanediol, 4-Terpineol, Salix Alba Bark Extract, "
        "Luffa Cylindrica Fruit Powder, Glycerin, Laminaria Digitata Extract, "
        "Tocopheryl Acetate, Lecithin, Glyceryl Linolenate, Retinyl Palmitate, "
        "Sodium Ascorbyl Phosphate, Xanthan Gum, Diatomaceous Earth, "
        "Glyceryl Caprylate, Phenylpropanol",
        BASE + "tulsi-turmeric-face-wash.png",
    ),
    (
        "Everyuth Naturals Lemon Cherry Face Wash",
        "Everyuth Naturals", "Face Wash",
        "Water, Sodium Lauryl Ether Sulphate, Cocamidopropyl Betaine, "
        "Sorbitol, Decyl Glucoside, Triethanolamine, Glycerine, Sodium Lactate, "
        "Acrylates/C10-30 Alkyl Acrylate Crosspolymer, Fragrance, "
        "Gamma-Polyglutamic Acid, Methyl Paraben, PEG 6000 Distearate, "
        "Sodium Chloride, Apple Extract, Disodium EDTA, Propyl Paraben, "
        "Methylisothiazolinone, Sodium Ascorbyl Phosphate, Lecithin, Xanthan Gum, "
        "Phenoxyethanol, Caprylyl Glycol, Glyceryl Caprylate, "
        "Honey, Lemon Fruit Extract, Tartrazine",
        BASE + "lemon-cherry-face-wash.png",
    ),
    # ── FACE WASH (Key ingredients only) ──
    (
        "Everyuth Naturals Neem Face Wash",
        "Everyuth Naturals", "Face Wash",
        "Azadirachta Indica Leaf Extract, Laminaria Digitata Extract, "
        "Tocopheryl Acetate, Sodium Ascorbyl Phosphate, Retinyl Palmitate, "
        "Aloe Barbadensis Leaf Extract, Glycerin",
        BASE + "neem-face-wash.png",
    ),
    # ── FACE WASH (Partial INCI) ──
    (
        "Everyuth Naturals Fruit Face Wash",
        "Everyuth Naturals", "Face Wash",
        "Sodium Lauryl Ether Sulphate, Cocamidopropyl Betaine, Sorbitol, "
        "Gamma Polyglutamic Acid, Decyl Glucoside, Sodium Lactate, Triethanolamine, "
        "Glycerine, Acrylates/C10-30 Alkyl Acrylate Crosspolymer, Fragrance, "
        "Isobutyl Paraben, Methyl Paraben, Ethyl Paraben, Propyl Paraben, Butyl Paraben, "
        "PEG 6000 Distearate, Sodium Chloride, Pyrus Malus (Apple) Fruit Extract, "
        "Disodium EDTA, Methylisothiazolinone, Laminaria Digitata Extract, "
        "Tocopheryl Acetate, Lecithin, Glyceryl Linoleate, Ascorbyl Palmitate, "
        "Sodium Ascorbyl Phosphate, Xanthan Gum, Diatomaceous Earth, "
        "Phenoxyethanol, Ethyl Paraben",
        BASE + "fruit-face-wash.png",
    ),
    # ── FACE SCRUB (Full INCI) ──
    (
        "Everyuth Naturals Exfoliating Walnut Scrub",
        "Everyuth Naturals", "Face Scrub",
        "Water, Glyceryl Monostearate, Liquid Paraffin, Walnut Shell Powder, "
        "Cetostearyl Alcohol, Cetyl Alcohol, Isopropyl Alcohol, Sorbitol, Starch, "
        "Apricot Kernel Oil, Sodium Lauryl Sulfate, Titanium Dioxide, Fragrance, "
        "Triethanolamine, Triclosan, Carbomer, Methyl Paraben, Glycerin, "
        "Laminaria Digitata Extract, Tocopheryl Acetate, Lecithin, Glyceryl Linoleate, "
        "Glyceryl Linolenate, Retinyl Palmitate, Sodium Ascorbyl Phosphate, "
        "Xanthan Gum, Diatomaceous Earth, Phenoxyethanol, Disodium EDTA, "
        "Butyl Paraben, Ethyl Paraben, Isobutyl Paraben, Propyl Paraben",
        BASE + "walnut-scrub-1.png",
    ),
    # ── FACE SCRUB (Key only) ──
    (
        "Everyuth Naturals Walnut Apricot Scrub",
        "Everyuth Naturals", "Face Scrub",
        "Juglans Regia Shell Powder, Prunus Armeniaca Kernel Oil, "
        "Tocopheryl Acetate, Laminaria Digitata Extract, Glycerin",
        BASE + "walnut-apricot-scrub.png",
    ),
    # ── PEEL-OFF (Full INCI) ──
    (
        "Everyuth Naturals Golden Glow Peel Off Mask",
        "Everyuth Naturals", "Peel-Off Mask",
        "Water, Alcohol, PEG 1500, Propylene Glycol, Orange Peel Extract, "
        "Methyl Paraben, Fragrance, Gellan Gum, Calcium Aluminum Borosilicate, "
        "Silica, Tin Oxide, Acetyl Heptapeptide-9, Colloidal Gold, "
        "Phenoxyethanol, Lactic Acid",
        BASE + "golden-glow-peel-off-mask-1-1.png",
    ),
    # ── PEEL-OFF (Key only) ──
    (
        "Everyuth Naturals Orange Peel Off Mask",
        "Everyuth Naturals", "Peel-Off Mask",
        "Citrus Aurantium Dulcis Peel Extract, Tocopheryl Acetate, "
        "Sodium Ascorbyl Phosphate, Retinyl Palmitate, Gellan Gum",
        BASE + "orange-peel-off-mask-1.png",
    ),
    # ── FACE PACK (Key only) ──
    (
        "Everyuth Naturals Cucumber Aloe Vera Face Pack",
        "Everyuth Naturals", "Face Pack",
        "Cucumis Sativus Fruit Extract, Aloe Barbadensis Leaf Extract, "
        "Sodium Ascorbyl Phosphate, Tocopheryl Acetate, Kaolin, Glycerin",
        BASE + "cucumber-face-pack-1.png",
    ),
    # ── GEL (Key only) ──
    (
        "Everyuth Naturals Nourishing Aloe Vera Cucumber Gel",
        "Everyuth Naturals", "Gel",
        "Aloe Barbadensis Leaf Juice, Cucumis Sativus Fruit Extract, "
        "Sodium Ascorbyl Phosphate, Tocopheryl Acetate, Carbomer, Glycerin",
        BASE + "nourishing-aloevera-and-cucumber-gel-1-2.png",
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
    verdict = (f"Contains {q} restricted/flagged ingredient(s) including parabens and/or MIT." if q else
               f"Contains {w} ingredient(s) worth monitoring." if w else
               "All analysed ingredients are generally recognised as safe.")
    recommendation = ("Avoid or use sparingly — contains commonly questioned ingredients (parabens/MIT)." if q else
                      "Use with awareness — contains synthetic ingredients worth knowing about." if w else
                      "Safe to use based on available ingredient information.")
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
    print(f"Inserting {len(PRODUCTS)} Everyuth Naturals products...\n")
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
