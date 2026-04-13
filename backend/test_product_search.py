import asyncio
import os
from dotenv import load_dotenv
from services import groq_service

load_dotenv()

async def test_product_analysis():
    print("Testing product analysis with Groq...")
    print(f"API Key: {os.getenv('GROQ_API_KEY')[:20]}...")
    
    try:
        print("\n1. Testing analyze_product for 'Parle-G'...")
        result = await groq_service.analyze_product("Parle-G")
        
        print(f"\nBrand: {result.get('brand')}")
        print(f"Category: {result.get('category')}")
        print(f"Awareness Score: {result.get('awareness_score')}")
        print(f"Number of ingredients: {len(result.get('ingredients', []))}")
        
        if result.get('ingredients'):
            print("\nFirst 3 ingredients:")
            for ing in result['ingredients'][:3]:
                print(f"  - {ing.get('name')} ({ing.get('classification')})")
        else:
            print("\n❌ NO INGREDIENTS RETURNED!")
            if 'error' in result:
                print(f"Error: {result['error']}")
        
        print(f"\nSummary: {result.get('summary')}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_product_analysis())
