"""
Lesson 5.3: Your First MCP Server - Personal Knowledge Server

Build a local "Second Brain" MCP server that allows AI assistants
to search project folders, documentation, notes, and saved resources.

Run: python lesson-03-personal-knowledge-server.py
"""

import os
import json
from pathlib import Path
from shared.mcp_server import MCPServer, Resource, Tool
from shared.resources import FileResource, KnowledgebaseResource
from shared.registry import ServiceRegistry


def create_personal_knowledge_server():
    """Create and configure personal knowledge server."""
    print("\n" + "=" * 60)
    print("PERSONAL KNOWLEDGE SERVER")
    print("=" * 60)

    # Initialize server
    server = MCPServer("PersonalKnowledge", version="1.0.0")

    # Setup registry
    registry = ServiceRegistry()

    # Example: File-based resource
    home_dir = str(Path.home())
    docs_path = os.path.join(home_dir, ".knowledge_base")
    file_resource = FileResource(docs_path)

    # Create sample documents
    sample_docs = [
        ("notes.md", "# My Notes\n- TODO: Research RAG systems\n- Completed: Module 3"),
        ("project-ideas.md", "# Project Ideas\n1. AI-powered search\n2. Knowledge bot"),
    ]

    for filename, content in sample_docs:
        try:
            file_resource.write_file(filename, content)
        except:
            pass

    print(f"\n✅ Created knowledge base at: {docs_path}")

    # Register file resources
    for doc_path in file_resource.list_files():
        filename = os.path.basename(doc_path)
        server.register_resource(
            Resource(
                name=filename,
                uri=f"file://{doc_path}",
                description=f"Knowledge document: {filename}",
                mimeType="text/markdown",
            ),
            handler=lambda uri, doc_path=doc_path: file_resource.read_file(
                os.path.basename(doc_path)
            ),
        )

    # Register tools
    def search_documents(query: str) -> str:
        """Search knowledge base."""
        results = []
        for doc_path in file_resource.list_files():
            try:
                content = file_resource.read_file(os.path.basename(doc_path))
                if query.lower() in content.lower():
                    results.append(os.path.basename(doc_path))
            except:
                pass

        return json.dumps({
            "query": query,
            "matches": results,
            "count": len(results),
        })

    search_tool = Tool(
        name="search_knowledge",
        description="Search personal knowledge base",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
            },
            "required": ["query"],
        },
    )

    server.register_tool(search_tool, search_documents)

    # Print server info
    print(f"\nServer: {server.get_server_info()['name']}")
    print(f"Resources: {len(server.list_resources())}")
    print(f"Tools: {len(server.list_tools())}")

    return server


def demo_server_interaction():
    """Demonstrate server capabilities."""
    print("\n" + "=" * 60)
    print("SERVER INTERACTION DEMO")
    print("=" * 60)

    server = create_personal_knowledge_server()

    # List resources
    print("\nAvailable Resources:")
    for resource in server.list_resources():
        print(f"  • {resource['name']}: {resource['description']}")

    # List tools
    print("\nAvailable Tools:")
    for tool in server.list_tools():
        print(f"  • {tool['name']}: {tool['description']}")

    # Execute tool
    print("\nExecuting tool: search_knowledge")
    try:
        result = server.call_tool("search_knowledge", {"query": "TODO"})
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")


def demo_jsonrpc_protocol():
    """Demonstrate JSON-RPC protocol."""
    print("\n" + "=" * 60)
    print("JSON-RPC PROTOCOL")
    print("=" * 60)

    server = create_personal_knowledge_server()

    # Example JSON-RPC requests
    requests = [
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
        },
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "resources/list",
        },
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "search_knowledge",
                "arguments": {"query": "RAG"},
            },
        },
    ]

    print("\nProcessing JSON-RPC requests:")
    for request in requests:
        response = server.handle_jsonrpc(request)
        print(f"\nRequest: {request['method']}")
        print(f"Response: {json.dumps(response, indent=2)[:100]}...")


def main():
    """Run demonstrations."""
    print("\n" + "🚀 LESSON 5.3: YOUR FIRST MCP SERVER".center(60, "="))

    try:
        demo_server_interaction()
        demo_jsonrpc_protocol()

        print("\n" + "=" * 60)
        print("✅ Personal Knowledge Server demonstrations complete!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
