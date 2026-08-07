"""
Lesson 6.2: Agent Memory Systems & LLM Reasoning (REFACTORED)

This lesson teaches how agents use integrated memory (semantic, episodic, short-term)
combined with LLM reasoning to maintain context and make intelligent decisions.

Each pattern demonstrates a distinct memory capability with BEFORE/AFTER comparison:
- WITHOUT memory: LLM sees only current query
- WITH memory: LLM has context from prior interactions, facts, history

Students learn: Memory transforms agents from stateless chatbots to contextual reasoners.

Run: python lesson-02-agent-memory-systems.py
Requires: export OPENROUTER_API_KEY='your-key-here'
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional

# Add imports for shared modules
sys.path.insert(0, str(Path(__file__).parent))

from shared.agent import Agent

# DEBUG: Set to True to see ORAR (Observe-Reason-Act-Reflect) cycle output
DEBUG = True



def clear_screen():
    """Clear terminal screen."""
    os.system("clear" if os.name == "posix" else "cls")


def validate_api_key():
    """Check if API key is set. Exit if not."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("\n" + "=" * 70)
        print("❌ OPENROUTER_API_KEY not set")
        print("=" * 70)
        print("\nSetup required:")
        print("  export OPENROUTER_API_KEY='your-key-here'")
        print("\nGet free API key:")
        print("  https://openrouter.ai (100+ models, free tier available)")
        print("\n" + "=" * 70)
        sys.exit(1)


def show_menu():
    """Display main menu."""
    clear_screen()
    print("\n" + "=" * 70)
    print("LESSON 6.2: AGENT MEMORY SYSTEMS & LLM REASONING")
    print("=" * 70)
    print()
    print("  Each pattern shows: WITHOUT memory vs WITH memory\n")
    print("    [1] PATTERN: Short-Term Memory (Current Conversation)")
    print("        → Agents remember recent interactions\n")
    print("    [2] PATTERN: Long-Term Memory (Persistent Facts)")
    print("        → Agents retain knowledge across sessions\n")
    print("    [3] PATTERN: Episodic Memory (Past Interactions)")
    print("        → Agents recall similar past situations\n")
    print("    [4] PATTERN: Semantic Memory (Knowledge Base)")
    print("        → Agents access company policies and facts\n")
    print("    [5] PATTERN: Integrated Memory (All Types Combined)")
    print("        → Full agent reasoning with complete memory\n")
    print("    [Q] Quit\n")
    print("=" * 70)


def demo_short_term_memory():
    """PATTERN 1: Short-Term Memory - Conversation Context"""
    clear_screen()
    print("\n" + "=" * 70)
    print("PATTERN 1: SHORT-TERM MEMORY - Current Conversation Context")
    print("=" * 70)
    
    print("\n📖 Concept:")
    print("  Short-term memory holds the current conversation context.")
    print("  Without it: Agent forgets what was just said.")
    print("  With it: Agent builds on previous messages.\n")
    
    user_interaction_1 = "My name is Alice and I work in sales."
    user_interaction_2 = "What was my name again?"
    user_interaction_3 = "What department do I work in?"
    
    print(f"User: {user_interaction_1}")
    print(f"User: {user_interaction_2}")
    print(f"User: {user_interaction_3}")
    
    input("\nPress [ENTER] to see WITHOUT memory...")
    
    # WITHOUT memory
    print("\n" + "-" * 70)
    print("WITHOUT MEMORY:")
    print("-" * 70)
    agent_no_mem = Agent(name="AgentNoMem", use_memory=False)
    
    print(f"\nQuery: {user_interaction_2}")
    response_no_mem = agent_no_mem.reason_with_memory(
        user_interaction_2,
        system_prompt="You are a helpful agent.",
        debug=DEBUG
    )
    print(f"Response: {response_no_mem[:200]}...")
    print("\n⚠️  Agent has no context! Can't answer.")
    
    input("\nPress [ENTER] to see WITH memory...")
    
    # WITH memory
    print("\n" + "-" * 70)
    print("WITH MEMORY:")
    print("-" * 70)
    agent_with_mem = Agent(name="AgentWithMem", use_memory=True)
    
    # Store context
    agent_with_mem.memory.semantic.add_short_term(agent_with_mem.name, f"User: {user_interaction_1}")
    
    print(f"\nStored context: '{user_interaction_1}'")
    print(f"Query: {user_interaction_2}")
    response_with_mem = agent_with_mem.reason_with_memory(
        user_interaction_2,
        system_prompt="You are a helpful agent.",
        include_context=True,
        debug=DEBUG
    )
    print(f"Response: {response_with_mem[:200]}...")
    print("\n✅ Agent recalls: 'Alice works in sales'")
    
    print("\n" + "-" * 70)
    input("Press [ENTER] to return to menu...")


def demo_long_term_memory():
    """PATTERN 2: Long-Term Memory - Persistent Facts"""
    clear_screen()
    print("\n" + "=" * 70)
    print("PATTERN 2: LONG-TERM MEMORY - Persistent Facts Across Sessions")
    print("=" * 70)
    
    print("\n📖 Concept:")
    print("  Long-term memory (SQLite) persists across script restarts.")
    print("  Without it: Agent forgets facts after restart.")
    print("  With it: Agent remembers customer info, policies, etc.\n")
    
    customer_facts = {
        "customer_name": "Acme Corp",
        "subscription_type": "Enterprise",
        "account_age_days": 180,
        "vip_status": "yes",
    }
    
    print("Facts to store:")
    for key, value in customer_facts.items():
        print(f"  {key}: {value}")
    
    input("\nPress [ENTER] to see WITHOUT memory...")
    
    # WITHOUT memory
    print("\n" + "-" * 70)
    print("WITHOUT MEMORY:")
    print("-" * 70)
    agent_no_mem = Agent(name="AgentNoMemFacts", use_memory=False)
    
    query = "Tell me about this customer's subscription and VIP status."
    print(f"\nQuery: {query}")
    response_no_mem = agent_no_mem.reason_with_memory(query, debug=DEBUG)
    print(f"Response: {response_no_mem[:300]}...")
    print("\n⚠️  Agent doesn't know customer details.")
    
    input("\nPress [ENTER] to see WITH memory...")
    
    # WITH memory
    print("\n" + "-" * 70)
    print("WITH MEMORY:")
    print("-" * 70)
    agent_with_mem = Agent(name="AgentWithMemFacts", use_memory=True)
    
    # Store facts
    for key, value in customer_facts.items():
        agent_with_mem.learn_fact(key, str(value))
        print(f"✓ Stored fact: {key} = {value}")
    
    print(f"\nQuery: {query}")
    response_with_mem = agent_with_mem.reason_with_memory(
        query,
        include_context=True,
        debug=DEBUG
    )
    print(f"Response: {response_with_mem[:300]}...")
    print("\n✅ Agent uses facts: Enterprise subscription, VIP status")
    
    # Show persistence
    print("\nPersistence check (facts survive restart):")
    print("-" * 70)
    agent_restart = Agent(name="AgentWithMemFacts", use_memory=True)
    print(f"Stored facts after restart: {agent_restart.memory.semantic.get_all_facts(agent_restart.name)}")
    print("✅ Facts persisted in SQLite!")
    
    print("\n" + "-" * 70)
    input("Press [ENTER] to return to menu...")


def demo_episodic_memory():
    """PATTERN 3: Episodic Memory - Learning from Past Interactions"""
    clear_screen()
    print("\n" + "=" * 70)
    print("PATTERN 3: EPISODIC MEMORY - Recalling Past Interactions")
    print("=" * 70)
    
    print("\n📖 Concept:")
    print("  Episodic memory stores past interactions and events (JSONL log).")
    print("  Without it: Agent treats each query as new, loses patterns.")
    print("  With it: Agent learns from history and improves decisions.\n")
    
    # Simulate past interactions
    past_interactions = [
        {"user": "I need a refund", "resolution": "Approved 30-day refund", "sentiment": "frustrated"},
        {"user": "How do I export data?", "resolution": "Sent export guide", "sentiment": "neutral"},
        {"user": "App crashed on login", "resolution": "Fixed in v2.1 release", "sentiment": "urgent"},
    ]
    
    print("Past customer interactions:")
    for i, interaction in enumerate(past_interactions, 1):
        print(f"  {i}. User: '{interaction['user'][:30]}...' → {interaction['resolution'][:30]}...")
    
    input("\nPress [ENTER] to see WITHOUT memory...")
    
    # WITHOUT memory
    print("\n" + "-" * 70)
    print("WITHOUT MEMORY:")
    print("-" * 70)
    agent_no_mem = Agent(name="AgentNoMemEpisodes", use_memory=False)
    
    query = "Customer says app keeps crashing. How should we respond?"
    print(f"\nQuery: {query}")
    response_no_mem = agent_no_mem.reason_with_memory(query, debug=DEBUG)
    print(f"Response: {response_no_mem[:250]}...")
    print("\n⚠️  Agent doesn't know about similar past issues.")
    
    input("\nPress [ENTER] to see WITH memory...")
    
    # WITH memory
    print("\n" + "-" * 70)
    print("WITH MEMORY:")
    print("-" * 70)
    agent_with_mem = Agent(name="AgentWithMemEpisodes", use_memory=True)
    
    # Record past episodes
    for interaction in past_interactions:
        agent_with_mem.memory.episodic.record_episode(
            agent_with_mem.name,
            "customer_interaction",
            {
                "description": interaction['user'][:50],
                "resolution": interaction['resolution'],
                "sentiment": interaction['sentiment']
            }
        )
    
    print(f"\nRecorded {len(past_interactions)} past episodes")
    print(f"Query: {query}")
    response_with_mem = agent_with_mem.reason_with_memory(
        query,
        include_context=True,
        debug=DEBUG
    )
    print(f"Response: {response_with_mem[:250]}...")
    print("\n✅ Agent recalls: 'App crash is a known issue (fixed in v2.1)'")
    
    print("\n" + "-" * 70)
    input("Press [ENTER] to return to menu...")


def demo_semantic_memory():
    """PATTERN 4: Semantic Memory - Knowledge Base & Policies"""
    clear_screen()
    print("\n" + "=" * 70)
    print("PATTERN 4: SEMANTIC MEMORY - Knowledge Base & Policies")
    print("=" * 70)
    
    print("\n📖 Concept:")
    print("  Semantic memory stores structured knowledge (policies, procedures).")
    print("  Without it: Agent makes up policy answers.")
    print("  With it: Agent knows company rules and can enforce them.\n")
    
    policies = {
        "policy_refund_window": "30 days from purchase",
        "policy_support_response": "Within 24 hours",
        "policy_data_export": "Available to all users",
    }
    
    print("Company policies to store:")
    for key, value in policies.items():
        print(f"  {key}: {value}")
    
    input("\nPress [ENTER] to see WITHOUT memory...")
    
    # WITHOUT memory
    print("\n" + "-" * 70)
    print("WITHOUT MEMORY:")
    print("-" * 70)
    agent_no_mem = Agent(name="AgentNoMemPolicy", use_memory=False)
    
    query = "Can I get a refund? It's been 45 days since purchase."
    print(f"\nQuery: {query}")
    response_no_mem = agent_no_mem.reason_with_memory(query, debug=DEBUG)
    print(f"Response: {response_no_mem[:250]}...")
    print("\n⚠️  Agent might make up wrong policy.")
    
    input("\nPress [ENTER] to see WITH memory...")
    
    # WITH memory
    print("\n" + "-" * 70)
    print("WITH MEMORY:")
    print("-" * 70)
    agent_with_mem = Agent(name="AgentWithMemPolicy", use_memory=True)
    
    # Store policies
    for key, value in policies.items():
        agent_with_mem.learn_fact(key, value)
        print(f"✓ Stored policy: {key}")
    
    print(f"\nQuery: {query}")
    response_with_mem = agent_with_mem.reason_with_memory(
        query,
        include_context=True,
        debug=DEBUG
    )
    print(f"Response: {response_with_mem[:250]}...")
    print("\n✅ Agent enforces: '30-day refund window has passed'")
    
    print("\n" + "-" * 70)
    input("Press [ENTER] to return to menu...")


def demo_integrated_memory():
    """PATTERN 5: Integrated Memory - All Memory Types Working Together"""
    clear_screen()
    print("\n" + "=" * 70)
    print("PATTERN 5: INTEGRATED MEMORY - All Memory Types Combined")
    print("=" * 70)
    
    print("\n📖 Concept:")
    print("  Agents combine all memory types for comprehensive reasoning.")
    print("  Without it: Agent is stateless chatbot.")
    print("  With it: Agent is contextual, learns, and improves.\n")
    
    input("Press [ENTER] to initialize integrated agent with memory...")
    
    # Setup integrated agent
    agent = Agent(name="IntegratedAgent", use_memory=True)
    
    print("\n" + "-" * 70)
    print("SETUP: Building agent memory")
    print("-" * 70)
    
    # Add facts
    agent.learn_fact("customer_status", "VIP")
    agent.learn_fact("support_tier", "Priority")
    print("✓ Added long-term facts")
    
    # Add relationships
    agent.learn_relationship("customer", "subscribes_to", "premium_plan")
    agent.learn_relationship("customer", "is_vip", "true")
    print("✓ Added relationships")
    
    # Add short-term context
    agent.memory.semantic.add_short_term(agent.name, "User asked about export options earlier")
    agent.memory.semantic.add_short_term(agent.name, "User mentioned account is 6 months old")
    print("✓ Added short-term context")
    
    # Record episodes
    agent.memory.episodic.record_episode(
        agent.name,
        "support_ticket",
        {"description": "Previous successful data export", "outcome": "resolved"}
    )
    print("✓ Added episode history")
    
    # Show memory state
    print("\n" + "-" * 70)
    print("MEMORY STATE:")
    print("-" * 70)
    print(agent.get_memory_summary())
    
    # Query with full memory
    input("\nPress [ENTER] to run query with integrated memory...")
    
    print("\n" + "-" * 70)
    print("QUERY WITH INTEGRATED MEMORY:")
    print("-" * 70)
    
    query = "I need to export my data and I'm in a hurry."
    print(f"\nQuery: {query}")
    
    response = agent.reason_with_memory(
        query,
        system_prompt="You are a helpful support agent. Consider the customer's VIP status and history.",
        include_context=True,
        temperature=0.7,
        debug=DEBUG
    )
    
    print(f"\nAgent Response:\n{response}")
    print("\n✅ Agent's reasoning uses:")
    print("  - Short-term: Recent conversation context")
    print("  - Long-term: Customer facts (VIP status)")
    print("  - Relationships: Subscription type")
    print("  - Episodes: Similar past issues")
    
    print("\n" + "-" * 70)
    input("Press [ENTER] to return to menu...")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main menu loop."""
    validate_api_key()
    
    patterns = {
        "1": ("Short-Term Memory", demo_short_term_memory),
        "2": ("Long-Term Memory", demo_long_term_memory),
        "3": ("Episodic Memory", demo_episodic_memory),
        "4": ("Semantic Memory", demo_semantic_memory),
        "5": ("Integrated Memory", demo_integrated_memory),
    }
    
    while True:
        show_menu()
        choice = input("Enter choice: ").strip().upper()
        
        if choice == "Q":
            print("\n✅ Goodbye!\n")
            break
        
        if choice in patterns:
            pattern_name, pattern_func = patterns[choice]
            try:
                pattern_func()
            except Exception as e:
                print(f"\n❌ Error: {e}")
                import traceback
                traceback.print_exc()
                input("Press [ENTER] to return to menu...")
        else:
            print(f"\n❌ Invalid choice. Try again.")
            input("Press [ENTER]...")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("MODULE 6, LESSON 6.2: AGENT MEMORY SYSTEMS & LLM REASONING")
    print("=" * 70)
    print("\nThis lesson teaches how agents use memory to become contextual reasoners.")
    print("Each pattern shows: WITHOUT memory vs WITH memory\n")
    input("Press [ENTER] to start...\n")
    
    main()
