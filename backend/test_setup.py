#!/usr/bin/env python3
"""
Test script to verify backend setup and GitHub service initialization.
Run this script to test if the backend is properly configured.
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
current_dir = Path(__file__).parent
app_dir = current_dir / "app"
sys.path.insert(0, str(app_dir))

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from config import settings
        print("✓ Config imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import config: {e}")
        return False
    
    try:
        from models import FileNode, FileType, RepositoryInfo
        print("✓ Models imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import models: {e}")
        return False
    
    try:
        from github_service import GitHubService
        print("✓ GitHub service imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import GitHub service: {e}")
        return False
    
    try:
        from routes.github_routes import router
        print("✓ GitHub routes imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import GitHub routes: {e}")
        return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    from config import settings
    
    if not settings.GITHUB_TOKEN:
        print("⚠ Warning: GITHUB_TOKEN not set")
        print("  Create a .env file with your GitHub token to test full functionality")
    else:
        print("✓ GITHUB_TOKEN is set")
    
    print(f"✓ App name: {settings.APP_NAME}")
    print(f"✓ App version: {settings.APP_VERSION}")
    print(f"✓ Debug mode: {settings.DEBUG}")
    
    return True

def test_github_service():
    """Test GitHub service initialization"""
    print("\nTesting GitHub service...")
    
    from github_service import GitHubService
    
    try:
        # This will fail if no token is set, but that's expected
        service = GitHubService()
        print("✓ GitHub service initialized successfully")
        return True
    except ValueError as e:
        if "GitHub token is required" in str(e):
            print("⚠ GitHub service requires GITHUB_TOKEN to be set")
            print("  This is expected if you haven't configured your .env file yet")
            return True
        else:
            print(f"✗ Unexpected error initializing GitHub service: {e}")
            return False
    except Exception as e:
        print(f"✗ Failed to initialize GitHub service: {e}")
        return False

def test_models():
    """Test Pydantic models"""
    print("\nTesting Pydantic models...")
    
    from models import FileNode, FileType, RepositoryInfo
    
    try:
        # Test FileNode creation
        file_node = FileNode(
            name="test.py",
            path="test.py",
            type=FileType.FILE,
            size=100,
            sha="abc123",
            url="https://api.github.com/repos/test/test/contents/test.py"
        )
        print("✓ FileNode model works correctly")
        
        # Test RepositoryInfo creation
        repo_info = RepositoryInfo(
            owner="testuser",
            name="testrepo",
            full_name="testuser/testrepo",
            description="Test repository",
            default_branch="main"
        )
        print("✓ RepositoryInfo model works correctly")
        
        return True
    except Exception as e:
        print(f"✗ Failed to test models: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 50)
    print("Backend Setup Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("GitHub Service", test_github_service),
        ("Pydantic Models", test_models),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name} Test:")
        print("-" * 30)
        
        if test_func():
            passed += 1
            print(f"✓ {test_name} test passed")
        else:
            print(f"✗ {test_name} test failed")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is ready to run.")
        print("\nNext steps:")
        print("1. Create a .env file with your GITHUB_TOKEN")
        print("2. Run: python -m app.main")
        print("3. Visit: http://localhost:8000/docs")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
