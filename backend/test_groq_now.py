import os
import asyncio
from dotenv import load_dotenv
from services import groq_service

load_dotenv()

async def test():
    print("Testing Groq product analysis...")
    result = await groq_service.analyze_product("Dove Soap")
    print(f"\nResult: {result}")
    print(f"\nIngredients count: {len(result.get('ingredients', []))}")
    print(f"Awareness score: {result.get('awareness_score')}")
    print(f"Brand: {result.get('brand')}")

if __name__ == "__main__":
    asyncio.run(test())
