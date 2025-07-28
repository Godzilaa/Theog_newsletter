from datetime import datetime
import logging
from typing import List, Dict
import hashlib

logger = logging.getLogger(__name__)

def format_article(article: Dict) -> Dict:
    """Format article data to ensure consistency"""
    return {
        'id': generate_article_id(article),
        'title': article.get('title', '').strip(),
        'url': article.get('url', ''),
        'description': article.get('description', '').strip(),
        'published_at': format_timestamp(article.get('published_at')),
        'source': article.get('source', 'Unknown'),
        'image_url': article.get('image_url'),
        'author': article.get('author'),
        'category': article.get('category'),
        'score': article.get('score'),
        'comments': article.get('comments')
    }

def generate_article_id(article: Dict) -> str:
    """Generate a unique ID for an article based on title and URL"""
    title = article.get('title', '')
    url = article.get('url', '')
    content = f"{title}{url}".encode('utf-8')
    return hashlib.md5(content).hexdigest()[:12]

def format_timestamp(timestamp) -> str:
    """Format timestamp to ISO format"""
    if not timestamp:
        return None
    
    try:
        if isinstance(timestamp, str):
            # Try parsing common timestamp formats
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                return dt.isoformat()
            except:
                pass
        elif isinstance(timestamp, datetime):
            return timestamp.isoformat()
        
        return str(timestamp)
    except Exception as e:
        logger.warning(f"Error formatting timestamp {timestamp}: {e}")
        return None

def deduplicate_articles(articles: List[Dict]) -> List[Dict]:
    """Remove duplicate articles based on title similarity"""
    seen_titles = set()
    unique_articles = []
    
    for article in articles:
        title = article.get('title', '').lower().strip()
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_articles.append(format_article(article))
    
    return unique_articles

def sort_articles_by_date(articles: List[Dict], reverse: bool = True) -> List[Dict]:
    """Sort articles by publication date"""
    def get_sort_key(article):
        timestamp = article.get('published_at')
        if timestamp:
            try:
                return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except:
                pass
        return datetime.min if reverse else datetime.max
    
    return sorted(articles, key=get_sort_key, reverse=reverse)

def filter_articles_by_keywords(articles: List[Dict], keywords: List[str]) -> List[Dict]:
    """Filter articles by keywords in title or description"""
    if not keywords:
        return articles
    
    filtered = []
    keywords_lower = [kw.lower() for kw in keywords]
    
    for article in articles:
        title = article.get('title', '').lower()
        description = article.get('description', '').lower()
        
        if any(keyword in title or keyword in description for keyword in keywords_lower):
            filtered.append(article)
    
    return filtered

def validate_article(article: Dict) -> bool:
    """Validate if an article has required fields"""
    required_fields = ['title', 'url']
    return all(article.get(field) for field in required_fields)

def paginate_results(articles: List[Dict], page: int = 1, page_size: int = 20) -> Dict:
    """Paginate article results"""
    total = len(articles)
    start = (page - 1) * page_size
    end = start + page_size
    
    return {
        'articles': articles[start:end],
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total': total,
            'pages': (total + page_size - 1) // page_size,
            'has_next': end < total,
            'has_prev': page > 1
        }
    }

def sanitize_html(text: str) -> str:
    """Remove HTML tags from text"""
    if not text:
        return ""
    
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(text, 'html.parser')
        return soup.get_text().strip()
    except ImportError:
        # Fallback: simple HTML tag removal
        import re
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text).strip()

def create_error_response(message: str, status_code: int = 500) -> Dict:
    """Create standardized error response"""
    return {
        'status': 'error',
        'message': message,
        'timestamp': datetime.now().isoformat()
    }, status_code

def create_success_response(data: any, message: str = None) -> Dict:
    """Create standardized success response"""
    response = {
        'status': 'success',
        'data': data,
        'timestamp': datetime.now().isoformat()
    }
    
    if message:
        response['message'] = message
    
    return response
