import asyncio
import httpx
import logging
from typing import List, Dict, Any, Optional
import urllib.parse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WBScraper:
    BASE_URL = "https://search.wb.ru/exactmatch/ru/common/v5/search"
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Origin": "https://www.wildberries.ru",
            "Referer": "https://www.wildberries.ru/catalog/0/search.aspx",
        }

    async def search_products(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Search for products by query and return a list of product data.
        """
        products = []
        page = 1
        retries = 3
        
        # WB loves HTTP/2
        async with httpx.AsyncClient(headers=self.headers, timeout=15.0, http2=True) as client:
            while len(products) < limit:
                try:
                    params = {
                        "appType": 1,
                        "curr": "rub",
                        "dest": -1257786,  # Moscow
                        "query": query,
                        "resultset": "catalog",
                        "sort": "popular",
                        "spp": 30,
                        "suppressSpellcheck": "false",
                        "page": page,
                    }
                    
                    url = f"{self.BASE_URL}?{urllib.parse.urlencode(params)}"
                    logger.info(f"Fetching page {page} for query '{query}'")
                    
                    response = await client.get(url)
                    
                    if response.status_code == 429:
                        wait_time = 2 * (4 - retries)
                        logger.warning(f"Rate limit hit (429), waiting {wait_time}s...")
                        await asyncio.sleep(wait_time)
                        if retries == 1: # Last retry
                            raise Exception("Wildberries blocked the request (429 Too Many Requests). Your IP might be restricted. Try using a proxy or running locally.")
                        continue
                        
                    response.raise_for_status()
                    
                    try:
                        data = response.json()
                    except Exception as e:
                        logger.error(f"Failed to decode JSON. Response text: {response.text[:200]}...")
                        break
                    
                    # Handle different API response structures
                    if 'data' in data and 'products' in data['data']:
                        page_products = data['data']['products']
                    elif 'products' in data:
                        page_products = data['products']
                    else:
                        logger.warning(f"No products found. Response Keys: {list(data.keys())}")
                        if 'data' in data:
                            logger.warning(f"Data Keys: {list(data['data'].keys())}")
                        break
                        
                    if not page_products:
                        logger.info(f"Empty products list. Response Keys: {list(data.keys())}")
                        if 'data' in data:
                             logger.info(f"Data content: {data['data']}")
                        break
                        
                    for prod in page_products:
                        if len(products) >= limit:
                            break
                        
                        # Extract price from sizes (WB API structure)
                        price = 0
                        if 'sizes' in prod and len(prod['sizes']) > 0:
                            price_data = prod['sizes'][0].get('price', {})
                            # 'product' is the sale price, 'basic' is the original price
                            raw_price = price_data.get('product', price_data.get('basic', 0))
                            price = raw_price / 100
                        
                        # Extract required fields
                        item = {
                            "id": prod.get("id"),
                            "name": prod.get("name"),
                            "brand": prod.get("brand"),
                            "price": price, 
                            "rating": prod.get("reviewRating"),
                            "url": f"https://www.wildberries.ru/catalog/{prod.get('id')}/detail.aspx"
                        }
                        products.append(item)
                    
                    page += 1
                    
                    # Be nice to the API
                    await asyncio.sleep(1.0)
                    
                except Exception as e:
                    logger.error(f"Error fetching data: {e}")
                    retries -= 1
                    if retries <= 0:
                        break
                    await asyncio.sleep(1)
                    
        return products

if __name__ == "__main__":
    # Simple test
    async def test():
        scraper = WBScraper()
        res = await scraper.search_products("носки", 10)
        print(f"Found {len(res)} products")
        if res:
            print(res[0])
            
    asyncio.run(test())
