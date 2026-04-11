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
