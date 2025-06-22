#!/usr/bin/env python3
"""
Simple API test without starting server
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from api import app
from fastapi.testclient import TestClient

def test_api_endpoints():
    """Test API endpoints using TestClient"""
    
    client = TestClient(app)
    
    # Test health endpoint
    print("Testing health endpoint...")
    response = client.get("/health")
    print(f"Health check: {response.json()}")
    
    # Test stats endpoint
    print("\nTesting stats endpoint...")
    response = client.get("/stats")
    print(f"Database stats: {response.json()}")
    
    # Test document processing with sample text file
    print("\nTesting document processing...")
    
    sample_file = Path("../output/sample_invoice.txt")
    if sample_file.exists():
        with open(sample_file, 'rb') as f:
            files = {'file': ('sample_invoice.txt', f, 'text/plain')}
            response = client.post("/extract_entities/", files=files)
            
        if response.status_code == 200:
            result = response.json()
            print("Invoice processing result:")
            print(f"Document Type: {result['document_type']}")
            print(f"Confidence: {result['confidence']}")
            print(f"Entities: {result['entities']}")
            print(f"Processing Time: {result['processing_time']}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    else:
        print("Sample invoice file not found")

if __name__ == "__main__":
    test_api_endpoints()