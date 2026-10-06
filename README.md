# WB-Parser

Wildberries product parser with a simple web interface and Excel export.

Enter a search query and the number of items: the service collects product name, brand, price and rating through the marketplace search API and returns an `.xlsx` file.

## Stack

- **FastAPI** web server with Jinja2 templates
- **httpx** (async) for requests to the marketplace search API
- **pandas** for the Excel export
- **Poetry**, **Docker** / **docker compose**

## Run locally

```bash
poetry install
poetry run uvicorn main:app --reload
```

Open http://127.0.0.1:8000, enter a query (e.g. `iphone 15`), set the number of items and start parsing. When it finishes, download the Excel file; files are also saved to `exports/`.

## Run with Docker

```bash
docker compose up -d --build
```

Server deployment steps are described in [DEPLOY.md](DEPLOY.md); a detailed walkthrough is in [walkthrough.md](walkthrough.md).

## Project structure

| File | Purpose |
|---|---|
| `main.py` | FastAPI app: web UI, parsing endpoint, file download |
| `scraper.py` | Async client for the marketplace search API |
| `exporter.py` | Export of results to Excel |
| `templates/` | Web interface |
| `test_export.py`, `verify_parsing.py` | Checks for export and parsing |

## Note

The marketplace rate-limits requests from data-center IPs. For server use, run with a reasonable request rate or configure a proxy in `scraper.py`.
