"""Base evaluation abstractions for companion lessons."""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseEval(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def evaluate(self, results: dict) -> dict[str, float]:
        ...  # pragma: no cover
