# Module 4: Practical RAG & Context Engineering — TODO Scaffold

This is the student workbook version with phase-based scaffolding. Each lesson builds RAG systems incrementally through PHASE comments.

## Working Through the Lessons

### Lesson 4.2: Embedding Your Data

**PHASE 1:** Document preparation
- Load sample documents
- Implement text chunking
- Show chunk statistics

**PHASE 2:** Embedding generation
- Initialize EmbeddingEngine
- Generate embeddings (Cohere or TF-IDF)
- Display embedding shapes

**PHASE 3:** Vector store integration
- Create VectorStore
- Add documents and embeddings
- Show store statistics

### Lesson 4.3: Vector Store Lab

**PHASE 1:** Basic storage
- Initialize vector store
- Store embeddings and documents
- Verify storage

**PHASE 2:** Similarity search
- Embed query
- Search vector store
- Display results with scores

**PHASE 3:** Metadata & persistence
- Add metadata to documents
- Filter by metadata
- Save/load vector store

### Lesson 4.4: Building the Pipeline

**PHASE 1:** Simple RAG
- Create document collection
- Initialize pipeline components
- Perform basic retrieval

**PHASE 2:** LLM integration
- Setup LLM client (optional)
- Generate grounded answers
- Show context used

**PHASE 3:** Error handling
- Add exception handling
- Log pipeline operations

### Lesson 4.5: RAG Optimization

**PHASE 1:** Problem diagnosis
- Show common retrieval issues
- Demonstrate missing documents
- Illustrate result ranking

**PHASE 2:** Hybrid retrieval
- Implement semantic search
- Implement keyword search
- Combine results

**PHASE 3:** Evaluation
- Calculate precision and recall
- Compute F1 score
- Analyze result quality

### Lesson 4.6: Capstone - Knowledge Bot

**PHASE 1:** Core bot
- KnowledgeBot class
- Document ingestion
- Query execution

**PHASE 2:** Streamlit UI
- Search interface
- Display results
- Show relevance scores

**PHASE 3:** Analytics
- Query history tracking
- Statistics display
- Export results

## Shared Modules to Implement

### shared/embeddings.py
- **EmbeddingEngine**: Cohere and TF-IDF support
- **Methods**: embed_documents(), embed_query()
- **PHASES**: 1) Basic structure, 2) Cohere integration, 3) TF-IDF fallback

### shared/vector_store.py
- **VectorStore**: In-memory storage with FAISS support
- **Methods**: add(), search(), save(), load()
- **PHASES**: 1) Basic storage, 2) Search operations, 3) Persistence

### shared/retriever.py
- **Retriever**: Semantic retrieval
- **HybridRetriever**: Semantic + keyword combined
- **PHASES**: 1) Basic retrieval, 2) Hybrid methods, 3) Reranking

### shared/prompts.py
- Prompt templates for RAG
- Context formatting functions
- **PHASES**: 1) Basic templates, 2) Dynamic formatting

### shared/rag_pipeline.py
- **RAGPipeline**: Complete workflow orchestration
- **RAGEvaluator**: Quality metrics calculation
- **PHASES**: 1) Pipeline structure, 2) Full workflow, 3) Evaluation

## Implementation Tips

1. **Start with Embeddings**: PHASE 1 focuses on the foundation
2. **Test Each Phase**: Run code after completing each phase
3. **Use Completed Version**: Reference project-completed/ if stuck
4. **Cohere Optional**: TF-IDF fallback works without API key

## Running Your Code

### Prerequisites
```bash
source .venv/bin/activate
pip install -r requirements-module-04.txt
export COHERE_API_KEY='your-key-here'  # Optional
```

### Script Lessons
```bash
python lesson-02-embedding-your-data.py
python lesson-03-vector-store-lab.py
python lesson-04-building-rag-pipeline.py
python lesson-05-rag-optimization.py
```

### Streamlit Lesson
```bash
streamlit run lesson-06-corporate-knowledge-bot.py
```

## Common Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: shared` | Ensure you're in the correct directory |
| Cohere API errors | TF-IDF fallback works without API key |
| Embedding shape mismatch | Check document count matches embedding count |
| Search returns no results | Verify documents were ingested correctly |

## Learning Resources

- **Embeddings**: cohere.com/docs/embeddings
- **Vector Search**: faiss.ai documentation
- **RAG Papers**: arxiv.org (search "retrieval-augmented generation")
- **Completed Code**: project-completed/module-04-*/

## Next Steps

After completing Module 4:
- ✅ You understand RAG architectures
- ✅ You can implement end-to-end retrieval systems
- ✅ You know optimization techniques
- ✅ Ready for Module 5: MCP Servers & Tooling
