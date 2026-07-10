import sqlite3
import datetime
from typing import List, Dict, Any, Optional
import os
import sys

# Import config (ensure hot_news_scraper path is in python path)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config

def get_db_connection():
    conn = sqlite3.connect(config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database and creates the news_items table if it doesn't exist."""
    os.makedirs(os.path.dirname(config.DATABASE_PATH), exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            source TEXT NOT NULL,
            region TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            published_time TEXT,
            fetched_time TEXT NOT NULL
        )
    """)
    # Add indexes for faster querying
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_region_category ON news_items (region, category)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_fetched_time ON news_items (fetched_time)")
    conn.commit()
    conn.close()

def save_news_items(items: List[Dict[str, Any]]) -> int:
    """
    Saves a list of news items to the database.
    Ignores duplicates based on the unique URL.
    Returns the number of newly inserted items.
    """
    if not items:
        return 0
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    inserted_count = 0
    fetched_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    for item in items:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO news_items (
                    title, url, source, region, category, description, published_time, fetched_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item.get("title"),
                item.get("url"),
                item.get("source"),
                item.get("region"),
                item.get("category"),
                item.get("description"),
                item.get("published_time"),
                fetched_time
            ))
            if cursor.rowcount > 0:
                inserted_count += 1
        except Exception as e:
            print(f"Error inserting news item: {e}", file=sys.stderr)
            
    conn.commit()
    conn.close()
    return inserted_count

def get_news(
    region: Optional[str] = None,
    category: Optional[str] = None,
    search_query: Optional[str] = None,
    limit: int = 60
) -> List[Dict[str, Any]]:
    """
    Retrieves news items based on filters.
    Sorted by fetched_time and published_time descending.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM news_items WHERE 1=1"
    params = []
    
    if region:
        query += " AND region = ?"
        params.append(region)
        
    if category:
        query += " AND category = ?"
        params.append(category)
        
    if search_query:
        query += " AND (title LIKE ? OR description LIKE ?)"
        params.append(f"%{search_query}%")
        params.append(f"%{search_query}%")
        
    # Sort order: get newest fetched news first
    query += " ORDER BY fetched_time DESC, published_time DESC LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    result = []
    for row in rows:
        result.append({
            "id": row["id"],
            "title": row["title"],
            "url": row["url"],
            "source": row["source"],
            "region": row["region"],
            "category": row["category"],
            "description": row["description"],
            "published_time": row["published_time"],
            "fetched_time": row["fetched_time"]
        })
        
    conn.close()
    return result

def cleanup_old_news(days: int = 7) -> int:
    """Deletes news items older than specified days to keep DB size small."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cutoff_date = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)).isoformat()
    
    cursor.execute("DELETE FROM news_items WHERE fetched_time < ?", (cutoff_date,))
    deleted_count = cursor.rowcount
    
    conn.commit()
    conn.close()
    return deleted_count

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
