# 01 Local Setup

1. Clone `ai-for-software-engineers` and open the folder in your terminal (macOS Terminal/iTerm or WSL Ubuntu).
2. Create and activate a virtual environment (`python -m venv .venv` followed by `source .venv/bin/activate` or `.\\.venv\\Scripts\\Activate.ps1`).
3. Install dependencies with `uv sync` if you use `uv`, or `pip install -r requirements.txt` when starting out.
4. Configure your editor to use `.venv` so linting, formatting, and IntelliSense resolve the shared helpers.
5. Review `shared/utils/helpers.py`, `shared/utils/settings.py`, and the lesson directories to understand how the repo is split between `project-todo/` and `project-completed/`.
