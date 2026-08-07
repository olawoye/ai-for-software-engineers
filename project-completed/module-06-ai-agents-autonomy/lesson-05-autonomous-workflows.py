"""
Lesson 6.5: Autonomous Workflows (REFACTORED)

This lesson teaches building autonomous, self-executing workflows that combine
agents (Lesson 6.2), tools (Lesson 6.3), and scheduling with state management.

Each pattern demonstrates workflow capabilities with comparison:
- WITHOUT workflows: Each task requires manual execution
- WITH workflows: Automation executes and improves over time

Students learn: Workflows scale agent capability from single queries to orchestrated processes.

Run: python lesson-05-autonomous-workflows.py
Requires: export OPENROUTER_API_KEY='your-key-here'
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
import time

sys.path.insert(0, str(Path(__file__).parent))
from shared.agent import Agent


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
    print("LESSON 6.5: AUTONOMOUS WORKFLOWS")
    print("=" * 70)
    print()
    print("  Each pattern shows: Manual execution vs Autonomous workflow\n")
    print("    [1] PATTERN: Workflow Definition & Triggers")
    print("        → Define multi-step workflows with scheduling\n")
    print("    [2] PATTERN: State Management Across Steps")
    print("        → Data flows through workflow steps\n")
    print("    [3] PATTERN: Execution History & Learning")
    print("        → Workflows improve through episodic memory\n")
    print("    [4] PATTERN: Error Handling & Recovery")
    print("        → Graceful degradation and retries\n")
    print("    [Q] Quit\n")
    print("=" * 70)


class WorkflowStep:
    """Represents a single step in a workflow."""
    
    def __init__(self, name: str, step_type: str, config: Dict[str, Any]):
        self.name = name
        self.step_type = step_type  # "agent_reasoning", "tool_call", "conditional", etc
        self.config = config


class WorkflowContext:
    """Execution context for workflow runs."""
    
    def __init__(self):
        self.step_outputs = {}
        self.errors = []
        self.start_time = datetime.now()
        self.end_time = None
    
    def add_output(self, step_name: str, output: Any):
        """Store step output."""
        self.step_outputs[step_name] = output
    
    def get_output(self, step_name: str) -> Optional[Any]:
        """Retrieve previous step output."""
        return self.step_outputs.get(step_name)
    
    def add_error(self, step_name: str, error: str):
        """Record step error."""
        self.errors.append({"step": step_name, "error": error, "time": datetime.now().isoformat()})
    
    def finish(self):
        """Mark workflow as complete."""
        self.end_time = datetime.now()
    
    def get_duration_seconds(self) -> float:
        """Get execution time."""
        end = self.end_time or datetime.now()
        return (end - self.start_time).total_seconds()


def demo_workflow_definition():
    """PATTERN 1: Workflow Definition & Triggers"""
    clear_screen()
    print("\n" + "=" * 70)
    print("PATTERN 1: WORKFLOW DEFINITION & TRIGGERS")
    print("=" * 70)
    
    print("\n📖 Concept:")
    print("  Define multi-step workflows with triggers (time-based, event-based).")
    print("  Without workflows: Manual execution of each step.")
    print("  With workflows: Automated execution on schedule.\n")
    
    workflow_def = [
        WorkflowStep("Query Data", "tool_call", {"tool": "search_knowledge", "args": {"query": "monthly metrics"}}),
        WorkflowStep("Analyze Results", "agent_reasoning", {"prompt": "Summarize key insights"}),
        WorkflowStep("Generate Report", "transform", {"type": "format_html"}),
    ]
    
    print("Workflow: Executive Report Generation")
    print("Trigger: Every Friday 5 PM\n")
    print("Steps:")
    for i, step in enumerate(workflow_def, 1):
        print(f"  {i}. {step.name} ({step.step_type})")
    
    input("\nPress [ENTER] to see WITHOUT workflow...")
    
    # WITHOUT workflow
    print("\n" + "-" * 70)
    print("WITHOUT WORKFLOW:")
    print("-" * 70)
    print(f"\nManual Process:")
    print(f"  Friday 5:00 PM - Manually query metrics")
    print(f"  Friday 5:10 PM - Manually analyze results")
    print(f"  Friday 5:20 PM - Manually format report")
    print(f"  Friday 5:30 PM - Manually send to team")
    print(f"\n⚠️  Requires human intervention. Easy to forget or delay.")
    
    input("\nPress [ENTER] to see WITH workflow...")
    
    # WITH workflow
    print("\n" + "-" * 70)
    print("WITH WORKFLOW:")
    print("-" * 70)
    print(f"\nAutomated Process:")
    print(f"  Friday 5:00 PM - Workflow triggers automatically")
    print(f"  Step 1: Query metrics (0.2s)")
    print(f"  Step 2: Analyze results (1.5s)")
    print(f"  Step 3: Generate report (0.5s)")
    print(f"  Friday 5:02 PM - Report automatically sent")
    print(f"\n✅ No human intervention needed. Consistent timing.")
    
    print("\n" + "-" * 70)
    input("Press [ENTER] to return to menu...")


def demo_state_management():
    """PATTERN 2: State Management - Data flows through steps."""
    clear_screen()
    print("\n" + "=" * 70)
    print("PATTERN 2: STATE MANAGEMENT - Data Flows Through Steps")
    print("=" * 70)
    
    print("\n📖 Concept:")
    print("  Each step uses outputs from previous steps via workflow context.")
    print("  Without state: Steps can't depend on each other.")
    print("  With state: Steps build on prior results.\n")
    
    input("Press [ENTER] to see WITHOUT state management...")
    
    # WITHOUT state
    print("\n" + "-" * 70)
    print("WITHOUT STATE MANAGEMENT:")
    print("-" * 70)
    print(f"\nStep 1: Query customer data")
    print(f"  Output: customer_list.json")
    print(f"\nStep 2: Analyze customer data")
    print(f"  Input: ??? (can't access Step 1 output)")
    print(f"  Must hardcode data path or requery")
    print(f"\n⚠️  Steps are isolated. Data coupling is fragile.")
    
    input("\nPress [ENTER] to see WITH state management...")
    
    # WITH state
    print("\n" + "-" * 70)
    print("WITH STATE MANAGEMENT:")
    print("-" * 70)
    
    context = WorkflowContext()
    
    # Step 1: Query
    print(f"\nStep 1: Query customer data")
    customer_data = {"customers": [{"id": 1, "name": "Acme"}, {"id": 2, "name": "TechCorp"}]}
    context.add_output("Query", customer_data)
    print(f"  Output: {len(customer_data['customers'])} customers queried")
    
    # Step 2: Analyze (uses Step 1 output)
    print(f"\nStep 2: Analyze customer data")
    query_result = context.get_output("Query")
    print(f"  Input: Retrieved from context (from Step 1)")
    print(f"  Data: {query_result}")
    analysis_result = {"total_customers": len(query_result['customers']), "status": "healthy"}
    context.add_output("Analyze", analysis_result)
    print(f"  Output: {analysis_result}")
    
    # Step 3: Generate (uses Step 2 output)
    print(f"\nStep 3: Generate report")
    analysis = context.get_output("Analyze")
    print(f"  Input: Retrieved from context (from Step 2)")
    print(f"  Data: {analysis}")
    print(f"  Output: Executive Report generated")
    
    print(f"\n✅ State flows seamlessly: Step1 → Step2 → Step3")
    
    print("\n" + "-" * 70)
    input("Press [ENTER] to return to menu...")


def demo_execution_history():
    """PATTERN 3: Execution History & Learning"""
    clear_screen()
    print("\n" + "=" * 70)
    print("PATTERN 3: EXECUTION HISTORY & LEARNING")
    print("=" * 70)
    
    print("\n📖 Concept:")
    print("  Store execution history to improve future runs.")
    print("  Without history: Each run is new, no learning.")
    print("  With history: Agent learns optimal paths and timing.\n")
    
    input("Press [ENTER] to see WITHOUT execution history...")
    
    # WITHOUT history
    print("\n" + "-" * 70)
    print("WITHOUT EXECUTION HISTORY:")
    print("-" * 70)
    print(f"\nRun 1: Executive report workflow")
    print(f"  Execution time: 2.3s")
    print(f"  Success: Yes")
    print(f"\nRun 2: Executive report workflow")
    print(f"  Agent: 'I'll try the same approach as always'")
    print(f"  Execution time: 2.3s")
    print(f"\nRun 3: Executive report workflow")
    print(f"  Agent: 'No idea what worked best last time'")
    print(f"  Execution time: 2.1s (lucky)")
    print(f"\n⚠️  No learning. Same approach every time.")
    
    input("\nPress [ENTER] to see WITH execution history...")
    
    # WITH history
    print("\n" + "-" * 70)
    print("WITH EXECUTION HISTORY:")
    print("-" * 70)
    
    agent = Agent(name="WorkflowAgent", use_memory=True)
    
    print(f"\nRun 1: Executive report workflow")
    agent.memory.episodic.record_episode(
        agent.name,
        "workflow_execution",
        {"name": "Executive Report", "duration": 2.3, "success": True, "steps_optimized": False}
    )
    print(f"  Duration: 2.3s, Success: ✓")
    print(f"  Stored in episodic memory")
    
    print(f"\nRun 2: Executive report workflow")
    agent.memory.episodic.record_episode(
        agent.name,
        "workflow_execution",
        {"name": "Executive Report", "duration": 2.1, "success": True, "steps_optimized": True}
    )
    print(f"  Agent recalls: 'Skipping Query step improved performance'")
    print(f"  Duration: 2.1s, Success: ✓")
    
    print(f"\nRun 3: Executive report workflow")
    agent.memory.episodic.record_episode(
        agent.name,
        "workflow_execution",
        {"name": "Executive Report", "duration": 1.9, "success": True, "steps_optimized": True}
    )
    print(f"  Agent: 'Apply optimization from Runs 1-2'")
    print(f"  Duration: 1.9s, Success: ✓ (17% faster than Run 1)")
    
    # Show learning
    episodes = agent.memory.episodic.get_episodes(agent.name, "workflow_execution", limit=3)
    print(f"\n✅ Execution history ({len(episodes)} runs):")
    print(f"  Learned: Skip Query step when cache is fresh")
    print(f"  Learned: Optimal run order reduces duration")
    print(f"  Performance trend: 2.3s → 2.1s → 1.9s (improving)")
    
    print("\n" + "-" * 70)
    input("Press [ENTER] to return to menu...")


def demo_error_handling():
    """PATTERN 4: Error Handling & Recovery"""
    clear_screen()
    print("\n" + "=" * 70)
    print("PATTERN 4: ERROR HANDLING & RECOVERY")
    print("=" * 70)
    
    print("\n📖 Concept:")
    print("  Workflows must handle failures gracefully with retries.")
    print("  Without error handling: Single failure stops entire workflow.")
    print("  With error handling: Workflows recover or degrade gracefully.\n")
    
    input("Press [ENTER] to see WITHOUT error handling...")
    
    # WITHOUT error handling
    print("\n" + "-" * 70)
    print("WITHOUT ERROR HANDLING:")
    print("-" * 70)
    print(f"\nWorkflow execution:")
    print(f"  Step 1: Query metrics ✓")
    print(f"  Step 2: Analyze data ✗ (API timeout)")
    print(f"  Step 3: Generate report ⊘ (skipped)")
    print(f"  Result: FAILED")
    print(f"\n⚠️  Single failure cascades. No recovery.")
    
    input("\nPress [ENTER] to see WITH error handling...")
    
    # WITH error handling
    print("\n" + "-" * 70)
    print("WITH ERROR HANDLING:")
    print("-" * 70)
    
    context = WorkflowContext()
    
    print(f"\nWorkflow execution:")
    print(f"  Step 1: Query metrics ✓")
    context.add_output("Query", {"data": "cached"})
    
    print(f"  Step 2: Analyze data")
    print(f"    Attempt 1: API timeout ✗")
    print(f"    Attempt 2: Retry with timeout=10s")
    print(f"    Result: ✓ (recovered)")
    context.add_output("Analyze", {"status": "recovered"})
    
    print(f"  Step 3: Generate report")
    print(f"    Input: Use fallback template (from Step 2)")
    print(f"    Result: ✓")
    context.add_output("Report", {"status": "generated", "type": "minimal"})
    
    context.finish()
    duration = context.get_duration_seconds()
    
    print(f"\n  Result: PARTIAL SUCCESS (degraded mode)")
    print(f"  Duration: {duration:.2f}s")
    print(f"  Errors logged: 1 (API timeout - retried)")
    
    print(f"\n✅ Workflow completes despite failure")
    print(f"✅ Error recorded in memory for pattern learning")
    
    print("\n" + "-" * 70)
    input("Press [ENTER] to return to menu...")


def main():
    """Main menu loop."""
    validate_api_key()
    
    patterns = {
        "1": ("Workflow Definition", demo_workflow_definition),
        "2": ("State Management", demo_state_management),
        "3": ("Execution History", demo_execution_history),
        "4": ("Error Handling", demo_error_handling),
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
    print("MODULE 6, LESSON 6.5: AUTONOMOUS WORKFLOWS")
    print("=" * 70)
    print("\nWorkflows combine agents + tools + scheduling for automation.")
    print("Each pattern shows: Manual execution vs Autonomous workflow\n")
    input("Press [ENTER] to start...\n")
    
    main()
