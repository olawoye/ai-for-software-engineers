"""
Lesson 3.6: AI Operations Assistant with Tool Calling — TODO Scaffold

Learn how LLMs orchestrate actions through tool calling and function selection.
Build an intelligent assistant that makes decisions about which tools to use.

BUSINESS SCENARIO:
AI assistants need to take actions, not just answer questions. This lesson teaches
how LLMs use tool calling to retrieve weather, access databases, and execute workflows.

Run: streamlit run lesson-06-ai-operations-assistant.py
Requires: export OPENROUTER_API_KEY='your-key-here'
"""

import streamlit as st
import time
import json

# ============================================================================
# STAGE 1: Tool Definitions & Registry
# ============================================================================
# Implement 5 functional tools and create a registry for tool calling.
# Available utilities: dict-based tool registry, tool metadata schemas
# TODO: Add your Stage 1 implementation here


# ============================================================================
# STAGE 2: Session State & Function Calling Logic
# ============================================================================
# Initialize session state and implement tool calling parsing/execution.
# Available utilities: st.session_state, regex for parsing tool calls, try/except
# TODO: Add your Stage 2 implementation here


# ============================================================================
# STAGE 3: Streamlit UI & Conversation Management
# ============================================================================
# Build chat interface with tool calling capability and result display.
# Available utilities: st.chat_message(), st.text_input(), tool execution display
# TODO: Add your Stage 3 implementation here


# ============================================================================
# STAGE 4: Analytics & Developer Insights
# ============================================================================
# Track tool usage analytics and display execution details.
# Available utilities: st.metrics(), st.expander(), JSON formatting
# TODO: Add your Stage 4 implementation here
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


# TODO PHASE 3: Input area
# - Use st.chat_input() instead of st.text_input() (auto-submits on Enter, auto-clears)
# - Placeholder text: "Ask me to look something up..."
# - This handles both input and button in one component


# ============================================================================
# MESSAGE PROCESSING & TOOL CALLING (PHASE 3)
# ============================================================================

# TODO PHASE 3: When user sends message:
# 1. Add user message to st.session_state.messages
# 2. Initialize LLMClient
# 3. Build prompt with tool context and conversation
# 4. Call client.complete() to get LLM response
# 5. Check st.session_state.tool_calling_enabled flag
# 6. If enabled, use extract_tool_call() to check if response contains tool call
# 7. If tool call found AND tool calling enabled:
#    - Execute tool with execute_tool()
#    - Track in tool_calls history
#    - Show st.info/st.success feedback
#    - Call LLM again to generate final response using tool result
# 8. If no tool call OR tool calling disabled:
#    - If disabled, show st.info() message
#    - Add response directly to messages
# 9. Call st.rerun()


# ============================================================================
# SIDEBAR: SETTINGS & AVAILABLE TOOLS (PHASE 3)
# ============================================================================

# TODO PHASE 3: Build sidebar with:
# 1. Settings section:
#    - st.toggle("🔧 Enable Tool Calling") to turn tools on/off
#    - Display whether tool calling is ON/OFF with st.success/st.warning
# 2. Available Tools section:
#    - Display each tool from TOOLS dict with st.expander
#    - Show: name, description, parameter, example usage
# 3. Statistics section:
#    - st.metric("Tools Used", st.session_state.total_tools_used)
#    - st.metric("Messages", len(st.session_state.messages))


# ============================================================================
# FOOTER: EDUCATIONAL CONTENT (PHASE 3)
# ============================================================================

# TODO PHASE 3: Expandable sections explaining:
# 1. "How This Works" - tool calling workflow diagram
# 2. "Why This Matters" - foundation for future modules
# 3. "Try These Examples" - sample prompts for each tool
