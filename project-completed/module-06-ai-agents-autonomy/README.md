# Module 6: AI Agents & Autonomy

**Objective:** Build autonomous agents with integrated memory and tool calling that learn from experience and execute complex workflows.

**Core Concept:** Agent = LLM Reasoning + Memory (SQLite + JSONL) + Tool Integration + Workflow Orchestration

---

## Lessons Overview

### Lesson 6.1: Agent Architecture & Design (Talking Head)
**Type:** Conceptual foundation  
**Topics:** Agent vs chatbot, ORAR loop, memory importance, autonomy patterns

---

### Lesson 6.2: Agent Memory Systems & LLM Reasoning (Menu-Driven CLI)
**Status:** ✅ Complete with real LLM integration + ORAR debug output

**Learning:** Each pattern compares WITHOUT memory vs WITH memory.

**Debug:** Set `DEBUG = True/False` at the top of the lesson file to show/hide ORAR cycle (Observe-Reason-Act-Reflect) internal reasoning steps.

**5 Patterns:**
1. **Short-Term Memory** — Conversation context with LLM
2. **Long-Term Memory** — Persistent facts (SQLite), survives restart
3. **Episodic Memory** — Past interactions stored as JSONL log
4. **Semantic Memory** — Company policies and knowledge base
5. **Integrated Memory** — All layers combined for comprehensive reasoning

**Run:**
```bash
export OPENROUTER_API_KEY='your-key-here'
python lesson-02-agent-memory-systems.py
```

**Architecture:**
- `shared/memory.py` — SemanticMemory (SQLite), EpisodicMemory (JSONL), ToolCallHistory
- `shared/agent.py` — Agent class with LLM reasoning and memory integration
- Memory uses OpenRouter API (gpt-3.5-turbo via shared LLM client)

---

### Lesson 6.3: Tool Use & Function Calling (Menu-Driven CLI)
**Status:** ✅ Complete with tool simulation + ORAR debug output

**Learning:** Each pattern compares WITHOUT tools vs WITH tools.

**Debug:** Set `DEBUG = True/False` at the top of the lesson file to show/hide ORAR cycle internal reasoning steps.

**4 Patterns:**
1. **Tool Discovery** — Agent learns available toolkit
2. **Tool Selection** — LLM chooses tools for task
3. **Sequential Execution** — Chaining multiple tools
4. **Memory Integration** — Agent learns optimal tool sequences

**Run:**
```bash
export OPENROUTER_API_KEY='your-key-here'
python lesson-03-tool-use-function-calling.py
```

**Architecture:**
- SimpleToolkit class simulates Module 5 MCP tools
- Agent memory stores tool invocations in JSONL log
- Demonstrates tool discovery and selection patterns

---

### Lesson 6.4: Chaining, CoT & Pipelines (Talking Head)
**Type:** Conceptual  
**Topics:** Chain-of-thought reasoning, prompt engineering for agents

---

### Lesson 6.5: Autonomous Workflows (Menu-Driven CLI)
**Status:** ✅ Complete with workflow state management

**Learning:** Each pattern compares manual execution vs autonomous workflow.

**4 Patterns:**
1. **Workflow Definition & Triggers** — Scheduled automation
2. **State Management** — Data flows through workflow steps
3. **Execution History & Learning** — Workflows improve over time
4. **Error Handling & Recovery** — Graceful degradation

**Run:**
```bash
export OPENROUTER_API_KEY='your-key-here'
python lesson-05-autonomous-workflows.py
```

**Architecture:**
- WorkflowStep — Individual step definition
- WorkflowContext — Shared state across execution
- Episodes stored in JSONL for learning and optimization

---

### Lesson 6.6: Multi-Agent Collaboration (Streamlit Dashboard - CAPSTONE)
**Status:** ✅ Complete with interactive dashboard

**Scenario:** Marketing campaign with 4 specialized agents coordinating real-time.

**Agents:**
- Campaign Manager (Orchestration)
- Content Agent (Material creation)
- Analytics Agent (Metrics analysis)
- Customer Service Agent (Feedback handling)

**Dashboard Features:**
- System state visualization (4 agents + their roles)
- Agent reasoning with LLM (tabs for each scenario)
- Execution history and memory tracking
- Full workflow orchestration

**Run:**
```bash
export OPENROUTER_API_KEY='your-key-here'
streamlit run lesson-06-multi-agent-collaboration.py
```

**Architecture:**
- Each agent has own SQLite + JSONL memory
- Shared toolkit concept (simulated)
- Cache-backed agent registry
- Multi-scenario execution (Strategy Review, Content, Analytics, Feedback, Full Workflow)

---

## Shared Utilities

**Memory System** (`shared/memory.py`):
- `SemanticMemory` — SQLite for facts & relationships
- `EpisodicMemory` — JSONL for temporal events
- `ToolCallHistory` — JSONL log for tool invocations
- `AgentMemoryManager` — Unified manager for all memory types

**Agent Implementation** (`shared/agent.py`):
- `Agent` class — LLM-integrated reasoning with memory
- `reason_with_memory()` — Query + context-aware responses
- `call_tool()` — Tool invocation with logging
- `learn_fact()/learn_relationship()` — Memory storage

---

## Learning Progression

1. **6.2** → Build foundational agent with memory types
2. **6.3** → Extend agent with tool calling
3. **6.5** → Orchestrate agent into autonomous workflows
4. **6.6** → Scale to multi-agent coordination with dashboard

Each lesson uses real LLM API calls (OpenRouter) and persistent storage (SQLite + JSONL) for production-ready patterns.

---

## Requirements

- `OPENROUTER_API_KEY` environment variable set
- Python 3.8+
- Dependencies: streamlit (for lesson 6.6 only)

```bash
pip install -r requirements-module-06.txt
```

---

## Key Takeaways

✅ Agents combine LLM reasoning with structured memory  
✅ Memory types serve different purposes (short/long-term, episodic, semantic)  
✅ Tools extend agents from thinkers to doers  
✅ Workflows automate multi-step processes with learning  
✅ Multi-agent systems scale via specialization and coordination  
✅ Persistent storage (SQLite + JSONL) enables cross-session learning

