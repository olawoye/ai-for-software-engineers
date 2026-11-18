"""
Token utilities for counting, estimating costs, and managing context windows.
"""
import math
import re
from typing import Dict, List

# Approximate tokens per word (varies by model and text type).
# A safer general planning heuristic is ~1.33 tokens/word.
TOKENS_PER_WORD = 1.33

# Model context window limits (in tokens)
AVAILABLE_MODELS = [
    "openai/gpt-4o",
    "openai/gpt-4o-mini",
    "anthropic/claude-sonnet-4.5",
    "openai/gpt-3.5-turbo-0613",
]

CONTEXT_WINDOWS = {
    "openai/gpt-4o": 128000,
    "openai/gpt-4o-mini": 128000,
    "anthropic/claude-sonnet-4.5": 1000000,
    "openai/gpt-3.5-turbo-0613": 4095,
}

# Approximate max output tokens per response (in tokens).
OUTPUT_WINDOWS = {
    "openai/gpt-4o": 16384,
    "openai/gpt-4o-mini": 16384,
    "anthropic/claude-sonnet-4.5": 64000,
    "openai/gpt-3.5-turbo-0613": 3685,
}

# Approximate pricing per 1M tokens (OpenRouter, may vary)
PRICING = {
    "openai/gpt-4o": {"input": 2.50, "output": 10.00},
    "openai/gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "anthropic/claude-sonnet-4.5": {"input": 3.00, "output": 15.00},
    "openai/gpt-3.5-turbo-0613": {"input": 1.00, "output": 2.00},
}

def estimate_tokens(text: str) -> int:
    """Estimate token count from text (rough approximation)."""
    words = len(text.split())
    # Round up to avoid systematically underestimating token budget.
    return math.ceil(words * TOKENS_PER_WORD)

def count_message_tokens(messages: List[Dict]) -> int:
    """Count approximate tokens in message list."""
    total = 0
    for msg in messages:
        total += estimate_tokens(msg.get("content", ""))
    return total

def get_context_window(model: str) -> int:
    """Get context window size for model."""
    return CONTEXT_WINDOWS.get(model, 4096)

def get_output_window(model: str) -> int:
    """Get max output tokens per response for model."""
    return OUTPUT_WINDOWS.get(model, 4096)

def calculate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> Dict:
    """
    Calculate API call cost.

    Returns:
        Dict with 'input_cost', 'output_cost', 'total_cost' (in USD)
    """
    pricing = PRICING.get(model, {"input": 0.0, "output": 0.0})

    input_cost = (prompt_tokens / 1_000_000) * pricing["input"]
    output_cost = (completion_tokens / 1_000_000) * pricing["output"]

    return {
        "input_cost": round(input_cost, 6),
        "output_cost": round(output_cost, 6),
        "total_cost": round(input_cost + output_cost, 6)
    }

def check_context_fit(model: str, prompt_tokens: int, estimated_completion: int = 500) -> Dict:
    """
    Check if prompt fits within model context window.

    Returns:
        Dict with 'fits', 'window_size', 'used', 'remaining', 'warning'
    """
    window = get_context_window(model)
    total_needed = prompt_tokens + estimated_completion

    return {
        "fits": total_needed <= window,
        "window_size": window,
        "used": prompt_tokens,
        "estimated_total": total_needed,
        "remaining": window - prompt_tokens,
        "warning": f"Prompt uses {(prompt_tokens/window)*100:.1f}% of context" if prompt_tokens > window * 0.8 else None
    }
