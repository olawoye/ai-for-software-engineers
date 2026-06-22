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
- Implement each PHASE in order
- Use the completed version (project-completed/) as reference
- Leverage shared utilities from shared/
- Output results to datasets/lesson-02-output.json
- Use Streamlit for interactive demonstration
"""

# ============================================================================
# PHASE 1: Imports & Setup
# ============================================================================
# TODO: Import required libraries:
#   - json (for saving results)
#   - streamlit (for UI)
#   - datetime (for timestamps)
#   - Path from pathlib (for file operations)
#
# TODO: Import from shared utilities:
#   - estimate_tokens, check_context_fit, calculate_cost from shared.tokens
#   - register_lesson from shared.streamlit_app

# ============================================================================
# PHASE 2: Output Directory & Persistence Functions
# ============================================================================
# TODO: Implement setup_output_dir():
#   - Create 'datasets' directory if it doesn't exist
#   - Return the directory path
#
# TODO: Implement load_lesson_output():
#   - Load datasets/lesson-02-output.json if it exists
#   - Return loaded JSON data or empty dict with structure:
#     {"lesson_2_2": {"explorations": []}}
#
# TODO: Implement save_lesson_output(data):
#   - Save data dict to datasets/lesson-02-output.json
#   - Use json.dump with indent=2 for readability

# ============================================================================
# PHASE 3: Token Analysis Engine
# ============================================================================
# TODO: Implement analyze_prompt(user_prompt, model, max_completion=500):
#   - Call estimate_tokens() on user_prompt
#   - Call check_context_fit() with prompt_tokens and max_completion
#   - Call calculate_cost() with model, prompt_tokens, max_completion
#   - Return dict with analysis results:
#     {
#       "prompt": user_prompt,
#       "model": model,
#       "prompt_tokens": <estimated>,
#       "estimated_completion_tokens": max_completion,
#       "context_analysis": <from check_context_fit>,
#       "estimated_cost": <from calculate_cost>,
#       "timestamp": <current ISO datetime>
#     }

# ============================================================================
# PHASE 4: Streamlit Dashboard Interface
# ============================================================================
# TODO: Implement render_lesson_2_2():
#   - Display lesson title and objective markdown
#   - Load lesson_data via load_lesson_output()
#
#   SECTION 1: Interactive Token Analyzer
#   - Add st.subheader() for "Token Analysis Tool"
#   - Create two-column row for controls:
#     COL 1: model selector (dropdown) with options:
#       "gpt-3.5-turbo", "gpt-4", "claude-3-sonnet", "claude-3-opus"
#     COL 2: slider for max_completion (100-2000 tokens, default 500)
#   - Create radio button for input_method: "Interactive" or "Use Example"
#   - If "Interactive": text area for user prompt
#   - If "Use Example": hardcoded prompt (disabled text area)
#   - Create button row (3 columns: btn1, btn2, spacer):
#     Use st.columns([1, 1, 2]) so buttons don't shrink analysis
#
#     BUTTON 1: "🔍 Analyze Prompt" (Theory-only, full-width results)
#     - Call analyze_prompt()
#     - Display results in FULL-WIDTH metrics (4 columns)
#     - Show context fit status (✅ Fits or ❌ Exceeds)
#     - Show cost analysis in 3-column metrics
#     - Append to lesson_data["lesson_2_2"]["explorations"]
#     - Save via save_lesson_output()
#     - Show success message
#
#     BUTTON 2: "⚡ Generate & Analyze (Live API)" (Practical, new section)
#     - Check if OPENROUTER_API_KEY is set (show error if missing)
#     - Call get_client("openrouter")
#     - Call call_llm() with model, user_prompt, max_completion
#     - NEW SECTION: Add st.markdown("---") to separate from above
#     - Add st.markdown("## 🎯 Live API Generation Results")
#     - Display response in scrollable container with border
#     - Show ACTUAL token usage from API (4-column metrics):
#       - Input tokens (response["usage"]["prompt_tokens"])
#       - Output tokens (response["usage"]["completion_tokens"])
#       - Total tokens (response["usage"]["total_tokens"])
#       - Model name
#     - Calculate ACTUAL cost from real tokens (3-column metrics)
#     - Create comparison table: Estimated vs Actual
#       Columns: Metric, Estimated, Actual
#       Rows: Prompt Tokens, Completion Tokens, Total Tokens, Total Cost
#     - Save full analysis (including response + actual usage) to lesson_data
#     - Handle errors: st.error() + st.info() with helpful tip about model availability
#
#   SECTION 2: Context Window Comparison
#   - Add st.subheader() for "Context Window Comparison"
#   - Display a table/dataframe of CONTEXT_WINDOWS from shared.tokens
#   - Add caption explaining trade-offs
#
#   SECTION 3: Token Budget Scenarios
#   - Add st.subheader() for "Token Budget Scenarios"
#   - Create selectbox with options:
#     "Short Q&A (100-word limit)"
#     "Medium Article (500-word limit)"
#     "Long Document (2000-word limit)"
#   - Map scenario to word count
#   - Calculate estimated tokens (~0.75 per word)
#   - Show remaining budget for gpt-3.5-turbo (4096 - used)
#
#   SECTION 4: Lesson Summary & Key Takeaways
#   - Add st.subheader() for "Key Takeaways"
#   - Display markdown with ✅ bullet points:
#     - Token Management
#     - Context Windows
#     - Cost Optimization
#     - Prompt Design
#
#   SECTION 5: Data Persistence
#   - Add st.subheader() for "Data Persistence"
#   - Show count of saved explorations
#   - Add caption: "Output saved to datasets/lesson-02-output.json for Lesson 2.3+"
#   - Button to view saved data as JSON

# ============================================================================
# PHASE 5: Register Lesson & Entry Point
# ============================================================================
# TODO: Call register_lesson():
#   - Register this lesson with name: "Lesson 2.2: Tokens & Context"
#   - Pass render_lesson_2_2 as the function
#
# TODO: Add if __name__ == "__main__":
#   - Call render_lesson_2_2() to run as standalone
#   - OR call render_dashboard() from shared.streamlit_app to run full dashboard

# ============================================================================
# EXPECTED OUTPUT (in datasets/lesson-02-output.json):
# ============================================================================
# {
#   "lesson_2_2": {
#     "explorations": [
#       {
#         "prompt": "Explain quantum computing...",
#         "model": "mistralai/mistral-7b-instruct",
#         "prompt_tokens": 8,
#         "estimated_completion_tokens": 500,
#         "context_analysis": {
#           "fits": true,
#           "window_size": 8192,
#           "used": 8,
#           "estimated_total": 508,
#           "remaining": 8184,
#           "warning": null
#         },
#         "estimated_cost": {
#           "input_cost": 0.000001,
#           "output_cost": 0.00021,
#           "total_cost": 0.000211
#         },
#         "timestamp": "2024-06-22T12:30:45.123456"
#       },
#       {
#         "prompt": "Explain quantum computing...",
#         "model": "mistralai/mistral-7b-instruct",
#         "prompt_tokens": 8,
#         "estimated_completion_tokens": 500,
#         "context_analysis": {...},
#         "estimated_cost": {...},
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
