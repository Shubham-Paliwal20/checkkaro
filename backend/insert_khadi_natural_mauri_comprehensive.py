"""
Insert Khadi Natural & Khadi Mauri Comprehensive Registry
100+ herbal personal care, skincare, and bath products
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['mineral oil', 'cyclomethicone', 'synthetic colour']
_WORTH = ['neem', 'tulsi', 'brahmi', 'bhringraj', 'shikakai', 'reetha', 'amla', 'henna', 'sandalwood', 'turmeric', 'aloe vera', 'honey', 'vitamin c', 'hyaluronic acid', 'tea tree', 'rose', 'green tea', 'saffron', 'basil', 'rosemary', 'charcoal']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'mineral oil' in n: return 'Mineral oil; occlusive ingredient'
        if 'cyclomethicone' in n: return 'Silicone; texture and shine'
    if cls == 'worth_knowing':
        if 'neem' in n: return 'Neem; antibacterial traditional remedy'
        if 'tulsi' in n: return 'Tulsi; immune-boosting herb'
        if 'brahmi' in n: return 'Brahmi; cooling and calming'
        if 'bhringraj' in n: return 'Bhringraj; traditional hair darkener'
        if 'shikakai' in n: return 'Shikakai; natural saponin cleanser'
        if 'reetha' in n: return 'Reetha (soapnuts); natural cleanser'
        if 'amla' in n: return 'Amla; vitamin C and antioxidant-rich'
        if 'henna' in n: return 'Henna; conditioning and coloring'
        if 'sandalwood' in n: return 'Sandalwood; cooling and aromatic'
        if 'turmeric' in n: return 'Turmeric; anti-inflammatory spice'
        if 'aloe' in n: return 'Aloe vera; soothing botanical'
        if 'honey' in n: return 'Honey; humectant and antibacterial'
        if 'vitamin' in n or 'ascorbic' in n: return 'Vitamin C; antioxidant and brightening'
        if 'hyaluronic' in n: return 'Hyaluronic acid; deep hydration'
        if 'tea tree' in n: return 'Tea tree; antimicrobial essential oil'
        if 'green tea' in n: return 'Green tea; antioxidant rich'
        if 'saffron' in n: return 'Saffron; luxury botanical extract'
        if 'charcoal' in n: return 'Activated charcoal; detoxifying'
    return 'Traditional herbal ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Contains synthetic or mineral ingredients'
    if cls == 'worth_knowing': return 'Natural and traditional herbal ingredients'
    return 'Herbal personal care ingredient'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    return [i.strip() for i in raw.split(',') if len(i.strip()) > 2]

def _build_obj(name: str) -> dict:
    cls = _classify(name)
    return {'name': name, 'aliases': '', 'classification': cls, 'one_line_note': _note(name, cls), 'regulatory_note': _reg_note(cls)}

def _score(ingredient_objs: list) -> int:
    score = 100
    for ing in ingredient_objs:
        if ing['classification'] == 'commonly_questioned': score -= 3
        elif ing['classification'] == 'worth_knowing': score -= 0
    return max(0, min(100, score))

PRODUCTS = [
    # KHADI NATURAL - HAIR CARE
    {"name": "Amla & Bhringraj Hair Cleanser", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Purified Water, Amla Extract, Bhringraj Extract, Reetha Extract, Aloe Vera Extract, Shikakai Extract, Neem Extract, Brahmi Extract, Coconut Oil."},
    {"name": "Neem & Aloe Vera Herbal Shampoo", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Purified Water, Neem Extract, Aloe Vera Extract, Reetha Extract, Shikakai Extract, Basil Extract, Rosemary Extract."},
    {"name": "Henna & Tulsi Conditioning Shampoo", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Purified Water, Henna Extract, Tulsi Extract, Reetha, Shikakai, Bhringraj, Brahmi, Aloe Vera."},
    {"name": "Rose & Honey Herbal Shampoo", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Purified Water, Rose Extract, Honey, Reetha, Shikakai, Aloe Vera, Green Tea Extract."},
    {"name": "Shikakai & Honey Hair Conditioner", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Purified Water, Shikakai Extract, Honey, Aloe Vera, Almond Oil, Wheatgerm Oil, Jojoba Oil."},
    {"name": "Saffron, Tulsi & Reetha Shampoo", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Purified Water, Saffron, Tulsi, Reetha, Lodhra, Aloe Vera, Shikakai Extract."},
    {"name": "Green Apple Shampoo + Conditioner", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Purified Water, Green Apple Extract, Aloe Vera, Reetha, Shikakai, Honey, Basil Extract."},
    {"name": "Anti-Dandruff Herbal Shampoo", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Purified Water, Neem, Tea Tree Oil, Basil, Lemon Oil, Aloe Vera, Shikakai, Reetha Extract."},
    {"name": "Onion Hair Oil", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Onion Seed Oil, Sunflower Oil, Coconut Oil, Almond Oil, Amla Oil, Bhringraj Oil, Brahmi Oil, Vitamin E."},
    {"name": "18 Herbs Herbal Hair Oil", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Sesame Oil, Coconut Oil, Amla, Brahmi, Bhringraj, Jatamansi, Neem, Tulsi, Rose, Henna, Shikakai."},
    {"name": "Rosemary & Henna Hair Oil", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Rosemary Oil, Henna Extract, Sesame Oil, Coconut Oil, Sunflower Oil, Vitamin E."},
    {"name": "Brahmi Hair Oil", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Brahmi Extract, Sesame Oil, Coconut Oil, Amla Extract, Bhringraj Extract, Licorice."},
    {"name": "Jatamansi Hair Oil", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Jatamansi Extract, Sesame Oil, Coconut Oil, Wheatgerm Oil, Almond Oil."},
    {"name": "Aloe Vera Hair Cleanser", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Purified Water, Aloe Vera Extract, Reetha, Shikakai, Honey, Neem Extract."},
    {"name": "Walnut & Apricot Hair Scrub", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Walnut Shell, Apricot Kernel Oil, Aloe Vera, Sesame Oil, Glycerin."},
    {"name": "Hibiscus & Aloe Vera Shampoo", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Hibiscus Extract, Aloe Vera, Reetha, Shikakai, Purified Water."},
    {"name": "Tea Tree & Neem Hair Oil", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Tea Tree Oil, Neem Oil, Sesame Oil, Coconut Oil, Vitamin E."},
    {"name": "Sandalwood Hair Cleanser", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Sandalwood Oil, Purified Water, Reetha, Shikakai, Aloe Vera."},
    {"name": "Almond & Saffron Conditioner", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Almond Oil, Saffron Extract, Aloe Vera, Purified Water, Shea Butter."},
    {"name": "Herbal Mehandi (Henna) Powder", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Henna Leaves Powder, Neem Powder, Amla Powder, Shikakai Powder, Brahmi Powder."},
    {"name": "Argan Oil Hair Cleanser", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Argan Oil, Reetha, Shikakai, Purified Water, Coconut Oil Extract, Vitamin E."},
    {"name": "Ginger & Lemon Hair Cleanser", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Ginger Oil, Lemon Oil, Aloe Vera, Reetha, Shikakai, Purified Water."},
    {"name": "Orange & Lemongrass Hair Cleanser", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Orange Oil, Lemongrass Oil, Reetha, Aloe Vera, Purified Water."},
    {"name": "Honey & Vanilla Hair Cleanser", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Honey, Vanilla Extract, Reetha, Shikakai, Purified Water."},
    {"name": "Soya Protein Hair Cleanser", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Soya Protein Extract, Reetha, Shikakai, Purified Water, Wheatgerm Oil."},
    # KHADI MAURI - HAIR CARE
    {"name": "Herbals Amla Shampoo", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Amla Extract, Reetha, Shikakai, Neem, Basil, Purified Water, Base Q.S."},
    {"name": "Anti-Dandruff Shampoo (Khadi Mauri)", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Tea Tree Oil, Neem Extract, Lemon Oil, Basil, Purified Water, Base Q.S."},
    {"name": "Herbal Sat Reetha Shampoo", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Reetha Extract, Shikakai, Amla, Basil, Purified Water, Base Q.S."},
    {"name": "Herbal Honey Shampoo", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Honey, Almond Oil, Shikakai, Reetha, Purified Water."},
    {"name": "Herbal Saffron Shampoo", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Saffron Extract, Aloe Vera, Shikakai, Purified Water."},
    {"name": "Herbal Neem Shampoo", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Neem Oil, Basil, Tulsi, Reetha, Purified Water."},
    {"name": "Conditioning Cream (Khadi Mauri)", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Aloe Vera, Almond Oil, Wheatgerm Oil, Purified Water, Emulsifying Wax."},
    {"name": "Herbal Hair Serum", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Argan Oil, Jojoba Oil, Vitamin E, Cyclomethicone."},
    {"name": "Vitalizing Hair Oil", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Sesame Oil, Coconut Oil, Amla, Brahmi, Bhringraj, Jatamansi."},
    {"name": "Amla Bhringraj Oil", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Amla Extract, Bhringraj, Sesame Oil, Coconut Oil."},
    {"name": "Anti-Graying Hair Oil", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Henna Oil, Sesame Oil, Coconut Oil, Vitamin E."},
    {"name": "Tea Tree Hair Oil", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Tea Tree Essential Oil, Sesame Oil, Mineral Oil."},
    {"name": "Hibiscus Shampoo", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Hibiscus Extract, Reetha, Shikakai, Aloe Vera, Purified Water."},
    {"name": "Fruit Shampoo", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Apple Extract, Papaya Extract, Lemon, Reetha, Purified Water."},
    {"name": "Herbal Aloevera Shampoo", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Aloe Vera Extract, Reetha, Shikakai, Purified Water."},
    # KHADI NATURAL - SKINCARE
    {"name": "Rose & Papaya Face Scrub", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Rose Extract, Papaya Extract, Walnut Shell, Wheatgerm Oil, Aloe Vera, Honey."},
    {"name": "Sandle & Rose Face Pack", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Sandalwood Powder, Rose Petal Powder, Fuller's Earth (Multani Mitti), Calamine Powder."},
    {"name": "Neem & Tulsi Face Wash", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Purified Water, Neem Extract, Tulsi Extract, Aloe Vera, Tea Tree Oil, Glycerin."},
    {"name": "Saffron & Papaya Anti-Wrinkle Cream", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Saffron Extract, Papaya Extract, Shea Butter, Kokum Butter, Wheatgerm Oil, Almond Oil."},
    {"name": "Aloe Vera Gel (Pure)", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Aloe Vera Extract, Purified Water, Glycerin, Vitamin E, Tea Tree Oil."},
    {"name": "Cucumber & Aloe Vera Face Freshness", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Cucumber Extract, Aloe Vera, Rose Water, Purified Water, Neem Extract."},
    {"name": "Gold Face Pack", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Gold Bhasma, Sandalwood Oil, Honey, Aloe Vera, Fuller's Earth."},
    {"name": "Fruit Face Pack", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Apple Extract, Papaya Extract, Orange Extract, Strawberry Extract, Fuller's Earth."},
    {"name": "Anti-Acne Face Pack", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Neem Powder, Basil Powder, Turmeric Powder, Fuller's Earth, Calamine."},
    {"name": "Lavender & Ylang Ylang Body Wash", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Lavender Oil, Ylang Ylang Oil, Aloe Vera, Glycerin, Purified Water."},
    {"name": "Sandalwood & Kesar Body Wash", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Sandalwood Oil, Saffron Extract, Aloe Vera, Honey, Purified Water."},
    {"name": "Rose Water (Herbal Toner)", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Steam Distilled Rose Water, Purified Water."},
    {"name": "Apricot & Walnut Cream Scrub", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Apricot Kernel Oil, Walnut Shell, Shea Butter, Aloe Vera, Glycerin."},
    {"name": "Fairness Face Pack", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Sandalwood, Turmeric, Licorice, Aloe Vera, Fuller's Earth."},
    {"name": "Night Cream with Green Tea", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Green Tea Extract, Shea Butter, Vitamin E, Jojoba Oil, Aloe Vera."},
    {"name": "Sunscreen Lotion SPF 30", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Aloe Vera, Ashwagandha, Sandalwood Oil, Cucumber, Sunflower Oil."},
    {"name": "Under Eye Gel", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Aloe Vera, Cucumber Extract, Almond Oil, Wheatgerm Oil, Green Tea."},
    {"name": "Lip Balm - Strawberry", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Shea Butter, Beeswax, Strawberry Extract, Almond Oil, Vitamin E."},
    {"name": "Lip Balm - Chocolate", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Cocoa Butter, Beeswax, Chocolate Flavor, Almond Oil, Shea Butter."},
    {"name": "Activated Charcoal Face Wash", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Activated Charcoal, Neem Extract, Aloe Vera, Purified Water, Menthol."},
    {"name": "Vitamin C Face Serum", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Vitamin C (L-Ascorbic Acid), Hyaluronic Acid, Aloe Vera Extract, Witch Hazel."},
    {"name": "Tea Tree & Basil Face Wash", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Tea Tree Oil, Basil Extract, Aloe Vera, Purified Water, Glycerin."},
    {"name": "Peppermint Face Wash", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Peppermint Oil, Spearmint Oil, Aloe Vera, Purified Water."},
    {"name": "Grape Seed & Aloe Vera Face Wash", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Grape Seed Extract, Aloe Vera, Purified Water, Honey."},
    {"name": "Sandalwood Face Scrub", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Sandalwood Oil, Walnut Shell, Wheatgerm Oil, Aloe Vera."},
    {"name": "Orange Peel Face Scrub", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Orange Peel Powder, Walnut Shell, Aloe Vera, Purified Water."},
    {"name": "Pearl Face Pack", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Pearl Bhasma, Sandalwood, Aloe Vera, Fuller's Earth."},
    {"name": "Chocolate Face Pack", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Cocoa Powder, Honey, Aloe Vera, Fuller's Earth."},
    {"name": "Neem & Tea Tree Face Pack", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Neem Extract, Tea Tree Oil, Basil, Fuller's Earth."},
    {"name": "Whitening Lip Balm", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Licorice Extract, Almond Oil, Shea Butter, Vitamin E."},
    # KHADI MAURI - SKINCARE
    {"name": "Anti-Acne Face Wash (Khadi Mauri)", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Neem Oil, Tea Tree Oil, Basil Extract, Purified Water."},
    {"name": "Saffron Face Wash", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Saffron Extract, Sandalwood Oil, Aloe Vera, Purified Water."},
    {"name": "Apricot Face Scrub", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Apricot Oil, Walnut Shell, Wheatgerm Oil, Aloe Vera."},
    {"name": "Ubtan Face Pack", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Turmeric, Sandalwood, Gram Flour, Saffron, Rose Water."},
    {"name": "Sunscreen SPF 40", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Aloe Vera, Ashwagandha, Titanium Dioxide, Zinc Oxide, Wheatgerm Oil."},
    {"name": "Fairness Cream", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Saffron, Licorice, Sandalwood, Aloe Vera, Base Q.S."},
    {"name": "Anti-Aging Cream", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Green Tea, Vitamin E, Shea Butter, Aloe Vera."},
    {"name": "Cleansing Milk", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Aloe Vera, Cucumber Extract, Lemon, Almond Oil."},
    {"name": "Rose Water Toner", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Distilled Rose Water, Glycerin, Purified Water."},
    {"name": "Charcoal Face Mask", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Activated Charcoal, Bentonite Clay, Aloe Vera, Tea Tree Oil."},
    {"name": "Vitamin E Moisturizer", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Vitamin E Oil, Wheatgerm Oil, Shea Butter, Aloe Vera."},
    {"name": "Papaya Face Wash", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Papaya Extract, Honey, Aloe Vera, Purified Water."},
    {"name": "Gold Cream", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Gold Dust, Aloe Vera, Saffron, Sandalwood Oil."},
    {"name": "Tea Tree Face Wash", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Tea Tree Oil, Basil, Aloe Vera, Purified Water."},
    {"name": "Cucumber Face Wash", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Cucumber Extract, Aloe Vera, Purified Water, Glycerin."},
    # KHADI NATURAL - SOAPS & BATH
    {"name": "Handmade Soap - Sandalwood", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Sandalwood Oil, Coconut Oil, Rice Bran Oil, Glycerin, Purified Water."},
    {"name": "Handmade Soap - Rose Water", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Rose Water, Rose Petals, Coconut Oil, Palm Oil, Glycerin."},
    {"name": "Handmade Soap - Neem Tulsi", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Neem Oil, Tulsi Oil, Basil Oil, Coconut Oil, Glycerin."},
    {"name": "Handmade Soap - Haldi Chandan", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Turmeric Extract, Sandalwood Oil, Coconut Oil, Glycerin, Purified Water."},
    {"name": "Handmade Soap - Charcoal", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Activated Charcoal, Aloe Vera Extract, Coconut Oil, Castor Oil."},
    {"name": "Handmade Soap - Jasmine", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Jasmine Oil, Mogra Extract, Coconut Oil, Glycerin."},
    {"name": "Handmade Soap - Lemon", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Lemon Oil, Wheatgerm Oil, Coconut Oil, Glycerin."},
    {"name": "Handmade Soap - Almond", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Almond Oil, Honey, Shea Butter, Coconut Oil."},
    {"name": "Body Lotion - Rose & Honey", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Rose Extract, Honey, Almond Oil, Wheatgerm Oil, Shea Butter."},
    {"name": "Body Lotion - Jasmine & Mogra", "brand": "Khadi Natural", "category": "Personal Care",
     "raw": "Jasmine Oil, Mogra Extract, Shea Butter, Aloe Vera, Kokum Butter."},
    # KHADI MAURI - BATH & BODY
    {"name": "Herbal Bath Oil", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Sesame Oil, Olive Oil, Lavender Oil, Rose Oil."},
    {"name": "Foot Crack Cream", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Shea Butter, Beeswax, Neem Oil, Turmeric, Mustard Oil."},
    {"name": "Herbal Moisturizer", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Aloe Vera, Peach Extract, Avocado Oil, Shea Butter."},
    {"name": "Hand Cream", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Milk Protein, Saffron Extract, Shea Butter, Almond Oil."},
    {"name": "Herbal Shaving Cream", "brand": "Khadi Mauri", "category": "Personal Care",
     "raw": "Sandalwood Oil, Menthol, Aloe Vera, Coconut Oil."},
]

def insert(p: dict) -> bool:
    name = p['name']
    raw = p['raw']
    parsed = _parse(raw)
    ingredient_objs = [_build_obj(i) for i in parsed]
    score = _score(ingredient_objs)
    try:
        existing = supabase.from_('ai_extracted_products').select('id').ilike('name', name).limit(1).execute()
        if existing.data:
            print(f"  skip (exists): {name}")
            return False
        supabase.from_('ai_extracted_products').insert({
            'name': name, 'brand': p['brand'], 'category': p['category'], 'image_url': None, 'images': [],
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Herbal personal care product. Score: {score}/100. Traditional formulation.",
            'fssai_note': 'Herbal personal care product with natural and traditional ingredients.',
            'verdict': 'Natural herbal formulation' if score >= 95 else 'Herbal product',
            'recommendation': 'Use as directed. Test for allergies with herbal ingredients.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Khadi Natural & Mauri comprehensive products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
