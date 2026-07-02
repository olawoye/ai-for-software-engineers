"""
Lesson 5.4: Connecting Real-World Tools - Email Analyst Server

Build an MCP server that analyzes emails, extracts business intelligence,
and routes messages for action. This lesson demonstrates how MCP enables
AI systems to participate in real business workflows.

This lesson demonstrates the core create_email_analyst_server() template method
that learners can reuse in their own projects for email/messaging integration.

Run:
    python lesson-04-email-analyst-server.py
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# Import from shared module (reference path)
sys.path.insert(0, str(Path(__file__).parent))
from shared.mcp_server import MCPServer, Tool
from shared.tools import EmailTools, TextTools


# ============================================================================
# CORE TEMPLATE METHOD: create_email_analyst_server()
# ============================================================================
# This method is the foundation of email analysis MCP servers.
# It registers tools for parsing, categorizing, and analyzing emails,
# enabling AI systems to integrate email processing into workflows.
#
# Template structure:
#   - Input: server_name
#   - Processing: define tool schemas, register handlers with EmailTools utilities
#   - Output: configured MCPServer ready for email analysis requests
#
# Reusability: Copy this method into your own projects with only:
#   - Email data source configuration (Gmail API, IMAP, webhook, etc.)
#   - Additional analysis tools (sentiment, urgency scoring, etc.)
#   - Custom routing logic for different email types
# ============================================================================

def create_email_analyst_server(
    server_name: str = "EmailAnalyst",
) -> MCPServer:
    """Core template method: Initialize and configure an Email Analysis MCP Server.
    
    This is the production-ready server initialization pattern for email analysis.
    Learners can extract this method and adapt it for their own email sources.
    
    Args:
        server_name: Name of the MCP server (for identification)
    
    Returns:
        MCPServer: Configured server with email analysis tools registered.
        Ready to accept client requests via JSON-RPC.
    
    Features:
        - Parse and structure raw email messages
        - Categorize email types (meeting, support, report, etc.)
        - Extract action items and TODOs
        - Analyze sentiment (positive, negative, neutral)
        - Identify unanswered messages for follow-up
    
    Example:
        >>> server = create_email_analyst_server('MyEmailAnalyzer')
        >>> tools = server.list_tools()  # Discover available analysis tools
        >>> parsed = server.call_tool('parse_email', {
        ...     'sender': 'boss@company.com',
        ...     'subject': 'Status Update',
        ...     'body': 'Please provide updates...'
        ... })
    """
    
    # Step 1: Initialize server
    server = MCPServer(name=server_name, version="1.0.0")
    
    print(f"✓ Initialized {server_name} MCP server")
    
    # Step 2: Define and register parse_email tool
    def parse_email(sender: str, subject: str, body: str) -> str:
        """Parse and structure raw email message.
        
        Args:
            sender: Email sender address
            subject: Email subject line
            body: Email body text
        
        Returns:
            JSON string with parsed email including sentiment
        """
        parsed = EmailTools.parse_email(sender, subject, body)
        return json.dumps(parsed)
    
    parse_tool = Tool(
        name="parse_email",
        description="Parse and structure an email message into components",
        inputSchema={
            "type": "object",
            "properties": {
                "sender": {
                    "type": "string",
                    "description": "Email sender address"
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject line"
                },
                "body": {
                    "type": "string",
                    "description": "Email body text"
                },
            },
            "required": ["sender", "subject", "body"],
        },
    )
    
    server.register_tool(parse_tool, parse_email)
    
    # Step 3: Define and register categorize_email tool
    def categorize_email(subject: str, body: str) -> str:
        """Categorize email type for routing.
        
        Args:
            subject: Email subject line
            body: Email body text
        
        Returns:
            Email category: meeting_request, support_request, status_report, or general
        """
        category = EmailTools.categorize_email(subject, body)
        return json.dumps({
            "category": category,
            "description": _category_descriptions.get(category, "Other email type")
        })
    
    categorize_tool = Tool(
        name="categorize_email",
        description="Classify email type for workflow routing",
        inputSchema={
            "type": "object",
            "properties": {
                "subject": {
                    "type": "string",
                    "description": "Email subject line"
                },
                "body": {
                    "type": "string",
                    "description": "Email body text"
                },
            },
            "required": ["subject", "body"],
        },
    )
    
    server.register_tool(categorize_tool, categorize_email)
    
    # Step 4: Define and register extract_action_items tool
    def extract_action_items(body: str) -> str:
        """Extract action items and TODOs from email.
        
        Args:
            body: Email body text
        
        Returns:
            JSON with list of action items
        """
        items = EmailTools.identify_action_items(body)
        return json.dumps({
            "action_items": items,
            "count": len(items),
            "requires_response": len(items) > 0
        })
    
    action_tool = Tool(
        name="extract_action_items",
        description="Extract action items and TODOs from email body",
        inputSchema={
            "type": "object",
            "properties": {
                "body": {
                    "type": "string",
                    "description": "Email body text"
                },
            },
            "required": ["body"],
        },
    )
    
    server.register_tool(action_tool, extract_action_items)
    
    # Step 5: Define and register analyze_sentiment tool
    def analyze_sentiment(text: str) -> str:
        """Analyze sentiment and urgency of email text.
        
        Args:
            text: Email text to analyze
        
        Returns:
            JSON with sentiment and urgency indicators
        """
        sentiment = EmailTools._analyze_sentiment(text)
        urgency_keywords = ["urgent", "asap", "critical", "immediately", "deadline"]
        is_urgent = any(keyword in text.lower() for keyword in urgency_keywords)
        
        return json.dumps({
            "sentiment": sentiment,
            "is_urgent": is_urgent,
            "priority": "high" if is_urgent else "normal"
        })
    
    sentiment_tool = Tool(
        name="analyze_sentiment",
        description="Analyze sentiment and urgency of email text",
        inputSchema={
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Email text to analyze"
                },
            },
            "required": ["text"],
        },
    )
    
    server.register_tool(sentiment_tool, analyze_sentiment)
    
    # Step 6: Define and register extract_keywords tool
    def extract_keywords(text: str, top_k: int = 5) -> str:
        """Extract important keywords from email.
        
        Args:
            text: Email text to analyze
            top_k: Number of top keywords to return (default: 5)
        
        Returns:
            JSON with keyword list
        """
        keywords = TextTools.extract_keywords(text, top_k)
        return json.dumps({
            "keywords": keywords,
            "count": len(keywords)
        })
    
    keyword_tool = Tool(
        name="extract_keywords",
        description="Extract important keywords from email text",
        inputSchema={
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Email text to analyze"
                },
                "top_k": {
                    "type": "integer",
                    "description": "Number of top keywords to extract (default: 5)",
                    "default": 5
                }
            },
            "required": ["text"],
        },
    )
    
    server.register_tool(keyword_tool, extract_keywords)
    
    print(f"✓ Registered {len(server.list_tools())} email analysis tools")
    
    return server


# Helper mapping for category descriptions
_category_descriptions = {
    "meeting_request": "Email requesting or scheduling a meeting",
    "support_request": "Email asking for help or reporting an issue",
    "status_report": "Email providing updates or reports",
    "general": "General email with no specific category",
}


# ============================================================================
# DEMONSTRATIONS: Show how the template works
# ============================================================================

def demo_tool_registration():
    """Demonstration 1: Tool registration and schemas."""
    print("\n" + "=" * 70)
    print("DEMO 1: TOOL REGISTRATION")
    print("=" * 70)
    
    server = create_email_analyst_server("DemoEmailAnalyst")
    
    print("\nRegistered Email Analysis Tools:")
    print("-" * 70)
    
    tools = server.list_tools()
    for i, tool in enumerate(tools, 1):
        print(f"{i}. {tool['name']}")
        print(f"   Description: {tool['description']}")
        print(f"   Input Schema: {json.dumps(tool['inputSchema']['properties'], indent=6)}")
        print()
    
    print(f"✅ Total tools: {len(tools)}")
    print("\nLearning Point:")
    print("  Each tool has a strict input schema that defines expected parameters.")
    print("  AI clients use schemas to understand how to call tools correctly.")


def demo_email_analysis():
    """Demonstration 2: Analyze a complex email through the pipeline."""
    print("\n" + "=" * 70)
    print("DEMO 2: EMAIL ANALYSIS PIPELINE")
    print("=" * 70)
    
    server = create_email_analyst_server("DemoEmailAnalyst")
    
    # Complex sample email
    email = {
        "sender": "customer@external.com",
        "subject": "URGENT: Critical Issue with RAG Implementation",
        "body": """Hi,

We're experiencing a critical issue with the RAG system that's affecting production.

Action items:
- Investigate embedding quality degradation
- Check vector database performance
- Review retrieval scoring logic
- Contact the support team about database limits

The system was working fine last week. Something changed in the latest deployment.

We need this resolved ASAP as it's impacting our customer-facing features.

Please let me know what you can do.

Thanks,
Customer Support Team""",
    }
    
    print(f"\nAnalyzing email from: {email['sender']}")
    print(f"Subject: {email['subject']}\n")
    
    # Parse email
    print("Step 1: Parse Email")
    print("-" * 70)
    parsed_result = server.tool_handlers['parse_email'](
        sender=email['sender'],
        subject=email['subject'],
        body=email['body']
    )
    parsed = json.loads(parsed_result)
    print(f"Parsed: {json.dumps(parsed, indent=2)}")
    
    # Categorize
    print("\nStep 2: Categorize")
    print("-" * 70)
    category_result = server.tool_handlers['categorize_email'](
        subject=email['subject'],
        body=email['body']
    )
    category = json.loads(category_result)
    print(f"Category: {category['category']}")
    print(f"Description: {category['description']}")
    
    # Analyze sentiment
    print("\nStep 3: Analyze Sentiment")
    print("-" * 70)
    sentiment_result = server.tool_handlers['analyze_sentiment'](
        text=email['body']
    )
    sentiment = json.loads(sentiment_result)
    print(f"Sentiment: {sentiment['sentiment']}")
    print(f"Urgent: {sentiment['is_urgent']}")
    print(f"Priority: {sentiment['priority']}")
    
    # Extract action items
    print("\nStep 4: Extract Action Items")
    print("-" * 70)
    actions_result = server.tool_handlers['extract_action_items'](
        body=email['body']
    )
    actions = json.loads(actions_result)
    print(f"Action Items ({actions['count']}):")
    for item in actions['action_items']:
        print(f"  • {item}")
    
    # Extract keywords
    print("\nStep 5: Extract Keywords")
    print("-" * 70)
    keywords_result = server.tool_handlers['extract_keywords'](
        text=email['body'],
        top_k=5
    )
    keywords = json.loads(keywords_result)
    print(f"Top Keywords: {', '.join(keywords['keywords'])}")
    
    print("\n✅ Email analysis complete")
    print("\nLearning Point:")
    print("  Tools work together in a pipeline to extract business intelligence.")
    print("  AI clients can orchestrate tools to build complex workflows.")


def demo_business_workflow():
    """Demonstration 3: Email workflow routing."""
    print("\n" + "=" * 70)
    print("DEMO 3: EMAIL WORKFLOW ROUTING")
    print("=" * 70)
    
    print("""
Business Workflow: Automated Email Triage
========================================

When an email arrives, the system:

1. PARSE → Structure and timestamp the message
2. CATEGORIZE → Determine email type (meeting, support, report, general)
3. ANALYZE SENTIMENT → Check urgency and tone
4. EXTRACT ITEMS → Find action items and TODOs
5. ROUTE → Dispatch to appropriate handler:

   ├─ URGENT + SUPPORT → Escalate to senior support agent
   ├─ MEETING REQUEST → Add to calendar, send confirmation
   ├─ STATUS REPORT → Archive and notify stakeholders
   ├─ HIGH PRIORITY + ACTION ITEMS → Create tickets
   └─ GENERAL → File for later review

Example Flow:
─────────────

Email: "URGENT: Production issue - RAG system down"
  ├─ Category: SUPPORT_REQUEST
  ├─ Sentiment: NEGATIVE
  ├─ Urgency: HIGH
  ├─ Action Items: 3 (investigate, fix, notify)
  └─ Route: → ESCALATE TO ENGINEERING LEAD
     └─ Create incident ticket with priority P1
        └─ Notify on-call engineer
           └─ Attach relevant logs and context

This workflow runs without human intervention, but can pause
for human confirmation on sensitive actions like escalation.

Integration with Module 6:
──────────────────────────

These tools become capabilities in the MCP Toolkit, which
autonomous agents in Module 6 can access to build complex
multi-step workflows combining email, knowledge bases, and
external systems.
""")
    
    print("\n✅ Workflow overview complete")
    print("\nLearning Point:")
    print("  MCP tools enable AI systems to participate as operational actors.")
    print("  Combined with security guardrails (Lesson 5.5), this scales workflows.")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("LESSON 5.4: CONNECTING REAL-WORLD TOOLS - EMAIL ANALYST SERVER")
    print("=" * 70)
    print("\nThis lesson demonstrates how to build email analysis capabilities")
    print("into MCP servers for business workflow integration.\n")
    
    # Run all demonstrations
    demo_tool_registration()
    print("\n" + "-" * 70 + "\n")
    
    demo_email_analysis()
    print("\n" + "-" * 70 + "\n")
    
    demo_business_workflow()
    
    print("\n" + "=" * 70)
    print("LESSON COMPLETE")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("  1. Email analysis tools extract business intelligence from messages")
    print("  2. Tool schemas define strict interfaces for AI clients")
    print("  3. Tools work together in pipelines for complex workflows")
    print("  4. Sentiment and urgency inform routing and priority")
    print("  5. create_email_analyst_server() is a reusable template\n")
    print("Next Lesson:")
    print("  Lesson 5.5 adds security guardrails to prevent unsafe actions\n")
