#!/usr/bin/env python3
"""
Fresh vector database demo with diverse documents
"""

import sys
from pathlib import Path
import shutil

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from vector_db import VectorDatabase, DocumentIndexer

def fresh_demo():
    """Fresh demonstration with diverse document types"""
    print("Fresh Vector Database Demo")
    print("=" * 40)
    
    # Remove old database
    db_path = Path("fresh_demo_db")
    if db_path.exists():
        shutil.rmtree(db_path)
    
    # Initialize new vector database
    vector_db = VectorDatabase("fresh_demo_db")
    indexer = DocumentIndexer(vector_db)
    
    # Index all documents
    output_dir = Path("output")
    if output_dir.exists():
        print(f"Indexing documents from {output_dir}...")
        indexed = indexer.index_directory(str(output_dir))
        print(f"Indexed {indexed} documents")
    
    # Save database
    vector_db.save()
    
    # Show stats
    stats = vector_db.get_stats()
    print(f"\nDatabase Statistics:")
    print(f"- Total documents: {stats['total_documents']}")
    print(f"- Document types: {stats['document_types']}")
    
    # Demo searches with diverse queries
    if stats['total_documents'] > 0:
        print(f"\nDemo Searches:")
        queries = [
            "service agreement contract",
            "quarterly business report", 
            "purchase order office supplies",
            "invoice payment terms",
            "financial performance revenue"
        ]
        
        for query in queries:
            print(f"\nQuery: '{query}'")
            results = vector_db.search_similar(query, k=3)
            
            for i, (metadata, score) in enumerate(results, 1):
                print(f"  {i}. {Path(metadata.file_path).name} ({metadata.document_type}) - {score:.3f}")
    
    print(f"\nDemo completed! Database saved to fresh_demo_db/")

if __name__ == "__main__":
    fresh_demo()