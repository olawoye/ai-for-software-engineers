"""
Lesson 4.2: Embedding Your Data

Learn how to prepare raw documents, chunk content appropriately,
generate embeddings, and create a retrieval-ready knowledge base.

Run: python lesson-02-embedding-your-data.py
"""

import os
from pathlib import Path
from shared.embeddings import EmbeddingEngine
from shared.vector_store import VectorStore


def demo_document_preparation():
    """Demonstrate document loading and chunking."""
    print("\n" + "=" * 60)
    print("DOCUMENT PREPARATION")
    print("=" * 60)

    # Sample documents (in production, would load from files)
    documents = [
        "Our company was founded in 2010 with a mission to democratize AI. We started with 5 employees and have grown to 500+ globally.",
        "Our flagship product, AI Studio, helps teams build and deploy AI applications without coding. It has served 10,000+ companies worldwide.",
        "Remote work is encouraged at our company. Employees receive $500/month home office stipend and flexible hours.",
        "We maintain a competitive benefits package including health insurance, 401k matching, and unlimited PTO for salaried employees.",
    ]

    print(f"\nLoaded {len(documents)} sample documents")

    # Simple chunking strategy
    def chunk_documents(docs, max_chunk_size=200):
        """Simple chunking by character limit."""
        chunks = []
        for doc in docs:
            words = doc.split()
            current_chunk = []

            for word in words:
                current_chunk.append(word)
                chunk_text = " ".join(current_chunk)
                if len(chunk_text) > max_chunk_size:
                    if len(current_chunk) > 1:
                        current_chunk.pop()
                        chunks.append(" ".join(current_chunk))
                        current_chunk = [word]
                    else:
                        chunks.append(chunk_text)
                        current_chunk = []

            if current_chunk:
                chunks.append(" ".join(current_chunk))

        return chunks

    chunks = chunk_documents(documents)
    print(f"After chunking: {len(chunks)} chunks")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\n  Chunk {i+1}: {chunk[:60]}...")


def demo_embedding_generation():
    """Generate embeddings from documents."""
    print("\n" + "=" * 60)
    print("EMBEDDING GENERATION")
    print("=" * 60)

    documents = [
        "Machine learning is a subset of artificial intelligence.",
        "Deep learning uses neural networks with multiple layers.",
        "Natural language processing helps computers understand text.",
    ]

    # Initialize embedding engine
    cohere_key = os.getenv("COHERE_API_KEY")
    embedding_engine = EmbeddingEngine(method="cohere" if cohere_key else "tfidf", cohere_api_key=cohere_key)

    print(f"\nEmbedding method: {embedding_engine.method}")
    print(f"Generating embeddings for {len(documents)} documents...")

    embeddings = embedding_engine.embed_documents(documents)
    print(f"Embedding shape: {embeddings.shape}")
    print(f"Embedding dimensions: {embeddings.shape[1]}")


def demo_vector_store_creation():
    """Create and populate vector store."""
    print("\n" + "=" * 60)
    print("VECTOR STORE CREATION")
    print("=" * 60)

    documents = [
        "Our company values innovation and creativity.",
        "We promote continuous learning and development.",
        "Work-life balance is important to us.",
    ]

    # Create vector store
    vector_store = VectorStore(embedding_dim=300)

    # Create embeddings
    cohere_key = os.getenv("COHERE_API_KEY")
    embedding_engine = EmbeddingEngine(method="cohere" if cohere_key else "tfidf", cohere_api_key=cohere_key)

    embeddings = embedding_engine.embed_documents(documents)

    # Add to store
    metadata = [
        {"source": "company_values", "doc_id": i}
        for i in range(len(documents))
    ]

    vector_store.add(documents, embeddings, metadata)

    # Print stats
    stats = vector_store.get_stats()
    print(f"\nVector Store Stats:")
    print(f"  Total documents: {stats['total_documents']}")
    print(f"  Embedding dimensions: {stats['embedding_dim']}")
    print(f"  Using FAISS: {stats['using_faiss']}")


def demo_data_sources():
    """Show different data source patterns."""
    print("\n" + "=" * 60)
    print("DATA SOURCE PATTERNS")
    print("=" * 60)

    print("""
Lesson 4.2 teaches ingestion from multiple sources:

1. Text Files (.txt)
   - Load directly
   - Split by paragraphs or sections

2. PDF Documents (.pdf)
   - Use PyPDF2 or pdfplumber
   - Extract text and structure

3. CSV/Spreadsheets
   - Combine rows into documents
   - Use column structure as metadata

4. Structured Data (JSON, Markdown)
   - Parse hierarchical structure
   - Create documents from sections

5. Web Pages
   - Scrape or API-fetch content
   - Preserve structure and links
    """)


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
