#!/usr/bin/env python3
"""
API demonstration and testing script
"""

import requests
import json
from pathlib import Path

def test_api():
    """Test the document processing API"""
    
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    print("Testing health endpoint...")
    response = requests.get(f"{base_url}/health")
    print(f"Health check: {response.json()}")
    
    # Test stats endpoint
    print("\nTesting stats endpoint...")
    response = requests.get(f"{base_url}/stats")
    print(f"Database stats: {response.json()}")
    
    # Test document processing
    print("\nTesting document processing...")
    
    # Test with sample invoice
    sample_file = Path("output/sample_invoice.txt")
    if sample_file.exists():
        with open(sample_file, 'rb') as f:
            files = {'file': ('sample_invoice.txt', f, 'text/plain')}
            response = requests.post(f"{base_url}/extract_entities/", files=files)
            
        if response.status_code == 200:
            result = response.json()
            print("Invoice processing result:")
            print(json.dumps(result, indent=2))
        else:
            print(f"Error: {response.status_code} - {response.text}")
    
    # Test with sample receipt
    sample_file = Path("output/sample_receipt.txt")
    if sample_file.exists():
        with open(sample_file, 'rb') as f:
            files = {'file': ('sample_receipt.txt', f, 'text/plain')}
            response = requests.post(f"{base_url}/extract_entities/", files=files)
            
        if response.status_code == 200:
            result = response.json()
            print("\nReceipt processing result:")
            print(json.dumps(result, indent=2))
        else:
            print(f"Error: {response.status_code} - {response.text}")

def create_curl_examples():
    """Generate curl command examples"""
    
    examples = """
# API Testing Examples

## Health Check
curl -X GET "http://localhost:8000/health"

## Database Stats
curl -X GET "http://localhost:8000/stats"

## Process Invoice Document
curl -X POST "http://localhost:8000/extract_entities/" \\
  -H "accept: application/json" \\
  -H "Content-Type: multipart/form-data" \\
  -F "file=@output/sample_invoice.txt"

## Process Receipt Document
curl -X POST "http://localhost:8000/extract_entities/" \\
  -H "accept: application/json" \\
  -H "Content-Type: multipart/form-data" \\
  -F "file=@output/sample_receipt.txt"

## Process PDF Document
curl -X POST "http://localhost:8000/extract_entities/" \\
  -H "accept: application/json" \\
  -H "Content-Type: multipart/form-data" \\
  -F "file=@sample_document.pdf"
"""
    
    with open("api_examples.md", "w") as f:
        f.write(examples)
    
    print("Created api_examples.md with curl commands")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "examples":
        create_curl_examples()
    else:
        test_api()