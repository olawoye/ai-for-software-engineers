"""
Lesson 5.4 TODO: Connecting Real-World Tools - Email Analyst Server

In this lesson, you'll build the core template method for an MCP server
that analyzes emails and enables business workflow automation.

Your goal: Implement create_email_analyst_server(), a reusable template that:
  - Registers tools for email parsing, categorization, and analysis
  - Integrates with shared EmailTools and TextTools utilities
  - Handles complex business workflows (triage, routing, escalation)
  - Demonstrates how MCP tools compose into workflows

PHASE 1: Core Template Method (create_email_analyst_server)
  - Accept parameter: server_name
  - Initialize MCPServer with name and version "1.0.0"
  - Define 5 tools with input schemas (see PHASE 2)
  - Register each tool with appropriate handler
  - Return configured server

PHASE 2: Tool Implementations (5 tools)
  Each tool should:
  - Accept structured inputs matching the schema
  - Use EmailTools or TextTools helpers (from shared/)
  - Return JSON string with results
  
  Tool 1: parse_email(sender, subject, body)
    - Call EmailTools.parse_email()
    - Return: {"sender", "subject", "body", "received_at", "sentiment"}
  
  Tool 2: categorize_email(subject, body)
    - Call EmailTools.categorize_email()
    - Return category and description
  
  Tool 3: extract_action_items(body)
    - Call EmailTools.identify_action_items()
    - Return: {"action_items": List[str], "count", "requires_response"}
  
  Tool 4: analyze_sentiment(text)
    - Call EmailTools._analyze_sentiment()
    - Add urgency detection (check for "urgent", "asap", etc.)
    - Return: {"sentiment", "is_urgent", "priority"}
  
  Tool 5: extract_keywords(text, top_k=5)
    - Call TextTools.extract_keywords()
    - Return: {"keywords": List[str], "count"}

PHASE 3: Demonstrations
  - demo_tool_registration(): Show all tools with schemas
  - demo_email_analysis(): Process a complex email through full pipeline
  - demo_business_workflow(): Show how tools compose into workflow
  - main(): Run all demonstrations with clear output

REFERENCE:
  - Completed implementation: project-completed/module-05-developing-mcp-servers-tooling/lesson-04-email-analyst-server.py
  - Email tools: shared/tools.py (EmailTools class)
  - Text tools: shared/tools.py (TextTools class)
  - MCP server base: shared/mcp_server.py
  - Business scenario: Automated email triage and workflow routing
  - Data flow: Email → Parse → Analyze (sentiment, category, items) → Route → Action

LEARNING GOALS:
  1. Design tool schemas for complex inputs (emails have multiple fields)
  2. Integrate with existing utilities from shared modules
  3. Compose tools into workflows (parse → categorize → route)
  4. Understand business intelligence extraction from text
  5. See how MCP enables AI participation in business processes
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
# PHASE 1: Core Template Method - create_email_analyst_server()
# ============================================================================
# TODO: Implement the core create_email_analyst_server() function
#
# Requirements:
#   1. Accept parameter: server_name (default: "EmailAnalyst")
#   2. Initialize MCPServer with name and version "1.0.0"
#   3. Implement 5 tool functions (see PHASE 2 below)
#   4. For each tool, create a Tool object with name, description, inputSchema
#   5. Register each tool with server.register_tool(tool, handler)
#   6. Print status messages for debugging
#   7. Return configured server
#
# Hints:
#   - Use json.dumps() to convert dicts to JSON strings for returns
#   - Use EmailTools and TextTools methods directly (don't reimplement)
#   - Input schemas must match tool parameters exactly
#   - Print statements help track initialization progress

def create_email_analyst_server(
    server_name: str = "EmailAnalyst",
) -> MCPServer:
    """TODO: Initialize and configure an Email Analysis MCP Server.
    
    This is the production-ready server initialization pattern for email analysis.
    Learners can extract this method and adapt it for their own email sources.
    
    Args:
        server_name: Name of the MCP server (for identification)
    
    Returns:
        MCPServer: Configured server with email analysis tools registered.
        Ready to accept client requests via JSON-RPC.
    """
    # Step 1: TODO Initialize server
    # Step 2-6: TODO Implement and register 5 tools (see PHASE 2 below)
    # Step 7: TODO Return configured server
    
    pass


# ============================================================================
# PHASE 2: Tool Implementations
# ============================================================================
# TODO: Implement these 5 tools to be registered in create_email_analyst_server()
#
# Tool 1: parse_email(sender: str, subject: str, body: str) -> str
#   - Call EmailTools.parse_email(sender, subject, body)
#   - Convert result to JSON string
#   - Return as string
#
# Tool 2: categorize_email(subject: str, body: str) -> str
#   - Call EmailTools.categorize_email(subject, body) to get category string
#   - Use _category_descriptions dict to get description
#   - Return JSON: {"category": str, "description": str}
#
# Tool 3: extract_action_items(body: str) -> str
#   - Call EmailTools.identify_action_items(body)
#   - Count items
#   - Return JSON: {"action_items": List, "count": int, "requires_response": bool}
#
# Tool 4: analyze_sentiment(text: str) -> str
#   - Call EmailTools._analyze_sentiment(text)
#   - Check for urgency keywords: "urgent", "asap", "critical", "immediately", "deadline"
#   - Return JSON: {"sentiment": str, "is_urgent": bool, "priority": str}
#
# Tool 5: extract_keywords(text: str, top_k: int = 5) -> str
#   - Call TextTools.extract_keywords(text, top_k)
#   - Return JSON: {"keywords": List[str], "count": int}

# TODO: Implement parse_email tool function
# TODO: Implement categorize_email tool function
# TODO: Implement extract_action_items tool function
# TODO: Implement analyze_sentiment tool function
# TODO: Implement extract_keywords tool function


# Helper mapping for category descriptions
_category_descriptions = {
    "meeting_request": "Email requesting or scheduling a meeting",
    "support_request": "Email asking for help or reporting an issue",
    "status_report": "Email providing updates or reports",
    "general": "General email with no specific category",
}


# ============================================================================
# PHASE 3: Demonstrations
# ============================================================================
# TODO: Implement demonstration functions to show how tools work
#
# demo_tool_registration()
#   - Create server
#   - List all tools
#   - Show each tool's description and input schema
#   - Print learning point about tool schemas
#
# demo_email_analysis()
#   - Create server
#   - Use a complex sample email with action items, urgency, etc.
#   - Call each tool in sequence:
#     1. parse_email()
#     2. categorize_email()
#     3. analyze_sentiment()
#     4. extract_action_items()
#     5. extract_keywords()
#   - Print results from each step
#   - Show full analysis pipeline output
#
# demo_business_workflow()
#   - Print a diagram/description of email workflow:
#     PARSE → CATEGORIZE → ANALYZE → ROUTE → ACTION
#   - Show example routing decisions (urgent + support → escalate)
#   - Explain integration with Module 6 agents
#
# main()
#   - Print lesson title
#   - Call each demonstration with separator lines
#   - Show lesson completion message with key takeaways

def demo_tool_registration():
    """TODO: Demonstrate tool registration."""
    # Print demo header
    # Create server
    # Get and iterate over server.list_tools()
    # Print each tool with description and input schema
    # Print learning point
    pass


def demo_email_analysis():
    """TODO: Demonstrate email analysis pipeline."""
    # Print demo header
    # Create server
    # Create a complex sample email with action items and urgency
    # Call each tool in sequence and print results
    # Show final analysis
    # Print learning point
    pass


def demo_business_workflow():
    """TODO: Demonstrate email workflow routing."""
    # Print demo header
    # Print workflow description with steps and routing decisions
    # Show example: "URGENT + SUPPORT_REQUEST → ESCALATE"
    # Explain integration with Module 6 agents
    # Print learning point
    pass


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # TODO: Print lesson title and introduction
    # TODO: Call demo_tool_registration()
    # TODO: Print separator line
    # TODO: Call demo_email_analysis()
    # TODO: Print separator line
    # TODO: Call demo_business_workflow()
    # TODO: Print lesson completion with key takeaways
    # TODO: Print next lesson reference
    pass
