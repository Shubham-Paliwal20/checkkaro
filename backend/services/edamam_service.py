"""
Edamam Food Database API integration.
Free API: https://developer.edamam.com/food-database-api
"""
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

EDAMAM_APP_ID = os.getenv("EDAMAM_APP_ID")
EDAMAM_APP_KEY = os.getenv("EDAMAM_APP_KEY")


async def search(product_name: str) -> dict:
    """
    Search Edamam Food Database for product ingredients.
    Returns structured data with ingredients list.
    """
    result = {
        "found": False,
        "product_name": product_name,
        "brand": None,
        "category": None,
        "image_url": None,
        "ingredients_text": "",
        "ingredients_list": []
    }
    
    # Skip if API credentials not configured
    if not EDAMAM_APP_ID or not EDAMAM_APP_KEY:
        print("[EDAMAM] API credentials not configured, skipping")
        return result
    
    try:
        url = "https://api.edamam.com/api/food-database/v2/parser"
        params = {
            "app_id": EDAMAM_APP_ID,
            "app_key": EDAMAM_APP_KEY,
            "ingr": product_name,
            "nutrition-type": "cooking"
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                hints = data.get("hints", [])
                
                if hints:
                    # Get the first matching food item
                    food_item = hints[0].get("food", {})
                    
                    # Extract basic info
                    food_label = food_item.get("label", product_name)
                    category = food_item.get("category", "")
                    image_url = food_item.get("image")
                    
                    # Edamam doesn't provide detailed ingredients list
                    # But we can get nutrients which indicate composition
                    nutrients = food_item.get("nutrients", {})
                    
                    # For packaged foods, try to get ingredients from hints
                    ingredients_list = []
                    
                    # Check if there are parsed ingredients
                    parsed = data.get("parsed", [])
                    if parsed:
                        for item in parsed:
                            food = item.get("food", {})
                            label = food.get("label", "")
                            if label and label not in ingredients_list:
                                ingredients_list.append(label)
                    
                    # Edamam is better for nutritional data than ingredients
                    # Only return if we have meaningful data
                    if ingredients_list and len(ingredients_list) > 3:
                        result["found"] = True
                        result["product_name"] = food_label
                        result["category"] = category
                        result["image_url"] = image_url
                        result["ingredients_text"] = ", ".join(ingredients_list)
                        result["ingredients_list"] = ingredients_list
                
                return result
            else:
                print(f"[EDAMAM] API returned status {response.status_code}")
                return result
                
    except Exception as e:
        print(f"[EDAMAM] Search error: {e}")
        return result
