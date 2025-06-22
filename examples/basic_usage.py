#!/usr/bin/env python3
"""
Basic usage examples for Advanced OCR Text Extraction
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import OCRProcessor

def example_single_file():
    """Example: Process a single file"""
    print("=== Example 1: Single File Processing ===")
    
    # Initialize OCR processor
    ocr = OCRProcessor(
        output_dir="output/single_file_results",
        ocr_engine="tesseract",
        language="eng"
    )
    
    # Process a single file (replace with your file path)
    file_path = "path/to/your/document.pdf"
    if Path(file_path).exists():
        ocr.process_file(file_path)
        print(f"Processed: {file_path}")
    else:
        print(f"File not found: {file_path}")

def example_batch_processing():
    """Example: Batch process directory"""
    print("\n=== Example 2: Batch Processing ===")
    
    # Initialize OCR processor with EasyOCR
    ocr = OCRProcessor(
        output_dir="output/batch_results",
        ocr_engine="easyocr",
        language="en"
    )
    
    # Process all files in a directory
    input_dir = "path/to/your/documents"
    if Path(input_dir).exists():
        ocr.batch_process(input_dir, max_workers=4)
        print(f"Batch processed: {input_dir}")
    else:
        print(f"Directory not found: {input_dir}")

def example_different_languages():
    """Example: Process documents in different languages"""
    print("\n=== Example 3: Multi-language Processing ===")
    
    languages = {
        "english": ("eng", "en"),
        "french": ("fra", "fr"),
        "german": ("deu", "de"),
        "spanish": ("spa", "es")
    }
    
    for lang_name, (tesseract_code, easyocr_code) in languages.items():
        print(f"\nProcessing {lang_name} documents:")
        
        # Tesseract example
        ocr_tesseract = OCRProcessor(
            output_dir=f"output/{lang_name}_tesseract",
            ocr_engine="tesseract",
            language=tesseract_code
        )
        
        # EasyOCR example
        ocr_easyocr = OCRProcessor(
            output_dir=f"output/{lang_name}_easyocr",
            ocr_engine="easyocr",
            language=easyocr_code
        )
        
        print(f"  Tesseract language code: {tesseract_code}")
        print(f"  EasyOCR language code: {easyocr_code}")

def example_kaggle_integration():
    """Example: Using Kaggle datasets"""
    print("\n=== Example 4: Kaggle Dataset Integration ===")
    
    from kaggle_datasets import KaggleDatasetManager
    
    # Initialize Kaggle manager
    kaggle_manager = KaggleDatasetManager()
    
    # List available datasets
    datasets = kaggle_manager.get_popular_ocr_datasets()
    print("Available datasets:")
    for name, dataset_id in datasets.items():
        print(f"  {name}: {dataset_id}")
    
    # Download and process a dataset
    dataset_name = "real-world-docs"
    print(f"\nDownloading {dataset_name}...")
    dataset_path = kaggle_manager.download_popular_dataset(dataset_name)
    
    if dataset_path:
        print(f"Dataset downloaded to: {dataset_path}")
        
        # Process the dataset
        ocr = OCRProcessor(
            output_dir=f"output/{dataset_name}_results",
            ocr_engine="tesseract",
            language="eng"
        )
        
        ocr.batch_process(dataset_path, max_workers=2)
        print("Dataset processing completed!")
    else:
        print("Failed to download dataset")

if __name__ == "__main__":
    print("Advanced OCR Text Extraction - Usage Examples")
    print("=" * 50)
    
    # Run examples (comment out the ones you don't want to run)
    example_single_file()
    example_batch_processing()
    example_different_languages()
    # example_kaggle_integration()  # Uncomment if you have Kaggle API set up
    
    print("\n" + "=" * 50)
    print("Examples completed! Check the output directory for results.")