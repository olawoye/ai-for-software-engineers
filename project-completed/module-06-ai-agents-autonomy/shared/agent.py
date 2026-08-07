"""
AI Agent with Integrated Memory and LLM Reasoning

Provides a practical agent implementation that uses real Claude/GPT APIs
for reasoning and decision-making, backed by persistent memory.

Students learn: how agents combine memory + LLM to make better decisions
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Optional, Any
import json
import importlib.util

# Load LLMClient from module-03
module_03_llm_path = Path(__file__).parent.parent.parent / "module-03-ai-developer-toolkit" / "shared" / "llm_client.py"
spec = importlib.util.spec_from_file_location("llm_client", module_03_llm_path)
llm_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(llm_module)
LLMClient = llm_module.LLMClient

from .memory import AgentMemoryManager


# ANSI color codes for debug output
CYAN_BG = "\033[106m"  # Bright cyan (light blue) background
DARK_TEXT = "\033[30m"  # Black text
RESET = "\033[0m"  # Reset to default


def print_debug_block(text: str):
    """Print debug output with light blue background for visual separation."""
    print(f"{CYAN_BG}{DARK_TEXT}{text}{RESET}")


class Agent:
    """AI Agent with integrated memory systems and LLM reasoning."""
    
    def __init__(
        self,
        name: str,
        api_key: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
        use_memory: bool = True,
        memory_dir: str = "./agent_memory"
    ):
        """Initialize an agent.
        
        Args:
            name: Agent identifier
            api_key: OpenRouter API key (defaults to env OPENROUTER_API_KEY)
            model: Model to use (default gpt-3.5-turbo via OpenRouter)
            use_memory: Whether to enable persistent memory
            memory_dir: Directory for memory storage
        """
        self.name = name
        self.model = model
        self.use_memory = use_memory
        
        # Initialize LLM client
        self.llm = LLMClient(api_key=api_key, model=model)
        
        # Initialize memory if enabled
        self.memory = None
        if use_memory:
            self.memory = AgentMemoryManager(name, db_dir=memory_dir)
    
    def reason_with_memory(
        self,
        query: str,
        system_prompt: Optional[str] = None,
        include_context: bool = True,
        temperature: float = 0.7,
        debug: bool = False,
    ) -> str:
        """Use LLM to reason about a query, informed by agent memory.
        
        Args:
            query: User question or task
            system_prompt: Optional system context
            include_context: Whether to include memory context
            temperature: LLM temperature (0.3 = precise, 0.7 = balanced, 0.9 = creative)
            debug: Whether to print ORAR cycle debug output
        
        Returns:
            LLM response
        """
        debug_output = ""
        
        # OBSERVE: Retrieve memory context
        debug_output += f"\n[OBSERVE] Agent '{self.name}' observing state...\n"
        
        prompt = query
        if include_context and self.memory:
            context = self.memory.get_context_for_reasoning()
            num_facts = len(self.memory.semantic.get_all_facts(self.name))
            num_episodes = len(self.memory.episodic.get_episodes(self.name))
            debug_output += f"  → Retrieved {num_facts} facts, {num_episodes} episodes from memory\n"
            prompt = f"{context}\n## Task\n{query}"
        else:
            debug_output += f"  → No memory context (memory disabled or empty)\n"
        
        # REASON: Prepare reasoning prompt
        debug_output += f"[REASON] Agent '{self.name}' reasoning about task...\n"
        debug_output += f"  → Task: {query[:80]}...\n"
        
        # ACT: Call LLM
        debug_output += f"[ACT] Agent '{self.name}' calling LLM (model: {self.model})...\n"
        response = self.llm.complete(prompt, temperature=temperature, max_tokens=500)
        debug_output += f"  → LLM Response: {response[:150]}...\n"
        
        # REFLECT: Record in memory
        debug_output += f"[REFLECT] Agent '{self.name}' reflecting & storing in memory...\n"
        
        if self.memory:
            self.memory.semantic.add_short_term(self.name, f"Query: {query[:100]}")
            self.memory.episodic.record_episode(
                self.name,
                "reasoning",
                {"query": query[:100], "response": response[:100]}
            )
            debug_output += f"  → Stored in short-term & episodic memory\n"
        
        if debug:
            print_debug_block(debug_output)
        
        return response
    
    def call_tool(self, tool_name: str, args: Dict[str, Any], debug: bool = False) -> Dict[str, Any]:
        """Invoke a tool and record the call in memory.
        
        Args:
            tool_name: Name of tool to call
            args: Tool arguments
            debug: Whether to print ORAR cycle debug output
        
        Returns:
            Tool result
        """
        debug_output = ""
        
        # OBSERVE: Tool requirements
        debug_output += f"\n[OBSERVE] Agent '{self.name}' observing tool requirements...\n"
        debug_output += f"  → Tool available: {tool_name}\n"
        
        # REASON: Decide to use tool
        debug_output += f"[REASON] Agent '{self.name}' deciding to use tool...\n"
        debug_output += f"  → Reasoning: Tool '{tool_name}' best for task\n"
        
        # ACT: Invoke tool
        debug_output += f"[ACT] Agent '{self.name}' invoking tool '{tool_name}'...\n"
        debug_output += f"  → Args: {args}\n"
        
        # Simulate tool call (real tool calls come from agent reasoning)
        result = {
            "success": True,
            "tool": tool_name,
            "args": args,
            "result": f"Executed {tool_name} with args {args}"
        }
        
        debug_output += f"  → Result: {result['result']}\n"
        
        # REFLECT: Record in tool call history
        debug_output += f"[REFLECT] Agent '{self.name}' recording tool call in memory...\n"
        
        if self.memory:
            self.memory.tool_calls.record_call(
                self.name,
                tool_name,
                args,
                result,
                success=True
            )
            debug_output += f"  → Stored in tool call history\n"
        
        if debug:
            print_debug_block(debug_output)
        
        return result
    
    def get_memory_summary(self) -> str:
        """Get a summary of agent memory state."""
        if not self.memory:
            return "[Memory disabled]"
        
        summary = f"=== Memory Summary for Agent: {self.name} ===\n\n"
        
        # Facts
        facts = self.memory.semantic.get_all_facts(self.name)
        summary += f"Facts ({len(facts)}):\n"
        for k, v in list(facts.items())[:5]:
            summary += f"  - {k}: {v}\n"
        
        # Relationships
        relationships = self.memory.semantic.get_relationships(self.name)
        summary += f"\nRelationships ({len(relationships)}):\n"
        for rel in relationships[:3]:
            summary += f"  - {rel['subject']} -{rel['predicate']}-> {rel['object']}\n"
        
        # Episodes
        episodes = self.memory.episodic.get_episodes(self.name)
        summary += f"\nRecent Episodes ({len(episodes)}):\n"
        for ep in episodes[:3]:
            summary += f"  - {ep['type']}: {ep['content'].get('description', 'N/A')}\n"
        
        # Tool calls
        calls = self.memory.tool_calls.get_calls(self.name)
        success_rate = self.memory.tool_calls.get_success_rate(self.name)
        summary += f"\nTool Calls: {len(calls)} total, {success_rate*100:.0f}% success rate\n"
        
        return summary
    
    def learn_fact(self, key: str, value: str):
        """Store a fact in long-term memory."""
        if self.memory:
            self.memory.semantic.add_fact(self.name, key, value)
    
    def learn_relationship(self, subject: str, predicate: str, obj: str):
        """Store a relationship in long-term memory."""
        if self.memory:
            self.memory.semantic.add_relationship(self.name, subject, predicate, obj)
    
    def get_context(self) -> str:
        """Get full memory context for reasoning."""
        if self.memory:
            return self.memory.get_context_for_reasoning()
        return "[No memory context]"
