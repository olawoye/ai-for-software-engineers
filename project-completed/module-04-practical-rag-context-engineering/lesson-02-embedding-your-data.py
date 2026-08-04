"""
Lesson 4.2: Embedding Your Data

Learn how to prepare raw documents, chunk content appropriately,
generate embeddings via Cohere, and create a retrieval-ready knowledge base.

This lesson demonstrates the core embed_documents() template method that
learners can reuse in their own projects with minimal configuration changes.

Run: python lesson-02-embedding-your-data.py
Requires: export COHERE_API_KEY='your-key-here'
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict
import numpy as np

# Import from shared module (reference path)
sys.path.insert(0, str(Path(__file__).parent))
from shared.embeddings import EmbeddingEngine, batch_similarity

# Load sample corpus
def load_sample_corpus() -> List[str]:
    """Load sample documents from sample-corpus.json."""
    corpus_path = Path(__file__).parent.parent.parent / "datasets" / "sample-corpus.json"
    try:
        with open(corpus_path, "r") as f:
            data = json.load(f)
            docs = list(data["sample_corpus"].values())
            return docs
    except Exception as e:
        print(f"Warning: Could not load corpus ({e}), using minimal sample")
        return [
            "Sample document 1: Basic content",
            "Sample document 2: More content",
            "Sample document 3: Additional content"
        ]


def clear_screen():
    """Clear terminal screen."""
    os.system("clear" if os.name == "posix" else "cls")


def validate_api_key():
    """Check if Cohere API key is set. Exit if not."""
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        print("\n" + "=" * 70)
        print("❌ COHERE_API_KEY not set")
        print("=" * 70)
        print("\nSetup required:")
        print("  export COHERE_API_KEY='your-key-here'")
        print("\nGet free API key:")
        print("  https://cohere.com (100k requests/month free)")
        print("\n" + "=" * 70)
        sys.exit(1)


def display_code(lines: list, title: str = ""):
    """Display code with line numbers."""
    if title:
        print(f"\n📝 {title}\n")
    for i, line in enumerate(lines, 1):
        print(f"  {i:2} | {line}")


# ============================================================================
# CORE TEMPLATE METHOD: embed_documents()
# ============================================================================

def embed_documents(
    documents: List[str],
    chunk_size: int = 512,
    chunk_overlap: int = 50,
    provider: str = "cohere",
    openrouter_key: str | None = None,
) -> List[Dict]:
    """Core template method: Chunk documents and generate embeddings.
    
    This is the production-ready ingestion pattern used across RAG systems.
    Learners can extract this method and adapt it for their own document sources.
    
    Args:
        documents: List of raw text documents
        chunk_size: Target characters per chunk (for context preservation)
        chunk_overlap: Overlap between chunks (prevents breaking key concepts)
        provider: "cohere" (default) - primary embedding provider
        openrouter_key: OpenRouter API key (or from env OPENROUTER_API_KEY)
    
    Returns:
        List of dicts with structure:
        {
            'chunk_id': str,
            'text': str,
            'embedding': np.ndarray,
            'metadata': dict with 'provider' showing method used,
            'char_count': int
        }
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
                'provider': engine.actual_method,  # Track actual provider after fallback
            },
            'char_count': chunk_info['char_count'],
        })
    
    return result


# ============================================================================
# HELPER: Smart chunking strategy
# ============================================================================

def _smart_chunk(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """Intelligently split text into overlapping chunks.
    
    Splits at sentence boundaries to preserve meaning.
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
# INTERACTIVE PATTERNS (Menu-driven)
# ============================================================================

def pattern_1_core_method():
    """PATTERN 1: Core embed_documents() Template Method"""
    clear_screen()
    print("\n" + "=" * 70)
    print("PATTERN 1: Core Method - embed_documents() Template")
    print("=" * 70)

    code_lines = [
        "def embed_documents(",
        "    documents: List[str],",
        "    chunk_size: int = 512,",
        "    chunk_overlap: int = 50,",
        "    provider: str = 'cohere',",
        ") -> List[Dict]:",
        "    # Step 1: Intelligently chunk documents",
        "    # Step 2: Initialize embedding engine",
        "    # Step 3: Generate embeddings (1024-dim)",
        "    # Step 4: Return chunks with embeddings + metadata",
    ]

    display_code(code_lines, "Core Template Method:")

    print("\n💡 What you'll learn:")
    print("  • How to intelligently chunk long documents")
    print("  • Generate semantic embeddings using Cohere")
    print("  • Structure output for vector storage")
    print("  • Reusable template for your own projects")

    print("\n📚 Key concepts:")
    print("  • Chunking preserves context boundaries (sentence-based)")
    print("  • Embeddings are 1024-dimensional semantic vectors")
    print("  • Metadata tracks document lineage and provider used")

    print("\n" + "-" * 70)
    input("Press [ENTER] to run this pattern with real embeddings...")

    # >>> CORE METHOD: Demonstration with sample corpus
    sample_docs = load_sample_corpus()[:3]  # Use first 3 documents from corpus

    # Use the core template method
    embedded_chunks = embed_documents(
        sample_docs,
        chunk_size=256,
        chunk_overlap=30,
        provider="cohere",
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

    print("\n" + "-" * 70)
    print("✅ Pattern complete. Return to menu.")


def pattern_2_semantic_search():
    """PATTERN 2: Semantic Search with Consistent Embeddings"""
    clear_screen()
    print("\n" + "=" * 70)
    print("PATTERN 2: Semantic Search with Embedded Queries")
    print("=" * 70)

    code_lines = [
        "# Step 1: Embed documents",
        "embedded_chunks = embed_documents(docs, provider='cohere')",
        "doc_embeddings = np.array([c['embedding'] for c in embedded_chunks])",
        "",
        "# Step 2: Embed query using SAME provider",
        "query_result = embed_documents([query], provider='cohere')",
        "query_embedding = query_result[0]['embedding']",
        "",
        "# Step 3: Compute cosine similarities",
        "similarities = batch_similarity(query_embedding, doc_embeddings)",
        "top_indices = np.argsort(similarities)[::-1][:3]",
    ]

    display_code(code_lines, "Semantic Search Pattern:")

    print("\n💡 What you'll learn:")
    print("  • Embedding queries consistently with documents")
    print("  • Computing cosine similarity between vectors")
    print("  • Retrieving most relevant documents by meaning")
    print("  • Why provider consistency matters for dimensions")

    print("\n📚 Key concepts:")
    print("  • Cohere embeddings: 1024-dimensional semantic vectors")
    print("  • Cosine similarity: measure meaning similarity (0-1 scale)")
    print("  • Vectorization enables semantic search, not keyword matching")

    print("\n" + "-" * 70)
    input("Press [ENTER] to run semantic search on sample docs...")

    # >>> REFERENCE: Get embeddings from sample corpus
    sample_docs = load_sample_corpus()[:3]
    
    embedded_chunks = embed_documents(sample_docs, chunk_size=256, provider="cohere")
    
    # Embed a query using the SAME provider as the documents
    query = "What is the company's remote work policy?"
    actual_provider = embedded_chunks[0]['metadata']['provider']
    
    query_result = embed_documents(
        [query],
        chunk_size=256,
        provider=actual_provider,
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

    print("-" * 70)
    print("✅ Pattern complete. Return to menu.")


def pattern_3_chunking_strategies():
    """PATTERN 3: Chunking Strategies Comparison"""
    clear_screen()
    print("\n" + "=" * 70)
    print("PATTERN 3: Chunking Strategies - Finding the Right Granularity")
    print("=" * 70)

    code_lines = [
        "def _smart_chunk(text: str, chunk_size: int, overlap: int):",
        "    \"\"\"Split at sentence boundaries.\"\"\"",
        "    sentences = text.split('. ')",
        "    chunks = []",
        "    current_chunk = []",
        "    current_length = 0",
        "    ",
        "    for sent in sentences:",
        "        if current_length + len(sent) > chunk_size and current_chunk:",
        "            chunks.append('. '.join(current_chunk))",
        "            # Overlap: keep last ~overlap chars",
        "            current_chunk = [...]",
        "        current_chunk.append(sent)",
        "    return chunks",
    ]

    display_code(code_lines, "Smart Chunking Algorithm:")

    print("\n💡 What you'll learn:")
    print("  • How to split documents at semantic boundaries")
    print("  • Trade-offs: smaller chunks vs. context preservation")
    print("  • Overlap prevents breaking key concepts across chunks")
    print("  • Choosing chunk_size for your domain and use case")

    print("\n📚 Key concepts:")
    print("  • Small chunks (100-150): precise retrieval, less context")
    print("  • Medium chunks (250-500): balanced (most common)")
    print("  • Large chunks (1000+): more context, less precision")
    print("  • Overlap helps with boundary issues in semantic search")

    print("\n" + "-" * 70)
    input("Press [ENTER] to see different chunk sizes in action...")

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

    print("\n" + "-" * 70)
    print("✅ Pattern complete. Return to menu.")


def pattern_4_provider_error_handling():
    """PATTERN 4: Error Handling & API Robustness"""
    clear_screen()
    print("\n" + "=" * 70)
    print("PATTERN 4: Error Handling - Production Readiness")
    print("=" * 70)

    code_lines = [
        "def embed_documents(documents: List[str]) -> List[Dict]:",
        "    if not COHERE_API_KEY:",
        "        raise RuntimeError(",
        "            'COHERE_API_KEY required. Set it or get one at cohere.com'",
        "        )",
        "    ",
        "    try:",
        "        embeddings = engine.embed_documents(chunk_texts)",
        "        print(f'✓ Generated {len(embeddings)} embeddings')",
        "        return results",
        "    except RuntimeError as e:",
        "        print(f'Embedding failed: {e}')",
        "        raise  # Let caller handle failure",
    ]

    display_code(code_lines, "Production Error Handling:")

    print("\n💡 What you'll learn:")
    print("  • How embeddings can fail (API key, rate limits, etc.)")
    print("  • Cohere as primary provider (no silent fallbacks)")
    print("  • Clear error messages for debugging")
    print("  • Why production systems need explicit error handling")

    print("\n📚 Key concepts:")
    print("  • Cohere API: 1024-dim embeddings with input_type")
    print("  • Dimension consistency is CRITICAL for similarity scoring")
    print("  • Clear errors help operators respond faster in production")
    print("  • No silent fallbacks prevent debugging nightmares")

    print("\n" + "-" * 70)
    input("Press [ENTER] to test embedding with valid config...")

    # Test with minimal docs
    test_docs = ["embedding test one", "embedding test two"]
    
    try:
        result = embed_documents(
            test_docs,
            chunk_size=100,
            provider="cohere",
        )
        
        print(f"\n✓ Successfully embedded {len(result)} chunks")
        print(f"✓ Provider used: {result[0]['metadata']['provider']}")
        print(f"✓ Embedding dims: {result[0]['embedding'].shape[0]}")
        print(f"✓ Metadata tracked: {result[0]['metadata']}")
        
    except RuntimeError as e:
        print(f"\n❌ Embedding failed: {e}")
        print("This is expected behavior - clear error, not silent failure!")

    print("\n" + "-" * 70)
    print("✅ Pattern complete. Return to menu.")


def show_menu():
    """Display main menu."""
    clear_screen()
    print("\n" + "=" * 70)
    print("🚀 LESSON 4.2: EMBEDDING YOUR DATA".center(70))
    print("=" * 70)
    print()
    print("  Choose a pattern to learn:\n")
    print("    [1] PATTERN: Core embed_documents() Template")
    print("        → Chunk documents, generate embeddings, structure output\n")
    print("    [2] PATTERN: Semantic Search with Embeddings")
    print("        → Query embeddings, similarity computation, retrieval\n")
    print("    [3] PATTERN: Chunking Strategies")
    print("        → Different chunk sizes, overlap, semantic boundaries\n")
    print("    [4] PATTERN: Error Handling & Robustness")
    print("        → API failures, clear errors, production readiness\n")
    print("    [Q] Quit\n")
    print("=" * 70)


def main():
    """Main interactive loop."""
    # Validate API key before starting
    validate_api_key()

    patterns = {
        "1": pattern_1_core_method,
        "2": pattern_2_semantic_search,
        "3": pattern_3_chunking_strategies,
        "4": pattern_4_provider_error_handling,
    }

    while True:
        show_menu()
        choice = input("Choose [1-4] or [Q] to quit: ").strip().lower()

        if choice == "q":
            clear_screen()
            print("\n✅ Thanks for learning! Remember to:")
            print("   • Extract embed_documents() into your projects")
            print("   • Chunk at sentence boundaries to preserve meaning")
            print("   • Keep queries and documents using same embedder")
            print("   • Monitor embeddings costs (Cohere free: 100k/month)")
            print("\n")
            break

        if choice in patterns:
            try:
                patterns[choice]()
            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupted. Returning to menu.\n")
            except Exception as e:
                clear_screen()
                print(f"\n❌ Error: {e}\n")
                import traceback
                traceback.print_exc()

            input("\nPress [ENTER] to return to menu...")
        else:
            print("❌ Invalid choice. Try again.")
            input("\nPress [ENTER] to continue...")


if __name__ == "__main__":
    main()
