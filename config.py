"""
Configuration settings for Advanced OCR Text Extraction
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
OUTPUT_DIR = PROJECT_ROOT / "output"
TESTS_DIR = PROJECT_ROOT / "tests"
DOCS_DIR = PROJECT_ROOT / "docs"
EXAMPLES_DIR = PROJECT_ROOT / "examples"

# Default settings
DEFAULT_OCR_ENGINE = "tesseract"
DEFAULT_LANGUAGE = "eng"
DEFAULT_OUTPUT_DIR = "output"
DEFAULT_WORKERS = 4

# OCR Engine settings
TESSERACT_CONFIG = {
    "psm_modes": ["--psm 6", "--psm 8", "--psm 4", "--psm 3"],
    "confidence_threshold": 10,
    "default_confidence": 60.0
}

EASYOCR_CONFIG = {
    "gpu": True,  # Use GPU if available
    "confidence_threshold": 0.1
}

# Image processing settings
IMAGE_PROCESSING = {
    "dpi": 300,  # For PDF conversion
    "contrast_enhancement": 1.2,
    "sharpness_enhancement": 1.1,
    "supported_formats": {'.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
}

# Language mappings
LANGUAGE_MAPPING = {
    # Tesseract -> EasyOCR
    "eng": "en",
    "fra": "fr", 
    "deu": "de",
    "spa": "es",
    "chi_sim": "zh",
    "ara": "ar",
    "rus": "ru",
    "jpn": "ja",
    "kor": "ko"
}

# Kaggle dataset configurations
KAGGLE_DATASETS = {
    "real-world-docs": "shaz13/real-world-documents-collections",
    "handwritten-text": "landlord/handwriting-recognition",
    "invoice-ocr": "valakhorasani/invoice-ocr-dataset",
    "receipt-ocr": "urbikn/sroie-datasetreceipt-ocr",
    "document-images": "mathewnik90/document-images-dataset"
}

# System paths (will be auto-detected)
SYSTEM_PATHS = {
    "tesseract": None,  # Auto-detected from PATH
    "poppler": None     # Auto-detected from PATH
}

def get_tesseract_path():
    """Get Tesseract executable path"""
    import shutil
    return shutil.which("tesseract")

def get_poppler_path():
    """Get Poppler path"""
    import shutil
    return shutil.which("pdftoppm")

def validate_system_dependencies():
    """Validate that required system dependencies are available"""
    issues = []
    
    if not get_tesseract_path():
        issues.append("Tesseract OCR not found in PATH")
    
    if not get_poppler_path():
        issues.append("Poppler utilities not found in PATH")
    
    return issues

if __name__ == "__main__":
    print("Advanced OCR Configuration")
    print("=" * 30)
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Tesseract path: {get_tesseract_path()}")
    print(f"Poppler path: {get_poppler_path()}")
    
    issues = validate_system_dependencies()
    if issues:
        print("\nIssues found:")
        for issue in issues:
            print(f"  [X] {issue}")
    else:
        print("\n[OK] All system dependencies are available")