"""
Lesson 2.6: Build a Mini Search Demo

OBJECTIVE: Build a production-like semantic search application combining
all concepts from Lessons 2.2-2.5.

BUSINESS SCENARIO: A consulting client needs a searchable knowledge repository.
Employees can quickly find information across company documents.

DEFAULT APPROACH: TF-IDF (lightweight, fast, works everywhere)
OPTIONAL UPGRADES: See Lesson 2.5 README for sentence-transformers or OpenRouter
"""

import os
import json
import streamlit as st
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Dict

# Primary: Cohere embeddings (free tier, semantic)
import cohere
from sklearn.metrics.pairwise import cosine_similarity

# Fallback: TF-IDF semantic search (lightweight)
from sklearn.feature_extraction.text import TfidfVectorizer

# Shared utilities
from shared.streamlit_app import register_lesson
from shared.data_loader import load_sample_corpus

# ============================================================================
# PHASE 1: Setup & Data Loading
# ============================================================================

def load_corpus_from_lesson_2_5():
    """Load corpus and metadata from Lesson 2.5 output."""
    try:
        output_path = Path("../datasets/lesson-05-output.json")
        if output_path.exists():
            with open(output_path, "r") as f:
                data = json.load(f)
                return data.get("lesson_2_5", {})
    except Exception as e:
        st.warning(f"Could not load Lesson 2.5 data: {e}")
    return None

def setup_output_dir():
    """Ensure output directory exists."""
    output_dir = Path("../datasets")
    output_dir.mkdir(exist_ok=True)
    return output_dir

def save_demo_output(corpus: Dict[str, str], search_history: List[Dict]):
    """Save demo results for future reference."""
    output_dir = setup_output_dir()
    output_path = output_dir / "lesson-06-output.json"

    data = {
        "lesson_2_6": {
            "corpus": corpus,
            "search_history": search_history,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "document_count": len(corpus),
                "search_count": len(search_history),
                "embedding_method": "TF-IDF"
            }
        }
    }

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

# ============================================================================
# PHASE 2: Search Engine (Cohere Primary, TF-IDF Fallback)
# ============================================================================

@st.cache_resource
def get_cohere_client():
    """Get or create Cohere client."""
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        return None
    return cohere.ClientV2(api_key=api_key)

def build_cohere_engine(corpus: Dict[str, str]) -> Tuple[np.ndarray, List[str], cohere.ClientV2]:
    """Build Cohere embedding search engine."""
    try:
        client = get_cohere_client()
        if not client:
            return None, None, None

        doc_texts = list(corpus.values())
        with st.spinner("🔄 Generating embeddings with Cohere..."):
            response = client.embed(
                texts=doc_texts,
                model="embed-english-v3.0",
                input_type="search_document"
            )

            embeddings_list = []

            # Try Cohere v2+ structure: response.embeddings.float
            if hasattr(response, 'embeddings'):
                emb_data = response.embeddings

                # Method 1: Try .float attribute (Cohere v2+)
                if hasattr(emb_data, 'float'):
                    embeddings_list = emb_data.float
                # Method 2: Try direct iteration on embeddings object
                elif hasattr(emb_data, '__iter__'):
                    for item in emb_data:
                        # Check if item has .float attribute
                        if hasattr(item, 'float'):
                            embeddings_list.append(item.float)
                        # Check if item has .embedding attribute
                        elif hasattr(item, 'embedding'):
                            embeddings_list.append(item.embedding)
                        # Otherwise assume it's a list/array
                        else:
                            embeddings_list.append(list(item) if hasattr(item, '__iter__') else item)

            if not embeddings_list:
                raise ValueError("Could not extract embeddings from Cohere response")

            # Convert to numpy array
            embeddings = np.array(embeddings_list).astype("float32")

            # Sanity check: embeddings should be high-dimensional
            if embeddings.ndim != 2:
                raise ValueError(f"Expected 2D array, got {embeddings.ndim}D with shape {embeddings.shape}")
            if embeddings.shape[1] < 10:
                raise ValueError(
                    f"Embeddings too small: shape {embeddings.shape}. "
                    f"Expected 100+ dimensions, got {embeddings.shape[1]}."
                )

        return embeddings, doc_texts, client
    except Exception as e:
        st.warning(f"⚠️ Cohere embedding failed: {e}. Using TF-IDF.")
        return None, None, None

def semantic_search_cohere(query: str, corpus: Dict[str, str], embeddings: np.ndarray,
                          doc_texts: List[str], client: cohere.ClientV2, top_k: int = 5) -> List[Dict]:
    """Cohere embedding based semantic search."""
    try:
        response = client.embed(
            texts=[query],
            model="embed-english-v3.0",
            input_type="search_query"
        )

        # Extract query embedding using same logic as document embeddings
        query_embedding = None

        if hasattr(response, 'embeddings'):
            emb_data = response.embeddings

            # Method 1: Try .float attribute (Cohere v2+)
            if hasattr(emb_data, 'float'):
                query_embedding = np.array([emb_data.float[0]]).astype("float32")
            # Method 2: Try direct indexing
            elif hasattr(emb_data, '__getitem__'):
                query_embedding = np.array([emb_data[0]]).astype("float32")
            # Method 3: Convert to list first
            else:
                emb_list = list(emb_data) if hasattr(emb_data, '__iter__') else [emb_data]
                query_embedding = np.array([emb_list[0]]).astype("float32")

        if query_embedding is None:
            raise ValueError("Could not extract query embedding")

    except Exception as e:
        st.error(f"Query embedding failed: {e}")
        return []

    similarities = cosine_similarity(query_embedding, embeddings)[0]
    doc_names = list(corpus.keys())
    sorted_indices = np.argsort(similarities)[::-1][:top_k]
    results = []

    for idx in sorted_indices:
        relevance = float(similarities[idx])
        if relevance < 0.1:
            continue

        doc_text = doc_texts[idx]
        snippet = doc_text[:300].strip()
        if len(doc_text) > 300:
            snippet += "..."

        results.append({
            "document": doc_names[idx],
            "snippet": snippet,
            "full_text": doc_text,
            "relevance": relevance,
            "relevance_percent": int(relevance * 100)
        })

    return results

def build_search_engine(corpus: Dict[str, str]) -> Tuple[TfidfVectorizer, np.ndarray]:
    """
    Build TF-IDF search engine.
    Returns (vectorizer, tfidf_matrix) for searching.
    """
    doc_texts = list(corpus.values())
    vectorizer = TfidfVectorizer(lowercase=True, stop_words="english", max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(doc_texts)
    return vectorizer, tfidf_matrix

def semantic_search(query: str, corpus: Dict[str, str], vectorizer: TfidfVectorizer,
                   tfidf_matrix: np.ndarray, top_k: int = 5) -> List[Dict]:
    """
    Perform TF-IDF based semantic search and return ranked results with metadata.
    Returns list of dicts with: document_name, snippet, relevance_score, full_text
    """
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, tfidf_matrix)[0]

    doc_names = list(corpus.keys())
    doc_texts = list(corpus.values())

    # Get top K
    sorted_indices = np.argsort(similarities)[::-1][:top_k]
    results = []

    for idx in sorted_indices:
        relevance = float(similarities[idx])
        if relevance < 0.001:  # Filter near-zero matches
            continue

        doc_text = doc_texts[idx]
        snippet = doc_text[:300].strip()
        if len(doc_text) > 300:
            snippet += "..."

        results.append({
            "document": doc_names[idx],
            "snippet": snippet,
            "full_text": doc_text,
            "relevance": relevance,
            "relevance_percent": int(relevance * 100)
        })

    return results

# ============================================================================
# PHASE 3: Streamlit Dashboard
# ============================================================================

def render_lesson_2_6():
    """Main Streamlit interface for Lesson 2.6 - Mini Search Demo."""

    st.set_page_config(page_title="Semantic Search Demo", layout="wide")

    # ========================================================================
    # SECTION 0: Initialization & Data Loading
    # ========================================================================

    if "corpus" not in st.session_state:
        lesson_2_5_data = load_corpus_from_lesson_2_5()
        if lesson_2_5_data and lesson_2_5_data.get("corpus"):
            st.session_state.corpus = lesson_2_5_data.get("corpus", {})
            st.session_state.corpus_loaded_from = "Lesson 2.5 Output"
            st.session_state.data_source = "../datasets/lesson-05-output.json"
        else:
            # Load shared sample corpus as fallback
            corpus, data_source = load_sample_corpus()
            st.session_state.corpus = corpus
            st.session_state.corpus_loaded_from = "Sample Data"
            st.session_state.data_source = data_source

    if "search_history" not in st.session_state:
        st.session_state.search_history = []

    if "index" not in st.session_state and len(st.session_state.corpus) > 0:
        # Try Cohere first, fall back to TF-IDF
        embeddings, doc_texts, client = build_cohere_engine(st.session_state.corpus)

        if embeddings is not None and client is not None:
            # Cohere succeeded
            st.session_state.embeddings = embeddings
            st.session_state.doc_texts = doc_texts
            st.session_state.client = client
            st.session_state.search_method = "Cohere"
        else:
            # Fallback to TF-IDF
            st.session_state.vectorizer, st.session_state.tfidf_matrix = build_search_engine(
                st.session_state.corpus
            )
            st.session_state.search_method = "TF-IDF"

    # ========================================================================
    # HEADER SECTION
    # ========================================================================

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>🔍 Semantic Search Demo</h1>", unsafe_allow_html=True)
        st.markdown(
            "<p style='text-align: center; color: gray;'>Find information across documents using natural language</p>",
            unsafe_allow_html=True
        )

    # ========================================================================
    # SECTION 1: Corpus Stats & Management
    # ========================================================================

    with st.expander("📚 Corpus Information", expanded=True):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Documents", len(st.session_state.corpus))
        with col2:
            st.metric("Loaded from", st.session_state.corpus_loaded_from)
        with col3:
            if st.session_state.corpus:
                total_chars = sum(len(text) for text in st.session_state.corpus.values())
                st.metric("Total Size", f"{total_chars / 1024:.1f} KB")
        with col4:
            st.metric("Method", "TF-IDF")

        # Data source indicator
        st.caption(f"📁 Data loaded from: `{st.session_state.data_source}`")

        # Show document list
        if st.session_state.corpus:
            st.markdown("**Documents in library:**")
            for i, doc_name in enumerate(st.session_state.corpus.keys(), 1):
                st.write(f"{i}. {doc_name}")

        # Add document during session
        st.divider()
        st.markdown("**➕ Add More Documents to Search**")
        st.caption("_Step 1: Give it a name | Step 2: Paste the text content_")

        col1, col2 = st.columns([2, 1])
        with col1:
            new_doc_name = st.text_input(
                "📝 Document name (e.g., 'Policy Update', 'FAQ Section'):",
                key="add_doc_name",
                placeholder="Enter a title or label for this document"
            )
        with col2:
            add_doc_btn = st.button("➕ Next", use_container_width=True, help="Click to continue to content input")

        if add_doc_btn and new_doc_name:
            if "add_doc_text" not in st.session_state:
                st.session_state.add_doc_text = True

        if st.session_state.get("add_doc_text", False):
            new_doc_text = st.text_area(
                "📄 Paste document content:",
                height=100,
                key="new_doc_content",
                placeholder="Paste your document text here (can be any length)"
            )

            if st.button("💾 Save & Rebuild Index", use_container_width=True):
                st.session_state.corpus[new_doc_name] = new_doc_text
                st.session_state.vectorizer, st.session_state.tfidf_matrix = build_search_engine(
                    st.session_state.corpus
                )
                st.session_state.add_doc_text = False
                st.success(f"✅ Added '{new_doc_name}' and rebuilt search index")
                st.rerun()

    # ========================================================================
    # SECTION 2: Search Bar (HERO)
    # ========================================================================

    st.markdown("---")

    if len(st.session_state.corpus) == 0:
        st.warning("⚠️ No documents loaded. Add documents using the Corpus Information section above.")
    else:
        # Hero search bar
        col1, col2 = st.columns([4, 1])
        with (col1):
            search_query = st.text_input(
                "🔎 Search across documents",
                value=st.session_state.get("last_search_query", ""),
                placeholder="What are you looking for? (e.g., 'What is the remote work policy?')",
                help="Type a natural language question or keywords"
            )
        with col2:
            search_button_clicked = st.button("🔍 Search", use_container_width=True, help="Click to search or press Enter")

        # Suggested queries
        st.markdown("**Try these searches:**")
        col1, col2, col3 = st.columns(3)
        suggestions = [
            "What are the benefits?",
            "Payment terms and compensation",
            "Remote work policy"
        ]

        with col1:
            if st.button(suggestions[0], use_container_width=True):
                search_query = suggestions[0]
                search_button_clicked = True

        with col2:
            if st.button(suggestions[1], use_container_width=True):
                search_query = suggestions[1]
                search_button_clicked = True

        with col3:
            if st.button(suggestions[2], use_container_width=True):
                search_query = suggestions[2]
                search_button_clicked = True

        # ====================================================================
        # SECTION 3: Search Results
        # ====================================================================

        if search_query and (search_button_clicked or search_query != st.session_state.get("last_search_query", "")):
            with st.spinner("🔍 Searching..."):
                # Use appropriate search method
                if st.session_state.search_method == "Cohere":
                    results = semantic_search_cohere(
                        search_query,
                        st.session_state.corpus,
                        st.session_state.embeddings,
                        st.session_state.doc_texts,
                        st.session_state.client,
                        top_k=5
                    )
                else:  # TF-IDF
                    results = semantic_search(
                        search_query,
                        st.session_state.corpus,
                        st.session_state.vectorizer,
                        st.session_state.tfidf_matrix,
                        top_k=5
                    )

                # Track search history and save query
                st.session_state.search_history.append({
                    "query": search_query,
                    "timestamp": datetime.now().isoformat(),
                    "result_count": len(results)
                })
                st.session_state.last_search_query = search_query
                st.session_state.search_results = results

            st.markdown("---")
            st.markdown(f"## Search Results ({len(results)} documents)")
            st.caption(f"Using: **{st.session_state.search_method}**")

            # Display results as cards
            for idx, result in enumerate(results, 1):
                with st.container(border=True):
                    # Header: Document name + Relevance score
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{idx}. {result['document']}**")
                    with col2:
                        st.metric(
                            "Match Score",
                            f"{result['relevance_percent']}%",
                            delta=None,
                            label_visibility="collapsed"
                        )

                    # Relevance bar (visual indicator)
                    relevance_pct = result['relevance_percent']
                    bar_color = "🟢" if relevance_pct > 70 else "🟡" if relevance_pct > 50 else "🔴"
                    st.markdown(
                        f"{bar_color} Relevance: {'█' * (relevance_pct // 10)}{'░' * (10 - relevance_pct // 10)}"
                    )

                    # Snippet
                    st.markdown("**Preview:**")
                    st.markdown(f"> {result['snippet']}")

                    # View full document
                    if st.button(
                        "📄 View Full Document",
                        key=f"view_{idx}",
                        use_container_width=True
                    ):
                        with st.expander(f"Full content: {result['document']}", expanded=True):
                            st.text(result['full_text'])

                    st.divider()

            # Pagination info
            st.caption(f"Showing {len(results)} results. Results are ranked by relevance to your query.")

        # ====================================================================
        # SECTION 4: Search Analytics
        # ====================================================================

        if st.session_state.search_history:
            with st.expander("📊 Search History", expanded=False):
                st.markdown(f"**Total searches:** {len(st.session_state.search_history)}")

                for search in st.session_state.search_history[-5:]:  # Last 5
                    st.write(f"• \"{search['query']}\" → {search['result_count']} results")

    # ========================================================================
    # SECTION 5: Takeaways & Next Steps
    # ========================================================================

    st.markdown("---")
    st.subheader("🎓 What You've Built")
    st.markdown(
        """
    This semantic search application demonstrates:

    ✅ **Lesson 2.2 (Tokens)**: Understanding context and token budgets for your queries

    ✅ **Lesson 2.4 (RAG)**: This IS retrieval-augmented generation! We retrieve relevant docs and can use them to augment prompts.

    ✅ **Lesson 2.5 (Embeddings)**: Converting documents and queries to semantic vectors for meaning-based matching

    ✅ **Vector Search**: TF-IDF enables fast retrieval across your document corpus

    ---

    **Real-world applications:**
    - Knowledge base search (internal docs, FAQ)
    - Legal document discovery
    - Medical record search
    - HR policy lookup
    - Foundation for RAG systems (feed top-K results to LLM for generating answers)
    """
    )

    # Save final state
    save_demo_output(st.session_state.corpus, st.session_state.search_history)

# ============================================================================
# PHASE 4: Register & Entry Point
# ============================================================================

register_lesson("Lesson 2.6: Mini Search Demo", render_lesson_2_6)

if __name__ == "__main__":
    render_lesson_2_6()
