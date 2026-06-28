"""
Lesson 4.2: Embedding Your Data

Learn how to prepare raw documents, chunk content appropriately,
generate embeddings via OpenRouter, and create a retrieval-ready knowledge base.

This lesson demonstrates the core embed_documents() template method that
learners can reuse in their own projects with minimal configuration changes.

Run: python lesson-02-embedding-your-data.py
     or: streamlit run lesson-02-embedding-your-data.py  (for interactive UI)
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np

# Import from shared module (reference path)
sys.path.insert(0, str(Path(__file__).parent))
from shared.embeddings import EmbeddingEngine, batch_similarity


# ============================================================================
# CORE TEMPLATE METHOD: embed_documents()
# ============================================================================
# This method is the foundation of document ingestion for RAG systems.
# It takes raw text, chunks it intelligently, generates embeddings,
# and returns a structured collection ready for vector storage.
# 
# Template structure:
#   - Input: documents (raw text), chunking parameters
#   - Processing: chunk preparation, embedding generation
#   - Output: structured dicts with text, embeddings, metadata
# 
# Reusability: Copy this method into your own projects with only:
#   - Embedding provider config (OpenRouter, Cohere, etc.)
#   - Document source adaptation (files, URLs, databases)
#   - Metadata schema customization
# ============================================================================

def embed_documents(
    documents: List[str],
    chunk_size: int = 512,
    chunk_overlap: int = 50,
    provider: str = "openrouter",
    openrouter_key: str | None = None,
) -> List[Dict]:
    """Core template method: Chunk documents and generate embeddings.
    
    This is the production-ready ingestion pattern used across RAG systems.
    Learners can extract this method and adapt it for their own document sources.
    
    Args:
        documents: List of raw text documents
        chunk_size: Target characters per chunk (for context preservation)
        chunk_overlap: Overlap between chunks (prevents breaking key concepts)
        provider: "openrouter", "cohere", or "tfidf"
        openrouter_key: OpenRouter API key (or from env OPENROUTER_API_KEY)
    
    Returns:
        List of dicts: {
            'chunk_id': str (unique ID),
            'text': str (chunk content),
            'embedding': np.ndarray (embedding vector),
            'metadata': dict (source, doc_idx, chunk_idx),
            'char_count': int (chunk length)
        }
    
    Example:
        >>> docs = ["Document 1 text...", "Document 2 text..."]
        >>> chunks = embed_documents(docs, chunk_size=512)
        >>> query_chunks = embed_documents(["How to scale?"], chunk_size=512)
        >>> similarities = batch_similarity(query_chunks[0]['embedding'], 
        ...                                  np.array([c['embedding'] for c in chunks]))
    """
    
    # Step 1: Chunk documents intelligently (preserve context boundaries)
    chunked_data = []
    for doc_idx, doc in enumerate(documents):
        chunks = _smart_chunk(doc, chunk_size, chunk_overlap)
        for chunk_idx, chunk_text in enumerate(chunks):
            chunked_data.append({
                'doc_idx': doc_idx,
                'chunk_idx': chunk_idx,
                'text': chunk_text,
                'char_count': len(chunk_text),
            })
    
    print(f"✓ Chunked {len(documents)} docs → {len(chunked_data)} chunks")
    
    # Step 2: Initialize embedding engine with chosen provider
    engine = EmbeddingEngine(
        method=provider,
        openrouter_key=openrouter_key or os.getenv("OPENROUTER_API_KEY")
    )
    print(f"✓ Using embedding provider: {engine.method}")
    
    # Step 3: Generate embeddings for all chunks
    chunk_texts = [c['text'] for c in chunked_data]
    embeddings = engine.embed_documents(chunk_texts)
    print(f"✓ Generated {len(embeddings)} embeddings (dims: {embeddings.shape[1]})")
    
    # Step 4: Combine chunks with embeddings and metadata
    result = []
    for i, (chunk_info, embedding) in enumerate(zip(chunked_data, embeddings)):
        result.append({
            'chunk_id': f"chunk_{chunk_info['doc_idx']}_{chunk_info['chunk_idx']}",
            'text': chunk_info['text'],
            'embedding': embedding,
            'metadata': {
                'doc_idx': chunk_info['doc_idx'],
                'chunk_idx': chunk_info['chunk_idx'],
                'char_count': chunk_info['char_count'],
                'provider': provider,
            },
            'char_count': chunk_info['char_count'],
        })
    
    return result


# ============================================================================
# HELPER: Smart chunking strategy
# ============================================================================

def _smart_chunk(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """Intelligently split text into overlapping chunks.
    
    Strategy:
    - Split by sentences first (preserve logical boundaries)
    - Group sentences until chunk_size is reached
    - Add overlap to maintain context across chunks
    """
    sentences = text.split('. ')
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        sent_length = len(sentence) + 2  # +2 for '. '
        
        if current_length + sent_length > chunk_size and current_chunk:
            # Finalize chunk and save
            chunk_text = '. '.join(current_chunk) + '.'
            chunks.append(chunk_text)
            
            # Start overlap: keep last ~overlap chars of current chunk
            overlap_text = chunk_text[-overlap:] if len(chunk_text) > overlap else chunk_text
            current_chunk = [overlap_text]
            current_length = len(overlap_text)
        
        current_chunk.append(sentence)
        current_length += sent_length
    
    # Add final chunk
    if current_chunk:
        chunks.append('. '.join(current_chunk) + '.')
    
    return [c for c in chunks if len(c.strip()) > 10]  # Filter tiny chunks


# ============================================================================
# DEMONSTRATION FUNCTIONS
# ============================================================================

def demo_core_method():
    """Demonstrate the core embed_documents() template method."""
    print("\n" + "=" * 70)
    print("DEMO 1: Core Method - embed_documents()")
    print("=" * 70)
    
    sample_docs = [
        "Our company was founded in 2010 with a mission to democratize AI. We started with 5 employees and have grown to 500+ globally. We maintain offices in San Francisco, London, and Singapore.",
        "Remote work is encouraged at our company. Employees receive $500/month home office stipend, flexible hours, and work from anywhere policy. We value work-life balance and continuous learning.",
        "Our flagship product, AI Studio, helps teams build and deploy AI applications without coding. It has served 10,000+ companies worldwide and processes over 1 billion requests monthly.",
    ]
    
    # Use the core template method
    embedded_chunks = embed_documents(
        sample_docs,
        chunk_size=256,
        chunk_overlap=30,
        provider="openrouter",
    )
    
    print(f"\n✓ Embedded chunks statistics:")
    print(f"  Total chunks: {len(embedded_chunks)}")
    print(f"  Avg chunk size: {np.mean([c['char_count'] for c in embedded_chunks]):.0f} chars")
    print(f"  Embedding dimensions: {embedded_chunks[0]['embedding'].shape[0]}")
    
    # Show sample output
    print(f"\n✓ Sample chunk (first 100 chars of text):")
    sample = embedded_chunks[0]
    print(f"  ID: {sample['chunk_id']}")
    print(f"  Text: {sample['text'][:100]}...")
    print(f"  Embedding (first 5 dims): {sample['embedding'][:5]}")
    
    return embedded_chunks


def demo_semantic_search(embedded_chunks: List[Dict]):
    """Demonstrate searching with embedded queries."""
    print("\n" + "=" * 70)
    print("DEMO 2: Semantic Search")
    print("=" * 70)
    
    # Embed a query using the same method
    query = "What is the company's remote work policy?"
    query_result = embed_documents(
        [query],
        chunk_size=256,
        provider="openrouter",
    )
    
    query_embedding = query_result[0]['embedding']
    doc_embeddings = np.array([c['embedding'] for c in embedded_chunks])
    
    # Find most similar chunks
    similarities = batch_similarity(query_embedding, doc_embeddings)
    top_indices = np.argsort(similarities)[::-1][:3]
    
    print(f"\nQuery: '{query}'")
    print(f"Top 3 relevant chunks:\n")
    
    for rank, idx in enumerate(top_indices, 1):
        chunk = embedded_chunks[idx]
        sim_score = similarities[idx]
        print(f"  [{rank}] Similarity: {sim_score:.3f}")
        print(f"      {chunk['text'][:90]}...")
        print()


def demo_chunking_strategies():
    """Show different chunking approaches."""
    print("\n" + "=" * 70)
    print("DEMO 3: Chunking Strategies")
    print("=" * 70)
    
    sample_text = (
        "The RAG architecture consists of three stages: retrieval, augmentation, and generation. "
        "First, user queries are converted to embeddings. "
        "Then, similar chunks are retrieved from the vector store. "
        "Finally, retrieved chunks augment the prompt before LLM generation."
    )
    
    print(f"\nOriginal text ({len(sample_text)} chars):")
    print(f"  {sample_text}\n")
    
    for chunk_size in [100, 150, 300]:
        chunks = _smart_chunk(sample_text, chunk_size=chunk_size, overlap=20)
        print(f"Chunk size={chunk_size}: {len(chunks)} chunks")
        for i, c in enumerate(chunks):
            print(f"  [{i+1}] ({len(c)} chars) {c[:60]}...")


def demo_provider_fallback():
    """Show automatic fallback between providers."""
    print("\n" + "=" * 70)
    print("DEMO 4: Provider Fallback Chain")
    print("=" * 70)
    
    print("\nEmbedding provider priority:")
    print("  1. OpenRouter (primary) - via Jina Embeddings v3")
    print("  2. Cohere (fallback) - if OpenRouter unavailable")
    print("  3. TF-IDF (fallback) - keyword-based, always available\n")
    
    # Test with minimal docs
    test_docs = ["embedding test one", "embedding test two"]
    
    result = embed_documents(
        test_docs,
        chunk_size=100,
        provider="openrouter",
    )
    
    print(f"✓ Successfully embedded {len(result)} chunks")
    print(f"✓ Provider used: {result[0]['metadata']['provider']}")


if __name__ == "__main__":
    # Run all demonstrations
    embedded_chunks = demo_core_method()
    demo_semantic_search(embedded_chunks)
    demo_chunking_strategies()
    demo_provider_fallback()
    
    print("\n" + "=" * 70)
    print("✓ Lesson 4.2 Complete: You've learned document embedding ingestion!")
    print("=" * 70)


def main():
    """Run all demonstrations."""
    print("\n" + "🚀 LESSON 4.2: EMBEDDING YOUR DATA".center(60, "="))

    try:
        demo_document_preparation()
        demo_embedding_generation()
        demo_vector_store_creation()
        demo_data_sources()

        print("\n" + "=" * 60)
        print("✅ Document ingestion complete!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
