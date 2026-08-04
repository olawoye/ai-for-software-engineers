"""
Embedding generation and management for RAG systems.
Supports OpenRouter embeddings via Jina, Cohere, and TF-IDF fallback.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
import os
import json
import requests


class EmbeddingEngine:
    """Unified interface for generating embeddings.
    
    Supports:
    - Cohere embeddings (primary, reliable)
    - OpenRouter via Jina Embeddings v3 (fallback, requires OpenRouter API key)
    """

    def __init__(
        self,
        method: str = "openrouter",
        openrouter_key: Optional[str] = None,
        openrouter_url: str = "https://openrouter.ai/api/v1",
        cohere_api_key: Optional[str] = None,
    ):
        """Initialize embedding engine.
        
        Args:
            method: "openrouter", "cohere", or "tfidf"
            openrouter_key: OpenRouter API key (uses env var if not provided)
            openrouter_url: OpenRouter base URL
            cohere_api_key: Cohere API key for fallback
        """
        self.method = method
        self.actual_method = method  # Track actual method after fallback
        self.openrouter_key = openrouter_key or os.getenv("OPENROUTER_API_KEY")
        self.openrouter_url = openrouter_url
        self.cohere_api_key = cohere_api_key or os.getenv("COHERE_API_KEY")

    def embed_documents(self, documents: List[str]) -> np.ndarray:
        """Generate embeddings for documents using Cohere.
        
        Raises RuntimeError if Cohere is not available or fails.
        """
        if not self.cohere_api_key:
            raise RuntimeError(
                "Cohere API key required. Set COHERE_API_KEY environment variable. "
                "Get a free key at https://cohere.com (100k requests/month free)"
            )
        
        return self._embed_cohere(documents, input_type="search_document")

    def embed_query(self, query: str) -> np.ndarray:
        """Generate embedding for a single query using Cohere."""
        return self._embed_cohere([query], input_type="search_query")[0]

    def _embed_cohere(self, texts: List[str], input_type: str = "search_document") -> np.ndarray:
        """Generate embeddings using Cohere API.
        
        Args:
            texts: List of texts to embed
            input_type: "search_document" for documents, "search_query" for queries
        
        Raises RuntimeError if API call fails.
        """
        try:
            import cohere
            client = cohere.ClientV2(api_key=self.cohere_api_key)
            
            response = client.embed(
                texts=texts,
                model="embed-english-v3.0",
                input_type=input_type
            )
            
            # Extract embeddings from response (handles multiple Cohere versions)
            embeddings_list = []
            
            if hasattr(response, 'embeddings'):
                emb_data = response.embeddings
                
                # Method 1: Try .float attribute (Cohere v2+)
                if hasattr(emb_data, 'float'):
                    embeddings_list = emb_data.float
                # Method 2: Try direct iteration on embeddings object
                elif hasattr(emb_data, '__iter__'):
                    for item in emb_data:
                        if hasattr(item, 'float'):
                            embeddings_list.append(item.float)
                        elif hasattr(item, 'embedding'):
                            embeddings_list.append(item.embedding)
                        else:
                            embeddings_list.append(list(item) if hasattr(item, '__iter__') else item)
            
            if not embeddings_list:
                raise ValueError("Could not extract embeddings from Cohere response")
            
            embeddings = np.array(embeddings_list, dtype=np.float32)
            
            # Validate embeddings
            if embeddings.ndim != 2:
                raise ValueError(f"Expected 2D array, got {embeddings.ndim}D with shape {embeddings.shape}")
            if embeddings.shape[1] < 10:
                raise ValueError(
                    f"Embeddings too small: shape {embeddings.shape}. "
                    f"Expected 100+ dimensions, got {embeddings.shape[1]}."
                )
            
            self.actual_method = "cohere"
            return embeddings
            
        except Exception as e:
            raise RuntimeError(f"Cohere embedding failed: {e}")


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
