import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the Flask application"""
    
    # Flask settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # API Keys
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    GNEWS_API_KEY = os.getenv('GNEWS_API_KEY')
    
    # News sources configuration
    DEFAULT_SOURCES = {
        'newsapi': True if NEWS_API_KEY else False,
        'gnews': True if GNEWS_API_KEY else False,
        'hackernews': True,
        'rss_feeds': True
    }
    
    # RSS Feed URLs
    RSS_FEEDS = {
        'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
        'cnn': 'http://rss.cnn.com/rss/edition.rss',
        'reuters': 'http://feeds.reuters.com/reuters/topNews',
        'techcrunch': 'https://techcrunch.com/feed/',
        'the_verge': 'https://www.theverge.com/rss/index.xml',
        'ars_technica': 'http://feeds.arstechnica.com/arstechnica/index',
        'wired': 'https://www.wired.com/feed/rss',
        'npr': 'https://feeds.npr.org/1001/rss.xml',
        'guardian': 'https://www.theguardian.com/world/rss',
        'nyt': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'
    }
    
    # News categories
    CATEGORIES = [
        'general', 'business', 'entertainment', 'health',
        'science', 'sports', 'technology', 'politics'
    ]
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE = 60
    
    # Cache settings
    CACHE_TIMEOUT = 300  # 5 minutes
    
    # Pagination
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
