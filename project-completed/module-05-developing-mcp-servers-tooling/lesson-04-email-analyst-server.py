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
import os

# Import from module-local shared (mcp_server, tools)
sys.path.insert(0, str(Path(__file__).parent))
from shared.mcp_server import MCPServer, Tool
from shared.tools import EmailTools, TextTools

# Import settings from root shared utils
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
try:
    from shared.utils.settings import load_settings
except ImportError:
    # Fallback if settings not found
    def load_settings():
        class Settings:
            openrouter_url = os.getenv("OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions")
            openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        return Settings()

# LLM imports for real analysis
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


# ============================================================================
# UI UTILITIES
# ============================================================================

def clear_screen():
    """Clear terminal screen."""
    import os
    os.system('clear' if os.name == 'posix' else 'cls')


def show_menu():
    """Display main menu."""
    clear_screen()
    print("\n" + "=" * 70)
    print("🚀 LESSON 5.4: CONNECTING REAL-WORLD TOOLS - EMAIL ANALYST SERVER".center(70))
    print("=" * 70)
    print()
    print("  Choose a pattern to learn:\n")
    print("    [1] PATTERN: Tool Registration & Schemas")
    print("        → Discover email analysis tools and input schemas\n")
    print("    [2] PATTERN: Email Analysis Pipeline")
    print("        → Parse, categorize, and analyze sample emails\n")
    print("    [3] PATTERN: Business Workflow Routing")
    print("        → Understand email triage and escalation patterns\n")
    print("    [4] PATTERN: Real Email System Integration")
    print("        → Step-by-step guide to connect POP/IMAP/Gmail/Webhook\n")
    print("    [Q] Quit\n")
    print("=" * 70)


# ============================================================================
# HELPER FUNCTIONS: Email loading and LLM analysis
# ============================================================================

def load_sample_email() -> Dict[str, str]:
    """Load sample email from datasets/sample-email.txt."""
    sample_path = Path(__file__).parent.parent.parent / "datasets" / "sample-email.txt"
    
    if not sample_path.exists():
        # Fallback if file doesn't exist
        return {
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
    
    with open(sample_path, "r") as f:
        content = f.read()
    
    # Parse email format
    lines = content.split("\n")
    sender = ""
    subject = ""
    body_start = 0
    
    for i, line in enumerate(lines):
        if line.startswith("From:"):
            sender = line.replace("From:", "").strip()
        elif line.startswith("Subject:"):
            subject = line.replace("Subject:", "").strip()
        elif line.strip() == "":
            body_start = i + 1
            break
    
    body = "\n".join(lines[body_start:]).strip()
    
    return {
        "sender": sender,
        "subject": subject,
        "body": body,
    }


def analyze_with_llm(prompt: str) -> str:
    """Call OpenRouter API with GPT-3.5 for analysis. Falls back to keyword-based if API unavailable."""
    if not HAS_REQUESTS:
        return None
    
    settings = load_settings()
    if not settings.openrouter_api_key:
        return None
    
    try:
        headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "Content-Type": "application/json",
        }
        
        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 200,
        }
        
        response = requests.post(settings.openrouter_url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        return None
    except Exception as e:
        print(f"⚠️  OpenRouter API error: {e}. Falling back to keyword-based analysis.")
        return None


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
    sample_email: Optional[Dict] = None,
) -> MCPServer:
    """Core template method: Initialize and configure an Email Analysis MCP Server.
    
    This is the production-ready server initialization pattern for email analysis.
    Learners can extract this method and adapt it for their own email sources.
    
    Args:
        server_name: Name of the MCP server (for identification)
        sample_email: Optional sample email to use. If None, loads from file.
    
    Returns:
        MCPServer: Configured server with email analysis tools registered.
        Ready to accept client requests via JSON-RPC.
    
    Features:
        - Parse and structure raw email messages
        - Categorize email types using GPT-3.5 via OpenRouter
        - Extract action items and TODOs
        - Analyze sentiment using GPT-3.5 (or keyword fallback)
        - Identify important keywords
    
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
    
    # Load sample email if not provided
    if sample_email is None:
        sample_email = load_sample_email()
    
    # Step 2: Define and register parse_email tool
    def parse_email(sender: Optional[str] = None, subject: Optional[str] = None, body: Optional[str] = None) -> str:
        """Parse and structure raw email message.
        
        Args:
            sender: Email sender address (optional, uses sample if not provided)
            subject: Email subject line (optional)
            body: Email body text (optional)
        
        Returns:
            JSON string with parsed email
        """
        # Use provided email or fall back to sample
        if sender is None:
            sender = sample_email["sender"]
        if subject is None:
            subject = sample_email["subject"]
        if body is None:
            body = sample_email["body"]
        
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
                    "description": "Email sender address (optional, uses sample if omitted)"
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject line (optional)"
                },
                "body": {
                    "type": "string",
                    "description": "Email body text (optional)"
                },
            },
        },
    )
    
    server.register_tool(parse_tool, parse_email)
    
    # Step 3: Define and register categorize_email tool with LLM
    def categorize_email(subject: Optional[str] = None, body: Optional[str] = None) -> str:
        """Categorize email type using GPT-3.5 via OpenRouter (with fallback to keyword analysis).
        
        Args:
            subject: Email subject line (optional, uses sample if not provided)
            body: Email body text (optional)
        
        Returns:
            JSON with email category and confidence
        """
        if subject is None:
            subject = sample_email["subject"]
        if body is None:
            body = sample_email["body"]
        
        # Try LLM first
        if HAS_REQUESTS:
            prompt = f"""Categorize this email into one of these categories:
- meeting_request: Email requesting or scheduling a meeting
- support_request: Email asking for help or reporting an issue
- status_report: Email providing updates or reports
- general: General email with no specific category

Subject: {subject}
Body: {body}

Respond with ONLY the category name (e.g., "support_request") and a confidence score 0-100.
Format: category|confidence"""
            
            result = analyze_with_llm(prompt)
            if result:
                try:
                    parts = result.strip().split("|")
                    category = parts[0].strip()
                    confidence = int(parts[1].strip()) if len(parts) > 1 else 80
                    return json.dumps({
                        "category": category,
                        "confidence": confidence,
                        "description": _category_descriptions.get(category, "Other email type"),
                        "method": "GPT-3.5 via OpenRouter"
                    })
                except:
                    pass
        
        # Fallback to keyword-based
        category = EmailTools.categorize_email(subject, body)
        return json.dumps({
            "category": category,
            "confidence": 70,
            "description": _category_descriptions.get(category, "Other email type"),
            "method": "Keyword-based fallback"
        })
    
    categorize_tool = Tool(
        name="categorize_email",
        description="Classify email type for workflow routing using AI analysis",
        inputSchema={
            "type": "object",
            "properties": {
                "subject": {
                    "type": "string",
                    "description": "Email subject line (optional, uses sample if omitted)"
                },
                "body": {
                    "type": "string",
                    "description": "Email body text (optional)"
                },
            },
        },
    )
    
    server.register_tool(categorize_tool, categorize_email)
    
    # Step 4: Define and register extract_action_items tool
    def extract_action_items(body: Optional[str] = None) -> str:
        """Extract action items and TODOs from email.
        
        Args:
            body: Email body text (optional, uses sample if not provided)
        
        Returns:
            JSON with list of action items
        """
        if body is None:
            body = sample_email["body"]
        
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
                    "description": "Email body text (optional, uses sample if omitted)"
                },
            },
        },
    )
    
    server.register_tool(action_tool, extract_action_items)
    
    # Step 5: Define and register analyze_sentiment tool with LLM
    def analyze_sentiment(text: Optional[str] = None) -> str:
        """Analyze sentiment and urgency of email using GPT-3.5 via OpenRouter.
        
        Args:
            text: Email text to analyze (optional, uses sample body if not provided)
        
        Returns:
            JSON with sentiment and urgency indicators
        """
        if text is None:
            text = sample_email["body"]
        
        # Try LLM first
        if HAS_REQUESTS:
            prompt = f"""Analyze the sentiment and urgency of this email text.
Respond with ONLY:
sentiment (positive/negative/neutral)
urgency (low/medium/high)
priority (normal/high/critical)

Email: {text}

Format: sentiment|urgency|priority"""
            
            result = analyze_with_llm(prompt)
            if result:
                try:
                    parts = result.strip().split("|")
                    sentiment = parts[0].strip()
                    urgency = parts[1].strip() if len(parts) > 1 else "medium"
                    priority = parts[2].strip() if len(parts) > 2 else "normal"
                    return json.dumps({
                        "sentiment": sentiment,
                        "urgency": urgency,
                        "priority": priority,
                        "method": "GPT-3.5 via OpenRouter"
                    })
                except:
                    pass
        
        # Fallback to keyword-based
        sentiment = EmailTools._analyze_sentiment(text)
        urgency_keywords = ["urgent", "asap", "critical", "immediately", "deadline"]
        is_urgent = any(keyword in text.lower() for keyword in urgency_keywords)
        
        return json.dumps({
            "sentiment": sentiment,
            "urgency": "high" if is_urgent else "low",
            "priority": "high" if is_urgent else "normal",
            "method": "Keyword-based fallback"
        })
    
    sentiment_tool = Tool(
        name="analyze_sentiment",
        description="Analyze sentiment and urgency of email text using AI",
        inputSchema={
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Email text to analyze (optional, uses sample if omitted)"
                },
            },
        },
    )
    
    server.register_tool(sentiment_tool, analyze_sentiment)
    
    # Step 6: Define and register extract_keywords tool
    def extract_keywords(text: Optional[str] = None, top_k: int = 5) -> str:
        """Extract important keywords from email.
        
        Args:
            text: Email text to analyze (optional, uses sample body if not provided)
            top_k: Number of top keywords to return (default: 5)
        
        Returns:
            JSON with keyword list
        """
        if text is None:
            text = sample_email["body"]
        
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
                    "description": "Email text to analyze (optional, uses sample if omitted)"
                },
                "top_k": {
                    "type": "integer",
                    "description": "Number of top keywords to extract (default: 5)",
                    "default": 5
                }
            },
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
    print("DEMO 1: TOOL REGISTRATION & SCHEMAS")
    print("=" * 70)
    
    server = create_email_analyst_server("DemoEmailAnalyst")
    
    print("\nRegistered Email Analysis Tools:")
    print("-" * 70)
    
    tools = server.list_tools()
    for i, tool in enumerate(tools, 1):
        print(f"\n{i}. {tool['name'].upper()}")
        print(f"   Description: {tool['description']}")
        print(f"   Input Parameters:")
        for param, details in tool['inputSchema']['properties'].items():
            print(f"     - {param}: {details.get('description', 'N/A')}")
    
    print(f"\n✅ Total tools: {len(tools)}")
    print("\nKey Features:")
    print("  • All input parameters are OPTIONAL")
    print("  • Tools use sample email from datasets/sample-email.txt if not provided")
    print("  • Sentiment & categorization use GPT-3.5 via OpenRouter (fallback to keyword analysis)")
    print("  • Perfect for agent integration: agents can call tools with or without params")


def demo_email_analysis():
    """Demonstration 2: Analyze a complex email through the pipeline."""
    print("\n" + "=" * 70)
    print("DEMO 2: EMAIL ANALYSIS PIPELINE (GPT-3.5 via OpenRouter)")
    print("=" * 70)
    
    # Load sample email from file
    sample_email = load_sample_email()
    server = create_email_analyst_server("DemoEmailAnalyst", sample_email=sample_email)
    
    email = sample_email
    
    print(f"\n📧 Analyzing email from: {email['sender']}")
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
    
    # Categorize with LLM
    print("\nStep 2: Categorize (GPT-3.5 via OpenRouter)")
    print("-" * 70)
    category_result = server.tool_handlers['categorize_email'](
        subject=email['subject'],
        body=email['body']
    )
    category = json.loads(category_result)
    print(f"Category: {category['category']}")
    print(f"Confidence: {category['confidence']}%")
    print(f"Description: {category['description']}")
    print(f"Method: {category['method']}")
    
    # Analyze sentiment with LLM
    print("\nStep 3: Analyze Sentiment (GPT-3.5 via OpenRouter)")
    print("-" * 70)
    sentiment_result = server.tool_handlers['analyze_sentiment'](
        text=email['body']
    )
    sentiment = json.loads(sentiment_result)
    print(f"Sentiment: {sentiment['sentiment'].upper()}")
    print(f"Urgency: {sentiment['urgency'].upper()}")
    print(f"Priority: {sentiment['priority'].upper()}")
    print(f"Method: {sentiment['method']}")
    
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
    print("  • Tools use GPT-3.5 via OpenRouter for sentiment and categorization")
    print("  • Fallback to keyword-based analysis if API unavailable")
    print("  • All tool parameters are optional (use sample email if omitted)")
    print("  • AI clients can provide custom emails or rely on samples")


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


def demo_real_email_integration():
    """Demonstration 4: Steps to integrate with real email systems."""
    print("\n" + "=" * 70)
    print("DEMO 4: REAL EMAIL SYSTEM INTEGRATION")
    print("=" * 70)
    
    print("""
Adapting This Template to Real Email Sources
============================================

The create_email_analyst_server() template works with any email data source.
Follow these 6 steps to connect your server to production email systems:

Step 1: Add Configuration
  Add EMAIL_SOURCE, credentials, and server settings at the top of your file.
  Learners typically choose IMAP (Gmail/Outlook), Gmail API, or webhook-based.

Step 2: Create an Email Fetcher Function
  Write a function to connect to your email source and retrieve messages.
  Return emails in {sender, subject, body, timestamp} format for consistency.

Step 3: Modify Server to Accept Email Source
  Extend create_email_analyst_server() to accept your email fetcher function.
  Pass it as a parameter so the server can retrieve real emails on demand.

Step 4: Add a Tool to List Emails
  Register a "list_emails" tool that calls your fetcher and returns unread messages.
  This gives AI clients access to discover and select emails for analysis.

Step 5: Add Security Guardrails (Critical!)
  Review Lesson 5.5 for credential management, rate limiting, approval gates,
  and audit logging before deploying to production.

Step 6: Test with Real Emails
  Call your server tools with actual emails from your configured source.
  Verify parsing, categorization, and analysis work as expected.
""")
    
    print("\n✅ Integration guide complete")
    print("\nNext Steps:")
    print("  1. Choose your email source (IMAP, Gmail API, or webhook)")
    print("  2. Follow Steps 1-6 above to integrate")
    print("  3. Review Lesson 5.5 for security guardrails")
    print("  4. Test with real emails")
    print("  5. Deploy as part of MCP Toolkit (Lesson 5.6 Capstone)")


# ============================================================================
# PATTERN WRAPPER FUNCTIONS: Interactive menu patterns
# ============================================================================

def pattern_1_tool_registration():
    """PATTERN 1: Tool Registration & Schemas."""
    print("\n" + "=" * 70)
    print("PATTERN 1: TOOL REGISTRATION & SCHEMAS")
    print("=" * 70)
    demo_tool_registration()
    input("\nPress Enter to continue...")


def pattern_2_email_analysis():
    """PATTERN 2: Email Analysis Pipeline."""
    print("\n" + "=" * 70)
    print("PATTERN 2: EMAIL ANALYSIS PIPELINE")
    print("=" * 70)
    demo_email_analysis()
    input("\nPress Enter to continue...")


def pattern_3_business_workflow():
    """PATTERN 3: Business Workflow Routing."""
    print("\n" + "=" * 70)
    print("PATTERN 3: BUSINESS WORKFLOW ROUTING")
    print("=" * 70)
    demo_business_workflow()
    input("\nPress Enter to continue...")


def pattern_4_real_integration():
    """PATTERN 4: Real Email System Integration."""
    print("\n" + "=" * 70)
    print("PATTERN 4: REAL EMAIL SYSTEM INTEGRATION")
    print("=" * 70)
    demo_real_email_integration()
    input("\nPress Enter to continue...")


def main():
    """Main interactive menu loop."""
    patterns = {
        "1": pattern_1_tool_registration,
        "2": pattern_2_email_analysis,
        "3": pattern_3_business_workflow,
        "4": pattern_4_real_integration,
    }

    while True:
        show_menu()
        choice = input("Choose [1-4] or [Q] to quit: ").strip().lower()

        if choice == "q":
            clear_screen()
            print("\n✅ Thanks for learning! Remember to:")
            print("   • Use create_email_analyst_server() as your MCP template")
            print("   • Register tools for parsing, categorizing, and analyzing emails")
            print("   • Add security guardrails before production use (Lesson 5.5)")
            print("   • Follow Steps 1-6 to connect to real email sources")
            print("   • Integrate into MCP Toolkit for autonomous agents (Lesson 5.6)\n")
            break
        
        if choice in patterns:
            try:
                patterns[choice]()
            except Exception as e:
                print(f"\n❌ Error: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("\n❌ Invalid choice. Please enter [1-4] or [Q]")
            input("Press Enter to try again...")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    main()
