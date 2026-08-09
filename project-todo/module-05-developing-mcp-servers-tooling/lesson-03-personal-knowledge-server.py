"""
Lesson 5.3: Your First MCP Server - Personal Knowledge Server — TODO Scaffold

Build the core template for an MCP server that exposes local files and documents
for AI client access through a standardized protocol.

BUSINESS SCENARIO:
AI assistants need structured access to company files, documentation, and knowledge
bases. This lesson teaches building MCP servers that safely expose these resources
to clients through discoverable Resources and callable Tools.

Run: python lesson-03-personal-knowledge-server.py
Requires: export OPENROUTER_API_KEY='your-key-here'
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional
import tempfile

# Import from shared module
sys.path.insert(0, str(Path(__file__).parent))
from shared.mcp_server import MCPServer, Resource, Tool
from shared.resources import FileResource


# ============================================================================
# STAGE 1: Core Template Method (create_knowledge_server)
# ============================================================================
# Initialize MCP server with resource discovery and tool registration.
# Available utilities: MCPServer, FileResource, Resource, Tool classes
# TODO: Add your Stage 1 implementation here


# ============================================================================
# STAGE 2: Tool Implementations
# ============================================================================
# Implement tools for searching and retrieving documents from the knowledge base.
# Available utilities: file I/O, JSON formatting, search utilities
# TODO: Add your Stage 2 implementation here


# ============================================================================
# STAGE 3: Demonstrations
# ============================================================================
# Show server capabilities through resource discovery, tool invocation, and protocol examples.
# Available utilities: JSON-RPC format, test queries, example data
# TODO: Add your Stage 3 implementation here


# ============================================================================
# STAGE 4: Main Entry Point
# ============================================================================
# Orchestrate demo execution and server initialization.
# Available utilities: argparse, file path handling, demo selector
# TODO: Add your Stage 4 implementation here
