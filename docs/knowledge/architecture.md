# Architecture & Runtime Stack

The shared Python runtime underpins both the Streamlit UI and the CLI agents. Key pillars:

- `Streamlit` drives the lightweight UI (`src/app.py`) and lets you preview lessons.
- `uvicorn` (invoked via `scripts/run_cli_agent.sh` or `uv run`) can host FastAPI or background agents later.
- `LangChain` orchestrates prompt chains, retrievers, and integrations with vector stores.
- `OpenAI` and `Anthropic` SDKs connect to both paid and free (OpenRouter/Ollama) endpoints via `shared/utils/settings.py`.
- `ChromaDB` stores lesson context and embeddings for RAG-style helpers.
- `uv` handles lightweight task execution and packaging for both CLI and UI flows.
- `shared/evals` standardizes custom evaluation metrics so tests and lesson logs align regardless of the module.

Shared helpers live in `src/` so both `project-completed/` lessons and `project-todo/` scaffolds can import them.
