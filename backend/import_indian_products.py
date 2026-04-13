"""
Bulk import popular Indian products from Open Food Facts into database.
This script fetches real product data and stores it permanently.
"""
import asyncio
import httpx
from db.supabase_client import supabase
from services import groq_service
import time

# Popular Indian product brands and categories
POPULAR_BRANDS = [
    "Parle", "Britannia", "ITC", "Amul", "Nestle", "Cadbury", "Haldiram",
    "Bikano", "Lays", "Kurkure", "Maggi", "Bournvita", "Horlicks",
    "Patanjali", "Dabur", "Himalaya", "Dove", "Pears", "Lifebuoy",
    "Colgate", "Pepsodent", "Clinic Plus", "Pantene", "Head & Shoulders",
    "Fair & Lovely", "Lakme", "Marico", "Godrej", "Tata", "Mother Dairy"
]

POPULAR_CATEGORIES = [
    "biscuits", "snacks", "noodles", "chocolates", "beverages",
    "dairy", "personal-care", "soaps", "shampoos", "toothpaste"
]


async def fetch_products_by_brand(brand: str, limit: int = 50):
    """Fetch products from Open Food Facts by brand"""
    try:
        url = "https://in.openfoodfacts.org/cgi/search.pl"
        params = {
            "brands": brand,
            "json": 1,
            "page_size": limit,
            "fields": "product_name,brands,categories,image_url,ingredients_text,ingredients,code"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("products", [])
            return []
    except Exception as e:
        print(f"Error fetching {brand}: {e}")
        return []


async def fetch_products_by_category(category: str, limit: int = 50):
    """Fetch products from Open Food Facts by category"""
    try:
        url = f"https://in.openfoodfacts.org/category/{category}.json"
        params = {
            "page_size": limit,
            "fields": "product_name,brands,categories,image_url,ingredients_text,ingredients,code"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("products", [])
            return []
    except Exception as e:
        print(f"Error fetching category {category}: {e}")
        return []


def parse_ingredients_list(product: dict) -> list:
    """Extract ingredients list from Open Food Facts product data"""
    ingredients_list = []
    
    # Try structured ingredients first
    ingredients = product.get("ingredients", [])
    if ingredients:
        for ing in ingredients:
            ing_name = ing.get("text") or ing.get("id", "")
            if ing_name:
                ingredients_list.append(ing_name.strip())
    
    # Fallback to text parsing
    if not ingredients_list:
        ingredients_text = product.get("ingredients_text", "")
        if ingredients_text:
            # Simple parsing: split by comma
            ingredients_list = [i.strip() for i in ingredients_text.split(",") if i.strip()]
    
    return ingredients_list


async def classify_and_score_ingredients(product_name: str, ingredients_text: str):
    """Use Groq AI to classify ingredients and calculate score"""
    try:
        result = await groq_service.analyze_ingredients_list(product_name, ingredients_text)
        return result
    except Exception as e:
        print(f"Error classifying ingredients for {product_name}: {e}")
        return None


async def save_product_to_database(product_data: dict):
    """Save product to products_catalog table"""
    try:
        # Check if product already exists
        existing = supabase.table("products_catalog").select("id").eq("name", product_data["name"]).execute()
        
        if existing.data:
            print(f"  ⏭ Skipping {product_data['name']} (already exists)")
            return None
        
        # Insert product
        result = supabase.table("products_catalog").insert(product_data).execute()
        
        if result.data:
            print(f"  ✓ Saved {product_data['name']} ({len(product_data.get('ingredients_list', []))} ingredients)")
            return result.data[0]["id"]
        return None
    except Exception as e:
        print(f"  ✗ Error saving {product_data.get('name')}: {e}")
        return None


async def import_brand_products(brand: str):
    """Import all products for a specific brand"""
    print(f"\n{'='*60}")
    print(f"Importing products for brand: {brand}")
    print(f"{'='*60}")
    
    products = await fetch_products_by_brand(brand, limit=100)
    print(f"Found {len(products)} products for {brand}")
    
    imported_count = 0
    
    for product in products:
        product_name = product.get("product_name")
        if not product_name:
            continue
        
        # Parse ingredients
        ingredients_list = parse_ingredients_list(product)
        if len(ingredients_list) < 2:
            print(f"  ⏭ Skipping {product_name} (insufficient ingredients)")
            continue
        
        ingredients_text = ", ".join(ingredients_list)
        
        # Classify ingredients using AI
        print(f"  🔍 Analyzing {product_name}...")
        analysis = await classify_and_score_ingredients(product_name, ingredients_text)
        
        if not analysis or not analysis.get("ingredients"):
            print(f"  ⏭ Skipping {product_name} (analysis failed)")
            continue
        
        # Prepare product data
        product_data = {
            "name": product_name,
            "brand": product.get("brands", "").split(",")[0].strip() if product.get("brands") else brand,
            "category": product.get("categories", "").split(",")[0].strip() if product.get("categories") else None,
            "barcode": product.get("code"),
            "image_url": product.get("image_url"),
            "ingredients_text": ingredients_text,
            "ingredients_list": ingredients_list,
            "awareness_score": analysis.get("awareness_score", 50),
            "summary": analysis.get("summary"),
            "fssai_note": analysis.get("fssai_note"),
            "verdict": analysis.get("verdict"),
            "recommendation": analysis.get("recommendation"),
            "data_source": "openfoodfacts",
            "is_verified": True
        }
        
        # Save to database
        product_id = await save_product_to_database(product_data)
        
        if product_id:
            imported_count += 1
            
            # Save classified ingredients
            for idx, ing in enumerate(analysis.get("ingredients", [])):
                try:
                    supabase.table("product_ingredients_catalog").insert({
                        "product_id": product_id,
                        "ingredient_name": ing.get("name"),
                        "classification": ing.get("classification"),
                        "one_line_note": ing.get("one_line_note"),
                        "regulatory_note": ing.get("regulatory_note"),
                        "position": idx + 1
                    }).execute()
                except Exception as e:
                    print(f"    ✗ Error saving ingredient: {e}")
        
        # Rate limiting - don't overwhelm Groq API
        await asyncio.sleep(2)
    
    print(f"\n✓ Imported {imported_count} products for {brand}")
    return imported_count


async def main():
    """Main import function"""
    print("="*60)
    print("INDIAN PRODUCTS BULK IMPORT")
    print("="*60)
    print(f"Importing products from {len(POPULAR_BRANDS)} popular brands")
    print("This will take approximately 30-60 minutes...")
    print("="*60)
    
    total_imported = 0
    
    for brand in POPULAR_BRANDS:
        try:
            count = await import_brand_products(brand)
            total_imported += count
            
            # Pause between brands to avoid rate limits
            print(f"\n⏸ Pausing 10 seconds before next brand...")
            await asyncio.sleep(10)
            
        except Exception as e:
            print(f"✗ Error importing {brand}: {e}")
            continue
    
    print("\n" + "="*60)
    print(f"IMPORT COMPLETE!")
    print(f"Total products imported: {total_imported}")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
