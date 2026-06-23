"""
Lesson 3.3: Rapid Prototyping with Streamlit — TODO Scaffold

Learn how Streamlit dramatically reduces the effort to build AI applications.
Connect user inputs, AI services, and outputs into functioning prototypes in minutes.

PHASE 1: Setup and configuration (page config, imports, session state, sidebar)
PHASE 2: Implement three interactive modes (classification, summarization, Q&A)
PHASE 3: API calls, error handling, metrics display, and footer

Run: streamlit run lesson-03-rapid-prototyping.py
Requires: export OPENROUTER_API_KEY='your-key-here'

Reference: project-completed/module-03-ai-developer-toolkit/lesson-03-rapid-prototyping.py
"""

import streamlit as st
import time
# TODO PHASE 1: Import LLM client and config
# from shared.llm_client import LLMClient
# from shared.config import MODELS, DEFAULT_MODEL, TEMP_PRECISE, TEMP_BALANCED, TEMP_CREATIVE


# TODO PHASE 1: Page configuration
# Use st.set_page_config() to set:
# - page_title: "Rapid Prototyping with Streamlit"
# - layout: "wide"
# - initial_sidebar_state: "expanded"


# TODO PHASE 1: Initialize session state for configuration persistence
# Store in session_state:
# - "model" (use DEFAULT_MODEL)
# - "temperature" (use TEMP_BALANCED)
# - "max_tokens" (default 200)


# ============================================================================
# HEADER & INTRODUCTION
# ============================================================================

# TODO PHASE 1: Display title with emoji and introduction
# Use st.title() and st.markdown()
# Explain that Streamlit enables rapid AI app prototyping without HTML/CSS


# TODO PHASE 1: Add divider
# st.divider()


# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

# TODO PHASE 1: Build sidebar configuration panel
# with st.sidebar:
#     st.header("⚙️ Configuration")
#
#     # >>> CUSTOMIZE: Model selector
#     # Use st.selectbox() with MODELS.values()
#     # Format display using lambda to show model names
#
#     # >>> CUSTOMIZE: Temperature slider
#     # Use st.slider() with range 0.0-1.0, step 0.1
#
#     # >>> CUSTOMIZE: Max tokens slider
#     # Use st.slider() with range 50-500, step 50
#
#     st.divider()
#
#     # >>> REFERENCE: Display current settings
#     # Use st.metric() to show model, temperature, max_tokens


# ============================================================================
# MODE SELECTION
# ============================================================================

# TODO PHASE 2: Mode selector
# Use st.radio() with options:
# - "Text Classification"
# - "Text Summarization"
# - "Question & Answer"
# Set horizontal=True


# ============================================================================
# MODE 1: TEXT CLASSIFICATION
# ============================================================================

# TODO PHASE 2: Implement "Text Classification" mode
# if mode == "Text Classification":
#     st.subheader("📋 Text Classification")
#
#     # >>> REFERENCE: Explanation section (expandable)
#     # with st.expander("💡 How it works", expanded=True):
#     #     st.markdown("""Common uses: sentiment analysis, ticket routing, intent detection""")
#
#     # >>> CUSTOMIZE: Example buttons
#     # Create 3 columns
#     # Define example_texts dict with Sentiment, Support, Topic examples
#     # Create buttons for each (key="btn_sentiment", "btn_support", "btn_topic")
#
#     # >>> REFERENCE: Session state for text persistence
#     # if "classification_text" not in st.session_state:
#     #     st.session_state.classification_text = ""
#     # Check button state and update session_state.classification_text
#
#     # >>> CUSTOMIZE: Text input
#     # Use st.text_area() with session_state.classification_text as value
#
#     # >>> CUSTOMIZE: Categories selector
#     # Use st.multiselect() with predefined category options
#
#     # >>> REFERENCE: Classify button and API call
#     # if st.button("🔍 Classify", type="primary", use_container_width=True):
#     #     - Validate text_input and categories
#     #     - Use st.spinner("Classifying...")
#     #     - Initialize LLMClient
#     #     - Create prompt: f"Classify into: {', '.join(categories)}\\n\\nText: ..."
#     #     - Call client.complete() with temperature and max_tokens
#     #     - Measure time with time.time()
#     #     - Display result with st.success()
#     #     - Show metrics (response time)
#
#     # >>> REFERENCE: Code comparison expander
#     # with st.expander("👨‍💻 See the code"):
#     #     Show Traditional Python vs Streamlit comparison


# ============================================================================
# MODE 2: TEXT SUMMARIZATION
# ============================================================================

# TODO PHASE 2: Implement "Text Summarization" mode
# elif mode == "Text Summarization":
#     st.subheader("📝 Text Summarization")
#
#     # Similar structure to Mode 1:
#     # - Explanation expander
#     # - Example buttons (Article, Meeting, Feedback) in columns
#     # - Text area for document input
#     # - Summarize button with real API call
#     # - Display result with metrics
#     # - Code comparison


# ============================================================================
# MODE 3: QUESTION & ANSWER
# ============================================================================

# TODO PHASE 2: Implement "Question & Answer" mode
# elif mode == "Question & Answer":
#     st.subheader("❓ Question & Answer")
#
#     # Similar structure:
#     # - Explanation expander
#     # - Example buttons (Policy, FAQ) in columns
#     # - Two columns: document input and question input
#     # - Answer button with real API call
#     # - Display result with metrics
#     # - Code comparison


# ============================================================================
# FOOTER
# ============================================================================

# TODO PHASE 3: Add footer content
# st.divider()
# st.markdown("""
# ### 🎓 Key Learnings
# - Speed: Build AI UIs in minutes, not weeks
# - No HTML/CSS: Pure Python + Streamlit handles UI
# - Rapid iteration: Change code, see results instantly
# - Real APIs: Connect to actual LLMs
# - Reusable patterns: Copy into your projects
#
# ### 📚 Next Steps
# 1. Customize examples with different prompts
# 2. Build your own mode
# 3. Deploy to cloud using `streamlit cloud`
# """)
#
# st.caption("Module 3.3 • Rapid Prototyping with Streamlit • Learn to build AI apps fast")
