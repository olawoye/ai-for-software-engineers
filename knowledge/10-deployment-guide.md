# 10 Deployment Guide

1. Choose a Python-friendly host (Streamlit Cloud, Render, Fly.io, or Railway) and point the service at `src/app.py` for the Streamlit experience.
2. Ensure `pyproject.toml`/`requirements.txt` capture all dependencies and set `PYTHONPATH` to include the root so `shared/` imports resolve.
3. Include environment variables (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `OPENROUTER_URL`, `OLLAMA_URL`) in the deploy service’s secret vaults.
4. Document any startup commands (e.g., `uv run streamlit run src/app.py`) within the platform’s web UI so reviewers can replicate the run locally.
5. When ready, add a `Procfile` or hosting-specific config referencing `uvicorn src.app:main --reload` if you later expose a FastAPI layer.
