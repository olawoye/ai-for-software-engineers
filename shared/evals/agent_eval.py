"""Agent behavior evaluation helpers."""

from .base_eval import BaseEval


class AgentEval(BaseEval):
    def evaluate(self, results: dict) -> dict[str, float]:
        return {
            "actions": float(len(results.get("actions", []))),
            "confidence": float(results.get("confidence", 0.0)),
        }
