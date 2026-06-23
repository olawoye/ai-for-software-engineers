"""
Lesson 2.5: Embeddings & Semantic Search

OBJECTIVE: Learn how embeddings enable semantic search on document meaning.
Build semantic search and understand how modern retrieval works.

BUSINESS SCENARIO: A legal firm wants to search thousands of contracts using
natural language ("What are the payment terms?") instead of exact keyword matches.

By the end of this lesson, students will:
- Generate embeddings/vectors from text
- Build semantic search on a document corpus
- Compare semantic vs keyword search
- Understand retrieval quality
- Create reusable corpus for Lesson 2.6

DEFAULT APPROACH: Cohere Embeddings (free tier, semantic search)
SETUP: Sign up for free API key at https://cohere.com (100k requests/month free)
OPTIONAL FALLBACKS:
  - TF-IDF (lightweight, keyword-based, no API key needed)
  - sentence-transformers (local, requires several GBs install)
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

# Fallback: TF-IDF semantic search (lightweight, no API key)
from sklearn.feature_extraction.text import TfidfVectorizer

# OPTIONAL: Uncomment for local embeddings (requires: pip install sentence-transformers faiss-cpu)
# from sentence_transformers import SentenceTransformer
# import faiss

# Shared utilities
from shared.streamlit_app import register_lesson
from shared.data_loader import load_sample_corpus

# ============================================================================
# PHASE 1: Setup & Configuration
# ============================================================================

# Sample document corpus (loaded from shared file)
SAMPLE_CORPUS = {}

def setup_output_dir():
    """Ensure output directory exists."""
    output_dir = Path("../datasets")
    output_dir.mkdir(exist_ok=True)
    return output_dir

def save_corpus_and_metadata(corpus: Dict[str, str], embedding_method: str):
    """Save corpus for Lesson 2.6."""
    output_dir = setup_output_dir()
    output_path = output_dir / "lesson-05-output.json"

    data = {
        "lesson_2_5": {
            "corpus": corpus,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "document_count": len(corpus),
                "embedding_method": embedding_method,
                "embedding_dimension": "varies by method"
            }
        }
    }

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

def load_corpus_and_metadata():
    """Load saved corpus and metadata."""
    try:
        output_path = Path("../datasets/lesson-05-output.json")
        if output_path.exists():
            with open(output_path, "r") as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Could not load previous data: {e}")
    return None

# ============================================================================
# PHASE 2: Embedding Builders (Choose One)
# ============================================================================

# APPROACH 1: Cohere Embeddings (DEFAULT - Free tier, semantic search)
@st.cache_resource
def get_cohere_client():
    """Get or create Cohere client."""
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        return None
    return cohere.ClientV2(api_key=api_key)

def build_cohere_search_engine(corpus: Dict[str, str]) -> Tuple[np.ndarray, List[str], cohere.ClientV2]:
    """
    Build Cohere embedding search engine.
    Returns (embeddings_matrix, doc_texts, client) for searching.
    """
    try:
        client = get_cohere_client()
        if not client:
            st.warning("⚠️ COHERE_API_KEY not set. Falling back to TF-IDF.")
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
                    f"Expected 100+ dimensions, got {embeddings.shape[1]}. "
                    f"Check Cohere API response format."
                )

        return embeddings, doc_texts, client
    except Exception as e:
        st.warning(f"⚠️ Cohere embedding failed: {e}. Falling back to TF-IDF.")
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
        if relevance < 0.1:  # Filter low-relevance matches
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

# APPROACH 2: TF-IDF (FALLBACK - Lightweight, no API key, keyword-based)
def build_tfidf_search_engine(corpus: Dict[str, str]) -> Tuple[TfidfVectorizer, np.ndarray]:
    """
    Build TF-IDF search engine (lightweight, works everywhere).
    Returns (vectorizer, tfidf_matrix) for searching.
    """
    doc_texts = list(corpus.values())
    vectorizer = TfidfVectorizer(lowercase=True, stop_words="english", max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(doc_texts)
    return vectorizer, tfidf_matrix

def semantic_search_tfidf(query: str, corpus: Dict[str, str], vectorizer: TfidfVectorizer,
                         tfidf_matrix: np.ndarray, top_k: int = 5) -> List[Dict]:
    """TF-IDF based semantic search."""
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, tfidf_matrix)[0]

    doc_names = list(corpus.keys())
    doc_texts = list(corpus.values())

    # Get top K
    sorted_indices = np.argsort(similarities)[::-1][:top_k]
    results = []

    for idx in sorted_indices:
        relevance = float(similarities[idx])
        if relevance < 0.001:  # Filter out near-zero matches
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

# APPROACH 2: OpenRouter Embeddings (OPTIONAL - Better quality, requires API key)
# Uncomment to use this instead of TF-IDF
# def build_openrouter_search_engine(corpus: Dict[str, str]):
#     # Requires: export OPENROUTER_API_KEY='...'
#     try:
#         client = get_client("openrouter")
#         doc_texts = list(corpus.values())
#         # Note: OpenRouter may not have public embedding endpoints
#         # For production, use Claude embeddings or OpenAI
#         st.warning("OpenRouter embeddings not yet integrated - using TF-IDF")
#         return build_tfidf_search_engine(corpus)
#     except Exception as e:
#         st.error(f"OpenRouter embedding failed: {e}. Falling back to TF-IDF.")
#         return build_tfidf_search_engine(corpus)

# APPROACH 3: sentence-transformers (OPTIONAL - Best quality, requires several GBs install)
# Uncomment to use: pip install sentence-transformers faiss-cpu
# @st.cache_resource
# def load_embedding_model():
#     return SentenceTransformer("all-MiniLM-L6-v2")
#
# def build_sentence_transformer_engine(corpus: Dict[str, str], model):
#     doc_texts = list(corpus.values())
#     embeddings = model.encode(doc_texts).astype("float32")
#     dimension = embeddings.shape[1]
#     index = faiss.IndexFlatL2(dimension)
#     index.add(embeddings)
#     return index, embeddings
#
# def semantic_search_sentence_transformer(query: str, corpus: Dict[str, str],
#                                         index, embeddings, model, top_k: int = 5):
#     query_embedding = model.encode([query]).astype("float32")
#     distances, indices = index.search(query_embedding, top_k)
#     doc_names = list(corpus.keys())
#     doc_texts = list(corpus.values())
#     results = []
#     for idx, distance in zip(indices[0], distances[0]):
#         relevance = 1 / (1 + distance)
#         doc_text = doc_texts[idx]
#         snippet = doc_text[:300].strip()
#         if len(doc_text) > 300:
#             snippet += "..."
#         results.append({
#             "document": doc_names[idx],
#             "snippet": snippet,
#             "full_text": doc_text,
#             "relevance": relevance,
#             "relevance_percent": int(relevance * 100)
#         })
#     return results

# ============================================================================
# PHASE 3: Streamlit Dashboard
# ============================================================================

def render_lesson_2_5():
    """Main Streamlit interface for Lesson 2.5."""
    st.markdown("## Lesson 2.5: Embeddings & Semantic Search")
    st.markdown(
        """
    Learn how embeddings and vector search enable semantic search on document meaning.
    This lesson uses **Cohere embeddings** (free tier) for true semantic understanding.
    """
    )

    # ========================================================================
    # SECTION 1: API Key Setup & Embedding Method
    # ========================================================================
    st.info(
        "🔑 **Setup Required**: This lesson uses Cohere embeddings (free tier).\n\n"
        "1. [Sign up for free at cohere.com](https://cohere.com) (no credit card needed)\n"
        "2. Get your API key from the dashboard\n"
        "3. Set it as an environment variable: `export COHERE_API_KEY='your-key-here'`\n"
        "4. Restart your Streamlit app\n\n"
        "**Free tier**: 100,000 requests/month - plenty for learning!\n\n"
        "If you don't have an API key, the app will automatically fall back to TF-IDF (keyword-based)."
    )

    with st.expander("⚙️ Embedding Method Details", expanded=False):
        st.markdown("""
        **Primary: Cohere Embeddings (DEFAULT)**
        - ✅ True semantic search (understands meaning, not just keywords)
        - ✅ Free tier: 100k requests/month
        - ✅ Fast and reliable

        **Fallback: TF-IDF**
        - ✅ Lightweight, no API key needed
        - ⚠️ Keyword-based (less semantic understanding)
        - ✅ Good for learning basics

        **Optional: sentence-transformers (Local)**
        - ✅ Best quality, runs locally
        - ⚠️ Requires `pip install sentence-transformers faiss-cpu` (~ several GBs)
        - ✅ No API key needed

        See README for setup instructions.
        """)

    # ========================================================================
    # SECTION 1B: Search Method Selection (For Demos/Comparison)
    # ========================================================================
    st.divider()
    col1, col2 = st.columns([2, 1])
    with col1:
        search_method = st.radio(
            "🔍 **Search Method** (for demo comparison):",
            ["Semantic Search (Cohere)", "Keyword Search (TF-IDF)"],
            horizontal=True,
            help="Semantic: understands meaning | Keyword: matches words only"
        )
    with col2:
        st.write("")  # Spacer for alignment
        if search_method == "Semantic Search (Cohere)":
            st.success("✨ Semantic")
        else:
            st.info("📝 Keyword")

    st.session_state.demo_search_method = search_method
    st.divider()

    # ========================================================================
    # SECTION 2: Document Corpus Management
    # ========================================================================
    st.subheader("1️⃣ Document Library")

    col1, col2 = st.columns([2, 1])
    with col1:
        corpus_source = st.radio("Corpus source:", ["Use Sample Docs", "Add Custom Docs"])
    with col2:
        top_k = st.slider("Top K results:", 1, 5, 3)

    # Load shared corpus or start with empty
    if corpus_source == "Use Sample Docs":
        corpus, data_source = load_sample_corpus()
        if not corpus:
            st.error("Could not load sample corpus.")
            corpus = {}
        st.success(f"✅ Loaded {len(corpus)} sample documents")
        st.caption(f"📁 Sample data loaded from: `{data_source}`")
    else:
        corpus = {}
        data_source = "custom"

    if corpus_source == "Add Custom Docs":
        st.markdown("**Add documents to the library:**")
        col1, col2 = st.columns(2)

        with col1:
            doc_name = st.text_input("Document name:", value="My Document")
        with col2:
            if st.button("➕ Add Document", use_container_width=True):
                st.session_state.add_doc = True

        if st.session_state.get("add_doc", False):
            doc_text = st.text_area("Document content:", height=100, placeholder="Paste document text here...")
            if st.button("💾 Save Document", use_container_width=True):
                corpus[doc_name] = doc_text
                st.success(f"✅ Added '{doc_name}' to library")
                st.session_state.add_doc = False

    with st.expander(f"📚 Corpus ({len(corpus)} documents)", expanded=False):
        for name in corpus.keys():
            st.write(f"- {name}")

    # ========================================================================
    # SECTION 3: Build Search Index
    # ========================================================================
    st.subheader("2️⃣ Build Search Index")

    if st.button("🔨 Build Search Index", use_container_width=True):
        with st.spinner("Building search index..."):
            # Build based on selected demo method
            if st.session_state.demo_search_method == "Semantic Search (Cohere)":
                # Try Cohere first
                embeddings, doc_texts, client = build_cohere_search_engine(corpus)
                if embeddings is not None and client is not None:
                    st.session_state.corpus = corpus
                    st.session_state.embeddings = embeddings
                    st.session_state.doc_texts = doc_texts
                    st.session_state.client = client
                    st.session_state.embedding_method = "Cohere Semantic"
                else:
                    # Cohere failed, fall back to TF-IDF
                    st.warning("Cohere not available, using TF-IDF instead")
                    vectorizer, tfidf_matrix = build_tfidf_search_engine(corpus)
                    st.session_state.corpus = corpus
                    st.session_state.vectorizer = vectorizer
                    st.session_state.tfidf_matrix = tfidf_matrix
                    st.session_state.embedding_method = "TF-IDF (Fallback)"
            else:
                # User selected TF-IDF keyword search
                vectorizer, tfidf_matrix = build_tfidf_search_engine(corpus)
                st.session_state.corpus = corpus
                st.session_state.vectorizer = vectorizer
                st.session_state.tfidf_matrix = tfidf_matrix
                st.session_state.embedding_method = "TF-IDF Keyword"

            # Save for Lesson 2.6
            save_corpus_and_metadata(corpus, st.session_state.embedding_method)

        st.success("✅ Search index built")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Documents", len(corpus))
        with col2:
            st.metric("Method", st.session_state.embedding_method)
        with col3:
            st.metric("Ready", "✅")

    # ========================================================================
    # SECTION 4: Semantic Search
    # ========================================================================
    st.subheader("3️⃣ Semantic Search Demo")

    if "embedding_method" not in st.session_state:
        st.info("💡 Click 'Build Search Index' above to enable search")
    else:
        query = st.text_input(
            "Enter your search query:",
            value="What are the payment terms and benefits?",
            placeholder="Search across documents..."
        )

        if st.button("🔍 Search", use_container_width=True):
            # Use appropriate search method
            if "Cohere" in st.session_state.embedding_method:
                results = semantic_search_cohere(
                    query,
                    st.session_state.corpus,
                    st.session_state.embeddings,
                    st.session_state.doc_texts,
                    st.session_state.client,
                    top_k
                )
            else:  # TF-IDF keyword search
                results = semantic_search_tfidf(
                    query,
                    st.session_state.corpus,
                    st.session_state.vectorizer,
                    st.session_state.tfidf_matrix,
                    top_k
                )

            st.session_state.search_results = results

        if "search_results" in st.session_state:
            st.markdown("---")
            st.markdown(f"## Search Results ({len(st.session_state.search_results)} matches)")
            st.caption(f"Using: **{st.session_state.embedding_method}**")

            for i, result in enumerate(st.session_state.search_results, 1):
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{i}. {result['document']}**")
                    with col2:
                        st.metric("Match", f"{result['relevance_percent']}%", label_visibility="collapsed")

                    relevance_pct = result['relevance_percent']
                    bar_color = "🟢" if relevance_pct > 70 else "🟡" if relevance_pct > 50 else "🔴"
                    st.markdown(
                        f"{bar_color} Relevance: {'█' * (relevance_pct // 10)}{'░' * (10 - relevance_pct // 10)}"
                    )

                    st.markdown("**Preview:**")
                    st.markdown(f"> {result['snippet']}")

                    if st.button("📄 View Full", key=f"view_{i}", use_container_width=True):
                        with st.expander(f"Full: {result['document']}", expanded=True):
                            st.text(result['full_text'])

                    st.divider()

    # ========================================================================
    # SECTION 5: Key Takeaways
    # ========================================================================
    st.subheader("4️⃣ Key Takeaways")
    st.markdown(
        """
    ✅ **Semantic Search**: Finds meaning, not just keywords

    ✅ **Embeddings**: Convert text to vectors for similarity comparison

    ✅ **TF-IDF**: Lightweight, proven, great for learning

    ✅ **Vector Databases**: FAISS, Pinecone, Weaviate for production

    ✅ **Real-World Uses**: Legal search, HR lookup, RAG systems
    """
    )

    # ========================================================================
    # SECTION 6: Data Persistence
    # ========================================================================
    st.subheader("5️⃣ Corpus for Lesson 2.6")
    corpus_data = load_corpus_and_metadata()
    if corpus_data:
        st.success("✅ Corpus saved")
        meta = corpus_data['lesson_2_5']['metadata']
        st.info(f"📊 {meta['document_count']} docs | Method: {meta['embedding_method']}")

# ============================================================================
# PHASE 4: Register & Entry Point
# ============================================================================

if "add_doc" not in st.session_state:
    st.session_state.add_doc = False

register_lesson("Lesson 2.5: Embeddings & Semantic Search", render_lesson_2_5)

if __name__ == "__main__":
    render_lesson_2_5()
