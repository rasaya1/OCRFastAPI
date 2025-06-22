"""
FastAPI application for document processing and entity extraction
"""

import os
import time
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
import asyncio

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

from main import OCRProcessor
from vector_db import VectorDatabase
from entity_extractor import LocalEntityExtractor

app = FastAPI(
    title="Document Processing API",
    description="OCR, classification, and entity extraction API",
    version="1.0.0"
)

# Initialize components
ocr_processor = OCRProcessor(ocr_engine="tesseract")
vector_db = VectorDatabase("api_vector_db")
entity_extractor = LocalEntityExtractor()

ALLOWED_EXTENSIONS = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp'}

@app.post("/extract_entities/")
async def extract_entities(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Extract entities from uploaded document
    """
    start_time = time.time()
    
    try:
        # Validate file format
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        try:
            # Process with OCR
            if file_ext == '.pdf':
                text, ocr_confidence = ocr_processor.process_pdf(temp_path)
            else:
                text, ocr_confidence = ocr_processor.process_image(temp_path)
            
            if not text.strip():
                raise HTTPException(status_code=422, detail="No text extracted from document")
            
            # Classify document type using vector database
            doc_type, classification_confidence = await classify_document(text)
            
            # Extract entities based on document type
            entities = await entity_extractor.extract_entities(text, doc_type)
            
            processing_time = time.time() - start_time
            
            return {
                "document_type": doc_type,
                "confidence": round(classification_confidence, 3),
                "entities": entities,
                "processing_time": f"{processing_time:.2f}s"
            }
            
        finally:
            # Clean up temporary file
            os.unlink(temp_path)
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

async def classify_document(text: str) -> tuple[str, float]:
    """
    Classify document type using vector database similarity search
    """
    try:
        # Search for similar documents
        results = vector_db.search_similar(text, k=1)
        
        if results:
            metadata, confidence = results[0]
            return metadata.document_type, confidence
        else:
            # Fallback classification
            return vector_db._detect_document_type(text), 0.5
            
    except Exception:
        # Fallback to simple keyword-based classification
        return vector_db._detect_document_type(text), 0.3

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/stats")
async def get_stats():
    """Get vector database statistics"""
    return vector_db.get_stats()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)