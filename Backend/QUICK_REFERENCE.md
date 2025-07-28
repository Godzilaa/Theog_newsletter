# Newsletter Backend - Quick Reference Guide

## ✅ Your API is Running Successfully!

**Base URL:** `http://localhost:5000` (not https)

## 🔧 Current Status: Basic Mode
Your API is running in basic mode with core functionality. This is perfect for getting started!

## 📍 Working Endpoints

### Health & Status
```bash
# Health check
curl "http://localhost:5000/"

# Detailed system status
curl "http://localhost:5000/api/status"
```

### News Sources
```bash
# Get available news sources
curl "http://localhost:5000/api/sources"

# Get available categories
curl "http://localhost:5000/api/categories"
```

### News Content
```bash
# Get Hacker News stories (always works)
curl "http://localhost:5000/api/basic/hackernews?limit=5"

# Get NewsAPI headlines (requires API key)
curl "http://localhost:5000/api/basic/newsapi?category=technology&limit=3"

# Available categories: general, business, entertainment, health, science, sports, technology
```

## 🗝️ API Keys Configuration

Edit `.env` file to add your API keys:

```env
NEWS_API_KEY=your_actual_api_key_here
GNEWS_API_KEY=your_actual_api_key_here
```

**Get free API keys:**
- NewsAPI: https://newsapi.org/ (30,000 requests/month free)
- GNews: https://gnews.io/ (100 requests/day free)

## 📊 Sample API Responses

### Hacker News Response
```json
{
  "status": "success",
  "source": "Hacker News",
  "count": 3,
  "data": [
    {
      "title": "Article Title",
      "url": "https://example.com",
      "score": 240,
      "comments": 81,
      "published_at": "2025-07-28T20:06:39"
    }
  ]
}
```

### NewsAPI Response
```json
{
  "status": "success",
  "source": "NewsAPI",
  "category": "technology",
  "count": 3,
  "data": [
    {
      "title": "Article Title",
      "url": "https://example.com",
      "description": "Article description...",
      "author": "Author Name",
      "published_at": "2025-07-28T18:30:00Z",
      "image_url": "https://example.com/image.jpg"
    }
  ]
}
```

## 🚀 Next Steps

### 1. For More Features (Optional)
```bash
# Install full dependencies for RSS feeds, content extraction, etc.
.\install-windows.bat
```

### 2. Frontend Integration
Your API is ready for frontend integration:
- CORS is enabled
- JSON responses
- RESTful endpoints
- Error handling

### 3. Testing Your API
```bash
# Run comprehensive tests
python test_api.py

# Quick manual test
curl "http://localhost:5000/api/basic/hackernews?limit=3"
```

## 🛠️ Troubleshooting

### Common Issues:
1. **"Connection refused"** → Make sure server is running: `python Scraper.py`
2. **"SSL/TLS error"** → Use `http://` not `https://`
3. **Empty NewsAPI results** → Check your API key in `.env` file
4. **503 errors on /api/news endpoints** → Normal in basic mode, use `/api/basic/` endpoints

### Server Status:
```bash
# Check if server is running
curl "http://localhost:5000/"

# Should return: {"status": "healthy", ...}
```

## 📁 File Structure
```
Backend/
├── Scraper.py          # Main Flask app (currently running)
├── .env               # Your API keys (edit this!)
├── test_api.py        # Test script
├── quick-start.bat    # Easy setup script
├── install-windows.bat # Full setup (optional)
└── venv/              # Virtual environment
```

## 🎯 Ready for Production?

For production deployment, consider:
- Use a proper WSGI server (gunicorn, uwsgi)
- Add rate limiting
- Use HTTPS
- Add caching
- Set up monitoring

**Your basic newsletter backend is fully functional and ready to use!** 🎉
