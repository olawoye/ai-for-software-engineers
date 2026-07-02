"""
Lesson 5.3: Your First MCP Server - Personal Knowledge Server

Build a local MCP server that exposes files and documents as resources,
with tools for searching and retrieving knowledge base content.

This lesson demonstrates the core create_knowledge_server() template method
that learners can reuse in their own projects with minimal configuration changes.

Run:
    python lesson-03-personal-knowledge-server.py
    
    To also see interactive JSON-RPC requests, set environment variable:
    export DEMO_JSONRPC=1 before running.
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
# CORE TEMPLATE METHOD: create_knowledge_server()
# ============================================================================
# This method is the foundation of MCP server creation for document access.
# It takes a knowledge directory, discovers files, registers them as resources,
# and provides tools for searching and retrieving content.
#
# Template structure:
#   - Input: knowledge_dir, server_name, file_extensions
#   - Processing: file discovery, resource registration, tool setup
#   - Output: configured MCPServer ready to handle client requests
#
# Reusability: Copy this method into your own projects with only:
#   - Knowledge directory configuration
#   - File extension filtering
#   - Custom resource metadata
#   - Additional tool definitions
# ============================================================================

def create_knowledge_server(
    knowledge_dir: str,
    server_name: str = "PersonalKnowledge",
    file_extensions: List[str] | None = None,
) -> MCPServer:
    """Core template method: Initialize and configure a Personal Knowledge MCP Server.
    
    This is the production-ready server initialization pattern for document access.
    Learners can extract this method and adapt it for their own knowledge sources.
    
    Args:
        knowledge_dir: Path to directory containing knowledge files
        server_name: Name of the MCP server (for identification)
        file_extensions: List of file extensions to index (default: ['.md', '.txt', '.py'])
    
    Returns:
        MCPServer: Configured server with resources and tools registered.
        Ready to accept client requests via JSON-RPC.
    
    Features:
        - Automatic file discovery and resource registration
        - Full-text search tool for knowledge base queries
        - Resource content retrieval
        - Statistics and metadata tracking
    
    Example:
        >>> server = create_knowledge_server('/path/to/docs', 'MyKnowledge')
        >>> resources = server.list_resources()  # Discover available documents
        >>> results = server.call_tool('search_knowledge', {'query': 'RAG'})
        >>> content = server.read_resource('file:///path/to/docs/guide.md')
    """
    
    # Step 1: Initialize server
    server = MCPServer(name=server_name, version="1.0.0")
    
    # Step 2: Setup file resource handler
    file_extensions = file_extensions or ['.md', '.txt', '.py']
    file_resource = FileResource(knowledge_dir)
    
    print(f"✓ Initialized {server_name} MCP server")
    print(f"  Knowledge directory: {knowledge_dir}")
    print(f"  File extensions: {', '.join(file_extensions)}")
    
    # Step 3: Discover and register resources
    discovered_files = []
    for ext in file_extensions:
        pattern = f"*{ext}"
        files = file_resource.list_files(pattern)
        discovered_files.extend(files)
    
    print(f"✓ Discovered {len(discovered_files)} knowledge files")
    
    for file_path in discovered_files:
        filename = Path(file_path).name
        
        # Create resource definition
        resource = Resource(
            name=filename,
            uri=f"file://{file_path}",
            description=f"Knowledge document: {filename}",
            mimeType="text/plain",
        )
        
        # Register resource with handler
        def make_handler(fp, filename):
            """Create closure to capture file path."""
            def handler(uri):
                try:
                    return file_resource.read_file(filename)
                except Exception as e:
                    return f"Error reading {filename}: {str(e)}"
            return handler
        
        server.register_resource(resource, handler=make_handler(file_path, filename))
    
    # Step 4: Define and register search tool
    def search_knowledge(query: str) -> str:
        """Search knowledge base for matching documents.
        
        Args:
            query: Search query string (case-insensitive keyword match)
        
        Returns:
            JSON string with query, matched files, and total count
        """
        results = []
        
        # Search through all discovered files
        for file_path in discovered_files:
            filename = Path(file_path).name
            try:
                content = file_resource.read_file(filename)
                # Simple keyword search (case-insensitive)
                if query.lower() in content.lower():
                    results.append({
                        "filename": filename,
                        "uri": f"file://{file_path}",
                        "matched_lines": sum(
                            1 for line in content.split('\n')
                            if query.lower() in line.lower()
                        )
                    })
            except Exception as e:
                pass  # Skip files with read errors
        
        return json.dumps({
            "query": query,
            "matches": results,
            "count": len(results),
        })
    
    search_tool = Tool(
        name="search_knowledge",
        description="Search personal knowledge base for documents containing query text",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query text (keyword match, case-insensitive)"
                }
            },
            "required": ["query"],
        },
    )
    
    server.register_tool(search_tool, search_knowledge)
    
    # Step 5: Define and register retrieval tool
    def get_document(filename: str) -> str:
        """Retrieve full content of a knowledge document.
        
        Args:
            filename: Name of the file to retrieve
        
        Returns:
            Document content, or error message if file not found
        """
        try:
            # Security: only allow access to files in knowledge_dir
            if filename not in [Path(f).name for f in discovered_files]:
                return json.dumps({"error": f"Document not found: {filename}"})
            
            content = file_resource.read_file(filename)
            return json.dumps({
                "filename": filename,
                "content": content,
                "size_bytes": len(content),
            })
        except Exception as e:
            return json.dumps({"error": f"Error retrieving {filename}: {str(e)}"})
    
    get_tool = Tool(
        name="get_document",
        description="Retrieve the full content of a knowledge document",
        inputSchema={
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Name of the file to retrieve"
                }
            },
            "required": ["filename"],
        },
    )
    
    server.register_tool(get_tool, get_document)
    
    # Step 6: Define and register stats tool
    def get_knowledge_stats() -> str:
        """Get statistics about knowledge base.
        
        Returns:
            JSON with file count, total size, and directory info
        """
        total_size = 0
        for file_path in discovered_files:
            total_size += os.path.getsize(file_path)
        
        return json.dumps({
            "total_files": len(discovered_files),
            "total_size_bytes": total_size,
            "base_directory": knowledge_dir,
            "file_extensions": file_extensions,
        })
    
    stats_tool = Tool(
        name="get_knowledge_stats",
        description="Get statistics about the knowledge base",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    )
    
    server.register_tool(stats_tool, get_knowledge_stats)
    
    print(f"✓ Registered {len(server.list_tools())} tools")
    
    return server


# ============================================================================
# DEMONSTRATIONS: Show how the template works
# ============================================================================

def demo_core_method():
    """Demonstration 1: Core server initialization and setup."""
    print("\n" + "=" * 70)
    print("DEMO 1: CORE TEMPLATE METHOD - create_knowledge_server()")
    print("=" * 70)
    
    # Create temporary knowledge directory for demo
    temp_dir = tempfile.mkdtemp(prefix="knowledge_")
    
    # Create sample documents
    sample_docs = [
        ("README.md", """# My Project
        
## Overview
This is my personal project documentation.

## RAG Resources
- Understanding RAG systems
- Vector databases
- Embedding models
"""),
        ("notes.md", """# My Notes

### TODO Items
- Research RAG systems
- Implement vector search
- Test embedding quality

### Completed
- Module 3 review
- Started Module 4
"""),
        ("guide.py", """# Code reference
# This is a sample Python guide

def create_embedding(text):
    '''Create semantic embedding'''
    pass

class RAGSystem:
    '''Retrieval augmented generation'''
    pass
"""),
    ]
    
    for filename, content in sample_docs:
        filepath = os.path.join(temp_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
    
    # Initialize server using the template method
    server = create_knowledge_server(
        knowledge_dir=temp_dir,
        server_name="DemoKnowledge",
        file_extensions=['.md', '.py']
    )
    
    print(f"\n✅ Server initialized successfully")
    print(f"   Server: {server.name} v{server.version}")
    print(f"   Knowledge Dir: {temp_dir}")
    
    return server, temp_dir


def demo_resource_discovery():
    """Demonstration 2: Discover registered resources."""
    print("\n" + "=" * 70)
    print("DEMO 2: RESOURCE DISCOVERY")
    print("=" * 70)
    
    server, temp_dir = demo_core_method()
    
    print("\nRegistered Resources:")
    print("-" * 70)
    
    resources = server.list_resources()
    for i, resource in enumerate(resources, 1):
        print(f"{i}. {resource['name']}")
        print(f"   URI: {resource['uri']}")
        print(f"   Description: {resource['description']}")
        print(f"   MIME Type: {resource['mimeType']}")
        print()
    
    print(f"✅ Total resources: {len(resources)}")
    print("\nLearning Point:")
    print("  Resources are discoverable by AI clients. They can list and read them.")
    print("  Each resource has a URI that clients use to retrieve content.")


def demo_tool_invocation():
    """Demonstration 3: Execute tools via the server."""
    print("\n" + "=" * 70)
    print("DEMO 3: TOOL INVOCATION")
    print("=" * 70)
    
    server, temp_dir = demo_core_method()
    
    print("\nAvailable Tools:")
    print("-" * 70)
    
    tools = server.list_tools()
    for i, tool in enumerate(tools, 1):
        print(f"{i}. {tool['name']}")
        print(f"   Description: {tool['description']}")
        print(f"   Input Schema: {json.dumps(tool['inputSchema'], indent=6)}")
        print()
    
    print("\nExecuting Tool: search_knowledge")
    print("-" * 70)
    
    test_queries = [
        "RAG",
        "TODO",
        "embedding",
    ]
    
    for query in test_queries:
        try:
            result = server.tool_handlers['search_knowledge'](query=query)
            result_data = json.loads(result)
            print(f"\nQuery: '{query}'")
            print(f"  Matches found: {result_data['count']}")
            for match in result_data['matches']:
                print(f"    • {match['filename']} ({match['matched_lines']} lines)")
        except Exception as e:
            print(f"Error executing search: {e}")
    
    print(f"\n✅ Tool execution complete")
    print("\nLearning Point:")
    print("  Tools are callable handlers that process structured inputs.")
    print("  Each tool has a schema that defines expected parameters.")


def demo_jsonrpc_protocol():
    """Demonstration 4: Show JSON-RPC protocol details."""
    print("\n" + "=" * 70)
    print("DEMO 4: JSON-RPC PROTOCOL")
    print("=" * 70)
    
    server, temp_dir = demo_core_method()
    
    print("\nJSON-RPC Protocol Overview:")
    print("-" * 70)
    print("MCP uses JSON-RPC 2.0 for client-server communication.")
    print("Clients send structured JSON requests; servers respond with results.\n")
    
    # Example JSON-RPC requests
    example_requests = [
        {
            "name": "List Available Resources",
            "request": {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "resources/list",
                "params": {}
            }
        },
        {
            "name": "Search Knowledge Base",
            "request": {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "search_knowledge",
                    "arguments": {
                        "query": "RAG"
                    }
                }
            }
        },
        {
            "name": "Retrieve Document",
            "request": {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "resources/read",
                "params": {
                    "uri": "file://README.md"
                }
            }
        },
    ]
    
    for example in example_requests:
        print(f"\n{example['name']}:")
        print("Request:")
        print(json.dumps(example['request'], indent=2))
        print("\nResponse Format:")
        print(json.dumps({
            "jsonrpc": "2.0",
            "id": example['request']['id'],
            "result": "[response data]"
        }, indent=2))
    
    print("\n✅ JSON-RPC examples shown")
    print("\nLearning Point:")
    print("  MCP clients communicate via standard JSON-RPC protocol.")
    print("  Servers expose methods like resources/list, tools/call, resources/read.")
    print("  All communication is request/response with structured JSON.")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("LESSON 5.3: YOUR FIRST MCP SERVER - PERSONAL KNOWLEDGE SERVER")
    print("=" * 70)
    print("\nThis lesson demonstrates how to build a reusable MCP server template")
    print("that exposes local files and documents for AI client access.\n")
    
    # Run all demonstrations
    demo_resource_discovery()
    print("\n" + "-" * 70 + "\n")
    
    demo_tool_invocation()
    print("\n" + "-" * 70 + "\n")
    
    demo_jsonrpc_protocol()
    
    print("\n" + "=" * 70)
    print("LESSON COMPLETE")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("  1. MCPServer manages resources (documents) and tools (functions)")
    print("  2. Resources are discovered and read by clients via URIs")
    print("  3. Tools are callable handlers with structured input schemas")
    print("  4. Communication uses JSON-RPC 2.0 protocol")
    print("  5. create_knowledge_server() is a reusable template you can adapt\n")
    print("Next Lesson:")
    print("  Lesson 5.4 connects real-world tools (like email) to MCP servers\n")
