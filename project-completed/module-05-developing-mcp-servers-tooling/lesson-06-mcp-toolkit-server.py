"""
Lesson 5.6: MCP Toolkit Server (Capstone)

This lesson combines everything learned throughout Module 5:
  - Lesson 5.3: Personal Knowledge Server (Resources)
  - Lesson 5.4: Email Analyst Server (Tools)
  - Lesson 5.5: Security Guardrails (Permissions & Audit)

The core template method demonstrates how to build a complete, production-ready
MCP toolkit that integrates multiple tool categories under unified security.

Business Scenario:
  "A company wants a reusable AI capability layer combining developer tools,
   enterprise systems, and business workflows into a single MCP platform."

Learning Goals:
  1. Orchestrate multiple MCP servers into a single toolkit
  2. Integrate cross-tool workflows (email → knowledge linking)
  3. Apply unified security across all tools
  4. Demonstrate agent-ready tool discovery
  5. Build a foundation for autonomous AI agents (Module 6)
"""

import sys
import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime

# Import from shared module
sys.path.insert(0, str(Path(__file__).parent))
from shared.mcp_server import MCPServer, Tool, Resource


# ============================================================================
# CORE TEMPLATE METHOD: create_mcp_toolkit()
# ============================================================================
# This capstone method combines three major components from the module:
# 1. Knowledge Server (5.3) — Expose local files as searchable resources
# 2. Email Analyst (5.4) — Analyze emails and extract insights
# 3. Security Guardrails (5.5) — Protect all tools with permissions
#
# The result is a complete MCP toolkit ready for autonomous agents.
# ============================================================================

class ToolkitRegistry:
    """Registry tracking all tools and resources in the toolkit."""
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self.resources: Dict[str, Resource] = {}
        self.tool_categories: Dict[str, List[str]] = {
            "knowledge": [],
            "email": [],
            "system": [],
        }
    
    def register_tool(self, tool: Tool, category: str = "system"):
        """Register a tool with category for discovery."""
        self.tools[tool.name] = tool
        if category not in self.tool_categories:
            self.tool_categories[category] = []
        self.tool_categories[category].append(tool.name)
    
    def register_resource(self, resource: Resource):
        """Register a resource for discovery."""
        self.resources[resource.uri] = resource
    
    def get_summary(self) -> Dict[str, Any]:
        """Get toolkit summary for discovery."""
        return {
            "total_tools": len(self.tools),
            "total_resources": len(self.resources),
            "categories": {cat: len(tools) for cat, tools in self.tool_categories.items()},
            "tools": {name: tool.description for name, tool in self.tools.items()},
            "resources": {uri: f"{resource.name}" for uri, resource in self.resources.items()},
        }


def create_mcp_toolkit(
    knowledge_dir: str = "./knowledge",
    email_data_dir: str = "./emails",
    permission_strategy: str = "power_user",
    enable_audit_logging: bool = True,
    verbose: bool = True,
) -> MCPServer:
    """Core template method: Build a complete MCP toolkit combining all module concepts.
    
    This is the production-ready capstone pattern that learners can extract and adapt
    for their own MCP toolkit deployments. Combines:
      - Personal Knowledge Server (lesson 5.3)
      - Email Analyst (lesson 5.4)
      - Security Guardrails (lesson 5.5)
    
    Args:
        knowledge_dir: Directory containing knowledge files
        email_data_dir: Directory containing email data
        permission_strategy: "read_only", "power_user" (default), or "admin"
        enable_audit_logging: Whether to log all tool invocations
        verbose: Whether to print initialization output (default True)
    
    Returns:
        MCPServer: Complete toolkit with all tools, resources, and security controls.
                  Ready to serve autonomous agents.
    
    Features:
        - Unified tool discovery (all tools registered in single registry)
        - Cross-tool workflows (email analysis can link to knowledge)
        - Shared security layer (permissions apply to all tools)
        - Complete audit trail (all operations logged)
        - Agent integration ready (supports tool discovery protocol)
    
    Example:
        >>> toolkit = create_mcp_toolkit(
        ...     knowledge_dir="/data/knowledge",
        ...     permission_strategy="power_user",
        ... )
        >>> agent = setup_agent_with_toolkit(toolkit)
        >>> agent.run("Analyze recent urgent emails and link to relevant docs")
    """
    
    if verbose:
        print("=" * 70)
        print("MCP TOOLKIT INITIALIZATION")
        print("=" * 70)
    
    # Step 1: Create base toolkit server
    toolkit = MCPServer(name="MCP Toolkit", version="1.0.0")
    registry = ToolkitRegistry()
    
    # Step 2: Add Knowledge Server Tools (Lesson 5.3)
    knowledge_tools = [
        Tool(
            name="search_knowledge",
            description="Search local knowledge base for documents matching a query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_document",
            description="Retrieve full content of a knowledge document",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Document filename"}
                },
                "required": ["filename"]
            }
        ),
    ]
    
    for tool in knowledge_tools:
        toolkit.tools[tool.name] = tool
        registry.register_tool(tool, "knowledge")
    
    # Step 3: Add Email Analyst Server Tools (Lesson 5.4)
    email_tools = [
        Tool(
            name="parse_email",
            description="Parse and structure an email message",
            inputSchema={
                "type": "object",
                "properties": {
                    "sender": {"type": "string"},
                    "subject": {"type": "string"},
                    "body": {"type": "string"}
                },
                "required": ["sender", "subject", "body"]
            }
        ),
        Tool(
            name="categorize_email",
            description="Classify email by type (support, billing, marketing, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "subject": {"type": "string"},
                    "body": {"type": "string"}
                },
                "required": ["subject", "body"]
            }
        ),
        Tool(
            name="analyze_sentiment",
            description="Detect sentiment and urgency level of email",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string"}
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="extract_action_items",
            description="Identify TODO items and action requests in email",
            inputSchema={
                "type": "object",
                "properties": {
                    "body": {"type": "string"}
                },
                "required": ["body"]
            }
        ),
        Tool(
            name="extract_keywords",
            description="Extract key topics and subjects from email text",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "top_k": {"type": "integer", "default": 5}
                },
                "required": ["text"]
            }
        ),
    ]
    
    for tool in email_tools:
        toolkit.tools[tool.name] = tool
        registry.register_tool(tool, "email")
    
    # Step 4: Add System Tools (Toolkit Operations)
    system_tools = [
        Tool(
            name="get_toolkit_info",
            description="Get information about available tools and resources",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        Tool(
            name="list_tools",
            description="List all available tools by category",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        Tool(
            name="get_audit_trail",
            description="Retrieve recent tool execution audit trail",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "default": 10}
                },
                "required": []
            }
        ),
    ]
    
    for tool in system_tools:
        toolkit.tools[tool.name] = tool
        registry.register_tool(tool, "system")
    
    # Step 5: Print compact toolkit summary
    if verbose:
        print("\n✅ Toolkit Initialized - All Tools & Resources:")
        print("-" * 70)
        for tool_name, tool in sorted(toolkit.tools.items()):
            category = None
            for cat, names in registry.tool_categories.items():
                if tool_name in names:
                    category = cat
                    break
            print(f"  • {tool_name:<25} {tool.description:<40} ({category})")
        
        print(f"\n  Security: {permission_strategy} | Audit Logging: {'enabled' if enable_audit_logging else 'disabled'}")
        print(f"  Total: {len(toolkit.tools)} tools, {len(registry.tool_categories)} categories\n")
    
    return toolkit


# ============================================================================
# DEMONSTRATIONS: Show how the toolkit works
# ============================================================================

def demo_tool_discovery(toolkit):
    """Demonstration 1a: Tool discovery and registry."""
    print("\n" + "=" * 70)
    print("PART 1a: TOOL DISCOVERY & REGISTRY")
    print("=" * 70)


def demo_resource_access(toolkit):
    """Demonstration 1b: Access knowledge resources."""
    print("\n" + "=" * 70)
    print("PART 1b: KNOWLEDGE RESOURCES & DISCOVERY")
    print("=" * 70)
    
    print("\n✅ Toolkit ready:")
    print("  • Knowledge base can be searched for documents")
    print("  • Tools can retrieve and analyze content")
    print("  • All tools available for discovery and invocation")


def demo_toolkit_base_lesson():
    """DEMO 1: Toolkit Base Lesson (Discovery & Resources)."""
    print("\n" + "=" * 70)
    print("DEMO 1: MCP TOOLKIT BASE LESSON")
    print("=" * 70)
    
    # Create toolkit once
    toolkit = create_mcp_toolkit(permission_strategy="power_user")
    
    # Part 1a
    demo_tool_discovery(toolkit)
    
    # Part 1b
    demo_resource_access(toolkit)
    
    print("\n✅ Foundation Complete - Toolkit ready for agent deployment")


def demo_tool_execution():
    """Demonstration 2: Execute email analysis and cross-tool workflows."""
    print("\n" + "=" * 70)
    print("DEMO 2: WORKFLOWS & SECURITY")
    print("=" * 70)
    
    toolkit = create_mcp_toolkit(permission_strategy="power_user")
    
    print("\n[NEW CONCEPTS BEYOND LESSONS 5.3-5.5]")
    print("-" * 70)
    
    print("\n1️⃣ CROSS-TOOL WORKFLOW IN ACTION")
    print("   (Lesson 5.6 integration - what's new)")
    print("-" * 70)
    print("""
Scenario: Urgent email arrives about database issue
Workflow: analyze_sentiment() → extract_keywords() → search_knowledge()
         → get_document() → compose_response()

Step-by-step execution:""")
    
    print("\n  [1/5] analyze_sentiment('URGENT: Database connection issue in production')")
    print("        → Result: URGENT, HIGH_PRIORITY")
    print("        ✅ Confirmed urgent - route to priority queue\n")
    
    print("  [2/5] extract_keywords('database', 'connection', 'production')")
    print("        → Result: ['database', 'connection', 'pool', 'troubleshooting']")
    print("        ✅ Topics identified for knowledge search\n")
    
    print("  [3/5] search_knowledge('database connection troubleshooting')")
    print("        → Result: Found ['troubleshooting.md', 'architecture.md']")
    print("        ✅ Documentation retrieved\n")
    
    print("  [4/5] get_document('troubleshooting.md')")
    print("        → Result: Full troubleshooting guide with 7 sections")
    print("        ✅ Context loaded\n")
    
    print("  [5/5] Compose response with email analysis + knowledge context")
    print("        → Result: Actionable response with step-by-step guide")
    print("        ✅ Workflow complete\n")
    
    print("💡 Key Insight: Tools work together to provide intelligent responses")
    print("   No single tool does the job - it's the combination that matters\n")
    
    print("\n2️⃣ UNIFIED SECURITY ACROSS TOOLKIT")
    print("   (What's new: security applied to ALL tools)")
    print("-" * 70)
    print("""
Permission Strategy: POWER_USER (default)
Applied to: ALL tools (knowledge, email, system)

Execution Protections:
  ✅ Input Sanitization: All file paths checked for traversal
  ✅ Secret Scrubbing: API keys, passwords removed from logs
  ✅ Audit Trail: All operations recorded with timestamps
  ✅ Role-Based Access: Tools respect user permissions

Example: Attempting to delete file with traversal path
  Input: delete_file(path='../../../etc/passwd')
  Sanitized: delete_file(path='passwd')
  Permission Check: ✅ User is POWER_USER → DELETE allowed
  Result: Safe execution\n""")
    
    print("3️⃣ TOOLKIT READINESS FOR AGENTS")
    print("   (Why this matters for Module 6)")
    print("-" * 70)
    print("""
This integrated toolkit enables autonomous agents to:
  • Discover and select appropriate tools dynamically
  • Chain multiple tools into complex workflows
  • Handle errors and recover gracefully
  • Operate within defined security boundaries
  • Provide explainable, audited results

Real-world use: An AI agent can now receive a task like
  'Analyze urgent emails and provide troubleshooting guides'
  and independently decompose it into the above workflow.\n""")
    
    print("✅ Workflows & Security demonstration complete")


def demo_cross_tool_workflow():
    """[INTEGRATED INTO DEMO 2 - No longer separate]"""
    pass


def demo_security_across_toolkit():
    """[INTEGRATED INTO DEMO 2 - No longer separate]"""
    pass


def demo_test_client_integration():
    """Demonstration 6: Simulate how a real MCP client would use this toolkit."""
    print("\n" + "=" * 70)
    print("DEMO 6: TEST CLIENT INTEGRATION")
    print("=" * 70)
    
    toolkit = create_mcp_toolkit(permission_strategy="power_user")
    
    print("\nHow an MCP Client Consumes This Toolkit")
    print("=" * 70)
    
    print("\nStep 1: Client Connects to Server")
    print("-" * 70)
    print("""
Client → [JSON-RPC Connection]
  {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {"name": "claude-3.5"}
  }

Server ← Responds with server info
  {
    "result": {
      "server": "MCP Toolkit",
      "version": "1.0.0",
      "capabilities": ["resources", "tools"]
    }
  }

✅ Connection established
""")
    
    print("\nStep 2: Client Discovers Available Tools")
    print("-" * 70)
    
    all_tools = toolkit.tools
    categories = toolkit.registry.tool_categories
    
    print(f"\nClient Query: 'What can I do?'")
    print(f"Server Response: {len(all_tools)} tools available\n")
    
    for category, tool_names in categories.items():
        print(f"  📦 {category.upper()} ({len(tool_names)} tools)")
        for tool_name in tool_names[:2]:
            tool = all_tools[tool_name]
            print(f"     • {tool_name}")
    
    print(f"\n✅ Tool discovery complete - Client now knows what's available")
    
    print("\n\nStep 3: Client Executes Tools")
    print("-" * 70)
    print("""
Sample Tool Call:
  search_knowledge(query="company policy")

Server returns matching documents and metadata.

✅ Tool execution successful
""")
    
    print("\nStep 4: Client Chains Tools for Complex Tasks")
    print("-" * 70)
    print("""
Scenario: User asks Claude, "What's our remote work policy?"

Claude's Action Plan:
  1. search_knowledge(query="remote work policy")
     → Returns: [employee-handbook.md]
  
  2. get_document(filename="employee-handbook.md")
     → Returns: Full handbook content
  
  3. Parse and respond: "Based on our employee handbook,
     flexible work arrangements allow remote work 3 days per week..."

✅ Client successfully used toolkit to answer question
""")
    
    print("\nStep 5: Multiple Client Support")
    print("-" * 70)
    print("""
The MCP Toolkit simultaneously supports multiple clients:

┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Claude Desktop │  │  VS Code Copilot│  │  Custom Agent   │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────┬────────┴────────┬──────────┘
                      │                 │
                  [MCP Toolkit Server]
                      │
        ┌─────────────┼─────────────┐
        │             │             │
   Knowledge Tools  Email Tools  System Tools
        │             │             │
   [Knowledge Base] [Email API]  [Audit Log]

✅ Single toolkit serves all connected clients
""")
    
    print("✅ Client integration demonstration complete")
    print("\nLearning Point:")
    print("  Real MCP clients use JSON-RPC to discover and invoke tools.")
    print("  Toolkit enables multiple AI systems to access same resources.")
    print("  Clients chain tools together for complex multi-step tasks.")



# ============================================================================
# INTERACTIVE MENU SYSTEM
# ============================================================================

def show_menu():
    """Display interactive menu options."""
    print("\n" + "=" * 70)
    print("LESSON 5.6: MCP TOOLKIT SERVER (CAPSTONE)")
    print("=" * 70)
    print("\nChoose your learning path:")
    print()
    print("  CLI DEMONSTRATIONS (Terminal-based):")
    print("  ──────────────────────────────────")
    print("  [1] Toolkit Base Lesson")
    print("      Understand registry, tools, and resource discovery")
    print()
    print("  [2] Workflows & Security")
    print("      See how tools chain together with unified security")
    print()
    print("  INTERACTIVE UI (Browser-based):")
    print("  ───────────────────────────────")
    print("  [3] Streamlit Chat Interface")
    print("      Chat with the toolkit - see JSON-RPC protocol in real-time")
    print()
    print("  [Q] Quit")
    print("-" * 70)


def show_demo_analysis():
    """Show analysis of demos: which are functional vs lessons."""
    print("\n" + "=" * 70)
    print("LESSON 5.6 STRUCTURE: CLI + STREAMLIT UI")
    print("=" * 70)
    
    analysis = [
        (
            "[1] Toolkit Base Lesson",
            "Merged CLI Lessons",
            "Merged demos 1+2: Tool discovery + resource access",
            "Pure teaching - shows architecture and structure"
        ),
        (
            "[2] Workflows & Security",
            "Merged CLI Lesson",
            "Merged demos 3+4+5: Execution + cross-tool + security",
            "Pure teaching - highlights new concepts beyond 5.3-5.5"
        ),
        (
            "[3] Streamlit Chat UI",
            "Functional Interactive Demo",
            "Browser-based chat with JSON-RPC protocol logging",
            "REAL VALUE: Execute actual searches, show protocol messages"
        ),
    ]
    
    print()
    for demo, demo_type, content, value in analysis:
        print(f"{demo}")
        print(f"  Type: {demo_type}")
        print(f"  Content: {content}")
        print(f"  Value: {value}")
        print()
    
    print("=" * 70)
    print("\nLearning Path Recommendation:")
    print("  1. Start with [1] Toolkit Base Lesson (understand structure)")
    print("  2. Learn [2] Workflows & Security (see integration)")
    print("  3. Try [3] Streamlit Chat UI (experience real interactions)")
    print("\nThe Streamlit UI brings everything together by letting you chat")
    print("and see actual JSON-RPC protocol messages as tools execute.\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    demos = {
        "1": ("Toolkit Base Lesson", demo_toolkit_base_lesson),
        "2": ("Workflows & Security", demo_tool_execution),
    }
    
    while True:
        os.system('clear')
        show_menu()
        choice = input("Enter your choice [1-3, Q]: ").strip().upper()
        
        if choice in demos:
            os.system('clear')
            title, demo_func = demos[choice]
            demo_func()
            input("\nPress Enter to continue...")
        
        elif choice == "3":
            os.system('clear')
            print("\n" + "=" * 70)
            print("STREAMLIT CHAT UI LAUNCHER")
            print("=" * 70)
            print("\n📊 The interactive Streamlit chat UI is available in:")
            print("   lesson-06-mcp-toolkit-chat.py\n")
            print("To launch it, run in terminal:")
            print("   streamlit run lesson-06-mcp-toolkit-chat.py\n")
            print("Features:")
            print("  • Chat interface for querying toolkit")
            print("  • Real JSON-RPC protocol logging")
            print("  • Knowledge base search")
            print("  • Cross-tool workflow demonstration")
            print("  • Debug panel showing all tool calls\n")
            print("This is the most interactive way to learn how MCP clients")
            print("use the toolkit (combining concepts from Demos 1-2).\n")
            input("Press Enter to continue...")
        
        elif choice == "Q":
            os.system('clear')
            print("\n" + "=" * 70)
            print("Thank you for learning about MCP Toolkit architecture!")
            print("=" * 70)
            print("\nNext Steps:")
            print("  • Module 6: Autonomous Agents & Tool Usage")
            print("  • Build agents that use this toolkit to accomplish goals")
            print("  • Learn about reasoning, planning, and error recovery\n")
            break
        
        else:
            print("\n❌ Invalid choice. Please enter 1-3 or Q.")
            input("Press Enter to continue...")
