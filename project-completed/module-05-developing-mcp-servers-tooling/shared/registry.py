"""
Tool and resource registry for MCP servers.
Central catalog of available capabilities.
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass


@dataclass
class ToolInfo:
    """Tool metadata."""

    name: str
    description: str
    category: str
    input_schema: Dict[str, Any]
    output_schema: Optional[Dict] = None
    requires_auth: bool = False
    rate_limited: bool = False


class ToolRegistry:
    """Central registry for all available tools."""

    def __init__(self):
        self.tools: Dict[str, ToolInfo] = {}
        self.handlers: Dict[str, Callable] = {}
        self.categories: Dict[str, List[str]] = {}

    def register(
        self,
        tool_info: ToolInfo,
        handler: Callable,
    ) -> None:
        """Register a tool with handler."""
        self.tools[tool_info.name] = tool_info
        self.handlers[tool_info.name] = handler

        if tool_info.category not in self.categories:
            self.categories[tool_info.category] = []

        self.categories[tool_info.category].append(tool_info.name)

    def get(self, name: str) -> Optional[ToolInfo]:
        """Get tool info by name."""
        return self.tools.get(name)

    def list_all(self) -> List[ToolInfo]:
        """List all tools."""
        return list(self.tools.values())

    def list_by_category(self, category: str) -> List[ToolInfo]:
        """List tools by category."""
        tool_names = self.categories.get(category, [])
        return [self.tools[name] for name in tool_names if name in self.tools]

    def get_handler(self, name: str) -> Optional[Callable]:
        """Get tool handler."""
        return self.handlers.get(name)

    def get_categories(self) -> List[str]:
        """List all categories."""
        return list(self.categories.keys())

    def get_stats(self) -> Dict:
        """Get registry statistics."""
        return {
            "total_tools": len(self.tools),
            "categories": len(self.categories),
            "auth_required": sum(1 for t in self.tools.values() if t.requires_auth),
            "rate_limited": sum(1 for t in self.tools.values() if t.rate_limited),
        }


class ResourceRegistry:
    """Central registry for all available resources."""

    def __init__(self):
        self.resources: Dict[str, Dict] = {}
        self.handlers: Dict[str, Callable] = {}

    def register(
        self,
        name: str,
        uri: str,
        description: str,
        handler: Callable,
        mime_type: str = "text/plain",
    ) -> None:
        """Register a resource."""
        self.resources[name] = {
            "uri": uri,
            "description": description,
            "mime_type": mime_type,
        }
        self.handlers[name] = handler

    def get(self, name: str) -> Optional[Dict]:
        """Get resource info."""
        return self.resources.get(name)

    def list_all(self) -> List[Dict]:
        """List all resources."""
        return [
            {
                "name": name,
                **info,
            }
            for name, info in self.resources.items()
        ]

    def get_handler(self, name: str) -> Optional[Callable]:
        """Get resource handler."""
        return self.handlers.get(name)

    def get_stats(self) -> Dict:
        """Get registry statistics."""
        return {
            "total_resources": len(self.resources),
        }


class ServiceRegistry:
    """Combined tool and resource registry."""

    def __init__(self):
        self.tools = ToolRegistry()
        self.resources = ResourceRegistry()

    def get_stats(self) -> Dict:
        """Get complete service statistics."""
        return {
            "tools": self.tools.get_stats(),
            "resources": self.resources.get_stats(),
        }

    def get_capabilities(self) -> Dict:
        """Get all capabilities summary."""
        return {
            "tools": [
                {
                    "name": t.name,
                    "description": t.description,
                    "category": t.category,
                }
                for t in self.tools.list_all()
            ],
            "resources": self.resources.list_all(),
        }
