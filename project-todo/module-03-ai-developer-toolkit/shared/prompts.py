"""
Reusable prompt templates — TODO scaffold

PHASE 1: Define basic prompts
PHASE 2: Add prompt with parameters
PHASE 3: Implement helper functions
"""

# PHASE 1: Lesson 3.2 API patterns
SUMMARIZATION_PROMPT = None  # TODO: Write a summarization prompt template

# PHASE 1: Lesson 3.3 Rapid prototyping
CLASSIFICATION_PROMPT = None  # TODO: Write a classification prompt template

# PHASE 1: Lesson 3.4 Chat interface
CHAT_SYSTEM_PROMPT = None  # TODO: Write a system prompt for chat

# PHASE 2: Lesson 3.6 Summarizer service
DOCUMENT_SUMMARY_PROMPT = None  # TODO: Write document summary prompt with {document} placeholder


def build_chat_context(system: str, history: list, user_input: str) -> list:
    """
    PHASE 3: Build message context for multi-turn chat.

    Args:
        system: System prompt defining assistant behavior
        history: List of previous messages
        user_input: Current user message

    Returns:
        List of messages formatted for API call
    """
    # TODO: Create message list structure
    # TODO: Add system message first
    # TODO: Add conversation history
    # TODO: Add current user message
    # TODO: Return formatted messages
    pass
