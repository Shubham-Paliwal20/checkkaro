import os
import base64
import json
import httpx
from anthropic import AsyncAnthropic

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL = "claude-3-5-haiku-20241022"

_client: AsyncAnthropic | None = None


def _get_client() -> AsyncAnthropic:
    global _client
    if _client is None:
        _client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    return _client


SYSTEM_PROMPT = """You are an ingredient classification specialist for CheckKaro, an Indian consumer awareness platform.

CLASSIFICATION:
- generally_recognised: No regulatory flags in any major jurisdiction
- worth_knowing: Has usage limits, restrictions in some countries, or ongoing research
- commonly_questioned: Restricted/banned in any country, flagged by EU/FDA/FSSAI/WHO

AWARENESS SCORE (start 100):
- worth_knowing ingredient: -8 pts
- commonly_questioned ingredient: -20 pts
- Banned in EU/Canada: -15 pts each
- Endocrine disruptor concerns: -15 pts
- Flagged in carcinogenicity studies: -20 pts
Minimum: 0, Maximum: 100

Language: never use "safe/unsafe/dangerous/toxic/cancer". Use "generally recognised / worth knowing / commonly questioned / flagged by researchers / restricted in some countries".

Always end summary with: "This information is for general awareness based on publicly available regulatory data. It is not a health assessment or medical advice."
"""


async def extract_ingredients_from_image(image_url: str, product_name: str) -> str:
    """Use Claude Vision to read ingredients text from a product label image."""
    try:
        async with httpx.AsyncClient(timeout=30.0) as http:
            img_resp = await http.get(image_url)
            if img_resp.status_code != 200:
                return "NOT_VISIBLE"
            img_b64 = base64.b64encode(img_resp.content).decode()
            mime = img_resp.headers.get("content-type", "image/jpeg").split(";")[0].strip()

        client = _get_client()
        msg = await client.messages.create(
            model=MODEL,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {"type": "base64", "media_type": mime, "data": img_b64},
                    },
                    {
                        "type": "text",
                        "text": (
                            f'This is a product label for "{product_name}". '
                            "Extract ONLY the ingredients list text exactly as printed on the label. "
                            "Return ONLY the raw ingredients text, no explanation. "
                            "If the ingredients section is not visible, return exactly: NOT_VISIBLE"
                        ),
                    },
                ],
            }],
        )
        return msg.content[0].text.strip()
    except Exception as e:
        print(f"[CLAUDE VISION ERROR] {e}")
        return "NOT_VISIBLE"


async def analyze_ingredients(product_name: str, ingredients_text: str) -> dict:
    """Classify ingredients list using Claude and return structured analysis."""
    prompt = f"""Product: {product_name}

Ingredients from label: {ingredients_text}

For EACH ingredient provide: name, aliases, classification, one_line_note (max 10 words), regulatory_note.
Also provide: brand, category, awareness_score (integer), summary (2 sentences + disclaimer), fssai_note, verdict, recommendation.

Return ONLY valid JSON, no markdown:
{{
  "brand": "string",
  "category": "string",
  "awareness_score": 75,
  "summary": "string",
  "fssai_note": "string",
  "verdict": "string",
  "recommendation": "string",
  "ingredients": [
    {{"name": "string", "aliases": "string", "classification": "generally_recognised", "one_line_note": "string", "regulatory_note": "string"}}
  ]
}}"""

    try:
        client = _get_client()
        msg = await client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        text = msg.content[0].text.strip()
        # Strip markdown fences if present
        if text.startswith("```"):
            text = text.split("```", 2)[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    except Exception as e:
        print(f"[CLAUDE ANALYSIS ERROR] {e}")
        return {
            "brand": "Unknown",
            "category": "General",
            "awareness_score": 50,
            "summary": f"Analysis for {product_name} could not be completed. This information is for general awareness based on publicly available regulatory data. It is not a health assessment or medical advice.",
            "fssai_note": "Subject to FSSAI regulations.",
            "verdict": "Analysis unavailable",
            "recommendation": "Unable to provide recommendation at this time.",
            "ingredients": [],
            "error": str(e),
        }
