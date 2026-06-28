"""
Lesson 4.5: RAG Optimization (TODO)

In this lesson, you'll learn to improve retrieval quality through post-processing
and reranking techniques that don't require additional document retrieval.

Business Scenario:
  A search system retrieves relevant documents but ranks them suboptimally. Users
  find irrelevant results in top positions. Your task is to apply optimization
  techniques to improve ranking without fetching more documents (cost-effective).

LEARNING OBJECTIVES:
  • Diagnose common retrieval problems
  • Apply reranking techniques for better result quality
  • Implement metadata filtering and scoring
  • Evaluate ranking quality with metrics (precision, recall, NDCG, MRR)
  • Combine query expansion with semantic search

REFERENCE:
  • See lesson-05-rag-optimization.py (completed version)
  • Review lesson-04-building-rag-pipeline.py for raw retrieval output
  • Review shared/vector_store.py for similarity calculations

Run: python lesson-05-rag-optimization.py
"""

import os
import sys
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional

# Add project paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent / "shared"))

# TODO (PHASE 1): Import necessary modules
# You'll need:
#   - numpy for numerical operations
#   - typing for type hints


# ============================================================================
# PHASE 1: IMPLEMENT THE CORE TEMPLATE METHOD
# ============================================================================
# Your main task: implement improve_retrieval() following this specification

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
    TODO: Improve raw retrieval results through post-processing and reranking.

    This method applies to results from semantic_search() (Lesson 4.3) to enhance
    ranking quality without re-running expensive retrieval operations.

    Implementation should:
    1. Apply metadata filters if provided (hard filter)
    2. Select improvement technique (rerank, query_expansion, metadata_filtering)
    3. Calculate improved scores using the selected technique:
       - rerank: Apply length normalization to combat length bias
       - query_expansion: Combine semantic similarity with keyword overlap
       - metadata_filtering: Apply metadata boosts to scores
    4. Re-rank results by improved scores
    5. Add final rank positions (1-indexed)
    6. Return updated results with original + improved scores + factors

    Args:
        raw_results: Retrieved chunks with {rank, chunk_id, text, similarity, metadata}
        query: Original user query (for context-aware reranking)
        query_embedding: Embedding vector for the query
        improvement_method: "rerank", "query_expansion", or "metadata_filtering"
        documents: All documents (needed for hybrid/keyword search)
        metadata_filters: Dict of {field: value} to filter results
        length_normalize: Whether to normalize scores by document length

    Returns:
        Improved ranked results list with:
            - rank: 1-indexed position (REQUIRED)
            - chunk_id: Original chunk identifier (REQUIRED)
            - text: Chunk content (REQUIRED)
            - original_similarity: Raw semantic similarity (REQUIRED)
            - improved_score: Post-processing adjusted score (REQUIRED)
            - improvement_method: Technique applied (REQUIRED)
            - factors: Dict showing how score was calculated (REQUIRED)

    HINTS:
      • Start with metadata filtering if filters provided
      • Each technique modifies the score calculation:
        - Rerank: score * length_penalty
        - Query expansion: average(semantic + keyword_overlap)
        - Metadata filtering: score * metadata_boost
      • Length penalty formula: 1.0 / (1 + log(doc_length))
      • Keyword overlap: count(query_words & doc_words) / count(query_words | doc_words)
      • Sort by improved_score descending
      • Add rank after sorting (1-indexed enumeration)
    """

    # TODO (PHASE 1): Implement all steps above
    raise NotImplementedError("Implement improve_retrieval() - see docstring for steps")


# ============================================================================
# PHASE 2: IMPLEMENT HELPER METHODS
# ============================================================================


def _calculate_keyword_overlap(query: str, results: List[Dict]) -> Dict[str, float]:
    """
    TODO: Calculate Jaccard similarity between query and documents.

    Implementation should:
    1. Split query into lowercase words
    2. For each result, split text into lowercase words
    3. Calculate Jaccard similarity: |intersection| / |union|
    4. Return dict mapping chunk_id to overlap score

    Args:
        query: User query string
        results: List of result dicts with 'chunk_id' and 'text'

    Returns:
        Dict: {chunk_id: overlap_score (0-1)}

    HINTS:
      • Use set operations for intersection/union
      • Handle edge cases (empty query, empty results)
      • Scores should be between 0.0 and 1.0
    """

    # TODO (PHASE 2): Implement keyword overlap calculation
    raise NotImplementedError("Implement _calculate_keyword_overlap() - see docstring")


def _evaluate_ranking(
    improved_results: List[Dict],
    ground_truth_relevant: List[int],
) -> Dict:
    """
    TODO: Evaluate ranking quality with multiple metrics.

    Implementation should calculate:
    1. Precision@K: (relevant_retrieved) / (total_retrieved)
    2. Recall@K: (relevant_retrieved) / (total_relevant)
    3. MRR: 1 / (rank_of_first_relevant_result) or 0 if none
    4. NDCG: Ranking quality metric accounting for position
       - DCG = sum(relevance / log2(position + 1))
       - IDCG = ideal DCG (all relevant docs first)
       - NDCG = DCG / IDCG

    Args:
        improved_results: Ranked results with chunk_id
        ground_truth_relevant: List of chunk_ids known to be relevant

    Returns:
        Dict with keys: precision, recall, mrr, ndcg, relevant_retrieved

    HINTS:
      • Precision and Recall: simple counts
      • MRR: first relevant result, 0 if no relevant result found
      • NDCG uses log2(i+2) to avoid log(1)=0
      • Handle empty lists (return 0 for undefined metrics)
    """

    # TODO (PHASE 2): Implement evaluation metrics
    raise NotImplementedError("Implement _evaluate_ranking() - see docstring")


# ============================================================================
# PHASE 3: IMPLEMENT DEMONSTRATIONS
# ============================================================================


def demo_reranking_impact():
    """
    TODO: Show how reranking improves result quality.

    This demo should:
    1. Create 3 simulated raw retrieval results with {chunk_id, text, similarity, metadata}
    2. Define a query and dummy embedding
    3. Apply improve_retrieval() with improvement_method="rerank"
    4. Print before/after results showing improvement
    5. Display score factors

    REQUIREMENTS:
      • Results should be about a technical topic (ML, AI, etc.)
      • Show at least 3 results
      • Display improvement in ranking due to length normalization
    """

    print("\n" + "=" * 70)
    print("DEMO 1: RERANKING IMPACT")
    print("=" * 70)

    # TODO (PHASE 3): Create raw_results, apply improve_retrieval with rerank
    raise NotImplementedError("Implement demo_reranking_impact()")


def demo_query_expansion():
    """
    TODO: Show improved retrieval through query expansion.

    This demo should:
    1. Create 3 simulated retrieval results
    2. Define a query about a concept
    3. Apply improve_retrieval() with improvement_method="query_expansion"
    4. Compare semantic scores vs keyword overlap
    5. Show combined scores

    REQUIREMENTS:
      • Show how keyword overlap complements semantic similarity
      • Display factors for each result
      • Demonstrate better ranking after expansion
    """

    print("\n" + "=" * 70)
    print("DEMO 2: QUERY EXPANSION & KEYWORD OVERLAP")
    print("=" * 70)

    # TODO (PHASE 3): Implement query expansion demo
    raise NotImplementedError("Implement demo_query_expansion()")


def demo_metadata_filtering():
    """
    TODO: Show metadata filtering and scoring.

    This demo should:
    1. Create 3 results with different metadata (year, region, type)
    2. Define metadata_filters to restrict results
    3. Apply improve_retrieval() with improvement_method="metadata_filtering"
    4. Show how metadata filtering reduces result set
    5. Demonstrate metadata-aware scoring

    REQUIREMENTS:
      • Results should have meaningful metadata (not dummy)
      • Show filtering effect on result count
      • Display metadata values in output
    """

    print("\n" + "=" * 70)
    print("DEMO 3: METADATA FILTERING")
    print("=" * 70)

    # TODO (PHASE 3): Implement metadata filtering demo
    raise NotImplementedError("Implement demo_metadata_filtering()")


def demo_evaluation_metrics():
    """
    TODO: Show ranking evaluation metrics.

    This demo should:
    1. Create improved results with chunk_ids
    2. Define ground truth relevant chunk_ids
    3. Call _evaluate_ranking() to calculate metrics
    4. Print metrics with interpretation
    5. Show how metrics guide optimization

    REQUIREMENTS:
      • Have both relevant and irrelevant results
      • Show metrics: precision, recall, MRR, NDCG
      • Explain what each metric means for users
    """

    print("\n" + "=" * 70)
    print("DEMO 4: EVALUATION METRICS")
    print("=" * 70)

    # TODO (PHASE 3): Implement evaluation metrics demo
    raise NotImplementedError("Implement demo_evaluation_metrics()")


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
        print("\nImplementation steps:")
        print("  PHASE 1: Implement improve_retrieval() core method")
        print("  PHASE 2: Implement _calculate_keyword_overlap() and _evaluate_ranking()")
        print("  PHASE 3: Implement all 4 demo functions")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
