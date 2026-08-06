"""
Lesson 5.3: Your First MCP Server - Personal Knowledge Server

Build a local MCP server that exposes files and documents as resources,
with tools for searching and retrieving knowledge base content.

This lesson demonstrates the core create_knowledge_server() template method
that learners can reuse in their own projects with minimal configuration changes.

Run:
    python lesson-03-personal-knowledge-server.py
    
    To see actual JSON-RPC requests/responses in debug output:
    export DEBUG_JSONRPC=1 && python lesson-03-personal-knowledge-server.py
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional
import tempfile
import uuid

# Import from shared module (reference path)
sys.path.insert(0, str(Path(__file__).parent))
from shared.mcp_server import MCPServer, Resource, Tool
from shared.resources import FileResource


# ============================================================================
# CONFIGURATION: Customize knowledge directory and options
# ============================================================================

# Primary knowledge directory (project folder by default)
KNOWLEDGE_DIR = str(Path(__file__).parent.parent.parent / "datasets")

# Optional: Use a temporary directory for user uploads/testing
# Uncomment below to enable, or set ENABLE_TEMP_DIR to True
# KNOWLEDGE_DIR = "/tmp/mcp_knowledge"  # or tempfile.mkdtemp(prefix="mcp_knowledge_")

# Flag to auto-create temporary directory (disabled by default)
# If True, creates KNOWLEDGE_DIR if it doesn't exist
ENABLE_TEMP_DIR = False

# File extensions to index
FILE_EXTENSIONS = ['.md', '.txt', '.py', '.json']

# Test queries for demo tool invocation (relevant to sample documents)
# Customize these to match your domain knowledge (e.g., "policy", "employee", "process")
TEST_QUERIES = [
    "policy",        # Will match policy-related content
    "employee",      # Will match employee documentation
    "procedure",     # Will match procedure guides
]


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def clear_screen():
    """Clear terminal screen."""
    os.system("clear" if os.name == "posix" else "cls")


def initialize_knowledge_dir():
    """Initialize knowledge directory, with optional temp directory creation."""
    knowledge_path = Path(KNOWLEDGE_DIR)
    
    # If using temp directory and flag is enabled, create it
    if ENABLE_TEMP_DIR and not knowledge_path.exists():
        try:
            knowledge_path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created knowledge directory: {KNOWLEDGE_DIR}")
            return True
        except Exception as e:
            print(f"⚠ Could not create directory {KNOWLEDGE_DIR}: {e}")
            print(f"  Using existing directory if available")
            return knowledge_path.exists()
    
    # Check if directory exists
    if not knowledge_path.exists():
        print(f"⚠ Knowledge directory does not exist: {KNOWLEDGE_DIR}")
        print(f"  Demos will use default sample documents.")
        return False
    
    return True


def show_menu():
    """Display main menu."""
    clear_screen()
    print("\n" + "=" * 70)
    print("🚀 LESSON 5.3: YOUR FIRST MCP SERVER - PERSONAL KNOWLEDGE SERVER".center(70))
    print("=" * 70)
    print()
    print("  Choose a pattern to learn:\n")
    print("    [1] PATTERN: Core MCP Server Initialization")
    print("        → Create server, register resources and tools\n")
    print("    [2] PATTERN: Resource Discovery & Access")
    print("        → List and read documents from knowledge base\n")
    print("    [3] PATTERN: Tool Invocation & Search")
    print("        → Execute tools, search knowledge, retrieve stats\n")
    print("    [4] PATTERN: JSON-RPC in Action (DEBUG MODE)")
    print("        → See actual JSON-RPC protocol messages\n")
    print("    [Q] Quit\n")
    print("=" * 70)


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

def demo_core_method(full_print_output=True):
    """Demonstration 1: Core server initialization and setup.
    
    Args:
        full_print_output: If True, show full initialization details.
                          If False, show minimal output (used by other demos).
    """
    if full_print_output:
        print("\n" + "=" * 70)
        print("DEMO 1: CORE TEMPLATE METHOD - create_knowledge_server()")
        print("=" * 70)
    
    # Use KNOWLEDGE_DIR if it exists, otherwise create temporary directory for demo
    knowledge_path = Path(KNOWLEDGE_DIR)
    
    if knowledge_path.exists() and list(knowledge_path.glob("*")):
        # Use existing knowledge directory
        demo_dir = str(knowledge_path)
        if full_print_output:
            print(f"\nUsing knowledge directory: {demo_dir}")
    else:
        # Create temporary knowledge directory for demo
        demo_dir = tempfile.mkdtemp(prefix="knowledge_")
        if full_print_output:
            print(f"\nUsing temporary demo directory: {demo_dir}")
        
        # Only create sample documents if ENABLE_TEMP_DIR is True
        if ENABLE_TEMP_DIR:
            # Create sample documents
            sample_docs = [
                ("employee-handbook.md", """# Employee Handbook

## Company Policy
Welcome to our organization!

## Work Policy
- Flexible work hours
- Remote work allowed 3 days/week
- Professional development budget

## Employee Benefits
- Health insurance
- 401k matching
- Paid time off
"""),
            ("procedures.md", """# Standard Operating Procedures

## Onboarding Procedure
1. First day orientation
2. Equipment setup
3. Team introduction
4. Project assignment

## Employee Review Process
- Quarterly check-ins
- Annual performance review
- Development planning
"""),
            ("faq.txt", """FAQ - Frequently Asked Questions

Q: What is the policy for remote work?
A: Employees can work remotely up to 3 days per week.

Q: How do I request time off?
A: Submit requests via the HR portal at least 2 weeks in advance.

Q: What employee development opportunities exist?
A: We offer training budgets and tuition reimbursement.
"""),
        ]
            
            for filename, content in sample_docs:
                filepath = os.path.join(demo_dir, filename)
                with open(filepath, 'w') as f:
                    f.write(content)
    
    # Initialize server using the template method
    server = create_knowledge_server(
        knowledge_dir=demo_dir,
        server_name="DemoKnowledge",
        file_extensions=FILE_EXTENSIONS
    )
    
    if full_print_output:
        print(f"\n✅ Server initialized successfully")
        print(f"   Server: {server.name} v{server.version}")
        print(f"   Knowledge Dir: {demo_dir}")
    else:
        print(f"✅ Server initialized")
    
    return server, demo_dir


def demo_resource_discovery():
    """Demonstration 2: Discover registered resources."""
    print("\n" + "=" * 70)
    print("DEMO 2: RESOURCE DISCOVERY")
    print("=" * 70)
    
    server, temp_dir = demo_core_method(full_print_output=False)
    
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


def demo_tool_invocation(full_print_output=True):
    """Demonstration 3: Execute tools via the server.
    
    Args:
        full_print_output: If True, show full headers and details.
                          If False, show minimal output (used by other demos).
    """
    if full_print_output:
        print("\n" + "=" * 70)
        print("DEMO 3: TOOL INVOCATION")
        print("=" * 70)
    
    server, temp_dir = demo_core_method(full_print_output=False)
    
    # Check if DEBUG_JSONRPC is enabled
    debug_jsonrpc = os.environ.get('DEBUG_JSONRPC', '').lower() == '1'
    
    print("\nAvailable Tools:")
    print("-" * 70)
    
    tools = server.list_tools()
    for i, tool in enumerate(tools, 1):
        print(f"{i}. {tool['name']}")
    
    if full_print_output:
        print("\nExecuting Tool: search_knowledge")
        print("-" * 70)
        print(f"\nTest Queries (configured at top of file):")
        print(f"  TEST_QUERIES = {TEST_QUERIES}\n")
    else:
        print("\nExecuting searches with DEBUG_JSONRPC enabled:")
        print("-" * 70 + "\n")
    
    if debug_jsonrpc:
        print("[DEBUG_JSONRPC ENABLED - Showing actual JSON-RPC protocol]")
        print("-" * 70)
    
    for query in TEST_QUERIES:
        try:
            # Construct JSON-RPC request
            jsonrpc_request = {
                "jsonrpc": "2.0",
                "id": str(uuid.uuid4())[:8],
                "method": "tools/call",
                "params": {
                    "name": "search_knowledge",
                    "arguments": {"query": query}
                }
            }
            
            # Show JSON-RPC request if debug enabled
            if debug_jsonrpc:
                print(f"\n→ CLIENT REQUEST (JSON-RPC):")
                print(json.dumps(jsonrpc_request, indent=2))
            
            # Execute tool
            result = server.tool_handlers['search_knowledge'](query=query)
            result_data = json.loads(result)
            
            # Construct JSON-RPC response
            jsonrpc_response = {
                "jsonrpc": "2.0",
                "id": jsonrpc_request["id"],
                "result": result_data
            }
            
            # Show JSON-RPC response if debug enabled
            if debug_jsonrpc:
                print(f"\n← SERVER RESPONSE (JSON-RPC):")
                print(json.dumps(jsonrpc_response, indent=2))
            
            # Show human-readable results
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
    if debug_jsonrpc:
        print("  JSON-RPC protocol shows request/response structure for tool calls.")
        print("  Real MCP clients use this protocol to communicate with servers.")





def pattern_1_core_method():
    """PATTERN 1: Core MCP Server Initialization."""
    print("\n" + "=" * 70)
    print("PATTERN 1: CORE MCP SERVER INITIALIZATION")
    print("=" * 70)
    demo_core_method()
    input("\nPress Enter to continue...")


def pattern_2_resource_discovery():
    """PATTERN 2: Resource Discovery & Access."""
    print("\n" + "=" * 70)
    print("PATTERN 2: RESOURCE DISCOVERY & ACCESS")
    print("=" * 70)
    demo_resource_discovery()
    input("\nPress Enter to continue...")


def pattern_3_tool_invocation():
    """PATTERN 3: Tool Invocation & Search."""
    print("\n" + "=" * 70)
    print("PATTERN 3: TOOL INVOCATION & SEARCH")
    print("=" * 70)
    demo_tool_invocation(full_print_output=True)
    input("\nPress Enter to continue...")


def pattern_4_jsonrpc_debug():
    """PATTERN 4: JSON-RPC in Action (DEBUG MODE)."""
    print("\n" + "=" * 70)
    print("PATTERN 4: JSON-RPC IN ACTION (DEBUG MODE)")
    print("=" * 70)
    print("\n⚙️  Enabling DEBUG_JSONRPC mode...")
    print("This will show actual JSON-RPC request/response messages\n")
    
    # Enable debug mode
    os.environ['DEBUG_JSONRPC'] = '1'
    
    # Run tool invocation demo with debug output
    demo_tool_invocation(full_print_output=True)
    
    input("\nPress Enter to continue...")


def main():
    """Main interactive menu loop."""
    # Initialize knowledge directory
    initialize_knowledge_dir()
    
    patterns = {
        "1": pattern_1_core_method,
        "2": pattern_2_resource_discovery,
        "3": pattern_3_tool_invocation,
        "4": pattern_4_jsonrpc_debug,
    }

    while True:
        show_menu()
        choice = input("Choose [1-4] or [Q] to quit: ").strip().lower()

        if choice == "q":
            clear_screen()
            print("\n✅ Thanks for learning! Remember to:")
            print("   • Use create_knowledge_server() as your MCP template")
            print("   • Register resources (documents) and tools (functions)")
            print("   • Connect via MCP client: Claude Desktop, or other AI clients")
            print("   • All communication uses standard JSON-RPC 2.0 protocol")
            print("\nMCP Clients that can use this server:")
            print("   • Claude Desktop (with MCP integration)")
            print("   • Any LLM client implementing MCP protocol")
            print("   • Not directly used by chat interfaces - it's a backend server")
            print("\n")
            break

        if choice in patterns:
            try:
                patterns[choice]()
            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupted. Returning to menu.\n")
            except Exception as e:
                clear_screen()
                print(f"\n❌ Error: {e}\n")
                import traceback
                traceback.print_exc()
            finally:
                input("\nPress Enter to return to menu...")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    main()
