# Module 4: Practical RAG & Context Engineering

This module teaches engineers how to build Retrieval-Augmented Generation (RAG) systems that allow AI models to reason over proprietary knowledge. Progress from understanding RAG architecture through implementing embeddings, vector search, retrieval pipelines, optimization strategies, and ultimately a deployable knowledge assistant.

By the end of this module, students will be capable of designing, building, debugging, and optimizing production-grade RAG systems that deliver accurate, grounded responses using custom business data.

## Module Overview

**Learning Path:**
1. **Lesson 4.1** (Talking Head): RAG Blueprint and system architecture
2. **Lesson 4.2** (Code): Document ingestion and embedding generation
3. **Lesson 4.3** (Code): Vector storage and similarity search
4. **Lesson 4.4** (Code): Building complete RAG pipelines
5. **Lesson 4.5** (Code): RAG optimization and quality improvement
6. **Lesson 4.6** (Code): Capstone — Corporate Knowledge Bot

## Lessons

### Lesson 4.1: The RAG Blueprint
**Type:** Talking Head (No Code)

Introduces RAG architecture and system design patterns.

---

### Lesson 4.2: Embedding Your Data
**Type:** Code Screencast  
**Status:** ✅ Complete  
**Provider:** OpenRouter (via Jina Embeddings v3, with Cohere and TF-IDF fallback)

Learn the production-ready document ingestion pattern for RAG systems.

#### Core Template Method
The lesson demonstrates **`embed_documents()`**, the foundational ingestion template that learners can extract and adapt for their own projects.

**Method Signature:**
```python
def embed_documents(
    documents: List[str],
    chunk_size: int = 512,
    chunk_overlap: int = 50,
    provider: str = "openrouter",
    openrouter_key: str | None = None,
) -> List[Dict]
```

**Returns:** List of structured dicts with:
- `chunk_id`: Unique identifier for each chunk
- `text`: Chunk content
- `embedding`: np.ndarray (semantic vector)
- `metadata`: doc_idx, chunk_idx, char_count, provider
- `char_count`: Length of chunk

#### Run Instructions
```bash
source .venv/bin/activate
export OPENROUTER_API_KEY='your-openrouter-key-here'
pip install -r requirements-module-04.txt
python lesson-02-embedding-your-data.py
```

**Fallback Provider Chain:**
1. **OpenRouter** (primary) — via Jina Embeddings v3
2. **Cohere** (fallback) — if OpenRouter unavailable
3. **TF-IDF** (fallback) — keyword-based, always available

#### What You'll Learn
- **Smart Chunking:** Split documents by sentences to preserve context
- **Overlap Strategy:** Maintain context across chunk boundaries
- **Embedding Generation:** Generate semantic vectors via OpenRouter
- **Metadata Association:** Track chunk provenance and source
- **Semantic Search:** Query embedded documents for similarity

#### Demonstrations
1. **Core Method**: Show embed_documents() producing structured output
2. **Semantic Search**: Query a document collection and rank by relevance
3. **Chunking Strategies**: Visualize how different chunk sizes affect splits
4. **Provider Fallback**: Show automatic downgrade from OpenRouter → Cohere → TF-IDF

#### Template Reusability
This method is designed for extraction into your own projects. To adapt it:
1. Change document source (files, URLs, databases, APIs)
2. Adjust metadata schema for your domain
3. Swap embedding provider in `EmbeddingEngine` initialization
4. Customize chunk_size and overlap for your use case

#### Key Concepts
- Text chunking and overlap management
- Semantic embeddings via production providers
- Metadata association with documents
- Batch embedding for efficiency
- Fallback patterns for production robustness

---

### Lesson 4.3: The Vector Store Lab
**Type:** Code Screencast  
**Status:** ✅ Complete  
**Backend:** NumPy (default) + FAISS (optional optimization)

Learn efficient storage and retrieval of embeddings for RAG systems.

#### Core Template Method
The lesson demonstrates **`semantic_search()`**, the core retrieval template that learners can extract and adapt for production systems.

**Method Signature:**
```python
def semantic_search(
    embedded_chunks: List[Dict],
    query_embedding: np.ndarray,
    top_k: int = 5,
    use_faiss: bool = False,
    metadata_filter: Dict | None = None,
) -> List[Dict]
```

**Input:** Embedded chunks from Lesson 4.2 (text, vectors, metadata)  
**Output:** Ranked results list with `{rank, chunk_id, text, similarity, metadata}`

#### Run Instructions
```bash
source .venv/bin/activate
pip install -r requirements-module-04.txt
python lesson-03-vector-store-lab.py
```

**Optional Performance Enhancement:**
```bash
pip install faiss-cpu  # ~100MB addition for large-scale search
```

#### What You'll Learn
- **Vector Storage:** Store embeddings efficiently in memory or FAISS
- **Semantic Search:** Find documents via similarity scoring (not keywords)
- **Ranking & Scoring:** Calculate and rank results by relevance
- **Metadata Filtering:** Filter search results by document properties
- **Backend Selection:** Choose between NumPy (simple) and FAISS (scale)
- **Performance Comparison:** Measure speed tradeoffs

#### Demonstrations
1. **Core Method**: Execute `semantic_search()` on embedded chunks
2. **Backend Comparison**: Measure NumPy vs FAISS performance
3. **Metadata Filtering**: Restrict search by category, type, source, etc.
4. **Production Options**: Overview of vector stores (Pinecone, ChromaDB, Qdrant, Milvus, Weaviate)

#### Vector Store Backends Explained

**NumPy (Default)**
- ✓ No installation required, works everywhere
- ✓ Fast for <10k documents
- ✓ Simple, easy to debug
- ✗ Not suitable for millions of documents
- ✗ All data in RAM (memory bound)
- Use: Prototypes, small datasets, testing

**FAISS (Facebook AI Similarity Search)**
- ✓ Millions of documents, fast retrieval
- ✓ Multiple indexing strategies
- ✓ GPU acceleration available
- ✗ Requires compilation, platform dependencies
- ✗ Complex API for advanced features
- Use: Production search, large scale, performance critical

**ChromaDB (Lightweight)**
- ✓ Persistent local storage
- ✓ Simple Python API
- ✓ Good for demos and small production systems
- ✗ Single machine scale
- ✗ Limited query options
- Use: Small apps, persistent development

**Pinecone (Managed Cloud)**
- ✓ Fully serverless, auto-scaling
- ✓ Built-in metadata filtering
- ✓ No ops overhead
- ✗ Usage-based pricing
- ✗ External API dependency
- Use: Enterprise apps, variable load

**Qdrant / Weaviate / Milvus (Self-Hosted)**
- ✓ Open source, customizable
- ✓ Self-hosted or cloud options
- ✓ Scalable architectures
- ✗ Operational complexity
- ✗ More setup required
- Use: Large-scale production, custom needs

#### Template Reusability
Extract `semantic_search()` into your projects:
1. Replace `VectorStore` with ChromaDB, Pinecone, or FAISS-backed version
2. Customize metadata_filter for your domain schema
3. Add query expansion or reranking for quality improvements
4. Scale backend as document count grows

#### Key Concepts
- Vector similarity (cosine, L2 distance)
- Ranking and top-k retrieval
- Metadata-aware search
- NumPy vs optimized backends
- Search quality vs performance tradeoffs

---

### Lesson 4.4: Building the Pipeline
**Type:** Code Screencast  
**Status:** ✅ Complete  
**Provider:** OpenRouter (Llama 2) for LLM answer generation

Assemble the complete end-to-end RAG workflow that combines Lessons 4.2, 4.3, and LLM generation into a production-ready pipeline.

#### Business Scenario
A company HR team needs an AI assistant that answers employee questions (remote work, benefits, PTO, professional development) using internal policy documents. The system must retrieve relevant policy docs and generate accurate, sourced answers in seconds.

#### Core Template Method
The lesson demonstrates **`build_rag_pipeline()`**, the orchestration template that learners can extract and adapt for production RAG systems.

**Method Signature:**
```python
def build_rag_pipeline(
    documents: List[str],
    query: str,
    top_k: int = 5,
    chunk_size: int = 512,
    chunk_overlap: int = 50,
    embedding_provider: str = "openrouter",
    openrouter_key: Optional[str] = None,
    llm_model: str = "meta-llama/llama-2-7b-chat",
) -> Dict
```

**Input:**
- `documents`: List of policy/knowledge documents
- `query`: User's natural language question

**Output:** Dict with:
- `answer`: Generated answer grounded in retrieved context
- `sources`: Retrieved documents with rank, text, and similarity scores
- `context`: Full context sent to LLM (for transparency/debugging)
- `retrieval_time`: Seconds spent on embedding & search
- `generation_time`: Seconds spent on LLM call
- `total_time`: Sum of retrieval + generation time
- `total_tokens`: Approximate tokens used (input + output)
- `retrieval_count`: Number of documents retrieved

#### Run Instructions
```bash
source .venv/bin/activate
export OPENROUTER_API_KEY='your-openrouter-key-here'
pip install -r requirements-module-04.txt
python lesson-04-building-rag-pipeline.py
```

**Environment Setup:**
1. Get free OpenRouter API key: https://openrouter.ai (signup with email)
2. Set `export OPENROUTER_API_KEY='your-key-here'`
3. Default LLM: `meta-llama/llama-2-7b-chat` (free, reliable)

#### Pipeline Architecture

**5-Stage RAG Pipeline:**

```
┌─────────────────┐
│  DOCUMENTS      │
│  (Your Data)    │
└────────┬────────┘
         │
    ┌────▼─────────────────────────────┐
    │ STAGE 1: INGESTION               │
    │ • Chunk by sentence boundaries   │
    │ • Generate embeddings (OpenRouter)│
    │ → Output: Indexed chunks         │
    └────┬─────────────────────────────┘
         │
    ┌────▼─────────────────────────────┐
    │ STAGE 2: RETRIEVAL               │
    │ • Embed user query               │
    │ • Search for top-K similar docs  │
    │ • Rank by cosine similarity      │
    │ → Output: Ranked docs + scores   │
    └────┬─────────────────────────────┘
         │
    ┌────▼─────────────────────────────┐
    │ STAGE 3: AUGMENTATION            │
    │ • Format docs as context         │
    │ • Build augmented prompt         │
    │ • Add grounding instructions     │
    │ → Output: LLM-ready prompt       │
    └────┬─────────────────────────────┘
         │
    ┌────▼─────────────────────────────┐
    │ STAGE 4: GENERATION              │
    │ • Call OpenRouter LLM            │
    │ • Generate grounded answer       │
    │ • Extract response               │
    │ → Output: Textual answer         │
    └────┬─────────────────────────────┘
         │
    ┌────▼─────────────────────────────┐
    │ STAGE 5: FORMATTING              │
    │ • Calculate timing metrics       │
    │ • Format citations               │
    │ • Estimate token usage           │
    │ → Output: Complete result dict   │
    └─────────────────────────────────┘
```

#### What You'll Learn

**Core Concepts:**
- Complete RAG workflow orchestration
- Document chunking strategy impact
- Semantic search integration
- Prompt augmentation for grounding
- LLM integration (OpenRouter API)
- Error handling and fallbacks
- Performance measurement

**Production Patterns:**
- Provider chaining (OpenRouter → Cohere → TF-IDF for embeddings)
- Graceful degradation without API keys
- Timing measurement for optimization
- Context transparency for debugging
- Token counting for cost estimation

**Data Flow:**
- Lesson 4.2 output (embedded chunks) feeds into Stage 1 ingestion
- Lesson 4.3 output (semantic_search logic) feeds into Stage 2 retrieval
- Combined context + query → LLM for generation

#### Demonstrations

**Demo 1: Core RAG Pipeline**
- HR knowledge base with 5 policy documents
- Query: "Can I work remotely and what equipment do I get?"
- Shows: Retrieved sources, generated answer, performance metrics

**Demo 2: Retrieval Quality Impact**
- Programming language knowledge base
- Three queries of varying specificity/difficulty
- Shows: How retrieval quality affects answer quality

**Demo 3: Chunking Strategy Comparison**
- Long ML document (200+ words)
- Test chunk sizes: 200, 512, 1024 characters
- Shows: Tradeoff between coverage and search speed

**Demo 4: Pipeline Stages Explained**
- Detailed walkthrough of each RAG stage
- Inputs and outputs at each step
- Benefits of modular design for optimization

#### Template Reusability

Extract `build_rag_pipeline()` for your projects:

1. **Change Data Source:**
   ```python
   documents = load_from_pdf("handbook.pdf")  # Replace load logic
   result = build_rag_pipeline(documents, query)
   ```

2. **Customize Retrieval:**
   ```python
   result = build_rag_pipeline(documents, query, top_k=10, chunk_size=1024)
   ```

3. **Switch LLM Model:**
   ```python
   result = build_rag_pipeline(
       documents, query,
       llm_model="meta-llama/llama-2-13b-chat"  # Larger model
   )
   ```

4. **Use Different Embedding Provider:**
   ```python
   result = build_rag_pipeline(
       documents, query,
       embedding_provider="cohere",  # Swap provider
       openrouter_key=None  # Use Cohere key instead
   )
   ```

#### Helper Methods

**`_smart_chunk(text, chunk_size, overlap)`**
- Split text by sentence boundaries (preserves context)
- Maintain overlap between chunks
- Filter out tiny chunks

**`_generate_answer_with_llm(prompt, api_key, model)`**
- Call OpenRouter chat completions API
- Handle missing API keys gracefully
- Parse and return LLM response

#### Key Concepts

- **Ingestion:** Document processing and embedding
- **Retrieval:** Semantic similarity search
- **Augmentation:** Prompt engineering with context
- **Generation:** LLM-based answer synthesis
- **Evaluation:** Quality metrics and performance timing
- **Modular Design:** Each stage can be optimized independently
- **Error Handling:** Graceful degradation when APIs unavailable
- **Transparency:** Full context and metrics in output

#### Integration with Previous Lessons

| Lesson | Component | Used in Stage |
|--------|-----------|---------------|
| 4.2 | `embed_documents()` | Ingestion (Stage 1) |
| 4.2 | `_smart_chunk()` | Ingestion (Stage 1) |
| 4.3 | `semantic_search()` | Retrieval (Stage 2) |
| 4.3 | Cosine similarity | Retrieval (Stage 2) |
| Module 3 | OpenRouter API | Generation (Stage 4) |

---

### Lesson 4.5: RAG Optimization
**Type:** Code Screencast  
**Status:** ✅ Complete  
**Provider:** OpenRouter (Jina v3) for embeddings

Improve retrieval quality through post-processing and reranking without fetching additional documents.

#### Business Scenario
A search system retrieves relevant documents but ranks them suboptimally. Users find irrelevant results in top positions. Your task is to apply optimization techniques to improve ranking quality without re-running expensive retrieval operations (cost-effective improvement).

#### Core Template Method
The lesson demonstrates **`improve_retrieval()`**, the ranking optimization template that learners can extract and adapt for production search systems.

**Method Signature:**
```python
def improve_retrieval(
    raw_results: List[Dict],
    query: str,
    query_embedding: np.ndarray,
    improvement_method: str = "rerank",
    documents: Optional[List[str]] = None,
    metadata_filters: Optional[Dict] = None,
    length_normalize: bool = True,
) -> List[Dict]
```

**Input:**
- `raw_results`: Retrieved chunks from `semantic_search()` (Lesson 4.3)
- `query`: Original query string (for context-aware reranking)
- `improvement_method`: Technique to apply ("rerank", "query_expansion", "metadata_filtering")

**Output:** Improved ranked results with:
- `rank`: 1-indexed position after reranking
- `original_similarity`: Raw semantic similarity
- `improved_score`: Post-processing adjusted score
- `factors`: Dict showing calculation details

#### Run Instructions
```bash
source .venv/bin/activate
export OPENROUTER_API_KEY='your-openrouter-key-here'  # Optional
python lesson-05-rag-optimization.py
```

#### Optimization Techniques Demonstrated

**1. Reranking (Length Normalization)**
- Problem: Long documents always rank highest due to size bias
- Solution: Penalize document length in score calculation
- Formula: `improved_score = similarity * (1 / (1 + log(doc_length)))`
- Benefit: Fair ranking regardless of document size

**2. Query Expansion (Semantic + Keyword Hybrid)**
- Problem: Pure semantic search misses keyword-specific docs
- Solution: Combine semantic similarity with keyword overlap
- Formula: `improved_score = (semantic_sim + keyword_overlap) / 2`
- Benefit: Better coverage for specific terminology

**3. Metadata Filtering & Scoring**
- Problem: Relevant documents filtered out by strict metadata
- Solution: Apply soft filters using metadata boosting scores
- Benefit: More flexible result targeting

#### What You'll Learn

**Optimization Concepts:**
- Post-processing retrieval without API calls
- Combining multiple ranking signals
- Metadata-aware filtering and scoring
- Length normalization to combat bias
- Cost-effective quality improvement

**Evaluation Metrics:**
- Precision@K: Fraction of top-K results that are relevant
- Recall@K: Coverage of all relevant documents
- MRR (Mean Reciprocal Rank): Position of first relevant result
- NDCG (Normalized Discounted Cumulative Gain): Ranking quality
- These enable quantifying improvement before/after optimization

#### Demonstrations

**Demo 1: Reranking Impact**
- Show raw retrieval results (before reranking)
- Apply length normalization
- Show improved ranking (after reranking)
- Display factors contributing to each score

**Demo 2: Query Expansion**
- Compare semantic-only vs semantic+keyword ranking
- Show how keyword overlap compensates for semantic gaps
- Demonstrate better ranking of domain-specific results

**Demo 3: Metadata Filtering**
- Show filtering by document type, date, region, etc.
- Display how metadata filters reduce result set
- Explain hard filters vs soft scoring boosts

**Demo 4: Evaluation Metrics**
- Show precision, recall, MRR, NDCG calculations
- Explain metric interpretation for business context
- Demonstrate how metrics guide optimization decisions

#### Template Reusability

Extract `improve_retrieval()` for your projects:

1. **Change Improvement Method:**
   ```python
   result = improve_retrieval(raw_results, query, query_embedding, 
                             improvement_method="query_expansion")
   ```

2. **Apply Metadata Filtering:**
   ```python
   result = improve_retrieval(raw_results, query, query_embedding,
                             metadata_filters={"department": "Engineering"})
   ```

3. **Evaluate Quality:**
   ```python
   metrics = _evaluate_ranking(improved_results, ground_truth_relevant)
   print(f"Precision: {metrics['precision']:.2f}")
   ```

#### Helper Methods

**`_calculate_keyword_overlap(query, results)`**
- Jaccard similarity between query words and document words
- Returns Dict[chunk_id → overlap_score 0-1]

**`_evaluate_ranking(improved_results, ground_truth_relevant)`**
- Calculates precision, recall, MRR, NDCG
- Returns metrics Dict for ranking quality assessment

#### Key Concepts

- **Bias Detection:** Long documents ranked higher due to similarity calculation
- **Multi-Signal Ranking:** Combine semantic, keyword, metadata signals
- **Cost-Effective:** Improve quality without additional API calls
- **Metrics-Driven:** Quantify improvements with evaluation metrics
- **Modular Design:** Apply optimization independently after retrieval

#### Integration with Previous Lessons

| Source | Method | Used in |
|--------|--------|---------|
| 4.3 | `semantic_search()` output | Input to improve_retrieval() |
| 4.4 | Raw retrieval results | Reranking target |
| 4.5 | Length normalization | Ranking adjustment |
| 4.5 | Keyword overlap | Hybrid signal |

---

### Lesson 4.6: Corporate Knowledge Bot (Capstone)
**Type:** Code Screencast  
**Status:** ✅ Complete  
**Deployment:** CLI (batch and interactive modes)

Build and deploy a complete RAG knowledge assistant that orchestrates all prior lessons into a production-ready system.

#### Business Scenario
A company needs an employee knowledge assistant that answers questions about policies, tech stack, offices, benefits, and culture. The system must:
- Ingest company documents
- Retrieve relevant policies in real-time
- Generate accurate answers with citations
- Track query analytics
- Scale to thousands of employees

#### Core Template Method
The lesson demonstrates **`deploy_knowledge_assistant()`**, the orchestration template that learners can extract to build deployable RAG systems in any domain.

**Method Signature:**
```python
def deploy_knowledge_assistant(
    documents: List[str],
    queries: Optional[List[str]] = None,
    embedding_provider: str = "openrouter",
    chunk_size: int = 512,
    top_k: int = 5,
    interactive_mode: bool = False,
) -> Dict
```

**Input:**
- `documents`: Knowledge base (policy docs, FAQs, etc.)
- `queries`: Batch queries to process (or None for interactive)
- `embedding_provider`: Primary embedding service
- `interactive_mode`: Accept queries from stdin vs batch

**Output:** Complete bot deployment Dict with:
- `answers`: List of {query, answer, sources, retrieval_time}
- `bot_stats`: {total_documents, total_queries, avg_retrieval_time}
- `query_history`: Timestamped query log for analytics
- `deployment_metadata`: Config and version info
- `errors`: Any issues encountered

#### Run Instructions
```bash
source .venv/bin/activate
export OPENROUTER_API_KEY='your-openrouter-key-here'
python lesson-06-corporate-knowledge-bot.py              # Run demos
python lesson-06-corporate-knowledge-bot.py --demo 1     # Specific demo
python lesson-06-corporate-knowledge-bot.py --interactive # Interactive mode
```

#### What You'll Learn

**Deployment Patterns:**
- Batch processing (pre-computed answers)
- Interactive mode (real-time user queries)
- Monitoring and analytics
- Error handling and fallbacks
- Scalability considerations

**Architecture:**
- Document ingestion and embedding
- Vector store initialization
- Query embedding and retrieval
- Answer generation or stubbing
- Performance metrics tracking

**Production Patterns:**
- Query history for audit trail
- Timing measurements for optimization
- Statistics aggregation
- Graceful degradation (fallbacks)
- Deployment metadata logging

#### Demonstrations

**Demo 1: Basic Bot Deployment**
- Load sample company documents (HR policies, tech stack, etc.)
- Process batch of employee questions
- Show answers with sources and timing
- Display bot statistics

**Demo 2: Scalability Considerations**
- Explain document size scaling (small, medium, large)
- Latency vs accuracy tradeoffs
- Update frequency strategies (static, daily, real-time)
- Cost optimization patterns
- Caching and performance tuning

**Demo 3: Deployment Options**
- **CLI Tool:** Batch processing, internal use
- **REST API:** Web integration, mobile apps
- **Streamlit UI:** Quick demos, internal tools
- **Slack Bot:** Employee self-service
- **Web Chat Widget:** Customer support
- **Desktop App:** Offline access
- When to use each and tradeoffs

**Demo 4: Monitoring & Observability**
- Retrieval quality metrics (precision, recall, NDCG)
- Performance metrics (query latency, cache hit rate)
- User satisfaction tracking (query volume, ratings)
- Cost monitoring (API calls, compute)
- Reliability metrics (uptime, error rate)
- When to alert and optimize

#### Template Reusability

Extract `deploy_knowledge_assistant()` to build bots for any domain:

1. **Customer Support Bot:**
   ```python
   support_docs = load_faq("support/faqs.txt")
   result = deploy_knowledge_assistant(support_docs)
   ```

2. **Internal Wiki:**
   ```python
   wiki_pages = load_docs("internal_wiki/")
   result = deploy_knowledge_assistant(wiki_pages, 
                                       embedding_provider="cohere")
   ```

3. **Product Documentation:**
   ```python
   docs = load_pdfs("product_docs/")
   result = deploy_knowledge_assistant(docs, 
                                       chunk_size=1024,
                                       top_k=10)
   ```

#### Capstone Integration

This lesson brings together all Module 4 components:

| Lesson | Component | Used in 4.6 |
|--------|-----------|------------|
| 4.2 | `embed_documents()` | Document ingestion |
| 4.2 | Smart chunking | Context preservation |
| 4.3 | `semantic_search()` | Query retrieval |
| 4.3 | Cosine similarity | Ranking |
| 4.4 | `build_rag_pipeline()` | Full orchestration |
| 4.5 | `improve_retrieval()` | Optional optimization |
| 4.5 | Evaluation metrics | Quality monitoring |

#### Deployment Architecture

```
┌─────────────────┐
│  Knowledge Docs │
├─────────────────┤
│  Chunking       │ ← Lesson 4.2
├─────────────────┤
│  Embeddings     │ ← Lesson 4.2
├─────────────────┤
│  Vector Store   │ ← Lesson 4.3
├─────────────────┤
│  Retrieval      │ ← Lessons 4.3-4.5
├─────────────────┤
│  Answer Gen     │ ← Lesson 4.4
├─────────────────┤
│  Analytics      │ ← Lesson 4.6
└─────────────────┘

User Query → Embed → Search → Retrieve → Generate → Return + Log
```

#### Key Concepts

- **Orchestration:** Combine all components into single bot method
- **Interactive vs Batch:** Support both modes transparently
- **Analytics:** Track query history and performance
- **Deployment:** Multiple deployment patterns available
- **Monitoring:** Built-in metrics for observability
- **Scalability:** Design decisions for different scales

#### Post-Lesson Checklist

After completing Lesson 4.6, you can:
- ✓ Build RAG systems from scratch to deployment
- ✓ Optimize retrieval quality independently
- ✓ Handle real-time and batch queries
- ✓ Monitor and observe production systems
- ✓ Scale to thousands of documents and queries
- ✓ Choose appropriate deployment patterns
- ✓ Build domain-specific knowledge assistants

---

## Shared Resources

All lessons leverage utilities in `shared/`:

- **`embeddings.py`** — Embedding generation (Cohere + TF-IDF)
- **`vector_store.py`** — In-memory vector storage with FAISS support
- **`retriever.py`** — Multi-stage retrieval (semantic, keyword, hybrid)
- **`prompts.py`** — RAG-specific prompt templates
- **`rag_pipeline.py`** — Complete RAG orchestration and evaluation

## Setup & Dependencies

### First-Time Setup
```bash
# Create clean virtual environment
rm -rf .venv
./setup.sh
source .venv/bin/activate

# Install Module 4 dependencies
pip install -r requirements-module-04.txt
```

**Dependencies:**
- numpy, scikit-learn (embeddings & retrieval)
- streamlit (UI for Lesson 4.6)
- cohere (optional, for semantic embeddings)
- faiss-cpu (optional, for large-scale search)

### API Keys
```bash
# Optional: Cohere for semantic embeddings (free tier: 100k requests/month)
export COHERE_API_KEY='your-key-here'

# Cohere signup: https://cohere.com (no credit card needed)
```

---

## Data & Evaluation

### Sample Knowledge Base
- `datasets/` contains sample company documents
- `evaluations/` contains test queries and expected answers

### Evaluation Datasets
```json
{
  "queries": [
    "What is our remote work policy?",
    "Where are our offices located?"
  ],
  "ground_truth": {
    "query_0": ["doc_3", "doc_7"],
    "query_1": ["doc_2"]
  }
}
```

---

## Module Progression

```
RAG Architecture
        ↓
Document Ingestion
        ↓
Embeddings & Vector Storage
        ↓
Similarity Search & Retrieval
        ↓
Prompt Augmentation
        ↓
LLM Generation
        ↓
Optimization & Evaluation
        ↓
Corporate Knowledge Bot
```

---

## Recommended Project Timeline

| Lesson | Time | Focus |
|--------|------|-------|
| 4.2 | 45 min | Document ingestion, chunking, embeddings |
| 4.3 | 45 min | Vector storage, similarity search |
| 4.4 | 45 min | Complete RAG pipeline |
| 4.5 | 60 min | Optimization, reranking, evaluation |
| 4.6 | 90 min | Capstone: Full knowledge bot |

**Total:** ~5-6 hours of hands-on development

---

## Next Steps

After completing Module 4:
- ✅ You can build RAG systems for domain-specific knowledge
- ✅ You understand embedding and retrieval optimization
- ✅ You can evaluate and improve RAG quality
- ✅ You're ready for Module 5: **Developing MCP Servers & Tooling**

In Module 5, you'll learn how to expose RAG systems (and other capabilities) as Model Context Protocol (MCP) servers for AI assistants and agents.

---

## Reference

- Full curriculum: `docs/curriculum_v1.md`
- Agent instructions: `agents.md`
- Module 3 (APIs & Deployment): `../module-03-ai-developer-toolkit/`
