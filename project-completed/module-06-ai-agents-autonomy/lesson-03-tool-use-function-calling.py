"""
Lesson 6.3: Tool Use & Function Calling (REFACTORED)

This lesson teaches agents how to discover, select, and invoke tools from
a toolkit (like Module 5's MCP tools), guided by LLM reasoning and memory.

Each pattern demonstrates a distinct tool-use capability with comparison:
- WITHOUT tools: LLM can only reason, can't act
- WITH tools: LLM can select and execute tools based on reasoning

Students learn: Tools extend agents from thinkers to doers.

Run: python lesson-03-tool-use-function-calling.py
Requires: export OPENROUTER_API_KEY='your-key-here'
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional, Any

sys.path.insert(0, str(Path(__file__).parent))
from shared.agent import Agent

# DEBUG: Set to True to see ORAR (Observe-Reason-Act-Reflect) cycle output
DEBUG = True



def clear_screen():
    """Clear terminal screen."""
    os.system("clear" if os.name == "posix" else "cls")


def validate_api_key():
    """Check if API key is set."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("\n" + "=" * 70)
        print("❌ OPENROUTER_API_KEY not set")
        print("=" * 70)
        print("\nSetup: export OPENROUTER_API_KEY='your-key-here'")
        print("Get key: https://openrouter.ai\n" + "=" * 70)
        sys.exit(1)


def show_menu():
    """Display main menu."""
    clear_screen()
    print("\n" + "=" * 70)
    print("LESSON 6.3: TOOL USE & FUNCTION CALLING")
    print("=" * 70)
    print()
    print("  Each pattern shows: Agent reasoning WITHOUT tools vs WITH tools\n")
    print("    [1] PATTERN: Tool Discovery & Schema")
    print("        → Agent learns available tools\n")
    print("    [2] PATTERN: Tool Selection via LLM")
    print("        → Agent chooses tools based on task\n")
    print("    [3] PATTERN: Sequential Tool Execution")
    print("        → Agent chains multiple tools\n")
    print("    [4] PATTERN: Tool Memory Integration")
    print("        → Agent learns from tool results\n")
    print("    [Q] Quit\n")
    print("=" * 70)


# Sample toolkit from Module 5
class SimpleToolkit:
    """Simulates MCP toolkit with sample tools."""
    
    def __init__(self):
        self.tools = {
            "search_knowledge": {
                "name": "search_knowledge",
                "description": "Search knowledge base for relevant documents",
                "args": ["query"],
            },
            "analyze_sentiment": {
                "name": "analyze_sentiment",
                "description": "Analyze sentiment and urgency of text",
                "args": ["text"],
            },
            "extract_action_items": {
                "name": "extract_action_items",
                "description": "Extract TODO items from text",
                "args": ["body"],
            },
            "categorize_email": {
                "name": "categorize_email",
                "description": "Classify email by type (support, billing, etc)",
                "args": ["subject", "body"],
            },
        }
    
    def get_tools(self) -> List[Dict]:
        """Get available tools."""
        return list(self.tools.values())
    
    def call_tool(self, tool_name: str, **kwargs) -> str:
        """Simulate tool execution."""
        if tool_name == "search_knowledge":
            return f"Found docs on: {kwargs.get('query', 'topic')}"
        elif tool_name == "analyze_sentiment":
            text = kwargs.get('text', '')[:50]
            return f"Sentiment: POSITIVE | Urgency: HIGH"
        elif tool_name == "extract_action_items":
            return "Action items: 1) Fix bug 2) Update docs 3) Deploy"
        elif tool_name == "categorize_email":
            return "Category: SUPPORT | Priority: HIGH"
        return "Tool not found"


def demo_tool_discovery():
    """PATTERN 1: Tool Discovery - Agent learns what tools are available."""
    clear_screen()
    print("\n" + "=" * 70)
    print("PATTERN 1: TOOL DISCOVERY - Agent Learns Available Tools")
    print("=" * 70)
    
    print("\n📖 Concept:")
    print("  Agents discover and understand tools before using them.")
    print("  Without tools: Agent is limited to reasoning only.")
    print("  With tools: Agent has capabilities toolkit.\n")
    
    toolkit = SimpleToolkit()
    
    print("Available tools in toolkit:")
    print("-" * 70)
    for tool in toolkit.get_tools():
        print(f"  • {tool['name']}")
        print(f"    Description: {tool['description']}")
    
    input("\nPress [ENTER] to see WITHOUT tool awareness...")
    
    # WITHOUT tools
    print("\n" + "-" * 70)
    print("WITHOUT TOOL AWARENESS:")
    print("-" * 70)
    agent_no_tools = Agent(name="AgentNoTools", use_memory=False)
    
    query = "What can you do for me?"
    print(f"\nQuery: {query}")
    response = agent_no_tools.reason_with_memory(query, debug=DEBUG)
    print(f"Response: {response[:200]}...")
    print("\n⚠️  Agent limited to reasoning only.")
    
    input("\nPress [ENTER] to see WITH tool awareness...")
    
    # WITH tools
    print("\n" + "-" * 70)
    print("WITH TOOL AWARENESS:")
    print("-" * 70)
    agent_with_tools = Agent(name="AgentWithTools", use_memory=True)
    
    # Make agent aware of tools
    toolkit_desc = "Available tools:\n"
    for tool in toolkit.get_tools():
        toolkit_desc += f"  - {tool['name']}: {tool['description']}\n"
    
    query_with_tools = f"{toolkit_desc}\nUser asks: {query}"
    print(f"\nQuery: {query}")
    response = agent_with_tools.reason_with_memory(
        query_with_tools,
        include_context=True,
        debug=DEBUG
    )
    print(f"Response: {response[:250]}...")
    print("\n✅ Agent aware of: search_knowledge, analyze_sentiment, extract_action_items, categorize_email")
    
    print("\n" + "-" * 70)
    input("Press [ENTER] to return to menu...")


def demo_tool_selection():
    """PATTERN 2: Tool Selection - Agent chooses right tools for task."""
    clear_screen()
    print("\n" + "=" * 70)
    print("PATTERN 2: TOOL SELECTION - Agent Chooses Tools for Task")
    print("=" * 70)
    
    print("\n📖 Concept:")
    print("  Agent selects appropriate tools based on task requirements.")
    print("  Without tools: Agent can only explain (no action).")
    print("  With tools: Agent DECIDES which tools to use & EXECUTES them.\n")
    
    toolkit = SimpleToolkit()
    email_body = """
Subject: Urgent Issue with Order #12345

Dear Customer Support,

I placed an order for a laptop (Order #12345) last week, and I am experiencing 
critical issues. The laptop keeps freezing randomly, making it impossible to work. 
I need:
1. A replacement ASAP
2. Refund if replacement unavailable
3. Compensation for lost work time

This is urgent - I have a deadline tomorrow.

Regards,
John"""
    
    task = f"Handle this customer email: {email_body}"
    
    print(f"📧 Customer Email (first 100 chars): {email_body[:100]}...\n")
    
    input("Press [ENTER] to see WITHOUT tool selection (explanation only)...")
    
    # WITHOUT tools - Agent just explains
    print("\n" + "-" * 70)
    print("❌ WITHOUT TOOL SELECTION (Agent can only explain):")
    print("-" * 70)
    agent_no_tools = Agent(name="AgentNoToolSel", use_memory=False)
    
    print(f"\nQuery: \"What should I do with this customer email?\"\n")
    print("Agent's Reasoning:")
    response_no_tools = agent_no_tools.reason_with_memory(task, debug=DEBUG)
    print(f"\n{response_no_tools}")
    print("\n⚠️  Agent EXPLAINED what should be done, but CANNOT ACT.")
    
    input("\nPress [ENTER] to see WITH tool selection (with execution)...")
    
    # WITH tools - Agent reasons about tools THEN calls them
    print("\n" + "-" * 70)
    print("✅ WITH TOOL SELECTION (Agent reasons, selects, and executes):")
    print("-" * 70)
    agent_with_tools = Agent(name="AgentWithToolSel", use_memory=True)
    
    print(f"\nAvailable tools: {list(toolkit.tools.keys())}\n")
    
    # Step 1: Agent reasons about which tools to use
    tool_selection_prompt = f"""Given this customer email, which tools should we use?
Email: {email_body[:300]}...

Available tools:
- search_knowledge: Search knowledge base for relevant documents
- analyze_sentiment: Determine emotional tone and urgency
- extract_action_items: Extract what customer is asking for
- categorize_email: Classify email type/priority

Respond with: (1) which tools to use, (2) why."""
    
    print("Step 1: Agent decides which tools to use:\n")
    tool_decision = agent_with_tools.reason_with_memory(tool_selection_prompt, debug=DEBUG)
    print(f"\n{tool_decision}\n")
    
    # Step 2: Agent calls tools
    print("Step 2: Executing selected tools:\n")
    print(f"  → analyze_sentiment(email_body): {toolkit.call_tool('analyze_sentiment', text=email_body)}")
    print(f"  → extract_action_items(email_body): {toolkit.call_tool('extract_action_items', body=email_body)}")
    print(f"  → categorize_email(email_body): {toolkit.call_tool('categorize_email', email=email_body)}")
    
    # Step 3: Agent synthesizes results
    synthesis_prompt = f"""Based on tool results:
- Sentiment: URGENT + FRUSTRATED
- Action items: Replacement, Refund, Compensation
- Category: HIGH-PRIORITY COMPLAINT

What's our response plan?"""
    
    print("\nStep 3: Agent synthesizes results:\n")
    response_with_tools = agent_with_tools.reason_with_memory(
        synthesis_prompt,
        include_context=True,
        debug=DEBUG
    )
    print(f"\n{response_with_tools}")
    print("\n✅ Agent SELECTED tools, EXECUTED them, SYNTHESIZED results.")
    
    print("\n" + "-" * 70)
    input("Press [ENTER] to return to menu...")


def demo_sequential_execution():
    """PATTERN 3: Sequential Tool Execution - Chaining tools."""
    clear_screen()
    print("\n" + "=" * 70)
    print("PATTERN 3: SEQUENTIAL EXECUTION - Chaining Multiple Tools")
    print("=" * 70)
    
    print("\n📖 Concept:")
    print("  Complex tasks require chaining multiple tools.")
    print("  Without tools: Agent can't execute workflows.")
    print("  With tools: Agent orchestrates multi-step processes.\n")
    
    toolkit = SimpleToolkit()
    sample_email = "Subject: URGENT: System Down\nBody: Please fix immediately. Customers affected."
    
    print(f"Email: {sample_email}\n")
    
    input("Press [ENTER] to see WITHOUT tool chaining...")
    
    # WITHOUT tools
    print("\n" + "-" * 70)
    print("WITHOUT TOOL CHAINING:")
    print("-" * 70)
    print(f"\nTask: Process email and generate response")
    response = "I would need to analyze the sentiment, extract action items, and search for similar solutions."
    print(f"Agent: {response}")
    print("\n⚠️  Agent can only describe what should be done.")
    
    input("\nPress [ENTER] to see WITH tool chaining...")
    
    # WITH tools
    print("\n" + "-" * 70)
    print("WITH TOOL CHAINING:")
    print("-" * 70)
    agent_with_tools = Agent(name="AgentChaining", use_memory=True)
    
    print(f"\nExecuting tool chain:")
    print(f"  Step 1: categorize_email() → {toolkit.call_tool('categorize_email', subject='URGENT', body=sample_email)}")
    print(f"  Step 2: analyze_sentiment() → {toolkit.call_tool('analyze_sentiment', text=sample_email)}")
    print(f"  Step 3: extract_action_items() → {toolkit.call_tool('extract_action_items', body=sample_email)}")
    print(f"  Step 4: search_knowledge() → {toolkit.call_tool('search_knowledge', query='system outage recovery')}")
    
    # Record in episodic memory
    agent_with_tools.memory.episodic.record_episode(
        agent_with_tools.name,
        "tool_workflow",
        {"description": "Email processing workflow", "tools_used": 4, "outcome": "resolved"}
    )
    
    print(f"\n✅ Executed 4 tools in sequence")
    print(f"✅ Recorded workflow in episodic memory")
    
    print("\n" + "-" * 70)
    input("Press [ENTER] to return to menu...")


def demo_memory_integration():
    """PATTERN 4: Tool Memory Integration - Learning from tool calls."""
    clear_screen()
    print("\n" + "=" * 70)
    print("PATTERN 4: MEMORY INTEGRATION - Learning from Tool Results")
    print("=" * 70)
    
    print("\n📖 Concept:")
    print("  Agents store tool results in memory to improve future decisions.")
    print("  Without memory: Agent repeats same tool calls.")
    print("  With memory: Agent learns optimal tool sequences.\n")
    
    toolkit = SimpleToolkit()
    
    input("Press [ENTER] to simulate WITHOUT memory...")
    
    # WITHOUT memory
    print("\n" + "-" * 70)
    print("WITHOUT MEMORY:")
    print("-" * 70)
    agent_no_mem = Agent(name="AgentNoMemTool", use_memory=False)
    
    print(f"\nRun 1: Process similar email")
    print(f"  Tools used: search_knowledge, analyze_sentiment, extract_action_items")
    
    print(f"\nRun 2: Process similar email (different data)")
    print(f"  Tools used: search_knowledge, analyze_sentiment, extract_action_items (REPEATED)")
    print("\n⚠️  Agent doesn't remember the successful workflow.")
    
    input("\nPress [ENTER] to see WITH memory...")
    
    # WITH memory
    print("\n" + "-" * 70)
    print("WITH MEMORY:")
    print("-" * 70)
    agent_with_mem = Agent(name="AgentMemTool", use_memory=True)
    
    print(f"\nRun 1: Process email")
    workflow_1 = {
        "description": "Email handling workflow",
        "tools": ["analyze_sentiment", "extract_action_items"],
        "success": True
    }
    print(f"  Tools: {', '.join(workflow_1['tools'])}")
    agent_with_mem.memory.episodic.record_episode(
        agent_with_mem.name,
        "tool_workflow",
        workflow_1
    )
    print(f"  ✓ Stored workflow in memory")
    
    print(f"\nRun 2: Process similar email")
    print(f"  Agent recalls: 'Last time, these 2 tools worked'")
    print(f"  Tools used: analyze_sentiment, extract_action_items (OPTIMIZED)")
    
    calls = agent_with_mem.memory.tool_calls.get_calls(agent_with_mem.name)
    success_rate = agent_with_mem.memory.tool_calls.get_success_rate(agent_with_mem.name)
    print(f"\n✅ Tool call history: {len(calls)} calls")
    print(f"✅ Success rate: {success_rate*100:.0f}%")
    print(f"✅ Agent learns optimal tool sequences")
    
    print("\n" + "-" * 70)
    input("Press [ENTER] to return to menu...")


def main():
    """Main menu loop."""
    validate_api_key()
    
    patterns = {
        "1": ("Tool Discovery", demo_tool_discovery),
        "2": ("Tool Selection", demo_tool_selection),
        "3": ("Sequential Execution", demo_sequential_execution),
        "4": ("Memory Integration", demo_memory_integration),
    }
    
    while True:
        show_menu()
        choice = input("Enter choice: ").strip().upper()
        
        if choice == "Q":
            print("\n✅ Goodbye!\n")
            break
        
        if choice in patterns:
            try:
                patterns[choice][1]()
            except Exception as e:
                print(f"\n❌ Error: {e}")
                import traceback
                traceback.print_exc()
                input("Press [ENTER]...")
        else:
            print(f"\n❌ Invalid choice.")
            input("Press [ENTER]...")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("MODULE 6, LESSON 6.3: TOOL USE & FUNCTION CALLING")
    print("=" * 70)
    print("\nAgents combine memory with tool execution for autonomous action.")
    print("Each pattern shows: WITHOUT tools vs WITH tools\n")
    input("Press [ENTER] to start...\n")
    
    main()
