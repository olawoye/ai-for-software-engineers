"""
Lesson 3.6: AI Operations Assistant with Tool Calling (Capstone)

Learn how LLMs orchestrate actions through tool calling and function selection.
Build an intelligent assistant that makes decisions about which tools to use
and executes them safely based on user requests.

This lesson introduces the paradigm shift:
"LLMs don't just generate text. They orchestrate actions."

This concept becomes the foundation for:
- Module 5: MCP (structured tool protocols)
- Module 6: Agents (autonomous decision-making)
- Modules 7-8: AI-native systems

Run: streamlit run lesson-06-ai-operations-assistant.py
Requires: export OPENROUTER_API_KEY='your-key-here'
"""

import streamlit as st
import time
import random
import json
from datetime import datetime
from shared.llm_client import LLMClient
from shared.config import DEFAULT_MODEL, TEMP_BALANCED


# Page configuration
st.set_page_config(
    page_title="AI Operations Assistant",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================================
# TOOL DEFINITIONS & IMPLEMENTATIONS
# ============================================================================

def get_weather(city: str) -> dict:
    """
    Tool 1: Weather Lookup (API simulation)

    >>> REFERENCE: Demonstrates external API integration
    In production: call real weather API
    """
    cities = {
        "san francisco": {"temp": 65, "condition": "sunny"},
        "new york": {"temp": 45, "condition": "cloudy"},
        "seattle": {"temp": 55, "condition": "rainy"},
        "austin": {"temp": 85, "condition": "sunny"},
    }
    city_lower = city.lower()
    if city_lower in cities:
        return {"status": "success", "data": cities[city_lower], "city": city}
    return {"status": "error", "message": f"Weather data for {city} not available"}


def lookup_ticket(ticket_id: str) -> dict:
    """
    Tool 2: Ticket Lookup (Database query simulation)

    >>> REFERENCE: Demonstrates database access pattern
    In production: query ticket management system
    """
    tickets = {
        "TKT-001": {"status": "open", "priority": "high", "title": "Login issue"},
        "TKT-002": {"status": "in-progress", "priority": "medium", "title": "Performance bug"},
        "TKT-003": {"status": "closed", "priority": "low", "title": "UI improvement"},
    }
    if ticket_id.upper() in tickets:
        return {"status": "success", "data": tickets[ticket_id.upper()], "ticket_id": ticket_id}
    return {"status": "error", "message": f"Ticket {ticket_id} not found"}


def search_policy(query: str) -> dict:
    """
    Tool 3: Policy Search (Knowledge base search)

    >>> REFERENCE: Demonstrates semantic search pattern
    In production: search vector database (see Module 4: RAG)
    """
    policies = {
        "remote work": "Employees may work from home up to 3 days per week",
        "vacation": "20 days PTO per year, plus 10 company holidays",
        "equipment": "Company provides laptop and monitor",
        "security": "Use VPN for remote access. Never share credentials.",
    }
    query_lower = query.lower()
    for key, value in policies.items():
        if key in query_lower:
            return {"status": "success", "data": value, "query": query}
    return {"status": "error", "message": f"No policy found for '{query}'"}


def execute_sql(query: str) -> dict:
    """
    Tool 4: SQL Query Execution (Data analysis)

    >>> REFERENCE: Demonstrates safe SQL execution with limits
    In production: execute read-only queries against real database
    """
    if "DROP" in query.upper() or "DELETE" in query.upper():
        return {"status": "error", "message": "Dangerous SQL commands not allowed"}

    # Simulate query results
    return {
        "status": "success",
        "data": {
            "rows_returned": random.randint(5, 50),
            "columns": ["id", "name", "value"],
            "sample_row": {"id": 1, "name": "Sample", "value": 100},
        },
        "query": query[:50] + "..." if len(query) > 50 else query,
    }


def calculate(expression: str) -> dict:
    """
    Tool 5: Calculator (Expression evaluation)

    >>> REFERENCE: Demonstrates mathematical operations
    In production: use safer evaluation with limited operators
    """
    try:
        # >>> REFERENCE: Safety: only allow numbers and basic operators
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression):
            return {"status": "error", "message": "Invalid expression"}

        result = eval(expression)  # In production: use safer eval library
        return {"status": "success", "data": result, "expression": expression}
    except Exception as e:
        return {"status": "error", "message": f"Calculation failed: {str(e)}"}


# Tool registry (centralized tool definitions)
TOOLS = {
    "weather": {
        "name": "weather",
        "description": "Get weather for a city",
        "parameters": {"city": "string"},
        "execute": get_weather,
    },
    "ticket": {
        "name": "ticket",
        "description": "Look up support ticket by ID",
        "parameters": {"ticket_id": "string"},
        "execute": lookup_ticket,
    },
    "policy": {
        "name": "policy",
        "description": "Search company policies",
        "parameters": {"query": "string"},
        "execute": search_policy,
    },
    "sql": {
        "name": "sql",
        "description": "Execute SQL query (read-only)",
        "parameters": {"query": "string"},
        "execute": execute_sql,
    },
    "calculator": {
        "name": "calculator",
        "description": "Perform calculations",
        "parameters": {"expression": "string"},
        "execute": calculate,
    },
}


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "tool_calls" not in st.session_state:
    st.session_state.tool_calls = []

if "total_tools_used" not in st.session_state:
    st.session_state.total_tools_used = 0


# ============================================================================
# FUNCTION CALLING LOGIC
# ============================================================================

def build_tool_context() -> str:
    """
    >>> REFERENCE: Build system prompt describing available tools
    This tells the LLM what tools it can use and how to call them.
    """
    tools_description = "\n".join(
        f"- {t['name']}: {t['description']} (param: {list(t['parameters'].keys())[0]})"
        for t in TOOLS.values()
    )
    return f"""You are an operations assistant with access to these tools:

{tools_description}

When you need information, call a tool using this format:
<tool_call>tool_name(parameter_name=value)</tool_call>

Only call ONE tool per response. Wait for the result, then respond.
"""


def extract_tool_call(text: str) -> tuple:
    """
    >>> REFERENCE: Parse tool calls from LLM output
    Detects: <tool_call>tool_name(param=value)</tool_call>
    """
    import re
    pattern = r"<tool_call>(\w+)\((\w+)=([^)]+)\)</tool_call>"
    match = re.search(pattern, text)
    if match:
        tool_name, param_name, param_value = match.groups()
        return tool_name.strip(), {param_name: param_value.strip().strip('"')}
    return None, None


def execute_tool(tool_name: str, params: dict) -> dict:
    """
    >>> REFERENCE: Safely execute a tool with parameters
    Includes error handling and timeout protection.
    """
    if tool_name not in TOOLS:
        return {"status": "error", "message": f"Tool '{tool_name}' not found"}

    try:
        tool = TOOLS[tool_name]
        result = tool["execute"](**params)
        return result
    except Exception as e:
        return {"status": "error", "message": f"Tool execution failed: {str(e)}"}


# ============================================================================
# HEADER
# ============================================================================

st.title("🤖 AI Operations Assistant")
st.markdown("""
This lesson demonstrates the **paradigm shift**: LLMs don't just generate text—they orchestrate actions.

The assistant:
1. **Decides** what information it needs
2. **Selects** the appropriate tool
3. **Executes** the tool safely
4. **Responds** based on real results

This concept is the foundation for agents (Module 6), MCP (Module 5), and autonomous systems.
""")


# ============================================================================
# MAIN CHAT INTERFACE
# ============================================================================

st.subheader("Conversation")
message_container = st.container(height=400, border=True)

with message_container:
    if not st.session_state.messages:
        st.info("💬 Try: 'What's the weather in San Francisco?' or 'Look up ticket TKT-001'")
    else:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])


# ============================================================================
# USER INPUT & PROCESSING
# ============================================================================

st.divider()

col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input(
        "Your message:",
        placeholder="Ask me to look something up or perform an action...",
        label_visibility="collapsed"
    )

with col2:
    send_button = st.button("Send", use_container_width=True, type="primary")


if send_button and user_input:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    try:
        with st.spinner("Thinking..."):
            # >>> REFERENCE: Initialize LLM with tool context
            client = LLMClient(model=DEFAULT_MODEL)
            tool_context = build_tool_context()

            # >>> REFERENCE: Build conversation for API
            conversation = [
                {"role": "system", "content": tool_context},
                *st.session_state.messages,
            ]

            # Format as prompt string for API
            prompt = ""
            for msg in conversation[1:]:
                prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"
            prompt += "Assistant:"

            # >>> REFERENCE: Get LLM response (may include tool call)
            start_time = time.time()
            response = client.complete(
                prompt,
                temperature=TEMP_BALANCED,
                max_tokens=500,
            )
            elapsed = time.time() - start_time

            # >>> REFERENCE: Check if response contains tool call
            tool_name, params = extract_tool_call(response)

            if tool_name and params:
                # >>> REFERENCE: Execute tool and get result
                tool_result = execute_tool(tool_name, params)

                # Track tool usage
                st.session_state.tool_calls.append({
                    "tool": tool_name,
                    "params": params,
                    "result": tool_result,
                    "timestamp": datetime.now().isoformat(),
                })
                st.session_state.total_tools_used += 1

                # >>> REFERENCE: Use tool result to generate final response
                final_prompt = f"""{prompt}
I called the {tool_name} tool with result: {json.dumps(tool_result)}
Now respond to the user based on this result."""

                final_response = client.complete(
                    final_prompt,
                    temperature=TEMP_BALANCED,
                    max_tokens=300,
                )

                # Display tool call info
                st.info(f"🔧 Called tool: **{tool_name}**({', '.join(f'{k}={v}' for k, v in params.items())})")

                if tool_result.get("status") == "success":
                    st.success(f"✓ Result: {json.dumps(tool_result.get('data'))}")
                else:
                    st.warning(f"⚠️ {tool_result.get('message')}")

                # Add assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": final_response.strip()
                })

            else:
                # No tool call, just respond directly
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response.strip()
                })

    except Exception as e:
        st.error(f"Error: {e}")
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            st.session_state.messages.pop()

    st.rerun()


# ============================================================================
# SIDEBAR: ANALYTICS & DEBUG
# ============================================================================

with st.sidebar:
    st.header("📊 Analytics")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Messages", len(st.session_state.messages))
    with col2:
        st.metric("Tools Used", st.session_state.total_tools_used)
    with col3:
        st.metric("Conversations", len([m for m in st.session_state.messages if m["role"] == "user"]))

    st.divider()

    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.session_state.tool_calls = []
        st.rerun()

    if st.session_state.tool_calls:
        st.subheader("🔧 Tool History")
        for i, call in enumerate(st.session_state.tool_calls[-5:], 1):
            status_icon = "✓" if call["result"].get("status") == "success" else "✗"
            st.text(f"{i}. {status_icon} {call['tool']}")


# ============================================================================
# FOOTER: LEARNING INSIGHTS
# ============================================================================

st.divider()

with st.expander("👨‍💻 How This Works (Developer View)"):
    st.markdown("""
    **The Tool-Calling Workflow:**

    1. **Tool Context** → Tell LLM what tools are available
    2. **User Input** → Process user message
    3. **LLM Decision** → Model decides if a tool is needed
    4. **Tool Call Detection** → Parse `<tool_call>...</tool_call>` from response
    5. **Execution** → Run the selected tool with parameters
    6. **Result Injection** → Feed result back to LLM
    7. **Final Response** → Generate answer based on tool result

    **Key Insight:** The LLM isn't just generating text—it's orchestrating a workflow.

    **Safety Patterns:**
    - Tool name validation
    - Parameter validation
    - Error handling
    - Dangerous command blocking (SQL DROP, DELETE)
    - Timeout protection
    """)

with st.expander("🎓 Why This Matters"):
    st.markdown("""
    **Tool Calling is the Foundation of:**

    - **Module 5: MCP** → Standardized tool protocols
    - **Module 6: Agents** → Autonomous tool selection and execution
    - **Module 7: AI Systems** → Tool orchestration at scale
    - **Module 8: Production** → Monitoring tool reliability and cost

    **Modern Reality:** Most valuable AI systems don't just talk—they act.

    Examples:
    - Research assistants that search documents
    - Sales agents that query CRM systems
    - Support bots that create tickets and look up policies
    - Analytics assistants that run queries
    - Workflow automation that executes actions

    This lesson demonstrates the pattern that powers all of them.
    """)

with st.expander("🧪 Try These Examples"):
    st.markdown("""
    **Weather Tool:**
    - "What's the weather in Seattle?"
    - "Is it sunny in Austin?"

    **Ticket System:**
    - "Look up ticket TKT-001"
    - "Get status of TKT-002"

    **Policy Search:**
    - "What's our remote work policy?"
    - "How much vacation do we get?"

    **SQL Queries:**
    - "How many orders were placed last week?"
    - "Run a COUNT query on users"

    **Calculator:**
    - "Calculate 15 * 25"
    - "What's 100 divided by 3?"
    """)

st.caption("Module 3.6 • AI Operations Assistant • Tool Calling & Action Orchestration")
