import gradio as gr
import requests
import json
from datetime import datetime
import subprocess
import time
import threading
import os

# Configuration
FLASK_URL = "http://localhost:5000"
flask_process = None

def check_flask_status():
    """Check if Flask backend is running"""
    try:
        response = requests.get(f"{FLASK_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_flask_backend():
    """Start the Flask backend in a separate process"""
    global flask_process
    try:
        flask_process = subprocess.Popen(
            ["python", "Scraper.py"],
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        time.sleep(3)  # Give Flask time to start
        return "✅ Flask backend started successfully!"
    except Exception as e:
        return f"❌ Error starting Flask backend: {str(e)}"

def stop_flask_backend():
    """Stop the Flask backend"""
    global flask_process
    if flask_process:
        flask_process.terminate()
        flask_process = None
        return "⏹️ Flask backend stopped"
    return "Flask backend was not running"

def get_backend_status():
    """Get backend status information"""
    if check_flask_status():
        try:
            response = requests.get(f"{FLASK_URL}/", timeout=5)
            data = response.json()
            
            status_info = f"""
🚀 **Backend Status**: {data.get('status', 'unknown').title()}
📊 **Version**: {data.get('version', 'unknown')}
🔑 **API Keys Configured**: 
   - NewsAPI: {'✅' if data.get('api_keys_configured', {}).get('newsapi') else '❌'}

📍 **Available Endpoints**:
{chr(10).join(['   - ' + ep for ep in data.get('available_endpoints', [])])}

⏰ **Last Updated**: {datetime.now().strftime('%H:%M:%S')}
            """
            return status_info
        except Exception as e:
            return f"❌ Error getting backend status: {str(e)}"
    else:
        return "❌ Flask backend is not running. Click 'Start Backend' to launch it."

def fetch_news(source, category="general", limit=10):
    """Fetch news from the specified source"""
    if not check_flask_status():
        return "❌ Flask backend is not running. Please start the backend first."
    
    try:
        if source == "Hacker News":
            url = f"{FLASK_URL}/api/hackernews"
            params = {"limit": limit}
        elif source == "NewsAPI":
            url = f"{FLASK_URL}/api/newsapi"
            params = {"category": category, "limit": limit}
        else:
            return "❌ Invalid news source selected"
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('status') == 'success':
            articles = data.get('data', [])
            
            if not articles:
                return f"📰 No articles found from {source}"
            
            # Format articles for display
            formatted_news = f"# 📰 {source} News\n\n"
            formatted_news += f"**Category**: {category.title()} | **Count**: {len(articles)} articles\n\n"
            
            for i, article in enumerate(articles, 1):
                formatted_news += f"## {i}. {article.get('title', 'No Title')}\n\n"
                
                if article.get('description'):
                    formatted_news += f"**Description**: {article['description']}\n\n"
                
                if article.get('source'):
                    formatted_news += f"**Source**: {article['source']}"
                
                if article.get('author'):
                    formatted_news += f" | **Author**: {article['author']}"
                
                if article.get('published_at'):
                    try:
                        pub_date = datetime.fromisoformat(article['published_at'].replace('Z', '+00:00'))
                        formatted_news += f" | **Published**: {pub_date.strftime('%Y-%m-%d %H:%M')}"
                    except:
                        formatted_news += f" | **Published**: {article['published_at']}"
                
                formatted_news += "\n\n"
                
                if article.get('url'):
                    formatted_news += f"🔗 [Read Full Article]({article['url']})\n\n"
                
                # Add extra info for Hacker News
                if source == "Hacker News":
                    if article.get('score'):
                        formatted_news += f"👍 **Score**: {article['score']}"
                    if article.get('comments'):
                        formatted_news += f" | 💬 **Comments**: {article['comments']}"
                    formatted_news += "\n\n"
                
                formatted_news += "---\n\n"
            
            return formatted_news
        else:
            error_msg = data.get('message', 'Unknown error occurred')
            return f"❌ Error fetching news: {error_msg}"
            
    except requests.RequestException as e:
        return f"❌ Network error: {str(e)}"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

def get_categories():
    """Get available news categories"""
    if not check_flask_status():
        return ["general"]  # Default category
    
    try:
        response = requests.get(f"{FLASK_URL}/api/categories", timeout=5)
        data = response.json()
        return data.get('data', ["general", "business", "technology", "sports", "health"])
    except:
        return ["general", "business", "technology", "sports", "health", "science", "entertainment"]

# Auto-start Flask backend when Gradio starts
def initialize_backend():
    """Initialize the Flask backend"""
    if not check_flask_status():
        start_flask_backend()

# Initialize backend in a separate thread
threading.Thread(target=initialize_backend, daemon=True).start()

# Create Gradio interface
with gr.Blocks(title="Newsletter App", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 📰 Newsletter App")
    gr.Markdown("Get the latest news from multiple sources in one place!")
    
    with gr.Tabs():
        # News Tab
        with gr.TabItem("📰 News"):
            with gr.Row():
                with gr.Column(scale=1):
                    news_source = gr.Radio(
                        choices=["Hacker News", "NewsAPI"],
                        value="Hacker News",
                        label="News Source"
                    )
                    
                    category = gr.Dropdown(
                        choices=get_categories(),
                        value="general",
                        label="Category (for NewsAPI)",
                        interactive=True
                    )
                    
                    limit = gr.Slider(
                        minimum=5,
                        maximum=20,
                        value=10,
                        step=1,
                        label="Number of Articles"
                    )
                    
                    fetch_btn = gr.Button("🔄 Fetch News", variant="primary")
                    
                with gr.Column(scale=2):
                    news_output = gr.Markdown(
                        value="Click 'Fetch News' to get the latest articles!",
                        label="News Articles"
                    )
            
            # Update category visibility based on source
            def update_category_visibility(source):
                if source == "NewsAPI":
                    return gr.update(visible=True)
                else:
                    return gr.update(visible=False)
            
            news_source.change(
                update_category_visibility,
                inputs=[news_source],
                outputs=[category]
            )
            
            fetch_btn.click(
                fetch_news,
                inputs=[news_source, category, limit],
                outputs=[news_output]
            )
        
        # Backend Management Tab
        with gr.TabItem("⚙️ Backend"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Backend Control")
                    start_btn = gr.Button("🚀 Start Backend", variant="primary")
                    stop_btn = gr.Button("⏹️ Stop Backend", variant="secondary")
                    status_btn = gr.Button("🔍 Check Status", variant="secondary")
                    
                with gr.Column():
                    backend_status = gr.Markdown(
                        value="Click 'Check Status' to see backend information",
                        label="Backend Status"
                    )
            
            start_btn.click(start_flask_backend, outputs=[backend_status])
            stop_btn.click(stop_flask_backend, outputs=[backend_status])
            status_btn.click(get_backend_status, outputs=[backend_status])
        
        # Setup Tab
        with gr.TabItem("📋 Setup"):
            gr.Markdown("""
            ### 🚀 Quick Setup Guide
            
            1. **Install Dependencies**:
               ```bash
               pip install flask flask-cors requests python-dotenv gradio
               ```
            
            2. **Configure API Keys** (Optional):
               - Create a `.env` file in the Backend folder
               - Add your NewsAPI key: `NEWS_API_KEY=your_api_key_here`
               - Get a free key from: [newsapi.org](https://newsapi.org/)
            
            3. **Start the App**:
               - The backend should start automatically
               - If not, use the 'Start Backend' button in the Backend tab
            
            ### 📰 Available News Sources
            
            - **Hacker News**: Tech news and discussions (no API key required)
            - **NewsAPI**: General news in multiple categories (requires free API key)
            
            ### 🔧 Troubleshooting
            
            - If backend fails to start, check that port 5000 is available
            - Check the Backend tab for status information
            - Make sure all dependencies are installed
            """)

# Auto-refresh status on load
app.load(get_backend_status, outputs=[])

if __name__ == "__main__":
    print("🚀 Starting Newsletter App with Gradio...")
    print("📝 The app will be available at: http://localhost:7860")
    print("🔧 Backend API runs on: http://localhost:5000")
    
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
