#!/usr/bin/env python3
"""
Quick vector database demo without interactive components
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from vector_db import VectorDatabase, DocumentIndexer

def quick_demo():
    """Quick demonstration of vector database functionality"""
    print("Quick Vector Database Demo")
    print("=" * 40)
    
    # Initialize vector database
    vector_db = VectorDatabase("quick_demo_db")
    indexer = DocumentIndexer(vector_db)
    
    # Index sample documents
    output_dir = Path("../output")
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
    
    # Demo searches
    if stats['total_documents'] > 0:
        print(f"\nDemo Searches:")
        queries = [
            "invoice payment",
            "business services", 
            "total amount",
            "company address"
        ]
        
        for query in queries:
            print(f"\nQuery: '{query}'")
            results = vector_db.search_similar(query, k=2)
            
            for i, (metadata, score) in enumerate(results, 1):
                print(f"  {i}. {Path(metadata.file_path).name} ({metadata.document_type}) - {score:.3f}")
    
    print(f"\nDemo completed! Database saved to quick_demo_db/")

if __name__ == "__main__":
    quick_demo()