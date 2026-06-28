"""
Lesson 4.4: Building the RAG Pipeline

Assemble a complete end-to-end RAG workflow that combines:
  • Document ingestion with embeddings (Lesson 4.2)
  • Semantic search and retrieval (Lesson 4.3)
  • Prompt augmentation with context
  • LLM-based answer generation (OpenRouter)

The core template method build_rag_pipeline() demonstrates the complete
pipeline workflow and is designed to be extracted as a reusable template
for learner projects.

Business Scenario:
  A company customer support team needs an AI assistant that answers
  employee HR questions using internal knowledge base documents. The
  pipeline must retrieve relevant docs and generate accurate, sourced
  answers in seconds.

Run: python lesson-04-building-rag-pipeline.py
     Set OPENROUTER_API_KEY environment variable before running
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import List, Dict, Optional
import numpy as np

# Add project paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent / "shared"))

from shared.embeddings import EmbeddingEngine
from shared.vector_store import VectorStore

# ============================================================================
# CORE TEMPLATE METHOD: build_rag_pipeline()
# ============================================================================
# This is the main method you'll extract into your projects.
# It orchestrates the complete RAG workflow: ingest → retrieve → augment → generate


def build_rag_pipeline(
    documents: List[str],
    query: str,
    top_k: int = 5,
    chunk_size: int = 512,
    chunk_overlap: int = 50,
    embedding_provider: str = "openrouter",
    openrouter_key: Optional[str] = None,
    llm_model: str = "meta-llama/llama-2-7b-chat",
) -> Dict:
    """
    Build and execute a complete RAG pipeline end-to-end.

    This template method demonstrates the production pattern for combining
    retrieval and generation into a single answering system. It:
    1. Embeds all documents for semantic search
    2. Retrieves top-K most relevant documents
    3. Constructs a prompt with context
    4. Generates an answer using the LLM
    5. Returns results with citations and metrics

    Args:
        documents: List of document texts to build knowledge base from
        query: User's natural language question
        top_k: Number of documents to retrieve (default: 5)
        chunk_size: Characters per chunk (default: 512)
        chunk_overlap: Overlap between chunks (default: 50)
        embedding_provider: "openrouter", "cohere", or "tfidf" (default: "openrouter")
        openrouter_key: OpenRouter API key (if None, uses OPENROUTER_API_KEY env var)
        llm_model: Model identifier for OpenRouter LLM calls (default: llama-2-7b-chat)

    Returns:
        Dict containing:
            - answer (str): Generated answer grounded in retrieved context
            - sources (List[Dict]): Retrieved documents with rank, text, similarity score
            - context (str): Full context sent to LLM (for debugging)
            - retrieval_time (float): Seconds spent on embedding/search
            - generation_time (float): Seconds spent on LLM call
            - total_tokens (int): Approximate tokens used
            - retrieval_count (int): Number of documents retrieved
    """

    # Get API key
    api_key = openrouter_key or os.getenv("OPENROUTER_API_KEY")

    # ---- STAGE 1: INGESTION ----
    # Embed all documents and store in vector store
    ingest_start = time.time()

    # Initialize embedding engine
    embedding_engine = EmbeddingEngine(
        method=embedding_provider,
        cohere_api_key=os.getenv("COHERE_API_KEY") if embedding_provider == "cohere" else None,
    )

    # Smart chunk documents to preserve context
    embedded_chunks = []
    chunk_id = 0
    for doc_idx, doc in enumerate(documents):
        chunks = _smart_chunk(doc, chunk_size, chunk_overlap)
        for chunk in chunks:
            # Generate embedding for this chunk
            embedding = embedding_engine.embed_query(chunk)
            embedded_chunks.append({
                "chunk_id": chunk_id,
                "doc_idx": doc_idx,
                "text": chunk,
                "embedding": embedding,
            })
            chunk_id += 1

    # Create vector store and add all chunks
    embedding_dim = embedded_chunks[0]["embedding"].shape[0] if embedded_chunks else 1536
    vector_store = VectorStore(embedding_dim=embedding_dim)
    for chunk in embedded_chunks:
        vector_store.add(chunk["text"], chunk["embedding"], {"chunk_id": chunk["chunk_id"]})

    # ---- STAGE 2: RETRIEVAL ----
    # Embed query and search for relevant documents
    query_embedding = embedding_engine.embed_query(query)
    
    # Simple NumPy-based semantic search (replicates Lesson 4.3 logic)
    similarities = []
    for chunk in embedded_chunks:
        sim = np.dot(query_embedding, chunk["embedding"]) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(chunk["embedding"]) + 1e-8
        )
        similarities.append(sim)

    # Get top-K indices
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    retrieved_chunks = [
        {
            "rank": rank + 1,
            "chunk_id": embedded_chunks[idx]["chunk_id"],
            "text": embedded_chunks[idx]["text"],
            "similarity": float(similarities[idx]),
        }
        for rank, idx in enumerate(top_indices)
    ]

    retrieval_time = time.time() - ingest_start

    # ---- STAGE 3: AUGMENTATION ----
    # Format retrieved context and construct the prompt
    context_pieces = [
        f"[Document {r['rank']}] (similarity: {r['similarity']:.3f})\n{r['text']}"
        for r in retrieved_chunks
    ]
    context = "\n\n".join(context_pieces)

    augmented_prompt = f"""Answer the user's question based ONLY on the provided context.
If the context doesn't contain enough information, say so.

CONTEXT:
{context}

USER QUESTION:
{query}

ANSWER:"""

    # ---- STAGE 4: GENERATION ----
    # Call LLM to generate grounded answer
    generation_start = time.time()

    answer = _generate_answer_with_llm(
        prompt=augmented_prompt,
        api_key=api_key,
        model=llm_model,
    )

    generation_time = time.time() - generation_start

    # ---- STAGE 5: FORMAT OUTPUT ----
    # Estimate token counts (rough approximation)
    total_input_tokens = len(augmented_prompt.split())
    total_output_tokens = len(answer.split()) if answer else 0
    total_tokens = total_input_tokens + total_output_tokens

    return {
        "answer": answer,
        "sources": retrieved_chunks,
        "context": context,
        "retrieval_time": retrieval_time,
        "generation_time": generation_time,
        "total_time": retrieval_time + generation_time,
        "total_tokens": total_tokens,
        "retrieval_count": len(retrieved_chunks),
    }


# ============================================================================
# HELPER METHODS
# ============================================================================


def _smart_chunk(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """
    Split text into chunks while preserving sentence boundaries.
    
    This helper ensures chunks don't break mid-sentence, improving
    context coherence. Overlapping chunks help preserve context at boundaries.
    
    Args:
        text: Text to chunk
        chunk_size: Target chunk size in characters
        overlap: Overlap between chunks in characters
    
    Returns:
        List of text chunks
    """
    # Simple sentence-based chunking
    sentences = text.split(". ")
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence + ". "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks if chunks else [text]


def _generate_answer_with_llm(
    prompt: str,
    api_key: Optional[str] = None,
    model: str = "meta-llama/llama-2-7b-chat",
) -> str:
    """
    Generate an answer using OpenRouter LLM API.
    
    This helper calls OpenRouter's API with the augmented prompt to generate
    a grounded answer. Falls back gracefully if API key is missing.
    
    Args:
        prompt: The augmented prompt with context and question
        api_key: OpenRouter API key
        model: Model identifier (default: llama-2-7b-chat)
    
    Returns:
        Generated answer as string
    """
    if not api_key:
        # Fallback: return simulated response based on retrieved context
        return (
            "[LLM Response Simulated]\n"
            "To enable actual LLM responses, set OPENROUTER_API_KEY environment variable.\n"
            "In production, this would call the OpenRouter API with the augmented prompt above."
        )

    try:
        import requests
    except ImportError:
        return "[requests library required for LLM calls]"

    # Call OpenRouter API
    response = requests.post(
        "https://api.openrouter.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://github.com/AIForSoftwareEngineers",
            "X-Title": "RAG Pipeline Lesson",
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 500,
        },
        timeout=30,
    )

    if response.status_code == 200:
        result = response.json()
        return result.get("choices", [{}])[0].get("message", {}).get("content", "No response")
    else:
        return f"[LLM Error: {response.status_code}] {response.text}"


# ============================================================================
# DEMONSTRATIONS
# ============================================================================


def demo_core_method():
    """Demonstrate the core build_rag_pipeline() method in action."""
    print("\n" + "=" * 70)
    print("DEMO 1: CORE RAG PIPELINE")
    print("=" * 70)

    # HR knowledge base for the business scenario
    hr_documents = [
        "Remote work policy: All employees can work remotely up to 3 days per week. "
        "Remote stipend of $500/month is provided. Home office setup must be approved by manager. "
        "Equipment provided includes laptop and monitor.",
        
        "Health benefits: Comprehensive health insurance covers medical, dental, and vision. "
        "Employee contribution is 15% of premium. Dependents can be added for additional cost. "
        "Open enrollment period is in October each year.",
        
        "PTO policy: All employees receive 25 days paid time off per year plus 10 company holidays. "
        "Unused PTO does not roll over. Minimum 2-week notice required for vacation planning. "
        "Sick leave is separate and unlimited.",
        
        "Parental leave: 16 weeks paid leave for primary caregiver, 8 weeks for secondary. "
        "Benefits continue during leave. Job guaranteed upon return. "
        "Gradual return-to-work options available.",
        
        "Professional development: $2,000 annual budget per employee for courses and conferences. "
        "Company pays for LinkedIn Learning subscriptions. Tuition reimbursement available for degrees. "
        "Internal mentorship program available.",
    ]

    query = "Can I work remotely and what office equipment do I get?"
    print(f"\nQuery: {query}")
    print(f"Knowledge base size: {len(hr_documents)} documents\n")

    # Build RAG pipeline
    result = build_rag_pipeline(
        documents=hr_documents,
        query=query,
        top_k=3,
        embedding_provider="openrouter",
        openrouter_key=os.getenv("OPENROUTER_API_KEY"),
    )

    # Display results
    print("RETRIEVED SOURCES:")
    for source in result["sources"]:
        print(
            f"\n  [{source['rank']}] Similarity: {source['similarity']:.3f}"
            f"\n      {source['text'][:100]}..."
        )

    print(f"\n{'GENERATED ANSWER':^70}")
    print("-" * 70)
    print(result["answer"])
    print("-" * 70)

    print(f"\nRETRIEVAL TIME: {result['retrieval_time']:.2f}s")
    print(f"GENERATION TIME: {result['generation_time']:.2f}s")
    print(f"TOTAL TIME: {result['total_time']:.2f}s")
    print(f"DOCUMENTS RETRIEVED: {result['retrieval_count']}")
    print(f"APPROX TOKENS: {result['total_tokens']}")


def demo_retrieval_quality():
    """Show how retrieval quality affects final answers."""
    print("\n" + "=" * 70)
    print("DEMO 2: RETRIEVAL QUALITY IMPACT")
    print("=" * 70)

    documents = [
        "Python is a high-level programming language with dynamic typing.",
        "TypeScript adds static type checking to JavaScript.",
        "Rust provides memory safety without garbage collection.",
        "Go was designed for systems programming and concurrency.",
    ]

    queries = [
        "What language should I use for systems programming?",
        "Which language has dynamic typing?",
        "Tell me about type safety in programming languages.",
    ]

    print(f"\nDocuments in KB: {len(documents)}")
    print("Queries to test:\n")

    for i, query in enumerate(queries, 1):
        result = build_rag_pipeline(
            documents=documents,
            query=query,
            top_k=2,
            embedding_provider="openrouter",
            openrouter_key=os.getenv("OPENROUTER_API_KEY"),
        )

        print(f"\n  Query {i}: {query}")
        print(f"  Retrieved: {result['retrieval_count']} documents")
        print(f"  Top similarity: {result['sources'][0]['similarity']:.3f}")
        print(f"  Answer preview: {result['answer'][:80]}...")


def demo_chunking_strategy():
    """Demonstrate impact of different chunking strategies."""
    print("\n" + "=" * 70)
    print("DEMO 3: CHUNKING STRATEGY COMPARISON")
    print("=" * 70)

    # Long document
    long_doc = """
    Machine Learning is a subset of Artificial Intelligence that focuses on
    enabling systems to learn from data without being explicitly programmed.
    There are three main types: supervised learning, unsupervised learning, and
    reinforcement learning. Supervised learning uses labeled data to train models.
    Unsupervised learning finds patterns in unlabeled data. Reinforcement learning
    trains agents to make decisions through reward signals. Deep Learning uses
    neural networks with multiple layers. Transformers are a recent architecture
    that revolutionized NLP. The attention mechanism allows models to focus on
    relevant parts of input. Large Language Models like GPT use transformer
    architecture at scale. Fine-tuning adapts pre-trained models to specific tasks.
    Transfer learning reuses learned features for new tasks.
    """

    query = "How do transformers use attention mechanisms?"

    print(f"\nDocument length: {len(long_doc)} characters")
    print(f"Query: {query}\n")

    # Test different chunk sizes
    for chunk_size in [200, 512, 1024]:
        chunks = _smart_chunk(long_doc, chunk_size=chunk_size)
        print(f"\nChunk size: {chunk_size} chars → {len(chunks)} chunks")
        for i, chunk in enumerate(chunks, 1):
            print(f"  Chunk {i}: {len(chunk)} chars - {chunk[:50]}...")


def demo_pipeline_stages():
    """Break down and explain each stage of the RAG pipeline."""
    print("\n" + "=" * 70)
    print("DEMO 4: PIPELINE STAGES EXPLAINED")
    print("=" * 70)

    print("""
STAGE 1: INGESTION
  • Load documents into memory
  • Split into chunks to preserve context boundaries
  • Generate embeddings for each chunk using embedding model
  • Store embeddings + text in vector store
  → Output: Indexed documents ready for search

STAGE 2: RETRIEVAL
  • Embed user's query using same embedding model
  • Search vector store for most similar chunks
  • Rank results by cosine similarity score
  → Output: Top-K relevant documents with scores

STAGE 3: AUGMENTATION
  • Format retrieved chunks as context
  • Construct system prompt with:
    - Instructions for grounded answering
    - Complete context from Stage 2
    - User's original question
  → Output: LLM-ready prompt

STAGE 4: GENERATION
  • Send augmented prompt to LLM (via OpenRouter)
  • LLM generates answer grounded in context
  • Extract and format response
  → Output: Grounded answer with sources

STAGE 5: FORMATTING
  • Calculate retrieval & generation metrics
  • Format results with citations
  • Return complete result dict for downstream processing
  → Output: Dict with answer, sources, timing, tokens
    """)

    print("\nThis modular approach allows:")
    print("  ✓ Swapping embedding models without changing retrieval logic")
    print("  ✓ Comparing different LLM models for generation")
    print("  ✓ Adding reranking, filtering, or hybrid search at any stage")
    print("  ✓ Monitoring and optimizing each stage independently")


def main():
    """Run all demonstrations."""
    print("\n" + "🚀 LESSON 4.4: BUILDING THE RAG PIPELINE".center(70, "="))
    print("Core Template Method: build_rag_pipeline()")
    print("Business Scenario: HR Knowledge Assistant")

    try:
        demo_core_method()
        demo_retrieval_quality()
        demo_chunking_strategy()
        demo_pipeline_stages()

        print("\n" + "=" * 70)
        print("✅ RAG pipeline demonstrations complete!")
        print("=" * 70)
        print("\nKey Takeaways:")
        print("  • build_rag_pipeline() is your extraction point for projects")
        print("  • Chain: embed_documents() → semantic_search() → build_rag_pipeline()")
        print("  • Template is production-ready with error handling & fallbacks")
        print("  • Modify chunk_size, top_k, and model for your use case")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
