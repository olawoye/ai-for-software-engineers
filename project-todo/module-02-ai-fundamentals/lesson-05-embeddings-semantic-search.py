"""
Lesson 2.5: Embeddings & Semantic Search (TODO - Scaffold)

OBJECTIVE: Learn how embeddings enable semantic search on document meaning.
Generate embeddings, build vector search, and understand how modern retrieval works.

BUSINESS SCENARIO: A legal firm wants to search thousands of contracts using
natural language ("What are the payment terms?") instead of exact keyword matches.

By the end of this lesson, students will:
- Generate embeddings from text
- Build semantic search on a document corpus
- Compare semantic vs keyword search
- Visualize and understand retrieval quality
- Create reusable corpus for Lesson 2.6

INSTRUCTIONS:
- Implement each PHASE in order
- Use the completed version as reference
- Start with sample corpus, allow learner to add more
- Generate embeddings using sentence-transformers
- Use FAISS for fast similarity search
- Provide side-by-side semantic vs keyword comparison
- Show similarity visualization (bar chart)
- Save corpus to datasets/lesson-05-output.json for Lesson 2.6

DEPENDENCIES:
- pip install sentence-transformers faiss-cpu scikit-learn
"""

# ============================================================================
# PHASE 1: Imports & Setup
# ============================================================================
# TODO: Import required libraries:
#   - json, streamlit, numpy, datetime, Path, List, Tuple, Dict
#   - SentenceTransformer from sentence_transformers
#   - faiss (vector database)
#   - cosine_similarity from sklearn.metrics.pairwise
#   - TfidfVectorizer from sklearn.feature_extraction.text
#   - matplotlib for visualization
#   - register_lesson from shared.streamlit_app
#
# TODO: Define SAMPLE_CORPUS dict with 5 realistic documents:
#   - Employment Agreement
#   - Confidentiality Agreement
#   - Remote Work Policy
#   - Code of Conduct
#   - Contractor Agreement
#   Each with multi-line text (~200-300 words, realistic content)

# ============================================================================
# PHASE 2: Model & Index Setup
# ============================================================================
# TODO: Implement load_embedding_model():
#   - Use st.cache_resource decorator (for performance)
#   - Load SentenceTransformer("all-MiniLM-L6-v2")
#   - Return model instance
#
# TODO: Implement setup_output_dir():
#   - Create ../datasets/ directory if not exists
#   - Return directory path
#
# TODO: Implement save_corpus_and_embeddings(corpus, embeddings):
#   - Save to ../datasets/lesson-05-output.json
#   - Include corpus text, metadata (timestamp, doc count, embedding model, dimension)
#   - Structure: {"lesson_2_5": {"corpus": {...}, "metadata": {...}}}
#
# TODO: Implement load_corpus_and_embeddings():
#   - Load from ../datasets/lesson-05-output.json if exists
#   - Return data or None
#
# TODO: Implement build_faiss_index(embeddings):
#   - Convert embeddings to float32 numpy array
#   - Create faiss.IndexFlatL2 (L2 distance index)
#   - Add embeddings to index via index.add()
#   - Return (index, embeddings_array)

# ============================================================================
# PHASE 3: Search Functions
# ============================================================================
# TODO: Implement semantic_search(query, corpus, embeddings_array, index, model, top_k=3):
#   - Encode query using model.encode([query]).astype("float32")
#   - Search index using index.search(query_embedding, top_k)
#   - Get back distances and indices from FAISS
#   - Convert L2 distance to similarity: similarity = 1 / (1 + distance)
#   - Return list of (document_name, similarity_score) tuples
#   - Documents should be ordered by similarity (highest first)
#
# TODO: Implement keyword_search(query, corpus, top_k=3):
#   - Use TfidfVectorizer with lowercase=True, stop_words="english"
#   - Fit vectorizer on all document texts + query
#   - Compute cosine_similarity between query vector and doc vectors
#   - Sort by similarity score
#   - Return list of (document_name, similarity_score) tuples

# ============================================================================
# PHASE 4: Streamlit Dashboard - Section 1: Corpus Management
# ============================================================================
# TODO: Implement render_lesson_2_5():
#   - Display title and objective markdown
#   - Load embedding model via load_embedding_model()
#
#   SECTION 1: Document Library
#   - Subheader "Document Library"
#   - Radio button: "Use Sample Docs" or "Add Custom Docs"
#   - Slider: top_k (1-5, default 3)
#   - Initialize corpus = SAMPLE_CORPUS.copy()
#
#   If "Add Custom Docs":
#   - Two columns: doc_name input + "Add Document" button
#   - When button clicked: set session_state.add_doc = True
#   - If session_state.add_doc:
#     - text_area for document content
#     - "Save Document" button to add to corpus
#     - Show success message
#   - Expander: Show all documents in library (list them)

# ============================================================================
# PHASE 5: Streamlit Dashboard - Section 2: Build Index
# ============================================================================
#   SECTION 2: Generate Embeddings
#   - Button: "🔨 Build Embedding Index" (full width)
#   - When clicked:
#     - Spinner: "Generating embeddings..."
#     - Get doc_texts = list(corpus.values())
#     - Call model.encode(doc_texts) to get embeddings
#     - Call build_faiss_index(embeddings) to get index + embeddings_array
#     - Save to session_state: corpus, embeddings, index
#     - Call save_corpus_and_embeddings() for Lesson 2.6
#     - Display metrics: Document count, Embedding dimension, Index size
#     - Show success message

# ============================================================================
# PHASE 6: Streamlit Dashboard - Section 3: Search
# ============================================================================
#   SECTION 3: Semantic Search Demo
#   - Check if "index" in st.session_state:
#     - If not: show info "Click 'Build Index' to enable search"
#     - If yes: continue
#   - text_input for user query (default "What are the payment terms...")
#   - Two columns with buttons:
#     COL 1: "🔍 Semantic Search" button
#       - Call semantic_search() with query, corpus, embeddings, index, model, top_k
#       - Save results to st.session_state.semantic_results
#       - Show success message
#     COL 2: "📖 Keyword Search" button
#       - Call keyword_search() with query, corpus, top_k
#       - Save results to st.session_state.keyword_results
#       - Show success message

# ============================================================================
# PHASE 7: Streamlit Dashboard - Section 3: Display Results (3 Tabs)
# ============================================================================
#   If semantic_results OR keyword_results exist:
#   - Add markdown divider (st.markdown("---"))
#   - Create 3 tabs: "Semantic Search" | "Keyword Search" | "Comparison"
#
#   TAB 1: Semantic Search Results
#   - Heading: "Semantic Search Results"
#   - Info: "Semantic search finds documents based on **meaning**..."
#   - For each result:
#     - 3-column row: [doc_name (3 cols), similarity (1 col), view button]
#     - Button click shows first 500 chars of document
#   - Similarity visualization:
#     - Use matplotlib bar chart: names on Y-axis, similarities on X-axis
#     - Color: steelblue
#     - X-axis range: 0 to 1
#
#   TAB 2: Keyword Search Results
#   - Heading: "Keyword Search Results"
#   - Info: "Keyword search finds documents based on **term frequency**..."
#   - Same layout as Semantic tab
#
#   TAB 3: Comparison
#   - Heading: "Side-by-Side Comparison"
#   - Create dataframe with columns:
#     - Rank (1, 2, 3, ...)
#     - Semantic Results (format: "Doc Name (0.856)")
#     - Keyword Results (format: "Doc Name (0.423)")
#   - Display as st.dataframe(use_container_width=True)
#   - Add markdown explaining differences between semantic and keyword search

# ============================================================================
# PHASE 8: Streamlit Dashboard - Sections 4 & 5: Takeaways & Persistence
# ============================================================================
#   SECTION 4: Key Takeaways
#   - Subheader "Key Takeaways"
#   - Display markdown with ✅ bullet points for:
#     - Embeddings (what they are, why useful)
#     - Vector databases (FAISS, ChromaDB, capabilities)
#     - Semantic vs Keyword search (when to use each)
#     - Real-world use cases (docs, recommendations, duplicate detection, RAG)
#
#   SECTION 5: Data for Lesson 2.6
#   - Subheader "Data for Lesson 2.6"
#   - Call load_corpus_and_embeddings()
#   - If data exists: show success, display corpus metadata
#   - Info: "Lesson 2.6 will use this corpus: X documents"

# ============================================================================
# PHASE 9: Session State & Entry Point
# ============================================================================
# TODO: Initialize session state:
#   - if "add_doc" not in st.session_state: st.session_state.add_doc = False
#
# TODO: Call register_lesson():
#   - Register with name: "Lesson 2.5: Embeddings & Semantic Search"
#   - Pass render_lesson_2_5 as function
#
# TODO: Add if __name__ == "__main__":
#   - Call render_lesson_2_5()

# ============================================================================
# EXPECTED OUTPUT (in datasets/lesson-05-output.json):
# ============================================================================
# {
#   "lesson_2_5": {
#     "corpus": {
#       "Employment Agreement": "EMPLOYMENT AGREEMENT\n\n1. POSITION...",
#       "Confidentiality Agreement": "CONFIDENTIALITY & NDA\n\n1. CONFIDENTIAL...",
#       ...
#     },
#     "metadata": {
#       "timestamp": "2024-06-22T15:45:30.123456",
#       "document_count": 5,
#       "embedding_model": "all-MiniLM-L6-v2",
#       "embedding_dimension": 384
#     }
#   }
# }

# ============================================================================
# TESTING CHECKLIST:
# ============================================================================
# ✅ Embedding model loads (first run may download ~60MB)
# ✅ Sample corpus displays correctly
# ✅ Custom document add/save works
# ✅ Build Index button generates embeddings and FAISS index
# ✅ Semantic search returns 3 most similar docs
# ✅ Keyword search returns 3 matches
# ✅ Results show similarity scores (0.0-1.0 range)
# ✅ Bar chart visualization displays correctly
# ✅ Semantic results differ from keyword results (showing semantic advantage)
# ✅ View document button shows preview
# ✅ Comparison table shows side-by-side results
# ✅ Corpus saved to lesson-05-output.json
# ✅ Metadata includes doc count and embedding dimension
# ✅ Run: streamlit run lesson-05-embeddings-semantic-search.py
# ✅ Deps: pip install -r requirements-module-02.txt
