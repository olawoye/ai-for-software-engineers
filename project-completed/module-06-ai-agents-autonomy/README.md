# Module 6: AI Agents & Autonomy

**Objective:** Build autonomous agents that perceive their environment, reason about state, take actions, and learn from outcomes. Integrate agents with tools (Module 5 MCP toolkit) to create complete autonomous systems.

**Core Concept:** Agent = Autonomous system with Observe → Reason → Act → Reflect decision loop + integrated memory

---

## Lesson Overview

### Lesson 6.1: Agent Architecture & Design (Talking Head)
- **Type:** Conceptual + Discussion
- **Topics:**
  - What makes an agent vs. a chatbot
  - Agent decision loops (ORAR)
  - Memory as foundation of agency
  - Autonomy patterns and degrees
- **Note:** Concepts consolidated into Lesson 6.2 code

### Lesson 6.2: Agent Memory Systems (Code Screencast)
**[PRIMARY IMPLEMENTATION LESSON - CONSOLIDATED]**

**Status:** ✅ Complete and verified

**Core Template Method:**
```python
create_agent_with_memory(
    agent_name: str,
    memory_strategy: str = "hybrid",
    max_short_term_items: int = 10,
    enable_persistence: bool = True,
) -> Agent
```

**Architecture:**
- **ShortTermMemory** — Working memory (current conversation, max 10 items)
- **LongTermMemory** — Persistent facts (survives session restarts, JSON-backed)
- **EpisodicMemory** — Past interactions (recalled by similarity matching)
- **SemanticMemory** — Knowledge base (organized by category)
- **Agent Class** — Orchestrates all memory layers + decision loop

**Business Scenario:** Customer support agent that remembers previous interactions, customer preferences, company policies, and historical actions.

**Run Instructions:**
```bash
cd project-completed/module-06-ai-agents-autonomy
python3 lesson-02-agent-memory-systems.py
```

**6 Demonstrations:**
1. **Agent Architecture** — Show ORAR loop, agent vs. chatbot
2. **Short-Term Memory** — Multi-turn conversation retention
3. **Long-Term Memory** — Persistent facts and retrieval
4. **Episodic Memory** — Recall past interactions by similarity
5. **Semantic Memory** — Knowledge base queries
6. **Integrated Memory** — Full agent decision loop with all memory layers

**Key Outputs:**
```
Agent memory context (all 4 layers combined):
  Recent conversation: [last 3 exchanges]
  Known facts: [persistent customer data]
  Recent episodes: [past interactions]
  Knowledge: [relevant policies/skills]

Agent Decision Loop:
  OBSERVE → Retrieve memory context
  REASON → Plan response using context
  ACT → Generate response + update state
  REFLECT → Store interaction in episodic memory
```

**Integration Points:**
- Prepares foundation for Lesson 6.3 (Tool integration)
- Memory enables tool selection and sequencing
- Episodic memory stores tool outcomes for future reference

**Files:**
- [Completed](lesson-02-agent-memory-systems.py) (~1000 lines, verified working)
- [TODO Scaffold](../../project-todo/module-06-ai-agents-autonomy/lesson-02-agent-memory-systems.py) (~400 lines, phase-based guidance)

---

### Lesson 6.3: Tool Use & Function Calling (Code Screencast)
**[PRIMARY TOOL INTEGRATION LESSON - COMPLETE]**

**Status:** ✅ Complete and verified

**Core Template Method:**
```python
create_agent_with_tools(
    agent_name: str,
    toolkit: Optional[MCPToolkit] = None,
    tool_selection_strategy: str = "keyword_match",
) -> ToolAwareAgent
```

**Architecture:**
- **MCPToolkit** — Represents external tool server with 8 tools
- **ToolSpec** — Describes individual tool (name, description, category, input_schema)
- **ToolAwareAgent** — Wraps agent with tool discovery, selection, and invocation
- **Tool Categories:**
  - Knowledge (2): search_knowledge, get_document
  - Email (4): parse_email, analyze_sentiment, extract_action_items, extract_keywords
  - System (2): list_tools, get_toolkit_info

**Business Scenario:** Sales manager agent identifies overdue accounts, retrieves CRM data, analyzes customer emails, and generates recovery action plans.

**Run Instructions:**
```bash
cd project-completed/module-06-ai-agents-autonomy
python3 lesson-03-tool-use-function-calling.py
```

**6 Demonstrations:**
1. **Tool Discovery** — Agent lists available tools from toolkit
2. **Tool Selection** — Agent chooses tools based on user query
3. **Single Tool Invocation** — Agent calls one tool (search_knowledge)
4. **Sequential Workflow** — Agent chains 3 tools (knowledge → email → actions)
5. **Error Handling** — Agent handles non-existent tool gracefully
6. **Memory Integration** — Tool results stored in episodic memory for learning

**Key Outputs:**
```
Tool Discovery: 8 tools found (2 knowledge, 4 email, 2 system)

Tool Selection:
  Query: "overdue accounts and email history"
  Selected: search_knowledge, parse_email, analyze_sentiment

Workflow Result:
  [1] search_knowledge: Found 2 documents about account recovery
  [2] parse_email: Email parsed successfully
  [3] extract_action_items: Identified 3 action items

Memory Storage:
  Tool call history: 3 calls recorded
  Pattern: knowledge → email analysis → action extraction
  Timestamps: All recorded for future reference
```

**Integration Points:**
- Bridges Lesson 6.2 (Agent Memory) with tool calling
- Tool results stored in episodic memory (lesson 6.2 pattern)
- Tool selection uses agent reasoning (lesson 6.2 ORAR loop)
- Prepares for Lesson 6.5 (Multi-tool workflows)

**Files:**
- [Completed](lesson-03-tool-use-function-calling.py) (~700 lines, verified working)
- [TODO Scaffold](../../project-todo/module-06-ai-agents-autonomy/lesson-03-tool-use-function-calling.py) (~300 lines, phase-based guidance)

---

### Lesson 6.4: Chaining, CoT & Pipelines (Talking Head)
**[PLANNED - CONCEPTUAL]**

**Topics:**
- Chain-of-thought (CoT) prompting
- Sequential tool pipelines
- Branching and conditional logic
- Error handling and backtracking

---

### Lesson 6.5: Autonomous Workflows (Code Screencast)
**[WORKFLOW ORCHESTRATION & LEARNING - COMPLETE]**

**Status:** ✅ Complete and verified

**Core Template Method:**
```python
create_autonomous_workflow(
    name: str,
    trigger_type: str = "manual",  # "manual", "time_based", "event_based"
    trigger_config: Optional[Dict] = None,  # Schedule or event config
    workflow_definition: Optional[List[Dict]] = None,  # Workflow steps
    success_criteria: Optional[str] = None,
    agent=None,
    toolkit=None,
) -> AutonomousWorkflow
```

**Architecture:**
- **WorkflowContext** — Tracks execution state across steps
- **WorkflowStep** — Represents individual step (tool call, decision, conditional, transform)
- **AutonomousWorkflow** — Container with trigger config, steps, execution history
- **WorkflowExecutor** — Engine that runs workflows with state management

**Business Scenario:** Weekly executive report automation
- **Trigger:** Every Friday 5 PM
- **Steps:**
  1. Query knowledge base for metrics
  2. Get recent emails
  3. Analyze sentiment from communications
  4. Compile findings into report
  5. Store report in long-term memory
- **Learning:** Success patterns stored in episodic memory improve future runs

**Run Instructions:**
```bash
cd project-completed/module-06-ai-agents-autonomy
python3 lesson-05-autonomous-workflows.py
```

**6 Demonstrations:**
1. **Workflow Definition** — Define multi-step workflow (4 steps)
2. **Trigger Configuration** — Set up scheduling (manual, time-based, event-based)
3. **Single Execution** — Run workflow and show all steps
4. **Conditional Branching** — Workflow with if/then logic
5. **State Persistence** — Store execution history and statistics
6. **Execution History Learning** — Show how history improves future runs

**Key Outputs:**
```
Workflow Definition: 4 steps (Query → Get → Analyze → Compile)

Trigger Types:
  - manual: Next execution = None (on-demand)
  - time_based: Next execution = Friday 5 PM
  - event_based: Next execution = None (event-driven)

Execution Result:
  Steps: 3/3 completed
  Duration: 0.00s
  Errors: 0
  
Execution Summary:
  Total executions: 3
  Success rate: 100%
  Avg duration: 0.05s
  
Learning from History:
  Pattern: Search → Analyze → Summarize (100% success)
  Episodic memory: 3 executions recorded
  Semantic memory: Best practices learned
```

**Memory Integration:**
- **Episodic:** Track each workflow execution (3 runs recorded → pattern recognized)
- **Long-term:** Store metrics, thresholds, workflow templates
- **Semantic:** Store best practices ("3-step flow works best")
- **Short-term:** Current execution state and step outputs

**Integration Points:**
- Builds on Lesson 6.2 (Agent Memory) for decision-making
- Builds on Lesson 6.3 (Tool Calling) for step execution
- Prepares for Lesson 6.6 (Multi-agent workflows)

**Files:**
- [Completed](lesson-05-autonomous-workflows.py) (~1100 lines, verified working)
- [TODO Scaffold](../../project-todo/module-06-ai-agents-autonomy/lesson-05-autonomous-workflows.py) (~400 lines, phase-based guidance)

---

### Lesson 6.6: Multi-Agent Collaboration (Code Screencast)
**[CAPSTONE - MULTI-AGENT ORCHESTRATION]**

**Status:** ✅ Complete and verified

**Core Template Method:**
```python
create_multi_agent_system(
    system_name: str,
    agents: List[ToolAwareAgent],
    shared_toolkit: Optional[MCPToolkit] = None,
    coordinator_strategy: str = "hierarchy",
) -> MultiAgentSystem
```

**Architecture:**
- **AgentRole** — Enum for specialized roles (MANAGER, CONTENT, ANALYTICS, SERVICE)
- **AgentCapability** — Tracks role, specialization, assigned tools, priority
- **AgentRegistry** — Central registry mapping agents to capabilities and roles
- **Message** — Represents inter-agent communication (sender, recipient, type, content)
- **MessageQueue** — Manages asynchronous agent communication with history
- **Coordinator** — Assigns tasks and resolves conflicts (hierarchy, voting, market-based)
- **MultiAgentSystem** — Container orchestrating all agents with shared resources

**Business Scenario:** Marketing campaign orchestration with team specialization
- **Campaign Manager Agent** — Manager role orchestrates overall strategy and delegates
- **Content Agent** — Content role creates marketing materials and campaigns
- **Analytics Agent** — Analytics role monitors metrics and provides insights
- **Customer Service Agent** — Service role handles customer interactions

**Tool Integration (from Module 5):**
- All agents access shared MCP toolkit
- Knowledge tools (search, documents) available to all agents
- Email tools (parse, analyze, extract) available to service and analytics agents
- System tools (list, info) available to manager for audit/coordination

**Coordination Strategies:**
- **Hierarchy** — Manager makes decisions, delegates to specialists (default)
- **Voting** — Agents vote on task assignment (consensus)
- **Market-based** — Agents bid for tasks (auction mechanism)

**Run Instructions:**
```bash
cd project-completed/module-06-ai-agents-autonomy
python3 lesson-06-multi-agent-collaboration.py
```

**6 Demonstrations:**
1. **System Setup & Agent Discovery** — Register 4 agents with specialization
2. **Agent Capabilities** — Show each agent's role, tools, and specialization
3. **Task Assignment** — Coordinator assigns tasks to appropriate agents
4. **Parallel Workflow Execution** — Multi-step workflow with specialized agents
5. **Inter-Agent Communication** — Messages flow between agents via queue
6. **Coordination Learning** — Show how shared episodic memory improves future runs

**Key Outputs:**
```
Multi-Agent System Initialization:
  ✓ System: Marketing Campaign System
  ✓ Coordinator Strategy: hierarchy
  ✓ Agents: 4
    - Manager: 1 (orchestration)
    - Content: 1 (materials creation)
    - Analytics: 1 (metrics analysis)
    - Service: 1 (customer interaction)
  ✓ Shared Toolkit: 8 tools available
  ✓ Status: Ready for multi-agent workflows

Task Assignment (Manager Coordinating):
  Task 1: Review campaign objectives
    → Assigned to: Campaign Manager (priority 1)
    → Tools: knowledge_search
  
  Task 2: Generate email campaign
    → Assigned to: Content Agent (priority 2)
    → Tools: get_document, email tools
  
  Task 3: Analyze customer feedback
    → Assigned to: Analytics Agent (priority 2)
    → Tools: parse_email, analyze_sentiment, extract_keywords

Agent Communication Pattern:
  Campaign Manager → Content Agent (task)
  Campaign Manager → Analytics Agent (task)
  Analytics Agent → Campaign Manager (result: "30% increase in engagement")
  
Workflow Execution with All Agents:
  Workflow: Weekly Campaign Execution
  Steps: 4 (Manager reviews → Content creates → Analytics analyzes → Service responds)
  Agents involved: 4
  Coordination style: Manager delegates to specialists
  Total execution time: 0.1s
  Success rate: 100%

Coordination Learning from Multiple Runs:
  Run 1: Manager → Content → Analytics → Service
  Run 2: Same pattern, 100% success
  Run 3: Same pattern, 100% success
  
  Learned pattern: "4-step hierarchical flow is most effective"
  All agents update episodic memory: This pattern works best
  Semantic memory: "Manager should coordinate, delegate to specialists"
```

**Memory Integration (Crosses All Previous Lessons):**
- **Short-term (6.2):** Current workflow state and message queue
- **Long-term (6.2):** Agent roles, capabilities, tool assignments
- **Episodic (6.2):** Execution history of workflows, learned patterns
- **Semantic (6.2):** Coordination strategies, best practices
- **Tool history (6.3):** Each tool call logged and available to all agents
- **Workflow history (6.5):** Multi-step patterns stored for reuse

**Scalability Pattern:**
```
Single Agent (Lesson 6.2)
  ↓
  Integrated memory + reasoning

Single Agent + Tools (Lesson 6.3)
  ↓
  Can execute complex tasks via tools

Single Agent + Workflows (Lesson 6.5)
  ↓
  Can orchestrate multi-step processes with scheduling

Multiple Agents + Coordination (Lesson 6.6)
  ↓
  Can tackle business processes requiring specialization and teamwork
```

**Integration Points:**
- **Lesson 6.2 Foundation:** Each agent has integrated memory (all 4 layers)
- **Lesson 6.3 Execution:** Each agent can discover and call tools
- **Lesson 6.5 Orchestration:** Workflows coordinate multi-agent execution
- **Lesson 6.6 Culmination:** Multi-agent system with specialization + coordination

**Files:**
- [Completed](lesson-06-multi-agent-collaboration.py) (~1300 lines, verified working)
- [TODO Scaffold](../../project-todo/module-06-ai-agents-autonomy/lesson-06-multi-agent-collaboration.py) (~500 lines, phase-based guidance)

---

## Data Flow: Lesson-to-Lesson Integration

```
Lesson 6.2 Output
  ↓
Agent with integrated memory (ShortTerm + LongTerm + Episodic + Semantic)
  ↓
Lesson 6.3 Input: Agent + MCP Toolkit
  ↓
Agent discovers and calls tools
Tools return results → stored in episodic memory for future reference
  ↓
Lesson 6.5 Input: Agent + Tools + Workflow scheduler
  ↓
Autonomous workflows execute multi-step tasks using agent memory + tool composition
  ↓
Lesson 6.6 Input: Multiple agents + shared tools + coordinator
  ↓
Multi-agent system orchestrates complex business processes
```

---

## Module 5 Tool Integration Strategy

**Strategic Tool Usage (by Lesson):**

| Lesson | Primary Use | Tools | Context |
|--------|------------|-------|---------|
| 6.2 | N/A (foundation only) | None | Memory architecture |
| 6.3 | **Direct integration** | All 10 (knowledge, email, system) | Tool calling basics |
| 6.4 | N/A (conceptual) | None | Theory only |
| 6.5 | **Workflow orchestration** | Knowledge + Email (primary) | Multi-step automation |
| 6.6 | **Shared access** | All 10 (distributed) | Multi-agent coordination |

**Key Decision:** Each agent has local memory (from 6.2) + shared access to tools (from Module 5)

---

## Shared Dependencies

All lessons reference:
- **shared.llm** — LLM interaction utilities
- **shared.mcp_server** — MCP server and tool infrastructure (Module 5)
- **shared.permissions** — Security and permission validation (Module 5)

---

## Curriculum Links

- **Module 5** (Prior): MCP Servers & Tools
  - Lesson 5.3: Personal Knowledge Server
  - Lesson 5.4: Email Analyst Server
  - Lesson 5.5: Security Guardrails
  - Lesson 5.6: MCP Toolkit Capstone (10 tools available for Module 6)

- **Module 7** (Next): AI-Native Systems Architecture
  - How agent systems scale in production
  - System design with multiple agents and tools

---

## Quick Reference: Template Methods by Lesson

| Lesson | Core Method | Returns |
|--------|------------|---------|
| 6.2 | `create_agent_with_memory()` | Agent (4 memory layers) |
| 6.3 | `create_agent_with_tools()` | Agent (memory + tool calling) |
| 6.5 | `create_autonomous_workflow()` | Workflow (scheduled automation) |
| 6.6 | `create_multi_agent_system()` | MultiAgentSystem (orchestrated agents) |

---

## Completion Status

✅ **MODULE 6 COMPLETE** — All code lessons implemented and verified

1. ✅ **Lesson 6.2:** Agent Memory Systems — COMPLETE (1000+ lines, 6/6 demos verified)
2. ✅ **Lesson 6.3:** Tool Use & Function Calling — COMPLETE (700 lines, 6/6 demos verified)
3. ✅ **Lesson 6.5:** Autonomous Workflows — COMPLETE (1100+ lines, 6/6 demos verified)
4. ✅ **Lesson 6.6:** Multi-Agent Collaboration (CAPSTONE) — COMPLETE (1300+ lines, 6/6 demos verified)

**Total:** ~4000 lines production code + ~1500 lines TODO scaffolds

---

## Business Value

By end of Module 6, learners can:
- Build agents that learn and adapt
- Call tools with context-aware decision making
- Automate multi-step business workflows
- Coordinate multiple specialized agents
- Integrate with enterprise tool ecosystems (like MCP servers)

**Real-world Applications:**
- Customer support automation (with memory and tool access)
- Data analysis workflows (autonomous multi-step research)
- Content generation pipelines (agent collaboration)
- Business process automation (scheduled autonomous workflows)

---

## Resource Scripts

### `resource_agent_loop.py`
A stateful ReAct (Reason + Act) agent loop implementation with execution guardrails. Designed to be imported and adapted for building safe, bounded autonomous systems.

**Location:** `resource_agent_loop.py`

**Classes:**

#### 1. `ExecutionGuardrails`
Real-time safety watcher enforcing step limits, token budgets, and detecting repetitive tool loops (stagnation).

**Constructor:**
```python
guardrails = ExecutionGuardrails(max_steps=5, max_token_budget=4000)
```

**Methods:**

- **`verify_step(action_signature: str, estimated_tokens: int)`**
  - Enforces execution rules before running an LLM or tool turn
  - Checks three guardrails:
    1. **Step Limit** — Raises exception if max_steps exceeded
    2. **Token Budget** — Raises exception if total tokens exceeded
    3. **Stagnation Detection** — Raises exception if action repeated 2+ times
  - Use when: Each agent iteration (thinking, tool call, observation)
  - Raises: `AgentGuardrailException` if any guardrail triggered
  - **Example:**
    ```python
    try:
        guardrails.verify_step(
            action_signature="query_database:users",
            estimated_tokens=150
        )
        # Safe to execute
    except AgentGuardrailException as e:
        print(f"Execution halted: {e}")
    ```

**Properties:**
- `current_step` — Current step count
- `accumulated_tokens` — Total tokens used so far
- `action_history` — List of all actions taken

#### 2. `StatefulReActAgent`
Implements the ReAct loop with explicit state management and guardrail checking.

**Constructor:**
```python
agent = StatefulReActAgent(guardrails=ExecutionGuardrails())
```

**Methods:**

1. **`log_state(role: str, content: str)`**
   - Appends message turn to agent's working memory
   - Roles: `"user"`, `"observation"`, `"reasoning"`
   - Use when: Recording each decision or observation
   - **Example:**
     ```python
     agent.log_state("user", "Fix the failing test")
     agent.log_state("reasoning", "I need to run tests first")
     agent.log_state("observation", "Tests show 3 failures")
     ```

2. **`run_loop(user_goal: str)`**
   - Executes the full agent reasoning and action loop
   - Implements Think → Act → Observe cycle with guardrails
   - Logs each step and catches execution guardrail exceptions
   - Use when: Running complete autonomous tasks
   - **Example:**
     ```python
     agent.run_loop("Debug and fix authentication timeout")
     # Output shows: Thinking, Action, Observation, Success or Guardrail Trigger
     ```

**Usage Example:**
```python
from resource_agent_loop import ExecutionGuardrails, StatefulReActAgent

# Setup guardrails
guardrails = ExecutionGuardrails(
    max_steps=5,           # Max 5 iterations
    max_token_budget=2000  # Max 2000 tokens
)

# Create agent
agent = StatefulReActAgent(guardrails=guardrails)

# Run autonomous task
try:
    agent.run_loop("Analyze failed API tests and apply fixes")
except Exception as e:
    print(f"Task failed: {e}")

# Access agent's execution state
for turn in agent.state:
    print(f"{turn['role']}: {turn['content'][:100]}...")
```

**Agent Execution Flow:**
```
Step 1: THINK (Reasoning)
  "I need to run the test suite to understand failures"
  [GuardrailCheck: step=1, tokens=350 ✓]
  
Step 2: ACT (Tool Execution)
  Execute: run_tests("test_auth.py")
  Result: "4 passed, 1 failed (test_auth_timeout)"
  [GuardrailCheck: step=2, tokens=400 ✓]
  
Step 3: OBSERVE (Process Result)
  "Tests show timeout issue. I should fix auth.py"
  
Step 4: ACT (Apply Fix)
  Execute: fix_code("auth.py")
  Result: "Successfully applied patch. Auth timeout updated to 30s."
  [GuardrailCheck: step=3, tokens=300 ✓]
  
Step 5: VERIFY (Re-test)
  Execute: run_tests("test_auth.py")
  Result: "4 passed, 0 failed ✓"
  [GuardrailCheck: step=4, tokens=300 ✓]
  
[Execution Success] Goal achieved within guardrail constraints
```

**Guardrail Examples:**

**Example 1: Max Steps Exceeded**
```python
guardrails = ExecutionGuardrails(max_steps=2)
# After 2 steps, next verify_step() raises:
# "[GUARDRAIL TRIGGERED] Max step limit reached (2 steps). Terminating execution loop."
```

**Example 2: Token Budget Exceeded**
```python
guardrails = ExecutionGuardrails(max_token_budget=500)
guardrails.verify_step("action_1", 300)  # OK
guardrails.verify_step("action_2", 300)  # Raises:
# "[GUARDRAIL TRIGGERED] Token budget exceeded (600 / 500 tokens)."
```

**Example 3: Stagnation Detection**
```python
guardrails = ExecutionGuardrails(max_steps=5)
guardrails.verify_step("query_db:users", 100)  # OK
guardrails.verify_step("query_db:users", 100)  # Raises:
# "[GUARDRAIL TRIGGERED] Stagnation detected. Action 'query_db:users' repeated multiple times."
```

**Design Patterns Demonstrated:**
- **Bounded Autonomy** — Execution limits prevent runaway loops
- **Stateful Reasoning** — Explicit state tracking for transparency
- **Think → Act → Observe** — ReAct loop with guardrails
- **Observable Execution** — Full action history logged for debugging
- **Graceful Fallback** — Guardrail triggers escalate to human-in-the-loop

**Run Sample:**
```bash
python resource_agent_loop.py
```

This demonstrates normal execution, stagnation detection, and token budget enforcement.

---

## Shared Resources

All lessons leverage utilities in `shared/`:

- **`memory.py`** — 4-layer memory system (short-term, long-term, episodic, semantic)
- **`tool_registry.py`** — Dynamic tool registration and execution
- **`agent.py`** — Agent class with memory integration
- **`workflow.py`** — Multi-step workflow orchestration and scheduling
- **`multi_agent.py`** — Multi-agent system with coordination

---

## Setup & Dependencies

### First-Time Setup
```bash
rm -rf .venv
./setup.sh
source .venv/bin/activate

pip install -r requirements-module-06.txt
```

**Dependencies:**
- Base: No external requirements (uses built-in Python libraries)
- Optional: `schedule` library for advanced workflow scheduling

### API Keys
```bash
# Optional: OpenRouter for LLM-powered agents (lessons 6.2-6.6)
export OPENROUTER_API_KEY='your-key-here'

# OpenRouter signup: https://openrouter.ai
```

### Verify Installation
```bash
# Test resource script
python resource_agent_loop.py

# Run a lesson
python lesson-02-agent-memory-systems.py
```
