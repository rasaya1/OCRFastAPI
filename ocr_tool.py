#!/usr/bin/env python3
"""
Advanced OCR Text Extraction Tool
Entry point script for the OCR processing system
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run main function
from main import main

if __name__ == "__main__":
    main()