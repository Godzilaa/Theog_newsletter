from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
import requests
from datetime import datetime
import gradio as gr

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

class SimpleNewsAPI:
    """Simple news aggregator using only requests"""
    
    def __init__(self, news_api_key=None, gnews_api_key=None):
        self.news_api_key = news_api_key
        self.gnews_api_key = gnews_api_key
    
    def get_hacker_news(self, limit=20):
        """Get Hacker News stories"""
        try:
            # Get top story IDs
            response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10)
            response.raise_for_status()
            
            story_ids = response.json()[:limit]
            articles = []
            
            for story_id in story_ids[:10]:  # Limit to avoid timeouts
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
            
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching Hacker News: {e}")
            return []
    
    def get_newsapi_headlines(self, category='general', limit=20):
        """Get headlines from NewsAPI"""
        if not self.news_api_key:
            return []
        
        try:
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                'apiKey': self.news_api_key,
                'category': category,
                'country': 'us',
                'pageSize': limit
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

# Initialize simple news aggregator
news_api = SimpleNewsAPI(
    news_api_key=os.getenv('NEWS_API_KEY'),
    gnews_api_key=os.getenv('GNEWS_API_KEY')
)

@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Newsletter Backend API is running (Basic Version)',
        'available_endpoints': [
            '/api/news/hackernews',
            '/api/news/newsapi' if os.getenv('NEWS_API_KEY') else None,
            '/api/status'
        ],
        'api_keys_configured': {
            'newsapi': bool(os.getenv('NEWS_API_KEY')),
            'gnews': bool(os.getenv('GNEWS_API_KEY'))
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/status')
def get_status():
    """Get system status"""
    return jsonify({
        'status': 'success',
        'version': 'basic',
        'dependencies_installed': {
            'flask': True,
            'requests': True,
            'python-dotenv': True
        },
        'api_keys': {
            'newsapi': bool(os.getenv('NEWS_API_KEY')),
            'gnews': bool(os.getenv('GNEWS_API_KEY'))
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/news/hackernews')
def get_hackernews():
    """Get Hacker News stories"""
    try:
        limit = request.args.get('limit', 20, type=int)
        articles = news_api.get_hacker_news(limit)
        
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

@app.route('/api/news/newsapi')
def get_newsapi():
    """Get NewsAPI headlines"""
    if not os.getenv('NEWS_API_KEY'):
        return jsonify({
            'status': 'error',
            'message': 'NewsAPI key not configured'
        }), 400
    
    try:
        category = request.args.get('category', 'general')
        limit = request.args.get('limit', 20, type=int)
        articles = news_api.get_newsapi_headlines(category, limit)
        
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

@app.route('/api/categories')
def get_categories():
    """Get available categories"""
    return jsonify({
        'status': 'success',
        'data': ['general', 'business', 'entertainment', 'health', 'science', 'sports', 'technology'],
        'timestamp': datetime.now().isoformat()
    })

with gr.Blocks() as demo:
    # Your Gradio components
    demo.load(...)  # <-- Only call load() inside this context

demo.launch()

if __name__ == '__main__':
    print("🚀 Starting Newsletter Backend (Basic Version)")
    print("=" * 50)
    
    if os.getenv('NEWS_API_KEY'):
        print("✅ NewsAPI key configured")
    else:
        print("⚠️  NewsAPI key not found - some features will be limited")
        print("   Get a free key from: https://newsapi.org/")
    
    if os.getenv('GNEWS_API_KEY'):
        print("✅ GNews API key configured")
    else:
        print("⚠️  GNews API key not found")
        print("   Get a free key from: https://gnews.io/")
    
    print("\n📖 API will be available at: http://localhost:5000")
    print("🔍 Available endpoints:")
    print("   - GET / (health check)")
    print("   - GET /api/status")
    print("   - GET /api/news/hackernews")
    if os.getenv('NEWS_API_KEY'):
        print("   - GET /api/news/newsapi?category=technology")
    print("   - GET /api/categories")
    print("\n" + "=" * 50)
    
    # Run the Flask app
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
