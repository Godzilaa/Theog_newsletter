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
            '/api/newsapi', 
            '/api/categories',
            '/api/generate-newsletter',
            '/api/newsletters',
            '/api/newsletters/<id>',
            '/api/scheduler/start',
            '/api/scheduler/stop',
            '/api/scheduler/status'
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

# Global variables for newsletter storage and scheduling
import threading
import schedule
import time
import json
from pathlib import Path

newsletter_storage = []
scheduler_running = False
scheduler_thread = None

def save_newsletter(content, metadata):
    """Save generated newsletter to storage"""
    global newsletter_storage
    
    newsletter_entry = {
        'id': len(newsletter_storage) + 1,
        'content': content,
        'metadata': metadata,
        'timestamp': datetime.now().isoformat(),
        'status': 'generated'
    }
    
    newsletter_storage.append(newsletter_entry)
    
    # Also save to file
    newsletters_dir = Path(__file__).parent / "generated_newsletters"
    newsletters_dir.mkdir(exist_ok=True)
    
    filename = f"newsletter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = newsletters_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(newsletter_entry, f, indent=2, ensure_ascii=False)
    
    # Keep only last 50 newsletters in memory
    if len(newsletter_storage) > 50:
        newsletter_storage = newsletter_storage[-50:]
    
    return newsletter_entry

def generate_newsletter_content(categories=None):
    """Generate newsletter content using CrewAI agents"""
    if categories is None:
        categories = ['technology', 'business', 'science', 'general']
    
    try:
        import sys
        from pathlib import Path
        
        # Add newsagent to path
        newsagent_src = Path(__file__).parent / "newsagent" / "src"
        if str(newsagent_src) not in sys.path:
            sys.path.insert(0, str(newsagent_src))
        
        from newsagent.crew import Newsagent
        
        # Prepare inputs
        inputs = {
            'categories': ', '.join(categories),
            'current_date': datetime.now().strftime('%Y-%m-%d'),
            'current_time': datetime.now().strftime('%H:%M:%S')
        }
        
        # Create and run the crew
        logger.info(f"Generating newsletter for categories: {categories}")
        crew = Newsagent().crew()
        result = crew.kickoff(inputs=inputs)
        
        # Extract content from result
        content = str(result) if result else "Newsletter generation completed"
        
        # Create metadata
        metadata = {
            'categories': categories,
            'generation_time': datetime.now().isoformat(),
            'word_count': len(content.split()),
            'char_count': len(content)
        }
        
        # Save to storage
        newsletter = save_newsletter(content, metadata)
        logger.info(f"Newsletter #{newsletter['id']} generated and saved")
        
        return newsletter
        
    except Exception as e:
        logger.error(f"Error generating newsletter: {e}")
        raise

def newsletter_scheduler_job():
    """Scheduled job to generate newsletters"""
    try:
        logger.info("🕐 Scheduled newsletter generation started")
        newsletter = generate_newsletter_content()
        logger.info(f"✅ Scheduled newsletter #{newsletter['id']} generated successfully")
    except Exception as e:
        logger.error(f"❌ Scheduled newsletter generation failed: {e}")

def start_newsletter_scheduler():
    """Start the newsletter scheduler"""
    global scheduler_running, scheduler_thread
    
    if scheduler_running:
        return {"status": "already_running", "message": "Scheduler is already running"}
    
    # Schedule newsletter generation every minute
    schedule.every(1).minutes.do(newsletter_scheduler_job)
    
    def run_scheduler():
        global scheduler_running
        scheduler_running = True
        logger.info("📅 Newsletter scheduler started - generating every minute")
        
        try:
            while scheduler_running:
                schedule.run_pending()
                time.sleep(1)
        except Exception as e:
            logger.error(f"Scheduler error: {e}")
        finally:
            scheduler_running = False
            logger.info("📅 Newsletter scheduler stopped")
    
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    return {"status": "started", "message": "Newsletter scheduler started - generating every minute"}

def stop_newsletter_scheduler():
    """Stop the newsletter scheduler"""
    global scheduler_running
    
    if not scheduler_running:
        return {"status": "not_running", "message": "Scheduler is not running"}
    
    scheduler_running = False
    schedule.clear()
    logger.info("📅 Newsletter scheduler stopped")
    
    return {"status": "stopped", "message": "Newsletter scheduler stopped"}

@app.route('/api/generate-newsletter', methods=['POST'])
def generate_newsletter():
    """Trigger newsletter generation manually"""
    try:
        # Get parameters from request
        data = request.get_json() if request.is_json else {}
        categories = data.get('categories', ['technology', 'business', 'science', 'general'])
        
        # Generate newsletter
        newsletter = generate_newsletter_content(categories)
        
        return jsonify({
            'status': 'success',
            'message': 'Newsletter generated successfully',
            'newsletter_id': newsletter['id'],
            'categories': categories,
            'metadata': newsletter['metadata'],
            'content_preview': newsletter['content'][:500] + "..." if len(newsletter['content']) > 500 else newsletter['content'],
            'timestamp': newsletter['timestamp']
        })
        
    except Exception as e:
        logger.error(f"Error generating newsletter: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/newsletters', methods=['GET'])
def get_newsletters():
    """Get list of generated newsletters"""
    try:
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Get newsletters with pagination
        newsletters = newsletter_storage[offset:offset + limit]
        
        # Return summary without full content
        newsletters_summary = []
        for newsletter in newsletters:
            newsletters_summary.append({
                'id': newsletter['id'],
                'timestamp': newsletter['timestamp'],
                'metadata': newsletter['metadata'],
                'content_preview': newsletter['content'][:200] + "..." if len(newsletter['content']) > 200 else newsletter['content'],
                'status': newsletter['status']
            })
        
        return jsonify({
            'status': 'success',
            'data': newsletters_summary,
            'total_count': len(newsletter_storage),
            'limit': limit,
            'offset': offset,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error fetching newsletters: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/newsletters/<int:newsletter_id>', methods=['GET'])
def get_newsletter(newsletter_id):
    """Get specific newsletter by ID"""
    try:
        # Find newsletter by ID
        newsletter = None
        for n in newsletter_storage:
            if n['id'] == newsletter_id:
                newsletter = n
                break
        
        if not newsletter:
            return jsonify({
                'status': 'error',
                'message': f'Newsletter with ID {newsletter_id} not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': newsletter,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error fetching newsletter {newsletter_id}: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/scheduler/start', methods=['POST'])
def start_scheduler():
    """Start automated newsletter generation"""
    try:
        result = start_newsletter_scheduler()
        return jsonify({
            'status': 'success',
            **result,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error starting scheduler: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/scheduler/stop', methods=['POST'])
def stop_scheduler():
    """Stop automated newsletter generation"""
    try:
        result = stop_newsletter_scheduler()
        return jsonify({
            'status': 'success',
            **result,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error stopping scheduler: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/scheduler/status', methods=['GET'])
def scheduler_status():
    """Get scheduler status"""
    try:
        return jsonify({
            'status': 'success',
            'scheduler_running': scheduler_running,
            'total_newsletters': len(newsletter_storage),
            'last_newsletter': newsletter_storage[-1]['timestamp'] if newsletter_storage else None,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting scheduler status: {e}")
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
    print("   - GET /api/newsapi?category=technology&limit=10")
    print("   - GET /api/categories")
    print("   - POST /api/generate-newsletter")
    print("   - GET /api/newsletters?limit=10&offset=0")
    print("   - GET /api/newsletters/<id>")
    print("   - POST /api/scheduler/start")
    print("   - POST /api/scheduler/stop")
    print("   - GET /api/scheduler/status")
    print("\n" + "=" * 40)
    
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug)