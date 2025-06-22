"""
Vector Database Implementation for OCR Document Indexing
"""

import os
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import faiss
from sentence_transformers import SentenceTransformer
import pickle
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DocumentMetadata:
    """Document metadata structure"""
    file_path: str
    document_type: str
    confidence_score: float
    processed_date: str
    text_preview: str

class VectorDatabase:
    """FAISS-based vector database for document similarity search"""
    
    def __init__(self, db_path: str = "vector_db", model_name: str = "all-MiniLM-L6-v2"):
        self.db_path = Path(db_path)
        self.db_path.mkdir(exist_ok=True)
        
        # Initialize embedding model
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        
        # Initialize FAISS index
        self.index = faiss.IndexFlatIP(self.embedding_dim)  # Inner product for cosine similarity
        self.metadata = []
        
        # Load existing database if available
        self._load_database()
    
    def _load_database(self):
        """Load existing database from disk"""
        index_path = self.db_path / "faiss_index.bin"
        metadata_path = self.db_path / "metadata.pkl"
        
        if index_path.exists() and metadata_path.exists():
            self.index = faiss.read_index(str(index_path))
            with open(metadata_path, 'rb') as f:
                self.metadata = pickle.load(f)
            print(f"Loaded database with {len(self.metadata)} documents")
    
    def _save_database(self):
        """Save database to disk"""
        index_path = self.db_path / "faiss_index.bin"
        metadata_path = self.db_path / "metadata.pkl"
        
        faiss.write_index(self.index, str(index_path))
        with open(metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)
    
    def _detect_document_type(self, text: str) -> str:
        """Simple document type detection based on keywords"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['service agreement', 'contract', 'agreement']):
            return 'contract'
        elif any(word in text_lower for word in ['purchase order', 'po number']):
            return 'purchase_order'
        elif any(word in text_lower for word in ['quarterly report', 'business report', 'executive summary']):
            return 'report'
        elif any(word in text_lower for word in ['receipt', 'store name', 'transaction']):
            return 'receipt'
        elif any(word in text_lower for word in ['invoice', 'bill to']):
            return 'invoice'
        else:
            return 'document'
    
    def add_document(self, text: str, file_path: str, confidence_score: float = 0.0):
        """Add a document to the vector database"""
        # Generate embedding
        embedding = self.model.encode([text], normalize_embeddings=True)
        
        # Detect document type
        doc_type = self._detect_document_type(text)
        
        # Create metadata
        metadata = DocumentMetadata(
            file_path=file_path,
            document_type=doc_type,
            confidence_score=confidence_score,
            processed_date=datetime.now().isoformat(),
            text_preview=text[:200] + "..." if len(text) > 200 else text
        )
        
        # Add to index
        self.index.add(embedding.astype(np.float32))
        self.metadata.append(metadata)
        
        print(f"Added {doc_type} document: {Path(file_path).name}")
        return len(self.metadata) - 1
    
    def search_similar(self, query: str, k: int = 5) -> List[Tuple[DocumentMetadata, float]]:
        """Search for similar documents"""
        if self.index.ntotal == 0:
            return []
        
        # Generate query embedding
        query_embedding = self.model.encode([query], normalize_embeddings=True)
        
        # Search
        scores, indices = self.index.search(query_embedding.astype(np.float32), min(k, self.index.ntotal))
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1:  # Valid result
                results.append((self.metadata[idx], float(score)))
        
        return results
    
    def get_documents_by_type(self, doc_type: str) -> List[DocumentMetadata]:
        """Get all documents of a specific type"""
        return [meta for meta in self.metadata if meta.document_type == doc_type]
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        type_counts = {}
        for meta in self.metadata:
            type_counts[meta.document_type] = type_counts.get(meta.document_type, 0) + 1
        
        return {
            'total_documents': len(self.metadata),
            'document_types': type_counts,
            'embedding_dimension': self.embedding_dim
        }
    
    def save(self):
        """Save database to disk"""
        self._save_database()
        print(f"Database saved to {self.db_path}")

class DocumentIndexer:
    """Document indexer that processes OCR results and adds to vector database"""
    
    def __init__(self, vector_db: VectorDatabase, ocr_processor=None):
        self.vector_db = vector_db
        self.ocr_processor = ocr_processor
    
    def index_text_file(self, file_path: str):
        """Index a text file directly"""
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        if text.strip():
            self.vector_db.add_document(text, file_path)
            return True
        return False
    
    def index_directory(self, directory: str, file_pattern: str = "*.txt"):
        """Index all text files in a directory"""
        directory = Path(directory)
        files = list(directory.glob(file_pattern))
        
        indexed_count = 0
        for file_path in files:
            if self.index_text_file(str(file_path)):
                indexed_count += 1
        
        print(f"Indexed {indexed_count} files from {directory}")
        return indexed_count
    
    def index_with_ocr(self, file_path: str):
        """Process file with OCR and add to index"""
        if not self.ocr_processor:
            raise ValueError("OCR processor not provided")
        
        text, confidence = self.ocr_processor.process_file(file_path)
        if text.strip():
            self.vector_db.add_document(text, file_path, confidence)
            return True
        return False

def main():
    """Demo of vector database functionality"""
    # Initialize vector database
    vector_db = VectorDatabase("demo_vector_db")
    indexer = DocumentIndexer(vector_db)
    
    # Index sample documents
    output_dir = Path("output")
    if output_dir.exists():
        indexed = indexer.index_directory(str(output_dir))
        print(f"Indexed {indexed} documents")
    
    # Save database
    vector_db.save()
    
    # Demo search
    print("\n=== Search Demo ===")
    queries = [
        "invoice payment terms",
        "business services",
        "total amount due"
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        results = vector_db.search_similar(query, k=3)
        
        for i, (metadata, score) in enumerate(results, 1):
            print(f"  {i}. {Path(metadata.file_path).name} ({metadata.document_type}) - Score: {score:.3f}")
            print(f"     Preview: {metadata.text_preview[:100]}...")
    
    # Show statistics
    print(f"\n=== Database Stats ===")
    stats = vector_db.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()