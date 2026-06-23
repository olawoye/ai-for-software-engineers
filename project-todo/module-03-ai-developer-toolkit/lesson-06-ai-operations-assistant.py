"""
Lesson 3.6: AI Operations Assistant with Tool Calling — TODO Scaffold

Learn how LLMs orchestrate actions through tool calling and function selection.
Build an intelligent assistant that makes decisions about which tools to use.

PHASE 1: Tool definitions and registry setup
PHASE 2: Function calling logic and tool execution
PHASE 3: Streamlit UI, conversation management, and analytics

Run: streamlit run lesson-06-ai-operations-assistant.py
Requires: export OPENROUTER_API_KEY='your-key-here'

Reference: project-completed/module-03-ai-developer-toolkit/lesson-06-ai-operations-assistant.py
"""

import streamlit as st
import time
import json
# TODO PHASE 1: Import required modules
# from shared.llm_client import LLMClient
# from shared.config import DEFAULT_MODEL, TEMP_BALANCED


# ============================================================================
# PHASE 1: TOOL DEFINITIONS & IMPLEMENTATIONS
# ============================================================================

# TODO PHASE 1: Implement 5 functional tools
#
# Tool 1: get_weather(city: str) -> dict
# - Return city weather (temp, condition)
# - Simulate with hardcoded cities dict
#
# Tool 2: lookup_ticket(ticket_id: str) -> dict
# - Return ticket status and priority
# - Simulate with hardcoded tickets dict
#
# Tool 3: search_policy(query: str) -> dict
# - Return matching company policy
# - Simulate with hardcoded policies dict
#
# Tool 4: execute_sql(query: str) -> dict
# - Return query results
# - Validate: block DROP/DELETE commands
# - Return success/error response
#
# Tool 5: calculate(expression: str) -> dict
# - Evaluate mathematical expression
# - Handle errors gracefully
# - Return result or error message


# TODO PHASE 1: Create TOOLS registry dict
# Structure:
# TOOLS = {
#     "weather": {
#         "name": "weather",
#         "description": "Get weather for a city",
#         "parameters": {"city": "string"},
#         "execute": get_weather,
#     },
#     ... (repeat for other 4 tools)
# }


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

# TODO PHASE 1: Initialize session state for:
# - "messages" (conversation history)
# - "tool_calls" (history of tool executions)
# - "total_tools_used" (counter for analytics)


# ============================================================================
# PHASE 2: FUNCTION CALLING LOGIC
# ============================================================================

# TODO PHASE 2: Implement build_tool_context()
# Docstring:
# """Build system prompt describing available tools."""
# Logic:
# - Loop through TOOLS registry
# - Create readable description of each tool
# - Include instruction: "Call tools using <tool_call>tool_name(param=value)</tool_call>"


# TODO PHASE 2: Implement extract_tool_call(text: str)
# Docstring:
# """Parse tool calls from LLM output."""
# Logic:
# - Use regex to find: <tool_call>tool_name(param_name=value)</tool_call>
# - Return tuple: (tool_name, {param_name: param_value})
# - Return (None, None) if no tool call found


# TODO PHASE 2: Implement execute_tool(tool_name: str, params: dict)
# Docstring:
# """Safely execute a tool with parameters."""
# Logic:
# - Validate tool exists in TOOLS registry
# - Try/except wrapper for error handling
# - Call tool["execute"](**params)
# - Return result dict


# ============================================================================
# PAGE SETUP & HEADER
# ============================================================================

# TODO PHASE 2: Configure Streamlit page
# st.set_page_config(page_title="AI Operations Assistant", layout="wide", ...)

# TODO PHASE 2: Display title and introduction markdown
# - Explain the paradigm shift: "LLMs orchestrate actions"
# - Show foundation for Modules 5-8


# ============================================================================
# MAIN CHAT INTERFACE (PHASE 3)
# ============================================================================

# TODO PHASE 3: Display conversation container
# - Show previous messages or info text
# - Use st.container(height=400, border=True)


# TODO PHASE 3: Input area (2 columns)
# - Column 1: st.text_input() for user message
# - Column 2: st.button("Send") primary type


# ============================================================================
# MESSAGE PROCESSING & TOOL CALLING (PHASE 3)
# ============================================================================

# TODO PHASE 3: When send button clicked:
# 1. Add user message to st.session_state.messages
# 2. Initialize LLMClient
# 3. Build prompt with tool context and conversation
# 4. Call client.complete() to get LLM response
# 5. Use extract_tool_call() to check if response contains tool call
# 6. If tool call found:
#    - Execute tool with execute_tool()
#    - Track in tool_calls history
#    - Show st.info/st.success feedback
#    - Call LLM again to generate final response using tool result
# 7. If no tool call:
#    - Just add response directly
# 8. Call st.rerun()


# ============================================================================
# SIDEBAR: ANALYTICS (PHASE 3)
# ============================================================================

# TODO PHASE 3: Sidebar with analytics
# - 3 metrics: Messages, Tools Used, Conversations
# - Clear Conversation button (resets session state)
# - Tool History (last 5 tool calls)


# ============================================================================
# FOOTER: EDUCATIONAL CONTENT (PHASE 3)
# ============================================================================

# TODO PHASE 3: Expandable sections explaining:
# 1. "How This Works" - tool calling workflow diagram
# 2. "Why This Matters" - foundation for future modules
# 3. "Try These Examples" - sample prompts for each tool
