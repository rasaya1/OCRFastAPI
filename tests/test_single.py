#!/usr/bin/env python3
"""Test script to check OCR on a single image"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import OCRProcessor

def test_single_image():
    # Find a sample image from the dataset
    dataset_path = Path(r"C:\Users\rasan\.cache\kagglehub\datasets\shaz13\real-world-documents-collections\versions\1")
    
    # Look for any image file
    image_files = list(dataset_path.rglob("*.jpg"))[:5]  # Get first 5 images
    
    if not image_files:
        print("No image files found in dataset")
        return
    
    # Test with both engines
    for engine in ['tesseract', 'easyocr']:
        print(f"\n=== Testing with {engine.upper()} ===")
        
        ocr = OCRProcessor(
            output_dir=f"test_{engine}",
            ocr_engine=engine,
            language='eng'
        )
        
        for i, img_path in enumerate(image_files):
            print(f"\nTesting image {i+1}: {img_path.name}")
            text, confidence = ocr.process_image(img_path)
            
            if text.strip():
                print(f"SUCCESS! Extracted text (confidence: {confidence:.1f}%):")
                print(f"Text preview: {text[:200]}...")
                break
            else:
                print("No text extracted")
        else:
            print(f"No text found in any of the {len(image_files)} test images with {engine}")

if __name__ == "__main__":
    test_single_image()