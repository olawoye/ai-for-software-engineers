# 08 Running Projects

1. Streamlit lessons: `uv run streamlit run src/app.py` displays the companion UI so you can browse `project-todo/` lessons alongside `project-completed/` references.
2. CLI walkthroughs: `uv run python -m src.cli_agent project-todo/...` prints the TODO blocks and reinforces the single-lesson rule from `agents.md`.
3. Scripts: `scripts/run_streamlit.sh` and `scripts/run_cli_agent.sh` wrap the above commands for macOS/WSL terminals; source `.venv` first.
4. Shared dependencies: `shared/utils/helpers.py` powers lesson listings and instrumentation so every run command stays consistent.
5. Document runtime variables or provider toggles (OpenAI vs. OpenRouter) in `docs/05-openrouter-setup.md` / `docs/06-ollama-setup.md` before executing heavy jobs.
