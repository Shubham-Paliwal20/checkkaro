import os
import json
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

# Use faster, smaller model to avoid rate limits
GROQ_MODEL = "llama-3.1-8b-instant"  # Faster and uses fewer tokens

GROQ_SYSTEM_PROMPT = """You are an ingredient information specialist for CheckKaro. Provide factual information about product ingredients based on FSSAI, WHO, EU, FDA regulations.

LANGUAGE RULES - never use: safe, unsafe, dangerous, harmful, toxic, poison, cancer, deadly, lethal, kill, disease, risk, hazard, warning
USE INSTEAD: generally recognised, worth knowing, commonly questioned, flagged by researchers, restricted in some countries, subject to ongoing research

CLASSIFICATION (BE STRICT):
- generally_recognised: ZERO regulatory flags, ZERO restrictions, ZERO debates anywhere
- worth_knowing: Has concentration limits OR usage restrictions OR research concerns
- commonly_questioned: Restricted/banned anywhere OR flagged by regulators OR scientific debate

SCORE CALCULATION - FOLLOW EXACTLY:
Start: 100 points

Subtract for EACH ingredient:
- Generally Recognised: 0
- Worth Knowing: 8
- Commonly Questioned: 20

Additional penalties PER ingredient (cumulative):
- Banned EU: 15
- Banned Canada: 15  
- WHO restricted: 12
- FSSAI limits: 8
- Skin sensitization: 8
- Endocrine disruptor: 15
- Carcinogenicity studies: 20
- Banned elsewhere: 10

CRITICAL RULES:
- Parabens = commonly_questioned (20) + endocrine (15) + banned (10) = 45 points MINIMUM
- Sulfates (SLS/SLES) = commonly_questioned (20) + skin (8) = 28 points MINIMUM
- Artificial Fragrance = worth_knowing (8) + skin (8) = 16 points MINIMUM
- Titanium Dioxide (cosmetics) = commonly_questioned (20) + EU ban (15) = 35 points MINIMUM
- Products with parabens/sulfates MUST score below 50
- Cosmetics with multiple questioned ingredients MUST score below 40

Min: 0, Max: 100

Always end summary: "This information is for general awareness based on publicly available regulatory data. It is not a health assessment or medical advice."
"""


def recalculate_awareness_score(ingredients: list) -> int:
    """
    Recalculate awareness score based on strict rules.
    This ensures consistent scoring regardless of AI calculation.
    """
    score = 100
    
    for ing in ingredients:
        classification = ing.get("classification", "worth_knowing").lower()
        name = ing.get("name", "").lower()
        regulatory_note = ing.get("regulatory_note", "").lower()
        
        # Basic classification penalties
        if classification == "generally_recognised":
            penalty = 0
        elif classification == "worth_knowing":
            penalty = 8
        elif classification == "commonly_questioned":
            penalty = 20
        else:
            penalty = 8  # default to worth_knowing
        
        score -= penalty
        
        # Additional penalties based on regulatory notes and ingredient names
        # Check for banned/restricted status
        if "banned in eu" in regulatory_note or "eu ban" in regulatory_note:
            score -= 15
        if "banned in canada" in regulatory_note:
            score -= 15
        if "who" in regulatory_note and ("restrict" in regulatory_note or "limit" in regulatory_note):
            score -= 12
        if "fssai" in regulatory_note and ("limit" in regulatory_note or "restrict" in regulatory_note):
            score -= 8
        if "sensitization" in regulatory_note or "allerg" in regulatory_note:
            score -= 8
        if "endocrine" in regulatory_note or "hormone" in regulatory_note:
            score -= 15
        if "carcinogen" in regulatory_note or "cancer" in regulatory_note:
            score -= 20
        if "banned" in regulatory_note and "eu" not in regulatory_note and "canada" not in regulatory_note:
            score -= 10
        
        # Specific ingredient penalties
        if "paraben" in name:
            score -= 15  # endocrine disruptor
            score -= 10  # banned in some countries
        if "sulfate" in name and ("sodium lauryl" in name or "sodium laureth" in name or "sls" in name or "sles" in name):
            score -= 8  # skin sensitization
        if "fragrance" in name or "parfum" in name or "perfume" in name:
            score -= 8  # allergen
        if "titanium dioxide" in name or "e171" in name:
            score -= 15  # EU ban in food
        if "bht" in name or "bha" in name:
            score -= 15  # endocrine concerns
        if "formaldehyde" in name:
            score -= 20  # carcinogen
        if "triclosan" in name:
            score -= 15  # banned in many countries
        if "phthalate" in name:
            score -= 15  # endocrine disruptor
    
    # Cap at 0 minimum
    return max(0, score)


async def analyze_product(product_name: str) -> dict:
    """
    Analyze a product and return ingredient breakdown with awareness score.
    """
    max_retries = 2
    last_error = None
    
    for attempt in range(max_retries):
        try:
            user_prompt = f"""Product: {product_name}

List ingredients with:
- name
- aliases
- classification (generally_recognised/worth_knowing/commonly_questioned) - BE STRICT
- one_line_note (max 10 words)
- regulatory_note (brief)

Provide:
- brand
- category
- awareness_score (0-100, CALCULATE STRICTLY: start 100, subtract per ingredient)
- summary (2 sentences with disclaimer)
- fssai_note
- verdict (based on score ranges)
- recommendation (based on score ranges)

IMPORTANT: Parabens/Sulfates/Fragrances in cosmetics = score MUST be below 50

Return valid JSON only.
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

            response = await groq_client.chat.completions.create(
                model=GROQ_MODEL,
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
            
            # RECALCULATE SCORE - Don't trust AI calculation
            if "ingredients" in result and len(result["ingredients"]) > 0:
                recalculated_score = recalculate_awareness_score(result["ingredients"])
                original_score = result.get("awareness_score", 50)
                result["awareness_score"] = recalculated_score
                print(f"[SCORE RECALC] Original: {original_score}, Recalculated: {recalculated_score}")
                
                # Update verdict and recommendation based on new score
                if recalculated_score >= 80:
                    result["verdict"] = "Generally recognised ingredients"
                    result["recommendation"] = "Can be used with general awareness"
                elif recalculated_score >= 60:
                    result["verdict"] = "Worth knowing about some ingredients"
                    result["recommendation"] = "Use with awareness of flagged ingredients"
                elif recalculated_score >= 40:
                    result["verdict"] = "Several ingredients commonly questioned"
                    result["recommendation"] = "Consider alternatives with fewer questioned ingredients"
                else:
                    result["verdict"] = "Many ingredients subject to restrictions"
                    result["recommendation"] = "Consider alternatives with fewer questioned ingredients"
            
            print(f"[GROQ SUCCESS] Analyzed {product_name} - {len(result.get('ingredients', []))} ingredients")
            return result
            
        except json.JSONDecodeError as e:
            print(f"[GROQ ERROR - Attempt {attempt + 1}] JSON decode error for {product_name}: {str(e)}")
            print(f"[GROQ ERROR] Raw content: {content[:200]}...")
            last_error = e
            if attempt < max_retries - 1:
                continue
        except Exception as e:
            print(f"[GROQ ERROR - Attempt {attempt + 1}] {type(e).__name__} for {product_name}: {str(e)}")
            last_error = e
            if attempt < max_retries - 1:
                continue
    
    # All retries failed - return fallback
    print(f"[GROQ FAILED] All {max_retries} attempts failed for {product_name}")
    return {
        "brand": "Unknown",
        "category": "General",
        "awareness_score": 50,
        "summary": f"Analysis for {product_name} could not be completed at this time. This information is for general awareness based on publicly available regulatory data. It is not a health assessment or medical advice.",
        "fssai_note": "Product subject to FSSAI regulations.",
        "verdict": "Analysis unavailable",
        "recommendation": "Unable to provide recommendation at this time",
        "ingredients": [],
        "error": str(last_error) if last_error else "Unknown error"
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
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": GROQ_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=800
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
        print(f"[GROQ ERROR] {str(e)}")
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

        response = await groq_client.chat.completions.create(
            model=GROQ_MODEL,
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
        
        # RECALCULATE SCORE - Don't trust AI calculation
        if "ingredients" in result and len(result["ingredients"]) > 0:
            recalculated_score = recalculate_awareness_score(result["ingredients"])
            original_score = result.get("awareness_score", 50)
            result["awareness_score"] = recalculated_score
            print(f"[SCORE RECALC] Original: {original_score}, Recalculated: {recalculated_score}")
            
            # Update verdict and recommendation based on new score
            if recalculated_score >= 80:
                result["verdict"] = "Generally recognised ingredients"
                result["recommendation"] = "Can be used with general awareness"
            elif recalculated_score >= 60:
                result["verdict"] = "Worth knowing about some ingredients"
                result["recommendation"] = "Use with awareness of flagged ingredients"
            elif recalculated_score >= 40:
                result["verdict"] = "Several ingredients commonly questioned"
                result["recommendation"] = "Consider alternatives with fewer questioned ingredients"
            else:
                result["verdict"] = "Many ingredients subject to restrictions"
                result["recommendation"] = "Consider alternatives with fewer questioned ingredients"
        
        return result

    except Exception as e:
        # Fallback response if Groq fails
        print(f"[GROQ ERROR] {str(e)}")
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
