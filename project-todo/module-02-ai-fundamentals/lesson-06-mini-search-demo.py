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
- Implement each PHASE in order
- Use completed version as reference
- Load corpus from Lesson 2.5 automatically
- Build polished, intuitive UI
- Focus: search bar + results to showcase semantic search power
- Allow adding documents mid-session
- Show corpus stats and search history
- Save results to datasets/lesson-06-output.json

DEPENDENCIES:
- Same as Lesson 2.5: sentence-transformers, faiss-cpu
"""

# ============================================================================
# PHASE 1: Imports & Setup Functions
# ============================================================================
# TODO: Import required libraries:
#   - json, streamlit, numpy, datetime, Path, List, Tuple, Dict
#   - SentenceTransformer, faiss
#   - register_lesson
#
# TODO: Implement load_embedding_model():
#   - Use @st.cache_resource decorator
#   - Load SentenceTransformer("all-MiniLM-L6-v2")
#   - Return model
#
# TODO: Implement load_corpus_from_lesson_2_5():
#   - Read ../datasets/lesson-05-output.json
#   - Extract corpus from lesson_2_5 key
#   - Return corpus dict or None
#
# TODO: Implement setup_output_dir():
#   - Create ../datasets/ if not exists
#   - Return path
#
# TODO: Implement save_demo_output(corpus, search_history):
#   - Save to ../datasets/lesson-06-output.json
#   - Include corpus, search_history, metadata (timestamp, doc_count, search_count, model)

# ============================================================================
# PHASE 2: Search Engine
# ============================================================================
# TODO: Implement build_search_engine(corpus, model):
#   - Get doc_texts from corpus values
#   - Encode texts: model.encode(doc_texts).astype("float32")
#   - Create FAISS IndexFlatL2
#   - Add embeddings to index
#   - Return (index, embeddings_array)
#
# TODO: Implement semantic_search(query, corpus, index, embeddings, model, top_k=5):
#   - Encode query: model.encode([query]).astype("float32")
#   - Search FAISS: index.search(query_embedding, top_k)
#   - Get distances and indices
#   - For each result:
#     - Convert distance to relevance (0-1): relevance = 1 / (1 + distance)
#     - Extract doc_name from corpus keys
#     - Extract snippet: first 300 chars of doc_text
#     - Append to + "..." if longer
#   - Return list of dicts:
#     {
#       "document": name,
#       "snippet": first 300 chars,
#       "full_text": full document,
#       "relevance": float (0-1),
#       "relevance_percent": int (0-100)
#     }

# ============================================================================
# PHASE 3: Session State Initialization
# ============================================================================
# TODO: At start of render_lesson_2_6():
#   - If "corpus" not in st.session_state:
#     - Load from Lesson 2.5 via load_corpus_from_lesson_2_5()
#     - Set corpus to loaded corpus or empty dict
#     - Set corpus_loaded_from = "Lesson 2.5" or "Empty"
#   - If "search_history" not in st.session_state:
#     - Initialize as empty list
#   - If "index" not in st.session_state AND corpus not empty:
#     - Build search engine via build_search_engine()
#     - Store index and embeddings in session_state

# ============================================================================
# PHASE 4: Streamlit Page Setup & Header
# ============================================================================
# TODO: In render_lesson_2_6():
#   - Set page config: page_title="Semantic Search Demo", layout="wide"
#   - Load embedding model via load_embedding_model()
#   - Create header section using 3-column layout:
#     - COL 1, 2, 3: middle column centered heading "<h1>🔍 Semantic Search Demo</h1>"
#     - Subheading: "<p style='text-align: center; color: gray;'>Find info across documents...</p>"
#     - Use st.markdown with unsafe_allow_html=True for styling

# ============================================================================
# PHASE 5: Corpus Stats & Document Management
# ============================================================================
# TODO: Create expander "📚 Corpus Information" (expanded=True):
#   - 4-column metrics row:
#     COL 1: st.metric("Documents", len(corpus))
#     COL 2: st.metric("Loaded from", corpus_loaded_from)
#     COL 3: Total size in KB (sum of all doc chars / 1024)
#     COL 4: st.metric("Model", "MiniLM-L6")
#   - List all documents: "1. Doc Name", "2. Doc Name", etc.
#   - Add document section:
#     - Divider (st.divider())
#     - "Add more documents:" heading
#     - 2-column row:
#       COL 1: text_input for new_doc_name
#       COL 2: button "➕ Add"
#     - If button clicked AND doc_name provided:
#       - Set session_state.add_doc_text = True
#     - If session_state.add_doc_text:
#       - text_area for new_doc_content (height=100)
#       - Button "💾 Save & Rebuild Index"
#       - On click:
#         - Add to corpus: corpus[new_doc_name] = text
#         - Rebuild index: build_search_engine()
#         - Reset session_state.add_doc_text = False
#         - Show success message
#         - st.rerun()

# ============================================================================
# PHASE 6: Hero Search Bar & Suggestions
# ============================================================================
# TODO: Add st.markdown("---") divider
#   - Check if corpus is empty:
#     - If empty: st.warning("No documents loaded...")
#     - If not empty: continue
#   - Hero search input:
#     - st.text_input with large placeholder
#     - Placeholder: "🔎 What are you looking for? (e.g., 'What is the remote work policy?')"
#   - Suggested queries section:
#     - Heading: "Try these searches:"
#     - 3 columns with buttons:
#       - "What are the benefits?"
#       - "Payment terms and compensation"
#       - "Remote work policy"
#     - Each button: if clicked, set search_query to suggestion text

# ============================================================================
# PHASE 7: Search Execution & Results Display
# ============================================================================
# TODO: If search_query is not empty:
#   - Spinner: "🔍 Searching..."
#   - Call semantic_search() with query, corpus, index, embeddings, model, top_k=5
#   - Append to search_history:
#     {
#       "query": search_query,
#       "timestamp": datetime.now().isoformat(),
#       "result_count": len(results)
#     }
#   - st.markdown("---")
#   - Heading: "## Search Results ({len(results)} documents)"
#
#   For each result (enumerate 1 to len):
#   - st.container(border=True):
#     - 2-column header:
#       COL 1: st.markdown(f"**{idx}. {result['document']}**")
#       COL 2: st.metric("Match Score", f"{result['relevance_percent']}%", label_visibility="collapsed")
#     - Relevance bar visual:
#       - Use emoji: 🟢 if >70%, 🟡 if >50%, 🔴 otherwise
#       - Bar: █ (filled) for relevance % / 10, ░ (empty) for rest
#       - Show as markdown: "🟢 Relevance: ████░░░░░░"
#     - Snippet section:
#       - Heading: "**Preview:**"
#       - Markdown quote: st.markdown(f"> {result['snippet']}")
#     - View full button:
#       - st.button("📄 View Full Document", key=f"view_{idx}", use_container_width=True)
#       - On click: open expander with full document text
#     - st.divider()
#
#   - After all results: st.caption("Showing X results. Ranked by relevance...")

# ============================================================================
# PHASE 8: Search History (Optional)
# ============================================================================
# TODO: If search_history is not empty:
#   - st.expander("📊 Search History", expanded=False):
#     - Display: f"**Total searches:** {len(search_history)}"
#     - Loop through last 5 searches:
#       - st.write(f"• \"{query}\" → {result_count} results")

# ============================================================================
# PHASE 9: Takeaways & Persistence
# ============================================================================
# TODO: st.markdown("---")
#   - st.subheader("🎓 What You've Built")
#   - Display markdown explaining:
#     - How this combines Lessons 2.2, 2.4, 2.5
#     - Token understanding (2.2)
#     - RAG concept (2.4)
#     - Embeddings in action (2.5)
#     - Real-world applications (HR search, legal discovery, RAG systems)
#   - Call save_demo_output(corpus, search_history)

# ============================================================================
# PHASE 10: Registration & Entry Point
# ============================================================================
# TODO: Call register_lesson():
#   - Register "Lesson 2.6: Mini Search Demo"
#   - Pass render_lesson_2_6 function
#
# TODO: Add if __name__ == "__main__":
#   - Call render_lesson_2_6()

# ============================================================================
# EXPECTED OUTPUT (in datasets/lesson-06-output.json):
# ============================================================================
# {
#   "lesson_2_6": {
#     "corpus": {
#       "Employment Agreement": "EMPLOYMENT AGREEMENT\n\n1. POSITION...",
#       ...
#     },
#     "search_history": [
#       {
#         "query": "What is the remote work policy?",
#         "timestamp": "2024-06-22T16:30:00.123456",
#         "result_count": 5
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
