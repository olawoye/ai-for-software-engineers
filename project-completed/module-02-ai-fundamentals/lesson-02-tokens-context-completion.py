"""
Lesson 2.2: Tokens, Context & Completion

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
"""

import os
import json
import streamlit as st
from datetime import datetime
from pathlib import Path

# Import shared utilities
from shared.api_client import get_client, call_llm
from shared.tokens import (
    estimate_tokens,
    count_message_tokens,
    get_context_window,
    calculate_cost,
    check_context_fit,
)
from shared.streamlit_app import register_lesson

# ============================================================================
# PHASE 1: Setup & Configuration
# ============================================================================

def setup_output_dir():
    """Ensure output directory exists."""
    output_dir = Path("datasets")
    output_dir.mkdir(exist_ok=True)
    return output_dir

def load_lesson_output():
    """Load previous lesson output if it exists."""
    output_path = Path("datasets/lesson-02-output.json")
    if output_path.exists():
        with open(output_path, "r") as f:
            return json.load(f)
    return {"lesson_2_2": {"explorations": []}}

def save_lesson_output(data):
    """Persist lesson output for downstream lessons."""
    output_dir = setup_output_dir()
    output_path = output_dir / "lesson-02-output.json"
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

# ============================================================================
# PHASE 2: Token Analysis Engine
# ============================================================================

def analyze_prompt(user_prompt: str, model: str, max_completion: int = 500):
    """
    Analyze a prompt for tokens, context fit, and estimated cost.

    Args:
        user_prompt: User's input text
        model: Model name
        max_completion: Expected completion length

    Returns:
        Dict with analysis results
    """
    prompt_tokens = estimate_tokens(user_prompt)
    context_fit = check_context_fit(model, prompt_tokens, max_completion)
    cost = calculate_cost(model, prompt_tokens, max_completion)

    return {
        "prompt": user_prompt,
        "model": model,
        "prompt_tokens": prompt_tokens,
        "estimated_completion_tokens": max_completion,
        "context_analysis": context_fit,
        "estimated_cost": cost,
        "timestamp": datetime.now().isoformat(),
    }

# ============================================================================
# PHASE 3: Interactive Streamlit Dashboard
# ============================================================================

def render_lesson_2_2():
    """Main Streamlit interface for Lesson 2.2."""
    st.markdown("## Lesson 2.2: Tokens, Context & Completion")
    st.markdown(
        """
    Learn how LLMs tokenize text, calculate costs, and handle context limits.
    This lesson teaches token budgeting for cost-effective and reliable AI applications.
    """
    )

    # Load previous explorations
    lesson_data = load_lesson_output()

    # ========================================================================
    # SECTION 1: Interactive Token Analyzer
    # ========================================================================
    st.subheader("1️⃣ Token Analysis Tool")

    col1, col2 = st.columns(2)
    with col1:
        model = st.selectbox(
            "Select Model",
            [
                "gpt-3.5-turbo",
                "gpt-4",
                "claude-3-sonnet",
                "claude-3-opus",
            ],
            help="All models available on OpenRouter. Swap with Anthropic/OpenAI models if you have direct API keys.",
        )

    with col2:
        max_completion = st.slider(
            "Expected Completion Length (tokens)",
            min_value=100,
            max_value=2000,
            value=500,
            step=100,
        )

    # Input: User prompt or fallback to hardcoded example
    input_method = st.radio("Input method:", ["Interactive", "Use Example"])

    if input_method == "Interactive":
        user_prompt = st.text_area(
            "Enter your prompt:",
            value="Explain quantum computing in simple terms.",
            height=100,
        )
    else:
        hardcoded_example = """You are an AI assistant for a software engineering course.
        A student asks: "How should I design a token-efficient prompt for an LLM?"
        Provide a detailed response with best practices."""
        user_prompt = st.text_area(
            "Example prompt:",
            value=hardcoded_example,
            height=100,
            disabled=True,
        )

    # Button row
    col_btn1, col_btn2, col_spacer = st.columns([1, 1, 2])
    with col_btn1:
        btn_analyze = st.button("🔍 Analyze Prompt", use_container_width=True)
    with col_btn2:
        btn_generate = st.button("⚡ Generate & Analyze (Live API)", use_container_width=True)

    # ========================================================================
    # BUTTON 1: Analyze Prompt (Theory Only)
    # ========================================================================
    if btn_analyze:
        analysis = analyze_prompt(user_prompt, model, max_completion)

        # Display results - FULL WIDTH
        st.markdown("### Analysis Results")

        col1a, col2a, col3a, col4a = st.columns(4)
        with col1a:
            st.metric("Prompt Tokens", analysis["prompt_tokens"])
        with col2a:
            st.metric("Est. Completion", analysis["estimated_completion_tokens"])
        with col3a:
            st.metric("Total Needed",
                     analysis["prompt_tokens"] + analysis["estimated_completion_tokens"])
        with col4a:
            window = analysis["context_analysis"]["window_size"]
            st.metric("Context Window", f"{window:,}")

        # Context fit status
        fits = analysis["context_analysis"]["fits"]
        status = "✅ Fits" if fits else "❌ Exceeds"
        st.info(f"**Status**: {status} | Remaining: {analysis['context_analysis']['remaining']:,} tokens")

        if analysis["context_analysis"]["warning"]:
            st.warning(analysis["context_analysis"]["warning"])

        # Cost analysis
        st.markdown("### Cost Analysis (Estimated)")
        cost = analysis["estimated_cost"]
        col1a, col2a, col3a = st.columns(3)
        with col1a:
            st.metric("Input Cost", f"${cost['input_cost']:.6f}")
        with col2a:
            st.metric("Output Cost", f"${cost['output_cost']:.6f}")
        with col3a:
            st.metric("Total Cost", f"${cost['total_cost']:.6f}")

        # Save to explorations
        lesson_data["lesson_2_2"]["explorations"].append(analysis)
        save_lesson_output(lesson_data)
        st.success("✅ Analysis saved to lesson-02-output.json")

    # ========================================================================
    # BUTTON 2: Generate & Analyze (Live API Call)
    # ========================================================================
    if btn_generate:
        if not os.getenv("OPENROUTER_API_KEY"):
            st.error("❌ OPENROUTER_API_KEY not set. Set via: export OPENROUTER_API_KEY='your-key'")
        else:
            try:
                with st.spinner("🤖 Calling LLM API..."):
                    client = get_client("openrouter")
                    response = call_llm(
                        client,
                        model,
                        [{"role": "user", "content": user_prompt}],
                        max_tokens=max_completion
                    )

                # New full-width section for live API results
                st.markdown("---")
                st.markdown("## 🎯 Live API Generation Results")

                # Display actual response
                st.markdown("### LLM Response")
                with st.container(border=True):
                    st.markdown(response["content"])

                # Display actual token usage
                st.markdown("### 📊 Actual Token Usage (From API)")
                col1a, col2a, col3a, col4a = st.columns(4)
                with col1a:
                    st.metric("Input Tokens", response["usage"]["prompt_tokens"])
                with col2a:
                    st.metric("Output Tokens", response["usage"]["completion_tokens"])
                with col3a:
                    st.metric("Total Tokens", response["usage"]["total_tokens"])
                with col4a:
                    st.metric("Model", response["model"])

                # Calculate actual cost
                actual_cost = calculate_cost(
                    model,
                    response["usage"]["prompt_tokens"],
                    response["usage"]["completion_tokens"]
                )

                st.markdown("### 💰 Actual Cost Analysis")
                col1a, col2a, col3a = st.columns(3)
                with col1a:
                    st.metric("Input Cost", f"${actual_cost['input_cost']:.6f}")
                with col2a:
                    st.metric("Output Cost", f"${actual_cost['output_cost']:.6f}")
                with col3a:
                    st.metric("Total Cost", f"${actual_cost['total_cost']:.6f}")

                # Compare estimate vs actual
                st.markdown("### 🔄 Estimate vs Actual")
                estimated = analyze_prompt(user_prompt, model, max_completion)
                comparison = {
                    "Metric": [
                        "Prompt Tokens",
                        "Completion Tokens",
                        "Total Tokens",
                        "Total Cost"
                    ],
                    "Estimated": [
                        estimated["prompt_tokens"],
                        estimated["estimated_completion_tokens"],
                        estimated["prompt_tokens"] + estimated["estimated_completion_tokens"],
                        f"${estimated['estimated_cost']['total_cost']:.6f}"
                    ],
                    "Actual": [
                        response["usage"]["prompt_tokens"],
                        response["usage"]["completion_tokens"],
                        response["usage"]["total_tokens"],
                        f"${actual_cost['total_cost']:.6f}"
                    ]
                }
                st.dataframe(comparison, use_container_width=True)

                # Save to explorations
                full_analysis = {
                    **estimated,
                    "actual_response": response["content"],
                    "actual_usage": response["usage"],
                    "actual_cost": actual_cost,
                }
                lesson_data["lesson_2_2"]["explorations"].append(full_analysis)
                save_lesson_output(lesson_data)
                st.success("✅ Full analysis saved to lesson-02-output.json")

            except Exception as e:
                st.error(f"❌ API Error: {str(e)}")
                st.info("💡 Tip: Not all models are available on all OpenRouter endpoints. Try 'gpt-3.5-turbo' or 'claude-3-sonnet' from the dropdown.")

    # ========================================================================
    # SECTION 2: Context Window Comparison
    # ========================================================================
    st.subheader("2️⃣ Context Window Comparison")

    from shared.tokens import CONTEXT_WINDOWS
    context_df = {
        "Model": list(CONTEXT_WINDOWS.keys()),
        "Context Window": list(CONTEXT_WINDOWS.values()),
    }
    st.dataframe(context_df, use_container_width=True)

    st.caption(
        "Models with larger context windows can handle longer prompts but may cost more."
    )

    # ========================================================================
    # SECTION 3: Token Budget Scenarios
    # ========================================================================
    st.subheader("3️⃣ Token Budget Scenarios")

    scenario = st.selectbox(
        "Scenario:",
        [
            "Short Q&A (100-word limit)",
            "Medium Article (500-word limit)",
            "Long Document (2000-word limit)",
        ],
    )

    scenario_words = {
        "Short Q&A (100-word limit)": 100,
        "Medium Article (500-word limit)": 500,
        "Long Document (2000-word limit)": 2000,
    }

    word_limit = scenario_words[scenario]
    estimated_tokens = int(word_limit * 0.75)

    st.write(f"**Word Limit**: {word_limit}")
    st.write(f"**Estimated Tokens**: {estimated_tokens}")
    st.write(
        f"**Remaining Budget** (gpt-3.5-turbo): {4096 - estimated_tokens:,} tokens"
    )

    # ========================================================================
    # SECTION 4: Lesson Summary & Takeaways
    # ========================================================================
    st.subheader("4️⃣ Key Takeaways")
    st.markdown(
        """
    ✅ **Token Management**:
    - Text is broken into tokens (~0.75 tokens per word on average)
    - Tokens affect both cost and context limits
    - Budget tokens early to avoid expensive failures

    ✅ **Context Windows**:
    - Every model has a maximum context size (e.g., 4K, 8K, 32K, 100K+)
    - Exceeding context → errors or truncated responses
    - Design prompts to fit comfortably within limits

    ✅ **Cost Optimization**:
    - Input tokens and completion tokens cost differently
    - Longer prompts = higher input costs
    - Shorter, focused prompts = lower cost and faster responses

    ✅ **Prompt Design**:
    - Be concise but clear
    - Avoid unnecessary examples or explanations
    - Test token usage before deploying
    """
    )

    # ========================================================================
    # SECTION 5: Persistence & Next Steps
    # ========================================================================
    st.subheader("5️⃣ Data Persistence")

    st.write(f"**Explorations saved**: {len(lesson_data['lesson_2_2']['explorations'])}")
    st.caption("Output is saved to `datasets/lesson-02-output.json` for Lesson 2.3+")

    if st.button("📥 View Saved Data"):
        st.json(lesson_data)

# ============================================================================
# PHASE 4: Register Lesson & Entry Point
# ============================================================================

# Register this lesson for the dashboard
register_lesson("Lesson 2.2: Tokens & Context", render_lesson_2_2)

if __name__ == "__main__":
    render_lesson_2_2()
