"""
BigBasket web scraper for Indian product ingredients.
Scrapes product pages respectfully with delays.
"""
import httpx
import asyncio
from bs4 import BeautifulSoup
from typing import Optional


async def search(product_name: str) -> dict:
    """
    Search BigBasket for product and scrape ingredients from product page.
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
        # Search for product
        search_url = f"https://www.bigbasket.com/ps/?q={product_name.replace(' ', '+')}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            # Search page
            response = await client.get(search_url, headers=headers)
            
            if response.status_code != 200:
                print(f"[BIGBASKET] Search failed with status {response.status_code}")
                return result
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find first product link
            # BigBasket structure may change, so we try multiple selectors
            product_link = None
            
            # Try different selectors
            selectors = [
                'a[href*="/pd/"]',  # Product detail links
                'a.ng-star-inserted[href*="/pd/"]',
                '.product a[href*="/pd/"]'
            ]
            
            for selector in selectors:
                link_elem = soup.select_one(selector)
                if link_elem and link_elem.get('href'):
                    product_link = link_elem['href']
                    if not product_link.startswith('http'):
                        product_link = f"https://www.bigbasket.com{product_link}"
                    break
            
            if not product_link:
                print("[BIGBASKET] No product link found in search results")
                return result
            
            # Be respectful - add delay
            await asyncio.sleep(1)
            
            # Get product detail page
            response = await client.get(product_link, headers=headers)
            
            if response.status_code != 200:
                print(f"[BIGBASKET] Product page failed with status {response.status_code}")
                return result
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract product info
            # Try to find product name
            product_name_elem = soup.select_one('h1') or soup.select_one('.product-name')
            if product_name_elem:
                result["product_name"] = product_name_elem.get_text(strip=True)
            
            # Try to find brand
            brand_elem = soup.select_one('.brand') or soup.select_one('[class*="brand"]')
            if brand_elem:
                result["brand"] = brand_elem.get_text(strip=True)
            
            # Try to find image
            img_elem = soup.select_one('img[src*="product"]') or soup.select_one('.product-image img')
            if img_elem and img_elem.get('src'):
                result["image_url"] = img_elem['src']
            
            # Try to find ingredients
            # BigBasket may have ingredients in different places
            ingredients_text = None
            
            # Try different selectors for ingredients
            ingredient_selectors = [
                'div:contains("Ingredients")',
                'div:contains("ingredients")',
                '[class*="ingredient"]',
                'div:contains("Contents")',
                '.product-description'
            ]
            
            for selector in ingredient_selectors:
                elem = soup.select_one(selector)
                if elem:
                    text = elem.get_text(strip=True)
                    # Check if it looks like ingredients
                    if len(text) > 20 and (',' in text or 'and' in text.lower()):
                        ingredients_text = text
                        break
            
            if ingredients_text:
                # Clean up the text
                ingredients_text = ingredients_text.replace("Ingredients:", "").replace("ingredients:", "").strip()
                
                # Parse into list
                # Try to split by comma, semicolon, or "and"
                ingredients_list = []
                
                # Split by comma first
                parts = ingredients_text.split(',')
                for part in parts:
                    # Further split by "and"
                    sub_parts = part.split(' and ')
                    for sub_part in sub_parts:
                        cleaned = sub_part.strip()
                        if cleaned and len(cleaned) > 1:
                            ingredients_list.append(cleaned)
                
                if ingredients_list and len(ingredients_list) > 3:
                    result["found"] = True
                    result["ingredients_text"] = ingredients_text
                    result["ingredients_list"] = ingredients_list
            
            return result
            
    except Exception as e:
        print(f"[BIGBASKET] Scraping error: {e}")
        return result
