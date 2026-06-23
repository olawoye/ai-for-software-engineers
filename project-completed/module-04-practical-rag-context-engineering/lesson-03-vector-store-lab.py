"""
Lesson 4.3: The Vector Store Lab

Learn to store embeddings, build indexes, execute similarity searches,
and compare retrieval results using different vector store implementations.

Run: python lesson-03-vector-store-lab.py
"""

import numpy as np
import os
from shared.embeddings import EmbeddingEngine
from shared.vector_store import VectorStore


def demo_vector_storage():
    """Demonstrate basic vector storage."""
    print("\n" + "=" * 60)
    print("VECTOR STORAGE BASICS")
    print("=" * 60)

    documents = [
        "Python is a popular programming language.",
        "JavaScript runs in web browsers.",
        "Go is known for concurrent programming.",
    ]

    # Initialize components
    cohere_key = os.getenv("COHERE_API_KEY")
    embedding_engine = EmbeddingEngine(method="cohere" if cohere_key else "tfidf", cohere_api_key=cohere_key)
    vector_store = VectorStore(embedding_dim=300)

    # Generate and store embeddings
    embeddings = embedding_engine.embed_documents(documents)
    vector_store.add(documents, embeddings)

    print(f"Stored {vector_store.get_stats()['total_documents']} documents")
    print(f"Embedding dimension: {vector_store.get_stats()['embedding_dim']}")


def demo_similarity_search():
    """Perform similarity searches."""
    print("\n" + "=" * 60)
    print("SIMILARITY SEARCH")
    print("=" * 60)

    documents = [
        "Machine learning enables computers to learn from data.",
        "Deep learning uses neural networks with many layers.",
        "Natural language processing analyzes human language.",
        "Computer vision processes and understands images.",
        "Reinforcement learning trains agents through rewards.",
    ]

    # Setup
    cohere_key = os.getenv("COHERE_API_KEY")
    embedding_engine = EmbeddingEngine(method="cohere" if cohere_key else "tfidf", cohere_api_key=cohere_key)
    vector_store = VectorStore(embedding_dim=300)

    embeddings = embedding_engine.embed_documents(documents)
    vector_store.add(documents, embeddings)

    # Search
    query = "What is neural network training?"
    query_embedding = embedding_engine.embed_query(query)

    results = vector_store.search(query_embedding, top_k=3)

    print(f"\nQuery: {query}")
    print(f"\nTop 3 Results:")
    for i, (doc, similarity, metadata) in enumerate(results, 1):
        print(f"\n{i}. Similarity: {similarity:.3f}")
        print(f"   Doc: {doc[:60]}...")


def demo_metadata_filtering():
    """Demonstrate metadata filtering."""
    print("\n" + "=" * 60)
    print("METADATA FILTERING")
    print("=" * 60)

    documents = [
        "Company founded in 2010",
        "We have 500+ employees",
        "Remote work policy: flexible hours",
        "Salary competitive with market",
        "Health insurance provided",
    ]

    metadata = [
        {"category": "company_info", "year": 2010},
        {"category": "company_info", "metric": "employees"},
        {"category": "benefits", "type": "work_arrangements"},
        {"category": "benefits", "type": "compensation"},
        {"category": "benefits", "type": "health"},
    ]

    # Setup
    cohere_key = os.getenv("COHERE_API_KEY")
    embedding_engine = EmbeddingEngine(method="cohere" if cohere_key else "tfidf", cohere_api_key=cohere_key)
    vector_store = VectorStore(embedding_dim=300)

    embeddings = embedding_engine.embed_documents(documents)
    vector_store.add(documents, embeddings, metadata)

    print(f"\nStored {len(documents)} documents with metadata")
    print(f"Categories: company_info, benefits")

    # Show metadata usage
    print("\nMetadata in stored documents:")
    for doc, meta in zip(documents[:3], metadata[:3]):
        print(f"  {doc[:40]}... → {meta}")


def demo_vector_store_persistence():
    """Save and load vector stores."""
    print("\n" + "=" * 60)
    print("VECTOR STORE PERSISTENCE")
    print("=" * 60)

    documents = ["Sample document 1", "Sample document 2"]

    # Create and save
    cohere_key = os.getenv("COHERE_API_KEY")
    embedding_engine = EmbeddingEngine(method="cohere" if cohere_key else "tfidf", cohere_api_key=cohere_key)
    vector_store = VectorStore(embedding_dim=300)

    embeddings = embedding_engine.embed_documents(documents)
    vector_store.add(documents, embeddings)

    # Save to disk
    save_path = "/tmp/vector_store.json"
    vector_store.save(save_path)
    print(f"Saved vector store to {save_path}")

    # Load from disk
    new_store = VectorStore(embedding_dim=300)
    new_store.load(save_path)
    print(f"Loaded vector store with {new_store.get_stats()['total_documents']} documents")


def demo_vector_store_comparison():
    """Compare vector store implementations."""
    print("\n" + "=" * 60)
    print("VECTOR STORE COMPARISON")
    print("=" * 60)

    print("""
Vector Store Options:

1. In-Memory (NumPy)
   ✅ Fast for small datasets (<1M docs)
   ✅ Easy to implement
   ❌ Not scalable
   ❌ Limited query options

2. FAISS (Facebook AI Similarity Search)
   ✅ Optimized for large-scale search
   ✅ GPU acceleration available
   ✅ Multiple indexing strategies
   ❌ Requires compilation
   ❌ Higher memory overhead

3. Pinecone (Cloud)
   ✅ Fully managed
   ✅ Serverless scaling
   ✅ Built-in metadata filtering
   ❌ Cost for large scale
   ❌ External dependency

4. Chroma (Lightweight)
   ✅ Persistent local storage
   ✅ Simple API
   ✅ Good for demos
   ❌ Limited scale
   ❌ Single machine

5. Milvus (Open Source)
   ✅ Scalable
   ✅ Multiple backends
   ✅ Self-hosted
   ❌ Complex setup
   ❌ Operational overhead
    """)


def main():
    """Run all demonstrations."""
    print("\n" + "🚀 LESSON 4.3: THE VECTOR STORE LAB".center(60, "="))

    try:
        demo_vector_storage()
        demo_similarity_search()
        demo_metadata_filtering()
        demo_vector_store_persistence()
        demo_vector_store_comparison()

        print("\n" + "=" * 60)
        print("✅ Vector store demonstrations complete!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
