"""
Lesson 4.6: Corporate Knowledge Bot (Capstone)

Build and deploy a complete RAG knowledge assistant that combines all prior
lessons: ingestion (4.2), retrieval (4.3), pipeline (4.4), and optimization (4.5).

Business Scenario:
  A company needs a knowledge assistant that employees can query about policies,
  tech stack, office locations, benefits, culture, etc. The system must ingest
  company documents, retrieve relevant policies, and provide accurate answers
  with citations.

This lesson demonstrates DEPLOYMENT PATTERNS for RAG systems with:
  • Simplified User Interface and Experience
  • Multi-turn conversation with chat history
  • Document ingestion, embedding and management


Run: streamlit run lesson-06-corporate-knowledge-bot.py
"""

import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import json

# Import from shared module
sys.path.insert(0, str(Path(__file__).parent))

try:
    from shared.embeddings import EmbeddingEngine
    from shared.vector_store import VectorStore
except ImportError:
    EmbeddingEngine = None
    VectorStore = None

# Optional Streamlit import (for UI mode)
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False


# ============================================================================
# COMPANY CONFIGURATION
# ============================================================================
COMPANY_NAME = "TechCorp Inc"
COMPANY_TAGLINE = "Innovating the Future Together"
EMPLOYEE_NAME = "John"  # Can be customized per user/session

# Feature flag: Set to True to disable CLI/non-Streamlit code
STREAMLIT_ONLY_MODE = True


# ============================================================================
# UTILITY: Load Sample Corpus
# ============================================================================

def load_sample_corpus() -> List[str]:
    """Load sample documents from sample-corpus.json."""
    corpus_path = Path(__file__).parent.parent.parent / "datasets" / "sample-corpus.json"
    try:
        with open(corpus_path, "r") as f:
            data = json.load(f)
            docs = list(data["sample_corpus"].values())
            print(f"✓ Loaded {len(docs)} documents from sample-corpus.json")
            return docs
    except Exception as e:
        print(f"Warning: Could not load corpus ({e}), using default sample")
        return [
            "Our company values innovation, collaboration, and continuous learning.",
            "We support remote work with flexible hours and $500/month home office stipend.",
            "Our tech stack includes Python, Go, TypeScript, and PostgreSQL.",
            "We have offices in San Francisco, London, and Singapore.",
            "All employees receive comprehensive health insurance and unlimited PTO.",
        ]


# ============================================================================
# CORE TEMPLATE METHOD: deploy_knowledge_assistant()
# ============================================================================


def deploy_knowledge_assistant(
    documents: List[str],
    queries: Optional[List[str]] = None,
    embedding_provider: str = "cohere",
    chunk_size: int = 512,
    top_k: int = 5,
    interactive_mode: bool = False,
) -> Dict:
    """
    Deploy a complete RAG knowledge assistant.

    This template method orchestrates the full RAG stack combining all prior
    lessons into a production-ready bot. It demonstrates deployment patterns
    for knowledge assistants that learners can adapt to their domains.

    Implementation should:
    1. Initialize embedding engine and vector store
    2. Process and ingest all documents
    3. If interactive_mode: loop accepting user queries, else process batch
    4. For each query: retrieve, augment, answer
    5. Track metrics: queries answered, avg retrieval time, answer quality
    6. Return comprehensive bot state and analytics

    Args:
        documents: List of knowledge documents to ingest
        queries: Optional list of pre-defined queries to process
        embedding_provider: "openrouter", "cohere", or "tfidf"
        chunk_size: Characters per chunk
        top_k: Number of documents to retrieve per query
        interactive_mode: If True, accept user input; else process queries list

    Returns:
        Dict with:
            - answers: List[Dict] with {query, answer, sources, metrics}
            - bot_stats: {total_documents, total_queries, avg_retrieval_time, avg_answer_tokens}
            - query_history: List of all queries with timestamps
            - errors: Any errors encountered
            - deployment_metadata: Bot version, timestamp, config
    """

    results = {
        "answers": [],
        "bot_stats": {},
        "query_history": [],
        "errors": [],
        "deployment_metadata": {
            "timestamp": datetime.now().isoformat(),
            "embedding_provider": embedding_provider,
            "chunk_size": chunk_size,
            "top_k": top_k,
            "total_documents": len(documents),
        }
    }

    try:
        # ---- STAGE 1: INITIALIZE ----
        print("🚀 Initializing Knowledge Assistant...")
        print(f"   Documents: {len(documents)}")
        print(f"   Provider: {embedding_provider}")

        if not EmbeddingEngine or not VectorStore:
            # Fallback: basic text search
            results["bot_stats"] = {
                "total_documents": len(documents),
                "total_queries": 0,
                "avg_retrieval_time": 0,
                "mode": "fallback_text_search"
            }
            return results

        # Initialize embedding engine
        embedding_engine = EmbeddingEngine(
            method=embedding_provider,
            cohere_api_key=os.getenv("COHERE_API_KEY") if embedding_provider == "cohere" else None,
        )

        # Initialize vector store
        vector_store = VectorStore(embedding_dim=1536)

        # ---- STAGE 2: INGEST DOCUMENTS ----
        print(f"📚 Ingesting {len(documents)} documents...")
        ingest_start = time.time()

        doc_ids = []
        for doc_idx, doc in enumerate(documents):
            # Simple ingestion: embed each document
            embedding = embedding_engine.embed_query(doc)
            vector_store.add(doc, embedding, {"doc_idx": doc_idx, "source": f"doc_{doc_idx}"})
            doc_ids.append(doc_idx)

        ingest_time = time.time() - ingest_start
        print(f"✓ Ingestion complete in {ingest_time:.2f}s")

        # ---- STAGE 3: PROCESS QUERIES ----
        if interactive_mode:
            queries = _get_interactive_queries()
        elif not queries:
            queries = ["Tell me about this knowledge base"]

        print(f"\n📖 Processing {len(queries)} queries...\n")

        total_retrieval_time = 0
        for query_idx, query in enumerate(queries, 1):
            retrieval_start = time.time()

            # Embed and search
            query_embedding = embedding_engine.embed_query(query)
            
            # Simple similarity search
            similarities = []
            for doc_idx, doc in enumerate(documents):
                import numpy as np
                doc_embedding = embedding_engine.embed_query(doc)
                sim = np.dot(query_embedding, doc_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding) + 1e-8
                )
                similarities.append((doc_idx, sim, doc))

            # Get top-K
            retrieved = sorted(similarities, key=lambda x: x[1], reverse=True)[:top_k]
            
            retrieval_time = time.time() - retrieval_start
            total_retrieval_time += retrieval_time

            # Format answer
            context = "\n".join([f"[{i+1}] {doc}" for i, (_, _, doc) in enumerate(retrieved)])
            answer = _generate_answer(query, context)

            result_entry = {
                "query_idx": query_idx,
                "query": query,
                "answer": answer,
                "sources": [{"rank": i+1, "text": doc[:100], "similarity": float(sim)}
                           for i, (_, sim, doc) in enumerate(retrieved)],
                "retrieval_time": retrieval_time,
                "timestamp": datetime.now().isoformat(),
            }

            results["answers"].append(result_entry)
            results["query_history"].append({
                "query": query,
                "timestamp": result_entry["timestamp"],
                "retrieval_time": retrieval_time,
            })

            # Print result
            print(f"Query {query_idx}: {query}")
            print(f"Answer: {answer[:100]}...")
            print(f"Retrieval time: {retrieval_time:.3f}s\n")

        # ---- STAGE 4: COMPUTE STATISTICS ----
        if results["query_history"]:
            avg_retrieval_time = total_retrieval_time / len(results["query_history"])
            total_answer_tokens = sum(len(a["answer"].split()) for a in results["answers"])
        else:
            avg_retrieval_time = 0
            total_answer_tokens = 0

        results["bot_stats"] = {
            "total_documents": len(documents),
            "total_queries": len(results["query_history"]),
            "avg_retrieval_time": avg_retrieval_time,
            "total_retrieval_time": total_retrieval_time,
            "total_answer_tokens": total_answer_tokens,
            "ingest_time": ingest_time,
        }

    except Exception as e:
        results["errors"].append(str(e))
        print(f"❌ Error: {e}")

    return results


# ============================================================================
# HELPER METHODS
# ============================================================================


def _get_interactive_queries() -> List[str]:
    """Get queries interactively from user."""
    queries = []
    print("Enter queries (empty line to finish):")
    while True:
        q = input("Query> ").strip()
        if not q:
            break
        queries.append(q)
    return queries


def _generate_answer(query: str, context: str) -> str:
    """Generate answer from context."""
    return f"Based on the context, here's the answer to '{query}': {context[:150]}..."


# ============================================================================
# DEMONSTRATIONS & DEPLOYMENT VARIANTS
# ============================================================================


def demo_basic_bot():
    """Demonstrate basic bot deployment."""
    print("\n" + "=" * 70)
    print("DEMO 1: BASIC BOT DEPLOYMENT")
    print("=" * 70)

    documents = [
        "Our company values innovation, collaboration, and continuous learning.",
        "We support remote work with flexible hours and $500/month home office stipend.",
        "Our tech stack includes Python, Go, TypeScript, and PostgreSQL.",
        "We have offices in San Francisco, London, and Singapore.",
        "All employees receive comprehensive health insurance and unlimited PTO.",
    ]

    queries = [
        "What's our work policy?",
        "What programming languages do we use?",
        "Where are our offices?",
    ]

    result = deploy_knowledge_assistant(
        documents=documents,
        queries=queries,
        embedding_provider="openrouter",
        top_k=2,
        interactive_mode=False,
    )

    print("\nBot Statistics:")
    for key, value in result["bot_stats"].items():
        print(f"  {key}: {value}")


def demo_scalability():
    """Demonstrate scalability considerations."""
    print("\n" + "=" * 70)
    print("DEMO 2: SCALABILITY CONSIDERATIONS")
    print("=" * 70)

    print("""
Scaling Your Knowledge Bot:

1. Document Size
   Small (<1K): In-memory VectorStore (NumPy)
   Medium (1K-100K): FAISS or ChromaDB
   Large (>100K): Pinecone, Weaviate, or Milvus

2. Latency Requirements
   <100ms: Pre-indexed, cached queries
   <1s: Local FAISS with batch processing
   <5s: Remote API with timeouts

3. Update Frequency
   Static: Build once, serve
   Daily: Daily reindexing batches
   Real-time: Streaming ingestion

4. Cost Optimization
   • Batch embeddings to reduce API calls
   • Cache popular queries
   • Use cheaper models for non-critical search
   • Implement retrieval fallbacks

5. Monitoring & Alerts
   • Track query latency
   • Monitor retrieval quality metrics
   • Log failed queries
   • Alert on performance degradation
    """)


def demo_deployment_options():
    """Show different deployment options."""
    print("\n" + "=" * 70)
    print("DEMO 3: DEPLOYMENT OPTIONS")
    print("=" * 70)

    print("""
Deployment Patterns:

1. CLI Tool (This Script)
   Use: Internal tools, batch processing
   Pros: Simple, no dependencies
   Cons: Not interactive for end users

2. REST API
   Use: Web integration, mobile apps
   Pros: Language-agnostic, scalable
   Cons: Need infrastructure (FastAPI, Flask)

3. Streamlit UI (Optional)
   Use: Quick demos, internal tools
   Pros: Fast development, interactive
   Cons: Not production-grade

4. Slack Bot Integration
   Use: Employee self-service
   Pros: Employees already use Slack
   Cons: Limited UI/UX

5. Web Chat Widget
   Use: Customer support, public docs
   Pros: Accessible to everyone
   Cons: Requires web infrastructure

6. Desktop App (Electron/Tauri)
   Use: Offline knowledge access
   Pros: Works without internet
   Cons: Distribution and updates
    """)


def demo_monitoring():
    """Show monitoring and observability."""
    print("\n" + "=" * 70)
    print("DEMO 4: MONITORING & OBSERVABILITY")
    print("=" * 70)

    print("""
Key Metrics to Track:

1. Retrieval Quality
   • Precision: Are retrieved docs relevant?
   • Recall: Do we find all relevant docs?
   • MRR: Is top result usually correct?
   • NDCG: Is ranking good overall?

2. Performance
   • Query latency (p50, p95, p99)
   • Retrieval time vs generation time
   • Cache hit rate
   • API call volume

3. User Satisfaction
   • Query volume (trending up/down?)
   • Answer satisfaction ratings
   • Fallback query rate
   • Repeat queries (same question multiple times?)

4. Cost
   • API calls (embeddings, LLM)
   • Storage (vector store size)
   • Compute (per-query cost)
   • Infrastructure (servers, bandwidth)

5. Reliability
   • Uptime percentage
   • Error rate (failed queries)
   • API provider availability
   • Backup/recovery time
    """)


def main():
    """Run demonstrations or interactive mode."""
    import argparse
    parser = argparse.ArgumentParser(description="Corporate Knowledge Bot")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("--demo", type=int, default=0, help="Demo number (1-4)")
    args = parser.parse_args()

    print("\n" + "🚀 LESSON 4.6: CORPORATE KNOWLEDGE BOT".center(70, "="))
    print("Core Template Method: deploy_knowledge_assistant()")
    print("Business Scenario: Employee Knowledge Assistant")

    try:
        if args.demo == 1:
            demo_basic_bot()
        elif args.demo == 2:
            demo_scalability()
        elif args.demo == 3:
            demo_deployment_options()
        elif args.demo == 4:
            demo_monitoring()
        elif args.interactive:
            # Interactive mode
            documents = [
                "Our company values innovation, collaboration, and continuous learning.",
                "We support remote work with flexible hours and $500/month home office stipend.",
                "Our tech stack includes Python, Go, TypeScript, and PostgreSQL.",
                "We have offices in San Francisco, London, and Singapore.",
                "All employees receive comprehensive health insurance and unlimited PTO.",
            ]
            result = deploy_knowledge_assistant(
                documents=documents,
                interactive_mode=True,
            )
        else:
            # Run all demos
            demo_basic_bot()
            demo_scalability()
            demo_deployment_options()
            demo_monitoring()

        print("\n" + "=" * 70)
        print("✅ Knowledge bot demonstrations complete!")
        print("=" * 70)
        print("\nKey Takeaways:")
        print("  • deploy_knowledge_assistant() is your extraction point")
        print("  • Combine all prior lessons: 4.2 → 4.3 → 4.4 → 4.5 → 4.6")
        print("  • Choose deployment pattern for your use case")
        print("  • Monitor key metrics in production")
        print("  • Plan for scalability from day one")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__" and not STREAMLIT_ONLY_MODE:
    main()


# ============================================================================
# STREAMLIT UI (only runs when: streamlit run lesson-06-corporate-knowledge-bot.py)
# ============================================================================

if HAS_STREAMLIT:
    def _generate_answer_with_llm(
        prompt: str,
        api_key: Optional[str] = None,
        model: str = "openai/gpt-3.5-turbo",
    ) -> str:
        """
        Generate an answer using OpenRouter LLM API.
        
        Adapted from Lesson 4.4 pattern.
        Falls back gracefully if API key is missing.
        """
        if not api_key:
            # Fallback: return simple extraction-based answer
            return "[To enable full LLM answers, set OPENROUTER_API_KEY environment variable]"

        try:
            import requests
        except ImportError:
            return "[requests library required for LLM calls]"

        # Call OpenRouter API
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "HTTP-Referer": "https://github.com/AIForSoftwareEngineers",
                    "X-Title": "Corporate Knowledge Bot",
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 300,
                },
                timeout=15,
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("choices", [{}])[0].get("message", {}).get("content", "No response from LLM")
            else:
                return f"[LLM Error: {response.status_code}]"
        except Exception as e:
            return f"[LLM Error: {str(e)}]"

    def generate_answer_from_context(query: str, retrieved_docs: List[Dict], company_name: str) -> tuple:
        """
        Generate a natural language answer grounded in retrieved documents.
        
        Uses OpenRouter LLM if available, falls back to document extraction.
        Returns: (answer_text, source_titles)
        """
        if not retrieved_docs:
            return "No relevant documents found. Try using different search terms or adding more documents.", []
        
        # Extract source titles (keep them short for citations)
        source_titles = []
        context_parts = []
        
        for doc_info in retrieved_docs:
            doc_text = doc_info['document']
            # Extract title (first 50 chars as doc name)
            title = doc_text[:50].replace('\n', ' ').strip()
            if len(doc_text) > 50:
                title += "..."
            source_titles.append(title)
            
            # Use first 400 chars for context
            context_parts.append(doc_text[:400])
        
        context = "\n\n".join(context_parts)
        
        # Build augmented prompt (Lesson 4.4 pattern) with system role context
        augmented_prompt = f"""You are an internal company AI assistant for employees at {company_name}.
Your role is to help {EMPLOYEE_NAME} find information and answers from company policies and documents.

Answer the user's question based ONLY on the provided context.
If the context doesn't contain enough information, say so briefly.
Provide a natural, friendly answer (1-2 sentences). Do not quote directly from documents.

CONTEXT:
{context}

USER QUESTION:
{query}

ANSWER:"""
        
        # Try OpenRouter first
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_key:
            answer = _generate_answer_with_llm(
                prompt=augmented_prompt,
                api_key=openrouter_key,
                model="openai/gpt-3.5-turbo",
            )
            if not answer.startswith("["):  # If not an error
                return answer, source_titles
        
        # Fallback: Extract key sentences from best document
        best_doc = retrieved_docs[0]['document']
        sentences = best_doc.replace('\n', ' ').split('. ')
        query_words = set(query.lower().split())
        
        scored_sentences = []
        for sent in sentences:
            if not sent.strip():
                continue
            sent_words = set(sent.lower().split())
            score = len(query_words & sent_words) / (len(query_words) + 1)
            scored_sentences.append((score, sent))
        
        scored_sentences.sort(reverse=True)
        selected = [s[1] for s in scored_sentences[:2] if s[0] > 0]
        answer = ". ".join(selected).strip()
        if not answer:
            answer = best_doc[:200].replace('\n', ' ')
        
        return answer, source_titles
    
    # Simple wrapper class for bot results with real search capability
    class StreamlitBotWrapper:
        """Wraps deploy_knowledge_assistant output for Streamlit UI with semantic search."""
        def __init__(self, results_dict: Dict, documents: List[str] = None, embedding_engine=None):
            self._results = results_dict
            self.query_history = results_dict.get("query_history", [])
            self.answers = results_dict.get("answers", [])
            self.bot_stats = results_dict.get("bot_stats", {})
            self.documents = documents or []
            self.embedding_engine = embedding_engine
            self.doc_embeddings = []
            
            # Pre-compute embeddings for documents if available
            if self.embedding_engine and self.documents:
                try:
                    self.doc_embeddings = [
                        self.embedding_engine.embed_query(doc) for doc in self.documents
                    ]
                    print(f"✓ Pre-computed {len(self.doc_embeddings)} embeddings")
                except Exception as e:
                    print(f"⚠ Warning: Could not pre-compute embeddings ({e}). Will use keyword fallback.")
                    self.doc_embeddings = []
            
        def get_stats(self) -> Dict:
            """Get bot statistics."""
            return self.bot_stats
        
        def _keyword_search(self, query: str, top_k: int = 5) -> List[tuple]:
            """Fallback keyword-based search when embeddings unavailable."""
            query_words = set(query.lower().split())
            scores = []
            
            for i, doc in enumerate(self.documents):
                doc_words = set(doc.lower().split())
                # Simple Jaccard similarity: intersection / union
                if not doc_words:
                    score = 0.0
                else:
                    intersection = len(query_words & doc_words)
                    union = len(query_words | doc_words)
                    score = intersection / union if union > 0 else 0.0
                scores.append((i, score, doc))
            
            # Sort by score and return top-k
            scores.sort(key=lambda x: x[1], reverse=True)
            return scores[:top_k]
            
        def search(self, query: str, top_k: int = 5) -> Dict:
            """Search knowledge base with semantic similarity or keyword fallback."""
            retrieved_documents = []
            
            if not self.documents:
                return {"query": query, "retrieved_documents": []}
            
            try:
                # If embeddings are available, use semantic search
                if self.embedding_engine and self.doc_embeddings:
                    try:
                        # Embed query
                        query_embedding = self.embedding_engine.embed_query(query)
                        
                        # Compute similarities
                        import numpy as np
                        similarities = []
                        for i, doc_embedding in enumerate(self.doc_embeddings):
                            dot = np.dot(query_embedding, doc_embedding)
                            norm = np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
                            similarity = dot / (norm + 1e-8)
                            similarities.append((i, similarity, self.documents[i]))
                        
                        # Sort by similarity and get top-k
                        similarities.sort(key=lambda x: x[1], reverse=True)
                        top_results = similarities[:top_k]
                    except Exception as e:
                        print(f"⚠ Semantic search failed ({e}), falling back to keyword search")
                        top_results = self._keyword_search(query, top_k)
                else:
                    # No embeddings available, use keyword search
                    top_results = self._keyword_search(query, top_k)
                
                # Format results
                for rank, (doc_idx, score, doc_text) in enumerate(top_results, 1):
                    retrieved_documents.append({
                        "document": doc_text,
                        "similarity": float(score),
                        "metadata": {"doc_idx": doc_idx, "rank": rank}
                    })
            except Exception as e:
                print(f"✗ Search error ({e})")
            
            return {"query": query, "retrieved_documents": retrieved_documents}

    # ========================================================================
    # Initialize Streamlit App
    # ========================================================================
    st.set_page_config(
        page_title="Corporate Knowledge Bot",
        page_icon="🤖",
        layout="wide",
    )

    st.title(f"🤖 {COMPANY_NAME} Knowledge Assistant")
    st.markdown(f"*{COMPANY_TAGLINE}*")

    # ========================================================================
    # Initialize Session State
    # ========================================================================
    if "bot" not in st.session_state:
        # Load sample documents from corporate knowledge base
        sample_documents = load_sample_corpus()
        
        # Initialize the bot using deploy_knowledge_assistant
        bot_results = deploy_knowledge_assistant(
            documents=sample_documents,
            embedding_provider="cohere",
            chunk_size=512,
            top_k=5,
            interactive_mode=False,
        )
        
        # Initialize embedding engine for search functionality
        # Cohere is optional (requires API key) - keyword search works without setup
        embedding_engine = None
        embedding_method = "keyword"
        
        try:
            cohere_key = os.getenv("COHERE_API_KEY")
            if cohere_key:
                try:
                    embedding_engine = EmbeddingEngine(
                        method="cohere",
                        cohere_api_key=cohere_key,
                    )
                    embedding_method = "cohere"
                    print("✓ Cohere embedding engine initialized (semantic search enabled)")
                except Exception as e:
                    print(f"⚠ Cohere initialization failed ({e}), using keyword search")
            else:
                print("ℹ COHERE_API_KEY not set - using keyword search (set env var for semantic search)")
        except Exception as e:
            print(f"⚠ Error checking embeddings ({e})")
        
        # Wrap results in bot wrapper for Streamlit interface with real search capability
        st.session_state.bot = StreamlitBotWrapper(
            bot_results,
            documents=sample_documents,
            embedding_engine=embedding_engine,
        )
        st.session_state.chat_history = []
        st.session_state.all_documents = sample_documents
        st.session_state.search_method = embedding_method

    # ========================================================================
    # Main Chat Interface (Top Section)
    # ========================================================================
    
    # Header with search method, doc count, and Manage Docs anchor link
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**Search Method:** {st.session_state.get('search_method', 'keyword').capitalize()} | **Docs:** {len(st.session_state.all_documents)}")
    with col2:
        st.markdown("[📁 Manage Docs](#manage-docs-section)")
    
    st.divider()

    # Chat Display
    st.subheader("💬 Chat")
    
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat Input
    st.divider()
    query = st.chat_input("Ask a question about the documents...", key="chat_input")
    
    if query:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": query})
        
        # Search knowledge base
        result = st.session_state.bot.search(query, top_k=3)
        
        # Generate LLM-based answer from retrieved documents
        if result["retrieved_documents"]:
            answer_text, source_titles = generate_answer_from_context(
                query,
                result["retrieved_documents"],
                COMPANY_NAME
            )
            
            # Format response with sources as addendum in small text
            if source_titles:
                sources_str = ", ".join(source_titles)
                response = f"{answer_text}\n\n_(Source: {sources_str})_"
            else:
                response = answer_text
        else:
            response = "No relevant documents found. Try:\n- Adding more documents with the 📁 button\n- Using different search terms\n- Checking your document formatting"
        
        # Add assistant message to history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

    # ========================================================================
    # Learning Resources (Middle Section)
    # ========================================================================
    st.divider()
    
    with st.expander("📚 How This Works"):
        st.markdown("""
### Lesson 4.6: Corporate Knowledge Bot

**Architecture:**
1. **Document Ingestion** - Load sample-corpus.json + user uploads
2. **Embedding** - Generate semantic vectors (Cohere or keyword fallback)
3. **Vector Store** - In-memory index for fast retrieval
4. **Search** - Find most relevant documents by similarity
5. **Generation** - LLM creates natural answers based on context

**Answer Generation:**
- **With OPENROUTER_API_KEY**: Uses GPT-3.5 to synthesize natural answers
- **Without API key**: Falls back to intelligent document extraction

**Search Methods:**
- **Keyword Search** (default): Fast, works offline, word matching
- **Semantic Search** (with COHERE_API_KEY): Meaning-based, better quality

**Key Learnings from Lessons 4.2-4.6:**
- 4.2: Chunk and embed documents → `embed_documents()`
- 4.3: Store vectors and retrieve → `VectorStore`
- 4.4: Build RAG pipeline → `build_rag_pipeline()`
- 4.5: Optimize retrieval → reranking, filtering, metrics
- 4.6: Deploy at scale → document management, user interface

**To Enable Full LLM Answers:**
```bash
export OPENROUTER_API_KEY='your-key-here'
# Get key: https://openrouter.ai (free credits available)
```

**Production Deployment:**
- Replace Streamlit with FastAPI for scalability
- Use Pinecone/Weaviate for >100k documents
- Add chat history persistence (database)
- Implement usage monitoring and cost tracking
""")

    st.divider()

    # ========================================================================
    # Document Management Section (Bottom - Closed by Default)
    # ========================================================================
    
    # Anchor for scroll link
    st.markdown("<a id='manage-docs-section'></a>", unsafe_allow_html=True)
    
    # Header with Manage Docs toggle button
    if st.button("📁 Manage Docs", key="manage_docs_btn"):
        st.session_state.show_doc_manager = not st.session_state.get("show_doc_manager", False)
    
    if st.session_state.get("show_doc_manager", False):
        with st.container(border=True):
            col_title, col_close = st.columns([1, 0.3])
            with col_title:
                st.subheader("📁 Document Management")
            with col_close:
                if st.button("✕ Close", key="close_doc_manager"):
                    st.session_state.show_doc_manager = False
                    st.rerun()
            
            tab1, tab2 = st.tabs(["Upload", "Paste Text"])
            
            with tab1:
                uploaded_file = st.file_uploader("Upload a text file or document", type=["txt", "md", "pdf"])
                if uploaded_file is not None:
                    try:
                        content = uploaded_file.read().decode("utf-8")
                        if content and content not in st.session_state.all_documents:
                            st.session_state.all_documents.append(content)
                            # Re-initialize bot with new documents
                            bot_results = deploy_knowledge_assistant(
                                documents=st.session_state.all_documents,
                                embedding_provider="cohere",
                            )
                            st.session_state.bot = StreamlitBotWrapper(
                                bot_results,
                                documents=st.session_state.all_documents,
                                embedding_engine=st.session_state.bot.embedding_engine,
                            )
                            st.success(f"✓ Added '{uploaded_file.name}' ({len(content)} chars)")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error processing file: {e}")
            
            with tab2:
                pasted_text = st.text_area("Paste document text here", height=150, key="paste_area")
                if st.button("Add Document", key="add_doc_btn"):
                    if pasted_text.strip() and pasted_text not in st.session_state.all_documents:
                        st.session_state.all_documents.append(pasted_text)
                        # Re-initialize bot with new documents
                        bot_results = deploy_knowledge_assistant(
                            documents=st.session_state.all_documents,
                            embedding_provider="cohere",
                        )
                        st.session_state.bot = StreamlitBotWrapper(
                            bot_results,
                            documents=st.session_state.all_documents,
                            embedding_engine=st.session_state.bot.embedding_engine,
                        )
                        st.success(f"✓ Added document ({len(pasted_text)} chars)")
                        st.rerun()
                    elif not pasted_text.strip():
                        st.warning("Please paste some text")
            
            st.info(f"Total documents in knowledge base: **{len(st.session_state.all_documents)}**")
            
            # Display list of documents with snippets and stats
            st.markdown("**📄 Available Documents:**")
            for i, doc in enumerate(st.session_state.all_documents, 1):
                # Calculate stats
                word_count = len(doc.split())
                char_count = len(doc)
                
                # Extract title: first few words
                words = doc.replace('\n', ' ').split()
                title_words = []
                for word in words[:10]:
                    title_words.append(word)
                    if word.endswith('.') or word.endswith(':'):
                        break
                doc_title = ' '.join(title_words[:8]).strip()
                if not doc_title:
                    doc_title = ' '.join(words[:5])
                
                st.markdown(f"**Doc {i}** ({word_count} words, {char_count} chars)  \n_{doc_title}_")

