"""Vector retrieval helpers for RAG lessons."""

def configure_retriever(name: str, collection: str) -> dict[str, str]:
    return {"name": name, "collection": collection}
