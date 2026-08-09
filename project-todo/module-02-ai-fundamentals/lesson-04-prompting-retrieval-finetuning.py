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
- Implement each STAGE to build a comparison tool across three approaches
- Build your own interface: Streamlit UI, CLI, or Python script
- Load sample policies or allow custom input
- Compare cost, complexity, latency, and quality across approaches
- Save results to datasets/lesson-04-output.json
- Reference the completed version for inspiration, not step-by-step replication
"""

# ============================================================================
# STAGE 1: Setup & Context Loading
# ============================================================================
# Build infrastructure and load context from previous lessons.
# Tasks: define sample policies, load Lesson 2.2 output for cost reference,
#        set up file I/O functions.
# Available shared utilities:
#   - shared.api_client: get_client(provider="openrouter")
#   - shared.tokens: estimate_tokens(), calculate_cost()
#   - Standard library: json, pathlib.Path, datetime

# TODO: Add your Stage 1 implementation here


# ============================================================================
# STAGE 2: Prompt Engineering Approach
# ============================================================================
# Implement prompt engineering: optimize the prompt without external documents.
# Logic: test multiple prompt variations (basic, detailed, chain-of-thought)
#        and compare results and costs.
# Available shared utilities:
#   - shared.api_client: call_llm(client, model, messages, temperature, max_tokens)
#   - shared.tokens: estimate_tokens(), calculate_cost()
# Task: return structured results with response, tokens, cost, and variant quality.

# TODO: Add your Stage 2 implementation here


# ============================================================================
# STAGE 3: Retrieval-Augmented Generation (RAG)
# ============================================================================
# Implement RAG: inject relevant documents into the prompt context.
# Logic: retrieve matching policies, augment prompt with retrieved text,
#        send augmented prompt to LLM.
# Available shared utilities:
#   - shared.api_client: call_llm()
#   - shared.tokens: estimate_tokens(), calculate_cost()
# Task: return results with retrieved docs, response, and cost comparison vs prompt engineering.

# TODO: Add your Stage 3 implementation here


# ============================================================================
# STAGE 4: Fine-Tuning Analysis
# ============================================================================
# Analyze fine-tuning as an alternative (do NOT actually fine-tune).
# Logic: estimate training cost, inference cost, and infrastructure overhead.
#        Compare tradeoffs with prompt engineering and RAG.
# Available shared utilities:
#   - shared.tokens: estimate_tokens(), calculate_cost()
# Task: return theoretical cost/benefit analysis with pros/cons.

# TODO: Add your Stage 4 implementation here


# ============================================================================
# STAGE 5: Comparison & Recommendations
# ============================================================================
# Compare all three approaches side-by-side.
# Display: cost, complexity, latency, maintainability, quality.
# Goal: help learners understand when to use each approach.
# Persistence: save comparison results to datasets/lesson-04-output.json.

# TODO: Add your Stage 5 implementation here
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
