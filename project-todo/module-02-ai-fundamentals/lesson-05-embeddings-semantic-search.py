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
- Implement each STAGE to build semantic search from text to vector search
- Build your own interface: Streamlit UI, CLI, or Python script
- Start with sample corpus or allow learner to add documents
- Compare semantic (embedding-based) vs keyword search
- Save corpus and embeddings to datasets/lesson-05-output.json for Lesson 2.6
- Reference the completed version for inspiration, not step-by-step replication

DEPENDENCIES:
- pip install sentence-transformers faiss-cpu scikit-learn
"""

# ============================================================================
# STAGE 1: Setup & Model Loading
# ============================================================================
# Initialize embedding model and output infrastructure.
# Tasks: load sentence transformer, set up directory for persistence.
# Available utilities:
#   - SentenceTransformer("all-MiniLM-L6-v2") for embedding generation
#   - Optional: @st.cache_resource for caching if using Streamlit
#   - Standard library: json, pathlib.Path, datetime, numpy

# TODO: Add your Stage 1 implementation here


# ============================================================================
# STAGE 2: Corpus Management
# ============================================================================
# Build or load document collection for searching.
# Tasks: define/load sample corpus, allow adding custom documents.
# Key structure: dict mapping document name to text.
# Consider: how many documents, document size, update mechanism.

# TODO: Add your Stage 2 implementation here


# ============================================================================
# STAGE 3: Generate Embeddings
# ============================================================================
# Convert documents to numerical vectors using embedding model.
# Tasks: encode all documents, store embeddings with corpus.
# Key operation: model.encode(doc_texts).astype("float32")
# Utilities available:
#   - SentenceTransformer.encode() returns numpy array
#   - numpy for array operations and serialization

# TODO: Add your Stage 3 implementation here


# ============================================================================
# STAGE 4: Build Search Index
# ============================================================================
# Create efficient similarity search structure (FAISS).
# Tasks: build index from embeddings, enable fast nearest-neighbor search.
# Key operations:
#   - faiss.IndexFlatL2() for L2 distance index
#   - index.add(embeddings) to add embeddings to index
#   - index.search(query_embedding, k) to find top-k neighbors
# Utilities: faiss library for vector database

# TODO: Add your Stage 4 implementation here


# ============================================================================
# STAGE 5: Compare Search Methods
# ============================================================================
# Demonstrate semantic search vs keyword-based search.
# Semantic search: embedding-based similarity (meaning-focused)
# Keyword search: TF-IDF or term frequency (exact term matching)
# Available utilities:
#   - sklearn.feature_extraction.text.TfidfVectorizer for keyword baseline
#   - sklearn.metrics.pairwise.cosine_similarity for comparison
# Task: show when semantic search outperforms keyword search and why.

# TODO: Add your Stage 5 implementation here


# ============================================================================
# STAGE 6: Persistence & Preparation for Lesson 2.6
# ============================================================================
# Save corpus and embeddings for use in next lesson.
# Format: datasets/lesson-05-output.json with {"lesson_2_5": {"corpus": ..., "metadata": ...}}
# Task: ensure Lesson 2.6 can load and use this data for search demo.

# TODO: Add your Stage 6 implementation here
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
