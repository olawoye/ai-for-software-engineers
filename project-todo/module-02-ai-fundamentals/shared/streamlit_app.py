"""
Shared Streamlit dashboard for multi-lesson demonstrations.
Each lesson registers its tab content via lesson_registry.
"""
import streamlit as st
from typing import Callable, Dict

# Global registry of lessons
lesson_registry: Dict[str, Callable] = {}

def register_lesson(lesson_name: str, lesson_func: Callable):
    """Register a lesson's Streamlit content."""
    lesson_registry[lesson_name] = lesson_func

def render_dashboard():
    """Main dashboard with tabs for each registered lesson."""
    st.set_page_config(page_title="AI Fundamentals - Module 2", layout="wide")
    st.title("🤖 Module 2: AI Fundamentals")
    st.markdown("Interactive lessons on tokens, context, embeddings, and more.")

    if not lesson_registry:
        st.warning("No lessons registered yet.")
        return

    tabs = st.tabs(list(lesson_registry.keys()))

    for tab, lesson_name in zip(tabs, lesson_registry.keys()):
        with tab:
            lesson_registry[lesson_name]()

if __name__ == "__main__":
    render_dashboard()
