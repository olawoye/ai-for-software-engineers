# Local IDE Setup

This guide keeps your workspace grounded in a predictable Python toolchain.

1. **Clone and open**
   - Clone this repo and open the root folder in your local IDE (VS Code, PyCharm, etc.).
   - Keep the terminal focused on the repo root.

2. **Python environment**
   - Create a virtual environment: `python -m venv .venv`.
   - Activate it per your OS: `.\.venv\Scripts\Activate.ps1` (PowerShell/WSL) or `source .venv/bin/activate` (macOS/Linux).

3. **Dependencies**
   - Install from `requirements.txt`.
   - Run `pip install -r requirements.txt` and confirm `langchain`, `streamlit`, `openai`, `anthropic`, `chromadb`, and `uvicorn` are installed.

4. **IDE helpers**
   - Configure linting (e.g., `pylint`, `flake8`) and formatting (`black`).
   - Point your AI assistant (Codex/Claude) at `agents.md` before asking for help.

5. **Streamlit workflow**
   - Launch the UI with `streamlit run src/app.py` and keep `docs/run-test-deploy.md` handy for deployment notes.
