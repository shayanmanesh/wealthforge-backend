#!/usr/bin/env python3
"""
Simple deployment test to verify the app can start without import errors.
"""

import sys
import os

def test_app_imports():
    """Test that the app can be imported without errors."""
    print("🧪 Testing app imports...")
    
    try:
        import app
        print("✅ App imported successfully")
        return True
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

def test_health_endpoint():
    """Test that the health endpoint works."""
    print("🏥 Testing health endpoint...")
    
    try:
        from fastapi.testclient import TestClient
        from app import app
        
        client = TestClient(app)
        response = client.get("/health")
        
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health endpoint returned {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Health endpoint test failed: {e}")
        return False

def main():
    """Run deployment tests."""
    print("🚀 Running deployment tests...\n")
    
    tests = [
        test_app_imports,
        test_health_endpoint
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Deployment should work.")
        return 0
    else:
        print("💥 Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())