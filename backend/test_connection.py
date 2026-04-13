import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

print("Testing Supabase connection...")
print(f"URL: {os.getenv('SUPABASE_URL')}")
print(f"Key: {os.getenv('SUPABASE_ANON_KEY')[:20]}...")

try:
    supabase = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_ANON_KEY")
    )
    
    # Test 1: Check ingredient_rules table
    print("\n1. Testing ingredient_rules table...")
    result = supabase.table("ingredient_rules").select("*").limit(5).execute()
    print(f"✓ Found {len(result.data)} ingredients")
    if result.data:
        print(f"  Sample: {result.data[0]['name']}")
    
    # Test 2: Check products table
    print("\n2. Testing products table...")
    result = supabase.table("products").select("*").limit(5).execute()
    print(f"✓ Found {len(result.data)} products")
    
    # Test 3: Try to insert a test product
    print("\n3. Testing product insert...")
    test_product = {
        "name": "Test Product",
        "name_normalized": "test product",
        "brand": "Test Brand",
        "category": "Test",
        "awareness_score": 75,
        "summary": "Test summary"
    }
    result = supabase.table("products").insert(test_product).execute()
    print(f"✓ Insert successful, ID: {result.data[0]['id']}")
    
    # Clean up test
    supabase.table("products").delete().eq("name", "Test Product").execute()
    print("✓ Test cleanup done")
    
    print("\n✅ All tests passed! Database is working correctly.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
