#!/usr/bin/env python3
"""
Test script for the Newsletter Backend API
"""

import requests
import json
import time
from datetime import datetime

API_BASE_URL = "http://localhost:5000"

def test_endpoint(endpoint, method="GET", data=None, expected_status=200):
    """Test a single API endpoint"""
    print(f"\n🧪 Testing {method} {endpoint}")
    
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
        
        if response.status_code == expected_status:
            print(f"✅ Status: {response.status_code}")
            
            # Try to parse JSON response
            try:
                json_data = response.json()
                print(f"✅ Valid JSON response")
                
                # Check for expected fields
                if 'status' in json_data:
                    print(f"✅ Status field: {json_data['status']}")
                
                if 'data' in json_data and isinstance(json_data['data'], (list, dict)):
                    data_length = len(json_data['data']) if isinstance(json_data['data'], list) else "dict"
                    print(f"✅ Data field: {data_length} items" if isinstance(data_length, int) else "✅ Data field: present")
                
                return True
                
            except json.JSONDecodeError:
                print(f"❌ Invalid JSON response")
                print(f"Response text: {response.text[:200]}...")
                return False
                
        else:
            print(f"❌ Expected status {expected_status}, got {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def run_all_tests():
    """Run comprehensive API tests"""
    print("🚀 Starting Newsletter Backend API Tests")
    print("=" * 50)
    
    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    for i in range(10):
        try:
            response = requests.get(f"{API_BASE_URL}/", timeout=5)
            if response.status_code == 200:
                print("✅ Server is ready!")
                break
        except:
            pass
        time.sleep(1)
    else:
        print("❌ Server is not responding. Make sure to start it with: python Scraper.py")
        return False
    
    tests = [
        # Basic endpoints
        ("/", "GET"),
        ("/api/status", "GET"),
        ("/api/sources", "GET"),
        ("/api/categories", "GET"),
        
        # Basic news endpoints (that work without full dependencies)
        ("/api/basic/hackernews?limit=5", "GET"),
        ("/api/basic/newsapi?category=technology&limit=3", "GET"),
        
        # These will return 503 errors but test the error handling
        ("/api/news?limit=5", "GET", None, 503),
        ("/api/news/category/technology?limit=3", "GET", None, 503),
        ("/api/news/search?q=tech&limit=3", "GET", None, 503),
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if len(test) == 2:
            endpoint, method = test
            success = test_endpoint(endpoint, method)
        elif len(test) == 3:
            endpoint, method, data = test
            success = test_endpoint(endpoint, method, data)
        else:
            endpoint, method, data, expected_status = test
            success = test_endpoint(endpoint, method, data, expected_status)
        
        if success:
            passed += 1
        
        time.sleep(0.5)  # Brief pause between tests
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

def test_performance():
    """Test API performance"""
    print("\n⚡ Performance Test")
    print("-" * 30)
    
    endpoints = [
        "/api/news?limit=10",
        "/api/news/hackernews?limit=5",
        "/api/categories"
    ]
    
    for endpoint in endpoints:
        start_time = time.time()
        try:
            response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=30)
            end_time = time.time()
            duration = end_time - start_time
            
            if response.status_code == 200:
                print(f"✅ {endpoint}: {duration:.2f}s")
            else:
                print(f"❌ {endpoint}: Failed ({response.status_code})")
                
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")

if __name__ == "__main__":
    success = run_all_tests()
    
    if success:
        test_performance()
    
    print(f"\n🏁 Testing completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
