"""
Validation utilities for MCP tool inputs.
Provides schema validation and input sanitization.
"""

from typing import Dict, Any, List, Optional
import re


class SchemaValidator:
    """Validates inputs against JSON schemas."""

    @staticmethod
    def validate_string(value: Any, min_length: int = 0, max_length: int = None) -> bool:
        """Validate string input."""
        if not isinstance(value, str):
            return False

        if len(value) < min_length:
            return False

        if max_length and len(value) > max_length:
            return False

        return True

    @staticmethod
    def validate_number(value: Any, minimum: float = None, maximum: float = None) -> bool:
        """Validate number input."""
        if not isinstance(value, (int, float)):
            return False

        if minimum is not None and value < minimum:
            return False

        if maximum is not None and value > maximum:
            return False

        return True

    @staticmethod
    def validate_enum(value: Any, allowed: List[Any]) -> bool:
        """Validate enum input."""
        return value in allowed

    @staticmethod
    def validate_object(value: Any, schema: Dict) -> bool:
        """Validate object against schema."""
        if not isinstance(value, dict):
            return False

        for field, field_schema in schema.items():
            if field not in value:
                if field_schema.get("required", False):
                    return False
                continue

            field_value = value[field]
            field_type = field_schema.get("type")

            if field_type == "string":
                if not SchemaValidator.validate_string(field_value):
                    return False
            elif field_type == "number":
                if not SchemaValidator.validate_number(field_value):
                    return False
            elif field_type == "enum":
                if not SchemaValidator.validate_enum(field_value, field_schema.get("allowed", [])):
                    return False

        return True


class InputSanitizer:
    """Sanitizes and normalizes user inputs."""

    @staticmethod
    def sanitize_text(text: str) -> str:
        """Remove potentially harmful characters."""
        # Remove null bytes
        text = text.replace("\x00", "")

        # Remove control characters (except whitespace)
        text = "".join(char for char in text if ord(char) >= 32 or char in "\n\t\r")

        return text.strip()

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename."""
        # Remove path separators and special characters
        filename = filename.replace("/", "").replace("\\", "")
        filename = re.sub(r"[<>:\"|?*]", "", filename)
        return filename.strip()

    @staticmethod
    def sanitize_email(email: str) -> Optional[str]:
        """Validate and normalize email."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        email = email.strip().lower()
        if re.match(pattern, email):
            return email

        return None

    @staticmethod
    def normalize_path(path: str, base_path: str) -> str:
        """Normalize and validate file path."""
        # Remove special characters that could be used for traversal
        path = path.replace("..", "").replace("~", "")
        path = path.lstrip("/")

        # Ensure it's under base_path
        full_path = f"{base_path}/{path}"
        return full_path.replace("//", "/")


class RateLimiter:
    """Simple rate limiting for tool calls."""

    def __init__(self, max_calls: int = 10, window_seconds: int = 60):
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.call_log: Dict[str, List[float]] = {}

    def is_allowed(self, user_id: str) -> bool:
        """Check if user is within rate limit."""
        import time

        now = time.time()
        window_start = now - self.window_seconds

        if user_id not in self.call_log:
            self.call_log[user_id] = []

        # Remove old calls
        self.call_log[user_id] = [
            timestamp for timestamp in self.call_log[user_id]
            if timestamp > window_start
        ]

        if len(self.call_log[user_id]) < self.max_calls:
            self.call_log[user_id].append(now)
            return True

        return False

    def get_remaining(self, user_id: str) -> int:
        """Get remaining calls for user."""
        import time

        now = time.time()
        window_start = now - self.window_seconds

        if user_id not in self.call_log:
            return self.max_calls

        recent_calls = [
            timestamp for timestamp in self.call_log[user_id]
            if timestamp > window_start
        ]

        return max(0, self.max_calls - len(recent_calls))
