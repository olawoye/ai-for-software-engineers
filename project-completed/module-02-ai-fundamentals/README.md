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
**Status:** 🔄 In Progress

Compare prompting, RAG, and fine-tuning strategies.

#### Run Instructions (when ready)
```bash
source .venv/bin/activate
export OPENROUTER_API_KEY='your-key-here'
streamlit run lesson-04-prompting-retrieval-finetuning.py
```

---

### Lesson 2.5: Embeddings & Semantic Search
**Type:** Code Screencast  
**Status:** 🔄 In Progress

Learn how embeddings power semantic search and retrieval systems.

#### Run Instructions (when ready)
```bash
source .venv/bin/activate
export OPENROUTER_API_KEY='your-key-here'
streamlit run lesson-05-embeddings-semantic-search.py
```

---

### Lesson 2.6: Build a Mini Search Demo
**Type:** Code Screencast  
**Status:** 🔄 In Progress

Build a complete semantic search application combining tokens, embeddings, and retrieval.

#### Run Instructions (when ready)
```bash
source .venv/bin/activate
export OPENROUTER_API_KEY='your-key-here'
streamlit run lesson-06-mini-search-demo.py
```

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

See the main [README.md](../../README.md) for project-wide setup instructions.

**Quick Start:**
```bash
./setup.sh
source .venv/bin/activate
```

## Reference

- Full curriculum: `docs/curriculum_v1.md`
- Agent instructions: `agents.md`
- Architecture guide: `docs/architecture.md`
