from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
import requests
from datetime import datetime

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Newsletter Backend API is running',
        'available_endpoints': [
            '/api/hackernews',
            '/api/newsapi',
            '/api/categories'
        ],
        'api_keys_configured': {
            'newsapi': bool(os.getenv('NEWS_API_KEY'))
        },
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

@app.route('/api/hackernews', methods=['GET'])
def get_hackernews():
    """Get Hacker News stories"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        # Get top story IDs
        response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10)
        response.raise_for_status()
        
        story_ids = response.json()[:min(limit, 15)]
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
                        'description': story.get('text', '')[:200] + '...' if story.get('text') else 'No description available',
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

@app.route('/api/newsapi', methods=['GET'])
def get_newsapi():
    """Get NewsAPI headlines"""
    if not os.getenv('NEWS_API_KEY'):
        return jsonify({
            'status': 'error',
            'message': 'NewsAPI key not configured. Please set NEWS_API_KEY in .env file.'
        }), 400
    
    try:
        category = request.args.get('category', 'general')
        limit = request.args.get('limit', 10, type=int)
        
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            'apiKey': os.getenv('NEWS_API_KEY'),
            'category': category,
            'country': 'us',
            'pageSize': min(limit, 50)
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
                    'description': article.get('description', 'No description available'),
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
    print("🚀 Starting Newsletter Backend API")
    print("=" * 40)
    
    if os.getenv('NEWS_API_KEY'):
        print("✅ NewsAPI key configured")
    else:
        print("⚠️  NewsAPI key not found - add it to .env file")
        print("   Get a free key from: https://newsapi.org/")
    
    print("\n📖 API will be available at: http://localhost:5000")
    print("🔗 Endpoints:")
    print("   - GET /api/hackernews?limit=10")
    print("   - GET /api/newsapi?category=technology&limit=10")
    print("   - GET /api/categories")
    print("\n" + "=" * 40)
    
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug)