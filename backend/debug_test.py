#!/usr/bin/env python3
"""
Debug script to test AI service directly
"""

import os
from dotenv import load_dotenv
from app.ai_service import AIService

# Load environment variables
load_dotenv()

def test_ai_service_directly():
    """Test AI service directly to debug the issue"""
    
    print("🔍 Debugging AI Service...")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    print(f"API Key configured: {'Yes' if api_key else 'No'}")
    if api_key:
        print(f"API Key length: {len(api_key)} characters")
        print(f"API Key starts with: {api_key[:10]}...")
    
    try:
        # Initialize AI service
        print("\n🔧 Initializing AI service...")
        ai_service = AIService()
        print("✅ AI service initialized successfully")
        
        # Test connection
        print("\n🌐 Testing connection...")
        is_connected = ai_service.test_connection()
        print(f"Connection test result: {is_connected}")
        
        # Test the improved method directly
        print("\n🧪 Testing generate_test_code_improved directly...")
        
        test_file_content = """
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
"""
        
        result = ai_service.generate_test_code_improved(
            "calculator.py",
            test_file_content,
            "Test function with valid input parameters"
        )
        
        print(f"✅ Generated code length: {len(result)} characters")
        print("\n📄 Generated Code:")
        print("-" * 40)
        print(result)
        
        # Check if it looks like mock code
        if "test_result" in result or "Replace with actual function call" in result:
            print("\n⚠️  WARNING: Generated code contains mock-like content!")
            print("This suggests the API call might be failing or returning unexpected content.")
        else:
            print("\n✅ Generated code looks like real AI content!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ai_service_directly()
