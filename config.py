import os

# Base directory of the scraper
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SQLite Database Path
DATABASE_PATH = os.path.join(BASE_DIR, "news.db")

# Scraper Interval in seconds (default: 30 minutes)
SCRAPE_INTERVAL = 1800

# News Category mappings (Display names in EN/ZH)
CATEGORIES = {
    "top": {"zh": "要闻", "en": "Top Picks"},
    "society": {"zh": "社会/国际", "en": "Society/World"},
    "business": {"zh": "财经", "en": "Business/Economy"},
    "technology": {"zh": "科技", "en": "IT/Technology"},
    "sports": {"zh": "体育", "en": "Sports"},
    "entertainment": {"zh": "娱乐/文化", "en": "Entertainment/Arts"}
}

# Regions configuration
REGIONS = {
    "JP": {"zh": "日本 🇯🇵", "en": "Japan"},
    "US": {"zh": "美国 🇺🇸", "en": "United States"}
}

# RSS Feed definitions grouped by Region and Category
NEWS_FEEDS = {
    "JP": {
        "top": {"url": "https://news.yahoo.co.jp/rss/topics/top-picks.xml", "source": "Yahoo! News Japan"},
        "society": {"url": "https://news.yahoo.co.jp/rss/topics/domestic.xml", "source": "Yahoo! News Japan"},
        "business": {"url": "https://news.yahoo.co.jp/rss/topics/business.xml", "source": "Yahoo! News Japan"},
        "technology": {"url": "https://news.yahoo.co.jp/rss/topics/it.xml", "source": "Yahoo! News Japan"},
        "sports": {"url": "https://news.yahoo.co.jp/rss/topics/sports.xml", "source": "Yahoo! News Japan"},
        "entertainment": {"url": "https://news.yahoo.co.jp/rss/topics/entertainment.xml", "source": "Yahoo! News Japan"}
    },
    "US": {
        "top": {"url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml", "source": "The New York Times"},
        "society": {"url": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml", "source": "The New York Times"},
        "business": {"url": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml", "source": "The New York Times"},
        "technology": {"url": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml", "source": "The New York Times"},
        "sports": {"url": "https://www.espn.com/espn/rss/news", "source": "ESPN News"},
        "entertainment": {"url": "https://rss.nytimes.com/services/xml/rss/nyt/Arts.xml", "source": "The New York Times"}
    }
}
