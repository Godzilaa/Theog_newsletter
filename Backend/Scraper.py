from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import logging
from datetime import datetime

# Try to import CORS, but continue without it if not available
try:
    from flask_cors import CORS
    CORS_AVAILABLE = True
except ImportError:
    CORS_AVAILABLE = False
    print("Warning: Flask-CORS not available. Install with: pip install flask-cors")

# Try to import news sources with fallback handling
try:
    from news_sources import NewsAggregator, Newspaper3kScraper
    NEWS_SOURCES_AVAILABLE = True
except ImportError as e:
    NEWS_SOURCES_AVAILABLE = False
    print(f"Info: Advanced news sources not available. Using basic functionality.")
    print(f"To install full dependencies, run: install-windows.bat")

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Enable CORS if available
if CORS_AVAILABLE:
    CORS(app)
else:
    # Manually add CORS headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

# Initialize news aggregator if dependencies are available
if NEWS_SOURCES_AVAILABLE:
    news_aggregator = NewsAggregator(
        news_api_key=os.getenv('NEWS_API_KEY'),
        gnews_api_key=os.getenv('GNEWS_API_KEY')
    )
else:
    news_aggregator = None

@app.route('/')
def health_check():
    """Health check endpoint"""
    dependency_status = {
        'news_sources': NEWS_SOURCES_AVAILABLE,
        'flask': True,
        'requests': True,
        'python_dotenv': True
    }
    
    # Available endpoints based on current setup
    available_endpoints = [
        '/api/status',
        '/api/categories',
        '/api/sources'
    ]
    
    if NEWS_SOURCES_AVAILABLE:
        available_endpoints.extend([
            '/api/news',
            '/api/news/category/{category}',
            '/api/news/search?q={query}',
            '/api/news/hackernews',
            '/api/news/rss/{feed_name}',
            '/api/article/extract'
        ])
    else:
        available_endpoints.extend([
            '/api/basic/hackernews',
            '/api/basic/newsapi' if os.getenv('NEWS_API_KEY') else None
        ])
    
    # Remove None values
    available_endpoints = [ep for ep in available_endpoints if ep is not None]
    
    return jsonify({
        'status': 'healthy',
        'message': 'Newsletter Backend API is running',
        'version': 'full' if NEWS_SOURCES_AVAILABLE else 'basic',
        'dependencies': dependency_status,
        'available_endpoints': available_endpoints,
        'api_keys_configured': {
            'newsapi': bool(os.getenv('NEWS_API_KEY')),
            'gnews': bool(os.getenv('GNEWS_API_KEY'))
        },
        'setup_notes': {
            'install_dependencies': 'Run install-windows.bat to install full dependencies' if not NEWS_SOURCES_AVAILABLE else 'All dependencies installed',
            'configure_api_keys': 'Edit .env file to add API keys for more news sources'
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/status', methods=['GET'])
def get_system_status():
    """Get detailed system status"""
    try:
        # Try importing various components
        dependencies = {}
        
        try:
            import flask
            dependencies['flask'] = flask.__version__
        except ImportError:
            dependencies['flask'] = 'Not available'
        
        try:
            import requests
            dependencies['requests'] = requests.__version__
        except ImportError:
            dependencies['requests'] = 'Not available'
        
        try:
            import feedparser
            dependencies['feedparser'] = feedparser.__version__
        except ImportError:
            dependencies['feedparser'] = 'Not available'
        
        try:
            import newspaper
            dependencies['newspaper3k'] = newspaper.__version__
        except ImportError:
            dependencies['newspaper3k'] = 'Not available'
        
        try:
            import bs4
            dependencies['beautifulsoup4'] = bs4.__version__
        except ImportError:
            dependencies['beautifulsoup4'] = 'Not available'
        
        return jsonify({
            'status': 'success',
            'system_ready': NEWS_SOURCES_AVAILABLE,
            'dependencies': dependencies,
            'environment': {
                'python_version': os.sys.version,
                'flask_env': os.getenv('FLASK_ENV', 'development'),
                'flask_debug': os.getenv('FLASK_DEBUG', 'True')
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/news', methods=['GET'])
def get_all_news():
    """Get news from all sources"""
    if not NEWS_SOURCES_AVAILABLE:
        return jsonify({
            'status': 'error',
            'message': 'News sources not available. Please install required dependencies.'
        }), 503
    
    try:
        limit = request.args.get('limit', 10, type=int)
        news_data = news_aggregator.get_all_news(limit_per_source=limit)
        
        return jsonify({
            'status': 'success',
            'data': news_data,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error fetching all news: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/news/category/<category>', methods=['GET'])
def get_news_by_category(category):
    """Get news by category"""
    if not NEWS_SOURCES_AVAILABLE:
        return jsonify({
            'status': 'error',
            'message': 'News sources not available. Please install required dependencies or use basic endpoints.'
        }), 503
    
    try:
        limit = request.args.get('limit', 20, type=int)
        articles = news_aggregator.get_news_by_category(category, limit)
        
        return jsonify({
            'status': 'success',
            'category': category,
            'data': articles,
            'count': len(articles),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error fetching news by category {category}: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/news/search', methods=['GET'])
def search_news():
    """Search news articles"""
    if not NEWS_SOURCES_AVAILABLE:
        return jsonify({
            'status': 'error',
            'message': 'News sources not available. Please install required dependencies.'
        }), 503
    
    try:
        query = request.args.get('q', '')
        limit = request.args.get('limit', 20, type=int)
        
        if not query:
            return jsonify({
                'status': 'error',
                'message': 'Query parameter "q" is required'
            }), 400
        
        articles = news_aggregator.search_news(query, limit)
        
        return jsonify({
            'status': 'success',
            'query': query,
            'data': articles,
            'count': len(articles),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error searching news for query {query}: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/news/hackernews', methods=['GET'])
def get_hacker_news():
    """Get Hacker News stories"""
    if not NEWS_SOURCES_AVAILABLE:
        return jsonify({
            'status': 'error',
            'message': 'News sources not available. Use /api/basic/hackernews for basic functionality.'
        }), 503
    
    try:
        limit = request.args.get('limit', 20, type=int)
        articles = news_aggregator.hacker_news.get_top_stories(limit)
        
        return jsonify({
            'status': 'success',
            'source': 'Hacker News',
            'data': articles,
            'count': len(articles),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error fetching Hacker News: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/news/rss/<feed_name>', methods=['GET'])
def get_rss_feed(feed_name):
    """Get articles from specific RSS feed"""
    try:
        limit = request.args.get('limit', 10, type=int)
        articles = news_aggregator.rss_scraper.get_feed_articles(feed_name, limit)
        
        return jsonify({
            'status': 'success',
            'feed': feed_name,
            'data': articles,
            'count': len(articles),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error fetching RSS feed {feed_name}: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/news/rss', methods=['GET'])
def get_all_rss_feeds():
    """Get all available RSS feeds"""
    try:
        feeds = list(news_aggregator.rss_scraper.feeds.keys())
        return jsonify({
            'status': 'success',
            'available_feeds': feeds,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error getting RSS feeds: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/article/extract', methods=['POST'])
def extract_article():
    """Extract full article content from URL"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({
                'status': 'error',
                'message': 'URL is required'
            }), 400
        
        article_content = Newspaper3kScraper.extract_article_content(url)
        
        return jsonify({
            'status': 'success',
            'data': article_content,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error extracting article from {url}: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/sources', methods=['GET'])
def get_available_sources():
    """Get all available news sources"""
    if not NEWS_SOURCES_AVAILABLE:
        # Provide basic sources when full dependencies aren't available
        sources = {
            'api_sources': [],
            'rss_feeds': [],
            'special_sources': ['hackernews'],
            'note': 'Limited functionality - install full dependencies for more sources'
        }
        
        if os.getenv('NEWS_API_KEY'):
            sources['api_sources'].append('newsapi')
        
        return jsonify({
            'status': 'success',
            'data': sources,
            'timestamp': datetime.now().isoformat()
        })
    
    # Full functionality when dependencies are available
    sources = {
        'api_sources': [],
        'rss_feeds': list(news_aggregator.rss_scraper.feeds.keys()),
        'special_sources': ['hackernews']
    }
    
    if news_aggregator.news_api:
        sources['api_sources'].append('newsapi')
    if news_aggregator.gnews_api:
        sources['api_sources'].append('gnews')
    
    return jsonify({
        'status': 'success',
        'data': sources,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get available news categories"""
    categories = [
        'general', 'business', 'entertainment', 'health',
        'science', 'sports', 'technology'
    ]
    
    return jsonify({
        'status': 'success',
        'data': categories,
        'timestamp': datetime.now().isoformat()
    })

# Basic endpoints that work without full dependencies
@app.route('/api/basic/hackernews', methods=['GET'])
def get_basic_hackernews():
    """Get Hacker News stories using basic requests"""
    try:
        import requests
        limit = request.args.get('limit', 20, type=int)
        
        # Get top story IDs
        response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10)
        response.raise_for_status()
        
        story_ids = response.json()[:min(limit, 10)]  # Limit to avoid timeouts
        articles = []
        
        for story_id in story_ids:
            try:
                story_response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json", timeout=5)
                story_response.raise_for_status()
                
                story = story_response.json()
                
                if story.get('title'):
                    articles.append({
                        'title': story['title'],
                        'url': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                        'description': story.get('text', '')[:200] + '...' if story.get('text') else '',
                        'published_at': datetime.fromtimestamp(story.get('time', 0)).isoformat() if story.get('time') else None,
                        'source': 'Hacker News',
                        'score': story.get('score', 0),
                        'comments': story.get('descendants', 0)
                    })
            except Exception as e:
                logger.warning(f"Error fetching HN story {story_id}: {e}")
                continue
        
        return jsonify({
            'status': 'success',
            'source': 'Hacker News',
            'data': articles,
            'count': len(articles),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error fetching Hacker News: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/basic/newsapi', methods=['GET'])
def get_basic_newsapi():
    """Get NewsAPI headlines using basic requests"""
    if not os.getenv('NEWS_API_KEY'):
        return jsonify({
            'status': 'error',
            'message': 'NewsAPI key not configured. Please set NEWS_API_KEY in .env file.'
        }), 400
    
    try:
        import requests
        category = request.args.get('category', 'general')
        limit = request.args.get('limit', 20, type=int)
        
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            'apiKey': os.getenv('NEWS_API_KEY'),
            'category': category,
            'country': 'us',
            'pageSize': min(limit, 100)
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
        
        return jsonify({
            'status': 'success',
            'source': 'NewsAPI',
            'category': category,
            'data': articles,
            'count': len(articles),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error fetching NewsAPI: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    # Check if API keys are configured
    if not os.getenv('NEWS_API_KEY'):
        logger.warning("NEWS_API_KEY not found in environment variables")
    if not os.getenv('GNEWS_API_KEY'):
        logger.warning("GNEWS_API_KEY not found in environment variables")
    
    # Run the Flask app
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug)