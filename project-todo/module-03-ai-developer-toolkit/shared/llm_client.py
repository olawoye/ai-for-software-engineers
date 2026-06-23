"""
Shared LLM client wrapper — TODO scaffold

Students will implement a unified client supporting multiple providers.

PHASE 1: Basic structure
- Create LLMClient class
- Implement __init__ with API key validation

PHASE 2: Complete method
- Implement complete() for simple text completions

PHASE 3: Advanced methods
- Implement call() for chat-based responses
- Add error handling
- Support temperature and max_tokens parameters
"""

import os
from typing import Optional, Dict, Any, List


class LLMClient:
    """Wrapper around LLM API for unified provider access."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        # PHASE 1: Initialize with API key validation
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model = model
        self.base_url = "https://openrouter.io/api/v1"

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")

    def complete(self, prompt: str, **kwargs) -> str:
        """
        PHASE 2: Send completion request and return text response.

        Args:
            prompt: Input prompt text
            **kwargs: Additional parameters (temperature, max_tokens, etc.)

        Returns:
            Response text
        """
        # TODO: Implement using call() method
        pass

    def call(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        PHASE 3: Make API call to OpenRouter.

        Args:
            messages: List of {"role": "user"|"assistant", "content": "..."} dicts
            temperature: Response randomness (0.0 = precise, 1.0 = creative)
            max_tokens: Maximum response length
            **kwargs: Additional API parameters

        Returns:
            Full API response dictionary
        """
        # TODO: Build request payload
        # TODO: Make HTTP POST request to OpenRouter
        # TODO: Return response JSON
        pass
