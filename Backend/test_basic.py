#!/usr/bin/env python3
"""
Simple test script for the Newsletter Backend API (Basic Version)
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:5000"

def test_endpoint(endpoint, description):
    """Test a single API endpoint"""
    print(f"\n🧪 Testing: {description}")
    print(f"📍 Endpoint: {endpoint}")
    
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Status: {response.status_code}")
            
            data = response.json()
            if 'data' in data:
                if isinstance(data['data'], list):
                    print(f"📊 Results: {len(data['data'])} items")
                    if data['data'] and isinstance(data['data'][0], dict):
                        print(f"📰 Sample: {data['data'][0].get('title', 'N/A')[:60]}...")
                elif isinstance(data['data'], dict):
                    print(f"📊 Results: Dictionary with {len(data['data'])} keys")
                else:
                    print(f"📊 Results: {data['data']}")
            
            return True
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"Error: {response.text[:200]}...")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def main():
    """Run basic API tests"""
    print("🚀 Newsletter Backend API - Basic Functionality Test")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        if response.status_code != 200:
            print("❌ Server is not responding correctly")
            return
    except:
        print("❌ Server is not running!")
        print("Please start it with: python Scraper.py")
        return
    
    print("✅ Server is running!")
    
    # Test basic endpoints
    tests = [
        ("/", "Health Check"),
        ("/api/status", "System Status"),
        ("/api/categories", "Available Categories"),
        ("/api/sources", "Available Sources"),
        ("/api/basic/hackernews?limit=3", "Hacker News Stories"),
    ]
    
    # Only test NewsAPI if key is configured
    health_response = requests.get(f"{API_BASE_URL}/")
    if health_response.status_code == 200:
        health_data = health_response.json()
        if health_data.get('api_keys_configured', {}).get('newsapi'):
            tests.append(("/api/basic/newsapi?category=technology&limit=3", "NewsAPI Headlines"))
    
    passed = 0
    total = len(tests)
    
    for endpoint, description in tests:
        if test_endpoint(endpoint, description):
            passed += 1
        time.sleep(0.5)  # Brief pause between tests
    
    print(f"\n📊 Test Summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your basic API is working correctly.")
        print("\n📋 Next Steps:")
        print("1. Edit .env file to add API keys for more functionality")
        print("2. Run install-windows.bat to install full dependencies")
        print("3. For production, consider using a proper WSGI server")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    print(f"\n🌐 API Documentation:")
    print(f"   Health Check: {API_BASE_URL}/")
    print(f"   Hacker News:  {API_BASE_URL}/api/basic/hackernews")
    print(f"   NewsAPI:      {API_BASE_URL}/api/basic/newsapi?category=technology")

if __name__ == "__main__":
    main()
