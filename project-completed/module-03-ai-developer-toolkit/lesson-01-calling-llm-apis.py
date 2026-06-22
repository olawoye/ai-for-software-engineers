"""Lesson 01: Calling LLM APIs."""

from typing import List


def build_api_prompt(context: str, question: str) -> str:
    return f"Context: {context}\nQuestion: {question}"


def sample_response(prompt: str) -> str:
    return f"This would be the model response for: {prompt}"


if __name__ == "__main__":
    prompt = build_api_prompt("LLM fundamentals", "How do you call an API?")
    print(sample_response(prompt))
