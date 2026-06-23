"""
Common MCP tools implementations.
Provides reusable tool patterns for email, file, and data operations.
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class EmailTools:
    """Email analysis and management tools."""

    @staticmethod
    def parse_email(sender: str, subject: str, body: str) -> Dict:
        """Parse and structure an email message."""
        return {
            "sender": sender,
            "subject": subject,
            "body": body,
            "received_at": datetime.now().isoformat(),
            "sentiment": EmailTools._analyze_sentiment(body),
        }

    @staticmethod
    def _analyze_sentiment(text: str) -> str:
        """Simple sentiment analysis (keyword-based)."""
        positive = ["good", "great", "excellent", "perfect", "thank"]
        negative = ["bad", "poor", "terrible", "urgent", "issue", "problem"]

        text_lower = text.lower()
        pos_count = sum(1 for word in positive if word in text_lower)
        neg_count = sum(1 for word in negative if word in text_lower)

        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        else:
            return "neutral"

    @staticmethod
    def categorize_email(subject: str, body: str) -> str:
        """Categorize email type."""
        text = (subject + " " + body).lower()

        if any(word in text for word in ["meeting", "schedule", "calendar"]):
            return "meeting_request"
        elif any(word in text for word in ["question", "help", "issue", "problem"]):
            return "support_request"
        elif any(word in text for word in ["report", "analysis", "update"]):
            return "status_report"
        else:
            return "general"

    @staticmethod
    def identify_action_items(body: str) -> List[str]:
        """Extract action items from email body."""
        items = []
        for line in body.split("\n"):
            line = line.strip()
            if line.startswith("-") or line.startswith("•") or line.startswith("*"):
                items.append(line.lstrip("-•* "))

        return items


class DataTools:
    """Data processing and analysis tools."""

    @staticmethod
    def summarize_data(data: List[Dict]) -> Dict:
        """Generate summary statistics."""
        if not data:
            return {"count": 0}

        return {
            "count": len(data),
            "fields": list(data[0].keys()) if data else [],
            "sample": data[0] if data else None,
        }

    @staticmethod
    def filter_data(data: List[Dict], criteria: Dict) -> List[Dict]:
        """Filter data by criteria."""
        results = []

        for item in data:
            match = True
            for key, value in criteria.items():
                if key not in item or item[key] != value:
                    match = False
                    break
            if match:
                results.append(item)

        return results

    @staticmethod
    def sort_data(data: List[Dict], field: str, descending: bool = False) -> List[Dict]:
        """Sort data by field."""
        return sorted(
            data,
            key=lambda x: x.get(field, ""),
            reverse=descending,
        )


class TextTools:
    """Text processing and analysis."""

    @staticmethod
    def extract_keywords(text: str, top_k: int = 5) -> List[str]:
        """Extract top keywords from text."""
        words = text.lower().split()
        stopwords = {"the", "a", "an", "and", "or", "is", "to", "in", "of"}

        filtered = [w for w in words if w not in stopwords and len(w) > 3]

        # Simple frequency count
        freq = {}
        for word in filtered:
            freq[word] = freq.get(word, 0) + 1

        sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in sorted_words[:top_k]]

    @staticmethod
    def truncate_text(text: str, max_length: int = 100) -> str:
        """Truncate text to max length."""
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."

    @staticmethod
    def count_statistics(text: str) -> Dict:
        """Count text statistics."""
        words = text.split()
        sentences = text.split(".")

        return {
            "characters": len(text),
            "words": len(words),
            "sentences": len([s for s in sentences if s.strip()]),
            "avg_word_length": sum(len(w) for w in words) / len(words) if words else 0,
        }
