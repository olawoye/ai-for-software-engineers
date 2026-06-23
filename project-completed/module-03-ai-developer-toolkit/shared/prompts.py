"""
Reusable prompt templates for Module 3 lessons.
Centralize prompt engineering to avoid redundancy and improve consistency.
"""

# Lesson 3.2: API Call patterns
SUMMARIZATION_PROMPT = """
Summarize the following text in 2-3 sentences:

{text}
"""

# Lesson 3.3: Rapid prototyping
CLASSIFICATION_PROMPT = """
Classify the following text into ONE of these categories: {categories}

Text: {text}

Respond with only the category name.
"""

# Lesson 3.4: Chat interface
CHAT_SYSTEM_PROMPT = """
You are a helpful AI assistant. Answer questions clearly and concisely.
If you don't know something, say so rather than guessing.
"""

# Lesson 3.6: Summarizer service
DOCUMENT_SUMMARY_PROMPT = """
Create a concise executive summary of this document in {language}:

---
{document}
---

Summary (max 150 words):
"""


def build_chat_context(system: str, history: list, user_input: str) -> list:
    """Build message context for multi-turn chat."""
    messages = [{"role": "system", "content": system}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_input})
    return messages
