import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Initialize client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Listing available Gemini models...")
try:
    models_pager = client.models.list()
    print(f"\nAvailable models:")
    for model in models_pager:
        print(f"  - {model.name}")
except Exception as e:
    print(f"Error listing models: {e}")
    import traceback
    traceback.print_exc()
