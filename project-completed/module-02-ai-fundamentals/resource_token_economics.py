"""
AI For Software Engineers — Module 2: AI Fundamentals
Resource: Token Economics & Context Window Toolkit
File: resource_token_economics.py
"""

from typing import Tuple, Dict, Any, List
import tiktoken


def budget_and_truncate_context(
    prompt: str, 
    max_token_budget: int = 2048, 
    model: str = "gpt-4o"
) -> Tuple[str, int]:
    """
    Ensures a prompt strictly adheres to token limits before API dispatch.
    Returns the (potentially truncated) prompt and its token count.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    
    tokens = encoding.encode(prompt)
    token_count = len(tokens)
    
    if token_count <= max_token_budget:
        return prompt, token_count
        
    # Truncate tokens to prevent context overflow
    truncated_tokens = tokens[:max_token_budget]
    truncated_prompt = encoding.decode(truncated_tokens)
    
    return truncated_prompt, len(truncated_tokens)


def calculate_request_cost(
    input_tokens: int,
    output_tokens: int,
    cached_tokens: int = 0,
    model: str = "gpt-4o"
) -> Dict[str, float]:
    """
    Computes total cost per API call factoring in prompt caching discounts.
    """
    # Pricing per 1M tokens (as of current benchmarks)
    pricing_catalog = {
        "gpt-4o": {"input": 2.50, "output": 10.00, "cache": 1.25},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60, "cache": 0.075},
        "claude-3-5-sonnet": {"input": 3.00, "output": 15.00, "cache": 0.30},
    }
    
    rates = pricing_catalog.get(model, pricing_catalog["gpt-4o"])
    
    uncached_inputs = max(0, input_tokens - cached_tokens)
    
    input_cost = (uncached_inputs / 1_000_000) * rates["input"]
    cache_cost = (cached_tokens / 1_000_000) * rates["cache"]
    output_cost = (output_tokens / 1_000_000) * rates["output"]
    
    total_cost = input_cost + cache_cost + output_cost
    
    return {
        "input_cost": round(input_cost, 6),
        "cache_cost": round(cache_cost, 6),
        "output_cost": round(output_cost, 6),
        "total_cost": round(total_cost, 6),
    }


def chunk_prompt_by_tokens(
    text: str, 
    chunk_size: int = 512, 
    overlap: int = 50, 
    model: str = "gpt-4o"
) -> List[str]:
    """
    Splits long text documents into overlapping token-aware chunks.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
        
    tokens = encoding.encode(text)
    chunks = []
    
    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunks.append(encoding.decode(chunk_tokens))
        start += chunk_size - overlap
        
    return chunks


if __name__ == "__main__":
    sample_text = "Building reliable LLM pipelines requires strict token management. " * 100
    
    # 1. Truncation check
    safe_prompt, count = budget_and_truncate_context(sample_text, max_token_budget=200)
    print(f"[Truncation] Token Count: {count}")
    
    # 2. Cost estimation
    cost_data = calculate_request_cost(input_tokens=5000, output_tokens=500, cached_tokens=3000, model="gpt-4o")
    print(f"[Cost Calculation] {cost_data}")
    
    # 3. Chunking
    chunks = chunk_prompt_by_tokens(sample_text, chunk_size=100, overlap=10)
    print(f"[Chunking] Generated {len(chunks)} chunks.")