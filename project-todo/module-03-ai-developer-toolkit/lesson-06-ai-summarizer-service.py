"""
Lesson 3.6: Deploy a Mini AI Service (Capstone) — TODO scaffold

Build a production-ready AI summarization service combining all Module 3 lessons.

PHASE 1: Core business logic (SummarizationService)
PHASE 2: Streamlit UI
PHASE 3: Statistics and deployment readiness

Run: streamlit run lesson-06-ai-summarizer-service.py
"""

import streamlit as st
from datetime import datetime
from typing import List, Optional, Dict

# TODO: Import from shared modules


class SummarizationService:
    """Core summarization business logic."""

    def __init__(self, model: str = "gpt-3.5-turbo"):
        """
        PHASE 1: Initialize service with model choice.

        TODO:
        - Store model name
        - Initialize empty history list
        """
        # TODO: Implement

    def summarize(self, document: str, language: str = "English") -> Optional[str]:
        """
        PHASE 1: Summarize a document using LLM.

        TODO:
        - Create LLMClient
        - Build prompt using DOCUMENT_SUMMARY_PROMPT
        - Call client.complete()
        - Log to history
        - Return summary
        """
        # TODO: Implement

    def get_stats(self) -> Dict:
        """
        PHASE 3: Return service statistics.

        TODO:
        - Count total requests
        - Count successful vs failed
        - Calculate average document length
        - Calculate average summary length
        - Return dict with these stats
        """
        # TODO: Implement


# PHASE 1: Page setup
st.set_page_config(page_title="AI Summarization Service", layout="centered")

st.title("📊 AI Summarization Service")
st.markdown("""
TODO: Add description of what this capstone service demonstrates
""")

# PHASE 1: Initialize session state
if "service" not in st.session_state:
    st.session_state.service = SummarizationService()


# PHASE 2: Sidebar configuration
with st.sidebar:
    st.header("⚙️ Service Configuration")

    # TODO: Add model selector
    # TODO: Add language selector
    # TODO: Show service statistics (if available)
    # TODO: Add clear history button


# PHASE 2: Main UI layout
col1, col2 = st.columns([2, 1])

with col1:
    # TODO: Add text area for document input
    # TODO: Add placeholder with helpful text
    pass

with col2:
    # TODO: Add info box with quick tips
    # - Recommended document length
    # - Expected processing time
    # - Output language
    pass


# PHASE 2: Action button
# TODO: Add "Summarize" button
# TODO: Add input validation (minimum length, etc.)
# TODO: Show spinner while processing


# PHASE 2: Display results
# TODO: Display summary result
# TODO: Show original vs summary length
# TODO: Show processing time


# PHASE 3: Request history
# TODO: Add expander showing recent requests
# TODO: Display as table or list


# PHASE 3: Footer with deployment info
st.divider()

st.info("""
TODO: Add deployment instructions showing:
- How to deploy to Streamlit Cloud
- How to deploy to Railway.app
- How to deploy with Docker
""")

st.caption("Module 3.6 • Capstone Project • Deploy a Mini AI Service")
