"""
AI For Software Engineers — Module 3: LLM Integration & API Engineering
Resource: Production LLM Gateway & Resiliency Toolkit
File: projects-completed/module-03/resource_llm_gateway.py
"""

import asyncio
import random
import time
from typing import AsyncGenerator, Dict, Any, List, Optional
from openai import AsyncOpenAI, APIError, RateLimitError, APIConnectionError


class ResilientLLMGateway:
    """
    Production-ready LLM API gateway wrapper supporting exponential backoff,
    jitter retries, primary/secondary model fallback routing, and async streaming.
    """

    def __init__(
        self,
        primary_model: str = "gpt-4o",
        fallback_model: str = "gpt-4o-mini",
        max_retries: int = 3,
        base_backoff_sec: float = 1.0,
    ):
        self.primary_model = primary_model
        self.fallback_model = fallback_model
        self.max_retries = max_retries
        self.base_backoff_sec = base_backoff_sec
        # Initialize standard async client (reads OPENAI_API_KEY from environment)
        self.client = AsyncOpenAI()

    async def execute_with_retry(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Executes a completion request using full jitter exponential backoff.
        """
        target_model = model or self.primary_model
        attempt = 0

        while attempt < self.max_retries:
            try:
                start_time = time.perf_counter()
                response = await self.client.chat.completions.create(
                    model=target_model,
                    messages=messages,
                    **kwargs
                )
                latency = round(time.perf_counter() - start_time, 3)

                return {
                    "content": response.choices[0].message.content,
                    "model_used": response.model,
                    "latency_sec": latency,
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                }

            except (RateLimitError, APIConnectionError) as e:
                attempt += 1
                if attempt >= self.max_retries:
                    raise e
                
                # Full Jitter Backoff Formula: sleep = random(0, min(cap, base * 2 ^ attempt))
                backoff = random.uniform(0, min(16.0, self.base_backoff_sec * (2 ** attempt)))
                print(f"[Warning] Transient error ({e.__class__.__name__}). Retrying in {backoff:.2f}s (Attempt {attempt}/{self.max_retries})")
                await asyncio.sleep(backoff)

    async def execute_with_fallback(
        self,
        messages: List[Dict[str, str]],
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Attempts execution on the primary model, falling back to a secondary model if unrecoverable API errors occur.
        """
        try:
            return await self.execute_with_retry(messages, model=self.primary_model, **kwargs)
        except (RateLimitError, APIError) as e:
            print(f"[Fallback Triggered] Primary model ({self.primary_model}) failed: {e}. Routing to fallback ({self.fallback_model})...")
            return await self.execute_with_retry(messages, model=self.fallback_model, **kwargs)

    async def stream_tokens(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        """
        Streams response tokens asynchronously as they arrive from the API provider.
        """
        target_model = model or self.primary_model
        stream = await self.client.chat.completions.create(
            model=target_model,
            messages=messages,
            stream=True,
            **kwargs
        )
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


if __name__ == "__main__":
    async def main():
        gateway = ResilientLLMGateway()
        test_messages = [
            {"role": "system", "content": "You are a concise engineering assistant."},
            {"role": "user", "content": "Explain circuit breaker pattern in LLM gateways in 2 sentences."}
        ]

        print("--- Testing Resilient Completion Execution ---")
        try:
            result = await gateway.execute_with_fallback(test_messages, max_tokens=100)
            print(f"Model Used : {result['model_used']}")
            print(f"Latency    : {result['latency_sec']}s")
            print(f"Tokens     : Input={result['prompt_tokens']}, Output={result['completion_tokens']}")
            print(f"Response   : {result['content']}\n")
        except Exception as err:
            print(f"Execution skipped (API Key missing or invalid): {err}\n")

        print("--- Testing Async Streaming ---")
        try:
            print("Stream Output: ", end="", flush=True)
            async for token in gateway.stream_tokens(test_messages, max_tokens=50):
                print(token, end="", flush=True)
            print("\n")
        except Exception as err:
            print(f"Streaming skipped (API Key missing or invalid): {err}")

    asyncio.run(main())