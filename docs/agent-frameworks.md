# Agent Frameworks Primer

- The course emphasizes **custom-built agent loops** first: observe → reason → act → reflect. Each lesson in `project-todo/module-06-ai-agents-autonomy/` should implement that loop with plain Python helpers and shared state in `shared/agents`.
- Use `shared/evals/AgentEval` to capture metrics (action counts, confidence) once your agent executes; log the results for future comparisons.
- After mastering the first-principles loop, introduce frameworks like **LangGraph** or **OpenAI Agents SDK** by mapping their abstractions back to the custom steps you already implemented. Treat those frameworks as overlays—not replacements—for the handcrafted code.
- Keep this doc updated with pointers to lesson files that demonstrate custom loops first before referencing the built-in orchestrators that appear later in the curriculum.
