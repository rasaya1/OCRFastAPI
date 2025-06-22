#!/usr/bin/env python3
"""
Simple document search utility using vector database
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from vector_db import VectorDatabase

def search_documents(query, db_path="quick_demo_db", top_k=3):
    """Search documents using vector similarity"""
    try:
        # Load existing database
        vector_db = VectorDatabase(db_path)
        
        if vector_db.get_stats()['total_documents'] == 0:
            print("No documents found in database. Run quick_vector_demo.py first.")
            return
        
        # Perform search
        results = vector_db.search_similar(query, k=top_k)
        
        print(f"Search Results for: '{query}'")
        print("=" * 50)
        
        if results:
            for i, (metadata, score) in enumerate(results, 1):
                print(f"\n{i}. {Path(metadata.file_path).name}")
                print(f"   Type: {metadata.document_type}")
                print(f"   Similarity: {score:.3f}")
                print(f"   Preview: {metadata.text_preview[:100]}...")
        else:
            print("No similar documents found.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        search_documents(query)
    else:
        # Demo searches
        demo_queries = [
            "professional services",
            "payment terms net 30",
            "software license",
            "tax calculation",
            "business address"
        ]
        
        for query in demo_queries:
            search_documents(query, top_k=2)
            print("\n" + "-" * 50 + "\n")