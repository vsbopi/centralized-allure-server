#!/usr/bin/env python3
"""
Test script to verify the branch structure functionality
"""

import os
import sys
from unittest.mock import patch, MagicMock

def test_branch_structure():
    """Test that the branch structure is working correctly"""
    try:
        # Mock S3 responses for branch structure
        mock_branches_response = {
            'CommonPrefixes': [
                {'Prefix': 'repo1/main/'},
                {'Prefix': 'repo1/develop/'},
                {'Prefix': 'repo1/feature-branch/'}
            ]
        }
        
        mock_reports_response = {
            'CommonPrefixes': [
                {'Prefix': 'repo1/main/allure-report/'},
                {'Prefix': 'repo1/main/allure-results/'}
            ]
        }
        
        with patch('boto3.client') as mock_boto3:
            mock_s3 = MagicMock()
            mock_s3.head_bucket.return_value = {}
            
            # Mock list_branches_for_repo
            mock_s3.list_objects_v2.side_effect = [
                mock_branches_response,  # For list_branches_for_repo
                mock_reports_response    # For list_reports_for_branch
            ]
            
            mock_boto3.return_value = mock_s3
            
            with patch.dict(os.environ, {
                'S3_BUCKET_NAME': 'test-bucket',
                'AWS_ACCESS_KEY_ID': 'test-key',
                'AWS_SECRET_ACCESS_KEY': 'test-secret'
            }):
                from app import S3ReportsServer
                
                server = S3ReportsServer()
                
                # Test list_branches_for_repo
                branches = server.list_branches_for_repo('repo1')
                expected_branches = ['develop', 'feature-branch', 'main']
                
                if sorted(branches) != expected_branches:
                    print(f"❌ Branch listing failed. Expected: {expected_branches}, Got: {sorted(branches)}")
                    return False
                
                print(f"✅ Branch listing works: {branches}")
                
                # Test list_reports_for_branch  
                reports = server.list_reports_for_branch('repo1', 'main')
                expected_reports = ['allure-report', 'allure-results']
                
                if sorted(reports) != expected_reports:
                    print(f"❌ Report listing failed. Expected: {expected_reports}, Got: {sorted(reports)}")
                    return False
                
                print(f"✅ Report listing for branch works: {reports}")
                
                return True
                
    except Exception as e:
        print(f"❌ Branch structure test error: {e}")
        return False

def test_new_routes():
    """Test that new routes are available"""
    try:
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
                
                # Test that new routes exist
                routes = [rule.rule for rule in app.url_map.iter_rules()]
                
                expected_new_routes = [
                    '/repo/<repo_name>/<branch_name>',
                    '/repo/<repo_name>/<branch_name>/<report_type>'
                ]
                
                for route in expected_new_routes:
                    if not any(route in r for r in routes):
                        print(f"❌ Missing new route: {route}")
                        return False
                
                print("✅ All new branch routes are available")
                return True
                
    except Exception as e:
        print(f"❌ Route test error: {e}")
        return False

def main():
    """Run all branch structure tests"""
    print("🧪 Testing Branch Structure Enhancement\n")
    
    tests = [
        ("Branch Structure Functionality", test_branch_structure),
        ("New Route Availability", test_new_routes)
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
        print("🎉 Branch structure enhancement is working correctly!")
        print("\n📁 Your S3 structure should now be:")
        print("   repo1/")
        print("   ├── main/")
        print("   │   ├── allure-report/")
        print("   │   └── allure-results/")
        print("   ├── develop/")
        print("   │   ├── allure-report/")
        print("   │   └── allure-results/")
        print("   └── feature-branch/")
        print("       ├── allure-report/")
        print("       └── allure-results/")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == '__main__':
    main()

