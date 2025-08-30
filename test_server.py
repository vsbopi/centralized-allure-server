#!/usr/bin/env python3
"""
Simple test script to verify the server setup
"""

import os
import sys
from unittest.mock import patch, MagicMock

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import flask
        import boto3
        from dotenv import load_dotenv
        import waitress
        print("✅ All required packages are available")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        return False

def test_config():
    """Test configuration loading"""
    try:
        from config import Config
        
        # Test with mock environment
        with patch.dict(os.environ, {
            'S3_BUCKET_NAME': 'test-bucket',
            'AWS_ACCESS_KEY_ID': 'test-key',
            'AWS_SECRET_ACCESS_KEY': 'test-secret'
        }):
            Config.validate()
            print("✅ Configuration validation works")
            return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_app_creation():
    """Test that the Flask app can be created"""
    try:
        # Mock S3 connection to avoid needing real AWS credentials
        with patch('boto3.client') as mock_boto3:
            mock_s3 = MagicMock()
            mock_s3.head_bucket.return_value = {}
            mock_boto3.return_value = mock_s3
            
            with patch.dict(os.environ, {
                'S3_BUCKET_NAME': 'test-bucket',
                'AWS_ACCESS_KEY_ID': 'test-key',
                'AWS_SECRET_ACCESS_KEY': 'test-secret'
            }):
                from app import app
                
                # Test that app has the expected routes
                routes = [rule.rule for rule in app.url_map.iter_rules()]
                expected_routes = ['/', '/repo/<repo_name>', '/files/<path:path>', '/health']
                
                for route in expected_routes:
                    if any(route in r for r in routes):
                        continue
                    else:
                        print(f"❌ Missing route: {route}")
                        return False
                
                print("✅ Flask app created successfully with all routes")
                return True
                
    except Exception as e:
        print(f"❌ App creation error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Centralized Allure Reports Server Setup\n")
    
    tests = [
        ("Package Imports", test_imports),
        ("Configuration", test_config),
        ("Flask App Creation", test_app_creation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your server setup is ready.")
        print("\nNext steps:")
        print("1. Copy .env.example to .env and configure your AWS credentials")
        print("2. Run: python app.py")
        print("3. Visit: http://localhost:8080")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
