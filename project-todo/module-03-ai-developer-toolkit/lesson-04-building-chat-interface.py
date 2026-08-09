"""
Lesson 3.4: Building Chat Interfaces — TODO Scaffold

Learn how to build multi-turn conversational AI interfaces with context management.
Master state persistence, conversation history, and context window constraints.

BUSINESS SCENARIO:
Customers need intuitive chat interfaces for support, consulting, and service delivery.
This lesson teaches how to manage conversation state and context properly.

Run: streamlit run lesson-04-building-chat-interface.py
Requires: export OPENROUTER_API_KEY='your-key-here'
"""

import streamlit as st
import time

# ============================================================================
# STAGE 1: Setup & Session State Initialization
# ============================================================================
# Initialize page config, session state for messages, and helper functions.
# Available utilities: st.set_page_config(), st.session_state, LLMClient
# TODO: Add your Stage 1 implementation here


# ============================================================================
# STAGE 2: Context Management Functions
# ============================================================================
# Implement helper functions for token budgeting and message formatting.
# Available utilities: message list operations, token estimation
# TODO: Add your Stage 2 implementation here


# ============================================================================
# STAGE 3: Header & Chat Display
# ============================================================================
# Build header and display conversation history.
# Available utilities: st.title(), st.markdown(), st.chat_message(), st.container()
# TODO: Add your Stage 3 implementation here


# ============================================================================
# STAGE 4: User Input & Message Handling
# ============================================================================
# Implement user input area and message submission logic.
# Available utilities: st.text_input(), st.button(), st.session_state.messages
# TODO: Add your Stage 4 implementation here


# ============================================================================
# STAGE 5: API Integration & Response Generation
# ============================================================================
# Call LLM to generate responses and update conversation state.
# Available utilities: LLMClient.complete(), error handling, metrics tracking
# TODO: Add your Stage 5 implementation here


# ============================================================================
# STAGE 6: Clear Conversation & Developer Insights
# ============================================================================
# Add clear button and footer explaining how the system works.
# Available utilities: st.button(), st.expander(), st.markdown()
# TODO: Add your Stage 6 implementation here
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
