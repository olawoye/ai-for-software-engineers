"""
Embedding generation and management for RAG systems.
Supports Cohere embeddings (primary, free tier) with TF-IDF fallback.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer


class EmbeddingEngine:
    """Unified interface for generating embeddings."""

    def __init__(self, method: str = "cohere", cohere_api_key: Optional[str] = None):
        self.method = method
        self.cohere_api_key = cohere_api_key
        self.tfidf_vectorizer = None

    def embed_documents(self, documents: List[str]) -> np.ndarray:
        """Generate embeddings for multiple documents."""
        if self.method == "cohere" and self.cohere_api_key:
            return self._embed_cohere(documents)
        else:
            return self._embed_tfidf(documents)

    def embed_query(self, query: str) -> np.ndarray:
        """Generate embedding for a single query."""
        if self.method == "cohere" and self.cohere_api_key:
            return self._embed_cohere([query])[0]
        else:
            return self._embed_tfidf([query])[0]

    def _embed_cohere(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings using Cohere API."""
        try:
            import cohere

            client = cohere.ClientV2(api_key=self.cohere_api_key)
            response = client.embed(
                model="embed-english-v3.0",
                input_type="search_document",
                texts=texts,
            )

            # Extract embeddings
            embeddings = []
            for item in response.embeddings:
                if hasattr(item, 'float'):
                    embeddings.append(item.float)
                else:
                    embeddings.append(item)

            return np.array(embeddings)
        except Exception as e:
            print(f"Cohere embedding failed: {e}. Falling back to TF-IDF.")
            return self._embed_tfidf(texts)

    def _embed_tfidf(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings using TF-IDF (keyword-based fallback)."""
        if self.tfidf_vectorizer is None:
            self.tfidf_vectorizer = TfidfVectorizer(max_features=300)
            self.tfidf_vectorizer.fit(texts)

        return self.tfidf_vectorizer.transform(texts).toarray().astype(np.float32)


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Calculate cosine similarity between two vectors."""
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(np.dot(vec1, vec2) / (norm1 * norm2))


def batch_similarity(query_vec: np.ndarray, doc_vecs: np.ndarray) -> np.ndarray:
    """Calculate similarity between query and multiple documents."""
    query_norm = np.linalg.norm(query_vec)
    if query_norm == 0:
        return np.zeros(len(doc_vecs))

    doc_norms = np.linalg.norm(doc_vecs, axis=1, keepdims=True)
    doc_norms[doc_norms == 0] = 1  # Avoid division by zero

    normalized_docs = doc_vecs / doc_norms
    similarities = np.dot(normalized_docs, query_vec) / query_norm

    return similarities
