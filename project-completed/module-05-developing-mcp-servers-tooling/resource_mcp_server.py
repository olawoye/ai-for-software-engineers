"""
AI For Software Engineers — Module 5: Model Context Protocol (MCP)
Resource: Standalone Lightweight MCP Server Protocol Handler
File: projects-completed/module-05/resource_mcp_server.py
"""

import asyncio
import json
import sys
from typing import Dict, Any, Callable


class MCPServer:
    """
    Lightweight, compliant MCP Server implementation handling JSON-RPC 2.0 
    handshakes, tool discovery, and execution over Stdio.
    """

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.tool_handlers: Dict[str, Callable] = {}

    def register_tool(self, name: str, description: str, input_schema: dict, handler: Callable):
        """Registers a tool capability with schema and execution callback."""
        self.tools[name] = {
            "name": name,
            "description": description,
            "inputSchema": input_schema,
        }
        self.tool_handlers[name] = handler

    def handle_request(self, request: dict) -> dict:
        """Parses and routes incoming JSON-RPC 2.0 requests."""
        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        # Handle Initialize Handshake
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {"listChanged": False}},
                    "serverInfo": {"name": self.name, "version": self.version},
                },
            }

        # Handle Tool Discovery
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"tools": list(self.tools.values())},
            }

        # Handle Tool Execution
        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})

            if tool_name not in self.tool_handlers:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Tool '{tool_name}' not found."},
                }

            try:
                result_text = self.tool_handlers[tool_name](**tool_args)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": str(result_text)}],
                        "isError": False,
                    },
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": f"Execution Error: {str(e)}"}],
                        "isError": True,
                    },
                }

        # Method Not Found Fallback
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method '{method}' unsupported."},
        }


# Sample Tool Implementation
def calculate_system_metrics(metric_type: str) -> str:
    """Mock handler for metric calculation tool."""
    if metric_type == "cpu":
        return json.dumps({"cpu_utilization": "14.2%", "status": "healthy"})
    elif metric_type == "memory":
        return json.dumps({"ram_used_gb": 6.4, "ram_total_gb": 16.0})
    return json.dumps({"error": "Unknown metric type"})


if __name__ == "__main__":
    # Instantiate Server
    mcp_server = MCPServer(name="SystemMonitorMCP", version="1.0.0")

    # Register Tool
    mcp_server.register_tool(
        name="get_system_metrics",
        description="Retrieves real-time system performance metrics.",
        input_schema={
            "type": "object",
            "properties": {
                "metric_type": {"type": "string", "enum": ["cpu", "memory"]}
            },
            "required": ["metric_type"],
        },
        handler=calculate_system_metrics,
    )

    # Test JSON-RPC Lifecycle Interactively
    print("=== TEST 1: Initialize Request ===")
    init_req = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
    print(json.dumps(mcp_server.handle_request(init_req), indent=2))

    print("\n=== TEST 2: List Tools Request ===")
    list_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
    print(json.dumps(mcp_server.handle_request(list_req), indent=2))

    print("\n=== TEST 3: Call Tool Request ===")
    call_req = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {"name": "get_system_metrics", "arguments": {"metric_type": "cpu"}},
    }
    print(json.dumps(mcp_server.handle_request(call_req), indent=2))