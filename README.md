# AI For Software Engineers Companion

This repository is the code companion for the "AI For Software Engineers" course. It mirrors the course flow with two parallel tracks: learners can follow a working codebase for each lesson (in `project-completed/`) while also using the commented scaffolds in `project-todo/` to drive hands-on builds either through an AI CLI agent or a traditional IDE.

## Repository Structure
- `agents.md` — instructions for Codex/Claude agents so they stay aligned with the course architecture and workflow.
- `shared/` — reusable helpers (LLM, RAG, agent, eval, and utility modules) that prevent code duplication and can be imported by every lesson.
- `docs/` — topic-focused guides (numbered `01-*` through `10-*`) for IDE/agent setup, deployment, and ops so the root README stays high level.
- `project-completed/` — working lesson artifacts keyed by module/lesson, intended as reference implementations.
- `project-todo/` — lesson scaffolds with commented TODOs that agents/learners update one lesson at a time; treat `project-completed/` as view-only.
- `scripts/` — wrappers such as `run_streamlit.sh` and `run_cli_agent.sh` for macOS/WSL so the proper flows start with the virtual environment active.
- `pyproject.toml` + `uv` — dependencies and entrypoints so `uv sync`, `uv run streamlit run src/app.py`, and `uv run pytest tests/` become the standard tooling commands.

## Setup Overview

### One-Time Project Setup (All Platforms)
1. Clone this repo and open it in your terminal.
2. **Run the setup script** (creates isolated virtual environment + installs all dependencies):
   ```bash
   ./setup.sh
   ```
3. **Activate the environment**:
   ```bash
   source .venv/bin/activate  # macOS/Linux/WSL
   # OR
   .venv\Scripts\Activate.ps1  # Windows PowerShell
   ```
4. **Set your API key** (OpenRouter recommended for cost-free access):
   ```bash
   export OPENROUTER_API_KEY='your-key-here'
   ```

### Local IDE
1. Clone this repo and open it inside VS Code or your preferred Python editor.
2. The `setup.sh` script handles virtual environment creation and dependency installation (see above).
3. Once activated, open `project-completed/` to explore working lessons or `project-todo/` to see scaffolded exercises.
4. Run lessons individually or use the Streamlit dashboard for guided navigation.

### VS Code / Codex / Claude Code Setup
1. **VS Code**: Install the Python extension and set the interpreter to your `.venv`. Use the Command Palette to run the helper scripts in `scripts/` for linting or launching Streamlit.
2. **Codex / Claude Code**: Point your workspace at this repository and start with the `agents.md` brief so the agent knows the folder boundaries and lesson priorities.
3. **Subscription vs. FREE MCP**: If you have OpenAI/Anthropic subscriptions, configure the keys via environment variables (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`). If you prefer free alternatives, set up [OpenRouter](https://github.com/openrouter/openrouter) or [Ollama](https://ollama.com/) locally and configure the endpoints via `shared/utils/settings.py` (see `docs/vscode-codex-setup.md`).

### Running Lessons
1. **Activate your virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

2. **Run an individual lesson** (e.g., Lesson 2.2):
   ```bash
   cd project-completed/module-02-ai-fundamentals
   streamlit run lesson-02-tokens-context-completion.py
   ```

3. **Check module-specific run instructions**:
   Each module's README (e.g., `project-completed/module-02-ai-fundamentals/README.md`) lists lesson-specific commands and dependencies.

4. **Streamlit Dashboard** (multi-lesson nav, when built):
   ```bash
   streamlit run project-completed/module-02-ai-fundamentals/shared/streamlit_app.py
   ```

5. **Testing & Validation** (future):
   ```bash
   pytest tests/
   python src/lessons/example_validation.py
   ```

## Docs Reference
Detailed procedures live in `docs/`, including the numbered guides (`docs/01-local-setup.md` through `docs/10-deployment-guide.md`) plus the agent-frameworks primer. Review the relevant guide whenever you move to a new module or toolchain.

## Important: Git & Commits

### `.gitignore` Protection
The repository includes a comprehensive `.gitignore` that excludes:
- ✅ Virtual environments (`.venv/`, `venv/`)
- ✅ API keys & credentials (`.env`, `*.pem`, `*.key`)
- ✅ Python cache (`__pycache__/`, `*.pyc`)
- ✅ IDE files (`.vscode/`, `.idea/`)
- ✅ Student testing files (`student_*/`, `test_*.py`, `scratch/`)
- ✅ Temporary data & logs

**Never commit:**
- API keys or credentials
- Personal `.env` files
- Virtual environment directories
- IDE-specific settings
- Student experimentation/sandbox work

See `.gitignore` for the full list.

## Course Alignment
Modules follow the course narrative from AI shift foundations to advanced capabilities and career transition. Each folder inside `project-todo/`/`project-completed/` is prefixed with the module number so you can easily correlate a lesson to the curriculum outline in `docs/module-structure.md`.

## Next Steps
- Start with `project-todo/module-01-ai-shift-for-engineers/lesson-01-why-this-course-matters.py` for the first guided exercise.
- Use `agents.md` when invoking Codex or Claude to ensure the agent always focuses on a single lesson section at a time and treats `project-completed/` as reference only.
