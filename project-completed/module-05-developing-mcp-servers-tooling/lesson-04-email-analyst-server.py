"""
Lesson 5.4: Connecting Real-World Tools - Email Analyst Server

Build an MCP server that can read emails, categorize, identify action items,
and generate summaries for workflow automation.

Run: python lesson-04-email-analyst-server.py
"""

import json
from shared.mcp_server import MCPServer, Tool
from shared.tools import EmailTools, TextTools
from shared.registry import ServiceRegistry, ToolInfo


def create_email_analyst_server():
    """Create email analysis MCP server."""
    print("\n" + "=" * 60)
    print("EMAIL ANALYST SERVER")
    print("=" * 60)

    server = MCPServer("EmailAnalyst", version="1.0.0")
    registry = ServiceRegistry()

    # Define email processing tools
    tools_config = [
        ToolInfo(
            name="parse_email",
            description="Parse and structure email message",
            category="email",
            input_schema={
                "type": "object",
                "properties": {
                    "sender": {"type": "string"},
                    "subject": {"type": "string"},
                    "body": {"type": "string"},
                },
                "required": ["sender", "subject", "body"],
            },
        ),
        ToolInfo(
            name="categorize_email",
            description="Categorize email type",
            category="email",
            input_schema={
                "type": "object",
                "properties": {
                    "subject": {"type": "string"},
                    "body": {"type": "string"},
                },
                "required": ["subject", "body"],
            },
        ),
        ToolInfo(
            name="extract_action_items",
            description="Extract action items from email",
            category="email",
            input_schema={
                "type": "object",
                "properties": {
                    "body": {"type": "string"},
                },
                "required": ["body"],
            },
        ),
    ]

    # Register tools
    for tool_config in tools_config:
        tool = Tool(
            name=tool_config.name,
            description=tool_config.description,
            inputSchema=tool_config.input_schema,
        )

        if tool_config.name == "parse_email":
            handler = lambda sender, subject, body: json.dumps(
                EmailTools.parse_email(sender, subject, body)
            )
        elif tool_config.name == "categorize_email":
            handler = lambda subject, body: EmailTools.categorize_email(subject, body)
        elif tool_config.name == "extract_action_items":
            handler = lambda body: json.dumps(EmailTools.identify_action_items(body))

        server.register_tool(tool, handler)
        registry.tools.register(tool_config, handler)

    print(f"\n✅ Registered {len(tools_config)} email tools")
    return server, registry


def demo_email_processing():
    """Demonstrate email analysis."""
    print("\n" + "=" * 60)
    print("EMAIL PROCESSING DEMO")
    print("=" * 60)

    server, registry = create_email_analyst_server()

    # Sample email
    email = {
        "sender": "boss@company.com",
        "subject": "Project Update Needed",
        "body": """Hi,

Please provide an update on the following:
- Status of RAG implementation
- Timeline for Module 4 completion
- Any blockers you're facing

Also, we have a meeting on Friday at 2pm to discuss progress.

Thanks,
Manager""",
    }

    print(f"\nProcessing email from: {email['sender']}")
    print(f"Subject: {email['subject']}")

    # Parse email
    parsed = server.call_tool("parse_email", email)
    print(f"\nParsed: {parsed}")

    # Categorize
    category = server.call_tool(
        "categorize_email",
        {"subject": email["subject"], "body": email["body"]},
    )
    print(f"Category: {category}")

    # Extract action items
    items = server.call_tool("extract_action_items", {"body": email["body"]})
    print(f"Action Items: {items}")


def demo_email_workflow():
    """Demonstrate email workflow automation."""
    print("\n" + "=" * 60)
    print("EMAIL WORKFLOW AUTOMATION")
    print("=" * 60)

    print("""
Workflow: Automated Email Processing

1. Incoming email detected
2. System parses email using parse_email tool
3. Categorizes using categorize_email tool
4. Extracts action items using extract_action_items
5. Routes to appropriate handler:
   - meeting_request → Calendar integration
   - support_request → Ticket system
   - status_report → Archive
   - general → Inbox

6. AI assistant can review and summarize
7. User gets action items in task list
    """)


def main():
    """Run demonstrations."""
    print("\n" + "🚀 LESSON 5.4: EMAIL ANALYST SERVER".center(60, "="))

    try:
        demo_email_processing()
        demo_email_workflow()

        print("\n" + "=" * 60)
        print("✅ Email Analyst demonstrations complete!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
