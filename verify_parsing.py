import asyncio
import os
from scraper import WBScraper
from exporter import save_to_excel

async def verify():
    print("Starting verification...")
    scraper = WBScraper()
    
    # 1. Test Scraper
    query = "носки"
    limit = 10
    print(f"Searching for '{query}' (limit {limit})...")
    products = await scraper.search_products(query, limit)
    
    if not products:
        print("❌ Scraper failed: No products found")
        return
        
    print(f"✅ Scraper success: Found {len(products)} products")
    print(f"Sample product: {products[0]}")
    
    # 2. Test Exporter
    print("Testing Excel export...")
    filename = save_to_excel(products, filename_prefix="test_verif")
    
    if filename and os.path.exists(os.path.join("exports", filename)):
        print(f"✅ Exporter success: File saved to exports/{filename}")
    else:
        print("❌ Exporter failed: File not created")
        return

    print("🎉 Verification passed successfully!")

if __name__ == "__main__":
    asyncio.run(verify())
