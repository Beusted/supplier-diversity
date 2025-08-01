#!/usr/bin/env python3
"""
Test script to verify authentication setup
Run this to check if all components are properly configured
"""

import sys
import os
from pathlib import Path

# Add frontend to path
sys.path.append(str(Path(__file__).parent / 'frontend'))

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import boto3
        print("✅ boto3 imported successfully")
    except ImportError as e:
        print(f"❌ boto3 import failed: {e}")
        return False
    
    try:
        from frontend.config import Config
        print("✅ Config module imported successfully")
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from frontend.auth_manager import CognitoAuthManager
        print("✅ CognitoAuthManager imported successfully")
    except ImportError as e:
        print(f"❌ CognitoAuthManager import failed: {e}")
        return False
    
    try:
        from frontend.auth_ui import require_authentication
        print("✅ Auth UI imported successfully")
    except ImportError as e:
        print(f"❌ Auth UI import failed: {e}")
        return False
    
    return True

def test_configuration():
    """Test if configuration is properly set up"""
    print("\n🔧 Testing configuration...")
    
    try:
        from frontend.config import Config
        
        if Config.is_configured():
            print("✅ All required configuration variables are set")
            print(f"   User Pool ID: {Config.AWS_COGNITO_USER_POOL_ID[:20]}...")
            print(f"   Client ID: {Config.AWS_COGNITO_CLIENT_ID[:20]}...")
            print(f"   Region: {Config.AWS_REGION}")
            return True
        else:
            missing = Config.get_missing_config()
            print(f"❌ Missing configuration variables: {', '.join(missing)}")
            print("   Please run 'python setup_aws_auth.py' to configure")
            return False
            
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_aws_connection():
    """Test AWS connection"""
    print("\n🌐 Testing AWS connection...")
    
    try:
        from frontend.auth_manager import CognitoAuthManager
        
        auth_manager = CognitoAuthManager()
        
        # Try to create a client (this will fail if credentials are wrong)
        client = auth_manager.cognito_client
        
        # Try to describe the user pool (this will fail if pool doesn't exist)
        response = client.describe_user_pool(UserPoolId=auth_manager.user_pool_id)
        
        pool_name = response['UserPool']['Name']
        print(f"✅ Successfully connected to User Pool: {pool_name}")
        return True
        
    except Exception as e:
        print(f"❌ AWS connection failed: {e}")
        print("   Check your AWS credentials and User Pool configuration")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        'frontend/auth_manager.py',
        'frontend/auth_ui.py',
        'frontend/config.py',
        'frontend/procurement_dashboard_with_auth.py',
        'setup_aws_auth.py',
        'docs/authentication_setup_guide.md'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("🚀 Authentication Setup Test")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Python Imports", test_imports),
        ("Configuration", test_configuration),
        ("AWS Connection", test_aws_connection)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your authentication system is ready.")
        print("   Run 'python start_dashboard.py' to start the authenticated dashboard")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("   Refer to docs/authentication_setup_guide.md for help")

if __name__ == "__main__":
    main()
