"""
Lesson 4.4: Building the RAG Pipeline (TODO)

In this lesson, you'll assemble a complete end-to-end RAG workflow that
combines retrieval (Lesson 4.2-4.3) and LLM generation into a single pipeline.

Business Scenario:
  A company needs an AI assistant that answers employee HR questions using
  internal knowledge base documents. Your system must retrieve relevant docs
  and generate accurate, sourced answers.

LEARNING OBJECTIVES:
  • Orchestrate embeddings, retrieval, and LLM calls into one pipeline
  • Handle document chunking and vector search transparently
  • Construct effective augmented prompts with retrieved context
  • Integrate OpenRouter LLM for answer generation
  • Format pipeline output with citations and performance metrics

REFERENCE:
  • See lesson-04-building-rag-pipeline.py (completed version)
  • Review shared/embeddings.py for EmbeddingEngine API
  • Review lesson-03-vector-store-lab.py for semantic_search patterns

Run: python lesson-04-building-rag-pipeline.py
"""

import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Optional
import numpy as np

# Add project paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent / "shared"))

# TODO (PHASE 1): Import necessary modules
# You'll need:
#   - EmbeddingEngine from shared.embeddings
#   - VectorStore from shared.vector_store
#   - time module (for measuring retrieval/generation time)
#   - requests module (for OpenRouter API calls)


# ============================================================================
# PHASE 1: IMPLEMENT THE CORE TEMPLATE METHOD
# ============================================================================
# Your main task: implement build_rag_pipeline() following this specification

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
    TODO: Build and execute a complete RAG pipeline end-to-end.

    This method should:
    1. Initialize EmbeddingEngine with the specified provider
    2. Chunk documents using _smart_chunk() helper (you'll implement this in PHASE 2)
    3. Generate embeddings for all chunks using embedding_engine.embed_query()
    4. Create a VectorStore and add all embedded chunks
    5. Embed the user query
    6. Search vector store for top-K most similar chunks (use cosine similarity)
    7. Format retrieved chunks as context
    8. Construct an augmented prompt with system instructions + context + query
    9. Call _generate_answer_with_llm() to get answer from LLM
    10. Calculate timing metrics and return complete result dict

    Args:
        documents: List of document texts to build knowledge base from
        query: User's natural language question
        top_k: Number of documents to retrieve (default: 5)
        chunk_size: Characters per chunk (default: 512)
        chunk_overlap: Overlap between chunks (default: 50)
        embedding_provider: "openrouter", "cohere", or "tfidf" (default: "openrouter")
        openrouter_key: OpenRouter API key (if None, uses OPENROUTER_API_KEY env var)
        llm_model: Model identifier for OpenRouter (default: meta-llama/llama-2-7b-chat)

    Returns:
        Dict with these required keys:
            - answer (str): Generated answer grounded in retrieved context
            - sources (List[Dict]): Each with keys: rank (1-indexed), chunk_id, text, similarity
            - context (str): Full context sent to LLM (for debugging)
            - retrieval_time (float): Seconds spent on embedding/search
            - generation_time (float): Seconds spent on LLM call
            - total_time (float): Sum of retrieval_time + generation_time
            - total_tokens (int): Approximate total tokens (input + output)
            - retrieval_count (int): Number of documents retrieved

    HINTS:
      • Start timing before Stage 1 (ingestion/retrieval)
      • Embedding dimension should match the embedding model output
      • For semantic search, use cosine similarity: dot(a, b) / (norm(a) * norm(b))
      • Retrieved chunks format: [{"rank": 1, "chunk_id": X, "text": "...", "similarity": 0.95}, ...]
      • Augmented prompt should include instructions, context, and question
      • Estimate tokens by counting words: roughly 1 token ≈ 0.75 words
    """

    # TODO (PHASE 1): Implement all 10 steps above
    # Replace this with your implementation
    raise NotImplementedError("Implement build_rag_pipeline() - see docstring for steps")


# ============================================================================
# PHASE 2: IMPLEMENT HELPER METHODS
# ============================================================================


def _smart_chunk(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """
    TODO: Split text into chunks while preserving sentence boundaries.

    This helper ensures chunks don't break mid-sentence, improving context
    coherence. Overlapping chunks help preserve context at chunk boundaries.

    Implementation should:
    1. Split text by sentence (use ". " as delimiter)
    2. Iterate through sentences, building chunks up to chunk_size
    3. When adding next sentence would exceed chunk_size, start new chunk
    4. Handle overlap by including last few sentences in next chunk
    5. Return list of non-empty chunks

    Args:
        text: Text to chunk
        chunk_size: Target chunk size in characters
        overlap: Overlap between chunks in characters

    Returns:
        List of text chunks, or [text] if text is very short

    HINTS:
      • Use text.split(". ") to find sentences
      • If result is a single chunk, return [text] to avoid empty lists
      • Track cumulative length to know when to start new chunk
      • Simple approach: don't worry about character-level overlap tracking;
        just ensure last sentence of previous chunk is included in next chunk
    """

    # TODO (PHASE 2): Implement sentence-aware chunking
    raise NotImplementedError("Implement _smart_chunk() - see docstring for steps")


def _generate_answer_with_llm(
    prompt: str,
    api_key: Optional[str] = None,
    model: str = "meta-llama/llama-2-7b-chat",
) -> str:
    """
    TODO: Generate an answer using OpenRouter LLM API.

    Implementation should:
    1. Check if api_key is provided; if not, try OPENROUTER_API_KEY env var
    2. If no key available, return graceful fallback message
    3. If requests library not available, return error message
    4. Call OpenRouter API endpoint: https://api.openrouter.ai/v1/chat/completions
    5. Send request with:
       - Method: POST
       - Headers: Authorization (Bearer token), HTTP-Referer, X-Title
       - JSON body: model, messages (list with user role), temperature, max_tokens
    6. Parse response and extract message content
    7. Handle HTTP errors gracefully with error message

    Args:
        prompt: The augmented prompt with context and question
        api_key: OpenRouter API key
        model: Model identifier

    Returns:
        Generated answer string, or fallback/error message

    HINTS:
      • Required headers: {"Authorization": f"Bearer {api_key}", ...}
      • Request timeout should be ~30 seconds
      • Response structure: result.get("choices", [{}])[0].get("message", {}).get("content", ...)
      • Use temperature=0.3 for factual responses, max_tokens=500 is reasonable
      • If status code != 200, return error message with status and text
    """

    # TODO (PHASE 2): Implement OpenRouter API call
    raise NotImplementedError("Implement _generate_answer_with_llm() - see docstring for steps")


# ============================================================================
# PHASE 3: IMPLEMENT DEMONSTRATIONS
# ============================================================================
# Each demo should call build_rag_pipeline() with different scenarios


def demo_core_method():
    """
    TODO: Demonstrate the core build_rag_pipeline() method.

    This demo should:
    1. Create an HR knowledge base (5-6 documents about policies)
    2. Define a realistic HR question
    3. Call build_rag_pipeline() with top_k=3
    4. Print retrieved sources with rank and similarity score
    5. Print the generated answer
    6. Print timing and token metrics

    REQUIREMENTS:
      • Knowledge base should be about HR policies (remote work, benefits, PTO, etc.)
      • Question should be answerable from the knowledge base
      • Display output clearly with separators and labels
    """

    print("\n" + "=" * 70)
    print("DEMO 1: CORE RAG PIPELINE")
    print("=" * 70)

    # TODO (PHASE 3): Create HR knowledge base and call build_rag_pipeline()
    raise NotImplementedError("Implement demo_core_method()")


def demo_retrieval_quality():
    """
    TODO: Show how retrieval quality affects answer quality.

    This demo should:
    1. Create a knowledge base about programming languages (4-5 documents)
    2. Define 3 different queries with varying difficulty/specificity
    3. For each query, call build_rag_pipeline() with top_k=2
    4. Compare results across queries
    5. Analyze which queries had better retrieval

    REQUIREMENTS:
      • Test queries should range from specific to vague
      • Display similarity scores and answer snippets
      • Show how better retrieval leads to better answers
    """

    print("\n" + "=" * 70)
    print("DEMO 2: RETRIEVAL QUALITY IMPACT")
    print("=" * 70)

    # TODO (PHASE 3): Implement quality comparison across queries
    raise NotImplementedError("Implement demo_retrieval_quality()")


def demo_chunking_strategy():
    """
    TODO: Demonstrate impact of different chunking strategies.

    This demo should:
    1. Create one long document about Machine Learning (200+ words)
    2. Define a specific query about a concept in that document
    3. Test 3 different chunk_size values: 200, 512, 1024
    4. For each chunk size, call build_rag_pipeline()
    5. Compare results: number of chunks, answer quality, timing

    REQUIREMENTS:
      • Show chunk count for each strategy
      • Display first 50 characters of each chunk
      • Explain trade-offs (more chunks = better coverage, slower search)
    """

    print("\n" + "=" * 70)
    print("DEMO 3: CHUNKING STRATEGY COMPARISON")
    print("=" * 70)

    # TODO (PHASE 3): Implement chunking strategy comparison
    raise NotImplementedError("Implement demo_chunking_strategy()")


def demo_pipeline_stages():
    """
    TODO: Explain and demonstrate each RAG pipeline stage.

    This demo should print out (and optionally demonstrate) these 5 stages:
    1. INGESTION: Document chunking and embedding
    2. RETRIEVAL: Query embedding and vector search
    3. AUGMENTATION: Constructing augmented prompt
    4. GENERATION: LLM answer creation
    5. FORMATTING: Output formatting with metrics

    For each stage, explain:
      • What happens in that stage
      • Inputs and outputs
      • Key decisions/parameters

    REQUIREMENTS:
      • Print clear stage breakdowns (can be text explanation or live demo)
      • Show benefits of modular pipeline design
      • Explain how to optimize each stage independently
    """

    print("\n" + "=" * 70)
    print("DEMO 4: PIPELINE STAGES EXPLAINED")
    print("=" * 70)

    # TODO (PHASE 3): Implement or print stage explanations
    raise NotImplementedError("Implement demo_pipeline_stages()")


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

    except NotImplementedError as e:
        print(f"\n⚠️  {e}")
        print("\nImplementation steps:")
        print("  PHASE 1: Implement build_rag_pipeline() core method")
        print("  PHASE 2: Implement _smart_chunk() and _generate_answer_with_llm()")
        print("  PHASE 3: Implement all 4 demo functions")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
