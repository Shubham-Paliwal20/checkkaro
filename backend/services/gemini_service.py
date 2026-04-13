import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv()

# Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

GEMINI_SYSTEM_PROMPT = """You are an ingredient information specialist for CheckKaro, an Indian consumer awareness platform. Your role is to provide factual, neutral, educational information about product ingredients based on publicly available data from FSSAI, WHO, EFSA, EU regulations, and peer-reviewed research.

STRICT LANGUAGE RULES — never use these words in any output:
safe, unsafe, dangerous, harmful, toxic, poison, cancer, carcinogen, deadly, lethal, kill, disease, risk, hazard, warning

USE ONLY this neutral language:
- "generally recognised" instead of safe
- "worth knowing" instead of concerning
- "commonly questioned" instead of unsafe/dangerous
- "flagged by researchers" instead of harmful
- "restricted in some countries" instead of banned/dangerous
- "subject to ongoing research" instead of controversial

CLASSIFICATION SYSTEM (BE VERY STRICT):
- generally_recognised: ONLY ingredients with ZERO regulatory flags, ZERO restrictions, ZERO debates in ANY major jurisdiction (US, EU, India, Canada, Australia, Japan)
- worth_knowing: Ingredients with concentration limits, usage restrictions in ANY country, or discussed in peer-reviewed research with concerns
- commonly_questioned: Ingredients restricted/banned in ANY country, flagged by ANY regulatory body (EU, FDA, Health Canada, FSSAI), or subject to scientific debate

AWARENESS SCORE CALCULATION (SCIENTIFIC & STRICT):
Start at 100

For EACH ingredient, subtract points:
- Generally Recognised: -0 points
- Worth Knowing: -8 points (stricter)
- Commonly Questioned: -20 points (much stricter)

ADDITIONAL PENALTIES (check each ingredient and apply ALL that match):
- Banned in EU: -15 points per ingredient
- Banned in Canada: -15 points per ingredient
- Restricted by WHO: -12 points per ingredient
- Has concentration limits in FSSAI: -8 points per ingredient
- Linked to skin sensitization/allergies: -8 points per ingredient
- Endocrine disruptor concerns: -15 points per ingredient
- Flagged in carcinogenicity studies: -20 points per ingredient
- Banned in ANY other country: -10 points per ingredient

MINIMUM SCORE: 0
MAXIMUM SCORE: 100

IMPORTANT: Be VERY strict. Products with ingredients banned in major countries should score below 40. Products with multiple questioned ingredients should score below 60. Products like Dove soap with parabens, sulfates, and other questioned ingredients should score 30-50 range.

Always end product summary with:
"This information is for general awareness based on publicly available regulatory data. It is not a health assessment or medical advice."
"""


async def call_gemini_api(prompt: str, max_tokens: int = 4000) -> dict:
    """Call Gemini API directly using REST"""
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"{GEMINI_SYSTEM_PROMPT}\n\n{prompt}"
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.3,
                    "maxOutputTokens": max_tokens
                }
            }
            
            response = await client.post(
                f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                raise Exception(f"Gemini API error: {response.status_code} - {response.text}")
            
            result = response.json()
            
            # Extract text from response
            if "candidates" in result and len(result["candidates"]) > 0:
                candidate = result["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    text = candidate["content"]["parts"][0]["text"]
                    
                    # Check finish reason
                    finish_reason = candidate.get("finishReason", "UNKNOWN")
                    print(f"[GEMINI] Finish reason: {finish_reason}, Length: {len(text)}")
                    
                    # Clean JSON from markdown
                    text = text.strip()
                    if text.startswith("```json"):
                        text = text[7:]
                    if text.startswith("```"):
                        text = text[3:]
                    if text.endswith("```"):
                        text = text[:-3]
                    text = text.strip()
                    
                    # Parse JSON
                    return json.loads(text)
            
            raise Exception("Invalid response structure from Gemini")
            
    except json.JSONDecodeError as e:
        print(f"[GEMINI JSON ERROR] {str(e)}")
        print(f"[GEMINI JSON ERROR] Text: {text[:500]}")
        raise
    except Exception as e:
        print(f"[GEMINI ERROR] {str(e)}")
        raise


async def analyze_product(product_name: str) -> dict:
    """
    Analyze a product and return ingredient breakdown with awareness score.
    """
    try:
        # Simplified prompt to reduce token usage
        user_prompt = f"""Product: {product_name}

List top 10 key ingredients with:
- name
- aliases  
- classification (generally_recognised/worth_knowing/commonly_questioned)
- one_line_note (max 8 words)
- regulatory_note (brief)

Also provide: brand, category, awareness_score (0-100), summary (2 sentences), fssai_note, verdict, recommendation

Return valid JSON:
{{
  "brand": "string",
  "category": "string",
  "awareness_score": 85,
  "summary": "string",
  "fssai_note": "string",
  "verdict": "string",
  "recommendation": "string",
  "ingredients": [
    {{
      "name": "string",
      "aliases": "string",
      "classification": "generally_recognised",
      "one_line_note": "string",
      "regulatory_note": "string"
    }}
  ]
}}"""

        result = await call_gemini_api(user_prompt, max_tokens=4096)
        return result

    except Exception as e:
        # Fallback response if Gemini fails
        print(f"[GEMINI ERROR] {str(e)}")
        return {
            "brand": "Unknown",
            "category": "General",
            "awareness_score": 50,
            "summary": f"Analysis for {product_name} could not be completed at this time. This information is for general awareness based on publicly available regulatory data. It is not a health assessment or medical advice.",
            "fssai_note": "Product subject to FSSAI regulations.",
            "verdict": "Analysis unavailable",
            "recommendation": "Unable to provide recommendation at this time",
            "ingredients": [],
            "error": str(e)
        }


async def analyze_ingredient(ingredient_name: str) -> dict:
    """
    Analyze a single ingredient and return detailed information.
    """
    try:
        user_prompt = f"""Ingredient: {ingredient_name}

Provide detailed information:
- name (full ingredient name)
- aliases (all alternative names and E-numbers as array)
- what_it_is (2 sentences in plain English)
- commonly_found_in (list of product types as string)
- classification (one of: generally_recognised, worth_knowing, commonly_questioned)
- one_line_note (neutral, max 10 words)
- countries_restricted (array of country names, empty if none)
- fssai_position (1 sentence about FSSAI/Indian regulation)

Return ONLY valid JSON, no markdown:
{{
  "name": "string",
  "aliases": ["string"],
  "what_it_is": "string",
  "commonly_found_in": "string",
  "classification": "generally_recognised",
  "one_line_note": "string",
  "countries_restricted": ["string"],
  "fssai_position": "string"
}}"""

        result = await call_gemini_api(user_prompt, max_tokens=3000)
        return result

    except Exception as e:
        # Fallback response
        print(f"[GEMINI ERROR] {str(e)}")
        return {
            "name": ingredient_name,
            "aliases": [],
            "what_it_is": f"Information about {ingredient_name} could not be retrieved at this time.",
            "commonly_found_in": "Various products",
            "classification": "worth_knowing",
            "one_line_note": "Analysis unavailable",
            "countries_restricted": [],
            "fssai_position": "Subject to FSSAI regulations.",
            "error": str(e)
        }


async def analyze_ingredients_list(product_name: str, ingredients_text: str) -> dict:
    """
    Analyze a known list of ingredients (from external source) and classify them.
    This is more accurate than estimating ingredients.
    """
    try:
        user_prompt = f"""Product: {product_name}

Known ingredients from product label: {ingredients_text}

For EACH ingredient in the list above, provide:
- name (ingredient name)
- aliases (alternative names or E-numbers)
- classification (one of: generally_recognised, worth_knowing, commonly_questioned) - BE VERY STRICT
- one_line_note (max 10 words, neutral language)
- regulatory_note (which countries restrict/ban it, FSSAI position)

Also provide:
- brand (brand name if known)
- category (e.g., Snacks, Beverages, Cosmetics, Personal Care)
- awareness_score (integer 0-100, USE THE STRICT CALCULATION)
- summary (2 sentences, neutral language, ending with disclaimer)
- fssai_note (1 sentence about FSSAI regulation)
- verdict (Based on score)
- recommendation (Based on score)

Return ONLY valid JSON, no markdown formatting.
{{
  "brand": "string",
  "category": "string",
  "awareness_score": 85,
  "summary": "string",
  "fssai_note": "string",
  "verdict": "string",
  "recommendation": "string",
  "ingredients": [
    {{
      "name": "string",
      "aliases": "string",
      "classification": "generally_recognised",
      "one_line_note": "string",
      "regulatory_note": "string"
    }}
  ]
}}"""

        result = await call_gemini_api(user_prompt, max_tokens=8000)
        return result

    except Exception as e:
        # Fallback response if Gemini fails
        print(f"[GEMINI ERROR] {str(e)}")
        return {
            "brand": "Unknown",
            "category": "General",
            "awareness_score": 50,
            "summary": f"Analysis for {product_name} could not be completed at this time. This information is for general awareness based on publicly available regulatory data. It is not a health assessment or medical advice.",
            "fssai_note": "Product subject to FSSAI regulations.",
            "verdict": "Analysis unavailable",
            "recommendation": "Unable to provide recommendation at this time",
            "ingredients": [],
            "error": str(e)
        }
