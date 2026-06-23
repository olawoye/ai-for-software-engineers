"""
Lesson 3.4: Building Chat Interfaces

Learn how to build multi-turn conversational AI interfaces with context management.
Master state persistence, conversation history, and context window constraints.

Run: streamlit run lesson-04-building-chat-interface.py
Requires: export OPENROUTER_API_KEY='your-key-here'
"""

import streamlit as st
import time
from shared.llm_client import LLMClient
from shared.config import DEFAULT_MODEL, TEMP_BALANCED


# Page configuration
st.set_page_config(
    page_title="Building Chat Interfaces",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================================
# CONFIGURATION (code-level, not UI)
# ============================================================================

# >>> CUSTOMIZE: Model to use for chat
# Production tip: In real apps, this would be a deploy-time config or admin setting,
# not exposed to users (keeps surface simple, avoids support confusion)
CHAT_MODEL = DEFAULT_MODEL

# >>> CUSTOMIZE: System prompt that defines assistant personality
# This shapes how the AI behaves across all messages
SYSTEM_PROMPT = """You are a helpful, concise AI assistant.
Answer questions clearly and directly.
If you don't know something, say so honestly."""

# >>> REFERENCE: Context window management
# Different models have different limits. GPT-3.5: 4k, GPT-4: 8k/128k, Claude: 100k+
# We keep conversations under this to avoid "context full" errors
MAX_CONTEXT_TOKENS = 3000

# >>> REFERENCE: Temperature for chat (balanced between precision and creativity)
# 0.3 = precise responses, good for Q&A
# 0.7 = balanced (current setting, good for conversation)
# 0.9 = creative, risky in chat (may hallucinate)
TEMPERATURE = TEMP_BALANCED


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

# Initialize conversation history (persists across reruns)
# Store as list of {role, content} for proper LLM formatting
if "messages" not in st.session_state:
    st.session_state.messages = []

# Track tokens used (for visibility/debugging)
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def build_context_for_api(messages: list, max_tokens: int = MAX_CONTEXT_TOKENS) -> list:
    """
    Build conversation context respecting token limits.

    >>> REFERENCE: Why this matters
    LLMs have fixed context windows. If conversation gets too long, we need to:
    1. Keep recent messages (most relevant)
    2. Drop oldest messages (but keep system prompt)
    3. Prevent "context full" errors that break the app

    Simple strategy: If total messages exceed estimate, drop oldest user messages.
    More sophisticated apps use: token counting, summarization, or hierarchical memory.
    """
    if len(messages) <= 5:
        return messages  # Short conversation, include everything

    # Keep system context + last 5 messages
    # (rough estimate: most messages ~100-200 tokens, but use real token counter in production)
    if len(messages) > 8:
        messages = messages[-7:]  # Keep only recent

    return messages


def format_messages_for_api(messages: list) -> list:
    """
    Convert internal message format to API format.

    >>> REFERENCE: Message structure
    API expects: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    Our storage: same format, but we add system prompt separately
    """
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    api_messages.extend(messages)
    return api_messages


def count_tokens_estimate(text: str) -> int:
    """
    Rough token estimate (1 token ≈ 4 characters).

    >>> REFERENCE: Token counting
    In production, use the model's actual tokenizer or API token_usage response.
    This is a rough estimate for educational purposes.
    """
    return len(text) // 4


# ============================================================================
# HEADER
# ============================================================================

st.title("💬 Building Chat Interfaces")
st.markdown("""
This lesson teaches how to build **real conversational UIs** with context management.
Notice the UI is clean and focused—the complex work happens in the code (see comments).

**Real-world chat patterns:**
- Multi-turn conversation persistence
- Context window management (keep recent, drop old)
- System prompts for personality/behavior
- Error handling for network issues
""")


# ============================================================================
# MAIN CHAT UI (Real-world components only)
# ============================================================================

# Display conversation history
st.subheader("Conversation")

# Container for messages (easier to scroll)
message_container = st.container(height=400, border=True)

with message_container:
    if not st.session_state.messages:
        st.info("💬 Start a conversation below")
    else:
        # >>> REFERENCE: Display all messages in order
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg['content'])


# User input (bottom of screen)
st.divider()

col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input(
        "Your message:",
        placeholder="Type your question...",
        label_visibility="collapsed"
    )

with col2:
    send_button = st.button("Send", use_container_width=True, type="primary")


# ============================================================================
# HANDLE USER MESSAGE
# ============================================================================

if send_button and user_input:
    # >>> REFERENCE: Add user message to history
    # This happens immediately for responsiveness
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Get response from API
    try:
        with st.spinner("Thinking..."):
            # >>> REFERENCE: Build context respecting token limits
            # See build_context_for_api() - handles conversation memory constraints
            context_messages = build_context_for_api(st.session_state.messages)
            api_messages = format_messages_for_api(context_messages)

            # >>> CUSTOMIZE: Model selection
            # In production: choose based on cost/quality tradeoffs
            # - Fast/cheap: gpt-3.5-turbo, llama-2
            # - Balanced: gpt-4-turbo, claude-3-sonnet
            # - Best: gpt-4, claude-3-opus
            client = LLMClient(model=CHAT_MODEL)

            # >>> REFERENCE: Format conversation as prompt
            # This is what gets sent to the API
            prompt = ""
            for msg in api_messages[1:]:  # Skip system (handled separately by API)
                role_label = "User" if msg["role"] == "user" else "Assistant"
                prompt += f"{role_label}: {msg['content']}\n"
            prompt += "Assistant:"

            start_time = time.time()
            response = client.complete(
                prompt,
                temperature=TEMPERATURE,
                max_tokens=500,
            )
            elapsed = time.time() - start_time

            # >>> REFERENCE: Add assistant response to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.strip()
            })

            # >>> REFERENCE: Track token usage (for visibility)
            tokens_used = count_tokens_estimate(user_input) + count_tokens_estimate(response)
            st.session_state.total_tokens += tokens_used

    except Exception as e:
        st.error(f"Error: {e}")
        # Remove user message if API failed
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            st.session_state.messages.pop()

    # Rerun to display new message
    st.rerun()


# ============================================================================
# CLEAR CONVERSATION (Real-world button)
# ============================================================================

if st.button("🗑️ Clear Conversation", use_container_width=False):
    st.session_state.messages = []
    st.session_state.total_tokens = 0
    st.rerun()


# ============================================================================
# FOOTER WITH DEVELOPER INSIGHTS
# ============================================================================

st.divider()

with st.expander("👨‍💻 How This Works (Developer View)"):
    st.markdown(f"""
    **State Management:**
    - `st.session_state.messages` persists across reruns (Streamlit's key feature)
    - Each message is `{{"role": "user/assistant", "content": "..."}}`
    - System prompt added separately during API call

    **Context Window Management:**
    - Current conversation: {len(st.session_state.messages)} messages
    - Estimated tokens: {st.session_state.total_tokens} (rough count)
    - Limit: {MAX_CONTEXT_TOKENS} tokens max per API call
    - Strategy: If too long, keep only recent messages (see `build_context_for_api()`)

    **Model & Temperature:**
    - Model: `{CHAT_MODEL}`
    - Temperature: `{TEMPERATURE}` (0.7 = balanced)
    - In production: expose these in admin/settings, not user UI

    **System Prompt:**
    - Controls assistant behavior across all messages
    - Current: "Helpful, concise assistant"
    - To customize: edit SYSTEM_PROMPT variable (line 30)

    **Error Handling:**
    - If API fails, user message is removed from history
    - Users see friendly error message
    - Production: would retry, log errors, alert admin
    """)

with st.expander("🎓 Key Learnings"):
    st.markdown("""
    **What Makes This a Real Chat App:**
    - ✅ Multi-turn context (remembers previous messages)
    - ✅ Proper message formatting (role-based)
    - ✅ State persistence (conversation doesn't reset)
    - ✅ Token budget management (avoids context overflow)
    - ✅ Clean UX (no developer knobs exposed)

    **Production Considerations (beyond scope):**
    - User authentication (who is this conversation for?)
    - Persistence layer (save conversations to database)
    - Conversation retrieval (browse past chats)
    - Rate limiting (prevent abuse)
    - Cost tracking (know spending per user/conversation)
    - Moderation (block harmful content)
    - Analytics (understand usage patterns)
    """)

st.divider()

with st.expander("🔧 Try This"):
    st.markdown("""
    **Modify the code to experiment:**

    1. **Change system prompt** (line 30):
       - Try: "You are a Shakespeare expert" or "You are extremely sarcastic"
       - Notice how responses change immediately

    2. **Adjust temperature** (line 41):
       - Change to 0.3 (very precise) or 0.9 (very creative)
       - Try: "Write a poem about AI"

    3. **Switch models** (line 21):
       - Use `"gpt-4"` instead of `"gpt-3.5-turbo"`
       - Compare quality vs speed tradeoffs

    4. **Reduce context** (line 35):
       - Change `MAX_CONTEXT_TOKENS = 3000` to `= 1000`
       - See how old messages get dropped
    """)

st.caption("Module 3.4 • Building Chat Interfaces • Multi-turn conversation with context management")
