"""
Lesson 5.3 TODO: Your First MCP Server - Personal Knowledge Server

In this lesson, you'll build the core template method for an MCP server
that exposes local files and documents for AI client access.

Your goal: Implement create_knowledge_server(), a reusable template that:
  - Discovers files in a knowledge directory
  - Registers them as MCP Resources
  - Provides Tools for searching and retrieving documents
  - Handles JSON-RPC protocol requests

PHASE 1: Core Template Method (create_knowledge_server)
  - Accept parameters: knowledge_dir, server_name, file_extensions
  - Initialize MCPServer with name and version
  - Create FileResource handler for the knowledge directory
  - Discover and register resources for each file
  - Register at least 2 tools: search_knowledge, get_document
  - Return the configured server

PHASE 2: Tool Implementations
  - search_knowledge(query): Search files for keyword matches
    Return JSON with query, list of matches, and count
  - get_document(filename): Retrieve full content of a document
    Return JSON with filename, content, and size
  - get_knowledge_stats(): Return KB statistics
    Return JSON with file count, total size, base directory

PHASE 3: Demonstrations
  - demo_core_method(): Show server initialization and setup
  - demo_resource_discovery(): List registered resources
  - demo_tool_invocation(): Execute tools with test queries
  - demo_jsonrpc_protocol(): Show JSON-RPC request/response examples
  - main(): Run all demonstrations

REFERENCE:
  - Completed implementation: project-completed/module-05-developing-mcp-servers-tooling/lesson-03-personal-knowledge-server.py
  - MCP server base: shared/mcp_server.py
  - File resources: shared/resources.py (FileResource class)
  - Business scenario: Enable AI assistants to access local project files and documentation
  - Data flow: Files → Resources → Tools → Client requests (JSON-RPC)

LEARNING GOALS:
  1. Understand how MCP servers expose capabilities to AI clients
  2. Learn to register resources (discoverable documents)
  3. Implement tools (callable functions with schemas)
  4. See JSON-RPC protocol in action
  5. Create reusable server templates for your own projects
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional
import tempfile

# Import from shared module (reference path)
sys.path.insert(0, str(Path(__file__).parent))
from shared.mcp_server import MCPServer, Resource, Tool
from shared.resources import FileResource


# ============================================================================
# PHASE 1: Core Template Method - create_knowledge_server()
# ============================================================================
# TODO: Implement the core create_knowledge_server() function
#
# Requirements:
#   1. Accept parameters: knowledge_dir, server_name, file_extensions
#   2. Initialize MCPServer with name and version "1.0.0"
#   3. Create FileResource(knowledge_dir) handler
#   4. Discover files matching extensions using file_resource.list_files(pattern)
#   5. For each discovered file:
#      - Create Resource with name, uri, description, mimeType
#      - Register with MCPServer.register_resource()
#   6. Implement and register tools (see PHASE 2)
#   7. Return configured server
#
# Hints:
#   - Use enumerate(file_extensions) to build glob patterns like "*{ext}"
#   - Resource URI format: f"file://{file_path}"
#   - Use make_handler closure to capture file path for each resource
#   - Print status messages for debugging (✓ notation helps readability)

def create_knowledge_server(
    knowledge_dir: str,
    server_name: str = "PersonalKnowledge",
    file_extensions: List[str] | None = None,
) -> MCPServer:
    """TODO: Initialize and configure a Personal Knowledge MCP Server.
    
    This is the production-ready server initialization pattern for document access.
    Learners can extract this method and adapt it for their own knowledge sources.
    
    Args:
        knowledge_dir: Path to directory containing knowledge files
        server_name: Name of the MCP server (for identification)
        file_extensions: List of file extensions to index (default: ['.md', '.txt', '.py'])
    
    Returns:
        MCPServer: Configured server with resources and tools registered.
        Ready to accept client requests via JSON-RPC.
    """
    # Step 1: TODO Initialize server
    # TODO Step 2: Setup file resource handler
    # TODO Step 3: Discover and register resources
    # TODO Step 4-6: Define and register tools (see PHASE 2 below)
    
    pass


# ============================================================================
# PHASE 2: Tool Implementations
# ============================================================================
# TODO: Implement these three tools to be registered in create_knowledge_server()
#
# Each tool should:
#   1. Accept structured inputs (defined in inputSchema)
#   2. Process the request
#   3. Return JSON string with results
#
# Tool 1: search_knowledge(query: str) -> str
#   - Search all discovered files for keyword matches
#   - Count matched lines per file
#   - Return: {"query": str, "matches": List[Dict], "count": int}
#
# Tool 2: get_document(filename: str) -> str
#   - Retrieve full content of a named document
#   - Include size in bytes
#   - Return: {"filename": str, "content": str, "size_bytes": int}
#
# Tool 3: get_knowledge_stats() -> str
#   - Calculate total files and size
#   - Return: {"total_files": int, "total_size_bytes": int, ...}

# TODO: Define search_knowledge tool function
# TODO: Define get_document tool function
# TODO: Define get_knowledge_stats tool function


# ============================================================================
# PHASE 3: Demonstrations
# ============================================================================
# TODO: Implement demonstration functions to show how the template works
#
# Each demo should:
#   1. Call create_knowledge_server() with sample data
#   2. Show one specific aspect (resources, tools, JSON-RPC, etc.)
#   3. Print clear output with learning points
#
# See completed version for full implementation details and output format

def demo_core_method():
    """TODO: Demonstrate core server initialization and setup."""
    # Create temporary directory with sample documents
    # Call create_knowledge_server()
    # Show successful initialization message
    # Return server and temp_dir for other demos
    pass


def demo_resource_discovery():
    """TODO: Demonstrate resource discovery."""
    # Call demo_core_method()
    # Get server.list_resources()
    # Print each resource with name, URI, description, MIME type
    # Show learning point about resource discovery
    pass


def demo_tool_invocation():
    """TODO: Demonstrate tool execution."""
    # Call demo_core_method()
    # List all tools with descriptions and schemas
    # Execute search_knowledge with test queries: ["RAG", "TODO", "embedding"]
    # Show matches and learning point about tool schemas
    pass


def demo_jsonrpc_protocol():
    """TODO: Demonstrate JSON-RPC protocol."""
    # Call demo_core_method()
    # Show JSON-RPC protocol overview
    # Display 3 example requests:
    #   1. List resources
    #   2. Search knowledge
    #   3. Retrieve document
    # Show request/response format
    # Explain JSON-RPC 2.0 concepts
    pass


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("LESSON 5.3: YOUR FIRST MCP SERVER - PERSONAL KNOWLEDGE SERVER")
    print("=" * 70)
    print("\nThis lesson demonstrates how to build a reusable MCP server template")
    print("that exposes local files and documents for AI client access.\n")
    
    # TODO: Call all demonstrations in order
    # TODO: Show lesson completion message with key takeaways
