"""
Lesson 4.3: The Vector Store Lab

Learn to store embeddings efficiently and execute semantic searches.
This lesson demonstrates the core semantic_search() template method
that consumes output from Lesson 4.2 and enables production-grade retrieval.

Builds on Lesson 4.2 (embed_documents) to create complete search pipelines.

Run: python lesson-03-vector-store-lab.py
     or: streamlit run lesson-03-vector-store-lab.py  (for interactive UI)
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

# Import lesson 4.2 for embedding generation
import importlib.util
spec = importlib.util.spec_from_file_location("lesson02", str(Path(__file__).parent / "lesson-02-embedding-your-data.py"))
lesson02 = importlib.util.module_from_spec(spec)


# ============================================================================
# CORE TEMPLATE METHOD: semantic_search()
# ============================================================================
# This method is the foundation of retrieval systems for RAG.
# It stores embedded chunks and executes efficient similarity searches.
# 
# Template structure:
#   - Input: embedded chunks from Lesson 4.2, query embedding, top_k
#   - Processing: store initialization, similarity computation, ranking
#   - Output: ranked results with similarity scores and metadata
# 
# Reusability: Copy this method into your own projects with:
#   - Vector store backend swap (NumPy → FAISS → Pinecone)
#   - Metadata filtering customization
#   - Query expansion or reranking
# ============================================================================

def semantic_search(
    embedded_chunks: List[Dict],
    query_embedding: np.ndarray,
    top_k: int = 5,
    use_faiss: bool = False,
    metadata_filter: Dict | None = None,
) -> List[Dict]:
    """Core template method: Store embeddings and execute semantic search.
    
    This method is production-ready and reusable for retrieval systems.
    It consumes embedded chunks from Lesson 4.2's embed_documents() method.
    
    Args:
        embedded_chunks: List of dicts from embed_documents() with:
                        {chunk_id, text, embedding, metadata, char_count}
        query_embedding: np.ndarray from embedding the query
        top_k: Number of top results to return
        use_faiss: Use FAISS for large-scale retrieval (requires faiss-cpu)
        metadata_filter: Optional dict to filter results by metadata
                        (e.g., {'provider': 'openrouter'})
    
    Returns:
        List of result dicts: {
            'rank': int (1-indexed),
            'chunk_id': str,
            'text': str,
            'similarity': float (0-1),
            'metadata': dict,
        }
    
    Example:
        >>> from lesson_02 import embed_documents
        >>> docs = ["Company policy...", "Benefits guide..."]
        >>> embedded = embed_documents(docs)
        >>> query_result = embed_documents(["What are benefits?"])
        >>> results = semantic_search(embedded, query_result[0]['embedding'])
        >>> print(f"Found {len(results)} matching policies")
    """
    
    # Step 1: Initialize vector store
    if not embedded_chunks:
        print("⚠️  No embedded chunks provided")
        return []
    
    embedding_dim = embedded_chunks[0]['embedding'].shape[0]
    vector_store = VectorStore(embedding_dim=embedding_dim, use_faiss=use_faiss)
    
    # Step 2: Extract documents, embeddings, and metadata from chunks
    chunk_texts = [c['text'] for c in embedded_chunks]
    chunk_embeddings = np.array([c['embedding'] for c in embedded_chunks])
    chunk_metadata = [c['metadata'] for c in embedded_chunks]
    chunk_ids = [c['chunk_id'] for c in embedded_chunks]
    
    # Add chunk_id to metadata for tracking
    for i, meta in enumerate(chunk_metadata):
        meta['chunk_id'] = chunk_ids[i]
    
    # Step 3: Add all chunks to vector store
    vector_store.add(chunk_texts, chunk_embeddings, chunk_metadata)
    print(f"✓ Indexed {len(embedded_chunks)} chunks")
    
    # Step 4: Execute similarity search
    search_results = vector_store.search(query_embedding, top_k=top_k * 2)
    print(f"✓ Retrieved top-{len(search_results)} candidates")
    
    # Step 5: Apply metadata filtering if provided
    filtered_results = search_results
    if metadata_filter:
        filtered_results = [
            (text, sim, meta) for text, sim, meta in search_results
            if all(meta.get(k) == v for k, v in metadata_filter.items())
        ]
        print(f"✓ Filtered to {len(filtered_results)} results")
    
    # Step 6: Format and rank results
    final_results = []
    for rank, (text, similarity, metadata) in enumerate(filtered_results[:top_k], 1):
        final_results.append({
            'rank': rank,
            'chunk_id': metadata.get('chunk_id', 'unknown'),
            'text': text,
            'similarity': float(similarity),
            'metadata': metadata,
        })
    
    return final_results


# ============================================================================
# HELPER: Performance Comparison Utility
# ============================================================================

def compare_search_backends(
    embedded_chunks: List[Dict],
    query_embedding: np.ndarray,
    top_k: int = 5,
) -> Dict:
    """Compare NumPy vs FAISS search performance.
    
    Returns timing and result count for both backends.
    """
    results = {}
    
    # NumPy search
    start = time.time()
    numpy_results = semantic_search(
        embedded_chunks,
        query_embedding,
        top_k=top_k,
        use_faiss=False,
    )
    numpy_time = time.time() - start
    results['numpy'] = {'time': numpy_time, 'results': len(numpy_results)}
    
    # FAISS search (if available)
    try:
        start = time.time()
        faiss_results = semantic_search(
            embedded_chunks,
            query_embedding,
            top_k=top_k,
            use_faiss=True,
        )
        faiss_time = time.time() - start
        results['faiss'] = {'time': faiss_time, 'results': len(faiss_results)}
        results['speedup'] = numpy_time / faiss_time if faiss_time > 0 else 1.0
    except Exception as e:
        print(f"FAISS comparison skipped: {e}")
    
    return results


# ============================================================================
# DEMONSTRATION FUNCTIONS
# ============================================================================

def demo_core_method():
    """Demonstrate the semantic_search() template method."""
    print("\n" + "=" * 70)
    print("DEMO 1: Core Method - semantic_search()")
    print("=" * 70)
    
    # Generate sample embedded chunks (from Lesson 4.2 pattern)
    sample_docs = [
        "Our company was founded in 2010. We serve 10,000+ customers worldwide.",
        "We offer competitive salaries and comprehensive benefits packages.",
        "Remote work is encouraged. Employees get $500/month home office stipend.",
        "We maintain offices in San Francisco, London, and Singapore.",
        "Our flagship product, AI Studio, helps teams build AI applications.",
    ]
    
    # For demo, use TF-IDF embeddings (always available)
    engine = EmbeddingEngine(method="tfidf")
    embeddings = engine.embed_documents(sample_docs)
    
    # Create embedded chunks structure (matching Lesson 4.2 output)
    embedded_chunks = [
        {
            'chunk_id': f"chunk_0_{i}",
            'text': doc,
            'embedding': emb,
            'metadata': {'doc_idx': 0, 'chunk_idx': i, 'provider': 'tfidf'},
            'char_count': len(doc),
        }
        for i, (doc, emb) in enumerate(zip(sample_docs, embeddings))
    ]
    
    print(f"✓ Generated {len(embedded_chunks)} embedded chunks")
    
    # Search for relevant documents
    query = "What is the company's remote work policy?"
    query_embedding = engine.embed_query(query)
    
    print(f"\nQuery: '{query}'")
    print(f"Query embedding dims: {query_embedding.shape[0]}\n")
    
    # Execute semantic search
    results = semantic_search(embedded_chunks, query_embedding, top_k=3)
    
    # Display results
    print("✓ Top 3 Results:")
    for result in results:
        print(f"\n  [{result['rank']}] Similarity: {result['similarity']:.3f}")
        print(f"      {result['text'][:80]}...")
        print(f"      Chunk ID: {result['chunk_id']}")
    
    return embedded_chunks, results


def demo_vector_store_backends():
    """Compare in-memory vs FAISS backends."""
    print("\n" + "=" * 70)
    print("DEMO 2: Vector Store Backends Comparison")
    print("=" * 70)
    
    # Create larger document set
    sample_docs = [
        "Python is a popular programming language for data science.",
        "JavaScript enables interactive web applications.",
        "Rust provides memory safety without garbage collection.",
        "Go excels at concurrent and distributed systems.",
        "Java powers enterprise backend applications.",
        "C++ offers high performance for systems programming.",
        "TypeScript adds static typing to JavaScript.",
        "Swift is Apple's modern programming language.",
    ]
    
    engine = EmbeddingEngine(method="tfidf")
    embeddings = engine.embed_documents(sample_docs)
    
    embedded_chunks = [
        {
            'chunk_id': f"chunk_{i}",
            'text': doc,
            'embedding': emb,
            'metadata': {'index': i, 'type': 'language_info'},
            'char_count': len(doc),
        }
        for i, (doc, emb) in enumerate(zip(sample_docs, embeddings))
    ]
    
    query_embedding = engine.embed_query("What languages are good for systems programming?")
    
    print(f"\nDataset: {len(embedded_chunks)} documents")
    print(f"Embedding dimensions: {embedded_chunks[0]['embedding'].shape[0]}\n")
    
    # Compare backends
    perf = compare_search_backends(embedded_chunks, query_embedding, top_k=3)
    
    print("Performance Comparison:")
    print(f"  NumPy search: {perf['numpy']['time']*1000:.2f}ms ({perf['numpy']['results']} results)")
    if 'faiss' in perf:
        print(f"  FAISS search: {perf['faiss']['time']*1000:.2f}ms ({perf['faiss']['results']} results)")
        print(f"  Speedup: {perf.get('speedup', 1.0):.1f}x")


def demo_metadata_filtering():
    """Demonstrate filtering results by metadata."""
    print("\n" + "=" * 70)
    print("DEMO 3: Metadata Filtering")
    print("=" * 70)
    
    # Documents with rich metadata
    sample_docs = [
        "Our health insurance covers medical, dental, and vision.",
        "We offer unlimited PTO for all full-time employees.",
        "Annual salary ranges from $100k to $200k based on experience.",
        "We provide $5000 annual professional development budget.",
        "401(k) matching program: 4% employer contribution.",
        "Stock options available for senior positions.",
    ]
    
    engine = EmbeddingEngine(method="tfidf")
    embeddings = engine.embed_documents(sample_docs)
    
    # Embed with rich metadata
    embedded_chunks = [
        {
            'chunk_id': f"chunk_{i}",
            'text': doc,
            'embedding': emb,
            'metadata': {
                'category': 'health' if i < 2 else 'time_off' if i == 2 else 'compensation',
                'doc_idx': 0,
                'chunk_idx': i,
            },
            'char_count': len(doc),
        }
        for i, (doc, emb) in enumerate(zip(sample_docs, embeddings))
    ]
    
    # Search with metadata filter
    query = "What benefits are available?"
    query_embedding = engine.embed_query(query)
    
    print(f"Query: '{query}'\n")
    
    # Search all results
    all_results = semantic_search(embedded_chunks, query_embedding, top_k=6)
    print(f"All results: {len(all_results)} documents\n")
    
    # Search filtered by compensation category
    compensation_filter = {'category': 'compensation'}
    filtered_results = semantic_search(
        embedded_chunks,
        query_embedding,
        top_k=6,
        metadata_filter=compensation_filter,
    )
    print(f"Filtered results (compensation only): {len(filtered_results)} documents")
    for result in filtered_results[:2]:
        print(f"  • {result['text'][:60]}... (sim: {result['similarity']:.3f})")


def demo_vector_store_options():
    """Overview of vector store options for production."""
    print("\n" + "=" * 70)
    print("DEMO 4: Vector Store Options for Production")
    print("=" * 70)
    
    print("""
Vector Store Implementations:

1. **In-Memory (NumPy)**
   ✓ No setup required
   ✓ Good for <10k documents
   ✓ Fast for prototypes
   ✗ All data in RAM
   ✗ Single machine only
   Use: Demos, testing, small datasets

2. **FAISS (Facebook AI Similarity Search)**
   ✓ Millions of documents
   ✓ GPU acceleration available
   ✓ Multiple index types
   ✗ Requires compilation
   ✗ Complex to manage at scale
   Use: High-performance search, research

3. **ChromaDB**
   ✓ Persistent local storage
   ✓ Simple Python API
   ✓ Good for production prototypes
   ✗ Limited scale
   ✗ Single machine
   Use: Small/medium production systems

4. **Pinecone (Cloud)**
   ✓ Fully managed
   ✓ Serverless scaling
   ✓ Built-in metadata filtering
   ✗ Requires API key
   ✗ Cost scales with usage
   Use: Enterprise applications, auto-scaling

5. **Weaviate (Self-Hosted)**
   ✓ Flexible deployment
   ✓ GraphQL API
   ✓ Multi-tenancy support
   ✗ Operational overhead
   ✗ Complex configuration
   Use: Large-scale self-hosted systems

6. **Qdrant**
   ✓ High performance
   ✓ Payload storage
   ✓ Good balance
   ✗ Newer ecosystem
   ✗ Smaller community
   Use: Modern vector search applications

**For this lesson:** We demonstrate NumPy (always available) with FAISS as an optional optimization.
""")


if __name__ == "__main__":
    # Run all demonstrations
    embedded_chunks, results = demo_core_method()
    demo_vector_store_backends()
    demo_metadata_filtering()
    demo_vector_store_options()
    
    print("\n" + "=" * 70)
    print("✓ Lesson 4.3 Complete: Vector store indexing and semantic search!")
    print("=" * 70)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
