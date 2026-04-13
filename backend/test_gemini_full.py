import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

prompt = """Product sold in India: Dove Soap. 

List ALL ingredients. Return ONLY valid JSON:
{
  "brand": "string",
  "category": "string",
  "awareness_score": 85,
  "summary": "string",
  "fssai_note": "string",
  "verdict": "string",
  "recommendation": "string",
  "ingredients": [
    {
      "name": "string",
      "aliases": "string",
      "classification": "generally_recognised",
      "one_line_note": "string",
      "regulatory_note": "string"
    }
  ]
}"""

print("Sending request to Gemini...")
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        temperature=0.3,
        max_output_tokens=4000,
        response_mime_type="application/json"
    )
)

print(f"\nResponse object type: {type(response)}")
print(f"Response text length: {len(response.text)}")
print(f"Response text:\n{response.text}")

# Check for finish_reason or other metadata
if hasattr(response, 'candidates'):
    print(f"\nCandidates: {response.candidates}")
    for i, candidate in enumerate(response.candidates):
        print(f"\nCandidate {i}:")
        if hasattr(candidate, 'finish_reason'):
            print(f"  Finish reason: {candidate.finish_reason}")
        if hasattr(candidate, 'content'):
            print(f"  Content length: {len(str(candidate.content))}")
