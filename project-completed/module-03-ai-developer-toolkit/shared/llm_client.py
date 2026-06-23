"""
Unified LLM client wrapper supporting multiple providers via OpenRouter.
Provides simple, extensible interface for API calls with consistent error handling.
"""

import os
import httpx
from typing import Optional, Dict, Any, List


class LLMClient:
    """Wrapper around OpenRouter API for unified provider access."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model = model
        self.base_url = "https://openrouter.io/api/v1"

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")

    def complete(self, prompt: str, **kwargs) -> str:
        """Send completion request and return text response."""
        response = self.call(messages=[{"role": "user", "content": prompt}], **kwargs)
        return response["choices"][0]["message"]["content"]

    def call(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Make API call to OpenRouter."""
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }

        if max_tokens:
            payload["max_tokens"] = max_tokens

        payload.update(kwargs)

        with httpx.Client() as client:
            response = client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
            )
            response.raise_for_status()
            return response.json()
