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
    "CN": {"zh": "中国 🇨🇳", "en": "China"},
    "JP": {"zh": "日本 🇯🇵", "en": "Japan"},
    "US": {"zh": "美国 🇺🇸", "en": "United States"},
    "UK": {"zh": "英国 🇬🇧", "en": "United Kingdom"}
}

# RSS Feed definitions grouped by Region and Category
NEWS_FEEDS = {
    "CN": {
        "top": {"url": "https://www.zaobao.com/realtime/china/rss", "source": "Lianhe Zaobao (China)"},
        "society": {"url": "https://www.zaobao.com/realtime/world/rss", "source": "Lianhe Zaobao (World)"},
        "business": {"url": "http://www.ftchinese.com/rss/news", "source": "FT Chinese"},
        "technology": {"url": "https://www.ithome.com/rss/", "source": "IT Home"},
        "sports": {"url": "https://sports.sina.com.cn/rss/sports_global.xml", "source": "Sina Sports"},
        "entertainment": {"url": "https://ent.sina.com.cn/rss/news/global.xml", "source": "Sina Entertainment"}
    },
    "JP": {
        "top": [
            {"url": "https://news.yahoo.co.jp/rss/topics/top-picks.xml", "source": "Yahoo! News Japan"},
            {"url": "https://www.nhk.or.jp/rss/news/cat0.xml", "source": "NHK News"}
        ],
        "society": [
            {"url": "https://news.yahoo.co.jp/rss/topics/domestic.xml", "source": "Yahoo! News Japan"},
            {"url": "https://www.nhk.or.jp/rss/news/cat1.xml", "source": "NHK News"}
        ],
        "business": [
            {"url": "https://news.yahoo.co.jp/rss/topics/business.xml", "source": "Yahoo! News Japan"},
            {"url": "https://www.nhk.or.jp/rss/news/cat4.xml", "source": "NHK News"}
        ],
        "technology": [
            {"url": "https://news.yahoo.co.jp/rss/topics/it.xml", "source": "Yahoo! News Japan"},
            {"url": "https://www.nhk.or.jp/rss/news/cat3.xml", "source": "NHK News"}
        ],
        "sports": [
            {"url": "https://news.yahoo.co.jp/rss/topics/sports.xml", "source": "Yahoo! News Japan"},
            {"url": "https://www.nhk.or.jp/rss/news/cat7.xml", "source": "NHK News"}
        ],
        "entertainment": [
            {"url": "https://news.yahoo.co.jp/rss/topics/entertainment.xml", "source": "Yahoo! News Japan"},
            {"url": "https://www.nhk.or.jp/rss/news/cat2.xml", "source": "NHK News"}
        ]
    },
    "US": {
        "top": [
            {"url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml", "source": "The New York Times"},
            {"url": "http://rss.cnn.com/rss/edition.rss", "source": "CNN"}
        ],
        "society": [
            {"url": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml", "source": "The New York Times"},
            {"url": "http://rss.cnn.com/rss/edition_world.rss", "source": "CNN"}
        ],
        "business": [
            {"url": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml", "source": "The New York Times"},
            {"url": "http://rss.cnn.com/rss/money_latest.rss", "source": "CNN"}
        ],
        "technology": [
            {"url": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml", "source": "The New York Times"},
            {"url": "http://rss.cnn.com/rss/edition_technology.rss", "source": "CNN"}
        ],
        "sports": [
            {"url": "https://www.espn.com/espn/rss/news", "source": "ESPN News"},
            {"url": "http://rss.cnn.com/rss/edition_motorsport.rss", "source": "CNN"}
        ],
        "entertainment": [
            {"url": "https://rss.nytimes.com/services/xml/rss/nyt/Arts.xml", "source": "The New York Times"},
            {"url": "http://rss.cnn.com/rss/edition_entertainment.rss", "source": "CNN"}
        ]
    },
    "UK": {
        "top": {"url": "http://feeds.bbci.co.uk/news/rss.xml", "source": "BBC News"},
        "society": {"url": "http://feeds.bbci.co.uk/news/world/rss.xml", "source": "BBC News"},
        "business": {"url": "http://feeds.bbci.co.uk/news/business/rss.xml", "source": "BBC News"},
        "technology": {"url": "http://feeds.bbci.co.uk/news/technology/rss.xml", "source": "BBC News"},
        "sports": {"url": "http://feeds.bbci.co.uk/sport/rss.xml", "source": "BBC Sport"},
        "entertainment": {"url": "http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml", "source": "BBC News"}
    }
}
