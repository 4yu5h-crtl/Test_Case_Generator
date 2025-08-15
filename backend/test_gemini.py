#!/usr/bin/env python3
"""
Test script to check if Gemini 2.5 Pro works with OpenRouter API
"""

import os
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from ai_service import AIService
from models import FileContent

def test_gemini_model():
    """Test if Gemini 2.5 Pro works with OpenRouter API"""
    print("Testing Gemini 2.5 Pro with OpenRouter API...")
    
    # Create a test file content
    test_file = FileContent(
        path="test.py",
        content="def add(a, b): return a + b",
        encoding="utf-8",
        size=24,
        sha="test123"
    )
    
    try:
        # Initialize AI service
        ai_service = AIService()
        print(f"AI Service initialized - Use Mock: {ai_service.use_mock}")
        
        if ai_service.use_mock:
            print("Using mock mode - no API key or insufficient balance")
            # Test mock mode
            summaries = ai_service.generate_test_case_summaries([test_file], "pytest")
            print(f"Mock summaries generated: {len(summaries)}")
            for summary in summaries:
                print(f"  - {summary['summary']}")
        else:
            print("Using real API - testing Gemini 2.5 Pro")
            # Test real API
            summaries = ai_service.generate_test_case_summaries([test_file], "pytest")
            print(f"Real summaries generated: {len(summaries)}")
            for summary in summaries:
                print(f"  - {summary['summary']}")
                
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_gemini_model()
    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed!")
