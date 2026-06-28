"""
Lesson 4.2 TODO: Embedding Your Data

In this lesson, you'll build the document ingestion pipeline for RAG systems.
Your goal: implement the core embed_documents() template method that chunks
raw text and generates embeddings via OpenRouter.

This method should be production-ready and reusable in your own projects.

PHASE 1: Core Template Method (embed_documents)
  - Accept documents, chunk_size, chunk_overlap, provider, and openrouter_key
  - Return a structured list of dicts with embeddings and metadata
  - Use the _smart_chunk helper to split text intelligently

PHASE 2: Smart Chunking Helper (_smart_chunk)
  - Split text by sentences to preserve logical boundaries
  - Implement overlap between chunks to maintain context
  - Filter out tiny chunks

PHASE 3: Demonstrations
  - demo_core_method(): Show the embed_documents() template in action
  - demo_semantic_search(): Query an embedded document collection
  - demo_chunking_strategies(): Visualize different chunk sizes
  - demo_provider_fallback(): Show provider priority (OpenRouter → Cohere → TF-IDF)

REFERENCE:
  - Completed implementation: project-completed/module-04-practical-rag-context-engineering/lesson-02-embedding-your-data.py
  - Embedding engine: shared/embeddings.py (updated for OpenRouter)
  - Settings: shared/utils/settings.py (provider config)
  - Business scenario: Transform company documentation into searchable knowledge base
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np

# Import from shared module
sys.path.insert(0, str(Path(__file__).parent))
from shared.embeddings import EmbeddingEngine, batch_similarity


# ============================================================================
# PHASE 1: Core Template Method - embed_documents()
# ============================================================================
# TODO: Implement the core embed_documents() function
# 
# Requirements:
#   1. Accept parameters: documents, chunk_size, chunk_overlap, provider, openrouter_key
#   2. Chunk documents using _smart_chunk helper
#   3. Initialize EmbeddingEngine with the chosen provider
#   4. Generate embeddings for all chunks
#   5. Return list of dicts: {chunk_id, text, embedding, metadata, char_count}
# 
# Hints:
#   - Use enumerate to track doc_idx and chunk_idx
#   - EmbeddingEngine.embed_documents() takes a list of strings
#   - Each result dict should have a unique chunk_id (e.g., "chunk_0_1")
#   - metadata dict should include provider, doc_idx, chunk_idx, char_count

def embed_documents(
    documents: List[str],
    chunk_size: int = 512,
    chunk_overlap: int = 50,
    provider: str = "openrouter",
    openrouter_key: str | None = None,
) -> List[Dict]:
    """TODO: Chunk documents and generate embeddings via OpenRouter or fallback.
    
    Args:
        documents: List of raw text documents
        chunk_size: Target characters per chunk
        chunk_overlap: Overlap between chunks
        provider: "openrouter", "cohere", or "tfidf"
        openrouter_key: OpenRouter API key (or from env OPENROUTER_API_KEY)
    
    Returns:
        List of dicts with chunk_id, text, embedding, metadata, char_count
    
    Example:
        >>> docs = ["Document text here...", "Another document..."]
        >>> chunks = embed_documents(docs, provider="openrouter")
        >>> print(f"Generated {len(chunks)} embedded chunks")
    """
    # TODO: PHASE 1 implementation


# ============================================================================
# PHASE 2: Smart Chunking Helper - _smart_chunk()
# ============================================================================
# TODO: Implement intelligent text chunking
# 
# Strategy:
#   1. Split by sentences (preserve logical boundaries)
#   2. Group sentences until chunk_size is reached
#   3. Add overlap between chunks for context preservation
#   4. Filter out tiny chunks (< 10 chars)
# 
# Hints:
#   - Use text.split('. ') to get sentences
#   - Track current_chunk and current_length as you build
#   - When reaching chunk_size, finalize and start with overlap
#   - Return a list of chunk strings

def _smart_chunk(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """TODO: Intelligently split text into overlapping chunks.
    
    Args:
        text: Raw text to chunk
        chunk_size: Target characters per chunk
        overlap: Character overlap between chunks
    
    Returns:
        List of chunk strings
    """
    # TODO: PHASE 2 implementation


# ============================================================================
# PHASE 3: Demonstration Functions
# ============================================================================

def demo_core_method():
    """TODO: Demonstrate the embed_documents() template method.
    
    Steps:
    1. Create 2-3 sample documents (company data, product info, policies)
    2. Call embed_documents() with chunk_size=256, provider="openrouter"
    3. Print statistics: number of chunks, avg chunk size, embedding dims
    4. Show sample chunk: ID, text snippet, first 5 embedding values
    5. Return the embedded_chunks for use in demo_semantic_search()
    """
    # TODO: PHASE 3.1 implementation


def demo_semantic_search(embedded_chunks: List[Dict]):
    """TODO: Demonstrate semantic search using embedded queries.
    
    Steps:
    1. Define a query string (e.g., "What is the remote work policy?")
    2. Call embed_documents() on the query with same chunk_size
    3. Use batch_similarity() to find top-3 matching chunks
    4. Display rank, similarity score, and chunk text for each result
    
    Hints:
    - query_embedding = embed_documents([query])[0]['embedding']
    - doc_embeddings = np.array([c['embedding'] for c in embedded_chunks])
    - similarities = batch_similarity(query_embedding, doc_embeddings)
    """
    # TODO: PHASE 3.2 implementation


def demo_chunking_strategies():
    """TODO: Show different chunking approaches and their effects.
    
    Steps:
    1. Define a sample multi-sentence text
    2. For each chunk_size in [100, 150, 300]:
       - Call _smart_chunk() to split the text
       - Print chunk count for this size
       - Show first 60 chars of each chunk
    3. Observe how chunk size affects splits
    """
    # TODO: PHASE 3.3 implementation


def demo_provider_fallback():
    """TODO: Show automatic fallback between embedding providers.
    
    Steps:
    1. Print provider priority: OpenRouter (1) → Cohere (2) → TF-IDF (3)
    2. Create 2 small test documents
    3. Call embed_documents() with provider="openrouter"
    4. Print which provider was actually used (check metadata)
    5. Note: If OpenRouter key is missing, Cohere is tried; if Cohere fails, TF-IDF is used
    """
    # TODO: PHASE 3.4 implementation


if __name__ == "__main__":
    # TODO: Call all demo functions
    # 1. embedded_chunks = demo_core_method()
    # 2. demo_semantic_search(embedded_chunks)
    # 3. demo_chunking_strategies()
    # 4. demo_provider_fallback()
    # 5. Print completion message
    pass
    """Run demonstrations."""
    print("\n" + "🚀 LESSON 4.2: EMBEDDING YOUR DATA".center(60, "="))

    try:
        demo_document_preparation()
        demo_embedding_generation()
        demo_vector_store_creation()

        print("\n" + "✅ Complete!".center(60, "="))

    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
