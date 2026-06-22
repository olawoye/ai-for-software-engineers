# VS Code, Codex, and Claude Code Guidance

1. **VS Code**
   - Install the Python extension and configure the interpreter to `.venv`.
   - Use the Command Palette to run `Python: Select Interpreter` and `Terminal: Create New Integrated Terminal` so it inherits the virtual environment.

2. **Codex / Claude Code**
   - Open this repository and read `agents.md` before invoking the agent.
   - Assign the agent a single lesson file (e.g., `project-todo/module-02-ai-fundamentals/lesson-01-llms-under-the-hood.py`).
   - Enforce the instruction: “Update only the TODO comments in the assigned lesson and keep the rest of the repo untouched.”

3. **Subscriptions vs. Free MCP options**
   - With paid access, set `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` using your provider console and confirm they appear in your environment.
- For a free stack, install [OpenRouter](https://github.com/openrouter/openrouter) or [Ollama](https://ollama.com/) and configure the downstream endpoint via `shared/utils/settings.py`.

4. **Tooling connection points**
   - Use `scripts/run_streamlit.sh` or `scripts/run_cli_agent.sh` to start recommended flows.
   - Toggle between the UI and CLI in VS Code’s terminal where you can step through the modules interactively.
