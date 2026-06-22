"""LLM helpers for the course companion."""

def prompt_builder(context: str, question: str) -> str:
    return f"Context: {context}\nQuestion: {question}"
