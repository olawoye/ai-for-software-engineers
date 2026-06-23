"""
Shared configuration and constants for Module 3 lessons.
Centralizes provider lists, model choices, and API settings.
"""

import os

# Available models via OpenRouter
MODELS = {
    "GPT-3.5 Turbo": "gpt-3.5-turbo",
    "GPT-4": "gpt-4",
    "Claude 3 Sonnet": "claude-3-sonnet",
    "Claude 3 Opus": "claude-3-opus",
}

# Default model for lessons
DEFAULT_MODEL = "gpt-3.5-turbo"

# Temperature ranges
TEMP_CREATIVE = 0.9
TEMP_BALANCED = 0.7
TEMP_PRECISE = 0.3

# Token limits for different lessons
CONTEXT_LIMITS = {
    "lesson_02": 2048,
    "lesson_03": 4096,
    "lesson_04": 8192,
    "lesson_05": 2048,
    "lesson_06": 4096,
}


def get_api_key() -> str:
    """Retrieve API key with validation."""
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise ValueError(
            "OPENROUTER_API_KEY not set. "
            "Export: export OPENROUTER_API_KEY='your-key-here'"
        )
    return key
