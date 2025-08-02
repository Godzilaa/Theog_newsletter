#!/usr/bin/env python3
"""
API Testing Script for Newsletter Automation System
"""

import requests
import json
import time
from datetime import datetime

API_BASE = "http://localhost:5000/api"

def test_api_endpoint(endpoint, method="GET", data=None, description=""):
    """Test an API endpoint and display results"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {method} {endpoint}")
    print(f"📝 {description}")
    print('='*60)
    
    try:
        url = f"{API_BASE}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=30)
        else:
            print(f"❌ Unsupported method: {method}")
            return
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            result = response.json()
            print(f"📋 Response:")
            print(json.dumps(result, indent=2, ensure_ascii=False)[:1000] + "..." if len(str(result)) > 1000 else json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"📋 Response: {response.text[:500]}...")
        
        if response.status_code < 400:
            print("✅ SUCCESS")
        else:
            print("❌ FAILED")
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION FAILED - Make sure the Flask API is running!")
    except requests.exceptions.Timeout:
        print("⏱️ TIMEOUT - Request took too long")
    except Exception as e:
        print(f"❌ ERROR: {e}")

def main():
    print("🚀 Newsletter API Testing Suite")
    print("=" * 60)
    print("⚠️  Make sure the Flask API is running on localhost:5000")
    print("   Run: python Scraper.py")
    print("=" * 60)
    
    # Test basic endpoints
    test_api_endpoint("/", description="Health check endpoint")
    
    test_api_endpoint("/categories", 
                     description="Get available news categories")
    
    test_api_endpoint("/newsapi?category=technology&limit=3", 
                     description="Get 3 tech articles from NewsAPI")
    
    test_api_endpoint("/newsapi?category=business&limit=2", 
                     description="Get 2 business articles from NewsAPI")
    
    # Test scheduler endpoints
    test_api_endpoint("/scheduler/status", 
                     description="Check scheduler status")
    
    test_api_endpoint("/scheduler/start", method="POST",
                     description="Start automated newsletter generation")
    
    time.sleep(2)  # Wait a moment
    
    test_api_endpoint("/scheduler/status", 
                     description="Check scheduler status after starting")
    
    # Test manual newsletter generation
    test_data = {
        "categories": ["technology", "science"]
    }
    test_api_endpoint("/generate-newsletter", method="POST", data=test_data,
                     description="Generate newsletter manually")
    
    # Test newsletter retrieval
    test_api_endpoint("/newsletters?limit=3", 
                     description="Get list of generated newsletters")
    
    # Stop scheduler
    test_api_endpoint("/scheduler/stop", method="POST",
                     description="Stop automated newsletter generation")
    
    print(f"\n{'='*60}")
    print("🎉 API Testing Complete!")
    print("=" * 60)
    print("📊 Dashboard available at: dashboard.html")
    print("🌐 Open dashboard.html in your browser to use the web interface")
    print("=" * 60)

if __name__ == "__main__":
    main()
