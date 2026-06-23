"""
Retrieval logic for RAG systems.
Handles query expansion, reranking, and multi-stage retrieval.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from .embeddings import EmbeddingEngine
from .vector_store import VectorStore


class Retriever:
    """Multi-stage retrieval system for RAG."""

    def __init__(
        self,
        vector_store: VectorStore,
        embedding_engine: EmbeddingEngine,
        top_k: int = 5,
    ):
        self.vector_store = vector_store
        self.embedding_engine = embedding_engine
        self.top_k = top_k

    def retrieve(self, query: str, top_k: Optional[int] = None) -> List[Dict]:
        """Retrieve relevant documents for a query."""
        if top_k is None:
            top_k = self.top_k

        # Stage 1: Embed query
        query_embedding = self.embedding_engine.embed_query(query)

        # Stage 2: Vector search
        results = self.vector_store.search(query_embedding, top_k=top_k * 2)

        # Stage 3: Rerank (optional - simple relevance threshold for now)
        ranked_results = [
            {
                "document": doc,
                "similarity": sim,
                "metadata": meta,
            }
            for doc, sim, meta in results
            if sim > 0.1  # Simple threshold
        ]

        # Return top K after filtering
        return ranked_results[:top_k]

    def retrieve_with_expansion(
        self, query: str, expansion_count: int = 3, top_k: Optional[int] = None
    ) -> List[Dict]:
        """Retrieve with query expansion for better coverage."""
        if top_k is None:
            top_k = self.top_k

        # Generate query variations (simple approach)
        queries = [query]
        if expansion_count > 0:
            # Add keyword-based variations
            keywords = query.split()[:2]
            if keywords:
                queries.append(" ".join(keywords))

        # Retrieve for each query variant
        all_results = {}
        for q in queries:
            results = self.retrieve(q, top_k=top_k)
            for r in results:
                doc = r["document"]
                if doc not in all_results:
                    all_results[doc] = r
                else:
                    # Update similarity if higher
                    all_results[doc]["similarity"] = max(
                        all_results[doc]["similarity"], r["similarity"]
                    )

        # Return sorted by similarity
        sorted_results = sorted(
            all_results.values(), key=lambda x: x["similarity"], reverse=True
        )
        return sorted_results[:top_k]

    def retrieve_with_metadata_filter(
        self,
        query: str,
        metadata_filter: Dict,
        top_k: Optional[int] = None,
    ) -> List[Dict]:
        """Retrieve documents matching metadata criteria."""
        if top_k is None:
            top_k = self.top_k

        # Get all results
        all_results = self.vector_store.search(
            self.embedding_engine.embed_query(query), top_k=len(self.vector_store.documents)
        )

        # Filter by metadata
        filtered = []
        for doc, sim, meta in all_results:
            if self._matches_filter(meta, metadata_filter):
                filtered.append(
                    {"document": doc, "similarity": sim, "metadata": meta}
                )

        return filtered[:top_k]

    @staticmethod
    def _matches_filter(metadata: Dict, filter_criteria: Dict) -> bool:
        """Check if metadata matches filter criteria."""
        for key, value in filter_criteria.items():
            if key not in metadata:
                return False
            if metadata[key] != value:
                return False
        return True


class HybridRetriever:
    """Hybrid retrieval combining semantic and keyword search."""

    def __init__(
        self,
        semantic_retriever: Retriever,
        keyword_retriever: "KeywordRetriever",
        semantic_weight: float = 0.7,
    ):
        self.semantic_retriever = semantic_retriever
        self.keyword_retriever = keyword_retriever
        self.semantic_weight = semantic_weight
        self.keyword_weight = 1.0 - semantic_weight

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve using both semantic and keyword search."""
        semantic_results = self.semantic_retriever.retrieve(query, top_k=top_k)
        keyword_results = self.keyword_retriever.retrieve(query, top_k=top_k)

        # Combine and deduplicate
        combined = {}
        for r in semantic_results:
            doc = r["document"]
            combined[doc] = {
                **r,
                "final_score": r["similarity"] * self.semantic_weight,
            }

        for r in keyword_results:
            doc = r["document"]
            if doc in combined:
                combined[doc]["final_score"] += r["similarity"] * self.keyword_weight
            else:
                combined[doc] = {
                    **r,
                    "final_score": r["similarity"] * self.keyword_weight,
                }

        # Sort by final score
        ranked = sorted(combined.values(), key=lambda x: x["final_score"], reverse=True)
        return ranked[:top_k]


class KeywordRetriever:
    """Simple keyword-based retriever."""

    def __init__(self, documents: List[str], top_k: int = 5):
        self.documents = documents
        self.top_k = top_k

    def retrieve(self, query: str, top_k: Optional[int] = None) -> List[Dict]:
        """Retrieve using keyword matching."""
        if top_k is None:
            top_k = self.top_k

        keywords = set(query.lower().split())
        results = []

        for i, doc in enumerate(self.documents):
            doc_keywords = set(doc.lower().split())
            overlap = len(keywords & doc_keywords)
            if overlap > 0:
                similarity = overlap / len(keywords)
                results.append(
                    {
                        "document": doc,
                        "similarity": similarity,
                        "metadata": {"doc_id": i},
                    }
                )

        sorted_results = sorted(
            results, key=lambda x: x["similarity"], reverse=True
        )
        return sorted_results[:top_k]
