#!/usr/bin/env python3
"""
Demo script for vector database document search
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from vector_db import VectorDatabase, DocumentIndexer

def demo_vector_search():
    """Demonstrate vector database functionality"""
    print("Vector Database Demo")
    print("=" * 30)
    
    # Initialize vector database
    vector_db = VectorDatabase("demo_vector_db")
    indexer = DocumentIndexer(vector_db)
    
    # Index existing OCR output files
    output_dir = Path("../output")
    if output_dir.exists():
        print(f"Indexing documents from {output_dir}...")
        indexed = indexer.index_directory(str(output_dir))
        print(f"Successfully indexed {indexed} documents")
    else:
        print("No output directory found. Run OCR processing first.")
        return
    
    # Save the database
    vector_db.save()
    
    # Interactive search demo
    print("\n" + "=" * 50)
    print("DOCUMENT SEARCH DEMO")
    print("=" * 50)
    
    # Predefined queries for demo
    demo_queries = [
        "invoice payment amount",
        "business services professional",
        "tax total calculation",
        "company contact information",
        "due date payment terms"
    ]
    
    print("\nRunning demo searches...")
    for query in demo_queries:
        print(f"\nQuery: '{query}'")
        results = vector_db.search_similar(query, k=3)
        
        if results:
            for i, (metadata, score) in enumerate(results, 1):
                print(f"  {i}. {Path(metadata.file_path).name}")
                print(f"     Type: {metadata.document_type} | Score: {score:.3f}")
                print(f"     Preview: {metadata.text_preview[:80]}...")
        else:
            print("  No results found")
    
    # Show database statistics
    print(f"\n" + "=" * 30)
    print("DATABASE STATISTICS")
    print("=" * 30)
    stats = vector_db.get_stats()
    print(f"Total documents: {stats['total_documents']}")
    print(f"Embedding dimension: {stats['embedding_dimension']}")
    print("Document types:")
    for doc_type, count in stats['document_types'].items():
        print(f"  - {doc_type}: {count}")
    
    # Interactive search
    print(f"\n" + "=" * 30)
    print("INTERACTIVE SEARCH")
    print("=" * 30)
    print("Enter search queries (or 'quit' to exit):")
    
    while True:
        try:
            query = input("\nSearch query: ").strip()
            if query.lower() in ['quit', 'exit', 'q']:
                break
            
            if not query:
                continue
            
            results = vector_db.search_similar(query, k=5)
            
            if results:
                print(f"\nFound {len(results)} similar documents:")
                for i, (metadata, score) in enumerate(results, 1):
                    print(f"\n{i}. {Path(metadata.file_path).name}")
                    print(f"   Type: {metadata.document_type}")
                    print(f"   Similarity: {score:.3f}")
                    print(f"   Preview: {metadata.text_preview}")
            else:
                print("No similar documents found.")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("\nDemo completed!")

if __name__ == "__main__":
    demo_vector_search()