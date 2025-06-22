#!/usr/bin/env python3
"""
Test the web interface functionality
"""

import sys
from pathlib import Path
import io

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from fastapi.testclient import TestClient
from web_interface import app

def test_web_interface():
    """Test web interface endpoints"""
    
    client = TestClient(app)
    
    print("Testing Web Interface")
    print("=" * 40)
    
    # Test home page
    print("1. Testing home page...")
    response = client.get("/")
    if response.status_code == 200:
        print("[OK] Home page loads successfully")
        print(f"    Content length: {len(response.content)} bytes")
    else:
        print(f"[FAIL] Home page failed: {response.status_code}")
    
    # Test stats endpoint
    print("\n2. Testing stats API...")
    response = client.get("/api/stats")
    if response.status_code == 200:
        stats = response.json()
        print("[OK] Stats API working")
        print(f"    Database stats: {stats}")
    else:
        print(f"[FAIL] Stats API failed: {response.status_code}")
    
    # Test file upload with sample content
    print("\n3. Testing file upload...")
    
    # Create sample invoice content
    sample_content = """INVOICE
ABC Corporation
123 Business Street
New York, NY 10001

BILL TO: XYZ Company
Invoice #: INV-2024-001
Date: January 15, 2024

Professional Services: $6,000.00
TOTAL: $6,000.00"""
    
    # Test with PDF file (simulated)
    file_content = io.BytesIO(sample_content.encode('utf-8'))
    files = [('files', ('test_invoice.pdf', file_content, 'application/pdf'))]
    
    response = client.post("/upload", files=files)
    
    if response.status_code == 200:
        print("[OK] File upload processed successfully")
        print(f"    Response length: {len(response.content)} bytes")
        # Check if response contains expected elements
        content = response.content.decode('utf-8')
        if 'Processing Results' in content:
            print("[OK] Results page generated")
        if 'invoice' in content.lower():
            print("[OK] Document classification working")
    else:
        print(f"[FAIL] File upload failed: {response.status_code}")
        print(f"    Error: {response.text}")
    
    print("\n" + "=" * 40)
    print("Web Interface Test Complete")
    print("=" * 40)
    print("\nTo test manually:")
    print("1. Run: python start_web_app.py")
    print("2. Visit: http://localhost:8000")
    print("3. Upload documents and see results")

if __name__ == "__main__":
    test_web_interface()