# 03 Claude Code Setup

1. Open the repo in Claude Code and read `agents.md` so the assistant knows the parallel track strategy.
2. Assign a single lesson file from `project-todo/` to the agent, and remind it to only edit the TODO comments for that file.
3. Keep `project-completed/` open in a separate tab for the agent to reference finished implementations without modifying them.
4. When dealing with API keys, define them as environment variables inside Claude Code before running scripts.
5. Use `uv run python -m src.cli_agent <lesson-path>` to show the agent the current content and TODO markers before editing.
