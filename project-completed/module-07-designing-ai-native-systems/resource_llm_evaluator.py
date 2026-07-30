"""
AI For Software Engineers — Module 7: Evaluations, LLMOps & Production Observability
Resource: Asynchronous LLM-as-a-Judge & Heuristic Evaluation Pipeline
File: projects-completed/module-07/resource_llm_evaluator.py
"""

import json
import time
from typing import Dict, Any, List


class HeuristicEvaluator:
    """Fast, zero-cost deterministic checks for output validation."""

    @staticmethod
    def check_json_schema(response_text: str) -> bool:
        """Verifies if output is valid JSON."""
        try:
            json.loads(response_text)
            return True
        except ValueError:
            return False

    @staticmethod
    def check_latency_sla(elapsed_ms: float, max_allowed_ms: float = 1500.0) -> bool:
        """Checks if response latency satisfies SLA limits."""
        return elapsed_ms <= max_allowed_ms


class LLMAsAJudgeEvaluator:
    """
    Evaluates response quality using LLM-as-a-Judge pattern for
    Faithfulness (Groundedness) and Answer Relevance.
    """

    def __init__(self, target_threshold: float = 0.85):
        self.target_threshold = target_threshold

    def evaluate_faithfulness(self, context: str, response: str) -> Dict[str, Any]:
        """
        Simulates evaluating whether claims in the response are supported
        by the retrieved context (Faithfulness Score).
        """
        # Mock evaluation logic for demonstration
        context_words = set(context.lower().split())
        response_words = set(response.lower().split())

        overlap = response_words.intersection(context_words)
        score = len(overlap) / (len(response_words) + 1e-5)
        
        # Scale score to 0.0 - 1.0 range
        faithfulness_score = round(min(1.0, score * 1.5), 2)
        passed = faithfulness_score >= self.target_threshold

        return {
            "metric": "faithfulness",
            "score": faithfulness_score,
            "passed": passed,
            "reason": "Claims grounded in retrieved context." if passed else "Potential hallucination detected."
        }


class ObservabilityPipeline:
    """Aggregates telemetry, run logs, and evaluation metrics for observability."""

    def __init__(self):
        self.telemetry_store: List[Dict[str, Any]] = []

    def log_run(self, trace_id: str, prompt: str, context: str, response: str, latency_ms: float):
        """Logs an inference trace and executes async evaluations."""
        # 1. Deterministic Checks
        is_json = HeuristicEvaluator.check_json_schema(response)
        within_sla = HeuristicEvaluator.check_latency_sla(latency_ms)

        # 2. LLM-as-a-Judge Check
        judge = LLMAsAJudgeEvaluator()
        faith_eval = judge.evaluate_faithfulness(context, response)

        record = {
            "trace_id": trace_id,
            "timestamp": time.time(),
            "latency_ms": latency_ms,
            "valid_json": is_json,
            "within_sla": within_sla,
            "faithfulness_score": faith_eval["score"],
            "eval_passed": faith_eval["passed"],
            "eval_reason": faith_eval["reason"]
        }

        self.telemetry_store.append(record)
        return record


if __name__ == "__main__":
    print("--- Running Module 7 LLMOps & Evaluation Engine ---")
    pipeline = ObservabilityPipeline()

    sample_context = "The Model Context Protocol (MCP) uses JSON-RPC 2.0 over stdio or SSE transports."
    sample_response = "MCP relies on JSON-RPC 2.0 over stdio transport for local process communication."
    
    start_time = time.time()
    # Simulate processing delay
    time.sleep(0.05)
    latency = (time.time() - start_time) * 1000

    result = pipeline.log_run(
        trace_id="tr_99021a",
        prompt="Explain MCP transport protocol.",
        context=sample_context,
        response=sample_response,
        latency_ms=latency
    )

    print("\n[Evaluation & Telemetry Trace]")
    print(json.dumps(result, indent=2))