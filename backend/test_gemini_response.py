import os
import asyncio
from dotenv import load_dotenv
from services import gemini_service

load_dotenv()

async def test():
    print("Testing Gemini product analysis...")
    result = await gemini_service.analyze_product("Dove Soap")
    print(f"\nResult: {result}")
    print(f"\nIngredients count: {len(result.get('ingredients', []))}")
    print(f"Awareness score: {result.get('awareness_score')}")

if __name__ == "__main__":
    asyncio.run(test())
