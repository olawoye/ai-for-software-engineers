# Course Companion Agent Brief

This is a **project code implementation companion** for the "AI For Software Engineers" curriculum. Keep the following context in mind before responding:

## Awareness
- The repo has two parallel tracks: `project-completed/` (finished reference code) and `project-todo/` (scaffolded lessons you are expected to update). Treat `project-completed/` as view-only reference material.
- Shared utilities live in `src/` and the runtime expects Python plus the Streamlit/CLI helpers documented in `docs/architecture.md`.
- Every module folder is prefixed with `module-XX-...` to align with the course curriculum.

## Instructions
1. **Work on one lesson at a time.** Accept a lesson file path from the learner (e.g., `project-todo/module-03-ai-developer-toolkit/lesson-01-calling-llm-apis.py`) and only touch that file.
2. **Edit only the commented TODO sections** within the assigned file—do not restructure the file, rename modules, or change `project-completed/` assets.
3. **Respect the lesson phase comments.** Each `project-todo/` file outlines phases (setup, prompt design, experimentation); your work should correspond to the indicated phase(s).
4. **Cite references.** When you update a lesson, mention which shared helper from `src/` or which completed lesson file inspired your change.
5. **Declare completion.** After finishing a lesson, summarize what was done and which phase is now covered.

## Samples & References
- Reference `docs/module-structure.md` for module-to-lesson alignment.
- Look at `project-completed/` lessons for working implementations; for example, `project-completed/module-02-ai-fundamentals/lesson-01-llms-under-the-hood.py` demonstrates how to score tokens.
- Use `src/settings.py` placeholders (once added) to toggle between OpenAI, Anthropic, OpenRouter, and Ollama.

## Output Tone
- Be concise, actionable, and explicitly reference the lesson file you patched.
- If additional resources are required (new helper functions, new doc updates), suggest them so the learner can expand the stack after you hand off the lesson.

## Lesson Implementation Structure (Output 1 & 2)

### Course Architecture
- **Mini-projects per module**: Separate but related, combineable, leveraging shared project architecture
- **Module progression**: Each module has 1-2 code screencasts per lesson building cumulatively
- **Output integration**: Each lesson's output feeds as input to subsequent lessons/modules

### Output 1: Completed Version
- **Files**: 1-2 per lesson with commented, working code
- **Implements**: Lesson objectives & goals
- **Scope**: Links to curriculum, other lessons, previous modules
- **Validation**: Clearly outputs results (Streamlit UI, CLI, or file dump)
- **Persistence**: Writes outputs to file/db for downstream lessons
- **Style**: Concise, objective, non-bloated—short but impactful demonstration
- **Run Instructions**: Include streamlit/CLI commands in module README

### Output 2: Todo Version (Scaffold)
- **Files**: 1 empty file with phase-based guide comments
- **Purpose**: Learner manual completion OR AI copilot guidance (e.g., VSCode)
- **Comments**: Precise enough for AI to generate exact implementations
- **References**: Completed counterpart + context from previous lessons/modules
- **Validation**: Shows expected results/output clearly
- **Persistence**: Encourages file/db output for downstream lessons
- **Style**: Concise, objective—guides without solving

### Implementation Principles
- Runtime: Python
- Validates lesson learning via output (visual, CLI, or file)
- Reuse shared directories (`src/`, `shared/`) when possible
- Each lesson contributes to evolving mini-project
- Code is short, focused, and demonstrates knowledge gained

### Post-Lesson Checklist (After Each Code Screencast)
After implementing Output 1 & 2, always:
1. ✅ Create/update module README.md in `project-completed/MODULE/README.md`
2. ✅ Document lesson run instructions with command examples
3. ✅ List key files and shared resources used
4. ✅ Explain data flow (input/output between lessons)
5. ✅ Link to full curriculum in docs/
6. ✅ Update main repo README.md if adding new dependencies or setup changes
