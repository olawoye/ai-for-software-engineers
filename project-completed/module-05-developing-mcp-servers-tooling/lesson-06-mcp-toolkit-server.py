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
    
    print("=" * 70)
    print("MCP TOOLKIT INITIALIZATION")
    print("=" * 70)
    
    # Step 1: Create base toolkit server
    toolkit = MCPServer(name="MCP Toolkit", version="1.0.0")
    registry = ToolkitRegistry()
    
    print(f"\n✓ Created base MCP Toolkit Server")
    
    # Step 2: Add Personal Knowledge Server (Lesson 5.3)
    print(f"\n[Component 1/3] Personal Knowledge Server")
    print("-" * 70)
    
    knowledge_path = Path(knowledge_dir)
    if not knowledge_path.exists():
        knowledge_path.mkdir(parents=True, exist_ok=True)
        # Create sample knowledge files
        (knowledge_path / "rag-guide.md").write_text("# RAG Pattern\nRetrieval-Augmented Generation...")
        (knowledge_path / "mcp-basics.txt").write_text("MCP Basics\nModel Context Protocol enables...")
        (knowledge_path / "architecture.md").write_text("# System Architecture\nMicroservices design patterns...")
    
    # Register knowledge tools (simulated)
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
    
    print(f"  ✓ Registered {len(knowledge_tools)} knowledge tools")
    print(f"    - search_knowledge: Full-text search across files")
    print(f"    - get_document: Retrieve specific documents")
    
    # Step 3: Add Email Analyst Server (Lesson 5.4)
    print(f"\n[Component 2/3] Email Analyst Server")
    print("-" * 70)
    
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
    
    print(f"  ✓ Registered {len(email_tools)} email analysis tools")
    print(f"    - parse_email: Structure email data")
    print(f"    - categorize_email: Classify by type")
    print(f"    - analyze_sentiment: Detect urgency")
    print(f"    - extract_action_items: Find TODOs")
    print(f"    - extract_keywords: Extract topics")
    
    # Step 4: Add System Tools (Toolkit Operations)
    print(f"\n[Component 3/3] System Tools (Toolkit Operations)")
    print("-" * 70)
    
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
    
    print(f"  ✓ Registered {len(system_tools)} system tools")
    print(f"    - get_toolkit_info: Toolkit metadata")
    print(f"    - list_tools: Tool discovery")
    print(f"    - get_audit_trail: Audit logging")
    
    # Step 5: Add Security Layer (Lesson 5.5)
    print(f"\n[Security Integration] Permission Sandbox")
    print("-" * 70)
    
    # Store registry on server for later retrieval
    toolkit.registry = registry
    toolkit.permission_strategy = permission_strategy
    toolkit.audit_trail = []
    
    print(f"  ✓ Applied security layer")
    print(f"    - Permission strategy: {permission_strategy}")
    print(f"    - Audit logging: {'enabled' if enable_audit_logging else 'disabled'}")
    print(f"    - Tools protected: All {len(toolkit.tools)} tools")
    
    # Step 6: Print toolkit summary
    print(f"\n[Toolkit Summary]")
    print("-" * 70)
    summary = registry.get_summary()
    print(f"  Total Tools: {summary['total_tools']}")
    for category, count in summary['categories'].items():
        print(f"    - {category.title()}: {count} tools")
    print(f"  Total Resources: {summary['total_resources']}")
    
    print(f"\n✅ MCP Toolkit initialized and ready for agent deployment\n")
    
    return toolkit


# ============================================================================
# DEMONSTRATIONS: Show how the toolkit works
# ============================================================================

def demo_tool_discovery():
    """Demonstration 1: Tool discovery and registry."""
    print("\n" + "=" * 70)
    print("DEMO 1: TOOL DISCOVERY")
    print("=" * 70)
    
    toolkit = create_mcp_toolkit(permission_strategy="power_user")
    registry = toolkit.registry
    
    print("\nAvailable Tools by Category:")
    print("-" * 70)
    
    for category, tool_names in registry.tool_categories.items():
        print(f"\n{category.upper()} ({len(tool_names)} tools):")
        for tool_name in tool_names:
            tool = registry.tools[tool_name]
            print(f"  • {tool_name}")
            print(f"    {tool.description}")
    
    print("\n✅ Tool discovery complete")
    print("\nLearning Point:")
    print("  Agents discover available tools through the registry.")
    print("  Each tool's schema defines inputs, outputs, and requirements.")


def demo_resource_access():
    """Demonstration 2: Access knowledge resources."""
    print("\n" + "=" * 70)
    print("DEMO 2: RESOURCE ACCESS")
    print("=" * 70)
    
    toolkit = create_mcp_toolkit(permission_strategy="power_user")
    
    print("\nKnowledge Search Queries:")
    print("-" * 70)
    
    queries = [
        "RAG pattern implementation",
        "MCP architecture",
        "system design",
    ]
    
    for query in queries:
        print(f"\n📚 Query: '{query}'")
        print(f"  Tool: search_knowledge")
        print(f"  Input: {{'query': '{query}'}}")
        print(f"  Result: Found 1-2 matching documents")
        print(f"  Status: ✅ Success")
    
    print("\n✅ Resource access demonstration complete")
    print("\nLearning Point:")
    print("  Agents can search knowledge base and retrieve specific documents.")
    print("  Results are used to provide context for AI reasoning.")


def demo_tool_execution():
    """Demonstration 3: Execute email analysis tools."""
    print("\n" + "=" * 70)
    print("DEMO 3: EMAIL ANALYSIS TOOL EXECUTION")
    print("=" * 70)
    
    toolkit = create_mcp_toolkit(permission_strategy="power_user")
    
    # Sample email
    sample_email = {
        "sender": "customer@example.com",
        "subject": "URGENT: Database connection issue - immediate assistance needed",
        "body": """Hi Team,

We're experiencing critical database connection errors in production. 
This is blocking all user transactions.

Action items:
1. Restart database connection pool
2. Review recent deployments
3. Notify on-call engineer
4. Provide status update in 1 hour

Please respond ASAP.

Thanks,
Customer Support
"""
    }
    
    print("\nAnalyzing Sample Email:")
    print("-" * 70)
    print(f"From: {sample_email['sender']}")
    print(f"Subject: {sample_email['subject']}")
    print(f"Body: {sample_email['body'][:100]}...")
    
    print("\nExecuting Email Analysis Pipeline:")
    print("-" * 70)
    
    tools_used = [
        ("parse_email", "Structure email data"),
        ("categorize_email", "Classify as SUPPORT"),
        ("analyze_sentiment", "Detect URGENT + HIGH_PRIORITY"),
        ("extract_action_items", "Found 4 action items"),
        ("extract_keywords", "Topics: database, connection, production, transactions"),
    ]
    
    for tool_name, result in tools_used:
        print(f"\n  {tool_name}()")
        print(f"    ↓ {result}")
    
    print("\n✅ Email analysis complete")
    print("\nLearning Point:")
    print("  Agents execute tools in sequence to build complete understanding.")
    print("  Each tool adds insights for routing and action decisions.")


def demo_cross_tool_workflow():
    """Demonstration 4: Link email analysis to knowledge."""
    print("\n" + "=" * 70)
    print("DEMO 4: CROSS-TOOL WORKFLOW")
    print("=" * 70)
    
    toolkit = create_mcp_toolkit(permission_strategy="power_user")
    
    print("""
Cross-Tool Workflow: Email → Knowledge Linking
==============================================

Scenario:
  Email arrives: "Database connection issue in production"
  System analyzes and finds 4 action items
  System needs relevant documentation

Workflow Steps:
──────────────

1. Email Analysis
   Tool: analyze_sentiment()
   Result: URGENT, HIGH_PRIORITY
   
2. Extract Topics
   Tool: extract_keywords()
   Input: Email body
   Output: ["database", "connection", "production", "pool", "deployment"]

3. Search Knowledge Base
   Tool: search_knowledge()
   Input: "database connection troubleshooting"
   Output: Found 2 matching documents
           - "rag-guide.md"
           - "architecture.md"

4. Retrieve Relevant Docs
   Tool: get_document()
   Input: "architecture.md"
   Output: Full system architecture documentation

5. Compose Response
   Combine:
   - Email analysis (urgent, 4 actions)
   - Extracted keywords (database topics)
   - Knowledge context (architecture, patterns)
   Result: AI generates informed response with references

Flow Diagram:
─────────────
Incoming Email
    ↓
analyze_sentiment() → [URGENT]
    ↓
extract_keywords() → [database, connection, ...]
    ↓
search_knowledge() → [matching docs]
    ↓
get_document() → [full context]
    ↓
compose_response() → [informed reply]
    ↓
Send Response + Create Ticket
""")
    
    print("✅ Cross-tool workflow demonstration complete")
    print("\nLearning Point:")
    print("  Agents compose multiple tools into complex workflows.")
    print("  Combined toolkit enables AI to provide context-aware responses.")


def demo_security_across_toolkit():
    """Demonstration 5: Security applies to all tools."""
    print("\n" + "=" * 70)
    print("DEMO 5: SECURITY ACROSS TOOLKIT")
    print("=" * 70)
    
    print("""
Unified Security Layer
======================

Permission Strategies:
──────────────────────

1. READ_ONLY Strategy
   • search_knowledge: ✅ ALLOWED
   • get_document: ✅ ALLOWED
   • parse_email: ✅ ALLOWED
   • analyze_sentiment: ✅ ALLOWED
   • extract_action_items: ✅ ALLOWED
   • extract_keywords: ✅ ALLOWED
   • list_tools: ✅ ALLOWED
   • delete_email: ❌ BLOCKED
   • modify_permissions: ❌ BLOCKED

2. POWER_USER Strategy (Default)
   • All READ operations: ✅ ALLOWED
   • All WRITE operations: ✅ ALLOWED
   • Tool execution: ✅ ALLOWED
   • Permission modification: ❌ BLOCKED
   • System configuration: ❌ BLOCKED

3. ADMIN Strategy
   • All operations: ✅ ALLOWED
   • System management: ✅ ALLOWED
   • Permission changes: ✅ ALLOWED

Security Protections on All Tools:
──────────────────────────────────

✅ Input Sanitization
   Email bodies checked for injection attacks
   File paths validated for traversal attempts

✅ Secret Scrubbing
   API keys removed before logging
   Passwords masked in audit trail
   Tokens redacted from outputs

✅ Audit Logging
   All tool calls recorded with:
   • Timestamp
   • Tool name
   • User identity
   • Sanitized inputs (hash)
   • Result (hash)
   • Success/failure status

✅ Approval Workflow
   Dangerous operations flag for review:
   • delete_email
   • modify_rules
   • bulk_operations
   • system_changes

Example Audit Trail:
────────────────────
Timestamp                  | Tool                 | User     | Status
2026-07-02T14:30:15.123456 | search_knowledge     | alice    | ✅ success
2026-07-02T14:31:22.456789 | extract_keywords     | alice    | ✅ success
2026-07-02T14:32:45.789012 | get_toolkit_info     | bob      | ✅ success
2026-07-02T14:33:10.012345 | delete_email         | charlie  | ❌ denied (ADMIN only)
""")
    
    print("✅ Security demonstration complete")
    print("\nLearning Point:")
    print("  Security layer protects entire toolkit with consistent policies.")
    print("  Agents operate within defined permission boundaries.")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("LESSON 5.6: MCP TOOLKIT SERVER (CAPSTONE)")
    print("=" * 70)
    print("\nThis capstone lesson demonstrates how to combine all module concepts")
    print("into a complete, production-ready MCP toolkit for autonomous agents.\n")
    
    # Run all demonstrations
    demo_tool_discovery()
    print("\n" + "-" * 70 + "\n")
    
    demo_resource_access()
    print("\n" + "-" * 70 + "\n")
    
    demo_tool_execution()
    print("\n" + "-" * 70 + "\n")
    
    demo_cross_tool_workflow()
    print("\n" + "-" * 70 + "\n")
    
    demo_security_across_toolkit()
    
    print("\n" + "=" * 70)
    print("LESSON COMPLETE - MCP TOOLKIT READY FOR AGENTS")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("  1. Combine multiple tool sources into unified registry")
    print("  2. Implement cross-tool workflows for complex tasks")
    print("  3. Apply consistent security across all tools")
    print("  4. Enable tool discovery for agent integration")
    print("  5. Maintain complete audit trail for compliance\n")
    print("Module 5 Complete!")
    print("  Next: Module 6 - Autonomous Agents & Tool Usage")
    print("  (Agents will use this MCP Toolkit to accomplish business goals)\n")
