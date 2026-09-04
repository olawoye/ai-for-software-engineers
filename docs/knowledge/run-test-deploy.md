# Running, Testing, and Deploying

-## Run
- Streams and CLI: `streamlit run src/app.py` and `python -m src.cli_agent` use the shared helpers in `src/`.
- Helper scripts: `scripts/run_streamlit.sh` and `scripts/run_cli_agent.sh` wrap those commands on macOS and WSL.
- Keep `project-completed/` open for reference while coding `project-todo/`.

## Test
- There are no automated tests yet; the pattern is to add lightweight validators in `src/tests/` as you expand lessons.
- Use `python src/lessons/example_validation.py` as a sanity check for dependency wiring.

## Deploy
- Pick a Python-friendly host (Streamlit Cloud, Render, Fly.io). Ensure `requirements.txt` matches the environment and point to `src/app.py` or `src/cli_agent.py` as the entry point.
- Use `uvicorn src.app:app --reload` (if a FastAPI submodule is added later) for production parity.
