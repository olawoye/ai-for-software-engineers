# Module 2: AI Fundamentals

This module establishes the technical foundation for the course. Students develop practical understanding of how modern Large Language Models work, how they process information, how context influences behavior, and how retrieval and embeddings enable AI systems to reason over proprietary knowledge.

## Module Overview

By the end of this module, students will:
- Understand core concepts that underpin RAG systems, agents, and production AI applications
- Learn how LLMs process information through tokens and context windows
- Explore prompting strategies, retrieval techniques, and fine-tuning trade-offs
- Build foundational AI applications using embeddings and semantic search

## Lessons

### Lesson 2.1: LLMs Under the Hood
**Type:** Talking Head (No Code)  
This lesson introduces Large Language Models from a software engineer's perspective.

### Lesson 2.2: Tokens, Context & Completion
**Type:** Code Screencast  
**Status:** ✅ Complete

Learn how LLMs tokenize text, manage context windows, and calculate costs.

#### Run Instructions
```bash
# Ensure virtual environment is active
source .venv/bin/activate

# Set your API key (OpenRouter is free-friendly)
export OPENROUTER_API_KEY='your-key-here'

# Run the Streamlit app
streamlit run lesson-02-tokens-context-completion.py
```

**What You'll Learn:**
- Token estimation and budgeting
- Context window constraints
- Cost calculation (input/output tokens)
- Prompt design within limits

**Output:** Results saved to `../datasets/lesson-02-output.json` for Lesson 2.3+

**Key Files:**
- `lesson-02-tokens-context-completion.py` — Main interactive app
- `shared/tokens.py` — Token utilities (reusable)
- `shared/api_client.py` — LLM API wrapper (reusable)
- `shared/streamlit_app.py` — Dashboard framework (reusable)

---

### Lesson 2.3: Transformer Architecture
**Type:** Talking Head (No Code)  
This lesson provides a visual explanation of transformer architecture and self-attention mechanisms.

---

### Lesson 2.4: Prompting, Retrieval & Fine-Tuning
**Type:** Code Screencast  
**Status:** ✅ Complete

Compare three approaches to improve AI outputs and choose the best for your scenario.

#### Run Instructions
```bash
source .venv/bin/activate
export OPENROUTER_API_KEY='your-key-here'
streamlit run lesson-04-prompting-retrieval-finetuning.py
```

**What You'll Learn:**
- Compare prompt engineering, RAG, and fine-tuning
- Evaluate tradeoffs: cost, complexity, maintainability
- Decision matrix for approach selection
- Real-world scenarios for each approach

**Output:** Results saved to `../datasets/lesson-04-output.json`

---

### Lesson 2.5: Embeddings & Semantic Search
**Type:** Code Screencast  
**Status:** ✅ Complete

Build semantic search using embeddings and vector databases.

#### Setup: Get Your Cohere API Key
This lesson uses **Cohere embeddings** by default (free tier, 100k requests/month).

1. **Sign up** at [cohere.com](https://cohere.com) (no credit card needed)
2. **Get API key** from dashboard
3. **Set environment variable:**
   ```bash
   export COHERE_API_KEY='your-key-here'
   ```

#### Run Instructions
```bash
source .venv/bin/activate
export COHERE_API_KEY='your-key-here'
streamlit run lesson-05-embeddings-semantic-search.py
```

**What You'll Learn:**
- Generate embeddings from text (semantic understanding)
- Build semantic search index using Cohere
- Understand embedding vectors and similarity
- Automatic fallback to TF-IDF if API key not set
- Create reusable document corpus

**Embedding Options:**
- **Primary (Cohere)**: True semantic search, free tier 100k requests/month → recommended for learning
- **Fallback (TF-IDF)**: Lightweight, keyword-based, no API key needed
- **Optional (sentence-transformers)**: Best quality, local, requires several GB install

**Output:** Corpus and metadata saved to `../datasets/lesson-05-output.json` → Lesson 2.6 input

**Key Concepts:**
- Semantic embeddings vs keyword search
- Vector similarity (cosine similarity)
- Relevance scoring
- Document ranking by meaning


---

### Lesson 2.6: Build a Mini Search Demo
**Type:** Code Screencast  
**Status:** ✅ Complete

Build a production-like semantic search application combining all lessons 2.2-2.5.

#### Run Instructions
```bash
source .venv/bin/activate
streamlit run lesson-06-mini-search-demo.py
```

**What You'll Learn:**
- Build complete search application
- Intuitive search interface with hero bar
- Results displayed as cards with relevance scores
- Add documents mid-session
- Track search analytics

**Output:** Application state saved to `../datasets/lesson-06-output.json`

**Key Features:**
- Loads corpus from Lesson 2.5 automatically
- Suggested queries to get started
- Result snippets + full document preview
- Relevance score visualization (🟢🟡🔴)
- Search history tracking
- TF-IDF search (lightweight, instant)

---

## Shared Resources

All lessons in this module leverage shared utilities in `shared/`:

- **`api_client.py`** — Consistent LLM client wrapper (supports OpenRouter, Anthropic, OpenAI)
- **`tokens.py`** — Token counting, context window validation, cost estimation
- **`embeddings.py`** — Embedding generation and comparison
- **`streamlit_app.py`** — Multi-lesson dashboard framework

## Data Flow

Each lesson outputs results to `datasets/lesson-XX-output.json`:
- Lesson 2.2 outputs token analyses → input for Lesson 2.3+
- Lesson 2.5 outputs embeddings → input for Lesson 2.6+
- All outputs feed into Module 3+ lessons

## Setup & Dependencies

### First-Time Setup (Required Once)
```bash
# Create clean virtual environment
rm -rf .venv  # Remove old venv if it exists
./setup.sh
source .venv/bin/activate

# Install Module 2 base dependencies (lightweight, ~50MB, includes Cohere)
pip install -r requirements-module-02.txt
```

**First run:** Lessons 2.2, 2.4, 2.5 are instant (cloud-based APIs, no downloads).

### Lessons 2.2 & 2.4: OpenRouter API Key
```bash
export OPENROUTER_API_KEY='your-key-here'
```

### Lesson 2.5: Cohere API Key (Primary Method - Recommended)
```bash
# Sign up free at https://cohere.com (no credit card needed)
# Free tier: 100k requests/month — plenty for learning and demos
export COHERE_API_KEY='your-key-here'
```

If `COHERE_API_KEY` is not set, Lesson 2.5 automatically falls back to TF-IDF (keyword-based, no API key needed).

### Optional Performance Upgrades

**For local semantic embeddings** (runs entirely on your machine):
```bash
# ⚠️ Warning: Adds several GB to venv size, requires PyTorch
pip install sentence-transformers faiss-cpu

# Then uncomment the sentence-transformer sections in:
# - lesson-05-embeddings-semantic-search.py (lines ~154-191)
# - lesson-06-mini-search-demo.py (similar section)
```

**Benefits of local embeddings:**
- ✅ No API key needed
- ✅ Runs locally, faster for repeated queries
- ⚠️ Large install (~several GB), slower first-time generation
- ✅ Highest quality embeddings available

**Lesson 2.5 Fallback Chain:**
1. **Cohere** (if `COHERE_API_KEY` set) → True semantic search, recommended for learning
2. **TF-IDF** (if Cohere unavailable) → Keyword-based, instant, no API key
3. **sentence-transformers** (if installed) → Best quality, local, no API key


---

## Reference

- Full curriculum: `docs/curriculum_v1.md`
- Agent instructions: `agents.md`
- Architecture guide: `docs/architecture.md`
