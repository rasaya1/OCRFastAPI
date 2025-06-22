import os
from pathlib import Path
import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance
import logging
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import easyocr
from scipy import ndimage
from skimage import filters, morphology

class OCRProcessor:
    def __init__(self, output_dir="output", ocr_engine="tesseract", language='eng'):
        """
        Initialize the OCR processor
        
        Args:
            output_dir (str): Directory to save output text files
            ocr_engine (str): OCR engine to use ('tesseract' or 'easyocr')
            language (str): Language for OCR processing
        """
        self.output_dir = output_dir
        self.ocr_engine = ocr_engine.lower()
        self.language = language
        self._setup_logging()
        self._setup_output_directory()
        
        if self.ocr_engine == 'easyocr':
            # Force language to be 'en' for EasyOCR (it uses 'en' not 'eng')
            self.reader = easyocr.Reader(['en'], gpu=False)

    def _setup_logging(self):
        """Configure logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def _setup_output_directory(self):
        """Create output directory if it doesn't exist"""
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def detect_layout(self, image):
        """Detect document layout type"""
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            img = img_array
        contours, _ = cv2.findContours(cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Analyze contour properties
        areas = [cv2.contourArea(c) for c in contours if cv2.contourArea(c) > 100]
        if not areas:
            return 'text'
        
        avg_area = np.mean(areas)
        area_std = np.std(areas)
        
        # Simple heuristic for layout detection
        if area_std / avg_area > 2.0:
            return 'mixed'  # Tables, forms, mixed content
        elif len(areas) > 50:
            return 'dense'  # Dense text, newspapers
        else:
            return 'text'   # Regular text documents

    def preprocess_image(self, image, layout_type='text'):
        """Simplified preprocessing for better OCR results"""
        img_array = np.array(image)
        
        # Handle different image formats
        if len(img_array.shape) == 3:
            # Color image
            if img_array.shape[2] == 4:  # RGBA
                img = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
            else:  # RGB
                img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            # Already grayscale
            gray = img_array
        
        # Simple preprocessing - just enhance contrast
        gray = cv2.convertScaleAbs(gray, alpha=1.2, beta=10)
        
        return Image.fromarray(gray)

    def process_with_tesseract(self, image, layout_type='text'):
        """Simplified Tesseract processing for better text extraction"""
        # Try multiple PSM modes
        psm_modes = ['--psm 6', '--psm 8', '--psm 4', '--psm 3']
        results = []
        
        for psm in psm_modes:
            try:
                # Simple approach without character whitelist
                text = pytesseract.image_to_string(image, config=psm)
                if text.strip():
                    results.append(text.strip())
            except:
                continue
        
        # Try with data extraction for confidence
        try:
            data = pytesseract.image_to_data(image, config='--psm 6', output_type=pytesseract.Output.DICT)
            text_parts, confidence_scores = [], []
            
            for i, conf in enumerate(data['conf']):
                if conf > 10 and data['text'][i].strip():  # Lower confidence threshold
                    text_parts.append(data['text'][i])
                    confidence_scores.append(float(conf))
            
            if text_parts:
                text = ' '.join(text_parts)
                avg_conf = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 50.0
                results.append(text.strip())
                return text.strip(), avg_conf
        except:
            pass
        
        # Return best result by length
        if results:
            best_text = max(results, key=len)
            return best_text, 60.0
        return "", 0.0

    def process_with_easyocr(self, image):
        """
        Process image using EasyOCR
        
        Args:
            image: PIL Image object
        
        Returns:
            tuple: (extracted text, confidence score)
        """
        # Convert PIL image to OpenCV format
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        else:
            img = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)
        
        # Get results from EasyOCR
        results = self.reader.readtext(img)
        
        text_parts = []
        confidence_scores = []
        
        for detection in results:
            text_parts.append(detection[1])
            confidence_scores.append(detection[2])
        
        text = ' '.join(text_parts)
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        
        return text.strip(), avg_confidence

    def process_image(self, image_path):
        """Process image with adaptive preprocessing"""
        try:
            image = Image.open(image_path)
            
            # Convert to RGB if needed
            if image.mode not in ('RGB', 'L'):
                image = image.convert('RGB')
            
            # Enhance image quality (only for color images)
            if image.mode == 'RGB':
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(1.2)
                enhancer = ImageEnhance.Sharpness(image)
                image = enhancer.enhance(1.1)
            
            # Detect layout type
            layout_type = self.detect_layout(image)
            
            # Preprocess based on layout
            processed_image = self.preprocess_image(image, layout_type)
            
            # Try both original and processed images
            results = []
            
            # Try original image first
            if self.ocr_engine == 'tesseract':
                text1, conf1 = self.process_with_tesseract(image, layout_type)
                if text1:
                    results.append((text1, conf1))
                
                # Try processed image
                text2, conf2 = self.process_with_tesseract(processed_image, layout_type)
                if text2:
                    results.append((text2, conf2))
            else:
                text1, conf1 = self.process_with_easyocr(image)
                if text1:
                    results.append((text1, conf1))
                
                text2, conf2 = self.process_with_easyocr(processed_image)
                if text2:
                    results.append((text2, conf2))
            
            # Return best result
            if results:
                return max(results, key=lambda x: len(x[0]))
            return "", 0.0
                
        except Exception as e:
            self.logger.error(f"Error processing image {image_path}: {str(e)}")
            return "", 0.0

    def process_pdf(self, pdf_path):
        """Process PDF with high-quality conversion and adaptive processing"""
        try:
            # Convert PDF to high-quality images
            images = convert_from_path(pdf_path, dpi=300, fmt='png')
            text_content, confidence_scores = [], []

            for i, image in enumerate(images):
                # Enhance image quality
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(1.2)
                
                # Detect layout for each page
                layout_type = self.detect_layout(image)
                processed_image = self.preprocess_image(image, layout_type)
                
                if self.ocr_engine == 'tesseract':
                    text, confidence = self.process_with_tesseract(processed_image, layout_type)
                else:
                    text, confidence = self.process_with_easyocr(processed_image)
                
                if text.strip():  # Only add non-empty pages
                    text_content.append(f"--- Page {i+1} ---\n{text}")
                    confidence_scores.append(confidence)

            full_text = "\n\n".join(text_content)
            avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
            
            return full_text, avg_confidence
            
        except Exception as e:
            self.logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
            return "", 0.0

    def process_file(self, file_path):
        """
        Process a file (either PDF or image)
        
        Args:
            file_path (str): Path to the file
        """
        file_path = Path(file_path)
        output_file = Path(self.output_dir) / f"{file_path.stem}.txt"
        metadata_file = Path(self.output_dir) / f"{file_path.stem}_metadata.txt"

        self.logger.info(f"Processing file: {file_path}")

        # Determine file type and process accordingly
        if file_path.suffix.lower() == '.pdf':
            text, confidence = self.process_pdf(file_path)
        elif file_path.suffix.lower() in ('.png', '.jpg', '.jpeg', '.tiff', '.bmp'):
            text, confidence = self.process_image(file_path)
        else:
            self.logger.warning(f"Unsupported file type: {file_path}")
            return

        # Save the extracted text and metadata
        if text:
            # Save the main text
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            # Save metadata
            with open(metadata_file, 'w', encoding='utf-8') as f:
                f.write(f"File: {file_path.name}\n")
                f.write(f"OCR Engine: {self.ocr_engine}\n")
                f.write(f"Confidence Score: {confidence:.2f}%\n")
                f.write(f"Language: {self.language}\n")
            
            self.logger.info(f"Text saved to: {output_file}")
            self.logger.info(f"Confidence Score: {confidence:.2f}%")
        else:
            self.logger.warning(f"No text extracted from: {file_path}")

    def batch_process(self, input_dir, max_workers=4):
        """
        Process all supported files in a directory using parallel processing
        
        Args:
            input_dir (str): Directory containing files to process
            max_workers (int): Maximum number of parallel workers
        """
        input_path = Path(input_dir)
        supported_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
        
        # Get list of all supported files (recursive search)
        files_to_process = [
            f for f in input_path.rglob('*') 
            if f.is_file() and f.suffix.lower() in supported_extensions
        ]
        
        if not files_to_process:
            self.logger.warning(f"No supported files found in {input_dir}")
            return
        
        self.logger.info(f"Found {len(files_to_process)} files to process")
        
        # Process files in parallel with progress bar
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            list(tqdm(
                executor.map(self.process_file, files_to_process),
                total=len(files_to_process),
                desc="Processing files"
            ))

def main():
    import argparse
    from kaggle_datasets import KaggleDatasetManager
    
    parser = argparse.ArgumentParser(description='Advanced OCR Text Extraction')
    parser.add_argument('input_path', nargs='?', help='Input file or directory path')
    parser.add_argument('--output', '-o', default='extracted_text', help='Output directory')
    parser.add_argument('--engine', '-e', choices=['tesseract', 'easyocr'], default='tesseract', help='OCR engine')
    parser.add_argument('--language', '-l', default='eng', help='Language code')
    parser.add_argument('--workers', '-w', type=int, default=4, help='Number of parallel workers')
    
    # Kaggle integration
    parser.add_argument('--kaggle-dataset', '-k', help='Kaggle dataset ID (e.g., shaz13/real-world-documents-collections)')
    parser.add_argument('--popular-dataset', '-p', choices=['real-world-docs', 'handwritten-text', 'invoice-ocr', 'receipt-ocr', 'document-images'], help='Download popular OCR dataset')
    parser.add_argument('--list-datasets', action='store_true', help='List available popular datasets')
    
    args = parser.parse_args()
    
    # Handle dataset listing
    if args.list_datasets:
        kaggle_manager = KaggleDatasetManager()
        datasets = kaggle_manager.get_popular_ocr_datasets()
        print("\nAvailable popular OCR datasets:")
        for name, dataset_id in datasets.items():
            print(f"  {name}: {dataset_id}")
        print("\nUsage: python main.py --popular-dataset real-world-docs")
        return
    
    # Handle Kaggle dataset download
    input_path = None
    if args.kaggle_dataset or args.popular_dataset:
        kaggle_manager = KaggleDatasetManager()
        
        if args.kaggle_dataset:
            dataset_path = kaggle_manager.download_dataset(args.kaggle_dataset)
        else:
            dataset_path = kaggle_manager.download_popular_dataset(args.popular_dataset)
        
        if dataset_path:
            input_path = Path(dataset_path)
            print(f"Using downloaded dataset: {input_path}")
        else:
            print("Failed to download dataset")
            return
    elif args.input_path:
        input_path = Path(args.input_path)
    else:
        parser.error("Must provide input_path, --kaggle-dataset, or --popular-dataset")
    
    # Initialize OCR processor
    ocr = OCRProcessor(
        output_dir=args.output,
        ocr_engine=args.engine,
        language=args.language
    )
    
    # Process files
    if input_path.is_file():
        ocr.process_file(input_path)
    elif input_path.is_dir():
        ocr.batch_process(input_path, max_workers=args.workers)
    else:
        print(f"Error: {input_path} is not a valid file or directory")

if __name__ == "__main__":
    main()
