import feedparser
import re
from bs4 import BeautifulSoup
import sys
import os
from typing import List, Dict, Any

# Ensure path is set
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config

def clean_html(html_text: str) -> str:
    """Helper to remove HTML tags and clean up spaces."""
    if not html_text:
        return ""
    # Strip HTML tags using BeautifulSoup
    soup = BeautifulSoup(html_text, "html.parser")
    text = soup.get_text(separator=" ")
    # Replace multiple spaces/newlines
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_rss_feed(url: str, region: str, category: str, source_name: str) -> List[Dict[str, Any]]:
    """
    Parses an RSS feed and returns a list of standardized news items.
    """
    print(f"Scraping {region} - {category} from: {url}")
    parsed = feedparser.parse(url)
    
    # Handle parsing errors or empty feeds
    if parsed.bozo and not parsed.entries:
        print(f"Warning: Failed to parse feed at {url} cleanly: {parsed.bozo_exception}")
        
    items = []
    for entry in parsed.entries:
        title = entry.get("title", "").strip()
        # Find the URL (link)
        url_link = entry.get("link", "").strip()
        if not title or not url_link:
            continue
            
        description = entry.get("summary", "") or entry.get("description", "")
        description = clean_html(description)
        
        # Limit description size
        if len(description) > 500:
            description = description[:497] + "..."
            
        # Get publication time
        pub_time = entry.get("published", "") or entry.get("pubDate", "") or entry.get("updated", "")
        
        items.append({
            "title": title,
            "url": url_link,
            "source": source_name,
            "region": region,
            "category": category,
            "description": description,
            "published_time": pub_time
        })
        
    print(f"Successfully scraped {len(items)} items.")
    return items

def scrape_all_feeds() -> List[Dict[str, Any]]:
    """
    Scrapes all configured feeds for JP and US.
    Returns a unified list of news items.
    """
    all_items = []
    
    for region, categories in config.NEWS_FEEDS.items():
        for category, feed_data in categories.items():
            # Support both a single dict or a list of dicts
            feeds = feed_data if isinstance(feed_data, list) else [feed_data]
            
            for feed_info in feeds:
                url = feed_info["url"]
                source_name = feed_info["source"]
                    
                try:
                    items = parse_rss_feed(url, region, category, source_name)
                    all_items.extend(items)
                except Exception as e:
                    print(f"Error scraping {region} {category} from {source_name}: {e}", file=sys.stderr)
                
    return all_items

if __name__ == "__main__":
    # Test scraping
    print("Testing scrapers...")
    # Just scrape US technology as a test
    test_url = config.NEWS_FEEDS["US"]["technology"]
    items = parse_rss_feed(test_url, "US", "technology", "The New York Times")
    print(f"Found {len(items)} items. Example:")
    if items:
        import pprint
        pprint.pprint(items[0])
