# Newsletter Backend

A comprehensive Flask-based backend for aggregating news from multiple sources including NewsAPI, GNews, Hacker News, and various RSS feeds.

## Features

- **Multiple News Sources**: 
  - NewsAPI integration
  - GNews API integration
  - Hacker News API
  - RSS feeds from major news outlets (BBC, CNN, Reuters, TechCrunch, etc.)
  - Web scraping with Newspaper3k

- **REST API Endpoints**:
  - Get news from all sources
  - Filter by category
  - Search functionality
  - Source-specific endpoints
  - Article content extraction

- **Data Processing**:
  - Article deduplication
  - Content summarization
  - Keyword extraction
  - Date-based sorting

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

### Installation

1. **Automated Setup** (Recommended):
   ```bash
   python setup.py
   ```

2. **Manual Setup**:
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

### Configuration

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```
   NEWS_API_KEY=your_news_api_key_here
   GNEWS_API_KEY=your_gnews_api_key_here
   ```

   Get API keys from:
   - [NewsAPI](https://newsapi.org/)
   - [GNews](https://gnews.io/)

### Running the Application

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

# Run the Flask application
python Scraper.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
- **GET** `/` - Health check endpoint

### News Endpoints
- **GET** `/api/news` - Get news from all sources
- **GET** `/api/news/category/{category}` - Get news by category
- **GET** `/api/news/search?q={query}` - Search news articles
- **GET** `/api/news/hackernews` - Get Hacker News stories
- **GET** `/api/news/rss/{feed_name}` - Get articles from specific RSS feed
- **GET** `/api/news/rss` - List available RSS feeds

### Utility Endpoints
- **GET** `/api/sources` - Get available news sources
- **GET** `/api/categories` - Get available categories
- **POST** `/api/article/extract` - Extract full article content from URL

### Query Parameters

Most endpoints support these optional parameters:
- `limit` - Number of articles to return (default: 10-20)
- `page` - Page number for pagination
- `category` - Filter by news category

### Example Requests

```bash
# Get top headlines
curl "http://localhost:5000/api/news?limit=10"

# Get technology news
curl "http://localhost:5000/api/news/category/technology"

# Search for articles
curl "http://localhost:5000/api/news/search?q=artificial+intelligence"

# Get Hacker News stories
curl "http://localhost:5000/api/news/hackernews"

# Extract article content
curl -X POST "http://localhost:5000/api/article/extract" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/article"}'
```

## Available News Sources

### API Sources (require keys)
- **NewsAPI**: Global news from 70,000+ sources
- **GNews**: Real-time news from Google News

### RSS Feeds (no key required)
- BBC News
- CNN
- Reuters
- TechCrunch
- The Verge
- Ars Technica
- Wired
- NPR
- The Guardian
- New York Times

### Special Sources
- **Hacker News**: Top stories from Hacker News community

## Categories

Available news categories:
- general
- business
- entertainment
- health
- science
- sports
- technology
- politics

## Response Format

All API responses follow this format:

```json
{
  "status": "success",
  "data": [...],
  "timestamp": "2025-07-28T10:30:00.000Z"
}
```

Error responses:
```json
{
  "status": "error",
  "message": "Error description",
  "timestamp": "2025-07-28T10:30:00.000Z"
}
```

## Article Schema

Each article object contains:

```json
{
  "id": "unique_article_id",
  "title": "Article title",
  "url": "https://example.com/article",
  "description": "Article summary/description",
  "published_at": "2025-07-28T10:30:00.000Z",
  "source": "Source name",
  "image_url": "https://example.com/image.jpg",
  "author": "Author name",
  "category": "technology",
  "score": 100,
  "comments": 25
}
```

## Development

### Project Structure

```
Backend/
├── Scraper.py          # Main Flask application
├── news_sources.py     # News source integrations
├── config.py          # Configuration settings
├── utils.py           # Utility functions
├── setup.py           # Setup script
├── requirements.txt   # Python dependencies
├── .env.example       # Environment template
└── .gitignore        # Git ignore rules
```

### Adding New Sources

To add a new news source:

1. Create a new class in `news_sources.py`
2. Implement required methods (`get_headlines`, etc.)
3. Add the source to `NewsAggregator`
4. Update the configuration in `config.py`

### Environment Variables

- `NEWS_API_KEY`: NewsAPI key
- `GNEWS_API_KEY`: GNews API key
- `FLASK_ENV`: Environment (development/production)
- `FLASK_DEBUG`: Enable debug mode
- `PORT`: Server port (default: 5000)

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure virtual environment is activated
2. **API key errors**: Check your `.env` file configuration
3. **Rate limiting**: Some APIs have usage limits
4. **Network timeouts**: Check internet connection and API service status

### Logs

The application logs important events and errors. Check console output for debugging information.

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation for the specific news sources
3. Create an issue on the project repository
