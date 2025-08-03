from crewai.tools import BaseTool
from typing import Type, List, Dict, Any
from pydantic import BaseModel, Field
import requests
import logging
import os
import base64
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

class ImageGeneratorInput(BaseModel):
    """Input schema for ImageGenerator."""
    prompt: str = Field(..., description="Detailed description of the image to generate for the news article")
    article_title: str = Field(..., description="Title of the news article this image is for")
    style: str = Field(default="professional", description="Style of image: professional, editorial, modern, minimal")

class ImageGenerator(BaseTool):
    name: str = "Image Generator"
    description: str = (
        "Generates professional images for news articles based on article content and headlines. "
        "Creates relevant, high-quality visuals that enhance newsletter articles."
    )
    args_schema: Type[BaseModel] = ImageGeneratorInput

    def _run(self, prompt: str, article_title: str, style: str = "professional") -> str:
        try:
            # Enhanced prompt for news-appropriate imagery
            enhanced_prompt = f"Professional {style} news illustration for article: '{article_title}'. {prompt}. High quality, editorial style, suitable for newsletter publication, clean and modern design, photorealistic"
            
            # Check if Stability AI key is available
            stability_key = os.getenv('STABILITY_API_KEY')
            
            if stability_key and stability_key.startswith('sk-'):
                try:
                    # Use Stability AI API
                    response = requests.post(
                        "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
                        headers={
                            "Authorization": f"Bearer {stability_key}",
                            "Content-Type": "application/json",
                            "Accept": "application/json"
                        },
                        json={
                            "text_prompts": [
                                {
                                    "text": enhanced_prompt,
                                    "weight": 1
                                }
                            ],
                            "cfg_scale": 7,
                            "height": 768,
                            "width": 1344,
                            "steps": 30,
                            "samples": 1
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("artifacts") and len(data["artifacts"]) > 0:
                            # Get the base64 image data
                            image_base64 = data["artifacts"][0]["base64"]
                            
                            # Save the image (optional - you could save to a local directory or cloud storage)
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            safe_title = "".join(c for c in article_title if c.isalnum() or c in (' ', '-', '_')).rstrip()[:30]
                            filename = f"ai_image_{safe_title}_{timestamp}.png"
                            
                            # For demo, we'll return the base64 data URL
                            image_url = f"data:image/png;base64,{image_base64}"
                            
                            image_result = {
                                'status': 'generated',
                                'image_url': image_url,
                                'alt_text': f"AI-generated professional illustration for: {prompt}",
                                'caption': f"AI-generated visual representation of {article_title}",
                                'prompt_used': enhanced_prompt,
                                'style': style,
                                'dimensions': "1344x768",
                                'article_title': article_title,
                                'generation_note': "Generated using Stability AI SDXL",
                                'filename': filename
                            }
                            
                            logger.info(f"Successfully generated image for article: {article_title}")
                            return str(image_result)
                    
                    # If API call failed, log the error and fall back to placeholder
                    logger.warning(f"Stability AI API call failed: {response.status_code} - {response.text}")
                    
                except Exception as api_error:
                    logger.error(f"Error calling Stability AI API: {api_error}")
            
            # Fallback to placeholder image
            safe_title = article_title.replace(' ', '+').replace(',', '').replace('.', '')[:50]
            placeholder_url = f"https://via.placeholder.com/1344x768/1e40af/ffffff?text={safe_title}"
            
            image_result = {
                'status': 'placeholder',
                'image_url': placeholder_url,
                'alt_text': f"Professional illustration for: {prompt}",
                'caption': f"Visual representation of {article_title}",
                'prompt_used': enhanced_prompt,
                'style': style,
                'dimensions': "1344x768",
                'article_title': article_title,
                'generation_note': "Placeholder image - Stability AI integration ready"
            }
            
            return str(image_result)
            
        except Exception as e:
            logger.error(f"Error in image generator: {e}")
            return f"Error generating image: {str(e)}"
