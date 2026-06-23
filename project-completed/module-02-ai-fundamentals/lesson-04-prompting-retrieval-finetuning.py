"""
Lesson 2.4: Prompting, Retrieval & Fine-Tuning

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
- Build intuition about approach selection
"""

import os
import json
import streamlit as st
from datetime import datetime
from pathlib import Path
from typing import List, Dict

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
from shared.data_loader import load_sample_corpus

# ============================================================================
# PHASE 1: Setup & Configuration
# ============================================================================

# Sample policies for demonstration
SAMPLE_POLICIES = {
    "Remote Work Policy": "...",
    "Vacation & PTO": "...",
    "Code of Conduct": "..."
}

def setup_output_dir():
    """Ensure output directory exists."""
    output_dir = Path("../datasets")
    output_dir.mkdir(exist_ok=True)
    return output_dir

def load_lesson_2_2_data():
    """Load results from Lesson 2.2 for context."""
    try:
        output_path = Path("../datasets/lesson-02-output.json")
        if output_path.exists():
            with open(output_path, "r") as f:
                data = json.load(f)
                # Filter out old Mistral entries, keep valid models only
                valid_models = {"gpt-3.5-turbo", "gpt-4", "claude-3-sonnet", "claude-3-opus"}
                explorations = data.get("lesson_2_2", {}).get("explorations", [])
                filtered = [e for e in explorations if e.get("model") in valid_models]
                return filtered[-1] if filtered else None
    except Exception as e:
        st.warning(f"Could not load Lesson 2.2 data: {e}")
    return None

def save_lesson_output(data):
    """Persist lesson output for downstream lessons."""
    output_dir = setup_output_dir()
    output_path = output_dir / "lesson-04-output.json"
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

def load_lesson_output():
    """Load previous lesson output if it exists."""
    output_path = Path("../datasets/lesson-04-output.json")
    if output_path.exists():
        with open(output_path, "r") as f:
            return json.load(f)
    return {"lesson_2_4": {"comparisons": [], "recommendations": []}}

# ============================================================================
# PHASE 2: Approach Implementations
# ============================================================================

def approach_prompt_engineering(question: str, model: str, max_tokens: int = 500) -> Dict:
    """
    APPROACH 1: Prompt Engineering
    Optimize the prompt itself without external knowledge.
    """
    if not os.getenv("OPENROUTER_API_KEY"):
        return {"error": "API key not set"}

    client = get_client("openrouter")

    # Three prompt variations to demonstrate differences
    prompts = {
        "basic": question,
        "detailed": f"""You are an expert HR consultant.
Answer the following question clearly and accurately.
Question: {question}""",
        "chain_of_thought": f"""You are an expert HR consultant.
Answer the following question step by step.
Think about the policy requirements, then provide a clear answer.
Question: {question}"""
    }

    results = {}
    for name, prompt_text in prompts.items():
        response = call_llm(
            client,
            model,
            [{"role": "user", "content": prompt_text}],
            max_tokens=max_tokens
        )
        cost = calculate_cost(model, response["usage"]["prompt_tokens"], response["usage"]["completion_tokens"])

        results[name] = {
            "response": response["content"],
            "tokens": response["usage"]["total_tokens"],
            "cost": cost["total_cost"],
            "prompt_variation": name
        }

    return {
        "approach": "Prompt Engineering",
        "results": results,
        "best_variant": min(results.items(), key=lambda x: x[1]["cost"])[0],
        "total_cost": sum(r["cost"] for r in results.values()),
        "complexity": "Low",
        "maintainability": "High",
        "latency": "Fast"
    }

def approach_rag(question: str, policies: Dict[str, str], model: str, max_tokens: int = 500) -> Dict:
    """
    APPROACH 2: Retrieval-Augmented Generation (RAG)
    Retrieve relevant policies, inject into context, then generate.
    """
    if not os.getenv("OPENROUTER_API_KEY"):
        return {"error": "API key not set"}

    client = get_client("openrouter")

    # Simple retrieval: find relevant policies by keyword matching
    question_lower = question.lower()
    relevant_policies = []

    for policy_name, policy_text in policies.items():
        if any(keyword in question_lower for keyword in policy_name.lower().split()):
            relevant_policies.append((policy_name, policy_text))

    if not relevant_policies:
        relevant_policies = list(policies.items())[:1]  # Fallback to first policy

    # Build augmented prompt
    context = "\n\n---\n\n".join([f"Policy: {name}\n{text}" for name, text in relevant_policies])
    augmented_prompt = f"""You are an HR assistant. Answer the following question using the provided policies.

POLICIES:
{context}

QUESTION: {question}

ANSWER:"""

    response = call_llm(
        client,
        model,
        [{"role": "user", "content": augmented_prompt}],
        max_tokens=max_tokens
    )
    cost = calculate_cost(model, response["usage"]["prompt_tokens"], response["usage"]["completion_tokens"])

    return {
        "approach": "RAG",
        "response": response["content"],
        "retrieved_policies": [name for name, _ in relevant_policies],
        "tokens": response["usage"]["total_tokens"],
        "cost": cost["total_cost"],
        "complexity": "Medium",
        "maintainability": "Medium",
        "latency": "Medium",
        "retrieval_quality": f"Retrieved {len(relevant_policies)} policies"
    }

def approach_finetuning_simulation(question: str, policies: Dict[str, str], model: str) -> Dict:
    """
    APPROACH 3: Fine-tuning (Theoretical Comparison)
    Show what fine-tuning would look like without actually fine-tuning.
    """
    # Calculate theoretical costs
    total_policy_tokens = sum(estimate_tokens(p) for p in policies.values())
    finetuning_cost = (total_policy_tokens / 1_000_000) * 8.0  # Rough estimate: $8 per 1M tokens

    return {
        "approach": "Fine-tuning",
        "response": "[Would generate custom model trained on your policies - not implemented in demo]",
        "complexity": "High",
        "maintainability": "Low",
        "latency": "Fast (once fine-tuned)",
        "setup_cost": f"${finetuning_cost:.2f}",
        "cost_per_inference": "$0.001",
        "notes": "Fine-tuning requires training time (hours to days) and minimum investment (~$10-50). Best for high-volume use cases.",
        "pros": ["Lowest inference cost", "Fast responses", "Custom model"],
        "cons": ["High setup cost", "Takes time to train", "Less flexible", "Requires training data"]
    }

# ============================================================================
# PHASE 3: Streamlit Dashboard
# ============================================================================

def render_lesson_2_4():
    """Main Streamlit interface for Lesson 2.4."""
    st.markdown("## Lesson 2.4: Prompting, Retrieval & Fine-Tuning")
    st.markdown(
        """
    Compare three approaches to improve AI outputs. Understand the tradeoffs
    in cost, complexity, maintainability, and performance for your use case.
    """
    )

    # Load previous data
    lesson_data = load_lesson_output()
    lesson_2_2_data = load_lesson_2_2_data()

    # ========================================================================
    # SECTION 1: Input Setup
    # ========================================================================
    st.subheader("1️⃣ Setup: Policy Knowledge Base")

    col1, col2 = st.columns(2)
    with col1:
        policy_source = st.radio("Policy source:", ["Use Sample Policies", "Paste Your Own"])

    if policy_source == "Use Sample Policies":
        # Load from shared corpus
        policies, data_source = load_sample_corpus()
        if not policies:
            st.error("Could not load sample policies. Using empty corpus.")
            policies = {}
        st.success(f"✅ Loaded {len(policies)} sample policies")
        st.caption(f"📁 Sample data loaded from: `{data_source}`")
    else:
        user_policy = st.text_area(
            "Paste your policy document(s):",
            value="Paste your company policy here...",
            height=150
        )
        policies = {"Custom Policy": user_policy}
        st.success("✅ Using your custom policy")

    # Model and parameters (can vary from 2.2)
    col1, col2, col3 = st.columns(3)
    with col1:
        model = st.selectbox(
            "Model for testing:",
            ["gpt-3.5-turbo", "gpt-4", "claude-3-sonnet", "claude-3-opus"],
            help="Same models from Lesson 2.2"
        )
    with col2:
        max_tokens = st.slider("Max tokens:", 100, 500, 300, 50)
    with col3:
        if lesson_2_2_data:
            st.info(f"📊 Lesson 2.2: {lesson_2_2_data.get('model')}")

    # User question
    user_question = st.text_input(
        "Ask an HR policy question:",
        value="What is the remote work policy?",
        placeholder="E.g., How much vacation do I get?"
    )

    # ========================================================================
    # SECTION 2: Run Comparison
    # ========================================================================
    st.subheader("2️⃣ Compare Approaches")

    if st.button("🚀 Run All Three Approaches", use_container_width=True):
        if not os.getenv("OPENROUTER_API_KEY"):
            st.error("❌ OPENROUTER_API_KEY not set")
        else:
            with st.spinner("Running comparison across 3 approaches..."):
                results = {
                    "question": user_question,
                    "model": model,
                    "max_tokens": max_tokens,
                    "timestamp": datetime.now().isoformat(),
                    "approaches": {}
                }

                # Run Approach 1: Prompt Engineering
                with st.status("Running Prompt Engineering...", expanded=False):
                    pe_result = approach_prompt_engineering(user_question, model, max_tokens)
                    results["approaches"]["prompt_engineering"] = pe_result

                # Run Approach 2: RAG
                with st.status("Running RAG...", expanded=False):
                    rag_result = approach_rag(user_question, policies, model, max_tokens)
                    results["approaches"]["rag"] = rag_result

                # Run Approach 3: Fine-tuning
                with st.status("Fine-tuning Analysis...", expanded=False):
                    ft_result = approach_finetuning_simulation(user_question, policies, model)
                    results["approaches"]["finetuning"] = ft_result

                # Display results
                st.markdown("---")
                st.markdown("## 📊 Comparison Results")

                # Tabs for each approach
                tab_pe, tab_rag, tab_ft, tab_comparison = st.tabs(
                    ["Prompt Engineering", "RAG", "Fine-tuning", "Decision Matrix"]
                )

                with tab_pe:
                    st.markdown("### Prompt Engineering Results")
                    pe = results["approaches"]["prompt_engineering"]
                    for variant, data in pe["results"].items():
                        st.markdown(f"**Variant: {variant}**")
                        st.write(data["response"])
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Tokens", data["tokens"])
                        with col2:
                            st.metric("Cost", f"${data['cost']:.6f}")
                        with col3:
                            st.metric("Variant", variant)
                        st.divider()

                with tab_rag:
                    st.markdown("### RAG Results")
                    rag = results["approaches"]["rag"]
                    st.write(rag["response"])
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Tokens", rag["tokens"])
                    with col2:
                        st.metric("Cost", f"${rag['cost']:.6f}")
                    with col3:
                        st.metric("Retrieved", len(rag["retrieved_policies"]))
                    with col4:
                        st.metric("Quality", rag["retrieval_quality"])

                with tab_ft:
                    st.markdown("### Fine-tuning Analysis")
                    ft = results["approaches"]["finetuning"]
                    st.info(ft["response"])
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Pros:**")
                        for pro in ft["pros"]:
                            st.write(f"✅ {pro}")
                    with col2:
                        st.markdown("**Cons:**")
                        for con in ft["cons"]:
                            st.write(f"❌ {con}")

                with tab_comparison:
                    st.markdown("### Decision Matrix")
                    comparison_data = {
                        "Approach": ["Prompt Eng.", "RAG", "Fine-tuning"],
                        "Setup Cost": ["$0", "$0", ft["setup_cost"]],
                        "Complexity": [
                            pe["complexity"],
                            rag["complexity"],
                            ft["complexity"]
                        ],
                        "Maintainability": [
                            pe["maintainability"],
                            rag["maintainability"],
                            ft["maintainability"]
                        ],
                        "Latency": [
                            pe["latency"],
                            rag["latency"],
                            ft["latency"]
                        ],
                        "Best For": [
                            "Quick answers, low cost",
                            "Knowledge base updates",
                            "High volume, custom model"
                        ]
                    }
                    st.dataframe(comparison_data, use_container_width=True)

                    st.markdown("### 💡 Recommendation Engine")
                    st.markdown("""
                    - **Choose Prompt Engineering** if: Low budget, simple questions, fast iteration
                    - **Choose RAG** if: Frequently updated knowledge, need context accuracy, moderate volume
                    - **Choose Fine-tuning** if: High volume, custom model acceptable, trained on your data
                    """)

                # Save results
                lesson_data["lesson_2_4"]["comparisons"].append(results)
                save_lesson_output(lesson_data)
                st.success(f"✅ Comparison saved to lesson-04-output.json")

    # ========================================================================
    # SECTION 3: Results History
    # ========================================================================
    st.subheader("3️⃣ Previous Comparisons")
    if lesson_data["lesson_2_4"]["comparisons"]:
        st.info(f"📋 {len(lesson_data['lesson_2_4']['comparisons'])} comparison(s) saved")
        if st.button("📥 View All Results"):
            st.json(lesson_data["lesson_2_4"]["comparisons"])
    else:
        st.caption("No comparisons yet. Run the comparison above to get started.")

    # ========================================================================
    # SECTION 4: Key Takeaways
    # ========================================================================
    st.subheader("4️⃣ Key Takeaways")
    st.markdown("""
    ✅ **Prompt Engineering**:
    - Fastest to implement
    - No external dependencies
    - Limited by base model knowledge
    - Cost scales with question volume

    ✅ **Retrieval-Augmented Generation**:
    - Grounds answers in your data
    - Handles frequent updates easily
    - Requires retrieval infrastructure
    - Better accuracy for domain knowledge

    ✅ **Fine-tuning**:
    - Customizes model for your use case
    - High setup cost, low inference cost
    - Best for high-volume applications
    - Requires training data and time
    """)

# ============================================================================
# PHASE 4: Register & Entry Point
# ============================================================================

register_lesson("Lesson 2.4: Prompting, RAG & Fine-tuning", render_lesson_2_4)

if __name__ == "__main__":
    render_lesson_2_4()
