# Wildberries Parser MVP - Walkthrough

## Overview
This application parses product data from Wildberries (Name, Brand, Price, Rating) and exports it to Excel. It features a simple web interface for easy use.

## Prerequisites
- Python 3.8+
- Active internet connection
- (Optional) Proxies if running from a data center (to avoid 429 blocks)

## Quick Start

### 1. Run the Application
The environment is managed by Poetry. Run the following command to start the web server:
```bash
poetry run uvicorn main:app --reload
```

### 2. Use the Parser
1. Open your browser and navigate to `http://127.0.0.1:8000`.
2. Enter a search query (e.g., "iphone 15").
3. Set the number of items to parse (e.g., 50).
4. Click **"Начать сбор данных"**.

### 3. Check Results
- After parsing is complete, a "Скачать Excel" button will appear.
- Click it to download the `.xlsx` file.
- Files are also saved in the `exports/` directory.

## Troubleshooting

### "Rate limit hit (429)" or "No products found"
Wildberries aggressively blocks requests from data center IPs (cloud servers). If you see this error:
1. **Try running this locally** on your personal computer (residential IP).
2. **Use a Proxy**: Edit `scraper.py` to add proxy support to the `httpx.AsyncClient`:
   ```python
   async with httpx.AsyncClient(proxies="http://user:pass@host:port", ...) as client:
   ```
3. **Wait**: Sometimes the block is temporary.

## Project Structure
- `main.py`: The web server (FastAPI).
- `scraper.py`: Logic for talking to WB internals.
- `exporter.py`: Logic for saving data to Excel.
- `templates/index.html`: The frontend user interface.
