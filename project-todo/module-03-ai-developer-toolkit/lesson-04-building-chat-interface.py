"""
Lesson 3.4: Building Chat Interfaces — TODO Scaffold

Learn how to build multi-turn conversational AI interfaces with context management.
Master state persistence, conversation history, and context window constraints.

PHASE 1: Setup and configuration (imports, page config, session state, helper functions)
PHASE 2: Chat UI (clean message display + input, NO sidebar controls)
PHASE 3: API calls, context management, error handling, developer insights

Run: streamlit run lesson-04-building-chat-interface.py
Requires: export OPENROUTER_API_KEY='your-key-here'

Reference: project-completed/module-03-ai-developer-toolkit/lesson-04-building-chat-interface.py
"""

import streamlit as st
import time
# TODO PHASE 1: Import required modules
# from shared.llm_client import LLMClient
# from shared.config import DEFAULT_MODEL, TEMP_BALANCED


# TODO PHASE 1: Page configuration
# st.set_page_config(page_title="...", layout="wide", initial_sidebar_state="collapsed")


# ============================================================================
# CONFIGURATION (code-level settings, not UI controls)
# ============================================================================

# TODO PHASE 1: Define code-level configuration
# >>> CUSTOMIZE: CHAT_MODEL - which model to use
# >>> CUSTOMIZE: SYSTEM_PROMPT - personality/behavior of assistant
# >>> REFERENCE: MAX_CONTEXT_TOKENS - token limit before dropping old messages
# >>> REFERENCE: TEMPERATURE - 0.3 (precise) vs 0.7 (balanced) vs 0.9 (creative)


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

# TODO PHASE 1: Initialize session state for:
# - "messages" (list of {role, content} dicts)
# - "total_tokens" (for tracking usage)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

# TODO PHASE 1: Implement build_context_for_api()
# Docstring:
# """
# Build conversation context respecting token limits.
#
# >>> REFERENCE: Why this matters
# If conversation gets too long, drop oldest messages (keep system + recent only).
# This prevents "context full" errors.
# """
# Logic:
# - If messages <= 5, return all
# - If messages > 8, keep only last 7
# - Return trimmed message list


# TODO PHASE 1: Implement format_messages_for_api()
# Docstring:
# """
# Convert internal format to API format.
# Add system prompt at beginning, keep rest as-is.
# """


# TODO PHASE 1: Implement count_tokens_estimate()
# Docstring:
# """
# Rough token count: len(text) // 4
# In production: use actual tokenizer.
# """


# ============================================================================
# HEADER
# ============================================================================

# TODO PHASE 1: Display title and introduction
# - st.title("💬 Building Chat Interfaces")
# - st.markdown(explanation of multi-turn context, token management, etc.)


# ============================================================================
# MAIN CHAT UI (Real-world components only)
# ============================================================================

# TODO PHASE 2: Display conversation history
# - Create container with height=400, border=True
# - If no messages, show info("💬 Start a conversation below")
# - Otherwise loop through messages and display with st.chat_message(role)


# TODO PHASE 2: User input area
# - Create 2 columns ([4, 1] ratio)
# - Column 1: st.text_input() for message
# - Column 2: st.button("Send") primary type


# ============================================================================
# HANDLE USER MESSAGE
# ============================================================================

# TODO PHASE 3: When send button + input:
# - Add user message to st.session_state.messages
# - Use st.spinner("Thinking...")
# - Build context using build_context_for_api()
# - Format for API using format_messages_for_api()
# - Initialize LLMClient with CHAT_MODEL
# - Build prompt string from messages
# - Call client.complete() with temperature and max_tokens
# - Add assistant response to session_state.messages
# - Update total_tokens
# - Call st.rerun()


# TODO PHASE 3: Error handling
# - Use try/except around API call
# - If error: show st.error()
# - Remove user message if API failed


# ============================================================================
# CLEAR CONVERSATION (Real-world button)
# ============================================================================

# TODO PHASE 2: Add clear button
# - if st.button("🗑️ Clear Conversation"):
# -     st.session_state.messages = []
# -     st.session_state.total_tokens = 0
# -     st.rerun()


# ============================================================================
# FOOTER WITH DEVELOPER INSIGHTS
# ============================================================================

# TODO PHASE 3: Add expander("👨‍💻 How This Works")
# Document:
# - State management (st.session_state.messages persistence)
# - Context window management (keep recent, drop old)
# - Model & temperature explanation
# - System prompt explanation
# - Error handling approach

# TODO PHASE 3: Add expander("🎓 Key Learnings")
# List:
# - ✅ Multi-turn context
# - ✅ Message formatting
# - ✅ State persistence
# - ✅ Token budget management
# - ✅ Clean UX (no dev knobs exposed)
# - Production considerations (auth, persistence, rate limiting, etc.)

# TODO PHASE 3: Add expander("🔧 Try This")
# Experiments:
# - Change system prompt (line X)
# - Adjust temperature (line X)
# - Switch models (line X)
# - Reduce context tokens (line X)


# ============================================================================
# CAPTION
# ============================================================================

# st.caption("Module 3.4 • Building Chat Interfaces • Multi-turn conversation with context management")
