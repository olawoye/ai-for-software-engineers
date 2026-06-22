"""RAG-specific evaluation helpers."""

from .base_eval import BaseEval


class RAGEval(BaseEval):
    def evaluate(self, results: dict) -> dict[str, float]:
        return {
            "recall": results.get("retrieved", 0) / max(results.get("total", 1), 1),
            "precision": results.get("relevant", 0) / max(results.get("retrieved", 1), 1),
        }
