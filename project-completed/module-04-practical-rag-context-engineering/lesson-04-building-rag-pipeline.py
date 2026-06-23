"""
Lesson 4.4: Building the Pipeline

Assemble the complete RAG workflow combining retrieval, prompt construction,
context augmentation, and LLM generation into a single end-to-end application.

Run: python lesson-04-building-rag-pipeline.py
"""

import os
import sys
from pathlib import Path

# Add shared modules to path
sys.path.insert(0, str(Path(__file__).parent))

from shared.embeddings import EmbeddingEngine
from shared.vector_store import VectorStore
from shared.retriever import Retriever
from shared.rag_pipeline import RAGPipeline
from shared.prompts import format_context


def demo_simple_rag():
    """Demonstrate a basic RAG pipeline."""
    print("\n" + "=" * 60)
    print("SIMPLE RAG PIPELINE")
    print("=" * 60)

    # Company knowledge base
    documents = [
        "Our company was founded in 2010 with a mission to democratize AI.",
        "We have over 500 employees across 15 countries.",
        "Remote work is fully supported with $500/month home office stipend.",
        "Our benefits include comprehensive health insurance and unlimited PTO.",
        "We use Python, Go, and TypeScript as our primary languages.",
    ]

    # Setup components
    cohere_key = os.getenv("COHERE_API_KEY")
    embedding_engine = EmbeddingEngine(
        method="cohere" if cohere_key else "tfidf",
        cohere_api_key=cohere_key
    )
    vector_store = VectorStore(embedding_dim=300)
    retriever = Retriever(vector_store, embedding_engine, top_k=3)

    # Initialize pipeline (without LLM for this demo)
    rag_pipeline = RAGPipeline(
        embedding_engine=embedding_engine,
        vector_store=vector_store,
        retriever=retriever,
        llm_client=None,
    )

    # Ingest documents
    print("Ingesting documents...")
    rag_pipeline.ingest_documents(documents)

    # Query
    query = "What is the work environment like?"
    print(f"\nQuery: {query}")

    result = rag_pipeline.query(query, top_k=3)

    print("\nRetrieved documents:")
    for i, doc_result in enumerate(result["retrieved_documents"], 1):
        print(f"\n{i}. (Similarity: {doc_result['similarity']:.3f})")
        print(f"   {doc_result['document'][:70]}...")

    print("\nContext passed to LLM:")
    print(result["context_used"][:300] + "...")


def demo_with_llm():
    """RAG pipeline with LLM generation."""
    print("\n" + "=" * 60)
    print("RAG WITH LLM GENERATION")
    print("=" * 60)

    # Try to import and setup LLM client
    try:
        from shared.llm_client import LLMClient  # Assuming Module 3 shared modules available
    except ImportError:
        print("Note: LLMClient not available. Would need OpenRouter API key setup.")
        print("In production, this step generates grounded answers using retrieved context.")
        return

    # Sample knowledge base
    documents = [
        "Python is known for its readable syntax and rapid development.",
        "Go excels at concurrent programming and systems development.",
        "TypeScript adds type safety to JavaScript for large projects.",
    ]

    # Setup
    cohere_key = os.getenv("COHERE_API_KEY")
    embedding_engine = EmbeddingEngine(
        method="cohere" if cohere_key else "tfidf",
        cohere_api_key=cohere_key
    )
    vector_store = VectorStore(embedding_dim=300)
    retriever = Retriever(vector_store, embedding_engine, top_k=2)

    # With LLM (if available)
    try:
        llm_client = LLMClient(model="gpt-3.5-turbo")
    except:
        llm_client = None

    rag_pipeline = RAGPipeline(
        embedding_engine=embedding_engine,
        vector_store=vector_store,
        retriever=retriever,
        llm_client=llm_client,
    )

    # Ingest
    rag_pipeline.ingest_documents(documents)

    # Query
    query = "Which language should I use for a web backend?"
    print(f"Query: {query}\n")

    result = rag_pipeline.query(query)

    print("Retrieved:")
    for doc in result["retrieved_documents"]:
        print(f"  • {doc['document'][:50]}... (sim: {doc['similarity']:.2f})")

    if result["answer"]:
        print(f"\nGenerated Answer:\n{result['answer']}")
    else:
        print("\nNo LLM client configured—would generate grounded answer here")


def demo_pipeline_components():
    """Show individual pipeline components."""
    print("\n" + "=" * 60)
    print("PIPELINE COMPONENTS")
    print("=" * 60)

    print("""
RAG Pipeline Stages:

1. INGESTION
   • Load documents
   • Chunk if needed
   • Generate embeddings
   → Output: Embedded documents in vector store

2. RETRIEVAL
   • Embed user query
   • Search vector store
   • Rank by similarity
   → Output: Top-K relevant documents

3. AUGMENTATION
   • Format retrieved docs as context
   • Construct prompt with query + context
   • Add system instructions
   → Output: LLM-ready prompt

4. GENERATION
   • Send augmented prompt to LLM
   • Stream or collect response
   • Extract structured output
   → Output: Grounded answer with sources

5. EVALUATION (Optional)
   • Check retrieval quality
   • Verify answer groundedness
   • Log metrics for monitoring
   → Output: Quality signals
    """)


def demo_rag_patterns():
    """Show different RAG patterns."""
    print("\n" + "=" * 60)
    print("RAG PATTERNS & VARIATIONS")
    print("=" * 60)

    print("""
Pattern 1: Standard RAG
Documents → Embeddings → Search → Retrieve → Augment → Generate

Pattern 2: Hybrid RAG
(Semantic Search + Keyword Search) → Rerank → Retrieve → Augment → Generate

Pattern 3: Iterative RAG
Query → Retrieve → Answer → Check Groundedness → Refine Query → Retrieve Again

Pattern 4: Multi-Index RAG
(Fast Index + Slow Index) → Retrieve → Rerank → Augment → Generate

Pattern 5: Self-Correcting RAG
Query → Retrieve → Generate → Check → Correct if needed → Regenerate
    """)


def main():
    """Run all demonstrations."""
    print("\n" + "🚀 LESSON 4.4: BUILDING THE PIPELINE".center(60, "="))

    try:
        demo_simple_rag()
        demo_with_llm()
        demo_pipeline_components()
        demo_rag_patterns()

        print("\n" + "=" * 60)
        print("✅ RAG pipeline demonstrations complete!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
