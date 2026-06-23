"""
Complete RAG pipeline combining all components.
Handles ingestion, retrieval, augmentation, and generation.
"""

from typing import List, Dict, Optional
from .embeddings import EmbeddingEngine
from .vector_store import VectorStore
from .retriever import Retriever
from .prompts import format_context


class RAGPipeline:
    """End-to-end RAG system."""

    def __init__(
        self,
        embedding_engine: EmbeddingEngine,
        vector_store: VectorStore,
        retriever: Retriever,
        llm_client=None,
    ):
        self.embedding_engine = embedding_engine
        self.vector_store = vector_store
        self.retriever = retriever
        self.llm_client = llm_client

    def ingest_documents(self, documents: List[str], metadata: Optional[List[Dict]] = None) -> None:
        """Ingest documents into the pipeline."""
        # Embed documents
        embeddings = self.embedding_engine.embed_documents(documents)

        # Add to vector store
        self.vector_store.add(documents, embeddings, metadata)

    def query(self, question: str, top_k: int = 5) -> Dict:
        """Execute full RAG pipeline."""
        # Stage 1: Retrieve
        retrieved = self.retriever.retrieve(question, top_k=top_k)

        # Stage 2: Augment (format context)
        retrieved_docs = [r["document"] for r in retrieved]
        context_prompt = format_context(retrieved_docs, question)

        # Stage 3: Generate (if LLM client available)
        answer = None
        if self.llm_client:
            try:
                answer = self.llm_client.complete(context_prompt)
            except Exception as e:
                answer = f"Error generating answer: {e}"

        return {
            "question": question,
            "retrieved_documents": retrieved,
            "answer": answer,
            "context_used": context_prompt,
        }

    def get_stats(self) -> Dict:
        """Get pipeline statistics."""
        return {
            "vector_store": self.vector_store.get_stats(),
            "embedding_method": self.embedding_engine.method,
            "retriever_top_k": self.retriever.top_k,
        }


class RAGEvaluator:
    """Evaluate RAG system performance."""

    @staticmethod
    def evaluate_retrieval(
        retrieved_docs: List[Dict],
        ground_truth_docs: List[str],
        top_k: int = 5,
    ) -> Dict:
        """Evaluate retrieval quality."""
        retrieved_texts = [r["document"] for r in retrieved_docs[:top_k]]

        # Calculate precision and recall
        matches = sum(1 for doc in retrieved_texts if doc in ground_truth_docs)

        precision = matches / len(retrieved_texts) if retrieved_texts else 0
        recall = matches / len(ground_truth_docs) if ground_truth_docs else 0

        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        return {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "matches": matches,
        }

    @staticmethod
    def evaluate_answer_groundedness(
        answer: str,
        retrieved_docs: List[str],
    ) -> Dict:
        """Check if answer is grounded in retrieved documents."""
        # Simple check: count how many nouns from answer appear in documents
        answer_words = set(answer.lower().split())
        doc_words = set(" ".join(retrieved_docs).lower().split())

        grounded_words = answer_words & doc_words
        grounding_score = len(grounded_words) / len(answer_words) if answer_words else 0

        return {
            "grounding_score": grounding_score,
            "grounded_words": len(grounded_words),
            "total_words": len(answer_words),
        }
