"""
Resource management for MCP servers.
Handles file access, knowledge bases, and document repositories.
"""

import os
from pathlib import Path
from typing import List, Dict, Optional


class FileResource:
    """Manages file-based resources."""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def list_files(self, pattern: str = "*.md") -> List[str]:
        """List files matching pattern."""
        return [str(f) for f in self.base_path.glob(pattern)]

    def read_file(self, filename: str) -> Optional[str]:
        """Read file contents."""
        filepath = self.base_path / filename

        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filename}")

        if not str(filepath).startswith(str(self.base_path)):
            raise PermissionError("Access denied")

        with open(filepath, "r") as f:
            return f.read()

    def write_file(self, filename: str, content: str) -> bool:
        """Write file contents."""
        filepath = self.base_path / filename

        if not str(filepath).startswith(str(self.base_path)):
            raise PermissionError("Access denied")

        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as f:
            f.write(content)
        return True

    def get_stats(self) -> Dict:
        """Get directory statistics."""
        files = list(self.base_path.glob("**/*"))
        return {
            "total_files": len([f for f in files if f.is_file()]),
            "total_dirs": len([f for f in files if f.is_dir()]),
            "base_path": str(self.base_path),
        }


class KnowledgebaseResource:
    """Manages knowledge base resources."""

    def __init__(self, documents: List[Dict] = None):
        self.documents = documents or []

    def add_document(self, title: str, content: str, metadata: Dict = None) -> str:
        """Add document to knowledge base."""
        doc_id = f"doc_{len(self.documents)}"
        self.documents.append({
            "id": doc_id,
            "title": title,
            "content": content,
            "metadata": metadata or {},
        })
        return doc_id

    def search_documents(self, query: str) -> List[Dict]:
        """Search documents by keyword."""
        results = []
        query_lower = query.lower()

        for doc in self.documents:
            if query_lower in doc["title"].lower() or query_lower in doc["content"].lower():
                results.append(doc)

        return results

    def get_document(self, doc_id: str) -> Optional[Dict]:
        """Get specific document."""
        for doc in self.documents:
            if doc["id"] == doc_id:
                return doc
        return None

    def list_documents(self) -> List[Dict]:
        """List all documents (metadata only)."""
        return [
            {
                "id": d["id"],
                "title": d["title"],
                "metadata": d["metadata"],
            }
            for d in self.documents
        ]
