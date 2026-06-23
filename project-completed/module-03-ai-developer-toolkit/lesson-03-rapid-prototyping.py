"""
Lesson 3.3: Rapid Prototyping with Streamlit

Learn how Streamlit dramatically reduces the effort to build AI applications.
Connect user inputs, AI services, and outputs into functioning prototypes
in minutes instead of weeks.

Run: streamlit run lesson-03-rapid-prototyping.py
Requires: export OPENROUTER_API_KEY='your-key-here'
"""

import streamlit as st
import time
from shared.llm_client import LLMClient
from shared.config import MODELS, DEFAULT_MODEL, TEMP_PRECISE, TEMP_BALANCED, TEMP_CREATIVE


# Page configuration
st.set_page_config(
    page_title="Rapid Prototyping with Streamlit",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "model" not in st.session_state:
    st.session_state.model = DEFAULT_MODEL
if "temperature" not in st.session_state:
    st.session_state.temperature = TEMP_BALANCED
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 200


# ============================================================================
# HEADER & INTRODUCTION
# ============================================================================

st.title("🚀 Rapid Prototyping with Streamlit")
st.markdown("""
This lesson shows how **Streamlit** lets you build AI applications in minutes.
Pick a use case, configure settings, and see instant results.
No HTML, CSS, or complex frameworks required—just Python!
""")

st.divider()


# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

with st.sidebar:
    st.header("⚙️ Configuration")

    # Model selector
    st.session_state.model = st.selectbox(
        "Select Model",
        options=list(MODELS.values()),
        format_func=lambda x: [k for k, v in MODELS.items() if v == x][0],
        help="Choose which LLM to use"
    )

    # Temperature slider
    st.session_state.temperature = st.slider(
        "Temperature (Creativity)",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.temperature,
        step=0.1,
        help="0.0 = precise, 1.0 = creative"
    )

    # Max tokens slider
    st.session_state.max_tokens = st.slider(
        "Max Tokens",
        min_value=50,
        max_value=500,
        value=st.session_state.max_tokens,
        step=50,
        help="Maximum response length"
    )

    st.divider()

    # Information display
    st.subheader("📊 Current Settings")
    st.metric("Model", st.session_state.model)
    st.metric("Temperature", f"{st.session_state.temperature:.1f}")
    st.metric("Max Tokens", st.session_state.max_tokens)


# ============================================================================
# MODE SELECTION
# ============================================================================

mode = st.radio(
    "Choose Application Mode:",
    ["Text Classification", "Text Summarization", "Question & Answer"],
    horizontal=True,
    help="Click to switch between different AI tasks"
)


# ============================================================================
# MODE 1: TEXT CLASSIFICATION
# ============================================================================

if mode == "Text Classification":
    st.subheader("📋 Text Classification")

    # Explanation
    with st.expander("💡 How it works", expanded=True):
        st.markdown("""
        **Classify any text** into predefined categories instantly.

        Common uses:
        - Sentiment analysis (positive/negative/neutral)
        - Topic categorization (sports, tech, politics, etc.)
        - Support ticket routing (bug, feature request, support)
        - Intent detection (book, cancel, upgrade, etc.)
        """)

    # Example buttons
    col1, col2, col3 = st.columns(3)
    example_texts = {
        "Sentiment": "This product is absolutely amazing! I love it!",
        "Support": "The app crashes every time I try to save files",
        "Topic": "Apple announced new AI features for iPhone 15"
    }

    col1.button("📝 Sentiment Example", key="btn_sentiment")
    col2.button("🎯 Support Ticket", key="btn_support")
    col3.button("📰 Tech News", key="btn_topic")

    # Initialize session state for examples
    if "classification_text" not in st.session_state:
        st.session_state.classification_text = ""

    if st.session_state.get("btn_sentiment"):
        st.session_state.classification_text = example_texts["Sentiment"]
    if st.session_state.get("btn_support"):
        st.session_state.classification_text = example_texts["Support"]
    if st.session_state.get("btn_topic"):
        st.session_state.classification_text = example_texts["Topic"]

    # Input
    text_input = st.text_area(
        "📝 Text to classify",
        value=st.session_state.classification_text,
        placeholder="Paste text here...",
        height=100,
        key="classification_input"
    )

    # Categories
    categories = st.multiselect(
        "Categories",
        options=["Positive", "Negative", "Neutral", "Bug", "Feature Request",
                 "Support", "Technology", "Politics", "Sports", "Entertainment"],
        default=["Positive", "Negative", "Neutral"],
        help="Select categories to classify into"
    )

    # Classify button
    if st.button("🔍 Classify", type="primary", use_container_width=True):
        if not text_input:
            st.warning("Please enter text to classify")
        elif not categories:
            st.warning("Please select at least one category")
        else:
            with st.spinner("Classifying..."):
                try:
                    client = LLMClient(model=st.session_state.model)
                    prompt = f"""Classify this text into ONE of these categories: {', '.join(categories)}

Text: "{text_input}"

Respond with only the category name."""

                    start = time.time()
                    response = client.complete(
                        prompt,
                        temperature=st.session_state.temperature,
                        max_tokens=st.session_state.max_tokens
                    )
                    elapsed = time.time() - start

                    # Display result
                    col1, col2 = st.columns(2)
                    with col1:
                        st.success(f"**Classification:** {response.strip()}")
                    with col2:
                        st.metric("Response Time", f"{elapsed:.2f}s")

                except Exception as e:
                    st.error(f"Error: {e}")

    # Code comparison
    with st.expander("👨‍💻 See the code"):
        st.markdown("**Traditional Python (50+ lines):**")
        st.code("""
import requests
from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/classify', methods=['POST'])
def classify():
    data = request.get_json()
    text = data.get('text')
    categories = data.get('categories', [])

    # Validate input
    if not text or not categories:
        return jsonify({'error': 'Missing data'}), 400

    # Setup API call
    headers = {'Authorization': f'Bearer {API_KEY}'}
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': f'Classify: {text}'}],
        'temperature': 0.7
    }

    # Make request
    response = requests.post('https://api.openai.com/v1/chat/completions',
                            headers=headers, json=payload)

    result = response.json()['choices'][0]['message']['content']

    return jsonify({'category': result})

if __name__ == '__main__':
    app.run(debug=True)
        """, language="python")

        st.markdown("**Streamlit (10 lines):**")
        st.code("""
import streamlit as st
from shared.llm_client import LLMClient

text = st.text_area("Text to classify")
categories = st.multiselect("Categories", [options])

if st.button("Classify"):
    client = LLMClient(model="gpt-3.5-turbo")
    response = client.complete(f"Classify: {text}")
    st.success(f"Result: {response}")
        """, language="python")


# ============================================================================
# MODE 2: TEXT SUMMARIZATION
# ============================================================================

elif mode == "Text Summarization":
    st.subheader("📝 Text Summarization")

    # Explanation
    with st.expander("💡 How it works", expanded=True):
        st.markdown("""
        **Summarize any text** into concise, actionable summaries.

        Common uses:
        - Long documents → executive summary
        - News articles → key points
        - Meeting notes → action items
        - Customer feedback → themes
        """)

    # Example buttons
    col1, col2, col3 = st.columns(3)

    example_docs = {
        "Article": """The latest breakthroughs in quantum computing are showing promising results.
        Researchers at major universities have achieved new milestones in quantum error correction,
        which has been a major obstacle in scaling quantum computers. These advances could lead to
        practical quantum computers within the next 5-10 years. Tech companies like IBM, Google, and
        Microsoft are investing billions in quantum research.""",

        "Meeting": """Team meeting on Q4 planning: Discussed roadmap for next quarter. John presented
        feature priorities. Sarah raised concerns about timeline. We agreed to extend sprint 1 by one
        week. Action items: 1) John to update requirements, 2) Sarah to assess resource availability,
        3) Follow-up meeting next Tuesday. Budget approved for additional cloud infrastructure.""",

        "Feedback": """Customer feedback from recent survey: 90% satisfaction with product quality.
        Main complaints: documentation could be clearer, onboarding takes too long, API documentation
        needs examples. Positive feedback: excellent customer support, frequent updates, responsive team.
        Recommendation: prioritize documentation improvements."""
    }

    col1.button("📰 News Article", key="btn_article")
    col2.button("📅 Meeting Notes", key="btn_meeting")
    col3.button("💬 Feedback", key="btn_feedback")

    if "summary_text" not in st.session_state:
        st.session_state.summary_text = ""

    if st.session_state.get("btn_article"):
        st.session_state.summary_text = example_docs["Article"]
    if st.session_state.get("btn_meeting"):
        st.session_state.summary_text = example_docs["Meeting"]
    if st.session_state.get("btn_feedback"):
        st.session_state.summary_text = example_docs["Feedback"]

    # Input
    doc_input = st.text_area(
        "📄 Document to summarize",
        value=st.session_state.summary_text,
        placeholder="Paste longer text here...",
        height=150,
        key="summary_input"
    )

    # Summarize button
    if st.button("✂️ Summarize", type="primary", use_container_width=True):
        if not doc_input:
            st.warning("Please enter a document to summarize")
        else:
            with st.spinner("Summarizing..."):
                try:
                    client = LLMClient(model=st.session_state.model)
                    prompt = f"""Summarize this text in 2-3 bullet points:

{doc_input}

Summary:"""

                    start = time.time()
                    response = client.complete(
                        prompt,
                        temperature=st.session_state.temperature,
                        max_tokens=st.session_state.max_tokens
                    )
                    elapsed = time.time() - start

                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.success("**Summary:**")
                        st.write(response)
                    with col2:
                        st.metric("Time", f"{elapsed:.2f}s")
                        st.metric("Tokens", st.session_state.max_tokens)

                except Exception as e:
                    st.error(f"Error: {e}")

    # Code comparison
    with st.expander("👨‍💻 See the code"):
        st.code("""
# Streamlit approach
import streamlit as st
from shared.llm_client import LLMClient

document = st.text_area("Document to summarize")

if st.button("Summarize"):
    client = LLMClient(model="gpt-3.5-turbo")
    summary = client.complete(f"Summarize: {document}")
    st.success(f"**Summary:**\\n{summary}")
        """, language="python")


# ============================================================================
# MODE 3: QUESTION & ANSWER
# ============================================================================

elif mode == "Question & Answer":
    st.subheader("❓ Question & Answer")

    # Explanation
    with st.expander("💡 How it works", expanded=True):
        st.markdown("""
        **Ask questions about a document** and get instant answers.

        Common uses:
        - Policy Q&A (employee handbook)
        - FAQ generation (product docs)
        - Document search (contracts)
        - Knowledge retrieval (research papers)
        """)

    # Example buttons
    col1, col2 = st.columns(2)

    example_docs_qa = {
        "Policy": """Our remote work policy: Employees can work from home up to 3 days per week.
        Home office stipend of $500/month is provided. Core hours are 10am-3pm in your timezone.
        All meetings should be recorded for asynchronous access. Equipment: Company provides laptop
        and monitor. Internet stipend: $50/month if working from home full-time.""",

        "FAQ": """Q: How do I reset my password? A: Visit login page, click "Forgot Password",
        enter your email. Q: What payment methods do you accept? A: Credit cards (Visa, Mastercard),
        PayPal, and bank transfers. Q: Is there a free trial? A: Yes, 14 days free with no credit card."""
    }

    col1.button("📋 Company Policy", key="btn_policy")
    col2.button("❓ Product FAQ", key="btn_faq")

    if "qa_document" not in st.session_state:
        st.session_state.qa_document = ""
    if "qa_question" not in st.session_state:
        st.session_state.qa_question = ""

    if st.session_state.get("btn_policy"):
        st.session_state.qa_document = example_docs_qa["Policy"]
        st.session_state.qa_question = "What is the remote work policy?"
    if st.session_state.get("btn_faq"):
        st.session_state.qa_document = example_docs_qa["FAQ"]
        st.session_state.qa_question = "How do I reset my password?"

    # Input
    col1, col2 = st.columns(2)

    with col1:
        document_qa = st.text_area(
            "📄 Document/Context",
            value=st.session_state.qa_document,
            placeholder="Paste document to search...",
            height=120,
            key="qa_document_input"
        )

    with col2:
        question_qa = st.text_area(
            "❓ Your Question",
            value=st.session_state.qa_question,
            placeholder="Ask a question...",
            height=120,
            key="qa_question_input"
        )

    # Answer button
    if st.button("🔍 Get Answer", type="primary", use_container_width=True):
        if not document_qa or not question_qa:
            st.warning("Please provide both a document and a question")
        else:
            with st.spinner("Finding answer..."):
                try:
                    client = LLMClient(model=st.session_state.model)
                    prompt = f"""Based on this document, answer the question:

Document:
{document_qa}

Question: {question_qa}

Answer:"""

                    start = time.time()
                    response = client.complete(
                        prompt,
                        temperature=st.session_state.temperature,
                        max_tokens=st.session_state.max_tokens
                    )
                    elapsed = time.time() - start

                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.success("**Answer:**")
                        st.write(response)
                    with col2:
                        st.metric("Time", f"{elapsed:.2f}s")

                except Exception as e:
                    st.error(f"Error: {e}")

    # Code comparison
    with st.expander("👨‍💻 See the code"):
        st.code("""
# Streamlit approach
import streamlit as st
from shared.llm_client import LLMClient

doc = st.text_area("Document")
question = st.text_input("Question")

if st.button("Get Answer"):
    client = LLMClient()
    answer = client.complete(f"Document: {doc}\\nQ: {question}")
    st.success(f"**A:** {answer}")
        """, language="python")


# ============================================================================
# FOOTER
# ============================================================================

st.divider()

st.markdown("""
### 🎓 Key Learnings

- **Speed**: Build AI UIs in minutes, not weeks
- **No HTML/CSS**: Pure Python + Streamlit handles the UI
- **Rapid iteration**: Change code, see results instantly
- **Real APIs**: Connect to actual LLMs, not mock data
- **Reusable patterns**: Copy patterns into your projects

### 📚 Next Steps

1. **Customize these examples** - try different prompts and models
2. **Build your own mode** - add classification, generation, analysis
3. **Deploy to cloud** - `streamlit cloud` for free hosting
4. **Production patterns** - Learn proper error handling, auth, databases

### 🚀 Deploy This App

```bash
streamlit cloud deploy
```

Open https://streamlit.io/cloud and connect your GitHub repo. Your app is live in seconds!
""")

st.caption("Module 3.3 • Rapid Prototyping with Streamlit • Learn to build AI apps fast")
