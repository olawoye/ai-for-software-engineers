"""
Lesson 4.5: RAG Optimization

Learn to diagnose and improve retrieval quality through hybrid search,
metadata filtering, query transformation, and reranking techniques.

Run: python lesson-05-rag-optimization.py
"""

import os
from shared.embeddings import EmbeddingEngine
from shared.vector_store import VectorStore
from shared.retriever import Retriever, HybridRetriever, KeywordRetriever
from shared.rag_pipeline import RAGEvaluator


def demo_retrieval_problems():
    """Demonstrate common retrieval problems."""
    print("\n" + "=" * 60)
    print("RETRIEVAL PROBLEMS")
    print("=" * 60)

    print("""
Common Retrieval Issues:

1. Missing Documents
   Problem: Query doesn't retrieve relevant documents
   Cause: Bad query embedding or insufficient semantic similarity
   Solution: Query expansion, embedding model improvement

2. Noisy Results
   Problem: Retrieved documents are tangentially relevant
   Cause: High false positive rate, broad similarity threshold
   Solution: Reranking, stricter similarity thresholds

3. Incomplete Coverage
   Problem: Different queries need different sources
   Cause: Single retrieval method (semantic or keyword)
   Solution: Hybrid search combining multiple methods

4. Metadata Not Used
   Problem: Relevant documents filtered out by metadata
   Cause: Metadata filtering too strict
   Solution: Relax constraints, use metadata scoring

5. Large Document Skew
   Problem: Long documents always rank highest
   Cause: Similarity not normalized by document length
   Solution: Length-aware scoring, document chunking
    """)


def demo_hybrid_search():
    """Compare semantic vs keyword vs hybrid retrieval."""
    print("\n" + "=" * 60)
    print("HYBRID SEARCH COMPARISON")
    print("=" * 60)

    documents = [
        "Machine learning systems learn from training data.",
        "Deep neural networks have multiple hidden layers.",
        "Natural language processing handles text input.",
        "Computer vision processes images and videos.",
        "Reinforcement learning optimizes through rewards.",
    ]

    # Setup
    cohere_key = os.getenv("COHERE_API_KEY")
    embedding_engine = EmbeddingEngine(
        method="cohere" if cohere_key else "tfidf",
        cohere_api_key=cohere_key
    )
    vector_store = VectorStore(embedding_dim=300)

    embeddings = embedding_engine.embed_documents(documents)
    vector_store.add(documents, embeddings)

    # Retrievers
    semantic_retriever = Retriever(vector_store, embedding_engine, top_k=3)
    keyword_retriever = KeywordRetriever(documents, top_k=3)

    # Test query
    query = "neural network layers"

    print(f"\nQuery: {query}")

    # Semantic search
    print("\nSemantic Search Results:")
    semantic_results = semantic_retriever.retrieve(query)
    for i, r in enumerate(semantic_results, 1):
        print(f"  {i}. {r['document'][:50]}... (sim: {r['similarity']:.3f})")

    # Keyword search
    print("\nKeyword Search Results:")
    keyword_results = keyword_retriever.retrieve(query)
    for i, r in enumerate(keyword_results, 1):
        print(f"  {i}. {r['document'][:50]}... (sim: {r['similarity']:.3f})")


def demo_query_expansion():
    """Show query expansion techniques."""
    print("\n" + "=" * 60)
    print("QUERY EXPANSION")
    print("=" * 60)

    print("""
Query Expansion Techniques:

1. Synonym Expansion
   Original: "large language model"
   Expanded: ["large language model", "LLM", "foundation model"]

2. Semantic Expansion
   Original: "How to train?"
   Expanded: ["How to train", "training process", "optimization"]

3. Contextual Expansion
   Original: "Benefits"
   Context: Company HR system
   Expanded: ["Benefits", "Health insurance", "PTO", "Compensation"]

4. Query Decomposition
   Original: "What are company practices?"
   Decomposed: [
       "What is our hiring process?",
       "How do we handle remote work?",
       "What benefits do we offer?"
   ]

5. Multi-Hop Expansion
   Query1: "AI tools we use"
   → Results mention "Python libraries"
   Query2: "What is Python pandas?"
   → Results provide context
    """)


def demo_reranking():
    """Demonstrate reranking for result quality."""
    print("\n" + "=" * 60)
    print("RERANKING")
    print("=" * 60)

    print("""
Reranking Strategies:

1. Simple Threshold
   Keep only results above similarity threshold
   Pro: Fast, simple
   Con: Binary decision, loses nuance

2. Length Normalization
   Penalize very long documents
   Score = similarity / (1 + log(doc_length))
   Pro: Fair to all documents
   Con: Reduces information from longer docs

3. Diversity Reranking
   Reduce redundancy in results
   Lower score if similar to previous results
   Pro: More diverse perspectives
   Con: May remove relevant variations

4. Learned Reranking
   Use ML model to score (query, doc) pairs
   Train on relevance labels
   Pro: Optimal for your data
   Con: Requires labeled data

5. Multi-Stage Reranking
   BM25 (fast) → Dense (accurate) → LLM (thorough)
   Pro: Balance speed and quality
   Con: Complex pipeline
    """)


def demo_metadata_filtering():
    """Advanced metadata filtering."""
    print("\n" + "=" * 60)
    print("METADATA FILTERING & SCORING")
    print("=" * 60)

    documents = [
        "Founded in 2010 in Silicon Valley",
        "Expanded to Europe in 2015",
        "Opened Asia office in 2018",
        "Went public in 2020",
    ]

    metadata = [
        {"year": 2010, "region": "US", "type": "founding"},
        {"year": 2015, "region": "EU", "type": "expansion"},
        {"year": 2018, "region": "APAC", "type": "expansion"},
        {"year": 2020, "region": "NASDAQ", "type": "milestone"},
    ]

    print("\nDocuments with metadata:")
    for doc, meta in zip(documents, metadata):
        print(f"  {doc} → {meta}")

    print("""
Filtering Examples:

1. Hard Filter
   Only documents where year >= 2015
   Result: 3 documents

2. Soft Filter (Scoring)
   Score boost if year >= 2015
   Result: All documents, but recent ones ranked higher

3. Multi-Field Filter
   region == "US" AND type == "founding"
   Result: 1 document

4. Range Filter
   2015 <= year <= 2020
   Result: 3 documents
    """)


def demo_evaluation():
    """Evaluate retrieval quality."""
    print("\n" + "=" * 60)
    print("RETRIEVAL EVALUATION")
    print("=" * 60)

    print("""
Retrieval Metrics:

1. Precision@K
   What fraction of top-K results are relevant?
   Good for: User-facing retrieval

2. Recall@K
   Did we find all relevant documents in top-K?
   Good for: Exhaustive search needs

3. MRR (Mean Reciprocal Rank)
   On average, at what position is first relevant result?
   Good for: Single-best-answer retrieval

4. NDCG (Normalized Discounted Cumulative Gain)
   How well are relevant docs ranked?
   Good for: Ranking quality assessment

5. MAP (Mean Average Precision)
   Average precision across multiple queries
   Good for: System-wide performance
    """)

    # Example evaluation
    retrieved = [
        {"document": "Relevant doc 1", "similarity": 0.9},
        {"document": "Irrelevant doc", "similarity": 0.7},
        {"document": "Relevant doc 2", "similarity": 0.6},
    ]

    ground_truth = [
        "Relevant doc 1",
        "Relevant doc 2",
        "Relevant doc 3",  # Not retrieved
    ]

    results = RAGEvaluator.evaluate_retrieval(retrieved, ground_truth)

    print(f"\nExample Evaluation:")
    print(f"  Precision@3: {results['precision']:.2f} (2/3 relevant)")
    print(f"  Recall@3: {results['recall']:.2f} (2/3 of all relevant)")
    print(f"  F1 Score: {results['f1']:.2f}")


def main():
    """Run all demonstrations."""
    print("\n" + "🚀 LESSON 4.5: RAG OPTIMIZATION".center(60, "="))

    try:
        demo_retrieval_problems()
        demo_hybrid_search()
        demo_query_expansion()
        demo_reranking()
        demo_metadata_filtering()
        demo_evaluation()

        print("\n" + "=" * 60)
        print("✅ RAG optimization demonstrations complete!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
