# 06 Ollama Setup

1. Install Ollama (https://ollama.com/) for a local, free inference endpoint and ensure the CLI can call `http://localhost:11434/completions`.
2. Set `OLLAMA_URL` in `.env` or your shell profile, and confirm `shared/utils/settings.py` picks it up when other keys are absent.
3. Use Ollama for early lessons where pricing is a concern, then swap to hosted OpenAI/Anthropic for more advanced modules.
4. Keep the same request schema across providers so lessons can reference the same `shared` helpers and only substitute the base URL.
5. Share troubleshooting notes (network, TLS) in `docs/08-running-projects.md` so learners know how to restart Llama models when necessary.
