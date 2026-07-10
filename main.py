import uvicorn
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import threading
import time

# Ensure current folder is in Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config
import database
import scrapers

app = FastAPI(
    title="Hot News Scraper API",
    description="API for accessing hot and categorized news from Japan and US.",
    version="1.0.0"
)

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def run_background_scraper():
    """Background worker that periodically updates news data."""
    # Wait a few seconds for the server to bind and start properly
    time.sleep(2)
    
    print("Background Scraper Thread: Started.")
    # Perform initial scrape on start if DB is empty
    try:
        existing_news = database.get_news(limit=1)
        if not existing_news:
            print("Database is empty. Running initial scrape...")
            items = scrapers.scrape_all_feeds()
            inserted = database.save_news_items(items)
            print(f"Initial scrape completed. Inserted {inserted} items.")
        else:
            print("Database already contains news. Skipping initial startup scrape.")
    except Exception as e:
        print(f"Error during startup scrape: {e}", file=sys.stderr)
        
    while True:
        try:
            # Sleep first for the interval
            time.sleep(config.SCRAPE_INTERVAL)
            print("Background Scraper Thread: Starting scheduled update...")
            items = scrapers.scrape_all_feeds()
            inserted = database.save_news_items(items)
            # Cleanup news older than 7 days
            deleted = database.cleanup_old_news(days=7)
            print(f"Scheduled update completed. Inserted {inserted} items, cleaned up {deleted} old items.")
        except Exception as e:
            print(f"Error in background scraper loop: {e}", file=sys.stderr)

@app.on_event("startup")
def startup_event():
    # Initialize database tables
    database.init_db()
    
    # Start the background scraping worker
    scraper_thread = threading.Thread(target=run_background_scraper, daemon=True)
    scraper_thread.start()

# API Endpoints
@app.get("/api/news")
def get_news_api(
    region: str = Query(None, description="Region code (JP or US)"),
    category: str = Query(None, description="News category (top, society, business, technology, sports, entertainment)"),
    search: str = Query(None, description="Search query string"),
    limit: int = Query(60, ge=1, le=200, description="Max number of items to return")
):
    try:
        items = database.get_news(region=region, category=category, search_query=search, limit=limit)
        return {
            "status": "success",
            "count": len(items),
            "data": items
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/scrape")
def trigger_scrape_api():
    """Manually trigger a scrape execution and return newly inserted count."""
    try:
        print("Manual scrape request received.")
        items = scrapers.scrape_all_feeds()
        inserted = database.save_news_items(items)
        return {
            "status": "success",
            "message": "Scrape completed successfully",
            "inserted": inserted
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/meta")
def get_meta_info():
    """Returns regions, categories and configuration metadata."""
    return {
        "regions": config.REGIONS,
        "categories": config.CATEGORIES,
        "scrape_interval_seconds": config.SCRAPE_INTERVAL
    }

# Serve Frontend static assets
static_dir = os.path.join(config.BASE_DIR, "static")
os.makedirs(static_dir, exist_ok=True)

# Route for index.html at root "/"
@app.get("/")
def read_index():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"status": "error", "message": "Frontend static file index.html not found. Backend is running successfully."}

# Mount static folder for CSS, JS, etc.
app.mount("/static", StaticFiles(directory=static_dir), name="static")

if __name__ == "__main__":
    print("Starting FastAPI app server...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
