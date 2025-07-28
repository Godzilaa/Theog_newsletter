import os
import requests
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import newspaper with fallback configuration
try:
    from newspaper import Article
    NEWSPAPER_AVAILABLE = True
except ImportError:
    NEWSPAPER_AVAILABLE = False
    logger.warning("Newspaper3k not available. Article extraction will be limited.")

class NewsAPI:
    """News API integration for fetching news articles"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2"
    
    def get_headlines(self, category: str = "general", country: str = "us", page_size: int = 20) -> List[Dict]:
        """Fetch top headlines from NewsAPI"""
        try:
            url = f"{self.base_url}/top-headlines"
            params = {
                'apiKey': self.api_key,
                'category': category,
                'country': country,
                'pageSize': page_size
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            articles = []
            
            for article in data.get('articles', []):
                if article.get('title') and article.get('url'):
                    articles.append({
                        'title': article['title'],
                        'url': article['url'],
                        'description': article.get('description', ''),
                        'published_at': article.get('publishedAt'),
                        'source': article.get('source', {}).get('name', 'NewsAPI'),
                        'image_url': article.get('urlToImage'),
                        'author': article.get('author')
                    })
            
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching NewsAPI headlines: {e}")
            return []

class GNewsAPI:
    """GNews API integration for fetching news articles"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://gnews.io/api/v4"
    
    def get_headlines(self, category: str = "general", lang: str = "en", max_articles: int = 20) -> List[Dict]:
        """Fetch headlines from GNews API"""
        try:
            url = f"{self.base_url}/top-headlines"
            params = {
                'apikey': self.api_key,
                'category': category,
                'lang': lang,
                'max': max_articles
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            articles = []
            
            for article in data.get('articles', []):
                if article.get('title') and article.get('url'):
                    articles.append({
                        'title': article['title'],
                        'url': article['url'],
                        'description': article.get('description', ''),
                        'published_at': article.get('publishedAt'),
                        'source': article.get('source', {}).get('name', 'GNews'),
                        'image_url': article.get('image'),
                        'author': None
                    })
            
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching GNews headlines: {e}")
            return []

class HackerNewsAPI:
    """Hacker News API integration"""
    
    def __init__(self):
        self.base_url = "https://hacker-news.firebaseio.com/v0"
    
    def get_top_stories(self, limit: int = 20) -> List[Dict]:
        """Fetch top stories from Hacker News"""
        try:
            # Get top story IDs
            top_stories_url = f"{self.base_url}/topstories.json"
            response = requests.get(top_stories_url, timeout=10)
            response.raise_for_status()
            
            story_ids = response.json()[:limit]
            articles = []
            
            for story_id in story_ids:
                try:
                    story_url = f"{self.base_url}/item/{story_id}.json"
                    story_response = requests.get(story_url, timeout=5)
                    story_response.raise_for_status()
                    
                    story = story_response.json()
                    
                    if story.get('title') and story.get('url'):
                        articles.append({
                            'title': story['title'],
                            'url': story['url'],
                            'description': story.get('text', ''),
                            'published_at': datetime.fromtimestamp(story.get('time', 0)).isoformat() if story.get('time') else None,
                            'source': 'Hacker News',
                            'image_url': None,
                            'author': story.get('by'),
                            'score': story.get('score', 0),
                            'comments': story.get('descendants', 0)
                        })
                except Exception as e:
                    logger.warning(f"Error fetching HN story {story_id}: {e}")
                    continue
            
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching Hacker News stories: {e}")
            return []

class RSSFeedScraper:
    """RSS feed scraper for various news sources"""
    
    def __init__(self):
        self.feeds = {
            'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'reuters': 'http://feeds.reuters.com/reuters/topNews',
            'techcrunch': 'https://techcrunch.com/feed/',
            'the_verge': 'https://www.theverge.com/rss/index.xml',
            'ars_technica': 'http://feeds.arstechnica.com/arstechnica/index',
            'wired': 'https://www.wired.com/feed/rss'
        }
    
    def get_feed_articles(self, feed_name: str, limit: int = 10) -> List[Dict]:
        """Fetch articles from a specific RSS feed"""
        try:
            if feed_name not in self.feeds:
                logger.error(f"Unknown feed: {feed_name}")
                return []
            
            feed_url = self.feeds[feed_name]
            feed = feedparser.parse(feed_url)
            
            articles = []
            for entry in feed.entries[:limit]:
                articles.append({
                    'title': entry.get('title', ''),
                    'url': entry.get('link', ''),
                    'description': entry.get('summary', ''),
                    'published_at': entry.get('published'),
                    'source': feed_name.replace('_', ' ').title(),
                    'image_url': None,
                    'author': entry.get('author')
                })
            
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching RSS feed {feed_name}: {e}")
            return []
    
    def get_all_feeds(self, limit_per_feed: int = 5) -> List[Dict]:
        """Fetch articles from all RSS feeds"""
        all_articles = []
        for feed_name in self.feeds:
            articles = self.get_feed_articles(feed_name, limit_per_feed)
            all_articles.extend(articles)
        return all_articles

class Newspaper3kScraper:
    """Newspaper3k scraper for extracting full article content"""
    
    @staticmethod
    def extract_article_content(url: str) -> Dict:
        """Extract full article content from URL"""
        if not NEWSPAPER_AVAILABLE:
            logger.warning("Newspaper3k not available. Using basic content extraction.")
            return Newspaper3kScraper._basic_content_extraction(url)
        
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            
            return {
                'title': article.title,
                'text': article.text,
                'summary': article.summary,
                'keywords': article.keywords,
                'authors': article.authors,
                'publish_date': article.publish_date.isoformat() if article.publish_date else None,
                'top_image': article.top_image,
                'url': url
            }
            
        except Exception as e:
            logger.error(f"Error extracting article content from {url}: {e}")
            return Newspaper3kScraper._basic_content_extraction(url)
    
    @staticmethod
    def _basic_content_extraction(url: str) -> Dict:
        """Basic content extraction using requests and BeautifulSoup"""
        try:
            import requests
            from bs4 import BeautifulSoup
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else ""
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc.get('content', '') if meta_desc else ""
            
            # Extract main content (basic approach)
            content_selectors = ['article', '.content', '.post-content', '.entry-content', 'main']
            text = ""
            for selector in content_selectors:
                content_div = soup.select_one(selector)
                if content_div:
                    text = content_div.get_text().strip()
                    break
            
            if not text:
                # Fallback: get all paragraph text
                paragraphs = soup.find_all('p')
                text = ' '.join([p.get_text().strip() for p in paragraphs])
            
            return {
                'title': title,
                'text': text[:1000] + '...' if len(text) > 1000 else text,
                'summary': description,
                'keywords': [],
                'authors': [],
                'publish_date': None,
                'top_image': None,
                'url': url
            }
            
        except Exception as e:
            logger.error(f"Error in basic content extraction from {url}: {e}")
            return {
                'title': '',
                'text': '',
                'summary': '',
                'keywords': [],
                'authors': [],
                'publish_date': None,
                'top_image': None,
                'url': url
            }
    
    @staticmethod
    def get_source_articles(source_url: str, limit: int = 10) -> List[Dict]:
        """Get articles from a news source homepage"""
        if not NEWSPAPER_AVAILABLE:
            logger.warning("Newspaper3k not available. Cannot scrape source articles.")
            return []
        
        try:
            from newspaper import build
            
            source = build(source_url, memoize_articles=False)
            articles = []
            
            for article in source.articles[:limit]:
                try:
                    article.download()
                    article.parse()
                    
                    if article.title and article.url:
                        articles.append({
                            'title': article.title,
                            'url': article.url,
                            'description': article.text[:200] + '...' if len(article.text) > 200 else article.text,
                            'published_at': article.publish_date.isoformat() if article.publish_date else None,
                            'source': source_url,
                            'image_url': article.top_image,
                            'author': ', '.join(article.authors) if article.authors else None
                        })
                except Exception as e:
                    logger.warning(f"Error processing article {article.url}: {e}")
                    continue
            
            return articles
            
        except Exception as e:
            logger.error(f"Error scraping source {source_url}: {e}")
            return []

class NewsAggregator:
    """Main news aggregator that combines all sources"""
    
    def __init__(self, news_api_key: str = None, gnews_api_key: str = None):
        self.news_api = NewsAPI(news_api_key) if news_api_key else None
        self.gnews_api = GNewsAPI(gnews_api_key) if gnews_api_key else None
        self.hacker_news = HackerNewsAPI()
        self.rss_scraper = RSSFeedScraper()
        self.newspaper_scraper = Newspaper3kScraper()
    
    def get_all_news(self, limit_per_source: int = 10) -> Dict[str, List[Dict]]:
        """Fetch news from all available sources"""
        news_data = {}
        
        # NewsAPI
        if self.news_api:
            news_data['newsapi'] = self.news_api.get_headlines(page_size=limit_per_source)
        
        # GNews
        if self.gnews_api:
            news_data['gnews'] = self.gnews_api.get_headlines(max_articles=limit_per_source)
        
        # Hacker News
        news_data['hackernews'] = self.hacker_news.get_top_stories(limit=limit_per_source)
        
        # RSS Feeds
        news_data['rss_feeds'] = self.rss_scraper.get_all_feeds(limit_per_feed=5)
        
        return news_data
    
    def get_news_by_category(self, category: str, limit: int = 20) -> List[Dict]:
        """Get news articles by category from multiple sources"""
        all_articles = []
        
        # NewsAPI by category
        if self.news_api:
            articles = self.news_api.get_headlines(category=category, page_size=limit//2)
            all_articles.extend(articles)
        
        # GNews by category
        if self.gnews_api:
            articles = self.gnews_api.get_headlines(category=category, max_articles=limit//2)
            all_articles.extend(articles)
        
        # Sort by published date
        all_articles.sort(key=lambda x: x.get('published_at', ''), reverse=True)
        return all_articles[:limit]
    
    def search_news(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for news articles across sources"""
        # This could be expanded to include search functionality
        # For now, we'll filter existing articles by title/description
        all_news = self.get_all_news(limit_per_source=50)
        matching_articles = []
        
        for source, articles in all_news.items():
            for article in articles:
                title = article.get('title', '').lower()
                description = article.get('description', '').lower()
                if query.lower() in title or query.lower() in description:
                    matching_articles.append(article)
        
        return matching_articles[:limit]
