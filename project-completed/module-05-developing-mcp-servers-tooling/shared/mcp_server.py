"""
Base MCP server implementation using JSON-RPC protocol.
Handles resource and tool discovery, registration, and invocation.
"""

import json
import uuid
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict


@dataclass
class Resource:
    """MCP Resource definition."""

    name: str
    uri: str
    description: str
    mimeType: str = "text/plain"
    resource_id: str = None

    def __post_init__(self):
        if self.resource_id is None:
            self.resource_id = str(uuid.uuid4())


@dataclass
class Tool:
    """MCP Tool definition."""

    name: str
    description: str
    inputSchema: Dict[str, Any]
    tool_id: str = None

    def __post_init__(self):
        if self.tool_id is None:
            self.tool_id = str(uuid.uuid4())


class MCPServer:
    """Base MCP server implementing JSON-RPC protocol."""

    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.resources: Dict[str, Resource] = {}
        self.tools: Dict[str, Tool] = {}
        self.tool_handlers: Dict[str, Callable] = {}
        self.resource_handlers: Dict[str, Callable] = {}

    def register_resource(
        self,
        resource: Resource,
        handler: Optional[Callable] = None,
    ) -> None:
        """Register a resource."""
        self.resources[resource.name] = resource
        if handler:
            self.resource_handlers[resource.name] = handler

    def register_tool(
        self,
        tool: Tool,
        handler: Callable,
    ) -> None:
        """Register a tool with its handler."""
        self.tools[tool.name] = tool
        self.tool_handlers[tool.name] = handler

    def list_resources(self) -> List[Dict]:
        """List available resources."""
        return [
            {
                "name": r.name,
                "uri": r.uri,
                "description": r.description,
                "mimeType": r.mimeType,
            }
            for r in self.resources.values()
        ]

    def list_tools(self) -> List[Dict]:
        """List available tools."""
        return [
            {
                "name": t.name,
                "description": t.description,
                "inputSchema": t.inputSchema,
            }
            for t in self.tools.values()
        ]

    def read_resource(self, uri: str) -> Optional[str]:
        """Read a resource by URI."""
        for resource in self.resources.values():
            if resource.uri == uri:
                if resource.name in self.resource_handlers:
                    return self.resource_handlers[resource.name](uri)
        return None

    def call_tool(self, tool_name: str, arguments: Dict) -> Any:
        """Call a tool with arguments."""
        if tool_name not in self.tool_handlers:
            raise ValueError(f"Tool '{tool_name}' not found")

        return self.tool_handlers[tool_name](**arguments)

    def handle_jsonrpc(self, request: Dict) -> Dict:
        """Handle JSON-RPC request."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        try:
            if method == "resources/list":
                result = self.list_resources()
            elif method == "resources/read":
                result = self.read_resource(params.get("uri"))
            elif method == "tools/list":
                result = self.list_tools()
            elif method == "tools/call":
                result = self.call_tool(
                    params.get("name"),
                    params.get("arguments", {}),
                )
            else:
                raise ValueError(f"Unknown method: {method}")

            return {
                "jsonrpc": "2.0",
                "result": result,
                "id": request_id,
            }

        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": str(e),
                },
                "id": request_id,
            }

    def get_server_info(self) -> Dict:
        """Get server information."""
        return {
            "name": self.name,
            "version": self.version,
            "resources": len(self.resources),
            "tools": len(self.tools),
        }
