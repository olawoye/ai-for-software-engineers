# AI For Software Engineers Companion

Course author: Ifeoluwa Mobolaji Olawoye

This repository is the code companion for the "AI For Software Engineers" course. It mirrors the course flow with two parallel tracks: learners can follow a working codebase for each lesson (in `project-completed/`) while also using the commented scaffolds in `project-todo/` to drive hands-on builds either through an AI CLI agent or a traditional IDE.

## Repository Structure
- `agents.md` — instructions for Codex/Claude agents so they stay aligned with the course architecture and workflow.
- `shared/` — reusable helpers (LLM, RAG, agent, eval, and utility modules) that prevent code duplication and can be imported by every lesson.
- `docs/` — GitHub Pages-ready course website and public landing pages written in Markdown with front matter for navigation.
- `docs/knowledge/` — public knowledge/reference material, setup notes, and curriculum context for the course site.
- `knowledge/` — local source/reference copy retained for project use while the public docs site uses the GitHub Pages version under `docs/`.
- `project-completed/` — working lesson artifacts keyed by module/lesson, intended as reference implementations.
- `project-todo/` — lesson scaffolds with commented TODOs that agents/learners update one lesson at a time; treat `project-completed/` as view-only.
- `scripts/` — wrappers such as `run_streamlit.sh` and `run_cli_agent.sh` for macOS/WSL so the proper flows start with the virtual environment active.
- `pyproject.toml` + `uv` — dependencies and entrypoints so `uv sync`, `uv run streamlit run src/app.py`, and `uv run pytest tests/` become the standard tooling commands.

## Course Website
The public course site lives in `docs/` and is designed for GitHub Pages at `https://olawoye.github.io/ai-for-software-engineers/` or the equivalent repository GitHub Pages URL. The docs area is intentionally lightweight and uses Markdown plus front matter for clean navigation and language entry points.

- `docs/index.md` — main course landing page
- `docs/es/README.md` — Spanish-language intro page
- `docs/knowledge/` — deeper setup, curriculum, and reference material served through GitHub Pages

## Setup Overview

### One-Time Project Setup (All Platforms)
1. Clone this repo and open it in your terminal.
2. **Run the setup script** (creates isolated virtual environment + installs dependencies for Modules 2-7):
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

**Note on Module 9:** The setup script includes dependencies for Modules 2-7 only. When you're ready to work on Module 9 (Lesson 9.2 - Fine-Tuning), install optional heavy dependencies separately:
   ```bash
   pip install -r requirements-module-09.txt  # PyTorch + HuggingFace (~2.5GB)
   ```
See [Module 9 README](project-completed/module-09-advanced-capabilities-specializations/README.md) for details on which fine-tuning paths require this.

### Local IDE
1. Clone this repo and open it inside VS Code or your preferred Python editor.
2. The `setup.sh` script handles virtual environment creation and dependency installation (see above).
3. Once activated, open `project-completed/` to explore working lessons or `project-todo/` to see scaffolded exercises.
4. Run lessons individually or use the Streamlit dashboard for guided navigation.

### VS Code / Codex / Claude Code Setup
1. **VS Code**: Install the Python extension and set the interpreter to your `.venv`. Use the Command Palette to run the helper scripts in `scripts/` for linting or launching Streamlit.
2. **Codex / Claude Code**: Point your workspace at this repository and start with the `agents.md` brief so the agent knows the folder boundaries and lesson priorities.
3. **Subscription vs. FREE MCP**: If you have OpenAI/Anthropic subscriptions, configure the keys via environment variables (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`). If you prefer free alternatives, set up [OpenRouter](https://github.com/openrouter/openrouter) or [Ollama](https://ollama.com/) locally and configure the endpoints via `shared/utils/settings.py` (see `docs/knowledge/vscode-codex-setup.md`).

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

5. **Testing & Validation**:
   ```bash
   # Run all resource script tests (validates resource_*.py files)
   pytest test_module_resources.py -v
   
   # Run module-specific tests
   pytest tests/
   ```

## Resource Scripts

Each module includes `resource_*.py` files — reusable code snippets and utilities you can import into your own projects. These are production-quality, well-tested helpers that complement the lesson code.

**Finding & Testing Resource Scripts:**
- All resource files follow the `resource_[name].py` naming convention
- Located in each module's folder (e.g., `project-completed/module-02-ai-fundamentals/resource_token_economics.py`)
- Run the automated test suite to validate all resource scripts:
  ```bash
  pytest test_module_resources.py -v
  ```
- This validates syntax, imports, callable functions, and the sample `__main__` block

**Using Resource Scripts:**
```python
from project-completed.module-02-ai-fundamentals.resource_token_economics import budget_and_truncate_context, calculate_request_cost

# Use the utilities in your own projects
safe_prompt, token_count = budget_and_truncate_context("Your text here", max_token_budget=2048)
cost = calculate_request_cost(input_tokens=5000, output_tokens=500)
```

## Knowledge Reference
Detailed procedures live in `docs/knowledge/`, including the numbered guides (`docs/knowledge/01-local-setup.md` through `docs/knowledge/10-deployment-guide.md`) plus the agent-frameworks primer. Review the relevant guide whenever you move to a new module or toolchain.

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
Modules follow the course narrative from AI shift foundations to advanced capabilities and career transition. Each folder inside `project-todo/`/`project-completed/` is prefixed with the module number so you can easily correlate a lesson to the curriculum outline in `docs/knowledge/module-structure.md`.

## Next Steps
- Start with `project-todo/module-01-ai-shift-for-engineers/lesson-01-why-this-course-matters.py` for the first guided exercise.
- Use `agents.md` when invoking Codex or Claude to ensure the agent always focuses on a single lesson section at a time and treats `project-completed/` as reference only.
