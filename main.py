from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import logging
from scraper import WBScraper
from exporter import save_to_excel

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
EXPORTS_DIR = os.path.join(BASE_DIR, "exports")

# Create directories if they don't exist
os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(EXPORTS_DIR, exist_ok=True)

# Mount static files (if we had CSS/JS files, but for now we manipulate template directly or use CDN)
# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

scraper = WBScraper()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/offline", response_class=HTMLResponse)
async def read_offline(request: Request):
    return templates.TemplateResponse("index_offline.html", {"request": request})

@app.post("/api/parse")
async def parse_data(query: str = Form(...), limit: int = Form(100)):
    try:
        logger.info(f"Received parse request: query='{query}', limit={limit}")
        
        # Scrape data
        products = await scraper.search_products(query, limit)
        
        if not products:
            return JSONResponse(content={"status": "error", "message": "No products found"}, status_code=404)
        
        # Save to Excel
        filename = save_to_excel(products, filename_prefix=query.replace(" ", "_"))
        
        return JSONResponse(content={
            "status": "success", 
            "message": f"Found {len(products)} products",
            "filename": filename,
            "count": len(products)
        })
        
    except Exception as e:
        logger.error(f"Error during parsing: {e}")
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.get("/api/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(EXPORTS_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    return JSONResponse(content={"status": "error", "message": "File not found"}, status_code=404)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
