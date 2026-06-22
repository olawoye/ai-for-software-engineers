"""
OpenRouter API client for consistent LLM access across lessons.
Supports model swapping (OpenRouter, Anthropic, OpenAI).
"""
import os
from openai import OpenAI

def get_client(provider="openrouter"):
    """
    Initialize LLM client based on provider.

    Args:
        provider: "openrouter", "anthropic", or "openai"

    Returns:
        Configured OpenAI-compatible client
    """
    if provider == "openrouter":
        return OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
        )
    elif provider == "anthropic":
        return OpenAI(
            base_url="https://api.anthropic.com/v1",
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
    elif provider == "openai":
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    else:
        raise ValueError(f"Unknown provider: {provider}")

def call_llm(client, model, messages, temperature=0.7, max_tokens=500):
    """
    Make LLM API call with consistent interface.

    Args:
        client: OpenAI client instance
        model: Model name (e.g., "gpt-3.5-turbo" or "mistralai/mistral-7b-instruct")
        messages: List of message dicts
        temperature: Sampling temperature
        max_tokens: Max completion tokens

    Returns:
        Dict with 'content', 'usage', 'model'
    """
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )

    return {
        "content": response.choices[0].message.content,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        },
        "model": response.model
    }
