"""
Token utilities for counting, estimating costs, and managing context windows.
"""
import re
from typing import Dict, List

# Approximate tokens per word (varies by model)
TOKENS_PER_WORD = 0.75

# Model context window limits (in tokens)
CONTEXT_WINDOWS = {
    "gpt-3.5-turbo": 4096,
    "gpt-4": 8192,
    "claude-3-sonnet": 200000,
    "claude-3-opus": 200000,
}

# Approximate pricing per 1M tokens (OpenRouter, may vary)
PRICING = {
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    "gpt-4": {"input": 30.0, "output": 60.0},
    "claude-3-sonnet": {"input": 3.0, "output": 15.0},
    "claude-3-opus": {"input": 15.0, "output": 75.0},
}

def estimate_tokens(text: str) -> int:
    """Estimate token count from text (rough approximation)."""
    words = len(text.split())
    return int(words * TOKENS_PER_WORD)

def count_message_tokens(messages: List[Dict]) -> int:
    """Count approximate tokens in message list."""
    total = 0
    for msg in messages:
        total += estimate_tokens(msg.get("content", ""))
    return total

def get_context_window(model: str) -> int:
    """Get context window size for model."""
    return CONTEXT_WINDOWS.get(model, 4096)

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
