"""
Lesson 2.4: Prompting, Retrieval & Fine-Tuning (TODO - Scaffold)

OBJECTIVE: Compare three primary methods to improve AI outputs:
1. Prompt Engineering - optimize prompts without external knowledge
2. Retrieval-Augmented Generation (RAG) - inject relevant documents into context
3. Fine-tuning - train a custom model on your data

BUSINESS SCENARIO: A company needs to build an internal policy Q&A assistant.
They must decide: prompt engineering, RAG, or fine-tuning? This lesson helps
evaluate tradeoffs in cost, complexity, maintainability, and performance.

By the end of this lesson, students will:
- Understand when to use each approach
- Compare results and costs across methods
- Make data-driven decisions for their specific use case

INSTRUCTIONS:
- Implement each PHASE in order
- Use the completed version as reference
- Load Lesson 2.2 output for context
- Allow sample policies + custom textarea input
- Compare all three approaches on same question
- Save results to datasets/lesson-04-output.json
"""

# ============================================================================
# PHASE 1: Imports & Setup
# ============================================================================
# TODO: Import required libraries:
#   - json, streamlit, datetime, Path, List, Dict
#
# TODO: Import shared utilities:
#   - get_client, call_llm from shared.api_client
#   - estimate_tokens, calculate_cost from shared.tokens
#   - register_lesson from shared.streamlit_app
#
# TODO: Define SAMPLE_POLICIES dict with 3 policies (e.g., Remote Work, PTO, Code of Conduct)
#   - Use multi-line strings (""") for policy text
#   - Keep each policy concise but realistic

# ============================================================================
# PHASE 2: File I/O Functions
# ============================================================================
# TODO: Implement setup_output_dir():
#   - Create ../datasets/ directory if not exists
#   - Return directory path
#
# TODO: Implement load_lesson_2_2_data():
#   - Read ../datasets/lesson-02-output.json
#   - Filter to valid models only: gpt-3.5-turbo, gpt-4, claude-3-sonnet, claude-3-opus
#   - Ignore old Mistral entries
#   - Return latest valid exploration or None
#
# TODO: Implement save_lesson_output(data):
#   - Save data dict to ../datasets/lesson-04-output.json
#   - Use json.dump with indent=2
#
# TODO: Implement load_lesson_output():
#   - Load lesson-04-output.json if exists
#   - Return dict with structure: {"lesson_2_4": {"comparisons": [], "recommendations": []}}

# ============================================================================
# PHASE 3: Approach 1 - Prompt Engineering
# ============================================================================
# TODO: Implement approach_prompt_engineering(question, model, max_tokens=500):
#   - Check if OPENROUTER_API_KEY is set (return error dict if not)
#   - Initialize OpenRouter client via get_client("openrouter")
#   - Create 3 prompt variations:
#     - "basic": just the question
#     - "detailed": add "You are an expert HR consultant" + clear instructions
#     - "chain_of_thought": add "Think step by step" + structure
#   - Call call_llm() for EACH variation
#   - For each: extract response, tokens, calculate cost via calculate_cost()
#   - Return dict with:
#     {
#       "approach": "Prompt Engineering",
#       "results": {variant_name: {response, tokens, cost, prompt_variation}},
#       "best_variant": which variant had lowest cost,
#       "total_cost": sum of all variants,
#       "complexity": "Low",
#       "maintainability": "High",
#       "latency": "Fast"
#     }

# ============================================================================
# PHASE 4: Approach 2 - Retrieval-Augmented Generation (RAG)
# ============================================================================
# TODO: Implement approach_rag(question, policies, model, max_tokens=500):
#   - Check if OPENROUTER_API_KEY is set
#   - Simple keyword-based retrieval: find policies matching question keywords
#   - If none match, use first policy as fallback
#   - Build augmented prompt with:
#     - "You are an HR assistant"
#     - POLICIES section (concatenate relevant policy_text with separators)
#     - QUESTION section
#   - Call call_llm() with augmented prompt
#   - Calculate cost from response
#   - Return dict with:
#     {
#       "approach": "RAG",
#       "response": generated response,
#       "retrieved_policies": [list of policy names used],
#       "tokens": total_tokens,
#       "cost": total_cost,
#       "complexity": "Medium",
#       "maintainability": "Medium",
#       "latency": "Medium",
#       "retrieval_quality": f"Retrieved {n} policies"
#     }

# ============================================================================
# PHASE 5: Approach 3 - Fine-tuning Simulation
# ============================================================================
# TODO: Implement approach_finetuning_simulation(question, policies, model):
#   - Calculate total tokens in all policies via estimate_tokens()
#   - Estimate fine-tuning cost (~$8 per 1M policy tokens)
#   - DO NOT actually fine-tune (would take hours/cost $$)
#   - Return theoretical comparison dict with:
#     {
#       "approach": "Fine-tuning",
#       "response": "[Theoretical fine-tuned model response]",
#       "complexity": "High",
#       "maintainability": "Low",
#       "latency": "Fast (once trained)",
#       "setup_cost": f"${cost:.2f}",
#       "cost_per_inference": "$0.001",
#       "pros": ["Lowest inference cost", "Fast responses", "Custom model"],
#       "cons": ["High setup cost", "Takes time", "Less flexible"]
#     }

# ============================================================================
# PHASE 6: Streamlit Dashboard
# ============================================================================
# TODO: Implement render_lesson_2_4():
#   - Load previous data via load_lesson_output()
#   - Load Lesson 2.2 data via load_lesson_2_2_data()
#   - Display title and objective markdown
#
#   SECTION 1: Setup
#   - Subheader "Setup: Policy Knowledge Base"
#   - Radio button: "Use Sample Policies" or "Paste Your Own"
#   - If Sample: load SAMPLE_POLICIES, show success
#   - If Custom: text_area for pasting policies, create {"Custom Policy": text}
#   - Model selector (dropdown): gpt-3.5-turbo, gpt-4, claude-3-sonnet, claude-3-opus
#   - Slider: max_tokens (100-500, default 300)
#   - Display Lesson 2.2 model info if available
#   - Text input: user_question (default "What is the remote work policy?")
#
#   SECTION 2: Run Comparison
#   - Button: "🚀 Run All Three Approaches" (full width)
#   - When clicked:
#     - Check OPENROUTER_API_KEY
#     - Show spinner "Running comparison..."
#     - Call approach_prompt_engineering() with status
#     - Call approach_rag() with status
#     - Call approach_finetuning_simulation() with status
#     - Build results dict with timestamp, question, model, all approaches
#     - Display 4 tabs:
#       TAB 1: Prompt Engineering (show each variant + response, tokens, cost)
#       TAB 2: RAG (show response, tokens, cost, retrieved policies)
#       TAB 3: Fine-tuning (show pros/cons, setup cost, notes)
#       TAB 4: Decision Matrix (comparison table + recommendation engine)
#     - Save results to lesson_data["lesson_2_4"]["comparisons"]
#     - Save via save_lesson_output()
#     - Show success message
#
#   SECTION 3: Results History
#   - Subheader "Previous Comparisons"
#   - Show count of saved comparisons
#   - Button to view all results as JSON
#
#   SECTION 4: Key Takeaways
#   - Display markdown with ✅ bullet points for each approach:
#     - Pros/cons
#     - When to use
#     - Considerations

# ============================================================================
# PHASE 7: Register & Entry Point
# ============================================================================
# TODO: Call register_lesson():
#   - Register with name: "Lesson 2.4: Prompting, RAG & Fine-tuning"
#   - Pass render_lesson_2_4 as the function
#
# TODO: Add if __name__ == "__main__":
#   - Call render_lesson_2_4()

# ============================================================================
# EXPECTED OUTPUT (in datasets/lesson-04-output.json):
# ============================================================================
# {
#   "lesson_2_4": {
#     "comparisons": [
#       {
#         "question": "What is the remote work policy?",
#         "model": "gpt-3.5-turbo",
#         "max_tokens": 300,
#         "timestamp": "2024-06-22T14:30:00.123456",
#         "approaches": {
#           "prompt_engineering": {
#             "approach": "Prompt Engineering",
#             "results": {
#               "basic": {
#                 "response": "...",
#                 "tokens": 45,
#                 "cost": 0.000015,
#                 "prompt_variation": "basic"
#               },
#               "detailed": {...},
#               "chain_of_thought": {...}
#             },
#             "best_variant": "basic",
#             "total_cost": 0.000045,
#             "complexity": "Low",
#             "maintainability": "High",
#             "latency": "Fast"
#           },
#           "rag": {
#             "approach": "RAG",
#             "response": "...",
#             "retrieved_policies": ["Remote Work Policy"],
#             "tokens": 156,
#             "cost": 0.000078,
#             "complexity": "Medium",
#             "maintainability": "Medium",
#             "latency": "Medium"
#           },
#           "finetuning": {
#             "approach": "Fine-tuning",
#             "response": "[Theoretical...]",
#             "complexity": "High",
#             "setup_cost": "$12.50",
#             "cost_per_inference": "$0.001",
#             "pros": [...],
#             "cons": [...]
#           }
#         }
#       }
#     ]
#   }
# }

# ============================================================================
# TESTING CHECKLIST:
# ============================================================================
# ✅ Load Lesson 2.2 data correctly (filters Mistral entries)
# ✅ Sample policies load and display
# ✅ Custom policy textarea works
# ✅ Model dropdown has correct options
# ✅ Prompt engineering: 3 variants generated, costs calculated
# ✅ RAG: retrieval works, augmented prompt correct, cost calculated
# ✅ Fine-tuning: theoretical costs shown, no actual training
# ✅ All 4 tabs display correctly
# ✅ Decision matrix shows comparison
# ✅ Recommendation engine explains when to use each
# ✅ Results saved to JSON
# ✅ Previous comparisons load and display
# ✅ Run: streamlit run lesson-04-prompting-retrieval-finetuning.py
