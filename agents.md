# Course Companion Agent Brief

This is a **project code implementation companion** for the "AI For Software Engineers" curriculum. Keep the following context in mind before responding:

## Awareness
- The repo has two parallel tracks: `project-completed/` (finished reference code) and `project-todo/` (scaffolded lessons you are expected to update). Treat `project-completed/` as view-only reference material.
- Shared utilities live in `src/` and the runtime expects Python plus the Streamlit/CLI helpers documented in the course knowledge guides under `docs/knowledge/` for the public GitHub Pages version.
- The public-facing course site is in `docs/` and is styled for GitHub Pages using Markdown files with front matter for clean navigation and simple landing pages.
- `docs/` is intended for public consumption; the local `knowledge/` folder remains as a project reference, while published course docs live under `docs/knowledge/`.
- Every module folder is prefixed with `module-XX-...` to align with the course curriculum.
- Each language folder under `docs/` should include its own landing page and setup guide as part of the localized site structure. For example, `docs/es/` should contain both `README.md` and `setup.html`, and future language folders should follow the same pattern.
- When adding a new language, copy the structure and intent of the source English page, preserve the original meaning, and keep technical terms in English where appropriate (for example: Python, LLM, API, embeddings, tokens, arrays, boolean, LangChain, Streamlit, Git, VS Code). Do not translate core programming concepts or tool names unless the language-specific convention is already standard and widely accepted in the target region.

## Instructions
1. **Work on one lesson at a time.** Accept a lesson file path from the learner (e.g., `project-todo/module-03-ai-developer-toolkit/lesson-01-calling-llm-apis.py`) and only touch that file.
2. **Edit only the commented TODO sections** within the assigned file—do not restructure the file, rename modules, or change `project-completed/` assets.
3. **Respect the lesson phase comments.** Each `project-todo/` file outlines phases (setup, prompt design, experimentation); your work should correspond to the indicated phase(s).
4. **Cite references.** When you update a lesson, mention which shared helper from `src/` or which completed lesson file inspired your change.
5. **Declare completion.** After finishing a lesson, summarize what was done and which phase is now covered.

## Samples & References
- Reference `docs/knowledge/module-structure.md` for module-to-lesson alignment.
- Use the public-facing docs site in `docs/` as the GitHub Pages landing surface; keep the pages concise and navigable with front matter and lightweight cross-links.
- Look at `project-completed/` lessons for working implementations; for example, `project-completed/module-02-ai-fundamentals/lesson-01-llms-under-the-hood.py` demonstrates how to score tokens.
- Use `src/settings.py` placeholders (once added) to toggle between OpenAI, Anthropic, OpenRouter, and Ollama.
- The course is primarily in English, but the docs site should support additional language entry points such as Spanish while keeping key frameworks, code, and syntax in English.

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

## Resource Scripts (`resource_*.py` Files)

Each module can include reusable utility scripts following the `resource_[name].py` naming convention. These are production-grade helper functions and utilities that learners can extract and use in their own projects.

### What Are Resource Scripts?
- **Purpose**: Provide copy-paste utilities that complement lesson code (token budgeting, cost calculation, embedding generation, etc.)
- **Location**: `project-completed/module-XX-[name]/resource_[name].py`
- **Quality Bar**: Must be well-tested, documented, and include a working `__main__` block
- **Scope**: Focused helpers (3-5 functions per file), not full applications

### Creating & Updating Resource Scripts
1. **Naming**: Always use `resource_[descriptive_name].py` format
2. **Functions**: Export 2-5 public functions with clear docstrings and type hints
3. **Example**: Include a `__main__` block that demonstrates each function with realistic data
4. **Testing**: All resource scripts are auto-tested by `test_module_resources.py`
   ```bash
   pytest test_module_resources.py -v
   ```
5. **Documentation**: When a resource script is added/updated, document it in the module's README under "Resource Scripts" section

### Example: Module 2's `resource_token_economics.py`
Located at `project-completed/module-02-ai-fundamentals/resource_token_economics.py`:
- `budget_and_truncate_context()` — ensure prompts stay within token limits
- `calculate_request_cost()` — compute API costs with prompt caching discounts
- `chunk_prompt_by_tokens()` — split text into overlapping token-aware chunks

Learners can import and reuse these in their projects:
```python
from resource_token_economics import budget_and_truncate_context, calculate_request_cost
safe_prompt, token_count = budget_and_truncate_context(text, max_token_budget=2048)
cost = calculate_request_cost(input_tokens=5000, output_tokens=500, cached_tokens=3000)
```

## Lesson-by-Lesson Implementation Workflow

### When Implementing Code Screencast Lessons

**Process:**
1. **Proposal Stage** (Agent → User)
   - Propose a specific implementation style for the lesson
   - Suggest optimal UI/UX (Streamlit, CLI, script output)
   - Describe input/output patterns
   - Explain how this best demonstrates the lesson objectives
   - Reference the curriculum learning goals

2. **Approval Stage** (User → Agent)
   - User reviews proposal and approves/requests changes
   - Agent notes any modifications

3. **Implementation Stage** (Agent)
   - Build production-ready implementation in `project-completed/`
   - Include full working code with comments
   - Test and verify it runs without errors
   - Add example data/usage

4. **Scaffold Generation Stage** (Agent)
   - Generate empty TODO version in `project-todo/`
   - Add PHASE-based comments guiding implementation
   - Reference the completed version
   - Include hints but not solutions
   - Ensure it's completable by students or AI assistants

5. **Documentation Stage** (Agent)
   - Update lesson section in module README
   - Document run instructions
   - Explain learning objectives demonstrated
   - Note any dependencies or setup required

### Why This Approach

- **User approval ensures alignment** with learning goals before implementation
- **Iterative design** catches poor UX/architecture early
- **Consistent style** across all lessons and modules
- **Educational value** maintained through thoughtful TODO scaffolding
- **Reusable pattern** for all future module implementations

## Code Example Generation Pattern/Architecture (Modules 4-6+)

Use this pattern for code-screencast lessons in Modules 4, 5, and 6 (and future modules unless explicitly overridden):

### 1) Proposal-First Pattern (Before Writing Code)
- For each code lesson, propose exactly 1 primary example method.
- A 2nd method is allowed only when it provides a clearly different implementation angle.
- Each proposed example must include:
   - Lesson objective alignment
   - What the method achieves
   - Inputs and outputs
   - Shared dependencies it references
   - Why this is the minimum useful implementation for the lesson
- Wait for learner approval before implementation.

### 2) Template-First Design Rule
- Each code example serves **dual purpose**: teaching the lesson concept AND providing a reusable template.
- Structure examples as production-ready patterns that learners can extract and adapt for their own projects.
- Include clear interfaces, minimal external dependencies, and intentional design choices that are transportable.
- Code must be self-contained enough to copy-paste into a new project with only minor configuration changes.

### 3) Method-Level Demo Rule
- Each example snippet is a single method.
- The method may call shared classes/utilities from `shared/`, `src/`, or prior modules.
- Keep each method modular and reusable so learners can copy it into personal projects with minimal coupling.

### 4) Single Facilitator Interface Rule
- Use exactly one facilitator per lesson demo set:
   - 1 Streamlit UI OR
   - 1 interactive CLI
- If there are 2 methods, both are demonstrated through the same facilitator.
- Interface selection guideline:
   - Streamlit UI: multiple inputs, mixed input types, uploads, or richer visual output
   - Interactive CLI: 1-2 text-only inputs and concise text output

### 5) UI/CLI Scope Rule
- UI/CLI is only an input/output bridge, not the core lesson.
- The core teaching artifact is the method implementation itself.
- Methods must include concise instructional comments explaining the implementation logic.

### 6) Learner Traceability Rule
- The facilitator must display:
   - Exact file path
   - Exact method name
   - Start line number (and end line when practical)
- This enables learners to jump directly from runtime behavior to source implementation.

### 7) Implementation Constraints
- Keep examples intentionally small but production-shaped.
- Reuse shared helpers where appropriate; do not duplicate infrastructure logic.
- Preserve compatibility with the existing module architecture and downstream lesson flow.
- Ensure outputs can be persisted when needed for subsequent lessons.

### 8) Delivery Sequence Per Lesson
1. Submit proposal with 1 (or at most 2) method demos.
2. Receive learner approval.
3. Implement completed version.
4. Implement TODO scaffold version.
5. Update README run instructions and data-flow notes.

### 9) Business Scenario Cohesion Rule
- Every example must be anchored to a realistic business scenario.
- Prefer the business scenario explicitly defined in `docs/knowledge/curriculum_v2.md` for that lesson.
- If a lesson does not define one, choose a common, practical scenario that fits the lesson objective.
- For modules with a lesson-6 capstone (for example Modules 4 and 5), lessons before the capstone should be designed so their examples can converge into the capstone system.
- This means earlier lessons may address different technical topics, but their outputs, data shapes, and design choices should intentionally support the capstone goal.
