"""
Lesson 2.2: Tokens, Context & Completion (TODO - Scaffold)

OBJECTIVE: Explore how LLMs process text through tokens and how context windows
constrain model behavior. Learn to estimate token usage, diagnose context failures,
and design prompts that operate within model limits.

BUSINESS SCENARIO: An AI application becomes expensive and produces poor answers
because prompts exceed context limits and token consumption was never monitored.

This lesson demonstrates:
1. How text is tokenized
2. Token budgeting and cost estimation
3. Context window constraints
4. Prompt design within limits
5. Persisting results for Lesson 2.3+

INSTRUCTIONS:
- Implement each STAGE in order, building toward a complete token analysis system
- Design your own interface: Streamlit UI, CLI, or Python script
- Save results to datasets/lesson-02-output.json for downstream lessons
- Reference the completed version for inspiration, not step-by-step replication
"""

# ============================================================================
# STAGE 1: Setup & Configuration
# ============================================================================
# Build infrastructure for file I/O and persistence.
# Key functions needed: load/save JSON, create output directory.
# Available shared utilities:
#   - shared.tokens: estimate_tokens(), check_context_fit(), calculate_cost(),
#                    get_context_window(), get_output_window()
#   - Standard library: json, pathlib.Path, datetime

# TODO: Add your Stage 1 implementation here


# ============================================================================
# STAGE 2: Token Analysis Engine
# ============================================================================
# Implement core analysis logic: estimate tokens, check context fit, calculate cost.
# Key logic: given a prompt + model + expected completion length,
#   determine if it fits and what it will cost.
# Available shared utilities:
#   - estimate_tokens(text: str) -> int
#   - check_context_fit(model: str, prompt_tokens: int, estimated_completion: int) -> Dict
#   - calculate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> Dict
#   - get_context_window(model: str) -> int

# TODO: Add your Stage 2 implementation here


# ============================================================================
# STAGE 3: User Interface (Build Your Way)
# ============================================================================
# Design input/output interface for token analysis.
# Option A: Streamlit dashboard with interactive controls
#   - Available: register_lesson() from shared.streamlit_app
#   - Build: model selector, prompt textarea, analysis button
# Option B: CLI with command-line prompts and formatted output
# Option C: Python script that reads from file or stdin
# Your choice! The goal: learners can explore token budgeting interactively.

# TODO: Add your Stage 3 implementation here


# ============================================================================
# STAGE 4: Display & Visualization
# ============================================================================
# Show token analysis results clearly.
# Display: prompt tokens, completion tokens, context fit status, estimated cost.
# Consider: metrics/tables for model comparison, warnings if over context limit.
# Optional: visualizations (bar charts, progress bars, relevance scores).

# TODO: Add your Stage 4 implementation here


# ============================================================================
# STAGE 5: Persistence
# ============================================================================
# Save analysis results to datasets/lesson-02-output.json.
# Structure: {"lesson_2_2": {"explorations": [analysis_dicts]}}
# This output feeds into Lesson 2.3+ for cost analysis and recommendations.

# TODO: Add your Stage 5 implementation here
#         "timestamp": "2024-06-22T12:35:22.987654",
#         "actual_response": "Quantum computing leverages quantum mechanics...",
#         "actual_usage": {
#           "prompt_tokens": 8,
#           "completion_tokens": 147,
#           "total_tokens": 155
#         },
#         "actual_cost": {
#           "input_cost": 0.000001,
#           "output_cost": 0.000062,
#           "total_cost": 0.000063
#         }
#       }
#     ]
#   }
# }

# ============================================================================
# TESTING CHECKLIST:
# ============================================================================
# ✅ Token estimator works correctly (test: 10 words ≈ 7-8 tokens)
# ✅ Context fit detection works (under 80% = OK, over 80% = warning)
# ✅ Cost calculation shows reasonable values
# ✅ Streamlit UI displays all sections
# ✅ Interactive prompt input works
# ✅ Example hardcoded prompt loads
# ✅ "Analyze Prompt" button: theory-only analysis displays correctly
# ✅ "Generate & Analyze" button: requires API key, shows error if missing
# ✅ Real LLM response displays in scrollable container
# ✅ Actual token usage from API matches response object
# ✅ Actual cost calculation is accurate
# ✅ Estimate vs Actual comparison table shows differences
# ✅ Analysis saved to JSON file (both theory and live)
# ✅ Previous explorations load on refresh
# ✅ Run: streamlit run lesson-02-tokens-context-completion.py
# ✅ Run with API key: export OPENROUTER_API_KEY='...' first
