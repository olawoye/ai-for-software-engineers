# 09 Testing Projects

1. Run `uv run python src/lessons/example_validation.py` to verify key dependencies (Streamlit, LangChain, ChromaDB) are importable.
2. Future modules should include dedicated tests under `tests/` so `uv run pytest tests/` succeeds; start with lightweight API expectations or helper outputs from `shared/utils`.
3. Reuse `shared/evals` (`BaseEval`, `RAGEval`, `AgentEval`) to keep performance metrics consistent when new evaluation scripts arrive.
4. Document your lesson-specific validation plan in `project-todo/module-XX/...` so later graders know how to rerun the checks.
5. Track test data or vector store snapshots under `datasets/` (future addition) but keep the repo tidy by mocking eval metrics until artifacts are ready.
