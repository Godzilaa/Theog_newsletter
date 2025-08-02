from crewai.tools import BaseTool
from typing import Type, List, Dict, Any
from pydantic import BaseModel, Field
import requests
import logging

logger = logging.getLogger(__name__)

class NewsScraperInput(BaseModel):
    """Input schema for NewsScraper."""
    category: str = Field(default="general", description="News category for NewsAPI (general, business, entertainment, health, science, sports, technology)")
    limit: int = Field(default=10, description="Number of articles to fetch (max 50)")

class NewsScraper(BaseTool):
    name: str = "News Scraper"
    description: str = (
        "Fetches news articles from NewsAPI by category. "
        "Returns structured article data including title, URL, description, author, and metadata."
    )
    args_schema: Type[BaseModel] = NewsScraperInput

    def _run(self, category: str = "general", limit: int = 10) -> str:
        try:
            base_url = "http://localhost:5000/api"
            url = f"{base_url}/newsapi"
            params = {"category": category, "limit": limit}
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == 'success':
                articles = data.get('data', [])
                
                # Format the response for the agent
                formatted_articles = []
                for article in articles:
                    formatted_article = {
                        'title': article.get('title', ''),
                        'url': article.get('url', ''),
                        'description': article.get('description', ''),
                        'published_at': article.get('published_at', ''),
                        'source': article.get('source', ''),
                        'author': article.get('author', ''),
                        'image_url': article.get('image_url', '')
                    }
                    formatted_articles.append(formatted_article)
                
                result = {
                    'status': 'success',
                    'source': 'newsapi',
                    'category': category,
                    'count': len(formatted_articles),
                    'articles': formatted_articles
                }
                
                return str(result)
            else:
                return f"Error from API: {data.get('message', 'Unknown error')}"
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error fetching news: {e}")
            return f"Network error: Make sure the Flask API is running on localhost:5000. Error: {str(e)}"
        except Exception as e:
            logger.error(f"Error in news scraper: {e}")
            return f"Error fetching news: {str(e)}"

class CategoryFetcherInput(BaseModel):
    """Input schema for CategoryFetcher - no inputs required."""
    pass

class CategoryFetcher(BaseTool):
    name: str = "Category Fetcher"
    description: str = (
        "Fetches available news categories from the NewsAPI. "
        "Returns a list of valid categories that can be used with the NewsAPI source."
    )
    args_schema: Type[BaseModel] = CategoryFetcherInput

    def _run(self) -> str:
        try:
            url = "http://localhost:5000/api/categories"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('status') == 'success':
                categories = data.get('data', [])
                return f"Available categories: {', '.join(categories)}"
            else:
                return f"Error: {data.get('message', 'Unknown error')}"
                
        except Exception as e:
            return f"Error fetching categories: {str(e)}"
