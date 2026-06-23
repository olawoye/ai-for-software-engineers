"""
Shared configuration and constants — TODO scaffold

PHASE 1: Define model options
PHASE 2: Add temperature constants
PHASE 3: Add context limits and API key validation
"""

import os

# PHASE 1: Available models via OpenRouter
MODELS = {
    # TODO: Add model names and their OpenRouter IDs
    # Example: "GPT-3.5 Turbo": "gpt-3.5-turbo"
}

# Default model for lessons
DEFAULT_MODEL = None  # TODO: Set default

# PHASE 2: Temperature ranges
TEMP_CREATIVE = None  # TODO: Set creative temperature (close to 1.0)
TEMP_BALANCED = None  # TODO: Set balanced temperature
TEMP_PRECISE = None  # TODO: Set precise temperature (close to 0.0)

# PHASE 3: Token limits for different lessons
CONTEXT_LIMITS = {
    # TODO: Add context windows
    # "lesson_02": 2048,
}


def get_api_key() -> str:
    """
    PHASE 3: Retrieve API key with validation.

    Returns:
        API key string

    Raises:
        ValueError: If API key not configured
    """
    # TODO: Get OPENROUTER_API_KEY from environment
    # TODO: Validate it's not empty
    # TODO: Return it or raise ValueError with helpful message
    pass
