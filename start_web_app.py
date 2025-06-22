#!/usr/bin/env python3
"""
Start the web application with document processing interface
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

import uvicorn

if __name__ == "__main__":
    print("Starting Document Processing Web Application...")
    print("=" * 50)
    print("Web Interface: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("Upload documents and get instant results!")
    print("=" * 50)
    
    uvicorn.run("src.web_interface:app", host="0.0.0.0", port=8000, reload=True)