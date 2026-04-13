import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def list_models():
    api_key = os.getenv("GEMINI_API_KEY")
    
    async with httpx.AsyncClient() as client:
        # Try v1beta
        print("Trying v1beta API...")
        response = await client.get(
            f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        )
        
        if response.status_code == 200:
            models = response.json()
            print(f"\nFound {len(models.get('models', []))} models in v1beta:")
            for model in models.get('models', []):
                name = model.get('name', '')
                methods = model.get('supportedGenerationMethods', [])
                if 'generateContent' in methods:
                    print(f"  ✓ {name}")
        else:
            print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    asyncio.run(list_models())
