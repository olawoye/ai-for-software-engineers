"""
AI For Software Engineers — Module 4: RAG Systems & Vector Databases
Resource: Production Hybrid RAG & Re-Ranking Engine
File: projects-completed/module-04/resource_rag_pipeline.py
"""

import math
from typing import List, Dict, Any, Tuple
from openai import OpenAI


class RecursiveChunker:
    """
    Recursively splits raw text documents into chunks using paragraph and sentence bounds
    to preserve semantic continuity without breaking mid-thought.
    """

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = ["\n\n", "\n", ". ", " "]

    def split_text(self, text: str) -> List[str]:
        """Splits document text using recursive boundary rules."""
        if len(text) <= self.chunk_size:
            return [text.strip()] if text.strip() else []

        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            if end < len(text):
                # Look for best separator boundary before hard cut
                boundary = -1
                for sep in self.separators:
                    pos = text.rfind(sep, start, end)
                    if pos != -1 and pos > start:
                        boundary = pos + len(sep)
                        break
                if boundary != -1:
                    end = boundary

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            # Apply chunk overlap step size
            step = max(1, self.chunk_size - self.chunk_overlap)
            start += step

        return chunks


class HybridRAGEngine:
    """
    Production-grade Hybrid RAG engine combining Dense Embeddings with
    Lexical (BM25-style) Search and Reciprocal Rank Fusion (RRF) re-ranking.
    """

    def __init__(self, embedding_model: str = "text-embedding-3-small"):
        self.embedding_model = embedding_model
        self.client = OpenAI()
        self.vector_store: List[Dict[str, Any]] = []

    def get_embedding(self, text: str) -> List[float]:
        """Generates dense embedding vector via OpenAI API."""
        response = self.client.embeddings.create(
            input=text,
            model=self.embedding_model
        )
        return response.data[0].embedding

    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float]) -> float:
        """Computes dot-product similarity over normalized vectors."""
        dot = sum(a * b for a, b in zip(v1, v2))
        norm_a = math.sqrt(sum(a * a for a in v1))
        norm_b = math.sqrt(sum(b * b for b in v2))
        return dot / (norm_a * norm_b + 1e-9)

    def ingest_document(self, text: str, doc_id: str = "doc_1"):
        """Chunk document, embed, and store in mock vector memory."""
        chunker = RecursiveChunker(chunk_size=300, chunk_overlap=30)
        chunks = chunker.split_text(text)

        for idx, chunk_text in enumerate(chunks):
            embedding = self.get_embedding(chunk_text)
            self.vector_store.append({
                "id": f"{doc_id}_chunk_{idx}",
                "text": chunk_text,
                "embedding": embedding,
                "tokens": chunk_text.lower().split()
            })
        print(f"[Ingestion Complete] Ingested {len(chunks)} chunks into Vector Memory.")

    def dense_search(self, query: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """Dense Vector Similarity Search."""
        query_vec = self.get_embedding(query)
        scored_chunks = []
        for chunk in self.vector_store:
            sim = self.cosine_similarity(query_vec, chunk["embedding"])
            scored_chunks.append((chunk, sim))

        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        return scored_chunks[:top_k]

    def lexical_search(self, query: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """Sparse Lexical BM25-style keyword search."""
        query_terms = set(query.lower().split())
        scored_chunks = []

        for chunk in self.vector_store:
            matches = sum(1 for term in query_terms if term in chunk["tokens"])
            score = matches / (len(chunk["tokens"]) + 1e-5)
            scored_chunks.append((chunk, score))

        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        return scored_chunks[:top_k]

    def reciprocal_rank_fusion(
        self,
        dense_results: List[Tuple[Dict[str, Any], float]],
        lexical_results: List[Tuple[Dict[str, Any], float]],
        k: int = 60,
        top_n: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Merges and re-ranks dense and sparse results using RRF logic:
        RRF_Score = SUM( 1 / (k + rank_i) )
        """
        rrf_scores: Dict[str, float] = {}
        chunk_map: Dict[str, Dict[str, Any]] = {}

        for rank, (chunk, _) in enumerate(dense_results, start=1):
            c_id = chunk["id"]
            chunk_map[c_id] = chunk
            rrf_scores[c_id] = rrf_scores.get(c_id, 0.0) + (1.0 / (k + rank))

        for rank, (chunk, _) in enumerate(lexical_results, start=1):
            c_id = chunk["id"]
            chunk_map[c_id] = chunk
            rrf_scores[c_id] = rrf_scores.get(c_id, 0.0) + (1.0 / (k + rank))

        sorted_chunk_ids = sorted(rrf_scores.keys(), key=lambda c_id: rrf_scores[c_id], reverse=True)
        return [chunk_map[c_id] for c_id in sorted_chunk_ids[:top_n]]


if __name__ == "__main__":
    raw_document = """
    RAG (Retrieval-Augmented Generation) optimizes the output of a large language model 
    by referencing an authoritative knowledge base outside its training data before generating a response. 
    Vector databases like Qdrant and Pinecone index embeddings using HNSW graph algorithms for fast similarity retrieval.
    
    Hybrid search combines dense vector similarity search with sparse lexical search (BM25) to solve precision issues. 
    Reciprocal Rank Fusion (RRF) merges the rank order of both dense and sparse retrieval streams into a unified context window.
    """

    print("--- Running Hybrid RAG & Re-Ranking Pipeline ---")
    try:
        rag_engine = HybridRAGEngine()
        rag_engine.ingest_document(raw_document, doc_id="module_04_rag")

        user_query = "How does hybrid search combine dense and sparse vectors?"
        dense_hits = rag_engine.dense_search(user_query, top_k=3)
        lexical_hits = rag_engine.lexical_search(user_query, top_k=3)

        top_chunks = rag_engine.reciprocal_rank_fusion(dense_hits, lexical_hits, top_n=2)

        print(f"\nQuery: '{user_query}'")
        print("\n--- Re-Ranked Context Assembly (Top-2 Chunks) ---")
        for i, chunk in enumerate(top_chunks, 1):
            print(f"[{i}] Chunk ID: {chunk['id']}")
            print(f"    Text    : {chunk['text']}\n")

    except Exception as e:
        print(f"Execution skipped (API Key missing or invalid): {e}")