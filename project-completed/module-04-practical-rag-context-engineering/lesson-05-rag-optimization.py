"""
Lesson 4.5: RAG Optimization

Improve retrieval quality through advanced techniques: reranking, hybrid search,
query expansion, and metadata filtering. This lesson demonstrates how to diagnose
and fix common retrieval problems in RAG systems.

Business Scenario:
  A search system retrieves relevant documents but ranks them suboptimally.
  Users find irrelevant results in top positions. Your task is to apply
  optimization techniques to improve ranking quality without retrieving
  more documents (cost-effective improvement).

Run: python lesson-05-rag-optimization.py
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

from shared.embeddings import EmbeddingEngine
from shared.vector_store import VectorStore

# ============================================================================
# CORE TEMPLATE METHOD: improve_retrieval()
# ============================================================================


def improve_retrieval(
    raw_results: List[Dict],
    query: str,
    query_embedding: np.ndarray,
    improvement_method: str = "rerank",
    documents: Optional[List[str]] = None,
    metadata_filters: Optional[Dict] = None,
    length_normalize: bool = True,
) -> List[Dict]:
    """
    Improve raw retrieval results through post-processing and reranking.

    This template method demonstrates production techniques for improving
    search quality without re-running expensive retrieval operations. Apply
    after semantic_search() (Lesson 4.3) to enhance result ranking.

    Args:
        raw_results: Retrieved chunks from semantic_search() with {rank, chunk_id, text, similarity, metadata}
        query: Original user query (for context-aware reranking)
        query_embedding: Embedding vector for the query
        improvement_method: "rerank", "hybrid", "expand", or "filter"
        documents: All documents (needed for hybrid/keyword search)
        metadata_filters: Dict of {field: value} to filter results
        length_normalize: Whether to normalize scores by document length

    Returns:
        Improved ranked results list with:
            - rank: 1-indexed position
            - chunk_id: Original chunk identifier
            - text: Chunk content
            - original_similarity: Raw semantic similarity
            - improved_score: Post-processing adjusted score
            - improvement_method: Technique applied
            - factors: Dict showing how score was calculated
    """

    if not raw_results:
        return []

    improved = []

    # ---- STEP 1: APPLY METADATA FILTERS ----
    if metadata_filters:
        filtered_results = [
            r for r in raw_results
            if all(
                r.get("metadata", {}).get(k) == v
                for k, v in metadata_filters.items()
            )
        ]
        raw_results = filtered_results if filtered_results else raw_results

    # ---- STEP 2: APPLY IMPROVEMENT TECHNIQUE ----

    if improvement_method == "rerank":
        # Multi-signal reranking: combine similarity + length normalization + recency
        for result in raw_results:
            similarity_score = result["similarity"]

            # Length normalization (penalize very long docs to avoid length bias)
            text_length = len(result["text"].split())
            length_penalty = 1.0 if not length_normalize else min(1.0, 50.0 / max(text_length, 1))

            # Combined score
            improved_score = similarity_score * length_penalty

            improved.append({
                "chunk_id": result["chunk_id"],
                "text": result["text"],
                "original_similarity": similarity_score,
                "improved_score": improved_score,
                "improvement_method": "rerank",
                "factors": {
                    "similarity": similarity_score,
                    "length_penalty": length_penalty,
                    "combined": improved_score,
                },
            })

    elif improvement_method == "query_expansion":
        # For queries with few results, expand and show alternative queries
        keyword_scores = _calculate_keyword_overlap(query, raw_results)
        for result in raw_results:
            combined = (result["similarity"] + keyword_scores[result["chunk_id"]]) / 2
            improved.append({
                "chunk_id": result["chunk_id"],
                "text": result["text"],
                "original_similarity": result["similarity"],
                "improved_score": combined,
                "improvement_method": "query_expansion",
                "factors": {
                    "semantic_sim": result["similarity"],
                    "keyword_overlap": keyword_scores[result["chunk_id"]],
                    "combined": combined,
                },
            })

    elif improvement_method == "metadata_filtering":
        # Apply strict metadata filtering to target specific document types
        for result in raw_results:
            metadata = result.get("metadata", {})
            metadata_score = 1.0  # Base score, can be customized
            improved_score = result["similarity"] * metadata_score
            improved.append({
                "chunk_id": result["chunk_id"],
                "text": result["text"],
                "original_similarity": result["similarity"],
                "improved_score": improved_score,
                "improvement_method": "metadata_filtering",
                "factors": {
                    "similarity": result["similarity"],
                    "metadata_boost": metadata_score,
                    "combined": improved_score,
                },
            })

    else:  # Default: just rerank
        return improve_retrieval(raw_results, query, query_embedding, "rerank", documents, metadata_filters, length_normalize)

    # ---- STEP 3: RE-RANK BY IMPROVED SCORES ----
    improved.sort(key=lambda x: x["improved_score"], reverse=True)

    # Add final rank positions
    for rank, result in enumerate(improved, 1):
        result["rank"] = rank

    return improved


# ============================================================================
# HELPER METHODS
# ============================================================================


def _calculate_keyword_overlap(query: str, results: List[Dict]) -> Dict[str, float]:
    """Calculate keyword overlap between query and documents."""
    query_words = set(query.lower().split())
    overlap_scores = {}

    for result in results:
        doc_words = set(result["text"].lower().split())
        overlap = len(query_words & doc_words)
        total = len(query_words | doc_words)
        score = overlap / total if total > 0 else 0.0
        overlap_scores[result["chunk_id"]] = score

    return overlap_scores


def _evaluate_ranking(
    improved_results: List[Dict],
    ground_truth_relevant: List[int],
) -> Dict:
    """
    Evaluate ranking quality with precision, recall, NDCG metrics.

    Args:
        improved_results: Ranked results from improve_retrieval()
        ground_truth_relevant: List of chunk_ids known to be relevant

    Returns:
        Dict with {precision, recall, mrr, ndcg}
    """
    k = len(improved_results)
    retrieved_ids = [r["chunk_id"] for r in improved_results]

    # Precision@K: How many retrieved are actually relevant
    relevant_retrieved = sum(1 for cid in retrieved_ids if cid in ground_truth_relevant)
    precision = relevant_retrieved / k if k > 0 else 0.0

    # Recall@K: How many relevant docs did we retrieve
    recall = relevant_retrieved / len(ground_truth_relevant) if ground_truth_relevant else 0.0

    # MRR: Position of first relevant result
    mrr = 0.0
    for rank, result in enumerate(improved_results, 1):
        if result["chunk_id"] in ground_truth_relevant:
            mrr = 1.0 / rank
            break

    # NDCG: Ranking quality considering relevance scores
    dcg = sum(
        (1.0 if improved_results[i]["chunk_id"] in ground_truth_relevant else 0.0) / np.log2(i + 2)
        for i in range(len(improved_results))
    )
    idcg = sum(1.0 / np.log2(i + 2) for i in range(min(len(ground_truth_relevant), k)))
    ndcg = dcg / idcg if idcg > 0 else 0.0

    return {
        "precision": precision,
        "recall": recall,
        "mrr": mrr,
        "ndcg": ndcg,
        "relevant_retrieved": relevant_retrieved,
    }


# ============================================================================
# DEMONSTRATIONS
# ============================================================================


def demo_reranking_impact():
    """Show how reranking improves result quality."""
    print("\n" + "=" * 70)
    print("DEMO 1: RERANKING IMPACT")
    print("=" * 70)

    # Simulated raw retrieval results (from Lesson 4.4)
    raw_results = [
        {
            "rank": 1,
            "chunk_id": 101,
            "text": "Deep learning neural networks with many hidden layers process visual data.",
            "similarity": 0.92,
            "metadata": {"doc_type": "technical"},
        },
        {
            "rank": 2,
            "chunk_id": 102,
            "text": "Neural networks and deep learning are areas of AI.",
            "similarity": 0.88,
            "metadata": {"doc_type": "overview"},
        },
        {
            "rank": 3,
            "chunk_id": 103,
            "text": "Network protocols and communication layers in systems.",
            "similarity": 0.71,
            "metadata": {"doc_type": "technical"},
        },
    ]

    query = "neural network architecture"
    query_embedding = np.array([0.5] * 10)  # Dummy embedding

    print(f"\nQuery: {query}")
    print("\nBEFORE Reranking:")
    for r in raw_results:
        print(f"  [{r['rank']}] Sim: {r['similarity']:.2f} - {r['text'][:50]}...")

    # Apply reranking
    improved = improve_retrieval(
        raw_results=raw_results,
        query=query,
        query_embedding=query_embedding,
        improvement_method="rerank",
        length_normalize=True,
    )

    print("\nAFTER Reranking (with length normalization):")
    for r in improved:
        print(f"  [{r['rank']}] Score: {r['improved_score']:.3f} - {r['text'][:50]}...")
        print(f"       Factors: {r['factors']}")


def demo_query_expansion():
    """Show improved retrieval through query expansion."""
    print("\n" + "=" * 70)
    print("DEMO 2: QUERY EXPANSION & KEYWORD OVERLAP")
    print("=" * 70)

    raw_results = [
        {
            "chunk_id": 201,
            "text": "Machine learning is a subset of artificial intelligence.",
            "similarity": 0.75,
        },
        {
            "chunk_id": 202,
            "text": "Deep neural networks learn patterns from data.",
            "similarity": 0.82,
        },
        {
            "chunk_id": 203,
            "text": "Training requires labeled datasets and optimization.",
            "similarity": 0.68,
        },
    ]

    query = "machine learning training process"

    print(f"\nQuery: {query}")
    print("Original (Semantic) Ranking:")
    for r in sorted(raw_results, key=lambda x: x["similarity"], reverse=True):
        print(f"  Sim: {r['similarity']:.2f} - {r['text'][:50]}...")

    # Apply query expansion (combining semantic + keyword)
    improved = improve_retrieval(
        raw_results=raw_results,
        query=query,
        query_embedding=np.array([0.5] * 10),
        improvement_method="query_expansion",
    )

    print("\nAfter Query Expansion (semantic + keyword):")
    for r in improved:
        print(f"  Score: {r['improved_score']:.3f} - {r['text'][:50]}...")
        print(f"         Semantic: {r['factors']['semantic_sim']:.3f}, Keyword: {r['factors']['keyword_overlap']:.3f}")


def demo_metadata_filtering():
    """Show metadata filtering and scoring."""
    print("\n" + "=" * 70)
    print("DEMO 3: METADATA FILTERING")
    print("=" * 70)

    raw_results = [
        {
            "chunk_id": 301,
            "text": "Founded in 2010 in Silicon Valley",
            "similarity": 0.85,
            "metadata": {"year": 2010, "region": "US", "type": "founding"},
        },
        {
            "chunk_id": 302,
            "text": "Expanded to Europe in 2015",
            "similarity": 0.78,
            "metadata": {"year": 2015, "region": "EU", "type": "expansion"},
        },
        {
            "chunk_id": 303,
            "text": "Opened Asia office in 2018",
            "similarity": 0.76,
            "metadata": {"year": 2018, "region": "APAC", "type": "expansion"},
        },
    ]

    query = "company expansion timeline"
    print(f"\nQuery: {query}")

    print("\nAll Results:")
    for r in raw_results:
        print(f"  [{r['metadata']['year']}] {r['metadata']['region']} - {r['text'][:40]}...")

    # Apply filtering for recent documents (>= 2015)
    metadata_filters = {"type": "expansion"}
    print(f"\nFiltering for: {metadata_filters}")

    improved = improve_retrieval(
        raw_results=raw_results,
        query=query,
        query_embedding=np.array([0.5] * 10),
        improvement_method="metadata_filtering",
        metadata_filters=metadata_filters,
    )

    print("Filtered Results:")
    for r in improved:
        print(f"  [{r['metadata']['year']}] Score: {r['improved_score']:.3f} - {r['text'][:40]}...")


def demo_evaluation_metrics():
    """Show evaluation metrics for ranking quality."""
    print("\n" + "=" * 70)
    print("DEMO 4: EVALUATION METRICS")
    print("=" * 70)

    improved_results = [
        {"chunk_id": 1, "text": "Relevant doc 1", "improved_score": 0.95},
        {"chunk_id": 2, "text": "Irrelevant doc", "improved_score": 0.80},
        {"chunk_id": 3, "text": "Relevant doc 2", "improved_score": 0.75},
        {"chunk_id": 4, "text": "Somewhat relevant", "improved_score": 0.60},
    ]

    # Ground truth: docs 1, 3, 5 are relevant
    ground_truth_relevant = [1, 3, 5]

    metrics = _evaluate_ranking(improved_results, ground_truth_relevant)

    print(f"\nRetrieved 4 results. Ground truth: 3 relevant documents")
    print(f"\nResults:")
    for r in improved_results:
        is_relevant = "✓" if r["chunk_id"] in ground_truth_relevant else "✗"
        print(f"  [{is_relevant}] {r['text']:20s} (Score: {r['improved_score']:.2f})")

    print(f"\nMetrics:")
    print(f"  Precision@4: {metrics['precision']:.3f} (How many retrieved are relevant?)")
    print(f"  Recall@4: {metrics['recall']:.3f} (How many relevant docs did we find?)")
    print(f"  MRR: {metrics['mrr']:.3f} (Position of first relevant result?)")
    print(f"  NDCG: {metrics['ndcg']:.3f} (Quality of ranking?)")
    print(f"  Relevant Retrieved: {metrics['relevant_retrieved']}/{len(ground_truth_relevant)}")

    print("\nInterpretation:")
    print("  • Precision = 2/4 = 0.5 (half of results are relevant)")
    print("  • Recall = 2/3 = 0.67 (we found 2 of 3 relevant docs)")
    print("  • MRR = 1/1 = 1.0 (first result is relevant)")
    print("  • NDCG: Balanced scoring for top-ranked relevant docs")


def main():
    """Run all demonstrations."""
    print("\n" + "🚀 LESSON 4.5: RAG OPTIMIZATION".center(70, "="))
    print("Core Template Method: improve_retrieval()")
    print("Business Scenario: Improve Search Result Quality")

    try:
        demo_reranking_impact()
        demo_query_expansion()
        demo_metadata_filtering()
        demo_evaluation_metrics()

        print("\n" + "=" * 70)
        print("✅ RAG optimization demonstrations complete!")
        print("=" * 70)
        print("\nKey Takeaways:")
        print("  • improve_retrieval() post-processes without re-retrieving")
        print("  • Reranking improves quality without API calls")
        print("  • Metadata filtering targets specific document types")
        print("  • Evaluation metrics quantify ranking improvements")
        print("  • Combine techniques for best results")

    except NotImplementedError as e:
        print(f"\n⚠️  {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
