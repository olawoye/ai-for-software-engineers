"""
Lesson 4.3 TODO: The Vector Store Lab

In this lesson, you'll build the retrieval layer for RAG systems.
Your goal: implement the core semantic_search() template method that
consumes embedded chunks from Lesson 4.2 and executes efficient searches.

This method should support NumPy (always available) and optional FAISS backend.

PHASE 1: Core Template Method (semantic_search)
  - Accept embedded_chunks, query_embedding, top_k, use_faiss, metadata_filter
  - Initialize VectorStore with proper embedding dimensions
  - Extract and add chunks to the store
  - Execute similarity search and rank results
  - Return structured results with similarity scores

PHASE 2: Performance Comparison Helper (compare_search_backends)
  - Test NumPy vs FAISS search performance
  - Measure timing and count results
  - Calculate speedup ratio

PHASE 3: Demonstrations
  - demo_core_method(): Execute semantic_search() on sample embedded chunks
  - demo_vector_store_backends(): Compare NumPy vs FAISS performance
  - demo_metadata_filtering(): Filter search results by metadata
  - demo_vector_store_options(): Overview of production vector store options

REFERENCE:
  - Completed implementation: project-completed/module-04-practical-rag-context-engineering/lesson-03-vector-store-lab.py
  - VectorStore class: shared/vector_store.py
  - Embedding utilities: shared/embeddings.py (batch_similarity)
  - Lesson 4.2: lesson-02-embedding-your-data.py (embedded chunks format)
  - Business scenario: Efficiently search millions of company policy documents
"""

import numpy as np
import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Tuple

# Import from shared module
sys.path.insert(0, str(Path(__file__).parent))
from shared.embeddings import EmbeddingEngine, batch_similarity
from shared.vector_store import VectorStore


# ============================================================================
# PHASE 1: Core Template Method - semantic_search()
# ============================================================================
# TODO: Implement the core semantic_search() function
# 
# Requirements:
#   1. Accept: embedded_chunks, query_embedding, top_k, use_faiss, metadata_filter
#   2. Initialize VectorStore with correct embedding dimensions
#   3. Extract texts, embeddings, metadata, and chunk IDs from embedded_chunks
#   4. Add all chunks to the vector store
#   5. Execute vector_store.search() to find similar chunks
#   6. Apply metadata filtering if provided (optional filter param)
#   7. Return list of result dicts with rank, chunk_id, text, similarity, metadata
# 
# Hints:
#   - embedded_chunks[0]['embedding'].shape[0] gives embedding dimensions
#   - vector_store.search(query_embedding, top_k) returns tuples: (text, sim, meta)
#   - Enumerate results to add 1-indexed rank
#   - Metadata filtering: only keep results where meta matches filter dict
#   - Return type should match results from demo_core_method()

def semantic_search(
    embedded_chunks: List[Dict],
    query_embedding: np.ndarray,
    top_k: int = 5,
    use_faiss: bool = False,
    metadata_filter: Dict | None = None,
) -> List[Dict]:
    """TODO: Store embeddings and execute semantic search.
    
    Args:
        embedded_chunks: List of dicts with {chunk_id, text, embedding, metadata, char_count}
        query_embedding: Query vector to search for
        top_k: Number of top results to return
        use_faiss: Use FAISS for large-scale retrieval (optional)
        metadata_filter: Dict to filter results by metadata (optional)
    
    Returns:
        List of result dicts: {rank, chunk_id, text, similarity, metadata}
    """
    # TODO: PHASE 1 implementation


# ============================================================================
# PHASE 2: Performance Comparison Helper - compare_search_backends()
# ============================================================================
# TODO: Compare NumPy vs FAISS search performance
# 
# Requirements:
#   1. Measure time for semantic_search() with use_faiss=False (NumPy)
#   2. Measure time for semantic_search() with use_faiss=True (FAISS)
#   3. Catch exceptions (FAISS may not be installed)
#   4. Calculate speedup: numpy_time / faiss_time
#   5. Return dict with timing and speedup information
# 
# Hints:
#   - Use time.time() before and after semantic_search() calls
#   - Store results in dict with keys: 'numpy', 'faiss', 'speedup'
#   - Each entry should have 'time' (in seconds) and 'results' (count)
#   - Wrap FAISS in try/except to handle missing dependency

def compare_search_backends(
    embedded_chunks: List[Dict],
    query_embedding: np.ndarray,
    top_k: int = 5,
) -> Dict:
    """TODO: Compare NumPy vs FAISS search performance.
    
    Args:
        embedded_chunks: Embedded chunks to search
        query_embedding: Query vector
        top_k: Number of results
    
    Returns:
        Dict with timing comparisons: {numpy: {...}, faiss: {...}, speedup: float}
    """
    # TODO: PHASE 2 implementation


# ============================================================================
# PHASE 3: Demonstration Functions
# ============================================================================

def demo_core_method():
    """TODO: Demonstrate the semantic_search() template method.
    
    Steps:
    1. Create 4-5 sample documents (company benefits, policies, etc.)
    2. Use TF-IDF to generate embeddings (always available)
    3. Build embedded_chunks list matching Lesson 4.2 output format
    4. Create a query and embed it
    5. Call semantic_search() with the embedded chunks
    6. Print rank, similarity, and text for top results
    7. Return embedded_chunks for use in demo_vector_store_backends()
    """
    # TODO: PHASE 3.1 implementation


def demo_vector_store_backends():
    """TODO: Compare in-memory NumPy vs FAISS backends.
    
    Steps:
    1. Create 8+ sample documents (languages, frameworks, etc.)
    2. Generate embeddings and embedded_chunks structure
    3. Create a query embedding
    4. Call compare_search_backends() to measure both backends
    5. Print timing results and speedup ratio
    6. Note: If FAISS unavailable, explain graceful fallback
    
    Hints:
    - Use a larger document set to see performance differences
    - Print results in milliseconds for readability
    - Note that FAISS requires: pip install faiss-cpu
    """
    # TODO: PHASE 3.2 implementation


def demo_metadata_filtering():
    """TODO: Demonstrate filtering search results by metadata.
    
    Steps:
    1. Create 6+ documents with rich metadata (category, type, etc.)
    2. Build embedded_chunks with metadata dicts
    3. Search without filter: call semantic_search() normally
    4. Search with filter: call semantic_search(metadata_filter={'category': 'compensation'})
    5. Compare result counts and display filtered results
    
    Hints:
    - Use different metadata categories (benefits, compensation, policies, etc.)
    - metadata_filter param is a dict like {'category': 'health'}
    - Only results matching ALL filter conditions should return
    """
    # TODO: PHASE 3.3 implementation


def demo_vector_store_options():
    """TODO: Show overview of production vector store options.
    
    Print a comparison table/list of vector store implementations:
    - In-Memory (NumPy): pros/cons, when to use
    - FAISS: pros/cons, when to use
    - ChromaDB: pros/cons, when to use
    - Pinecone: pros/cons, when to use
    - Weaviate or Qdrant: pros/cons, when to use
    
    This is a reference guide, not interactive code.
    
    Hints:
    - Use structured text with emojis/symbols for readability
    - Include pros (✓), cons (✗), and use case
    - Note tradeoffs: cost vs scale, setup vs performance
    """
    # TODO: PHASE 3.4 implementation


if __name__ == "__main__":
    # TODO: Call all demo functions
    # 1. embedded_chunks, results = demo_core_method()
    # 2. demo_vector_store_backends()
    # 3. demo_metadata_filtering()
    # 4. demo_vector_store_options()
    # 5. Print completion message
    pass
