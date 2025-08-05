#!/usr/bin/env python3
"""
InfoPulse Newsletter API Server
Provides REST API endpoints for the InfoPulse frontend
"""

import os
import logging
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import traceback
import threading
import time
import json
from werkzeug.middleware.proxy_fix import ProxyFix

# Add the newsagent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'newsagent', 'src'))

try:
    from newsagent.main import run_newsletter_generation
    from newsagent.tools.custom_tool import NewsScraper, CategoryFetcher, ImageGenerator
    CREW_AVAILABLE = True
except ImportError as e:
    logging.warning(f"CrewAI modules not available: {e}")
    CREW_AVAILABLE = False

# Import Scraper for NewsAPI
try:
    from Scraper import NewsAPI
    NEWSAPI_AVAILABLE = True
except ImportError:
    logging.warning("NewsAPI Scraper not available")
    NEWSAPI_AVAILABLE = False

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"]}})  # Enable CORS for frontend

# Available news categories
CATEGORIES = ['general', 'business', 'entertainment', 'health', 'science', 'sports', 'technology']

# In-memory storage for pre-generated articles
ARTICLE_CACHE = {
    'articles': [],
    'last_generated': None,
    'generation_in_progress': False,
    'next_generation': None
}

# Cache duration (in hours)
CACHE_DURATION_HOURS = 2

@app.route('/news')
def get_news():
    """Get news articles, optionally filtered by category"""
    category = request.args.get('category')
    if ARTICLE_CACHE['articles']:
        articles = ARTICLE_CACHE['articles']
        if category:
            articles = [a for a in articles if a.get('category', '').lower() == category.lower()]
        return jsonify(articles)
    return jsonify([])

@app.route('/generate-image', methods=['POST'])
def generate_image():
    """Generate an AI image based on prompt"""
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400
            
        # Use ImageGenerator from newsagent
        image_generator = ImageGenerator()
        image_url = image_generator.generate(prompt)
        
        return jsonify({"url": image_url})
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/summarize', methods=['POST'])
def summarize_text():
    """Summarize text using AI"""
    try:
        data = request.get_json()
        text = data.get('text')
        if not text:
            return jsonify({"error": "No text provided"}), 400
            
        # Use text summarization from newsagent
        from newsagent.tools.custom_tool import TextSummarizer
        summarizer = TextSummarizer()
        summary = summarizer.summarize(text)
        
        return jsonify({"summary": summary})
    except Exception as e:
        logger.error(f"Error summarizing text: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/explain', methods=['POST'])
def explain_text():
    """Explain text using AI"""
    try:
        data = request.get_json()
        text = data.get('text')
        if not text:
            return jsonify({"error": "No text provided"}), 400
            
        # Use text explanation from newsagent
        from newsagent.tools.custom_tool import TextExplainer
        explainer = TextExplainer()
        explanation = explainer.explain(text)
        
        return jsonify({"explanation": explanation})
    except Exception as e:
        logger.error(f"Error explaining text: {e}")
        return jsonify({"error": str(e)}), 500

def generate_articles_background():
    """Background function to generate articles"""
    global ARTICLE_CACHE
    
    if ARTICLE_CACHE['generation_in_progress']:
        logger.info("Generation already in progress, skipping...")
        return
    
    try:
        ARTICLE_CACHE['generation_in_progress'] = True
        logger.info("Starting background article generation using Newsagent agent (CrewAI)...")

        from newsagent.crew import Newsagent
        from datetime import datetime
        all_articles = []
        per_category_articles = {}
        # Reduce categories processed per minute (e.g., 3 per minute)
        categories_to_process = CATEGORIES[:3]  # Limit to 3 categories for initial processing
        
        for category in categories_to_process:
            # Prepare inputs for the agent
            inputs = {
                'categories': category,
                'current_date': datetime.now().strftime('%Y-%m-%d'),
                'current_time': datetime.now().strftime('%H:%M:%S')
            }
            try:
                crew = Newsagent().crew()
                result = crew.kickoff(inputs=inputs)
                # result should contain articles, but may need formatting
                articles = result.get('articles', []) if isinstance(result, dict) else []
                if not articles:
                    # fallback: try to parse result if it's a string
                    import ast
                    try:
                        parsed = ast.literal_eval(result)
                        articles = parsed.get('articles', [])
                    except Exception:
                        articles = []
                # Only keep the latest article for this category
                if articles:
                    latest_article = articles[0]
                    latest_article['category'] = category
                    all_articles.append(latest_article)
                    per_category_articles[category] = [latest_article]
                    logger.info(f"Generated 1 article for {category} using Newsagent agent.")
                else:
                    logger.warning(f"No articles generated for {category} by Newsagent agent.")
            except Exception as agent_error:
                logger.error(f"Newsagent agent generation failed for {category}: {agent_error}")
            # Increase delay to 5s to avoid LLM rate limits
            time.sleep(5)

        if NEWSAPI_AVAILABLE and len(CATEGORIES) > 3:
            news_api = NewsAPI()
            for category in CATEGORIES[3:]:
                try:
                    articles = news_api.get_top_headlines(category=category, page_size=1)
                    if articles:
                        latest_article = articles[0]
                        latest_article['category'] = category
                        all_articles.append(latest_article)
                        per_category_articles[category] = [latest_article]
                        logger.info(f"Fetched 1 article for {category} using NewsAPI batch.")
                    else:
                        logger.warning(f"No articles found for {category} in NewsAPI batch.")
                except Exception as newsapi_error:
                    logger.error(f"NewsAPI batch fetch failed for {category}: {newsapi_error}")
                # Add a delay to avoid NewsAPI rate limits (safe: 1s per call)
                time.sleep(1)
        
        # Update the cache with the newly generated articles
        ARTICLE_CACHE['articles'] = all_articles
        ARTICLE_CACHE['last_generated'] = datetime.now()
    except Exception as e:
        logger.error(f"Error in background article generation: {e}")
    finally:
        ARTICLE_CACHE['generation_in_progress'] = False

@app.route('/api/categories/<category>/newsletter', methods=['POST'])
def generate_category_newsletter(category):
    """Generate a newsletter for a specific category with AI images"""
    try:
        if category not in CATEGORIES:
            return jsonify({
                'status': 'error',
                'message': f'Invalid category. Available categories: {", ".join(CATEGORIES)}'
            }), 400

        data = request.get_json() or {}
        limit = data.get('limit', 5)
        include_images = data.get('include_images', True)

        logger.info(f"Generating {category} newsletter with {limit} articles using Newsagent agent (CrewAI)")

        if CREW_AVAILABLE:
            # Use Newsagent agent (CrewAI) for category-specific newsletter generation
            from newsagent.crew import Newsagent
            from datetime import datetime
            # Prepare inputs for the agent
            inputs = {
                'categories': category,
                'current_date': datetime.now().strftime('%Y-%m-%d'),
                'current_time': datetime.now().strftime('%H:%M:%S')
            }
            try:
                crew = Newsagent().crew()
                result = crew.kickoff(inputs=inputs)
                # result should contain articles, but may need formatting
                articles = result.get('articles', []) if isinstance(result, dict) else []
                if not articles:
                    # fallback: try to parse result if it's a string
                    import ast
                    try:
                        parsed = ast.literal_eval(result)
                        articles = parsed.get('articles', [])
                    except Exception:
                        articles = []
                # Only keep the latest article for this category
                if articles:
                    latest_article = articles[0]
                    latest_article['category'] = category
                    logger.info(f"Generated 1 article for {category} using Newsagent agent.")
                else:
                    logger.warning(f"No articles generated for {category} by Newsagent agent.")
            except Exception as agent_error:
                logger.error(f"Newsagent agent generation failed for {category}: {agent_error}")
                return jsonify({
                    'status': 'error',
                    'message': f"Newsagent agent error: {agent_error}"
                }), 500
        else:
            return jsonify({
                'status': 'error',
                'message': 'CrewAI modules not available'
            }), 503

        if include_images and CREW_AVAILABLE:
            # Add AI images to the article using Newsagent's ImageGenerator
            from newsagent.tools.custom_tool import ImageGenerator
            image_generator = ImageGenerator()
            
            try:
                prompt = f"High-quality {category} news illustration for: {latest_article['title'][:80]}"
                image_result = image_generator._run(
                    prompt=prompt,
                    article_title=latest_article['title'],
                    style="premium"
                )
                
                if image_result:
                    latest_article['ai_image'] = eval(image_result) if isinstance(image_result, str) else image_result
                else:
                    latest_article['ai_image'] = {'status': 'failed'}
            except Exception as img_error:
                logger.warning(f"Image generation failed: {img_error}")
                latest_article['ai_image'] = {'status': 'failed'}

        return jsonify({
            'status': 'success',
            'category': category,
            'count': 1,
            'articles': [latest_article]
        })
        
    except Exception as e:
        logger.error(f"Error generating {category} newsletter: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/categories/<category>', methods=['GET'])
def get_category_articles(category):
    """Get latest articles for a specific category"""
    try:
        # category is passed as a URL parameter
        if category not in CATEGORIES:
            return jsonify({
                'status': 'error',
                'message': f'Invalid category. Available categories: {", ".join(CATEGORIES)}'
            }), 400

        limit = request.args.get('limit', 10, type=int)

        if NEWSAPI_AVAILABLE:
            news_api = NewsAPI()
            articles = news_api.get_top_headlines(category=category, page_size=limit)
            if articles:
                return jsonify({
                    'status': 'success',
                    'category': category,
                    'count': len(articles),
                    'articles': articles
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': f'No articles found for category: {category}'
                }), 404
        else:
            return jsonify({
                'status': 'error',
                'message': 'NewsAPI not available'
            }), 503
    except Exception as e:
        logger.error(f"Error fetching {category} articles: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/quick-run', methods=['POST'])
def quick_run():
    """Quick run: Generate newsletter with 3 articles, minimal processing"""
    try:
        data = request.get_json() or {}
        categories = data.get('categories', ['technology', 'business'])
        
        if ARTICLE_CACHE['generation_in_progress']:
            return jsonify({
                'status': 'busy',
                'message': 'Another generation is in progress'
            }), 409
        
        def quick_generation():
            global ARTICLE_CACHE
            ARTICLE_CACHE['generation_in_progress'] = True
            
            try:
                all_articles = []
                if NEWSAPI_AVAILABLE:
                    news_api = NewsAPI()
                    for category in categories[:2]:  # Limit to 2 categories for quick run
                        articles = news_api.get_top_headlines(category=category, page_size=2)
                        if articles:
                            all_articles.extend(articles[:2])  # 2 articles per category
                        # Add a delay to avoid NewsAPI rate limits (safe: 1s per call)
                        time.sleep(1)
                
                ARTICLE_CACHE['articles'] = all_articles
                ARTICLE_CACHE['last_generated'] = datetime.now()
                ARTICLE_CACHE['generation_in_progress'] = False
                
            except Exception as e:
                logger.error(f"Quick generation error: {e}")
                ARTICLE_CACHE['generation_in_progress'] = False
        
        thread = threading.Thread(target=quick_generation, daemon=True)
        thread.start()
        
        return jsonify({
            'status': 'success',
            'run_type': 'quick',
            'message': 'Quick generation started',
            'estimated_duration': '30 seconds'
        })
        
    except Exception as e:
        logger.error(f"Quick run error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/scheduler/standard-run', methods=['POST'])
def standard_schedule_run():
    """Standard run: Generate newsletter with 6-8 articles, with AI images"""
    try:
        data = request.get_json() or {}
        categories = data.get('categories', ['technology', 'business', 'general'])
        
        if ARTICLE_CACHE['generation_in_progress']:
            return jsonify({
                'status': 'busy',
                'message': 'Another generation is in progress'
            }), 409
        
        # Start standard generation in background (this is our current generate_articles_background)
        thread = threading.Thread(target=generate_articles_background, daemon=True)
        thread.start()
        
        return jsonify({
            'status': 'success',
            'run_type': 'standard',
            'message': 'Standard generation started with AI images',
            'estimated_duration': '2-3 minutes'
        })
        
    except Exception as e:
        logger.error(f"Standard run error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/scheduler/premium-run', methods=['POST'])
def premium_schedule_run():
    """Premium run: Generate newsletter with 10+ articles, AI images, and enhanced processing"""
    try:
        data = request.get_json() or {}
        categories = data.get('categories', CATEGORIES[:4])  # Use more categories
        
        if ARTICLE_CACHE['generation_in_progress']:
            return jsonify({
                'status': 'busy',
                'message': 'Another generation is in progress'
            }), 409
        
        def premium_generation():
            global ARTICLE_CACHE
            ARTICLE_CACHE['generation_in_progress'] = True
            
            try:
                all_articles = []
                if NEWSAPI_AVAILABLE:
                    news_api = NewsAPI()
                    image_generator = ImageGenerator()
                    
                    for category in categories:
                        articles = news_api.get_top_headlines(category=category, page_size=4)
                        if articles:
                            # Add AI images to all articles
                            for article in articles:
                                try:
                                    prompt = f"High-quality {category} news illustration for: {article['title'][:80]}"
                                    image_result = image_generator._run(
                                        prompt=prompt,
                                        article_title=article['title'],
                                        style="premium"
                                    )
                                    
                                    if image_result:
                                        article['ai_image'] = eval(image_result) if isinstance(image_result, str) else image_result
                                        
                                except Exception as img_error:
                                    logger.warning(f"Image generation failed: {img_error}")
                                    article['ai_image'] = {'status': 'failed'}
                            
                            all_articles.extend(articles)
                        # Add a delay to avoid NewsAPI rate limits (safe: 1s per call)
                        time.sleep(1)
                
                ARTICLE_CACHE['articles'] = all_articles
                ARTICLE_CACHE['last_generated'] = datetime.now()
                ARTICLE_CACHE['generation_in_progress'] = False
                
            except Exception as e:
                logger.error(f"Premium generation error: {e}")
                ARTICLE_CACHE['generation_in_progress'] = False
        
        thread = threading.Thread(target=premium_generation, daemon=True)
        thread.start()
        
        return jsonify({
            'status': 'success',
            'run_type': 'premium',
            'message': 'Premium generation started with enhanced AI processing',
            'estimated_duration': '5-7 minutes'
        })
        
    except Exception as e:
        logger.error(f"Premium run error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/categories', methods=['GET'])
def get_available_categories():
    """Get list of available news categories"""
    return jsonify({
        'status': 'success',
        'categories': CATEGORIES,
        'total_count': len(CATEGORIES)
    })

@app.route('/api/scheduler/run-types', methods=['GET'])
def get_run_types():
    """Get available scheduler run types"""
    return jsonify({
        'status': 'success',
        'run_types': {
            'quick': {
                'description': 'Fast generation with 4 articles, no AI images',
                'duration': '30 seconds',
                'articles': '4',
                'ai_images': False
            },
            'standard': {
                'description': 'Balanced generation with 6-8 articles and AI images',
                'duration': '2-3 minutes',
                'articles': '6-8',
                'ai_images': True
            },
            'premium': {
                'description': 'Full generation with 10+ articles, premium AI images',
                'duration': '5-7 minutes',
                'articles': '10+',
                'ai_images': True
            }
        }
    })

if __name__ == '__main__':
    # Check environment variables
    newsapi_key = os.getenv('NEWSAPI_KEY')
    if not newsapi_key:
        logger.warning("NEWSAPI_KEY not found in environment variables")
    
    stability_key = os.getenv('STABILITY_API_KEY')
    if not stability_key:
        logger.warning("STABILITY_API_KEY not found in environment variables")
    
    gemini_key = os.getenv('GOOGLE_API_KEY')
    if not gemini_key:
        logger.warning("GOOGLE_API_KEY not found in environment variables")
    
    logger.info("Starting InfoPulse Newsletter API Server...")
    logger.info(f"NewsAPI Available: {NEWSAPI_AVAILABLE}")
    logger.info(f"CrewAI Available: {CREW_AVAILABLE}")
    
    # Trigger initial generation
    initial_generation_thread = threading.Thread(target=generate_articles_background, daemon=True)
    initial_generation_thread.start()

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
