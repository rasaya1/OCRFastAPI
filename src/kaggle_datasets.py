import kagglehub
import os
from pathlib import Path
import logging

class KaggleDatasetManager:
    """Manage Kaggle dataset downloads for OCR processing"""
    
    def __init__(self, cache_dir="kaggle_datasets"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)
    
    def download_dataset(self, dataset_id, force_download=False):
        """Download Kaggle dataset"""
        try:
            if force_download:
                self.logger.info(f"Force downloading dataset: {dataset_id}")
            else:
                self.logger.info(f"Downloading dataset: {dataset_id}")
            
            path = kagglehub.dataset_download(dataset_id)
            self.logger.info(f"Dataset downloaded to: {path}")
            return path
        except Exception as e:
            self.logger.error(f"Failed to download dataset {dataset_id}: {str(e)}")
            return None
    
    def get_popular_ocr_datasets(self):
        """Return list of popular OCR datasets"""
        return {
            "real-world-docs": "shaz13/real-world-documents-collections",
            "handwritten-text": "landlord/handwriting-recognition",
            "invoice-ocr": "valakhorasani/invoice-ocr-dataset",
            "receipt-ocr": "urbikn/sroie-datasetreceipt-ocr",
            "document-images": "mathewnik90/document-images-dataset"
        }
    
    def download_popular_dataset(self, dataset_name):
        """Download a popular OCR dataset by name"""
        datasets = self.get_popular_ocr_datasets()
        if dataset_name in datasets:
            return self.download_dataset(datasets[dataset_name])
        else:
            available = ", ".join(datasets.keys())
            self.logger.error(f"Dataset '{dataset_name}' not found. Available: {available}")
            return None