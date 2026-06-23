"""
Lesson 5.6: Mini Project - The MCP Toolkit Server (Capstone)

Combine personal knowledge server, email analyst, and security
into a multi-tool MCP server ready for agent consumption.

Run: python lesson-06-mcp-toolkit-server.py
"""

import json
from shared.mcp_server import MCPServer, Tool, Resource
from shared.resources import FileResource, KnowledgebaseResource
from shared.tools import EmailTools, TextTools, DataTools
from shared.registry import ServiceRegistry, ToolInfo
from shared.permissions import PermissionManager, Role, Permission
from shared.validation import RateLimiter


class MCPToolkit:
    """Complete MCP toolkit combining all modules."""

    def __init__(self):
        self.server = MCPServer("MCPToolkit", version="1.0.0")
        self.registry = ServiceRegistry()
        self.permissions = PermissionManager()
        self.rate_limiter = RateLimiter(max_calls=100, window_seconds=60)

    def setup_knowledge_tools(self):
        """Add knowledge search tools."""
        kb = KnowledgebaseResource()

        # Add sample documents
        kb.add_document(
            "Module Overview",
            "MCP enables AI assistants to access tools and resources securely.",
            {"type": "guide"},
        )

        def search_knowledge(query: str) -> str:
            results = kb.search_documents(query)
            return json.dumps({"results": len(results), "docs": results[:3]})

        tool = Tool(
            name="search_knowledge",
            description="Search knowledge base",
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        )
        self.server.register_tool(tool, search_knowledge)

    def setup_email_tools(self):
        """Add email processing tools."""

        def parse_email(sender: str, subject: str, body: str) -> str:
            result = EmailTools.parse_email(sender, subject, body)
            return json.dumps(result)

        tool = Tool(
            name="parse_email",
            description="Parse email message",
            inputSchema={
                "type": "object",
                "properties": {
                    "sender": {"type": "string"},
                    "subject": {"type": "string"},
                    "body": {"type": "string"},
                },
                "required": ["sender", "subject", "body"],
            },
        )
        self.server.register_tool(tool, parse_email)

    def setup_text_tools(self):
        """Add text analysis tools."""

        def extract_keywords(text: str, top_k: int = 5) -> str:
            keywords = TextTools.extract_keywords(text, top_k)
            return json.dumps({"keywords": keywords})

        tool = Tool(
            name="extract_keywords",
            description="Extract keywords from text",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "top_k": {"type": "number", "default": 5},
                },
                "required": ["text"],
            },
        )
        self.server.register_tool(tool, extract_keywords)

    def get_capabilities(self) -> Dict:
        """Get all capabilities."""
        return {
            "server": self.server.get_server_info(),
            "tools": self.server.list_tools(),
            "resources": self.server.list_resources(),
        }


def demo_toolkit():
    """Demonstrate complete toolkit."""
    print("\n" + "=" * 60)
    print("MCP TOOLKIT SERVER")
    print("=" * 60)

    toolkit = MCPToolkit()
    toolkit.setup_knowledge_tools()
    toolkit.setup_email_tools()
    toolkit.setup_text_tools()

    capabilities = toolkit.get_capabilities()

    print(f"\nServer: {capabilities['server']['name']}")
    print(f"Tools: {len(capabilities['tools'])}")
    print(f"Resources: {len(capabilities['resources'])}")

    print("\nAvailable Tools:")
    for tool in capabilities["tools"]:
        print(f"  • {tool['name']}: {tool['description']}")

    # Demo tool calls
    print("\n" + "=" * 60)
    print("TOOL INVOCATION DEMO")
    print("=" * 60)

    try:
        # Search knowledge
        result = toolkit.server.call_tool(
            "search_knowledge", {"query": "MCP"}
        )
        print(f"\nSearch result: {result}")

        # Parse email
        result = toolkit.server.call_tool(
            "parse_email",
            {
                "sender": "user@example.com",
                "subject": "Meeting tomorrow",
                "body": "Let's discuss the new features.",
            },
        )
        print(f"\nParsed email: {json.loads(result)['sentiment']}")

        # Extract keywords
        result = toolkit.server.call_tool(
            "extract_keywords",
            {"text": "AI assistant helps with tasks and productivity"},
        )
        print(f"\nKeywords: {json.loads(result)['keywords']}")

    except Exception as e:
        print(f"Error: {e}")


def demo_deployment_readiness():
    """Show deployment considerations."""
    print("\n" + "=" * 60)
    print("DEPLOYMENT READINESS")
    print("=" * 60)

    print("""
Checklist for Production MCP Servers:

Configuration ✅
  ☐ Environment variables for secrets
  ☐ Logging configured
  ☐ Error handling in place
  ☐ Resource limits set

Security ✅
  ☐ Permission checks
  ☐ Input validation
  ☐ Rate limiting
  ☐ Audit logging

Testing ✅
  ☐ Unit tests for tools
  ☐ Integration tests
  ☐ Security tests
  ☐ Load testing

Documentation ✅
  ☐ Tool documentation
  ☐ Setup instructions
  ☐ API documentation
  ☐ Example usage

Monitoring ✅
  ☐ Error tracking
  ☐ Performance metrics
  ☐ Uptime monitoring
  ☐ Alert system

Deployment ✅
  ☐ Docker container
  ☐ CI/CD pipeline
  ☐ Rollback plan
  ☐ Scaling strategy
    """)


def main():
    """Run demonstrations."""
    print("\n" + "🚀 LESSON 5.6: MCP TOOLKIT (CAPSTONE)".center(60, "="))

    try:
        demo_toolkit()
        demo_deployment_readiness()

        print("\n" + "=" * 60)
        print("✅ MCP Toolkit demonstrations complete!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
