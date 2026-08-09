"""
Lesson 2.6: Build a Mini Search Demo (TODO - Scaffold)

OBJECTIVE: Build a production-like semantic search application combining all
concepts from Lessons 2.2-2.5 into a single working product.

BUSINESS SCENARIO: A consulting client needs a searchable knowledge repository
where employees can find information using natural language queries.

By the end of this lesson, students will have built:
- A complete semantic search application
- Intuitive search interface with hero search bar
- Results displayed as cards with relevance scores
- Real product-like user experience

INSTRUCTIONS:
- Implement each STAGE to build a complete, polished search application
- Build your own interface: Streamlit UI, CLI, or Python script
- Load corpus from Lesson 2.5 automatically
- Make search intuitive and results clear
- Track search history and corpus stats
- Save final corpus and usage data to datasets/lesson-06-output.json
- Reference the completed version for inspiration, not step-by-step replication

DEPENDENCIES:
- Same as Lesson 2.5: sentence-transformers, faiss-cpu
"""

# ============================================================================
# STAGE 1: Setup & Data Loading
# ============================================================================
# Initialize embedding model and load corpus from Lesson 2.5.
# Tasks: load sentence transformer, load lesson-05-output.json corpus,
#        initialize session state (index, search history).
# Available utilities:
#   - SentenceTransformer("all-MiniLM-L6-v2")
#   - Optional: @st.cache_resource for Streamlit caching
#   - Standard library: json, pathlib.Path, datetime, numpy

# TODO: Add your Stage 1 implementation here


# ============================================================================
# STAGE 2: Build Search Engine
# ============================================================================
# Create FAISS-backed semantic search from corpus embeddings.
# Tasks: encode corpus documents, build vector index, prepare for fast search.
# Key operations:
#   - model.encode(doc_texts) to generate embeddings
#   - faiss.IndexFlatL2() for similarity search
#   - index.search(query_embedding, k) for retrieval
# Utilities: faiss library, numpy for arrays

# TODO: Add your Stage 2 implementation here


# ============================================================================
# STAGE 3: Build User Interface (Your Choice)
# ============================================================================
# Design search interface and interaction model.
# Option A: Streamlit dashboard with search bar, results cards, corpus info
#   - Available: register_lesson() from shared.streamlit_app
# Option B: CLI with prompt-based search and formatted results
# Option C: Python script with file-based search and output
# Goal: make search intuitive and results discoverable.

# TODO: Add your Stage 3 implementation here


# ============================================================================
# STAGE 4: Display Search Results Clearly
# ============================================================================
# Format and present search results to user.
# Display: document name, relevance score, text snippet, option to view full text.
# Consider: result ranking, visual indicators (bars, colors), information hierarchy.
# Optional: visualizations of relevance scores.

# TODO: Add your Stage 4 implementation here


# ============================================================================
# STAGE 5: Track Search History & Corpus Analytics
# ============================================================================
# Monitor usage patterns and corpus metadata.
# Track: search queries, result counts, popular searches.
# Display: corpus stats (doc count, size), search history, model info.
# Purpose: help learners understand search behavior and corpus coverage.

# TODO: Add your Stage 5 implementation here


# ============================================================================
# STAGE 6: Document Management & Persistence
# ============================================================================
# Allow adding documents mid-session and persist final corpus.
# Tasks: update corpus, rebuild search index, save to datasets/lesson-06-output.json.
# Format: {"lesson_2_6": {"corpus": {...}, "search_history": [...], "metadata": {...}}

# TODO: Add your Stage 6 implementation here
#       },
#       ...
#     ],
#     "metadata": {
#       "timestamp": "2024-06-22T16:35:00.123456",
#       "document_count": 5,
#       "search_count": 3,
#       "embedding_model": "all-MiniLM-L6-v2"
#     }
#   }
# }

# ============================================================================
# TESTING CHECKLIST:
# ============================================================================
# ✅ Page loads with hero search bar prominent
# ✅ Corpus loads from Lesson 2.5 automatically
# ✅ Corpus stats display correctly (count, size, model)
# ✅ Document list shows all loaded documents
# ✅ Can add new documents mid-session
# ✅ Adding document rebuilds search index
# ✅ Search bar placeholder is clear and helpful
# ✅ Suggested query buttons work (populate search bar)
# ✅ Typing query and searching returns results
# ✅ Results display as cards with:
#    ✅ Document name (heading)
#    ✅ Relevance score (%), visual bar (🟢/🟡/🔴)
#    ✅ Snippet preview (first 300 chars)
#    ✅ "View Full Document" button
# ✅ Results are sorted by relevance (highest first)
# ✅ Results count shows at bottom
# ✅ Search history tracks queries
# ✅ "What You've Built" section explains concepts
# ✅ Output saved to lesson-06-output.json
# ✅ Run: streamlit run lesson-06-mini-search-demo.py
# ✅ No errors with empty corpus (shows warning)
# ✅ Responsive on desktop and mobile
