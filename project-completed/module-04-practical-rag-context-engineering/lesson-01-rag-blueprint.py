"""Lesson 01: Practical RAG blueprint."""

from dataclasses import dataclass


@dataclass
class RAGConfig:
    retriever: str
    retriever_config: dict
    response_strategy: str


def blueprint() -> RAGConfig:
    return RAGConfig(
        retriever="Chroma",
        retriever_config={"collection": "course-notes"},
        response_strategy="ranked"
    )


if __name__ == "__main__":
    print(blueprint())
