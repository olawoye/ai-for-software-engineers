# 07 MCP Setup

1. MCP modules run inside `project-todo/module-05-developing-mcp-servers-tooling/`. Use FastAPI/Uvicorn stubs for upcoming lessons.
2. Shared utilities (`shared/evals`, `shared/agents`, `shared/utils`) provide consistent logging, monitoring hooks, and evaluation scaffolding for server lessons.
3. Document endpoints, secrets, and observability requirements before implementing the lesson code per `agents.md`.
4. Use `uv run` scripts to launch the server components so that MCP tooling, CLI agents, and Streamlit views can reuse the same runtime dependencies.
5. When migrating to cloud, ensure you capture API key handling as shown in `shared/utils/settings.py` so deployments inherit the same environment variables.
