"""
Lesson 6.3 TODO: Tool Use & Function Calling

This lesson teaches agents how to discover, select, and invoke tools from an
external toolkit (like the MCP Toolkit Server from Module 5). Agents use their
memory to reason about which tools to call and when.

Building on Lesson 6.2 (Agent Memory Systems), you will add:
  - Tool discovery: Agents learn what tools are available
  - Tool selection: Agents choose tools based on user input + memory context
  - Tool invocation: Agents call tools, capture results, store in memory
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

PART 1: Tool Representation & Toolkit Setup
PART 2: Agent Enhancement for Tool Calling
PART 3: Core Template Method & Demonstrations

REFERENCE FILES:
  - Completed: project-completed/module-06-ai-agents-autonomy/lesson-03-tool-use-function-calling.py
  - Module 5 Toolkit: project-completed/module-05-developing-mcp-servers-tooling/lesson-06-mcp-toolkit-server.py
  - Agent Memory: project-completed/module-06-ai-agents-autonomy/lesson-02-agent-memory-systems.py
  - Curriculum: docs/curriculum_v1.md (Module 6 sections)
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
from dataclasses import dataclass


# ============================================================================
# PHASE 1: Tool Representation & Toolkit
# ============================================================================

@dataclass
class ToolSpec:
    """TODO: Represent an available tool that an agent can call.
    
    Should include:
    - name: Tool identifier
    - description: What the tool does
    - category: Which category it belongs to (knowledge, email, system)
    - input_schema: JSON schema describing tool inputs
    
    Methods needed:
    - to_dict(): Serialize for discovery
    """
    pass


class MCPToolkit:
    """TODO: Represent an MCP Toolkit Server with discoverable tools.
    
    Key responsibilities:
    - Store registered tools
    - Organize tools by category
    - Support tool discovery
    - Simulate tool invocation
    
    Methods needed:
    - __init__(name): Initialize toolkit
    - register_tool(tool): Add tool to toolkit
    - get_tools_by_category(category): Retrieve tools by category
    - get_tool(name): Get specific tool
    - list_tools(): Return all tools for discovery
    - invoke_tool(tool_name, args): Execute tool and return results
    
    Implementation hint:
    - For each tool, simulate realistic behavior in invoke_tool()
    - Example: search_knowledge returns mock documents with snippets
    - Example: analyze_sentiment returns sentiment + confidence
    - Use the completed version as reference for realistic responses
    """
    pass


def create_default_toolkit() -> MCPToolkit:
    """TODO: Create and populate default toolkit with tools from Module 5.
    
    Should register 8 tools across 3 categories:
    
    KNOWLEDGE (2):
      - search_knowledge: Search company knowledge base
      - get_document: Retrieve specific document
    
    EMAIL (4):
      - parse_email: Parse and structure email
      - analyze_sentiment: Detect email sentiment/urgency
      - extract_action_items: Find TODOs in email
      - extract_keywords: Extract topics from text
    
    SYSTEM (2):
      - list_tools: List available tools
      - get_toolkit_info: Get toolkit metadata
    
    Implementation hint:
    - Create ToolSpec for each tool with proper input_schema
    - Register each with appropriate category
    - Return fully configured toolkit
    
    Reference the completed version for exact tool specs.
    """
    pass


# ============================================================================
# PHASE 2: Agent Enhancement for Tool Calling
# ============================================================================

class ToolAwareAgent:
    """TODO: Agent enhanced with tool discovery and calling capability.
    
    Wraps a base Agent and adds:
    - Tool discovery
    - Tool selection
    - Tool invocation
    - Tool result storage in memory
    
    Attributes needed:
    - name: Agent name
    - toolkit: MCPToolkit instance
    - tools_cache: Dict of discovered tools
    - tool_call_history: List of tool invocations
    - tool_selection_rules: Dict mapping keywords to tools
    
    Methods needed:
    - discover_tools() -> List[Dict]: List available tools
    - select_tools(user_input) -> List[str]: Choose tools for request
    - call_tool(tool_name, args) -> Dict: Execute single tool
    - call_tools_in_sequence(tools, args_list) -> List[Dict]: Execute multiple tools
    - get_tool_call_history_summary() -> str: Summarize recent calls
    
    Implementation hints:
    - Tool selection can use keyword matching against rules
    - Example rule: if "email" in query, select email tools
    - Tool invocation records timestamp, args, result, success status
    - Tool call history enables learning from past patterns
    """
    pass


# ============================================================================
# PHASE 3: Core Template Method
# ============================================================================

def create_agent_with_tools(
    agent_name: str,
    toolkit: Optional[MCPToolkit] = None,
    tool_selection_strategy: str = "keyword_match",
) -> ToolAwareAgent:
    """TODO: Core template method - Create agent with tool-calling capability.
    
    This is the production-ready pattern for building agents that can discover
    and invoke tools from external toolkits (like MCP servers).
    
    Args:
        agent_name: Name of the agent
        toolkit: MCPToolkit instance (create default if None)
        tool_selection_strategy: Strategy for choosing tools
    
    Returns:
        ToolAwareAgent: Agent ready to discover, select, and call tools
    
    Implementation steps:
    1. Create toolkit if not provided
    2. Create ToolAwareAgent instance
    3. Discover available tools
    4. Print initialization summary showing toolkit and tools
    5. Return configured agent
    
    Expected output:
    - Agent name and toolkit name
    - Number of tools discovered
    - Tools organized by category
    - Ready status
    """
    pass


# ============================================================================
# PHASE 4: Demonstrations (6 Total)
# ============================================================================

def demo_tool_discovery():
    """TODO: Demo 1 - Agent discovers available tools from toolkit.
    
    Show:
    - Create agent with create_agent_with_tools()
    - Call discover_tools()
    - Display tools organized by category
    - Show each tool name + description
    """
    pass


def demo_tool_selection():
    """TODO: Demo 2 - Agent selects appropriate tools based on user request.
    
    Show:
    - Test 3 different user queries
    - For each query, call select_tools()
    - Display which tools were selected
    - Explain why those tools were chosen
    
    Example queries:
    - "I need to review overdue accounts and their email history"
    - "What actions should we take based on recent communications?"
    - "Show me relevant company policies"
    """
    pass


def demo_single_tool_invocation():
    """TODO: Demo 3 - Agent calls a single tool and processes result.
    
    Show:
    - Call search_knowledge tool
    - Display result status (success/failure)
    - Show tool results (e.g., documents found)
    - Display tool call history count
    """
    pass


def demo_sequential_workflow():
    """TODO: Demo 4 - Agent chains multiple tools in sequence.
    
    Demonstrate realistic workflow:
    1. Search knowledge for account information
    2. Parse customer email
    3. Extract action items from email
    
    Show:
    - Each step and what it returns
    - Total tools called
    - Tools used in sequence
    
    Scenario: Review account ACC-2024-156 and generate action plan
    """
    pass


def demo_error_handling():
    """TODO: Demo 5 - Agent handles tool failures gracefully.
    
    Show:
    - Attempt to call non-existent tool
    - Display error result
    - Show tool call history recorded failure
    - Explain graceful degradation strategy
    """
    pass


def demo_memory_integration():
    """TODO: Demo 6 - Tool results stored in agent memory for learning.
    
    Show:
    - Execute 3-step workflow
    - Store tool invocations as episode in memory
    - Display tool call history
    - Explain how agent learns from tool outcomes
    
    Connection to Lesson 6.2:
    - Tool results → episodic memory (interaction history)
    - Tool patterns → semantic memory (which tools work together)
    - Recent calls → short-term memory (current context)
    """
    pass


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # TODO: Print lesson title and description
    # TODO: Call all 6 demonstrations in order
    # TODO: Print separator lines between demos
    # TODO: Print completion summary with key takeaways
    # TODO: Reference next lessons (6.4, 6.5, 6.6)
    pass
