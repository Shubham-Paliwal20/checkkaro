import os
import json
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

GROQ_SYSTEM_PROMPT = """You are an ingredient information specialist for CheckKaro, an Indian consumer awareness platform. Your role is to provide factual, neutral, educational information about product ingredients based on publicly available data from FSSAI, WHO, EFSA, EU regulations, and peer-reviewed research.

STRICT LANGUAGE RULES — never use these words in any output:
safe, unsafe, dangerous, harmful, toxic, poison, cancer, carcinogen, deadly, lethal, kill, disease, risk, hazard, warning

USE ONLY this neutral language:
- "generally recognised" instead of safe
- "worth knowing" instead of concerning
- "commonly questioned" instead of unsafe/dangerous
- "flagged by researchers" instead of harmful
- "restricted in some countries" instead of banned/dangerous
- "subject to ongoing research" instead of controversial

CLASSIFICATION SYSTEM:
- generally_recognised: no notable regulatory flags in major jurisdictions
- worth_knowing: permitted but discussed in research or has regulatory limits
- commonly_questioned: restricted or banned in 1+ countries or subject to significant scientific debate

AWARENESS SCORE CALCULATION:
Start at 100
Subtract 3 for each worth_knowing ingredient
Subtract 12 for each commonly_questioned ingredient
Minimum score is 5

Always end product summary with:
"This information is for general awareness based on publicly available regulatory data. It is not a health assessment or medical advice."
"""


async def analyze_product(product_name: str) -> dict:
    """
    Analyze a product and return ingredient breakdown with awareness score.
    """
    try:
        user_prompt = f"""Product sold in India: {product_name}. 

List all known ingredients. For each ingredient provide:
- name (ingredient name)
- aliases (alternative names or E-numbers)
- classification (one of: generally_recognised, worth_knowing, commonly_questioned)
- one_line_note (max 10 words, neutral language)
- regulatory_note (FSSAI position if known)

Also provide:
- brand (brand name if known)
- category (e.g., Snacks, Beverages, Cosmetics, Personal Care)
- awareness_score (integer 0-100, calculated as described)
- summary (2 sentences, neutral language, ending with disclaimer)
- fssai_note (1 sentence about FSSAI regulation)

Return ONLY valid JSON, no markdown formatting. Use this structure:
{{
  "brand": "string",
  "category": "string",
  "awareness_score": 85,
  "summary": "string",
  "fssai_note": "string",
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

        response = await groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": GROQ_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )

        content = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        
        result = json.loads(content)
        return result

    except Exception as e:
        # Fallback response if Groq fails
        return {
            "brand": "Unknown",
            "category": "General",
            "awareness_score": 50,
            "summary": f"Analysis for {product_name} could not be completed at this time. This information is for general awareness based on publicly available regulatory data. It is not a health assessment or medical advice.",
            "fssai_note": "Product subject to FSSAI regulations.",
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

        response = await groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": GROQ_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )

        content = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        
        result = json.loads(content)
        return result

    except Exception as e:
        # Fallback response
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
