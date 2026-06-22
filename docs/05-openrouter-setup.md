# 05 OpenRouter Setup

1. Install OpenRouter (see https://github.com/openrouter/openrouter) and expose the HTTP endpoint on `https://api.openrouter.ai/v1/chat/completions`.
2. Update `OPENROUTER_URL` in your environment or `.env` variant if you self-host or use a custom API key.
3. Use `shared/utils/settings.py` to switch between paid OpenAI/Anthropic keys and OpenRouter.
4. When working through RAG or agent lessons, replace the provider block with the `openrouter_url` field rather than hard-coding into lesson files.
5. Document any additional headers or trace IDs you collect for debugging in `docs/08-running-projects.md` so future lessons reuse the pattern.
