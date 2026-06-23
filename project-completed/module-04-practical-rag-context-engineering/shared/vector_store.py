"""
Vector store for managing embeddings and semantic search.
Lightweight in-memory implementation using FAISS for fast similarity search.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
import json


class VectorStore:
    """In-memory vector store with FAISS support."""

    def __init__(self, embedding_dim: int = 300, use_faiss: bool = False):
        self.embedding_dim = embedding_dim
        self.embeddings = []
        self.documents = []
        self.metadata = []
        self.use_faiss = use_faiss
        self.faiss_index = None

        if use_faiss:
            try:
                import faiss
                self.faiss_index = faiss.IndexFlatL2(embedding_dim)
            except ImportError:
                print("FAISS not installed. Using numpy for similarity search.")
                self.use_faiss = False

    def add(
        self,
        documents: List[str],
        embeddings: np.ndarray,
        metadata: Optional[List[Dict]] = None,
    ) -> None:
        """Add documents and embeddings to the store."""
        if len(embeddings) != len(documents):
            raise ValueError("Number of embeddings must match number of documents")

        self.documents.extend(documents)
        self.embeddings.extend(embeddings)

        if metadata is None:
            metadata = [{"doc_id": i} for i in range(len(documents))]
        self.metadata.extend(metadata)

        # Update FAISS index if enabled
        if self.use_faiss and self.faiss_index is not None:
            self.faiss_index.add(embeddings.astype(np.float32))

    def search(
        self, query_embedding: np.ndarray, top_k: int = 5
    ) -> List[Tuple[str, float, Dict]]:
        """Search for similar documents."""
        if len(self.embeddings) == 0:
            return []

        embeddings_array = np.array(self.embeddings).astype(np.float32)

        if self.use_faiss and self.faiss_index is not None:
            distances, indices = self.faiss_index.search(
                query_embedding.reshape(1, -1).astype(np.float32), top_k
            )
            results = []
            for i, idx in enumerate(indices[0]):
                if idx == -1:
                    break
                results.append(
                    (
                        self.documents[idx],
                        float(1 / (1 + distances[0][i])),  # Convert distance to similarity
                        self.metadata[idx],
                    )
                )
            return results
        else:
            # Numpy-based search
            from .embeddings import batch_similarity

            similarities = batch_similarity(query_embedding, embeddings_array)
            top_indices = np.argsort(similarities)[::-1][:top_k]

            results = []
            for idx in top_indices:
                if similarities[idx] > 0:
                    results.append(
                        (self.documents[idx], float(similarities[idx]), self.metadata[idx])
                    )

            return results

    def clear(self) -> None:
        """Clear all stored data."""
        self.embeddings = []
        self.documents = []
        self.metadata = []
        if self.use_faiss and self.faiss_index is not None:
            import faiss
            self.faiss_index = faiss.IndexFlatL2(self.embedding_dim)

    def save(self, filepath: str) -> None:
        """Save vector store to disk."""
        data = {
            "documents": self.documents,
            "embeddings": [e.tolist() if isinstance(e, np.ndarray) else e for e in self.embeddings],
            "metadata": self.metadata,
        }
        with open(filepath, "w") as f:
            json.dump(data, f)

    def load(self, filepath: str) -> None:
        """Load vector store from disk."""
        with open(filepath, "r") as f:
            data = json.load(f)

        self.documents = data["documents"]
        self.embeddings = [np.array(e) for e in data["embeddings"]]
        self.metadata = data["metadata"]

        if self.use_faiss and self.faiss_index is not None:
            embeddings_array = np.array(self.embeddings).astype(np.float32)
            self.faiss_index.add(embeddings_array)

    def get_stats(self) -> Dict:
        """Get store statistics."""
        return {
            "total_documents": len(self.documents),
            "embedding_dim": self.embedding_dim,
            "using_faiss": self.use_faiss,
        }
