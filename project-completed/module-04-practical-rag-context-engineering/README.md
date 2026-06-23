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

Learn how to prepare raw documents, chunk content appropriately, generate embeddings, and create a retrieval-ready knowledge base.

#### Run Instructions
```bash
source .venv/bin/activate
export COHERE_API_KEY='your-key-here'  # Optional for Cohere embeddings
pip install -r requirements-module-04.txt
python lesson-02-embedding-your-data.py
```

**What You'll Learn:**
- Document preparation and chunking strategies
- Embedding generation (Cohere + TF-IDF fallback)
- Creating retrieval-ready document collections
- Data source patterns (text, PDF, CSV, JSON)

**Key Concepts:**
- Text chunking and overlap management
- Semantic embeddings vs keyword indexing
- Metadata association with documents
- Batch processing for efficiency

---

### Lesson 4.3: The Vector Store Lab
**Type:** Code Screencast  
**Status:** ✅ Complete

Learn to store embeddings, build indexes, and execute similarity searches.

#### Run Instructions
```bash
source .venv/bin/activate
export COHERE_API_KEY='your-key-here'  # Optional
python lesson-03-vector-store-lab.py
```

**What You'll Learn:**
- Vector storage architectures
- Similarity search and ranking
- Metadata filtering and metadata-aware retrieval
- Vector store persistence (save/load)
- Comparison of implementations (FAISS, Pinecone, ChromaDB, Milvus)

**Vector Store Options:**
- **In-Memory** (NumPy): Fast for <1M docs, used in this course
- **FAISS**: Optimized for large-scale search, GPU acceleration
- **Pinecone**: Fully managed cloud service
- **ChromaDB**: Lightweight persistent storage
- **Milvus**: Scalable open-source option

---

### Lesson 4.4: Building the Pipeline
**Type:** Code Screencast  
**Status:** ✅ Complete

Assemble the complete RAG workflow combining all components.

#### Run Instructions
```bash
source .venv/bin/activate
export COHERE_API_KEY='your-key-here'  # Optional
python lesson-04-building-rag-pipeline.py
```

**What You'll Learn:**
- RAG pipeline architecture (ingest → retrieve → augment → generate)
- Prompt construction with retrieved context
- Document retrieval and ranking
- LLM integration for answer generation
- RAG patterns and variations

**Pipeline Stages:**
1. **Ingestion** → Embed documents and store
2. **Retrieval** → Find relevant documents
3. **Augmentation** → Format as LLM context
4. **Generation** → Use LLM to answer
5. **Evaluation** → Measure quality

---

### Lesson 4.5: RAG Optimization
**Type:** Code Screencast  
**Status:** ✅ Complete

Improve retrieval quality through advanced techniques.

#### Run Instructions
```bash
source .venv/bin/activate
python lesson-05-rag-optimization.py
```

**What You'll Learn:**
- Diagnosing retrieval problems
- Hybrid search (semantic + keyword)
- Query expansion for better coverage
- Reranking strategies
- Metadata-based filtering
- Retrieval quality evaluation (precision, recall, F1)

**Optimization Techniques:**
- Semantic + keyword hybrid search
- Query expansion and decomposition
- Multi-stage reranking
- Metadata filtering and scoring
- Length normalization

**Evaluation Metrics:**
- Precision@K: Fraction of relevant results
- Recall@K: Coverage of relevant documents
- MRR: Position of first relevant result
- NDCG: Quality of ranking
- MAP: System-wide performance

---

### Lesson 4.6: Corporate Knowledge Bot (Capstone)
**Type:** Code Screencast  
**Status:** ✅ Complete

Build a deployable knowledge assistant combining all Module 4 concepts.

#### Run Instructions
```bash
source .venv/bin/activate
export COHERE_API_KEY='your-key-here'  # Optional
streamlit run lesson-06-corporate-knowledge-bot.py
```

**What You'll Learn:**
- Complete knowledge bot architecture
- Document ingestion at scale
- Search interface design
- Query history and analytics
- Deployment patterns

**Features:**
- Semantic search over company knowledge base
- Suggested queries for exploration
- Search quality metrics (relevance scores)
- Query history tracking
- Metadata-aware filtering
- Deployment-ready code

**Output:** Production-ready knowledge assistant

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
