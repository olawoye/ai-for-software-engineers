"""
Lesson 6.3: Tool Use & Function Calling

This lesson teaches agents how to discover, select, and invoke tools from an
external toolkit (like the MCP Toolkit Server from Module 5). Agents use their
memory to reason about which tools to call and when.

Building on Lesson 6.2 (Agent Memory Systems), this lesson adds:
  - Tool discovery: Agents learn what tools are available
  - Tool selection: Agents choose tools based on user input + memory context
  - Tool invocation: Agents call tools, capture results, store in episodic memory
  - Error handling: Agents respond gracefully to tool failures

Business Scenario:
  "A sales manager agent needs to identify overdue accounts, retrieve CRM data,
   analyze customer emails, and generate a recovery action plan. The agent
   discovers available tools, decides which ones to use based on the request,
   executes them in sequence, and remembers successful tool workflows for future use."

Learning Goals:
  1. Understand how agents discover and select tools
  2. Implement tool invocation patterns
  3. Integrate tool results with agent memory (episodic + semantic)
  4. Handle tool failures gracefully
  5. Create reusable tool-calling patterns
  6. Prepare for autonomous workflows (Lesson 6.5)

Key Concept:
  Tool calling is not just execution—it's a decision process guided by memory.
  - Semantic memory: "Tool A is for knowledge queries"
  - Episodic memory: "Last time we used Tools B+C together, it worked"
  - Short-term memory: "Current user asked for account status + emails"
  → Agent reasons: Use Tool A (knowledge) + Tool B (email analysis)
  
Integration with Module 5:
  The MCP Toolkit Server (lesson-06-mcp-toolkit-server.py) provides 10 tools:
    Knowledge: search_knowledge, get_document
    Email: parse_email, categorize_email, analyze_sentiment, extract_action_items, extract_keywords
    System: list_tools, get_toolkit_info
  
  This lesson demonstrates how agents select and invoke these tools.
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass


# ============================================================================
# PHASE 1: Tool Representation & Toolkit
# ============================================================================

@dataclass
class ToolSpec:
    """Represents an available tool that an agent can call."""
    name: str
    description: str
    category: str  # "knowledge", "email", "system"
    input_schema: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize tool spec for discovery."""
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "input_schema": self.input_schema,
        }


class MCPToolkit:
    """Represents an MCP Toolkit Server with discoverable tools.
    
    In production, this would connect to an actual MCP server.
    For this lesson, it simulates the toolkit from Lesson 5.6.
    """
    
    def __init__(self, name: str = "DefaultToolkit"):
        self.name = name
        self.tools: Dict[str, ToolSpec] = {}
        self.categories: Dict[str, List[str]] = {
            "knowledge": [],
            "email": [],
            "system": [],
        }
    
    def register_tool(self, tool: ToolSpec):
        """Register a tool in the toolkit."""
        self.tools[tool.name] = tool
        if tool.category not in self.categories:
            self.categories[tool.category] = []
        self.categories[tool.category].append(tool.name)
    
    def get_tools_by_category(self, category: str) -> List[ToolSpec]:
        """Get all tools in a category."""
        tool_names = self.categories.get(category, [])
        return [self.tools[name] for name in tool_names]
    
    def get_tool(self, name: str) -> Optional[ToolSpec]:
        """Get a specific tool by name."""
        return self.tools.get(name)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools (for agent discovery)."""
        return [tool.to_dict() for tool in self.tools.values()]
    
    def invoke_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate tool invocation and return results.
        
        In production, this would call the actual MCP server.
        For this lesson, we simulate realistic results.
        """
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found in toolkit",
            }
        
        tool = self.tools[tool_name]
        
        # Simulate different tool behaviors
        if tool_name == "search_knowledge":
            return {
                "success": True,
                "results": [
                    {"document": "account_policy.md", "snippet": "Accounts 30+ days overdue should be escalated to recovery team"},
                    {"document": "customer_data.md", "snippet": "Customer ID ACC-2024-156 - $5,200 balance, invoice due 2026-06-28"},
                ],
                "query": args.get("query", ""),
            }
        
        elif tool_name == "get_document":
            return {
                "success": True,
                "document": args.get("filename", "unknown.md"),
                "content": "# Sample Document\n\nThis is a sample document retrieved from knowledge base.\n\nKey info: Company policies and customer data stored here.",
            }
        
        elif tool_name == "parse_email":
            return {
                "success": True,
                "parsed_email": {
                    "from": args.get("sender", ""),
                    "subject": args.get("subject", ""),
                    "body_length": len(args.get("body", "")),
                    "has_attachments": False,
                },
            }
        
        elif tool_name == "analyze_sentiment":
            text = args.get("text", "").lower()
            if "urgent" in text or "asap" in text:
                sentiment = "urgent"
            elif "thank" in text or "appreciate" in text:
                sentiment = "positive"
            else:
                sentiment = "neutral"
            return {
                "success": True,
                "sentiment": sentiment,
                "confidence": 0.85,
                "text_length": len(args.get("text", "")),
            }
        
        elif tool_name == "extract_action_items":
            return {
                "success": True,
                "action_items": [
                    "Review account status",
                    "Prepare recovery plan",
                    "Follow up with customer",
                ],
                "count": 3,
            }
        
        elif tool_name == "extract_keywords":
            return {
                "success": True,
                "keywords": ["payment", "overdue", "account", "recovery", "urgent"],
                "top_k": args.get("top_k", 5),
            }
        
        elif tool_name == "list_tools":
            return {
                "success": True,
                "tools": self.list_tools(),
                "total": len(self.tools),
            }
        
        elif tool_name == "get_toolkit_info":
            return {
                "success": True,
                "toolkit_name": self.name,
                "total_tools": len(self.tools),
                "categories": {cat: len(tools) for cat, tools in self.categories.items()},
            }
        
        else:
            return {
                "success": True,
                "tool": tool_name,
                "args": args,
                "result": f"Tool {tool_name} executed successfully",
            }


def create_default_toolkit() -> MCPToolkit:
    """Create a toolkit with tools from Module 5 (Lesson 5.6)."""
    toolkit = MCPToolkit(name="SalesOperationsToolkit")
    
    # Knowledge tools
    toolkit.register_tool(ToolSpec(
        name="search_knowledge",
        description="Search company knowledge base for relevant documents",
        category="knowledge",
        input_schema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
            },
            "required": ["query"]
        }
    ))
    
    toolkit.register_tool(ToolSpec(
        name="get_document",
        description="Retrieve a specific document from the knowledge base",
        category="knowledge",
        input_schema={
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Document filename"},
            },
            "required": ["filename"]
        }
    ))
    
    # Email tools
    toolkit.register_tool(ToolSpec(
        name="parse_email",
        description="Parse and structure an email message",
        category="email",
        input_schema={
            "type": "object",
            "properties": {
                "sender": {"type": "string"},
                "subject": {"type": "string"},
                "body": {"type": "string"}
            },
            "required": ["sender", "subject", "body"]
        }
    ))
    
    toolkit.register_tool(ToolSpec(
        name="analyze_sentiment",
        description="Detect sentiment and urgency level of email",
        category="email",
        input_schema={
            "type": "object",
            "properties": {
                "text": {"type": "string"}
            },
            "required": ["text"]
        }
    ))
    
    toolkit.register_tool(ToolSpec(
        name="extract_action_items",
        description="Identify TODO items and action requests in email",
        category="email",
        input_schema={
            "type": "object",
            "properties": {
                "body": {"type": "string"}
            },
            "required": ["body"]
        }
    ))
    
    toolkit.register_tool(ToolSpec(
        name="extract_keywords",
        description="Extract key topics and subjects from text",
        category="email",
        input_schema={
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "top_k": {"type": "integer", "default": 5}
            },
            "required": ["text"]
        }
    ))
    
    # System tools
    toolkit.register_tool(ToolSpec(
        name="list_tools",
        description="List all available tools in the toolkit",
        category="system",
        input_schema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ))
    
    toolkit.register_tool(ToolSpec(
        name="get_toolkit_info",
        description="Get information about the toolkit and its capabilities",
        category="system",
        input_schema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ))
    
    return toolkit


# ============================================================================
# PHASE 2: Agent Enhancement for Tool Calling
# ============================================================================

class ToolAwareAgent:
    """Agent enhanced with tool discovery and calling capability.
    
    Wraps a base Agent from Lesson 6.2 and adds:
      - Tool discovery
      - Tool selection
      - Tool invocation
      - Tool result storage in memory
    """
    
    def __init__(self, agent_name: str, toolkit: Optional[MCPToolkit] = None):
        self.name = agent_name
        self.toolkit = toolkit or create_default_toolkit()
        self.tools_cache: Dict[str, ToolSpec] = {}
        self.tool_call_history: List[Dict[str, Any]] = []
        self.tool_selection_rules: Dict[str, List[str]] = {
            "account": ["search_knowledge", "get_document"],
            "email": ["parse_email", "analyze_sentiment"],
            "action": ["extract_action_items"],
            "keyword": ["extract_keywords"],
        }
    
    def discover_tools(self) -> List[Dict[str, Any]]:
        """Discover available tools in the toolkit."""
        tools = self.toolkit.list_tools()
        for tool_dict in tools:
            self.tools_cache[tool_dict["name"]] = ToolSpec(
                name=tool_dict["name"],
                description=tool_dict["description"],
                category=tool_dict["category"],
                input_schema=tool_dict["input_schema"],
            )
        return tools
    
    def select_tools(self, user_input: str) -> List[str]:
        """Determine which tools to use based on user input.
        
        Uses keyword matching against selection rules.
        In production, this would use semantic matching or learned patterns.
        """
        selected = set()
        user_lower = user_input.lower()
        
        for keyword, tools in self.tool_selection_rules.items():
            if keyword in user_lower:
                selected.update(tools)
        
        # Default: include knowledge tools for most queries
        if not selected:
            selected.add("search_knowledge")
        
        return list(selected)
    
    def call_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool and record the invocation.
        
        Returns:
            Tool result dict with 'success', 'data', and any tool-specific fields
        """
        result = self.toolkit.invoke_tool(tool_name, args)
        
        # Record in history
        call_record = {
            "timestamp": datetime.now().isoformat(),
            "tool_name": tool_name,
            "args": args,
            "result": result,
            "success": result.get("success", False),
        }
        self.tool_call_history.append(call_record)
        
        return result
    
    def call_tools_in_sequence(
        self, 
        tools: List[str], 
        args_list: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Call multiple tools in sequence, passing results forward.
        
        Args:
            tools: List of tool names to call
            args_list: List of args dicts (one per tool)
        
        Returns:
            List of results from each tool call
        """
        results = []
        for tool_name, args in zip(tools, args_list):
            result = self.call_tool(tool_name, args)
            results.append(result)
        return results
    
    def get_tool_call_history_summary(self) -> str:
        """Get a summary of recent tool calls for memory integration."""
        if not self.tool_call_history:
            return "No tools called yet"
        
        summary = f"Tool call history ({len(self.tool_call_history)} total):\n"
        for call in self.tool_call_history[-5:]:  # Last 5
            status = "✓" if call["success"] else "✗"
            summary += f"  {status} {call['tool_name']} - {call['timestamp']}\n"
        return summary


# ============================================================================
# PHASE 3: Core Template Method
# ============================================================================

def create_agent_with_tools(
    agent_name: str,
    toolkit: Optional[MCPToolkit] = None,
    tool_selection_strategy: str = "keyword_match",
) -> ToolAwareAgent:
    """Core template method: Create agent with tool-calling capability.
    
    This is the production-ready pattern for building agents that can discover
    and invoke tools. Combines Lesson 6.2 (Agent memory) + Tool calling.
    
    Args:
        agent_name: Name of the agent
        toolkit: MCPToolkit instance (default: create new toolkit)
        tool_selection_strategy: How to choose tools ("keyword_match", "semantic_match", "rules")
    
    Returns:
        ToolAwareAgent: Agent ready to discover, select, and call tools
    
    Pattern:
        1. Create toolkit with available tools
        2. Create ToolAwareAgent instance
        3. Agent can now:
           - Discover available tools
           - Select tools based on user input
           - Call tools and store results
           - Learn from tool outcomes
    """
    if toolkit is None:
        toolkit = create_default_toolkit()
    
    agent = ToolAwareAgent(agent_name, toolkit)
    
    print(f"\n{'='*70}")
    print(f"AGENT WITH TOOLS INITIALIZATION")
    print(f"{'='*70}")
    print(f"✓ Creating agent: {agent_name}")
    print(f"✓ Toolkit: {toolkit.name}")
    print(f"✓ Strategy: {tool_selection_strategy}")
    
    # Discover tools
    tools = agent.discover_tools()
    print(f"\n✓ Tools discovered: {len(tools)}")
    for category in toolkit.categories:
        count = len(toolkit.categories[category])
        if count > 0:
            print(f"  - {category}: {count} tools")
    
    print(f"\n✓ Agent ready for tool-based reasoning")
    print(f"{'='*70}\n")
    
    return agent


# ============================================================================
# PHASE 4: Demonstrations (6 Total)
# ============================================================================

def demo_tool_discovery():
    """Demo 1: Agent discovers available tools from toolkit."""
    print("\n" + "="*70)
    print("DEMO 1: TOOL DISCOVERY")
    print("="*70)
    
    agent = create_agent_with_tools("DiscoveryAgent")
    
    print("\nAgent discovering tools from toolkit:")
    print("-" * 70)
    
    tools = agent.discover_tools()
    
    print(f"\nFound {len(tools)} tools organized by category:\n")
    
    for category in agent.toolkit.categories:
        category_tools = agent.toolkit.get_tools_by_category(category)
        if category_tools:
            print(f"  [{category.upper()}]")
            for tool in category_tools:
                print(f"    • {tool.name}: {tool.description}")
            print()
    
    print("✅ Tool discovery demonstration complete")


def demo_tool_selection():
    """Demo 2: Agent selects appropriate tools based on user request."""
    print("\n" + "="*70)
    print("DEMO 2: TOOL SELECTION")
    print("="*70)
    
    agent = create_agent_with_tools("SelectionAgent")
    
    test_queries = [
        "I need to review overdue accounts and their email history",
        "What actions should we take based on recent communications?",
        "Show me relevant company policies",
    ]
    
    print("\nAgent selecting tools for different queries:\n")
    
    for query in test_queries:
        selected_tools = agent.select_tools(query)
        print(f"Query: '{query}'")
        print(f"Selected tools:")
        for tool_name in selected_tools:
            tool = agent.toolkit.get_tool(tool_name)
            if tool:
                print(f"  ✓ {tool_name} ({tool.category})")
        print()
    
    print("✅ Tool selection demonstration complete")


def demo_single_tool_invocation():
    """Demo 3: Agent calls a single tool and processes the result."""
    print("\n" + "="*70)
    print("DEMO 3: SINGLE TOOL INVOCATION")
    print("="*70)
    
    agent = create_agent_with_tools("ExecutionAgent")
    
    print("\nAgent calling 'search_knowledge' tool:")
    print("-" * 70)
    
    result = agent.call_tool(
        "search_knowledge",
        {"query": "overdue accounts recovery policy"}
    )
    
    print(f"\nTool invocation result:")
    print(f"  Status: {'✓ Success' if result.get('success') else '✗ Failed'}")
    print(f"  Query: {result.get('query')}")
    print(f"  Results found: {len(result.get('results', []))}")
    
    if result.get('results'):
        print(f"\n  Search results:")
        for i, res in enumerate(result.get('results', []), 1):
            print(f"    {i}. {res.get('document')}")
            print(f"       → {res.get('snippet')}")
    
    print(f"\nTool call history: {len(agent.tool_call_history)} calls")
    print("✅ Single tool invocation demonstration complete")


def demo_sequential_workflow():
    """Demo 4: Agent chains multiple tools in sequence.
    
    Demonstrates a realistic workflow: Query knowledge base → Parse email → Extract actions
    """
    print("\n" + "="*70)
    print("DEMO 4: SEQUENTIAL TOOL WORKFLOW")
    print("="*70)
    
    agent = create_agent_with_tools("WorkflowAgent")
    
    print("\nAgent executing multi-step workflow for account review:")
    print("-" * 70)
    print("\nScenario: Review account ACC-2024-156 and generate action plan")
    
    # Step 1: Search knowledge for account info
    print("\n  [Step 1/3] Searching knowledge base for account information")
    result1 = agent.call_tool(
        "search_knowledge",
        {"query": "customer ACC-2024-156 balance overdue status"}
    )
    print(f"    Result: Found {len(result1.get('results', []))} relevant documents")
    
    # Step 2: Parse customer email
    print("\n  [Step 2/3] Parsing recent customer email")
    result2 = agent.call_tool(
        "parse_email",
        {
            "sender": "customer@example.com",
            "subject": "Payment delay - account ACC-2024-156",
            "body": "We are experiencing cash flow issues this month. Please allow 7 days extension."
        }
    )
    print(f"    Result: Email parsed successfully")
    
    # Step 3: Extract action items
    print("\n  [Step 3/3] Extracting action items from communication")
    result3 = agent.call_tool(
        "extract_action_items",
        {"body": "We are experiencing cash flow issues this month. Please allow 7 days extension."}
    )
    action_count = result3.get('count', 0)
    print(f"    Result: Identified {action_count} action items")
    
    print(f"\nWorkflow complete:")
    print(f"  Total tools called: {len(agent.tool_call_history)}")
    print(f"  Tools used: {', '.join([call['tool_name'] for call in agent.tool_call_history[-3:]])}")
    
    print("✅ Sequential workflow demonstration complete")


def demo_error_handling():
    """Demo 5: Agent handles tool failures gracefully."""
    print("\n" + "="*70)
    print("DEMO 5: ERROR HANDLING")
    print("="*70)
    
    agent = create_agent_with_tools("ErrorHandlingAgent")
    
    print("\nAgent attempting to call non-existent tool:")
    print("-" * 70)
    
    result = agent.call_tool(
        "nonexistent_tool",
        {"some_arg": "value"}
    )
    
    print(f"\nTool call result:")
    print(f"  Tool: nonexistent_tool")
    print(f"  Status: {'✓ Success' if result.get('success') else '✗ Failed'}")
    if not result.get('success'):
        print(f"  Error: {result.get('error')}")
    
    print(f"\nAgent response strategy:")
    print(f"  1. Detected tool call failure")
    print(f"  2. Logged error in tool_call_history")
    print(f"  3. Can suggest alternative tools")
    
    print(f"\nTool history shows:")
    last_call = agent.tool_call_history[-1]
    print(f"  - Attempted: {last_call['tool_name']}")
    print(f"  - Success: {last_call['success']}")
    print(f"  - Recorded: {last_call['timestamp']}")
    
    print("\n✅ Error handling demonstration complete")


def demo_memory_integration():
    """Demo 6: Tool results stored in agent memory for learning.
    
    This bridges Lesson 6.2 (Memory) with Lesson 6.3 (Tools).
    Agent stores tool invocations in episodic memory to learn from them.
    """
    print("\n" + "="*70)
    print("DEMO 6: MEMORY INTEGRATION")
    print("="*70)
    
    agent = create_agent_with_tools("MemoryAgent")
    
    print("\nAgent with integrated memory learning from tool calls:")
    print("-" * 70)
    
    # Execute a workflow
    print("\n[Workflow] Customer account review with tool integration:")
    
    print("\n  Step 1: Query knowledge base")
    agent.call_tool("search_knowledge", {"query": "account recovery procedures"})
    
    print("  Step 2: Analyze customer email")
    agent.call_tool("analyze_sentiment", {"text": "Please help! Our business is struggling."})
    
    print("  Step 3: Extract action items")
    agent.call_tool("extract_action_items", {"body": "Need payment plan, contact manager"})
    
    # Show what the agent learned
    print("\n[Memory Storage] Agent stores tool workflow in episodic memory:")
    print(f"  Type: Tool execution sequence")
    print(f"  Pattern: knowledge_search → sentiment_analysis → action_extraction")
    print(f"  Timestamp: {datetime.now().isoformat()}")
    print(f"  Success: All 3 tools executed successfully")
    
    print(f"\n[Tool Call History] Full record of tool invocations:")
    print(f"  Total calls: {len(agent.tool_call_history)}")
    
    for i, call in enumerate(agent.tool_call_history[-3:], 1):
        status = "✓" if call['success'] else "✗"
        print(f"  {i}. {status} {call['tool_name']} → {call['result'].get('success', False)}")
    
    print(f"\n[Future Learning] Agent can now:")
    print(f"  • Recognize similar requests")
    print(f"  • Reuse this successful tool sequence")
    print(f"  • Suggest same tools for similar queries")
    print(f"  • Track which tool combinations work best")
    
    print("\n✅ Memory integration demonstration complete")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("MODULE 6, LESSON 6.3: TOOL USE & FUNCTION CALLING")
    print("="*70)
    print("""
Agents learn to discover, select, and invoke tools from an external toolkit.
This bridges Lesson 6.2 (Agent Memory) with practical tool integration.

Business Scenario:
  Sales manager agent identifies overdue accounts, retrieves CRM data,
  analyzes customer emails, and generates recovery action plans.

Key Concepts:
  1. Tool discovery - agents learn what tools are available
  2. Tool selection - agents choose tools based on user input + memory
  3. Tool invocation - agents execute tools and capture results
  4. Memory integration - tool outcomes improve future decisions
    """)
    
    # Run all demonstrations
    demo_tool_discovery()
    demo_tool_selection()
    demo_single_tool_invocation()
    demo_sequential_workflow()
    demo_error_handling()
    demo_memory_integration()
    
    # Final summary
    print("\n" + "="*70)
    print("LESSON COMPLETE - AGENTS WITH TOOL CALLING READY")
    print("="*70)
    print("""
Key Takeaways:
  1. Agents discover and select tools based on context
  2. Tool results integrate with agent memory systems
  3. Tool call history enables learning and pattern recognition
  4. Error handling allows graceful degradation
  5. Tool orchestration prepares for autonomous workflows (Lesson 6.5)

Next Steps:
  Lesson 6.4: Chaining, CoT & Pipelines (talking head)
  Lesson 6.5: Autonomous Workflows (agents + tools + scheduling)
  Lesson 6.6: Multi-Agent Collaboration (coordinated agents with shared tools)
    """)
