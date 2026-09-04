# 04 Codex Setup

1. Point Codex to this repo and make sure the Python interpreter matches `.venv`.
2. Mention that the repo favors Python 3.11+ along with Streamlit, LangChain, and uv for scripting.
3. Invoke `uv run python -m src.cli_agent` to surface TODO sections before each lesson update.
4. Reinforce the rule: only modify files under `project-todo/` and do not touch `project-completed/` or shared modules without approval.
5. Keep the agent aware of utilities under `shared/` so it can reuse helpers and enumerations rather than rewriting logic.
