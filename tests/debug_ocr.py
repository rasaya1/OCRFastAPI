#!/usr/bin/env python3
"""Debug OCR issues"""

import pytesseract
from PIL import Image
import cv2
import numpy as np
from pathlib import Path

def debug_single_image():
    # Find a sample image
    dataset_path = Path(r"C:\Users\rasan\.cache\kagglehub\datasets\shaz13\real-world-documents-collections\versions\1")
    image_files = list(dataset_path.rglob("*.jpg"))[:3]
    
    for img_path in image_files:
        print(f"\n=== Debugging: {img_path.name} ===")
        
        try:
            # Load image
            image = Image.open(img_path)
            print(f"Image mode: {image.mode}, Size: {image.size}")
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Try direct OCR without preprocessing
            print("Trying direct OCR...")
            text1 = pytesseract.image_to_string(image)
            print(f"Direct result: '{text1.strip()}'")
            
            # Try with different PSM
            print("Trying PSM 8...")
            text2 = pytesseract.image_to_string(image, config='--psm 8')
            print(f"PSM 8 result: '{text2.strip()}'")
            
            # Try with PSM 13 (raw line)
            print("Trying PSM 13...")
            text3 = pytesseract.image_to_string(image, config='--psm 13')
            print(f"PSM 13 result: '{text3.strip()}'")
            
            # Check if image has any text-like regions
            img_array = np.array(image)
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Simple threshold
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            
            # Count black vs white pixels
            black_pixels = np.sum(thresh == 0)
            white_pixels = np.sum(thresh == 255)
            total_pixels = thresh.size
            
            print(f"Image analysis:")
            print(f"  Black pixels: {black_pixels} ({black_pixels/total_pixels*100:.1f}%)")
            print(f"  White pixels: {white_pixels} ({white_pixels/total_pixels*100:.1f}%)")
            
            if any(text.strip() for text in [text1, text2, text3]):
                print("SUCCESS: Found some text!")
                break
            else:
                print("No text found with any method")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    debug_single_image()