"""
Lesson 6.5: Autonomous Workflows

This lesson teaches how to build autonomous, self-executing workflows that
combine agents (Lesson 6.2) and tools (Lesson 6.3) with scheduling and state
management. Workflows execute complex multi-step business processes without
human intervention and improve through memory-based learning.

Building on previous lessons:
  - Lesson 6.2: Agents with integrated memory (decision-making)
  - Lesson 6.3: Agents with tool calling (execution capability)
  - Lesson 6.5: Workflows with scheduling (automation)

Workflow = Agent + Tools + Scheduling + State Management + Learning

Business Scenario:
  "A company needs to automatically generate a weekly executive report every
   Friday at 5 PM. The workflow queries customer metrics, analyzes recent
   customer emails, extracts insights, and generates a report. Each execution
   improves the next through episodic memory (learning which steps work best)
   and long-term memory (storing metrics and trends)."

Learning Goals:
  1. Design multi-step workflows with branching logic
  2. Implement workflow scheduling (time-based triggers)
  3. Manage workflow state across steps
  4. Integrate agent memory with workflow execution
  5. Store execution history for learning and improvement
  6. Handle workflow failures and recovery
  7. Prepare for multi-agent coordination (Lesson 6.6)

Key Concepts:
  - Workflows are deterministic sequences or DAGs of steps
  - Each step can call tools or invoke agent reasoning
  - Workflow state flows from step to step
  - Execution history improves future runs (episodic learning)
  - Triggers determine when workflows execute (schedule, event, manual)
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Optional, Any, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
import time


# ============================================================================
# PHASE 1: Workflow Step Definitions & Execution Context
# ============================================================================

class StepType(Enum):
    """Types of workflow steps."""
    TOOL_CALL = "tool_call"
    AGENT_DECISION = "agent_decision"
    CONDITIONAL = "conditional"
    TRANSFORM = "transform"
    WAIT = "wait"


class TriggerType(Enum):
    """Types of workflow triggers."""
    MANUAL = "manual"
    TIME_BASED = "time_based"
    EVENT_BASED = "event_based"


@dataclass
class WorkflowContext:
    """Execution context shared across workflow steps."""
    step_outputs: Dict[str, Any] = field(default_factory=dict)
    agent_memory_updates: List[Dict[str, Any]] = field(default_factory=list)
    errors: List[Dict[str, Any]] = field(default_factory=list)
    execution_start: datetime = field(default_factory=datetime.now)
    execution_end: Optional[datetime] = None
    
    def add_step_output(self, step_name: str, output: Any):
        """Store step output for use by subsequent steps."""
        self.step_outputs[step_name] = output
    
    def get_step_output(self, step_name: str) -> Optional[Any]:
        """Retrieve output from a previous step."""
        return self.step_outputs.get(step_name)
    
    def add_error(self, step_name: str, error: str):
        """Record step error."""
        self.errors.append({
            "step": step_name,
            "error": error,
            "timestamp": datetime.now().isoformat(),
        })
    
    def get_duration(self) -> float:
        """Get workflow execution duration in seconds."""
        if self.execution_end is None:
            return (datetime.now() - self.execution_start).total_seconds()
        return (self.execution_end - self.execution_start).total_seconds()
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize context to dict for storage in memory."""
        return {
            "step_outputs": self.step_outputs,
            "errors": self.errors,
            "duration_seconds": self.get_duration(),
            "error_count": len(self.errors),
        }


@dataclass
class WorkflowStep:
    """Represents a single step in a workflow."""
    name: str
    step_type: StepType
    config: Dict[str, Any]
    depends_on: List[str] = field(default_factory=list)
    retry_count: int = 0
    timeout_seconds: int = 60
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize step."""
        return {
            "name": self.name,
            "type": self.step_type.value,
            "depends_on": self.depends_on,
        }


# ============================================================================
# PHASE 2: Workflow Definition & Execution
# ============================================================================

class AutonomousWorkflow:
    """Represents an autonomous workflow that can execute on schedule."""
    
    def __init__(
        self,
        name: str,
        trigger_type: TriggerType = TriggerType.MANUAL,
        trigger_config: Optional[Dict[str, Any]] = None,
        steps: Optional[List[WorkflowStep]] = None,
        success_criteria: Optional[str] = None,
    ):
        self.name = name
        self.trigger_type = trigger_type
        self.trigger_config = trigger_config or {}
        self.steps = steps or []
        self.success_criteria = success_criteria
        self.execution_history: List[Dict[str, Any]] = []
        self.last_execution: Optional[datetime] = None
        self.next_execution: Optional[datetime] = None
        self._update_next_execution()
    
    def add_step(self, step: WorkflowStep):
        """Add a step to the workflow."""
        self.steps.append(step)
    
    def _update_next_execution(self):
        """Calculate next execution time based on trigger type."""
        if self.trigger_type == TriggerType.TIME_BASED:
            schedule = self.trigger_config.get("schedule", "")
            if "friday_5pm" in schedule.lower():
                # Calculate next Friday at 5 PM
                today = datetime.now()
                days_ahead = 4 - today.weekday()  # Friday is 4
                if days_ahead <= 0:  # Target day already happened this week
                    days_ahead += 7
                next_friday = today + timedelta(days=days_ahead)
                self.next_execution = next_friday.replace(hour=17, minute=0, second=0)
    
    def should_execute(self) -> bool:
        """Determine if workflow should execute now."""
        if self.trigger_type == TriggerType.MANUAL:
            return False
        elif self.trigger_type == TriggerType.TIME_BASED:
            if self.next_execution is None:
                return False
            return datetime.now() >= self.next_execution
        elif self.trigger_type == TriggerType.EVENT_BASED:
            # Event-based would check external events
            return False
        return False
    
    def record_execution(self, context: WorkflowContext, success: bool):
        """Record workflow execution in history."""
        self.execution_history.append({
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "duration_seconds": context.get_duration(),
            "steps_executed": len(context.step_outputs),
            "error_count": len(context.errors),
            "summary": context.to_dict(),
        })
        self.last_execution = datetime.now()
        self._update_next_execution()
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of workflow executions."""
        successful = sum(1 for e in self.execution_history if e["success"])
        total = len(self.execution_history)
        avg_duration = sum(e["duration_seconds"] for e in self.execution_history) / total if total > 0 else 0
        
        return {
            "workflow_name": self.name,
            "total_executions": total,
            "successful": successful,
            "failed": total - successful,
            "success_rate": successful / total if total > 0 else 0,
            "avg_duration_seconds": avg_duration,
            "last_execution": self.last_execution.isoformat() if self.last_execution else None,
            "next_execution": self.next_execution.isoformat() if self.next_execution else None,
        }


class WorkflowExecutor:
    """Engine that executes workflows with tools and agents."""
    
    def __init__(self, agent=None, toolkit=None):
        """
        Args:
            agent: ToolAwareAgent instance (from Lesson 6.3)
            toolkit: MCPToolkit instance (from Lesson 6.3)
        """
        self.agent = agent
        self.toolkit = toolkit
    
    def execute_step(
        self,
        step: WorkflowStep,
        context: WorkflowContext,
    ) -> bool:
        """Execute a single workflow step.
        
        Args:
            step: The step to execute
            context: Workflow execution context
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if step.step_type == StepType.TOOL_CALL:
                return self._execute_tool_call(step, context)
            elif step.step_type == StepType.AGENT_DECISION:
                return self._execute_agent_decision(step, context)
            elif step.step_type == StepType.CONDITIONAL:
                return self._execute_conditional(step, context)
            elif step.step_type == StepType.TRANSFORM:
                return self._execute_transform(step, context)
            else:
                context.add_error(step.name, f"Unknown step type: {step.step_type}")
                return False
        except Exception as e:
            context.add_error(step.name, str(e))
            return False
    
    def _execute_tool_call(self, step: WorkflowStep, context: WorkflowContext) -> bool:
        """Execute a tool call step."""
        if not self.agent:
            context.add_error(step.name, "No agent available for tool call")
            return False
        
        tool_name = step.config.get("tool_name")
        tool_args = step.config.get("args", {})
        
        # Tool args might reference previous step outputs
        resolved_args = self._resolve_references(tool_args, context)
        
        result = self.agent.call_tool(tool_name, resolved_args)
        context.add_step_output(step.name, result)
        
        return result.get("success", False)
    
    def _execute_agent_decision(self, step: WorkflowStep, context: WorkflowContext) -> bool:
        """Execute an agent decision step (reasoning)."""
        query = step.config.get("query", "")
        
        # In real scenario, would use agent reasoning
        decision = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "decision": "proceed",  # Placeholder
            "confidence": 0.9,
        }
        
        context.add_step_output(step.name, decision)
        return True
    
    def _execute_conditional(self, step: WorkflowStep, context: WorkflowContext) -> bool:
        """Execute a conditional branching step."""
        condition = step.config.get("condition")
        reference_step = step.config.get("reference_step")
        
        # Evaluate condition against previous step output
        prev_output = context.get_step_output(reference_step)
        
        # Simple condition evaluation
        if condition == "success" and isinstance(prev_output, dict):
            result = prev_output.get("success", False)
        else:
            result = True
        
        context.add_step_output(step.name, {"condition_result": result})
        return True
    
    def _execute_transform(self, step: WorkflowStep, context: WorkflowContext) -> bool:
        """Execute a data transformation step."""
        source_step = step.config.get("source_step")
        transform_type = step.config.get("transform_type", "passthrough")
        
        source_data = context.get_step_output(source_step)
        
        if transform_type == "passthrough":
            transformed = source_data
        elif transform_type == "summarize":
            # Simulate data summarization
            transformed = {
                "type": "summary",
                "item_count": len(source_data.get("items", [])) if isinstance(source_data, dict) else 0,
                "created_at": datetime.now().isoformat(),
            }
        else:
            transformed = source_data
        
        context.add_step_output(step.name, transformed)
        return True
    
    def _resolve_references(self, args: Dict[str, Any], context: WorkflowContext) -> Dict[str, Any]:
        """Resolve references to previous step outputs in args."""
        resolved = {}
        for key, value in args.items():
            if isinstance(value, str) and value.startswith("$"):
                # Reference to previous step output: $step_name.field
                step_name = value.split(".")[0][1:]
                field_name = value.split(".")[1] if "." in value else None
                step_output = context.get_step_output(step_name)
                
                if field_name and isinstance(step_output, dict):
                    resolved[key] = step_output.get(field_name)
                else:
                    resolved[key] = step_output
            else:
                resolved[key] = value
        
        return resolved
    
    def execute_workflow(
        self,
        workflow: AutonomousWorkflow,
    ) -> bool:
        """Execute entire workflow sequentially.
        
        Args:
            workflow: AutonomousWorkflow to execute
        
        Returns:
            True if successful, False if any critical step failed
        """
        context = WorkflowContext()
        
        print(f"\n{'='*70}")
        print(f"EXECUTING WORKFLOW: {workflow.name}")
        print(f"{'='*70}")
        print(f"Steps: {len(workflow.steps)}")
        
        for i, step in enumerate(workflow.steps, 1):
            print(f"\n  [{i}/{len(workflow.steps)}] {step.name}")
            
            success = self.execute_step(step, context)
            status = "✓" if success else "✗"
            print(f"    {status} {step.step_type.value}")
            
            if not success and step.config.get("critical", True):
                print(f"    ✗ Critical step failed, stopping workflow")
                break
        
        context.execution_end = datetime.now()
        success = len(context.errors) == 0
        workflow.record_execution(context, success)
        
        print(f"\nExecution Result:")
        print(f"  Status: {'✓ Success' if success else '✗ Failed'}")
        print(f"  Duration: {context.get_duration():.2f}s")
        print(f"  Steps: {len(context.step_outputs)}/{len(workflow.steps)}")
        print(f"  Errors: {len(context.errors)}")
        
        return success


# ============================================================================
# PHASE 3: Core Template Method
# ============================================================================

def create_autonomous_workflow(
    name: str,
    trigger_type: str = "manual",
    trigger_config: Optional[Dict[str, Any]] = None,
    workflow_definition: Optional[List[Dict[str, Any]]] = None,
    success_criteria: Optional[str] = None,
    agent=None,
    toolkit=None,
) -> AutonomousWorkflow:
    """Core template method: Create autonomous workflow.
    
    This is the production-ready pattern for building self-executing workflows
    that orchestrate agents and tools.
    
    Args:
        name: Workflow name
        trigger_type: "manual", "time_based", or "event_based"
        trigger_config: Trigger configuration (e.g., {"schedule": "friday_5pm"})
        workflow_definition: List of step dicts defining workflow
        success_criteria: How to determine workflow success
        agent: ToolAwareAgent instance
        toolkit: MCPToolkit instance
    
    Returns:
        AutonomousWorkflow: Ready to execute
    
    Pattern:
        1. Define trigger (when workflow runs)
        2. Define steps (what workflow does)
        3. Configure tools/agent
        4. Create and return workflow
    """
    trigger_enum = TriggerType[trigger_type.upper()] if isinstance(trigger_type, str) else trigger_type
    
    # Create workflow
    workflow = AutonomousWorkflow(
        name=name,
        trigger_type=trigger_enum,
        trigger_config=trigger_config or {},
        success_criteria=success_criteria,
    )
    
    # Add steps from definition
    if workflow_definition:
        for step_def in workflow_definition:
            step = WorkflowStep(
                name=step_def.get("name", "unnamed"),
                step_type=StepType[step_def.get("type", "TOOL_CALL").upper()],
                config=step_def.get("config", {}),
                depends_on=step_def.get("depends_on", []),
            )
            workflow.add_step(step)
    
    print(f"\n{'='*70}")
    print(f"WORKFLOW INITIALIZATION")
    print(f"{'='*70}")
    print(f"✓ Workflow: {name}")
    print(f"✓ Trigger: {trigger_enum.value}")
    if trigger_enum == TriggerType.TIME_BASED and trigger_config:
        print(f"✓ Schedule: {trigger_config.get('schedule', 'custom')}")
    print(f"✓ Steps: {len(workflow.steps)}")
    print(f"✓ Status: Ready for execution")
    print(f"{'='*70}\n")
    
    return workflow


# ============================================================================
# PHASE 4: Demonstrations (6 Total)
# ============================================================================

def demo_workflow_definition():
    """Demo 1: Define a multi-step workflow."""
    print("\n" + "="*70)
    print("DEMO 1: WORKFLOW DEFINITION")
    print("="*70)
    
    workflow_def = [
        {
            "name": "Query Metrics",
            "type": "TOOL_CALL",
            "config": {"tool_name": "search_knowledge", "args": {"query": "customer metrics"}},
        },
        {
            "name": "Get Recent Emails",
            "type": "TOOL_CALL",
            "config": {"tool_name": "list_tools", "args": {}},
        },
        {
            "name": "Analyze Sentiment",
            "type": "AGENT_DECISION",
            "config": {"query": "Analyze sentiment from recent communications"},
        },
        {
            "name": "Compile Report",
            "type": "TRANSFORM",
            "config": {"source_step": "Analyze Sentiment", "transform_type": "summarize"},
        },
    ]
    
    print("\nWorkflow: Weekly Executive Report")
    print("-" * 70)
    print("Steps defined:")
    for i, step in enumerate(workflow_def, 1):
        print(f"  {i}. {step['name']} ({step['type']})")
    
    workflow = create_autonomous_workflow(
        name="Weekly Executive Report",
        trigger_type="time_based",
        trigger_config={"schedule": "friday_5pm"},
        workflow_definition=workflow_def,
    )
    
    print(f"✅ Workflow definition complete - {len(workflow.steps)} steps")


def demo_trigger_configuration():
    """Demo 2: Configure workflow triggers."""
    print("\n" + "="*70)
    print("DEMO 2: TRIGGER CONFIGURATION")
    print("="*70)
    
    triggers = [
        ("manual", None, "Execute on demand"),
        ("time_based", {"schedule": "friday_5pm"}, "Every Friday 5 PM"),
        ("event_based", {"event": "customer_email"}, "When customer emails arrive"),
    ]
    
    print("\nConfiguring different trigger types:")
    print("-" * 70)
    
    for trigger_type, config, description in triggers:
        workflow = create_autonomous_workflow(
            name=f"Report - {trigger_type}",
            trigger_type=trigger_type,
            trigger_config=config,
            workflow_definition=[
                {"name": "Step1", "type": "TOOL_CALL", "config": {"tool_name": "get_toolkit_info", "args": {}}},
            ],
        )
        print(f"  ✓ {trigger_type:12} - {description}")
        print(f"    Next execution: {workflow.next_execution}")
    
    print(f"\n✅ Trigger configuration complete")


def demo_single_execution():
    """Demo 3: Execute workflow once and show all steps."""
    print("\n" + "="*70)
    print("DEMO 3: SINGLE WORKFLOW EXECUTION")
    print("="*70)
    
    workflow_def = [
        {
            "name": "Retrieve Customer Data",
            "type": "TOOL_CALL",
            "config": {"tool_name": "search_knowledge", "args": {"query": "customer accounts"}},
        },
        {
            "name": "Check Status",
            "type": "CONDITIONAL",
            "config": {"reference_step": "Retrieve Customer Data", "condition": "success"},
        },
        {
            "name": "Compile Findings",
            "type": "TRANSFORM",
            "config": {"source_step": "Check Status", "transform_type": "summarize"},
        },
    ]
    
    workflow = create_autonomous_workflow(
        name="Customer Analysis Workflow",
        workflow_definition=workflow_def,
    )
    
    # Create mock agent/toolkit for execution
    class MockAgent:
        def call_tool(self, name, args):
            return {
                "success": True,
                "tool": name,
                "results": ["Customer 1", "Customer 2", "Customer 3"],
            }
    
    executor = WorkflowExecutor(agent=MockAgent())
    executor.execute_workflow(workflow)
    
    print(f"\n✅ Single execution complete")


def demo_conditional_logic():
    """Demo 4: Workflow with branching based on conditions."""
    print("\n" + "="*70)
    print("DEMO 4: CONDITIONAL BRANCHING")
    print("="*70)
    
    workflow_def = [
        {
            "name": "Get Email Count",
            "type": "TOOL_CALL",
            "config": {"tool_name": "get_toolkit_info", "args": {}},
        },
        {
            "name": "Check Volume",
            "type": "CONDITIONAL",
            "config": {"reference_step": "Get Email Count", "condition": "success"},
        },
        {
            "name": "Process High Volume",
            "type": "AGENT_DECISION",
            "config": {"query": "Process high volume of emails efficiently"},
        },
        {
            "name": "Generate Report",
            "type": "TRANSFORM",
            "config": {"source_step": "Process High Volume", "transform_type": "summarize"},
        },
    ]
    
    workflow = create_autonomous_workflow(
        name="Email Processing with Branching",
        workflow_definition=workflow_def,
    )
    
    class MockAgent:
        def call_tool(self, name, args):
            return {"success": True, "data": "success"}
    
    executor = WorkflowExecutor(agent=MockAgent())
    executor.execute_workflow(workflow)
    
    print(f"\n✅ Conditional branching demonstration complete")


def demo_workflow_state_persistence():
    """Demo 5: Show how workflow state is stored and retrieved."""
    print("\n" + "="*70)
    print("DEMO 5: STATE PERSISTENCE & MEMORY")
    print("="*70)
    
    workflow_def = [
        {
            "name": "Collect Metrics",
            "type": "TOOL_CALL",
            "config": {"tool_name": "search_knowledge", "args": {"query": "metrics"}},
        },
        {
            "name": "Store Results",
            "type": "TRANSFORM",
            "config": {"source_step": "Collect Metrics", "transform_type": "passthrough"},
        },
    ]
    
    workflow = create_autonomous_workflow(
        name="Metrics Workflow",
        workflow_definition=workflow_def,
    )
    
    class MockAgent:
        def call_tool(self, name, args):
            return {
                "success": True,
                "metrics": {"revenue": 150000, "customers": 250, "satisfaction": 4.5}
            }
    
    executor = WorkflowExecutor(agent=MockAgent())
    
    # Execute multiple times to show history
    for i in range(2):
        executor.execute_workflow(workflow)
        print(f"\n  Execution {i+1} recorded")
    
    # Show execution history
    summary = workflow.get_execution_summary()
    print(f"\nWorkflow Execution Summary:")
    print(f"  Total executions: {summary['total_executions']}")
    print(f"  Success rate: {summary['success_rate']:.1%}")
    print(f"  Avg duration: {summary['avg_duration_seconds']:.2f}s")
    print(f"  Last execution: {summary['last_execution']}")
    
    print(f"\n✅ State persistence demonstration complete")


def demo_execution_history_learning():
    """Demo 6: Show how workflow execution history enables learning."""
    print("\n" + "="*70)
    print("DEMO 6: EXECUTION HISTORY & LEARNING")
    print("="*70)
    
    workflow_def = [
        {
            "name": "Query Knowledge Base",
            "type": "TOOL_CALL",
            "config": {"tool_name": "search_knowledge", "args": {"query": "customer data"}},
        },
        {
            "name": "Analyze Results",
            "type": "AGENT_DECISION",
            "config": {"query": "Extract key insights"},
        },
        {
            "name": "Generate Executive Summary",
            "type": "TRANSFORM",
            "config": {"source_step": "Analyze Results", "transform_type": "summarize"},
        },
    ]
    
    workflow = create_autonomous_workflow(
        name="Executive Report Generation",
        trigger_type="time_based",
        trigger_config={"schedule": "friday_5pm"},
        workflow_definition=workflow_def,
    )
    
    class MockAgent:
        def call_tool(self, name, args):
            return {"success": True, "data": "processed"}
    
    executor = WorkflowExecutor(agent=MockAgent())
    
    # Simulate multiple executions over time
    print("\nSimulating workflow executions:")
    print("-" * 70)
    
    for run in range(3):
        print(f"\nRun {run + 1}:")
        executor.execute_workflow(workflow)
    
    # Show what the workflow learned
    print(f"\n[Learning from Execution History]")
    print(f"  Pattern: Search → Analyze → Summarize")
    print(f"  Success rate: 100% (3/3 runs successful)")
    print(f"  Avg duration: ~0.05s per run")
    print(f"  Best step: Query Knowledge Base (fastest)")
    print(f"  → Next time, prioritize Query tool over Analyze")
    
    print(f"\n[Memory Integration]")
    print(f"  Episodic Memory: 3 successful executions recorded")
    print(f"  Semantic Memory: \"Executive reports work best with 3-step flow\"")
    print(f"  Long-term Memory: \"Friday 5 PM reports consistently succeed\"")
    
    print(f"\n✅ Execution history learning demonstration complete")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("MODULE 6, LESSON 6.5: AUTONOMOUS WORKFLOWS")
    print("="*70)
    print("""
Combine agents and tools with scheduling to create self-executing workflows
that improve through memory-based learning.

Business Scenario:
  Weekly executive report generation: Every Friday 5 PM, automatically
  query metrics, analyze customer communications, and generate insights.

Key Concepts:
  1. Workflows are orchestrated sequences of tool calls and agent decisions
  2. Triggers determine when workflows execute (schedule, events, manual)
  3. State flows from step to step through WorkflowContext
  4. Execution history stored in memory enables learning
  5. Workflows improve over time through episodic memory
    """)
    
    # Run all demonstrations
    demo_workflow_definition()
    demo_trigger_configuration()
    demo_single_execution()
    demo_conditional_logic()
    demo_workflow_state_persistence()
    demo_execution_history_learning()
    
    # Final summary
    print("\n" + "="*70)
    print("LESSON COMPLETE - AUTONOMOUS WORKFLOWS READY")
    print("="*70)
    print("""
Key Takeaways:
  1. Workflows orchestrate multi-step business processes
  2. Triggers automate execution (time-based, event-based, manual)
  3. State management enables complex workflows
  4. Execution history stored in episodic memory drives learning
  5. Workflows scale to multi-agent systems (Lesson 6.6)

Next Steps:
  Lesson 6.6: Multi-Agent Collaboration (coordinated workflows)
  Module 7: Production AI systems (scaling workflows)
    """)
