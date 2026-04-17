"""
Load additional Indian products into Supabase database
Run this script to add more products to the database
"""

import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env file")
    exit(1)

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Additional products to add
additional_products = [
    # HONEY & SPREADS
    {
        'name': 'Dabur Honey',
        'brand': 'Dabur',
        'category': 'Food',
        'ingredients_text': 'Pure Honey',
        'ingredients_list': ['Pure Honey'],
        'data_source': 'manual',
        'is_verified': True,
        'search_count': 80
    },
    {
        'name': 'Kissan Mixed Fruit Jam',
        'brand': 'Kissan',
        'category': 'Food',
        'ingredients_text': 'Sugar, Mixed Fruit Pulp (Apple, Banana, Papaya, Pineapple, Mango, Grape), Acidity Regulator (E330), Gelling Agent (E440), Preservative (E211)',
        'ingredients_list': ['Sugar', 'Apple Pulp', 'Banana Pulp', 'Papaya Pulp', 'Pineapple Pulp', 'Mango Pulp', 'Grape Pulp', 'Citric Acid', 'Pectin', 'Sodium Benzoate'],
        'data_source': 'manual',
        'is_verified': True,
        'search_count': 80
    },
    {
        'name': 'Nutella Hazelnut Spread',
        'brand': 'Nutella',
        'category': 'Food',
        'ingredients_text': 'Sugar, Palm Oil, Hazelnuts (13%), Skimmed Milk Powder (8.7%), Fat-Reduced Cocoa (7.4%), Emulsifier (Soy Lecithin), Vanillin',
        'ingredients_list': ['Sugar', 'Palm Oil', 'Hazelnuts', 'Skimmed Milk Powder', 'Cocoa Powder', 'Soy Lecithin', 'Vanillin'],
        'data_source': 'manual',
        'is_verified': True,
        'search_count': 70
    },
    # COOKING OILS
    {
        'name': 'Fortune Sunflower Oil',
        'brand': 'Fortune',
        'category': 'Cooking Oil',
        'ingredients_text': 'Refined Sunflower Oil',
        'ingredients_list': ['Refined Sunflower Oil'],
        'data_source': 'manual',
        'is_verified': True,
        'search_count': 80
    },
    {
        'name': 'Saffola Gold Oil',
        'brand': 'Saffola',
        'category': 'Cooking Oil',
        'ingredients_text': 'Refined Rice Bran Oil, Refined Sunflower Oil',
        'ingredients_list': ['Refined Rice Bran Oil', 'Refined Sunflower Oil'],
        'data_source': 'manual',
        'is_verified': True,
        'search_count': 75
    },
    # SPICES
    {
        'name': 'MDH Chana Masala',
        'brand': 'MDH',
        'category': 'Spices',
        'ingredients_text': 'Coriander, Cumin, Dry Mango, Black Pepper, Red Chilli, Iodised Salt, Black Salt, Dry Ginger, Pomegranate Seeds, Mint Leaves, Carom Seeds, Cloves, Nutmeg, Mace, Green Cardamom, Bay Leaves, Asafoetida',
        'ingredients_list': ['Coriander', 'Cumin', 'Dry Mango', 'Black Pepper', 'Red Chilli', 'Iodised Salt', 'Black Salt', 'Dry Ginger', 'Pomegranate Seeds', 'Mint Leaves', 'Carom Seeds', 'Cloves', 'Nutmeg', 'Mace', 'Green Cardamom', 'Bay Leaves', 'Asafoetida'],
        'data_source': 'manual',
        'is_verified': True,
        'search_count': 60
    },
    {
        'name': 'Everest Garam Masala',
        'brand': 'Everest',
        'category': 'Spices',
        'ingredients_text': 'Coriander, Cumin, Black Pepper, Cassia, Cloves, Cardamom, Mace, Nutmeg, Bay Leaves',
        'ingredients_list': ['Coriander', 'Cumin', 'Black Pepper', 'Cassia', 'Cloves', 'Cardamom', 'Mace', 'Nutmeg', 'Bay Leaves'],
        'data_source': 'manual',
        'is_verified': True,
        'search_count': 55
    },
    # READY TO EAT
    {
        'name': 'MTR Ready to Eat Paneer Butter Masala',
        'brand': 'MTR',
        'category': 'Ready to Eat',
        'ingredients_text': 'Water, Paneer (Milk) (15%), Tomato Paste, Onion, Butter (3%), Cashew Paste, Cream (Milk), Sugar, Refined Sunflower Oil, Ginger, Garlic, Salt, Spices, Kasuri Methi, Acidity Regulator (E330)',
        'ingredients_list': ['Water', 'Paneer', 'Tomato Paste', 'Onion', 'Butter', 'Cashew Paste', 'Cream', 'Sugar', 'Refined Sunflower Oil', 'Ginger', 'Garlic', 'Salt', 'Spices', 'Kasuri Methi', 'Citric Acid'],
        'data_source': 'manual',
        'is_verified': True,
        'search_count': 60
    },
    {
        'name': 'ITC Aashirvaad Atta',
        'brand': 'ITC',
        'category': 'Food',
        'ingredients_text': 'Whole Wheat Flour',
        'ingredients_list': ['Whole Wheat Flour'],
        'data_source': 'manual',
        'is_verified': True,
        'search_count': 90
    },
    # CONDIMENTS
    {
        'name': 'Maggi Tomato Ketchup',
        'brand': 'Maggi',
        'category': 'Condiments',
        'ingredients_text': 'Tomato Paste, Sugar, Water, Iodised Salt, Acidity Regulator (E260), Spices, Thickener (E1442), Preservative (E211)',
        'ingredients_list': ['Tomato Paste', 'Sugar', 'Water', 'Iodised Salt', 'Acetic Acid', 'Spices', 'Modified Starch', 'Sodium Benzoate'],
        'data_source': 'manual',
        'is_verified': True,
        'search_count': 70
    },
    {
        'name': 'Kissan Fresh Tomato Ketchup',
        'brand': 'Kissan',
        'category': 'Condiments',
        'ingredients_text': 'Tomatoes, Sugar, Salt, Spices, Acidity Regulator (E260), Preservative (E211)',
        'ingredients_list': ['Tomatoes', 'Sugar', 'Salt', 'Spices', 'Acetic Acid', 'Sodium Benzoate'],
        'data_source': 'manual',
        'is_verified': True,
        'search_count': 75
    },
    # BREAKFAST CEREALS
    {
        'name': 'Kelloggs Corn Flakes',
        'brand': 'Kelloggs',
        'category': 'Breakfast Cereal',
        'ingredients_text': 'Milled Corn, Sugar, Malt Flavouring, Iodised Salt, Vitamins, Minerals',
        'ingredients_list': ['Milled Corn', 'Sugar', 'Malt Flavouring', 'Iodised Salt', 'Vitamins', 'Minerals'],
        'data_source': 'manual',
        'is_verified': True,
        'search_count': 65
    },
    {
        'name': 'Kelloggs Chocos',
        'brand': 'Kelloggs',
        'category': 'Breakfast Cereal',
        'ingredients_text': 'Wheat Flour, Sugar, Cocoa Solids, Edible Vegetable Oil, Iodised Salt, Minerals, Vitamins, Emulsifier (E322)',
        'ingredients_list': ['Wheat Flour', 'Sugar', 'Cocoa Solids', 'Edible Vegetable Oil', 'Iodised Salt', 'Minerals', 'Vitamins', 'Soy Lecithin'],
        'data_source': 'manual',
        'is_verified': True,
        'search_count': 60
    },
    # JUICES
    {
        'name': 'Real Fruit Juice Mango',
        'brand': 'Real',
        'category': 'Beverages',
        'ingredients_text': 'Water, Mango Pulp (20%), Sugar, Acidity Regulator (E330), Antioxidant (E300), Stabilizer (E440), Natural Flavour',
        'ingredients_list': ['Water', 'Mango Pulp', 'Sugar', 'Citric Acid', 'Ascorbic Acid', 'Pectin', 'Natural Flavour'],
        'data_source': 'manual',
        'is_verified': True,
        'search_count': 60
    },
    {
        'name': 'Tropicana 100% Orange Juice',
        'brand': 'Tropicana',
        'category': 'Beverages',
        'ingredients_text': 'Orange Juice (100%)',
        'ingredients_list': ['Orange Juice'],
        'data_source': 'manual',
        'is_verified': True,
        'search_count': 55
    },
    {
        'name': 'Frooti Mango Drink',
        'brand': 'Frooti',
        'category': 'Beverages',
        'ingredients_text': 'Water, Mango Pulp (10%), Sugar, Acidity Regulator (E330), Antioxidant (E300), Stabilizer (E440), Natural Flavour, Colour (E160a)',
        'ingredients_list': ['Water', 'Mango Pulp', 'Sugar', 'Citric Acid', 'Ascorbic Acid', 'Pectin', 'Natural Flavour', 'Beta Carotene'],
        'data_source': 'manual',
        'is_verified': True,
        'search_count': 50
    },
    # ICE CREAMS
    {
        'name': 'Amul Vanilla Ice Cream',
        'brand': 'Amul',
        'category': 'Dessert',
        'ingredients_text': 'Milk, Sugar, Milk Solids, Edible Vegetable Oil, Emulsifier (E471), Stabilizers (E412, E410, E407), Natural Vanilla Flavour',
        'ingredients_list': ['Milk', 'Sugar', 'Milk Solids', 'Edible Vegetable Oil', 'Mono and Diglycerides', 'Guar Gum', 'Locust Bean Gum', 'Carrageenan', 'Natural Vanilla Flavour'],
        'data_source': 'manual',
        'is_verified': True,
        'search_count': 45
    },
    # TEA & COFFEE
    {
        'name': 'Tata Tea Gold',
        'brand': 'Tata',
        'category': 'Beverages',
        'ingredients_text': 'Black Tea',
        'ingredients_list': ['Black Tea'],
        'data_source': 'manual',
        'is_verified': True,
        'search_count': 85
    },
    {
        'name': 'Nescafe Classic Coffee',
        'brand': 'Nescafe',
        'category': 'Beverages',
        'ingredients_text': 'Coffee',
        'ingredients_list': ['Coffee'],
        'data_source': 'manual',
        'is_verified': True,
        'search_count': 80
    },
    # BAKERY
    {
        'name': 'Britannia Bread',
        'brand': 'Britannia',
        'category': 'Bakery',
        'ingredients_text': 'Refined Wheat Flour (Maida), Water, Sugar, Edible Vegetable Oil (Palmolein), Yeast, Iodised Salt, Gluten, Emulsifiers (E471, E472e), Flour Treatment Agent (E300)',
        'ingredients_list': ['Refined Wheat Flour', 'Water', 'Sugar', 'Palmolein Oil', 'Yeast', 'Iodised Salt', 'Gluten', 'Mono and Diglycerides', 'DATEM', 'Ascorbic Acid'],
        'data_source': 'manual',
        'is_verified': True,
        'search_count': 70
    },
    # DETERGENTS
    {
        'name': 'Surf Excel Matic Detergent',
        'brand': 'Surf Excel',
        'category': 'Household',
        'ingredients_text': 'Anionic Surfactants, Non-Ionic Surfactants, Soap, Enzymes, Optical Brightener, Perfume, Water',
        'ingredients_list': ['Anionic Surfactants', 'Non-Ionic Surfactants', 'Soap', 'Enzymes', 'Optical Brightener', 'Perfume', 'Water'],
        'data_source': 'manual',
        'is_verified': True,
        'search_count': 40
    },
]

def load_products():
    """Load additional products into Supabase"""
    print("🚀 Starting to load additional products...")
    print(f"📦 Total products to add: {len(additional_products)}")
    
    success_count = 0
    error_count = 0
    
    for product in additional_products:
        try:
            # Check if product already exists
            existing = supabase.table('products_catalog').select('id').eq('name', product['name']).execute()
            
            if existing.data:
                print(f"⏭️  Skipping '{product['name']}' - already exists")
                continue
            
            # Insert product
            result = supabase.table('products_catalog').insert(product).execute()
            
            if result.data:
                success_count += 1
                print(f"✅ Added: {product['name']} ({product['brand']})")
            else:
                error_count += 1
                print(f"❌ Failed to add: {product['name']}")
                
        except Exception as e:
            error_count += 1
            print(f"❌ Error adding '{product['name']}': {str(e)}")
    
    print("\n" + "="*60)
    print(f"✅ Successfully added: {success_count} products")
    print(f"❌ Errors: {error_count}")
    print(f"📊 Total in batch: {len(additional_products)}")
    print("="*60)

if __name__ == "__main__":
    load_products()
