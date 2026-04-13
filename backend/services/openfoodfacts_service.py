import httpx
from typing import Optional


async def get_product_image(product_name: str) -> Optional[str]:
    """
    Fetch product image from Open Food Facts API.
    Returns image URL or None if not found.
    """
    try:
        url = "https://world.openfoodfacts.org/cgi/search.pl"
        params = {
            "search_terms": product_name,
            "json": 1,
            "page_size": 5,
            "search_simple": 1
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                products = data.get("products", [])
                
                # Find first product with an image
                for product in products:
                    image_url = product.get("image_url")
                    if image_url:
                        return image_url
                
                return None
            else:
                return None
                
    except Exception as e:
        # Gracefully handle timeouts and errors
        print(f"Open Food Facts API error: {e}")
        return None


async def search(product_name: str) -> dict:
    """
    Search Open Food Facts for complete product data including ingredients.
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
    
    try:
        url = "https://world.openfoodfacts.org/cgi/search.pl"
        params = {
            "search_terms": product_name,
            "json": 1,
            "page_size": 5,
            "search_simple": 1,
            "fields": "product_name,brands,categories,image_url,ingredients_text,ingredients"
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                products = data.get("products", [])
                
                if products:
                    # Get the first matching product
                    product = products[0]
                    
                    # Extract ingredients
                    ingredients_text = product.get("ingredients_text", "")
                    ingredients = product.get("ingredients", [])
                    
                    # Build ingredients list
                    ingredients_list = []
                    if ingredients:
                        for ing in ingredients:
                            ing_name = ing.get("text") or ing.get("id", "")
                            if ing_name:
                                ingredients_list.append(ing_name.strip())
                    
                    # If no structured ingredients, try to parse text
                    if not ingredients_list and ingredients_text:
                        # Simple parsing: split by comma
                        ingredients_list = [i.strip() for i in ingredients_text.split(",") if i.strip()]
                    
                    if ingredients_list:
                        result["found"] = True
                        result["product_name"] = product.get("product_name", product_name)
                        result["brand"] = product.get("brands", "").split(",")[0].strip() if product.get("brands") else None
                        result["category"] = product.get("categories", "").split(",")[0].strip() if product.get("categories") else None
                        result["image_url"] = product.get("image_url")
                        result["ingredients_text"] = ingredients_text
                        result["ingredients_list"] = ingredients_list
                
                return result
            else:
                return result
                
    except Exception as e:
        print(f"Open Food Facts search error: {e}")
        return result
