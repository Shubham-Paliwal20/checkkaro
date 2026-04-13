import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

print("Testing Groq API connection...")
print(f"API Key: {os.getenv('GROQ_API_KEY')[:20]}...")

try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    print("\nSending test request to Groq...")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello, CheckKaro!' in JSON format: {\"message\": \"your response\"}"}
        ],
        temperature=0.3,
        max_tokens=100
    )
    
    content = response.choices[0].message.content
    print(f"\n✓ Groq API Response:\n{content}")
    print("\n✅ Groq API is working correctly!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
