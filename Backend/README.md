# 📰 Newsletter Automation System with AI Agents

An automated newsletter generation system powered by **Google Gemini** AI and **CrewAI** framework. Features researcher and writer agents that automatically fetch news from NewsAPI and generate professional newsletters.

## 🚀 Features

- **AI-Powered Agents**: Researcher and Writer agents using Google Gemini
- **Automated Image Generation**: AI-generated images for each newsletter article
- **Automated Scheduling**: Generate newsletters automatically with configurable intervals
- **NewsAPI Integration**: Comprehensive news coverage from reliable sources
- **RESTful API**: Complete REST API for all operations
- **Web Dashboard**: Beautiful HTML dashboard for monitoring and control
- **Newsletter Storage**: Persistent storage and retrieval system
- **Category Filtering**: Technology, Business, Science, Health, Sports, Entertainment, General

## 🛠️ Setup & Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Create a `.env` file with:
```
GOOGLE_API_KEY=your_google_gemini_api_key_here
NEWS_API_KEY=your_newsapi_key_here

# Optional: For image generation (choose one)
OPENAI_API_KEY=your_openai_api_key_here
STABILITY_API_KEY=your_stability_ai_key_here
```

### 3. Start the System
```bash
# Start the Flask API server
python Scraper.py

# Open the web dashboard
# Open dashboard.html in your browser
```

## 📊 API Endpoints

### Newsletter Management
- `POST /api/generate-newsletter` - Generate newsletter manually
- `GET /api/newsletters` - List all generated newsletters
- `GET /api/newsletters/<id>` - Get specific newsletter by ID

### Scheduler Control
- `POST /api/scheduler/start` - Start automated generation
- `POST /api/scheduler/stop` - Stop automated generation
- `GET /api/scheduler/status` - Check scheduler status

### News Sources
- `GET /api/newsapi?category=technology&limit=10` - Get NewsAPI articles
- `GET /api/categories` - Get available news categories

## 🖥️ Web Dashboard

Open `dashboard.html` in your browser for a beautiful web interface that provides:

- **Scheduler Control**: Start/stop automated generation
- **Manual Generation**: Create newsletters on-demand
- **Newsletter Browser**: View all generated newsletters
- **Real-time Status**: Monitor system status
- **Statistics**: Track generation metrics

## 🤖 AI Agents

### Researcher Agent
- Fetches news from multiple sources
- Analyzes articles for relevance and importance
- Categorizes content by theme and priority
- Identifies trending topics and breaking news

### Writer Agent
- Transforms research into professional articles
- Creates compelling headlines
- Structures content for readability
- Maintains professional news writing tone

## 💰 Cost-Effective Solution

- **Google Gemini**: Free tier available with generous limits
- **NewsAPI**: Free tier provides 1000+ requests/day
- **Hacker News**: Completely free API access

## 📁 Project Structure

```
Backend/
├── Scraper.py              # Flask API server
├── dashboard.html          # Web dashboard
├── setup.py               # Setup script
├── test_api.py            # API testing suite
├── quick_test.py          # Quick newsletter test
├── newsagent/             # CrewAI package
│   ├── src/newsagent/
│   │   ├── crew.py        # Agent definitions
│   │   ├── main.py        # Main execution
│   │   ├── config/
│   │   │   ├── agents.yaml # Agent configurations
│   │   │   └── tasks.yaml  # Task definitions
│   │   └── tools/
│   │       └── custom_tool.py # News fetching tools
└── generated_newsletters/  # Storage for newsletters
```

## 🧪 Testing

### Test All Endpoints
```bash
python test_api.py
```

### Test Newsletter Generation
```bash
python quick_test.py
```

### Manual API Testing
```bash
# Start scheduler
curl -X POST http://localhost:5000/api/scheduler/start

# Generate newsletter
curl -X POST http://localhost:5000/api/generate-newsletter \
  -H "Content-Type: application/json" \
  -d '{"categories":["technology","science"]}'

# Get newsletters
curl http://localhost:5000/api/newsletters

# Stop scheduler
curl -X POST http://localhost:5000/api/scheduler/stop
```

## 📈 Usage Examples

### 1. Automated Newsletter Generation
```python
import requests

# Start automated generation every minute
response = requests.post('http://localhost:5000/api/scheduler/start')
print(response.json())

# Check status
status = requests.get('http://localhost:5000/api/scheduler/status')
print(f"Running: {status.json()['scheduler_running']}")
```

### 2. Manual Newsletter Generation
```python
import requests

# Generate newsletter for specific categories
data = {"categories": ["technology", "business", "science"]}
response = requests.post(
    'http://localhost:5000/api/generate-newsletter',
    json=data
)

newsletter = response.json()
print(f"Newsletter #{newsletter['newsletter_id']} generated!")
```

### 3. Retrieve Generated Newsletters
```python
import requests

# Get list of newsletters
newsletters = requests.get('http://localhost:5000/api/newsletters').json()
print(f"Total newsletters: {newsletters['total_count']}")

# Get specific newsletter
newsletter_id = 1
newsletter = requests.get(f'http://localhost:5000/api/newsletters/{newsletter_id}').json()
print(newsletter['data']['content'])
```

## 🎯 Use Cases

- **News Aggregation**: Automatically compile daily tech news
- **Content Creation**: Generate newsletter content for blogs/websites
- **Market Research**: Track trends in specific industries
- **Educational Content**: Create educational newsletters on various topics
- **Business Intelligence**: Monitor industry news and developments

## 🔧 Configuration

### Newsletter Categories
Modify categories in the API call or dashboard:
- `technology` - Tech news and innovations
- `business` - Business and finance news
- `science` - Scientific discoveries and research
- `health` - Health and medical news
- `general` - General news and current events

### Scheduling Frequency
Currently set to generate every minute. To change:
1. Modify `schedule.every(1).minutes.do(...)` in the Flask app
2. Restart the server

## 🛡️ Security Notes

- API keys are stored in `.env` file (not committed to git)
- Flask runs in debug mode for development
- Use production WSGI server for production deployment
- CORS is enabled for dashboard access

## 📚 Dependencies

- **CrewAI**: AI agent framework
- **Flask**: Web API framework
- **Google Gemini**: LLM for AI agents
- **Requests**: HTTP library
- **Schedule**: Task scheduling
- **Python-dotenv**: Environment variables

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make your changes
4. Test thoroughly
5. Submit pull request

## 📄 License

This project is open source and available under the MIT License.

---

**🎉 Ready to automate your newsletter generation!**

Start the Flask API, open the dashboard, and watch as AI agents automatically research and write professional newsletters every minute using the power of Google Gemini and CrewAI! 🚀
