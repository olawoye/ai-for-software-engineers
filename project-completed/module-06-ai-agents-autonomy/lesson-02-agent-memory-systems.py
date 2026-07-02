"""
Lesson 6.2: Agent Memory Systems & Architecture (Consolidated)

This lesson combines agent architecture concepts (Lesson 6.1) with memory system
implementation (Lesson 6.2) to create the first comprehensive agent code lesson.

PART 1: Agent Architecture Foundations
  - What agents are vs. chatbots
  - Agent loop: Observe → Reason → Act → Reflect
  - Why memory is critical for agent autonomy
  - Memory types: Short-term, Long-term, Episodic, Semantic

PART 2: Memory Systems Implementation
  - Core template method: create_agent_with_memory()
  - Memory classes for each type
  - Agent class integrating memory
  - Memory persistence and retrieval patterns

PART 3: Demonstrations
  - Short-term memory (current conversation)
  - Long-term memory (persistent facts)
  - Episodic memory (specific past interactions)
  - Semantic memory (knowledge & skills)
  - Cross-conversation consistency

Business Scenario:
  "A customer support agent must remember previous interactions, customer
   preferences, company policies, and historical actions across multiple
   conversations. Without memory, the agent would repeat itself and forget
   critical context."

Learning Goals:
  1. Understand agent architecture and decision loops
  2. Implement multiple memory types
  3. Build agents that learn and retain context
  4. Prepare agents to use tools (Lesson 6.3)
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Optional, Any, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum


# ============================================================================
# AGENT ARCHITECTURE CONCEPTS (from Lesson 6.1)
# ============================================================================
"""
Agent vs. Chatbot:
  Chatbot: Responds to user input (reactive)
    User → Process → Response
  
  Agent: Pursues goals autonomously (proactive)
    Observe → Reason → Act → Reflect → (repeat)

Agent Decision Loop:
  1. OBSERVE: Perceive current state, receive user message, check memory
  2. REASON: Process information, plan action, evaluate options
  3. ACT: Execute action (tool call, response, state change)
  4. REFLECT: Evaluate outcome, learn, update memory, assess progress

Why Memory Matters for Agents:
  - Maintain context across conversations
  - Learn from past interactions
  - Make consistent decisions
  - Provide personalized responses
  - Remember user preferences
  - Track long-term goals
"""


# ============================================================================
# MEMORY TYPE DEFINITIONS
# ============================================================================

class MemoryType(Enum):
    """Types of agent memory."""
    SHORT_TERM = "short_term"      # Current conversation context (volatile)
    LONG_TERM = "long_term"        # Persistent facts and relationships
    EPISODIC = "episodic"          # Specific interactions and events
    SEMANTIC = "semantic"          # Knowledge, skills, facts


@dataclass
class MemoryEntry:
    """Single memory entry."""
    timestamp: str
    content: str
    memory_type: MemoryType
    importance: float = 0.5  # 0.0-1.0 importance score
    tags: Set[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = set()


class ShortTermMemory:
    """Working memory for current conversation.
    
    Volatile, limited capacity, fast retrieval.
    Typical capacity: last 5-10 items.
    """
    
    def __init__(self, max_items: int = 10):
        self.max_items = max_items
        self.items: List[MemoryEntry] = []
    
    def add(self, content: str, importance: float = 0.5):
        """Add item to short-term memory."""
        entry = MemoryEntry(
            timestamp=datetime.now().isoformat(),
            content=content,
            memory_type=MemoryType.SHORT_TERM,
            importance=importance
        )
        self.items.append(entry)
        # Keep only most recent items
        if len(self.items) > self.max_items:
            # Remove lowest importance items
            self.items.sort(key=lambda x: x.importance)
            self.items = self.items[-(self.max_items):]
    
    def get_context(self) -> str:
        """Get all short-term memory as context string."""
        if not self.items:
            return "[No recent conversation context]"
        context = "Recent conversation:\n"
        for item in self.items[-5:]:  # Last 5 items
            context += f"  - {item.content}\n"
        return context
    
    def clear(self):
        """Clear short-term memory."""
        self.items = []


class LongTermMemory:
    """Persistent memory across conversations.
    
    Durable facts, relationships, learned patterns.
    Survives conversation restarts.
    """
    
    def __init__(self, storage_file: str = "agent_longterm_memory.json"):
        self.storage_file = storage_file
        self.facts: Dict[str, Any] = {}
        self.relationships: Dict[str, List[str]] = {}
        self.load()
    
    def add_fact(self, key: str, value: Any):
        """Store a fact in long-term memory."""
        self.facts[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        self.save()
    
    def add_relationship(self, entity: str, relationship: str, target: str):
        """Store entity relationship."""
        if entity not in self.relationships:
            self.relationships[entity] = []
        rel_str = f"{relationship} {target}"
        if rel_str not in self.relationships[entity]:
            self.relationships[entity].append(rel_str)
        self.save()
    
    def get_fact(self, key: str) -> Optional[Any]:
        """Retrieve fact from long-term memory."""
        if key in self.facts:
            return self.facts[key]["value"]
        return None
    
    def get_summary(self) -> str:
        """Get long-term memory summary for context."""
        summary = "Known facts:\n"
        for key, data in list(self.facts.items())[:5]:  # First 5 facts
            summary += f"  - {key}: {data['value']}\n"
        return summary
    
    def save(self):
        """Persist to storage."""
        try:
            data = {
                "facts": self.facts,
                "relationships": self.relationships
            }
            Path(self.storage_file).write_text(json.dumps(data, indent=2))
        except Exception as e:
            print(f"Warning: Could not save long-term memory: {e}")
    
    def load(self):
        """Load from storage."""
        try:
            if Path(self.storage_file).exists():
                data = json.loads(Path(self.storage_file).read_text())
                self.facts = data.get("facts", {})
                self.relationships = data.get("relationships", {})
        except Exception as e:
            print(f"Warning: Could not load long-term memory: {e}")


class EpisodicMemory:
    """Memory of specific interactions and events.
    
    Episode = specific conversation, task, or interaction.
    Enables recall of "what happened last time".
    """
    
    def __init__(self, max_episodes: int = 50):
        self.max_episodes = max_episodes
        self.episodes: List[Dict[str, Any]] = []
    
    def record_episode(self, episode_type: str, description: str, 
                      outcome: str, participants: List[str] = None):
        """Record an episode (interaction, task, event)."""
        episode = {
            "timestamp": datetime.now().isoformat(),
            "type": episode_type,
            "description": description,
            "outcome": outcome,
            "participants": participants or [],
        }
        self.episodes.append(episode)
        # Keep only most recent episodes
        if len(self.episodes) > self.max_episodes:
            self.episodes = self.episodes[-self.max_episodes:]
    
    def recall_similar_episodes(self, query: str, top_k: int = 3) -> List[Dict]:
        """Find similar past episodes."""
        # Simple string matching for demo
        similar = []
        for ep in reversed(self.episodes):  # Most recent first
            if any(word in ep["description"].lower() for word in query.lower().split()):
                similar.append(ep)
                if len(similar) >= top_k:
                    break
        return similar
    
    def get_episode_summary(self) -> str:
        """Summarize recent episodes."""
        if not self.episodes:
            return "[No episode history]"
        summary = f"Recent episodes ({len(self.episodes)} total):\n"
        for ep in self.episodes[-3:]:  # Last 3
            summary += f"  - {ep['type']}: {ep['description']} → {ep['outcome']}\n"
        return summary


class SemanticMemory:
    """Knowledge, facts, skills, and concepts.
    
    Semantic = meaning-based, conceptual.
    Examples: product knowledge, company policies, industry facts.
    """
    
    def __init__(self):
        self.knowledge_base: Dict[str, Dict[str, str]] = {}
        # Structure: {category: {concept: description}}
    
    def add_knowledge(self, category: str, concept: str, description: str):
        """Add knowledge/fact to semantic memory."""
        if category not in self.knowledge_base:
            self.knowledge_base[category] = {}
        self.knowledge_base[category][concept] = description
    
    def get_knowledge(self, category: str, concept: str = None) -> Optional[str]:
        """Retrieve knowledge."""
        if category not in self.knowledge_base:
            return None
        if concept is None:
            # Return all in category
            return self.knowledge_base[category]
        return self.knowledge_base[category].get(concept)
    
    def get_relevant_knowledge(self, query: str) -> str:
        """Retrieve relevant knowledge for query."""
        relevant = []
        query_words = query.lower().split()
        for category, concepts in self.knowledge_base.items():
            for concept, desc in concepts.items():
                if any(word in concept.lower() or word in desc.lower() 
                       for word in query_words):
                    relevant.append(f"{concept}: {desc}")
        if relevant:
            return "Relevant knowledge:\n  - " + "\n  - ".join(relevant[:3])
        return "[No relevant knowledge found]"


# ============================================================================
# CORE TEMPLATE METHOD: create_agent_with_memory()
# ============================================================================

class Agent:
    """AI Agent with integrated memory systems."""
    
    def __init__(
        self,
        name: str,
        short_term_memory: ShortTermMemory,
        long_term_memory: LongTermMemory,
        episodic_memory: EpisodicMemory,
        semantic_memory: SemanticMemory,
    ):
        self.name = name
        self.short_term = short_term_memory
        self.long_term = long_term_memory
        self.episodic = episodic_memory
        self.semantic = semantic_memory
        self.conversation_count = 0
    
    def get_memory_context(self) -> str:
        """Retrieve all relevant memory as context for reasoning."""
        context = f"Agent {self.name} memory context:\n"
        context += f"{'='*60}\n"
        context += self.short_term.get_context() + "\n"
        context += self.long_term.get_summary() + "\n"
        context += self.episodic.get_episode_summary() + "\n"
        return context
    
    def observe(self, user_input: str) -> str:
        """OBSERVE phase: Perceive input and retrieve memory."""
        # Add to short-term memory
        self.short_term.add(f"User: {user_input}", importance=0.8)
        # Get memory context
        memory_context = self.get_memory_context()
        return memory_context
    
    def reason(self, user_input: str, memory_context: str) -> str:
        """REASON phase: Plan response using memory."""
        reasoning = f"Planning response to: {user_input}\n"
        reasoning += f"Using memory context to inform decision...\n"
        # In real implementation, this would call LLM
        reasoning += "[Reasoning with memory integration complete]"
        return reasoning
    
    def act(self, decision: str, user_input: str) -> str:
        """ACT phase: Execute action and record."""
        response = f"Agent {self.name}: {decision}"
        # Record to short-term memory
        self.short_term.add(f"Agent: {response}", importance=0.8)
        return response
    
    def reflect(self, user_input: str, response: str, success: bool = True):
        """REFLECT phase: Learn and update memory."""
        # Record episode
        self.episodic.record_episode(
            episode_type="conversation",
            description=user_input[:50],
            outcome="success" if success else "failed"
        )
        # Update long-term if important
        if len(user_input) > 20:
            self.long_term.add_fact(
                f"interaction_{self.conversation_count}",
                user_input[:100]
            )
        self.conversation_count += 1
    
    def run_decision_loop(self, user_input: str) -> str:
        """Execute full agent loop: Observe → Reason → Act → Reflect."""
        # 1. OBSERVE
        memory_context = self.observe(user_input)
        
        # 2. REASON
        reasoning = self.reason(user_input, memory_context)
        
        # 3. ACT
        decision = "I understand your request and will help"
        response = self.act(decision, user_input)
        
        # 4. REFLECT
        self.reflect(user_input, response, success=True)
        
        return response


def create_agent_with_memory(
    agent_name: str,
    memory_strategy: str = "hybrid",
    max_short_term_items: int = 10,
    enable_persistence: bool = True,
) -> Agent:
    """Core template method: Build an agent with integrated memory systems.
    
    This is the production-ready pattern for creating agents with persistent,
    context-aware memory. Learners can extract and adapt this for their own
    agent implementations.
    
    Args:
        agent_name: Name of the agent
        memory_strategy: "short_only", "long_only", or "hybrid" (default)
        max_short_term_items: Maximum items in working memory
        enable_persistence: Whether to persist long-term memory to disk
    
    Returns:
        Agent: Fully-configured agent with all memory layers integrated
    
    Features:
        - Short-term memory (conversation context)
        - Long-term memory (persistent facts and relationships)
        - Episodic memory (past interactions)
        - Semantic memory (knowledge base)
        - Memory-aware decision making (Observe → Reason → Act → Reflect)
        - Persistent storage support
    
    Example:
        >>> agent = create_agent_with_memory(
        ...     agent_name="CustomerSupport",
        ...     memory_strategy="hybrid"
        ... )
        >>> response = agent.run_decision_loop("What's my account status?")
    """
    
    print("=" * 70)
    print("AGENT INITIALIZATION WITH MEMORY")
    print("=" * 70)
    
    print(f"\n✓ Creating agent: {agent_name}")
    print(f"  Memory strategy: {memory_strategy}")
    
    # Create memory layers
    print(f"\n[Memory Layer 1] Short-Term Memory")
    short_term = ShortTermMemory(max_items=max_short_term_items)
    print(f"  ✓ Initialized (capacity: {max_short_term_items} items)")
    
    print(f"\n[Memory Layer 2] Long-Term Memory")
    long_term = LongTermMemory(
        storage_file=f".agent_memory/{agent_name.lower()}_longterm.json" if enable_persistence else None
    )
    print(f"  ✓ Initialized (persistence: {'enabled' if enable_persistence else 'disabled'})")
    
    print(f"\n[Memory Layer 3] Episodic Memory")
    episodic = EpisodicMemory(max_episodes=50)
    print(f"  ✓ Initialized (max episodes: 50)")
    
    print(f"\n[Memory Layer 4] Semantic Memory")
    semantic = SemanticMemory()
    # Populate with sample knowledge
    semantic.add_knowledge("policies", "refund", "30-day money-back guarantee")
    semantic.add_knowledge("policies", "support", "24/7 support available")
    semantic.add_knowledge("product", "feature_1", "Real-time analytics")
    semantic.add_knowledge("product", "feature_2", "Custom dashboards")
    print(f"  ✓ Initialized (4 knowledge entries)")
    
    # Create agent
    agent = Agent(
        name=agent_name,
        short_term_memory=short_term,
        long_term_memory=long_term,
        episodic_memory=episodic,
        semantic_memory=semantic,
    )
    
    print(f"\n[Agent Decision Loop]")
    print(f"  ✓ Agent configured with full memory architecture")
    print(f"  Decision loop: Observe → Reason → Act → Reflect")
    
    print(f"\n✅ Agent '{agent_name}' ready with integrated memory\n")
    
    return agent


# ============================================================================
# DEMONSTRATIONS
# ============================================================================

def demo_agent_architecture():
    """Demonstration 1: Agent architecture and decision loop."""
    print("\n" + "=" * 70)
    print("DEMO 1: AGENT ARCHITECTURE & DECISION LOOP")
    print("=" * 70)
    
    print("""
Agent vs. Chatbot
=================

Chatbot (Reactive):
  User Input → Process → Response
  - Stateless
  - No memory
  - Same response for same input
  - Example: Simple FAQ bot

Agent (Autonomous):
  Observe → Reason → Act → Reflect → (repeat)
  - Stateful
  - Persistent memory
  - Context-aware responses
  - Goal-directed behavior
  - Example: Customer support agent

Agent Decision Loop
===================

1. OBSERVE
   └─ Perceive user input
   └─ Retrieve relevant memory
   └─ Build context for reasoning

2. REASON
   └─ Process information
   └─ Evaluate options
   └─ Plan action

3. ACT
   └─ Execute decision
   └─ Provide response
   └─ Update state

4. REFLECT
   └─ Evaluate outcome
   └─ Learn from interaction
   └─ Update memory
   └─ Check goal progress

Why Memory Matters
==================

Without Memory:
  ❌ Repeats same question
  ❌ Forgets customer preferences
  ❌ Can't learn from mistakes
  ❌ Provides generic responses

With Memory:
  ✅ Remembers conversation context
  ✅ Recalls customer preferences
  ✅ Learns and improves
  ✅ Provides personalized responses
""")
    
    print("✅ Agent architecture demonstration complete\n")


def demo_short_term_memory():
    """Demonstration 2: Short-term memory (conversation context)."""
    print("\n" + "=" * 70)
    print("DEMO 2: SHORT-TERM MEMORY (Conversation Context)")
    print("=" * 70)
    
    agent = create_agent_with_memory("DemoAgent")
    
    print("\nSimulating multi-turn conversation:")
    print("-" * 70)
    
    conversation = [
        "My name is Alice",
        "I have a question about billing",
        "How do I update my payment method?",
    ]
    
    for i, user_msg in enumerate(conversation, 1):
        print(f"\nTurn {i}:")
        print(f"  User: {user_msg}")
        response = agent.run_decision_loop(user_msg)
        print(f"  Agent: {response}")
    
    print("\nShort-Term Memory After Conversation:")
    print(agent.short_term.get_context())
    
    print("✅ Short-term memory demonstration complete\n")


def demo_long_term_memory():
    """Demonstration 3: Long-term memory (persistent learning)."""
    print("\n" + "=" * 70)
    print("DEMO 3: LONG-TERM MEMORY (Persistent Facts)")
    print("=" * 70)
    
    agent = create_agent_with_memory("LongTermAgent")
    
    print("\nAdding persistent facts:")
    print("-" * 70)
    
    facts = [
        ("customer_name", "Alice Johnson"),
        ("customer_tier", "Premium"),
        ("preferred_contact", "email"),
    ]
    
    for key, value in facts:
        agent.long_term.add_fact(key, value)
        print(f"  ✓ Added: {key} = {value}")
    
    print("\nRetrieving from long-term memory:")
    print("-" * 70)
    for key, _ in facts:
        retrieved = agent.long_term.get_fact(key)
        print(f"  Retrieved: {key} = {retrieved}")
    
    print("\nLong-term memory persists across conversations:")
    print(agent.long_term.get_summary())
    
    print("✅ Long-term memory demonstration complete\n")


def demo_episodic_memory():
    """Demonstration 4: Episodic memory (past interactions)."""
    print("\n" + "=" * 70)
    print("DEMO 4: EPISODIC MEMORY (Past Interactions)")
    print("=" * 70)
    
    agent = create_agent_with_memory("EpisodeAgent")
    
    print("\nRecording interaction episodes:")
    print("-" * 70)
    
    episodes = [
        ("support_ticket", "Customer asked about refund policy", "resolved"),
        ("product_demo", "Showed customer dashboard features", "interested"),
        ("billing_issue", "Updated payment method for account", "success"),
    ]
    
    for ep_type, desc, outcome in episodes:
        agent.episodic.record_episode(ep_type, desc, outcome)
        print(f"  ✓ Recorded {ep_type}: {outcome}")
    
    print("\nRecalling similar past episodes:")
    print("-" * 70)
    similar = agent.episodic.recall_similar_episodes("refund", top_k=2)
    for ep in similar:
        print(f"  Found: {ep['type']} - {ep['description']}")
    
    print("\nEpisodic memory summary:")
    print(agent.episodic.get_episode_summary())
    
    print("✅ Episodic memory demonstration complete\n")


def demo_semantic_memory():
    """Demonstration 5: Semantic memory (knowledge base)."""
    print("\n" + "=" * 70)
    print("DEMO 5: SEMANTIC MEMORY (Knowledge Base)")
    print("=" * 70)
    
    agent = create_agent_with_memory("KnowledgeAgent")
    
    print("\nAgent's semantic knowledge base:")
    print("-" * 70)
    
    # Add more knowledge
    agent.semantic.add_knowledge("troubleshooting", "login_failed", "Try password reset")
    agent.semantic.add_knowledge("troubleshooting", "slow_loading", "Clear browser cache")
    
    print("\nQuerying knowledge base:")
    print("-" * 70)
    
    queries = [
        "refund policy",
        "dashboard features",
        "password issue",
    ]
    
    for query in queries:
        knowledge = agent.semantic.get_relevant_knowledge(query)
        print(f"\nQuery: '{query}'")
        print(f"Result:\n{knowledge}")
    
    print("\n✅ Semantic memory demonstration complete\n")


def demo_memory_integration():
    """Demonstration 6: All memory types working together."""
    print("\n" + "=" * 70)
    print("DEMO 6: INTEGRATED MEMORY IN ACTION")
    print("=" * 70)
    
    agent = create_agent_with_memory("IntegratedAgent")
    
    print("\nSetting up agent context:")
    print("-" * 70)
    
    # Add knowledge
    agent.semantic.add_knowledge("company", "policy_response_time", "24 hours max")
    agent.semantic.add_knowledge("company", "policy_refund", "30-day guarantee")
    
    # Add persistent fact
    agent.long_term.add_fact("customer_status", "VIP")
    agent.long_term.add_relationship("customer", "subscribed_to", "premium_plan")
    
    print("✓ Added semantic knowledge (policies)")
    print("✓ Added long-term facts (customer status)")
    
    print("\nRunning agent decision loop with integrated memory:")
    print("-" * 70)
    
    user_input = "I want to know about refunds"
    print(f"\nUser: {user_input}")
    
    # Execute full loop
    response = agent.run_decision_loop(user_input)
    
    print(f"\nAgent response: {response}")
    
    print("\nAgent's complete memory context:")
    print(agent.get_memory_context())
    
    print("✅ Integrated memory demonstration complete\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("LESSON 6.2: AGENT MEMORY SYSTEMS & ARCHITECTURE (Consolidated)")
    print("=" * 70)
    print("\nThis lesson teaches agent architecture fundamentals combined with")
    print("practical memory system implementation. Agents use memory to maintain")
    print("context across conversations and make intelligent decisions.\n")
    
    # Part 1: Concepts
    demo_agent_architecture()
    print("\n" + "-" * 70 + "\n")
    
    # Part 2: Memory implementations
    demo_short_term_memory()
    print("\n" + "-" * 70 + "\n")
    
    demo_long_term_memory()
    print("\n" + "-" * 70 + "\n")
    
    demo_episodic_memory()
    print("\n" + "-" * 70 + "\n")
    
    demo_semantic_memory()
    print("\n" + "-" * 70 + "\n")
    
    # Part 3: Integration
    demo_memory_integration()
    
    print("\n" + "=" * 70)
    print("LESSON COMPLETE - AGENTS WITH MEMORY READY")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("  1. Agents use decision loops (Observe → Reason → Act → Reflect)")
    print("  2. Memory types serve different purposes (short, long, episodic, semantic)")
    print("  3. Integrated memory enables context-aware responses")
    print("  4. Memory persistence allows learning across sessions")
    print("  5. Agent architecture forms foundation for tool use (Lesson 6.3)\n")
    print("Next Steps:")
    print("  Lesson 6.3: Integrate agents with Module 5 MCP Tools")
    print("  Lesson 6.5: Build autonomous workflows using agent + tools\n")
