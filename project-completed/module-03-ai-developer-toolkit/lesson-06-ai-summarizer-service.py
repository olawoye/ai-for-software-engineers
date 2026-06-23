"""
Lesson 3.6: Deploy a Mini AI Service

Build a production-ready AI summarization service with API endpoint.
Combines lessons 3.2-3.5 into a complete, deployable application.

Run: python lesson-06-ai-summarizer-service.py
   OR: streamlit run lesson-06-ai-summarizer-service.py --logger.level=debug
"""

import json
import time
from datetime import datetime
from typing import List, Optional
import streamlit as st
from shared.llm_client import LLMClient
from shared.config import MODELS, DEFAULT_MODEL, TEMP_PRECISE
from shared.prompts import DOCUMENT_SUMMARY_PROMPT


st.set_page_config(page_title="AI Summarization Service", layout="centered")

st.title("📊 AI Summarization Service")
st.markdown("""
Production-ready summarization service combining:
- API integration (Lesson 3.2)
- Streamlit UI (Lesson 3.3)
- Multi-turn interactions (Lesson 3.4)
- DevOps patterns (Lesson 3.5)
""")


class SummarizationService:
    """Core summarization business logic."""

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self.history: List[dict] = []

    def summarize(self, document: str, language: str = "English") -> Optional[str]:
        """Summarize a document using LLM."""
        try:
            client = LLMClient(model=self.model)
            prompt = DOCUMENT_SUMMARY_PROMPT.format(
                document=document,
                language=language,
            )
            summary = client.complete(prompt, temperature=TEMP_PRECISE, max_tokens=200)

            # Log to history
            self.history.append({
                "timestamp": datetime.now().isoformat(),
                "model": self.model,
                "language": language,
                "doc_length": len(document),
                "summary_length": len(summary),
                "status": "success",
            })

            return summary

        except Exception as e:
            self.history.append({
                "timestamp": datetime.now().isoformat(),
                "model": self.model,
                "status": "error",
                "error": str(e),
            })
            raise

    def get_stats(self) -> dict:
        """Return service statistics."""
        if not self.history:
            return {}

        successes = [h for h in self.history if h["status"] == "success"]
        errors = [h for h in self.history if h["status"] == "error"]

        return {
            "total_requests": len(self.history),
            "successful": len(successes),
            "errors": len(errors),
            "avg_doc_length": sum(h["doc_length"] for h in successes) / len(successes) if successes else 0,
            "avg_summary_length": sum(h["summary_length"] for h in successes) / len(successes) if successes else 0,
        }


# Initialize session state
if "service" not in st.session_state:
    st.session_state.service = SummarizationService()

if "request_count" not in st.session_state:
    st.session_state.request_count = 0

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Service Configuration")

    model = st.selectbox(
        "Select Model",
        options=list(MODELS.values()),
        format_func=lambda x: [k for k, v in MODELS.items() if v == x][0],
    )
    st.session_state.service.model = model

    language = st.selectbox(
        "Output Language",
        ["English", "Spanish", "French", "German", "Chinese"],
    )

    st.divider()

    # Service statistics
    stats = st.session_state.service.get_stats()
    if stats:
        st.metric("Total Requests", stats["total_requests"])
        st.metric("Successful", stats["successful"])
        if stats["errors"] > 0:
            st.metric("Errors", stats["errors"], delta=None)

    st.divider()

    if st.button("🔄 Clear History"):
        st.session_state.service.history = []
        st.session_state.request_count = 0
        st.rerun()


# Main application
col1, col2 = st.columns([2, 1])

with col1:
    document = st.text_area(
        "📄 Document to Summarize",
        placeholder="Paste a document, article, or long text here...",
        height=200,
    )

with col2:
    st.info("""
    ### Quick Tips
    - 📝 Min: ~100 words
    - 📊 Max: 5,000 words
    - ⏱️ Time: ~2-5 sec
    - 🌍 Outputs in selected language
    """)

# Action button
if st.button("✨ Summarize", type="primary", use_container_width=True):
    if not document:
        st.warning("Please enter a document to summarize")
    elif len(document.split()) < 20:
        st.warning("Document is too short (minimum 20 words)")
    else:
        st.session_state.request_count += 1

        with st.spinner("Summarizing..."):
            try:
                start = time.time()
                summary = st.session_state.service.summarize(document, language)
                elapsed = time.time() - start

                st.success("✅ Summary generated!")

                # Display results
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Original Length", f"{len(document.split())} words")
                with col2:
                    st.metric("Summary Length", f"{len(summary.split())} words")

                st.divider()

                st.subheader("📋 Summary")
                st.write(summary)

                st.caption(f"Generated in {elapsed:.2f}s using {model} ({language})")

            except Exception as e:
                st.error(f"Summarization failed: {str(e)}")


# Request history
st.divider()

if st.session_state.request_count > 0:
    with st.expander("📊 Request History"):
        history_df = None

        if st.session_state.service.history:
            import pandas as pd

            # Convert history to dataframe
            history_list = []
            for h in st.session_state.service.history[-10:]:  # Last 10
                history_list.append({
                    "Time": h["timestamp"][:19],
                    "Status": h["status"],
                    "Model": h.get("model", "N/A"),
                    "Doc Length": h.get("doc_length", "N/A"),
                })

            history_df = pd.DataFrame(history_list)
            st.dataframe(history_df, use_container_width=True)


# Footer with deployment info
st.divider()

st.info("""
### 🚀 Deployment Ready
This service is production-ready and can be deployed to:
- **Streamlit Cloud** - Free, instant deployment
- **Railway.app** - $5/month starter, auto-scaling
- **Docker** - Deploy anywhere with Docker support
- **AWS Lambda** - Serverless with custom handler

See Lesson 3.5 (DevOps) for deployment instructions.
""")

st.caption("Module 3.6 • Capstone Project • Deploy a Mini AI Service")
