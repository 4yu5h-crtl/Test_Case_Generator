#!/usr/bin/env python3
"""
Test script for the new /ai/generate-test endpoint
"""

import requests
import json

def test_generate_test_endpoint():
    """Test the new generate-test endpoint"""
    
    # Test data
    test_data = {
        "file_name": "calculator.py",
        "file_content": """
def add(a, b):
    \"\"\"Add two numbers\"\"\"
    return a + b

def subtract(a, b):
    \"\"\"Subtract b from a\"\"\"
    return a - b

def multiply(a, b):
    \"\"\"Multiply two numbers\"\"\"
    return a * b

def divide(a, b):
    \"\"\"Divide a by b\"\"\"
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
""",
        "scenario": "Test function with valid input parameters"
    }
    
    try:
        # Make the request
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/ai/generate-test",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ SUCCESS! Generated test code:")
            print("=" * 50)
            print(f"File: {result.get('file_name')}")
            print(f"Scenario: {result.get('scenario')}")
            print("\nGenerated Code:")
            print("-" * 30)
            print(result.get('code', 'No code generated'))
        else:
            print(f"\n❌ ERROR: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to server. Make sure the server is running on port 8001.")
    except requests.exceptions.Timeout:
        print("❌ ERROR: Request timed out.")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    print("Testing new /ai/generate-test endpoint...")
    print("=" * 50)
    test_generate_test_endpoint()
