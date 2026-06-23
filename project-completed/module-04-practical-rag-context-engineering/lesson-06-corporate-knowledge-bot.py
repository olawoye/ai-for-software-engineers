"""
Lesson 4.6: Mini-App - Corporate Knowledge Bot (Capstone)

Build a deployable RAG knowledge assistant combining ingestion, embeddings,
retrieval, storage, prompt assembly, and user interaction into complete app.

Run: streamlit run lesson-06-corporate-knowledge-bot.py
"""

import os
import streamlit as st
from pathlib import Path
from datetime import datetime

from shared.embeddings import EmbeddingEngine
from shared.vector_store import VectorStore
from shared.retriever import Retriever
from shared.rag_pipeline import RAGPipeline, RAGEvaluator
from shared.prompts import format_context, format_citations


st.set_page_config(page_title="Corporate Knowledge Bot", layout="wide")

st.title("🤖 Corporate Knowledge Bot")
st.markdown("""
Semantic search over company knowledge with RAG-powered answers.
Built with embeddings, vector search, and LLM augmentation.
""")


class KnowledgeBot:
    """Corporate knowledge assistant."""

    def __init__(self):
        self.embedding_engine = None
        self.vector_store = None
        self.retriever = None
        self.rag_pipeline = None
        self.query_history = []

    def initialize(self, cohere_key: str = None):
        """Initialize bot components."""
        self.embedding_engine = EmbeddingEngine(
            method="cohere" if cohere_key else "tfidf",
            cohere_api_key=cohere_key,
        )
        self.vector_store = VectorStore(embedding_dim=300)
        self.retriever = Retriever(self.vector_store, self.embedding_engine, top_k=5)
        self.rag_pipeline = RAGPipeline(
            embedding_engine=self.embedding_engine,
            vector_store=self.vector_store,
            retriever=self.retriever,
            llm_client=None,
        )

    def ingest_documents(self, documents, metadata=None):
        """Add documents to knowledge base."""
        self.rag_pipeline.ingest_documents(documents, metadata)

    def search(self, query):
        """Search knowledge base."""
        result = self.rag_pipeline.query(query, top_k=5)
        self.query_history.append({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "results_count": len(result["retrieved_documents"]),
        })
        return result

    def get_stats(self):
        """Get bot statistics."""
        return {
            "total_documents": self.vector_store.get_stats()["total_documents"],
            "queries_made": len(self.query_history),
            "embedding_method": self.embedding_engine.method,
        }


# Initialize session state
if "bot" not in st.session_state:
    cohere_key = os.getenv("COHERE_API_KEY")
    bot = KnowledgeBot()
    bot.initialize(cohere_key)
    st.session_state.bot = bot

    # Load sample knowledge base
    sample_docs = [
        "Our company values innovation, collaboration, and continuous learning.",
        "We support remote work with flexible hours and $500/month home office stipend.",
        "Our tech stack includes Python, Go, TypeScript, and PostgreSQL.",
        "We have offices in San Francisco, London, and Singapore.",
        "All employees receive comprehensive health insurance and unlimited PTO.",
        "We conduct quarterly all-hands meetings and regular team building events.",
        "Promoted employees typically advance every 18-24 months based on performance.",
        "We use Slack for communication and GitHub for code collaboration.",
    ]
    bot.ingest_documents(sample_docs)


# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Knowledge Bot Configuration")

    search_method = st.radio(
        "Search Method",
        ["Semantic (Embeddings)", "Keyword Match"],
        help="Semantic uses AI embeddings; Keyword uses exact word matching",
    )

    top_k = st.slider("Number of Results", 1, 10, 5)

    st.divider()

    # Statistics
    stats = st.session_state.bot.get_stats()
    st.metric("Documents in KB", stats["total_documents"])
    st.metric("Queries Made", stats["queries_made"])
    st.metric("Search Method", search_method.split("(")[0].strip())

    st.divider()

    # Add documents
    if st.button("➕ Add Documents"):
        st.session_state.adding_docs = True

    if st.checkbox("📁 Load Sample Company Handbook"):
        st.info("Sample documents already loaded in the knowledge base.")


# Main search interface
col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_input(
        "🔍 Ask a question about company policies, benefits, or operations",
        placeholder="e.g., What is our remote work policy?",
    )

with col2:
    search_button = st.button("Search", type="primary", use_container_width=True)


# Display results
if search_button and query:
    with st.spinner("Searching knowledge base..."):
        result = st.session_state.bot.search(query)

        if not result["retrieved_documents"]:
            st.warning("No matching documents found.")
        else:
            # Results summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Results Found", len(result["retrieved_documents"]))
            with col2:
                avg_sim = sum(r["similarity"] for r in result["retrieved_documents"]) / len(result["retrieved_documents"])
                st.metric("Avg Similarity", f"{avg_sim:.2f}")
            with col3:
                st.metric("Top Result Score", f"{result['retrieved_documents'][0]['similarity']:.2f}")

            st.divider()

            # Display results
            st.subheader("📄 Retrieved Documents")
            for i, doc_result in enumerate(result["retrieved_documents"], 1):
                with st.expander(f"Result {i} (Relevance: {doc_result['similarity']:.1%})"):
                    st.write(doc_result["document"])
                    st.caption(f"Metadata: {doc_result['metadata']}")


# Suggested queries
st.divider()

st.subheader("💡 Suggested Queries")

suggested_queries = [
    "What is our remote work policy?",
    "Where are our office locations?",
    "What benefits do employees receive?",
    "What technologies do we use?",
    "How do we handle employee growth?",
]

cols = st.columns(2)
for idx, query in enumerate(suggested_queries):
    if idx % 2 == 0:
        col = cols[0]
    else:
        col = cols[1]

    with col:
        if st.button(query, key=f"suggest_{idx}", use_container_width=True):
            st.session_state.last_query = query
            st.rerun()


# Query history
if st.session_state.bot.query_history:
    st.divider()
    with st.expander("📊 Query History"):
        import pandas as pd

        history_data = []
        for h in st.session_state.bot.query_history[-10:]:
            history_data.append({
                "Time": h["timestamp"][:19],
                "Query": h["query"][:50],
                "Results": h["results_count"],
            })

        df = pd.DataFrame(history_data)
        st.dataframe(df, use_container_width=True)


# Footer
st.divider()

st.info("""
### About This Knowledge Bot
- **Embeddings**: Cohere (free tier) with TF-IDF fallback
- **Vector Store**: In-memory with metadata support
- **Retrieval**: Semantic similarity search
- **Purpose**: Employee self-service knowledge access

### Deployment Ready
Deploy to Streamlit Cloud, Railway, or any Kubernetes cluster.
See Lesson 4.6 documentation for deployment steps.
""")

st.caption("Module 4.6 • Capstone Project • Corporate Knowledge Bot • RAG Fundamentals Complete")
