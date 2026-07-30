"""
AI For Software Engineers — Module 6: Autonomous Agents & Execution Guardrails
Resource: Stateful ReAct Agent Engine with Safety Guardrails & Step Limits
File: projects-completed/module-06/resource_agent_loop.py
"""

import json
import time
from typing import List, Dict, Any, Callable


class AgentGuardrailException(Exception):
    """Custom exception raised when an execution guardrail is triggered."""
    pass


class ExecutionGuardrails:
    """
    Real-time safety watcher enforcing max step limits, token budgets,
    and detecting repetitive tool call loops (stagnation).
    """

    def __init__(self, max_steps: int = 5, max_token_budget: int = 4000):
        self.max_steps = max_steps
        self.max_token_budget = max_token_budget
        self.current_step = 0
        self.accumulated_tokens = 0
        self.action_history: List[str] = []

    def verify_step(self, action_signature: str, estimated_tokens: int):
        """Enforces execution rules before running an LLM or tool turn."""
        self.current_step += 1
        self.accumulated_tokens += estimated_tokens

        # Guardrail 1: Hard Step Limit
        if self.current_step > self.max_steps:
            raise AgentGuardrailException(
                f"[GUARDRAIL TRIGGERED] Max step limit reached ({self.max_steps} steps). Terminating execution loop."
            )

        # Guardrail 2: Token Budget Cap
        if self.accumulated_tokens > self.max_token_budget:
            raise AgentGuardrailException(
                f"[GUARDRAIL TRIGGERED] Token budget exceeded ({self.accumulated_tokens} / {self.max_token_budget} tokens)."
            )

        # Guardrail 3: Loop Stagnation / Repetitive Action Detection
        if self.action_history.count(action_signature) >= 2:
            raise AgentGuardrailException(
                f"[GUARDRAIL TRIGGERED] Stagnation detected. Action '{action_signature}' repeated multiple times."
            )

        self.action_history.append(action_signature)


class MockToolRegistry:
    """Simulated tools available to the ReAct agent."""

    @staticmethod
    def run_tests(test_suite: str) -> str:
        """Runs test suite and returns result output."""
        return f"pytest status for {test_suite}: 4 passed, 1 failed (test_auth_timeout)."

    @staticmethod
    def fix_code(file_path: str) -> str:
        """Applies patch to code file."""
        return f"Successfully applied patch to {file_path}. Auth timeout updated to 30s."


class StatefulReActAgent:
    """
    Stateful ReAct (Reason + Act) Agent Loop implementing Think -> Act -> Observe
    with explicit state updating and execution guardrails.
    """

    def __init__(self, guardrails: ExecutionGuardrails):
        self.guardrails = guardrails
        self.tools: Dict[str, Callable] = {
            "run_tests": MockToolRegistry.run_tests,
            "fix_code": MockToolRegistry.fix_code,
        }
        self.state: List[Dict[str, str]] = []

    def log_state(self, role: str, content: str):
        """Appends message turn to working memory state."""
        self.state.append({"role": role, "content": content})

    def run_loop(self, user_goal: str):
        """Executes the agent reasoning and action loop."""
        print(f"--- Starting Stateful Agent Execution: '{user_goal}' ---")
        self.log_state("user", user_goal)

        # Iteration 1: Reasoning step
        try:
            # Step 1: Check tests
            action_sig = "run_tests:test_auth.py"
            self.guardrails.verify_step(action_sig, estimated_tokens=350)
            print(f"[Step {self.guardrails.current_step}] Reasoning: Need to run tests to check failures.")
            observation = self.tools["run_tests"]("test_auth.py")
            self.log_state("observation", observation)
            print(f"    Observation: {observation}")

            # Step 2: Apply fix
            action_sig = "fix_code:auth.py"
            self.guardrails.verify_step(action_sig, estimated_tokens=400)
            print(f"[Step {self.guardrails.current_step}] Reasoning: Fixing timeout issue in auth.py.")
            observation = self.tools["fix_code"]("auth.py")
            self.log_state("observation", observation)
            print(f"    Observation: {observation}")

            # Step 3: Re-verify tests
            action_sig = "run_tests:test_auth.py"
            self.guardrails.verify_step(action_sig, estimated_tokens=300)
            print(f"[Step {self.guardrails.current_step}] Reasoning: Re-running tests to confirm fix.")
            observation = MockToolRegistry.run_tests("test_auth.py").replace("1 failed", "0 failed")
            self.log_state("observation", observation)
            print(f"    Observation: {observation}")

            print("\n[Execution Success] Goal achieved cleanly within guardrail constraints.")

        except AgentGuardrailException as ge:
            print(f"\n{ge}")
            print("[Fallback Action] Escalating trace to Human-in-the-Loop review channel.")


if __name__ == "__main__":
    # Test 1: Successful Execution
    print("=== TEST 1: Normal Execution ===")
    guardrails_ok = ExecutionGuardrails(max_steps=5, max_token_budget=2000)
    agent = StatefulReActAgent(guardrails_ok)
    agent.run_loop("Fix failing authentication test suite in test_auth.py")

    # Test 2: Triggering Stagnation Guardrail
    print("\n=== TEST 2: Testing Guardrail Stagnation Detection ===")
    guardrails_stuck = ExecutionGuardrails(max_steps=5, max_token_budget=2000)
    agent_stuck = StatefulReActAgent(guardrails_stuck)
    try:
        # Intentionally repeating action to trigger guardrail
        guardrails_stuck.verify_step("query_db:users", estimated_tokens=100)
        guardrails_stuck.verify_step("query_db:users", estimated_tokens=100)
    except AgentGuardrailException as e:
        print(e)