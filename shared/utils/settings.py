"""Provider configuration shared across lessons."""

from dataclasses import dataclass
import os


@dataclass
class ProviderSettings:
    openai_key: str | None
    anthropic_key: str | None
    openrouter_url: str | None
    ollama_url: str | None


def load_settings() -> ProviderSettings:
    return ProviderSettings(
        openai_key=os.getenv("OPENAI_API_KEY"),
        anthropic_key=os.getenv("ANTHROPIC_API_KEY"),
        openrouter_url=os.getenv(
            "OPENROUTER_URL", "https://api.openrouter.ai/v1/chat/completions"
        ),
        ollama_url=os.getenv("OLLAMA_URL", "http://localhost:11434/completions"),
    )
