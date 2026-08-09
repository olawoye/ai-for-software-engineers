"""
Lesson 7.5: Evaluation & Performance Frameworks for AI Systems

This lesson teaches how to systematically evaluate AI systems using reusable evaluation
frameworks that measure retrieval quality, agent performance, system efficiency, and
business impact. This is a PRODUCTION-READY TOOL designed to be extracted and used
in learner's own projects.

Business Scenario:
  "A company deployed AI agents (from Module 6) but can't measure whether the system
   is working. They need evaluation frameworks to measure:
   - Retrieval quality (for RAG systems)
   - Agent success rates (for autonomous agents)
   - System efficiency (latency, throughput, cost)
   - Business impact (workflow completion, time savings)"

Core Design Principle: Reusable Tool
  This implementation is NOT just a course demo. It's designed as:
  1. Modular components (TestCase, Metric, EvaluationResult)
  2. Pluggable evaluators (easy to add new types)
  3. Framework-agnostic (works with ANY AI system)
  4. Extract-and-use pattern (copy into your projects)
  5. Reporting & benchmarking (track improvement over time)

Learning Goals:
  1. Design test datasets with meaningful test cases
  2. Define and calculate evaluation metrics
  3. Compare systems using benchmarks
  4. Generate evaluation reports with insights
  5. Build extensible evaluation frameworks for production systems

TEMPLATE-FIRST PATTERN:
  Primary Method: create_evaluation_framework()
    - Takes system config, evaluation types, test dataset
    - Returns ready-to-use EvaluationFramework
    - Designed as reusable pattern for learner projects

DEMONSTRATIONS (4-5 total):
  1. RAG Evaluation — Test retrieval quality on knowledge queries
  2. Agent Evaluation — Test agent success using Module 6 agents
  3. System Evaluation — Measure latency, throughput, cost
  4. Business Evaluation — Workflow completion, time savings
  5. Benchmark Tracking — Show improvement across multiple runs

KEY CLASSES (Reusable):
  - TestCase: Define test scenarios
  - Metric: Calculate performance measurements
  - EvaluationResult: Score test cases
  - EvaluationFramework: Container (main template)
  - Benchmark: Track improvement over time
  - EvaluationReport: Generate reports with insights

USAGE PATTERN FOR LEARNERS:
  ```python
  # Step 1: Create evaluation framework
  framework = create_evaluation_framework(
      framework_name="My RAG System Evaluator",
      evaluation_types=["rag", "system"],
      test_dataset=my_test_cases,
      metrics_config=my_metrics
  )
  
  # Step 2: Run evaluation
  results = framework.evaluate_system(my_rag_system)
  
  # Step 3: Generate report
  report = framework.generate_report()
  
  # Step 4: Compare against baseline
  improvement = framework.compare_to_baseline(baseline_results)
  ```

This pattern works for:
  - RAG systems (retrieval evaluation)
  - Agent systems (task completion evaluation)
  - Chat systems (response quality evaluation)
  - Any AI system that needs measurement
"""

import json
import time
import os
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Callable, Tuple
from enum import Enum
from datetime import datetime
from collections import defaultdict


# ============================================================================
# PHASE 1: Core Evaluation Data Structures
# ============================================================================

class EvaluationType(Enum):
    """Types of evaluation available in the framework."""
    RAG = "rag"  # Retrieval quality
    AGENT = "agent"  # Task completion
    SYSTEM = "system"  # Latency, throughput, cost
    BUSINESS = "business"  # Workflow outcomes


@dataclass
class TestCase:
    """
    Represents a single test case for evaluation.
    
    Reusable across any AI system evaluation:
    - RAG: query → expected documents
    - Agent: task → expected completion
    - System: request → expected response time
    - Business: workflow → expected outcome
    """
    test_id: str
    test_type: str  # "retrieval", "agent_task", "latency", "business_flow"
    input_data: Dict[str, Any]
    expected_output: Any
    success_criteria: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert test case to dictionary."""
        return {
            "test_id": self.test_id,
            "test_type": self.test_type,
            "input_data": self.input_data,
            "expected_output": self.expected_output,
            "success_criteria": self.success_criteria,
            "metadata": self.metadata,
        }


@dataclass
class Metric:
    """
    Represents a measurable performance metric.
    
    Reusable metric patterns:
    - Precision: Correct out of total (for retrieval)
    - Recall: Relevant found out of total relevant
    - LatencyP95: 95th percentile latency
    - CostPerRequest: Total cost / request count
    - SuccessRate: Successful tasks / total tasks
    """
    name: str
    calculation_fn: Callable[[List[Dict]], float]
    unit: str  # "percentage", "seconds", "dollars", "count"
    target_value: Optional[float] = None  # Target for this metric
    
    def calculate(self, results: List[Dict]) -> float:
        """Calculate metric value from results."""
        return self.calculation_fn(results)


@dataclass
class EvaluationResult:
    """Result of evaluating a single test case."""
    test_case: TestCase
    actual_output: Any
    passed: bool
    score: float  # 0.0 to 1.0
    metrics: Dict[str, float]  # e.g., {"latency": 0.45, "precision": 0.92}
    duration: float  # execution time in seconds
    error: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Benchmark:
    """Represents benchmark results from a complete evaluation run."""
    benchmark_id: str
    evaluation_name: str
    evaluation_type: EvaluationType
    total_tests: int
    passed_tests: int
    failed_tests: int
    average_score: float
    metrics_summary: Dict[str, float]  # Aggregated metrics
    duration: float  # Total evaluation time
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    results: List[EvaluationResult] = field(default_factory=list)
    
    @property
    def pass_rate(self) -> float:
        """Calculate pass rate."""
        if self.total_tests == 0:
            return 0.0
        return self.passed_tests / self.total_tests
    
    def to_dict(self) -> Dict:
        """Convert benchmark to dictionary."""
        return {
            "benchmark_id": self.benchmark_id,
            "evaluation_name": self.evaluation_name,
            "evaluation_type": self.evaluation_type.value,
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "failed_tests": self.failed_tests,
            "pass_rate": self.pass_rate,
            "average_score": self.average_score,
            "metrics_summary": self.metrics_summary,
            "duration": duration,
            "timestamp": self.timestamp,
        }


# ============================================================================
# PHASE 2: Evaluation Framework Container
# ============================================================================

class EvaluationFramework:
    """
    Reusable evaluation framework for any AI system.
    
    This is the main reusable tool. Extract this class into your projects
    to evaluate your own AI systems.
    
    Key methods:
    - evaluate_system(): Run evaluation on a system
    - generate_report(): Create evaluation report
    - compare_to_baseline(): Track improvement over time
    - add_evaluation_type(): Extend framework with new evaluators
    """
    
    def __init__(
        self,
        framework_name: str,
        evaluation_types: List[str],
        test_dataset: List[TestCase],
        metrics_config: Optional[Dict[str, Metric]] = None,
    ):
        """
        Initialize evaluation framework.
        
        Args:
            framework_name: Name of this evaluation framework
            evaluation_types: List of evaluation types to support
                ["rag", "agent", "system", "business"]
            test_dataset: List of test cases to evaluate against
            metrics_config: Dict of metric_name -> Metric definitions
        """
        self.framework_name = framework_name
        self.evaluation_types = evaluation_types
        self.test_dataset = test_dataset
        self.metrics_config = metrics_config or {}
        
        self.evaluation_history: List[Benchmark] = []
        self.current_results: List[EvaluationResult] = []
        
        # Track evaluators for each type
        self.evaluators: Dict[str, Callable] = {
            "rag": self._evaluate_rag,
            "agent": self._evaluate_agent,
            "system": self._evaluate_system,
            "business": self._evaluate_business,
        }
    
    def evaluate_system(
        self,
        system_fn: Callable,
        evaluation_type: str = "rag",
    ) -> Benchmark:
        """
        Run evaluation on a system using test cases.
        
        Args:
            system_fn: Function that takes test input and returns output
            evaluation_type: Type of evaluation to run
                ("rag", "agent", "system", "business")
        
        Returns:
            Benchmark: Results of evaluation
        """
        start_time = time.time()
        self.current_results = []
        
        passed = 0
        failed = 0
        scores = []
        all_metrics = defaultdict(list)
        
        # Filter test cases for this evaluation type
        # More flexible matching: handles both exact matches and prefix matches
        relevant_tests = [
            t for t in self.test_dataset 
            if t.test_type.startswith(evaluation_type) or 
               evaluation_type in t.test_type or
               (evaluation_type == "rag" and "retrieval" in t.test_type) or
               (evaluation_type == "agent" and "agent_task" in t.test_type) or
               (evaluation_type == "system" and "system_" in t.test_type) or
               (evaluation_type == "business" and "business_" in t.test_type)
        ]
        
        for test_case in relevant_tests:
            try:
                # Run the system with test input
                result_start = time.time()
                actual_output = system_fn(test_case.input_data)
                result_duration = time.time() - result_start
                
                # Score the result
                score, metrics = self._score_result(test_case, actual_output)
                
                # Record result
                eval_result = EvaluationResult(
                    test_case=test_case,
                    actual_output=actual_output,
                    passed=score >= 0.8,  # Pass if score >= 80%
                    score=score,
                    metrics=metrics,
                    duration=result_duration,
                )
                
                self.current_results.append(eval_result)
                
                if eval_result.passed:
                    passed += 1
                else:
                    failed += 1
                
                scores.append(score)
                for metric_name, value in metrics.items():
                    all_metrics[metric_name].append(value)
                    
            except Exception as e:
                failed += 1
                eval_result = EvaluationResult(
                    test_case=test_case,
                    actual_output=None,
                    passed=False,
                    score=0.0,
                    metrics={},
                    duration=0.0,
                    error=str(e),
                )
                self.current_results.append(eval_result)
        
        # Calculate aggregated metrics
        metrics_summary = {}
        for metric_name, values in all_metrics.items():
            if values:
                metrics_summary[metric_name] = sum(values) / len(values)
        
        # Create benchmark result
        total_duration = time.time() - start_time
        average_score = sum(scores) / len(scores) if scores else 0.0
        
        benchmark = Benchmark(
            benchmark_id=f"bench_{int(time.time())}",
            evaluation_name=self.framework_name,
            evaluation_type=EvaluationType(evaluation_type),
            total_tests=len(relevant_tests),
            passed_tests=passed,
            failed_tests=failed,
            average_score=average_score,
            metrics_summary=metrics_summary,
            duration=total_duration,
            results=self.current_results,
        )
        
        self.evaluation_history.append(benchmark)
        return benchmark
    
    def _score_result(
        self,
        test_case: TestCase,
        actual_output: Any,
    ) -> Tuple[float, Dict[str, float]]:
        """
        Score a test result.
        
        This is extensible - override for custom scoring logic.
        Handles various output types: dicts, strings, booleans, etc.
        """
        metrics = {}
        score = 0.0
        
        # Handle dict outputs
        if isinstance(actual_output, dict) and isinstance(test_case.expected_output, dict):
            # Compare dict keys that exist in expected output
            matching_keys = 0
            total_keys = len(test_case.expected_output)
            
            if total_keys == 0:
                score = 1.0
            else:
                for key, expected_val in test_case.expected_output.items():
                    if key in actual_output:
                        actual_val = actual_output[key]
                        # For numeric values, check if close enough
                        if isinstance(expected_val, (int, float)) and isinstance(actual_val, (int, float)):
                            if abs(actual_val - expected_val) / max(abs(expected_val), 1) < 0.2:
                                matching_keys += 1
                        # For bool/string values, check equality
                        elif actual_val == expected_val or str(actual_val).lower() == str(expected_val).lower():
                            matching_keys += 1
                
                score = min(1.0, matching_keys / total_keys)
        
        # Handle string outputs
        elif isinstance(actual_output, str) and isinstance(test_case.expected_output, str):
            score = self._string_similarity(actual_output, test_case.expected_output)
        
        # Handle boolean outputs
        elif isinstance(actual_output, bool) and isinstance(test_case.expected_output, bool):
            score = 1.0 if actual_output == test_case.expected_output else 0.0
        
        # Direct equality
        elif actual_output == test_case.expected_output:
            score = 1.0
        
        # Fallback: assume partial success
        else:
            score = 0.6  # Partial credit for attempting
        
        # Add metric calculations
        if "latency" in test_case.metadata:
            metrics["latency"] = test_case.metadata["latency"]
        if "cost" in test_case.metadata:
            metrics["cost"] = test_case.metadata["cost"]
        if "time_saved" in test_case.metadata:
            metrics["time_saved"] = test_case.metadata["time_saved"]
        
        return score, metrics
    
    def _string_similarity(self, s1: str, s2: str) -> float:
        """Calculate similarity between two strings (0.0 to 1.0)."""
        if s1 == s2:
            return 1.0
        
        # Simple word overlap metric
        words1 = set(s1.lower().split())
        words2 = set(s2.lower().split())
        
        if not words1 and not words2:
            return 1.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def _evaluate_rag(self, test_input: Dict) -> Dict:
        """RAG evaluation handler."""
        # Simulate RAG evaluation
        return {
            "precision": 0.92,
            "recall": 0.88,
            "f1_score": 0.90,
        }
    
    def _evaluate_agent(self, test_input: Dict) -> Dict:
        """Agent evaluation handler."""
        # Simulate agent evaluation
        return {
            "task_success": 0.85,
            "tool_success": 0.90,
            "goal_completion": 0.80,
        }
    
    def _evaluate_system(self, test_input: Dict) -> Dict:
        """System evaluation handler."""
        # Simulate system evaluation
        return {
            "latency_p95": 0.45,
            "throughput": 100.0,
            "cost_per_request": 0.005,
        }
    
    def _evaluate_business(self, test_input: Dict) -> Dict:
        """Business evaluation handler."""
        # Simulate business evaluation
        return {
            "workflow_completion": 0.95,
            "time_saved_hours": 2.5,
            "user_satisfaction": 0.88,
        }
    
    def generate_report(self) -> Dict:
        """Generate evaluation report from last benchmark."""
        if not self.evaluation_history:
            return {"error": "No evaluation history"}
        
        latest_benchmark = self.evaluation_history[-1]
        
        report = {
            "framework_name": self.framework_name,
            "evaluation_type": latest_benchmark.evaluation_type.value,
            "timestamp": latest_benchmark.timestamp,
            "summary": {
                "total_tests": latest_benchmark.total_tests,
                "passed": latest_benchmark.passed_tests,
                "failed": latest_benchmark.failed_tests,
                "pass_rate": f"{latest_benchmark.pass_rate:.1%}",
                "average_score": f"{latest_benchmark.average_score:.2f}",
                "total_duration_s": f"{latest_benchmark.duration:.2f}",
            },
            "metrics": latest_benchmark.metrics_summary,
            "test_results": [
                {
                    "test_id": r.test_case.test_id,
                    "passed": r.passed,
                    "score": f"{r.score:.2f}",
                    "duration_s": f"{r.duration:.3f}",
                    "error": r.error,
                }
                for r in latest_benchmark.results
            ],
        }
        
        return report
    
    def compare_to_baseline(self, baseline_benchmark: Benchmark) -> Dict:
        """Compare current results to a baseline benchmark."""
        if not self.evaluation_history:
            return {"error": "No current evaluation results"}
        
        current = self.evaluation_history[-1]
        
        comparison = {
            "baseline_timestamp": baseline_benchmark.timestamp,
            "current_timestamp": current.timestamp,
            "pass_rate_change": {
                "baseline": f"{baseline_benchmark.pass_rate:.1%}",
                "current": f"{current.pass_rate:.1%}",
                "improvement": f"{(current.pass_rate - baseline_benchmark.pass_rate):.1%}",
            },
            "average_score_change": {
                "baseline": f"{baseline_benchmark.average_score:.2f}",
                "current": f"{current.average_score:.2f}",
                "improvement": f"{(current.average_score - baseline_benchmark.average_score):.2f}",
            },
            "metrics_comparison": {},
        }
        
        for metric_name in current.metrics_summary:
            baseline_value = baseline_benchmark.metrics_summary.get(metric_name, 0)
            current_value = current.metrics_summary.get(metric_name, 0)
            
            if baseline_value != 0:
                change_pct = ((current_value - baseline_value) / abs(baseline_value)) * 100
            else:
                change_pct = 0
            
            comparison["metrics_comparison"][metric_name] = {
                "baseline": f"{baseline_value:.3f}",
                "current": f"{current_value:.3f}",
                "change_pct": f"{change_pct:+.1f}%",
            }
        
        return comparison
    
    def get_summary(self) -> Dict:
        """Get framework summary and history."""
        return {
            "framework_name": self.framework_name,
            "evaluation_types": self.evaluation_types,
            "total_benchmarks": len(self.evaluation_history),
            "test_cases_count": len(self.test_dataset),
            "benchmarks": [
                {
                    "timestamp": b.timestamp,
                    "evaluation_type": b.evaluation_type.value,
                    "pass_rate": f"{b.pass_rate:.1%}",
                    "average_score": f"{b.average_score:.2f}",
                }
                for b in self.evaluation_history
            ],
        }


# ============================================================================
# PHASE 3: Core Template Method (Production-Ready)
# ============================================================================

def create_evaluation_framework(
    framework_name: str,
    evaluation_types: List[str],
    test_dataset: Optional[List[TestCase]] = None,
    metrics_config: Optional[Dict[str, Metric]] = None,
) -> EvaluationFramework:
    """
    CORE REUSABLE TEMPLATE METHOD - Create evaluation framework for any AI system.
    
    This is the primary method to extract and use in your projects. It returns
    a production-ready evaluation framework that can measure:
    - RAG systems (retrieval quality)
    - Agent systems (task completion)
    - System performance (latency, throughput, cost)
    - Business outcomes (workflow completion, time savings)
    
    Args:
        framework_name: Name for this evaluation framework
        evaluation_types: List of evaluation types
            ["rag", "agent", "system", "business"]
        test_dataset: List of TestCase objects for evaluation
        metrics_config: Optional dict of metric configurations
    
    Returns:
        EvaluationFramework: Ready to evaluate systems
    
    Example Usage (for learner projects):
        ```python
        # Step 1: Define test cases
        test_cases = [
            TestCase(
                test_id="rag_001",
                test_type="retrieval",
                input_data={"query": "customer data"},
                expected_output={"documents": [...]},
                success_criteria="Contains 2+ relevant documents"
            ),
            # ... more test cases
        ]
        
        # Step 2: Create framework
        framework = create_evaluation_framework(
            framework_name="My RAG Evaluator",
            evaluation_types=["rag"],
            test_dataset=test_cases
        )
        
        # Step 3: Evaluate your system
        results = framework.evaluate_system(my_rag_system_fn, "rag")
        
        # Step 4: Get insights
        report = framework.generate_report()
        print(report)
        ```
    
    Integration Points:
    - Use with Module 6 agents: evaluate_system(agent.execute_task, "agent")
    - Use with RAG systems: evaluate_system(rag_retriever, "rag")
    - Use with any callable: evaluate_system(your_function, "system")
    """
    
    # Create default test dataset if not provided
    if test_dataset is None:
        test_dataset = _create_default_test_dataset()
    
    # Create framework
    framework = EvaluationFramework(
        framework_name=framework_name,
        evaluation_types=evaluation_types,
        test_dataset=test_dataset,
        metrics_config=metrics_config,
    )
    
    return framework


def _create_default_test_dataset() -> List[TestCase]:
    """Create default test dataset for demonstrations."""
    return [
        # RAG tests
        TestCase(
            test_id="rag_001",
            test_type="retrieval_search",
            input_data={"query": "customer support policies"},
            expected_output={"relevant_docs": 2},
            success_criteria="Find 2+ relevant policy documents",
            metadata={"latency": 0.35},
        ),
        TestCase(
            test_id="rag_002",
            test_type="retrieval_search",
            input_data={"query": "pricing information"},
            expected_output={"relevant_docs": 1},
            success_criteria="Find pricing document",
            metadata={"latency": 0.28},
        ),
        # Agent tests
        TestCase(
            test_id="agent_001",
            test_type="agent_task",
            input_data={"task": "Find overdue accounts"},
            expected_output={"task_completed": True},
            success_criteria="Successfully find overdue accounts",
            metadata={"cost": 0.005},
        ),
        TestCase(
            test_id="agent_002",
            test_type="agent_task",
            input_data={"task": "Generate report"},
            expected_output={"task_completed": True},
            success_criteria="Successfully generate report",
            metadata={"cost": 0.008},
        ),
        # System tests
        TestCase(
            test_id="sys_001",
            test_type="system_latency",
            input_data={"request_count": 10},
            expected_output={"latency_p95": 0.5},
            success_criteria="P95 latency < 1.0 second",
            metadata={"latency": 0.45},
        ),
        # Business tests
        TestCase(
            test_id="biz_001",
            test_type="business_flow",
            input_data={"workflow": "daily_reports"},
            expected_output={"completed": True},
            success_criteria="Complete workflow successfully",
            metadata={"time_saved": 2.5},
        ),
    ]


# ============================================================================
# DEMONSTRATIONS (4-5 Total)
# ============================================================================

def demo_rag_evaluation():
    """Demo 1: Evaluate RAG system retrieval quality."""
    print("\n" + "="*70)
    print("DEMO 1: RAG EVALUATION")
    print("="*70)
    
    # Create RAG test cases
    rag_tests = [
        TestCase(
            test_id="rag_1",
            test_type="retrieval_search",
            input_data={"query": "customer data security"},
            expected_output={"documents_found": 2, "precision": 0.95},
            success_criteria="Find 2+ security-related documents with high precision",
            metadata={"latency": 0.32},
        ),
        TestCase(
            test_id="rag_2",
            test_type="retrieval_search",
            input_data={"query": "API rate limits"},
            expected_output={"documents_found": 1, "precision": 0.90},
            success_criteria="Find API documentation with good precision",
            metadata={"latency": 0.28},
        ),
    ]
    
    # Create framework
    framework = create_evaluation_framework(
        framework_name="Knowledge Base Retrieval Evaluator",
        evaluation_types=["rag"],
        test_dataset=rag_tests,
    )
    
    # Mock RAG system
    def mock_rag_system(query_input: Dict) -> Dict:
        query = query_input.get("query", "")
        if "security" in query.lower():
            return {"documents_found": 2, "precision": 0.95}
        elif "rate" in query.lower():
            return {"documents_found": 1, "precision": 0.90}
        return {"documents_found": 0}
    
    # Evaluate
    print("\nRunning RAG evaluation...")
    results = framework.evaluate_system(mock_rag_system, "rag")
    
    print(f"\n✓ Total Tests: {results.total_tests}")
    print(f"✓ Passed: {results.passed_tests}")
    print(f"✓ Pass Rate: {results.pass_rate:.1%}")
    print(f"✓ Average Score: {results.average_score:.2f}")
    print(f"✓ Execution Time: {results.duration:.2f}s")
    
    print("\nKey Metrics:")
    for metric, value in results.metrics_summary.items():
        print(f"  • {metric}: {value:.3f}")
    
    print("\n✅ RAG evaluation demonstration complete")
    return framework


def demo_agent_evaluation():
    """Demo 2: Evaluate agent task completion."""
    print("\n" + "="*70)
    print("DEMO 2: AGENT EVALUATION")
    print("="*70)
    
    # Create agent test cases
    agent_tests = [
        TestCase(
            test_id="agent_1",
            test_type="agent_task",
            input_data={"task": "Find overdue customer accounts", "days_overdue": 30},
            expected_output={"task_completed": True, "accounts_found": True},
            success_criteria="Successfully identify overdue accounts",
            metadata={"cost": 0.006},
        ),
        TestCase(
            test_id="agent_2",
            test_type="agent_task",
            input_data={"task": "Analyze customer feedback", "month": "June"},
            expected_output={"task_completed": True, "sentiment": "positive"},
            success_criteria="Generate customer sentiment analysis",
            metadata={"cost": 0.008},
        ),
        TestCase(
            test_id="agent_3",
            test_type="agent_task",
            input_data={"task": "Create weekly report"},
            expected_output={"task_completed": True, "sections": 4},
            success_criteria="Generate comprehensive weekly report",
            metadata={"cost": 0.010},
        ),
    ]
    
    # Create framework
    framework = create_evaluation_framework(
        framework_name="Multi-Agent Task Evaluator",
        evaluation_types=["agent"],
        test_dataset=agent_tests,
    )
    
    # Mock agent system
    def mock_agent_system(task_input: Dict) -> Dict:
        task = task_input.get("task", "").lower()
        if "overdue" in task:
            return {"task_completed": True, "accounts_found": True}
        elif "feedback" in task or "analyze" in task:
            return {"task_completed": True, "sentiment": "positive", "score": 0.82}
        elif "report" in task:
            return {"task_completed": True, "sections": 4}
        return {"task_completed": False}
    
    # Evaluate
    print("\nRunning agent evaluation...")
    results = framework.evaluate_system(mock_agent_system, "agent")
    
    print(f"\n✓ Total Tasks: {results.total_tests}")
    print(f"✓ Completed: {results.passed_tests}")
    print(f"✓ Completion Rate: {results.pass_rate:.1%}")
    print(f"✓ Average Quality: {results.average_score:.2f}")
    
    print("\nAgent Performance Breakdown:")
    for i, result in enumerate(results.results, 1):
        status = "✓ PASS" if result.passed else "✗ FAIL"
        print(f"  {i}. Task {result.test_case.test_id}: {status} (Score: {result.score:.2f})")
    
    print("\n✅ Agent evaluation demonstration complete")
    return framework


def demo_system_evaluation():
    """Demo 3: Evaluate system performance (latency, throughput, cost)."""
    print("\n" + "="*70)
    print("DEMO 3: SYSTEM EVALUATION")
    print("="*70)
    
    # Create system test cases
    system_tests = [
        TestCase(
            test_id="sys_latency_1",
            test_type="system_latency",
            input_data={"num_requests": 100},
            expected_output={"latency_p95": 0.5},
            success_criteria="P95 latency < 0.5 seconds",
            metadata={"latency": 0.42},
        ),
        TestCase(
            test_id="sys_throughput_1",
            test_type="system_throughput",
            input_data={"duration_seconds": 60},
            expected_output={"throughput_rps": 100},
            success_criteria="Support 100+ requests per second",
            metadata={"throughput": 95},
        ),
        TestCase(
            test_id="sys_cost_1",
            test_type="system_cost",
            input_data={"requests": 1000},
            expected_output={"cost_per_request": 0.005},
            success_criteria="Cost < $0.01 per request",
            metadata={"cost": 0.0048},
        ),
    ]
    
    # Create framework
    framework = create_evaluation_framework(
        framework_name="AI System Performance Evaluator",
        evaluation_types=["system"],
        test_dataset=system_tests,
    )
    
    # Mock system
    def mock_system(perf_input: Dict) -> Dict:
        test_type = perf_input.get("test_type", "latency")
        return {
            "latency_p95": 0.42,
            "throughput_rps": 95,
            "cost_per_request": 0.0048,
        }
    
    # Evaluate
    print("\nRunning system performance evaluation...")
    results = framework.evaluate_system(mock_system, "system")
    
    print(f"\n✓ Tests Run: {results.total_tests}")
    print(f"✓ Passed: {results.passed_tests}")
    print(f"✓ Pass Rate: {results.pass_rate:.1%}")
    print(f"✓ Total Duration: {results.duration:.2f}s")
    
    print("\nSystem Metrics:")
    for metric, value in results.metrics_summary.items():
        if metric == "latency":
            print(f"  • P95 Latency: {value:.3f}s")
        elif metric == "throughput":
            print(f"  • Throughput: {value:.1f} RPS")
        elif metric == "cost":
            print(f"  • Cost per Request: ${value:.4f}")
    
    print("\n✅ System evaluation demonstration complete")
    return framework


def demo_business_evaluation():
    """Demo 4: Evaluate business outcomes (workflow completion, time savings)."""
    print("\n" + "="*70)
    print("DEMO 4: BUSINESS EVALUATION")
    print("="*70)
    
    # Create business test cases
    business_tests = [
        TestCase(
            test_id="biz_workflow_1",
            test_type="business_flow",
            input_data={"workflow": "customer_report", "frequency": "daily"},
            expected_output={"completed": True, "time_saved_hours": 2.5},
            success_criteria="Generate daily customer report, save 2+ hours",
            metadata={"time_saved": 2.5},
        ),
        TestCase(
            test_id="biz_workflow_2",
            test_type="business_flow",
            input_data={"workflow": "account_recovery", "frequency": "weekly"},
            expected_output={"completed": True, "recovery_rate": 0.25},
            success_criteria="Identify overdue accounts, improve recovery rate",
            metadata={"time_saved": 4.0},
        ),
    ]
    
    # Create framework
    framework = create_evaluation_framework(
        framework_name="Business Impact Evaluator",
        evaluation_types=["business"],
        test_dataset=business_tests,
    )
    
    # Mock business system
    def mock_business_system(business_input: Dict) -> Dict:
        workflow = business_input.get("workflow", "").lower()
        if "report" in workflow:
            return {"completed": True, "time_saved_hours": 2.5, "user_satisfaction": 0.92}
        elif "recovery" in workflow:
            return {"completed": True, "recovery_rate": 0.26, "revenue_impact": 5000}
        return {"completed": False}
    
    # Evaluate
    print("\nRunning business evaluation...")
    results = framework.evaluate_system(mock_business_system, "business")
    
    print(f"\n✓ Workflows Evaluated: {results.total_tests}")
    print(f"✓ Successful: {results.passed_tests}")
    print(f"✓ Success Rate: {results.pass_rate:.1%}")
    print(f"✓ Average Impact Score: {results.average_score:.2f}")
    
    print("\nBusiness Outcomes:")
    for metric, value in results.metrics_summary.items():
        if metric == "time_saved":
            print(f"  • Total Time Saved: {value:.1f} hours")
        elif metric == "revenue_impact":
            print(f"  • Revenue Impact: ${value:.0f}")
        elif metric == "user_satisfaction":
            print(f"  • User Satisfaction: {value:.1%}")
    
    print("\n✅ Business evaluation demonstration complete")
    return framework


def demo_benchmark_tracking():
    """Demo 5: Track improvement across multiple evaluation runs."""
    print("\n" + "="*70)
    print("DEMO 5: BENCHMARK TRACKING & IMPROVEMENT")
    print("="*70)
    
    # Create test dataset
    test_cases = [
        TestCase(
            test_id="track_1",
            test_type="retrieval_search",
            input_data={"query": "test query"},
            expected_output={"result": "found"},
            success_criteria="Find result",
            metadata={"latency": 0.35},
        ),
        TestCase(
            test_id="track_2",
            test_type="retrieval_search",
            input_data={"query": "another query"},
            expected_output={"result": "found"},
            success_criteria="Find result",
            metadata={"latency": 0.32},
        ),
    ]
    
    # Create framework
    framework = create_evaluation_framework(
        framework_name="Performance Tracking System",
        evaluation_types=["rag"],
        test_dataset=test_cases,
    )
    
    # Mock system (improving over time)
    call_count = [0]
    
    def improving_system(query_input: Dict) -> Dict:
        call_count[0] += 1
        # Simulate improvement: latency decreases over time
        base_latency = 0.35
        improvement = call_count[0] * 0.02
        return {"result": "found", "latency": max(0.25, base_latency - improvement)}
    
    # Run multiple evaluations
    print("\nRunning 3 consecutive evaluations...")
    
    run_results = []
    for run_num in range(1, 4):
        print(f"\n  Run {run_num}:")
        results = framework.evaluate_system(improving_system, "rag")
        run_results.append(results)
        print(f"    Pass Rate: {results.pass_rate:.1%}")
        print(f"    Average Score: {results.average_score:.2f}")
        print(f"    Duration: {results.duration:.2f}s")
    
    # Compare baseline (run 1) to current (run 3)
    print("\n" + "-"*70)
    print("Improvement Analysis:")
    print("-"*70)
    comparison = framework.compare_to_baseline(run_results[0])
    
    print(f"Baseline (Run 1):")
    print(f"  Pass Rate: {comparison['pass_rate_change']['baseline']}")
    print(f"  Average Score: {comparison['average_score_change']['baseline']}")
    
    print(f"\nCurrent (Run 3):")
    print(f"  Pass Rate: {comparison['pass_rate_change']['current']}")
    print(f"  Average Score: {comparison['average_score_change']['current']}")
    
    print(f"\nImprovement:")
    print(f"  Pass Rate Change: {comparison['pass_rate_change']['improvement']}")
    print(f"  Average Score Change: {comparison['average_score_change']['improvement']}")
    
    # Show summary
    print("\n" + "-"*70)
    print("Framework Summary:")
    summary = framework.get_summary()
    print(f"  Framework Name: {summary['framework_name']}")
    print(f"  Total Benchmarks: {summary['total_benchmarks']}")
    print(f"  Test Cases: {summary['test_cases_count']}")
    
    print("\n✅ Benchmark tracking demonstration complete")
    return framework


# ============================================================================
# INTERACTIVE MENU-DRIVEN CLI
# ============================================================================

def display_main_menu():
    """Display main menu options."""
    print("\n" + "="*70)
    print("LESSON 7.5: EVALUATION & PERFORMANCE FRAMEWORKS FOR AI SYSTEMS")
    print("="*70)
    print("\nThis is a PRODUCTION-READY evaluation framework tool.")
    print("Extract the classes and methods into your own projects!\n")
    
    print("SELECT AN OPTION:")
    print("\n  INTERACTIVE DEMONSTRATIONS (with mock outputs):")
    print("  1. RAG Evaluation - Test retrieval quality")
    print("  2. Agent Evaluation - Test task completion")
    print("  3. System Evaluation - Test performance (latency, throughput, cost)")
    print("  4. Business Evaluation - Test business outcomes")
    print("  5. Benchmark Tracking - Track improvement across runs")
    print("\n  REAL-WORLD USAGE PATTERNS (code examples you can adapt):")
    print("  6. View Framework Information")
    print("  7. View Real-World Usage Patterns")
    print("\n  Q. Quit")
    print("-"*70)


def display_framework_info():
    """Display framework information and reusable components."""
    os.system("clear" if os.name == "posix" else "cls")
    print("\n" + "="*70)
    print("FRAMEWORK INFORMATION & REUSABLE COMPONENTS")
    print("="*70)
    
    print("\nKey Reusable Classes:")
    print("  • TestCase: Define test scenarios with expected outcomes")
    print("  • Metric: Define measurable performance metrics")
    print("  • EvaluationResult: Score for a single test case")
    print("  • Benchmark: Aggregate results from evaluation runs")
    print("  • EvaluationFramework: Main reusable container")
    
    print("\nCore Template Method:")
    print("  create_evaluation_framework()")
    print("    - framework_name: Name for this evaluation")
    print("    - evaluation_types: ['rag', 'agent', 'system', 'business']")
    print("    - test_dataset: List of TestCase objects")
    print("    - Returns: Ready-to-use EvaluationFramework")
    
    print("\nCore Use Case:")
    print("  1. Systematically evaluate AI systems (RAG, agents, workflows)")
    print("  2. Measure performance (latency, throughput, accuracy, ROI)")
    print("  3. Track improvement over time with benchmarks")
    print("  4. Compare against baselines for continuous improvement")
    
    print("\nReusable Pattern for Your Projects:")
    print("  ```python")
    print("  # Step 1: Create framework")
    print("  framework = create_evaluation_framework(")
    print("      framework_name='My RAG Evaluator',")
    print("      evaluation_types=['rag'],")
    print("      test_dataset=my_test_cases")
    print("  )")
    print("  ")
    print("  # Step 2: Run evaluation")
    print("  results = framework.evaluate_system(your_system, 'rag')")
    print("  ")
    print("  # Step 3: Generate report")
    print("  report = framework.generate_report()")
    print("  ```")


def display_real_world_patterns():
    """Display real-world usage patterns that learners can adapt."""
    os.system("clear" if os.name == "posix" else "cls")
    print("\n" + "="*70)
    print("REAL-WORLD USAGE PATTERNS")
    print("="*70)
    print("\nThese patterns show how to use the evaluation framework with")
    print("actual systems from earlier modules. Copy and adapt these patterns")
    print("for your own projects!\n")
    
    print("PATTERN 1: EVALUATE A RAG SYSTEM (from Module 4)")
    print("-"*70)
    print("Location: example_rag_evaluation_pattern()")
    print("\nWhat it does:")
    print("  • Define test cases for retrieval quality")
    print("  • Create wrapper function for your RAG system")
    print("  • Run evaluation and measure precision, recall, relevance")
    print("\nWhen to use:")
    print("  • Testing knowledge base retrieval systems")
    print("  • Measuring which documents are found and ranked correctly")
    print("  • Comparing RAG performance over time")
    print("\nKey metrics:")
    print("  • docs_retrieved: Number of documents found")
    print("  • avg_relevance: Relevance score (0-1)")
    print("  • precision: What % of results are relevant?")
    
    print("\n" + "-"*70)
    print("PATTERN 2: EVALUATE AN AGENT SYSTEM (from Module 6)")
    print("-"*70)
    print("Location: example_agent_evaluation_pattern()")
    print("\nWhat it does:")
    print("  • Define test cases for agent task completion")
    print("  • Create wrapper function for your agent")
    print("  • Measure task success, error handling, memory usage")
    print("\nWhen to use:")
    print("  • Testing autonomous agents with multiple tools")
    print("  • Measuring task completion rates")
    print("  • Verifying error handling and recovery")
    print("\nKey metrics:")
    print("  • task_completed: Did agent finish the task?")
    print("  • error_handled: Did agent recover from errors?")
    print("  • success_rate: % of tasks completed successfully")
    
    print("\n" + "-"*70)
    print("PATTERN 3: SYSTEM EVALUATION (Latency, Throughput, Cost)")
    print("-"*70)
    print("Location: example_system_evaluation_pattern()")
    print("\nWhat it does:")
    print("  • Measure response time (SLA compliance)")
    print("  • Measure throughput (requests per second)")
    print("  • Calculate cost per request")
    print("\nWhen to use:")
    print("  • Ensuring system meets performance SLAs")
    print("  • Monitoring resource usage and costs")
    print("  • Optimizing infrastructure and models")
    print("\nKey metrics:")
    print("  • response_time_seconds: Latency")
    print("  • requests_per_second: Throughput capacity")
    print("  • cost_per_request: Cost efficiency")
    
    print("\n" + "-"*70)
    print("PATTERN 4: BUSINESS EVALUATION (Workflow Outcomes)")
    print("-"*70)
    print("Location: example_business_evaluation_pattern()")
    print("\nWhat it does:")
    print("  • Measure workflow completion time")
    print("  • Calculate cost savings and ROI")
    print("  • Track quality improvements")
    print("\nWhen to use:")
    print("  • Justifying AI investment to business leaders")
    print("  • Tracking savings (time, money, quality)")
    print("  • Measuring real business impact")
    print("\nKey metrics:")
    print("  • time_hours: How long to complete workflow?")
    print("  • cost_saved_dollars: How much money saved?")
    print("  • roi_percent: Return on investment")
    
    print("\n" + "-"*70)
    print("PATTERN 5: BENCHMARK TRACKING (Track Improvements)")
    print("-"*70)
    print("Location: example_benchmark_tracking_pattern()")
    print("\nWhat it does:")
    print("  • Evaluate v1.0 of your system")
    print("  • Evaluate v1.1 with improvements")
    print("  • Compare and show progress")
    print("\nWhen to use:")
    print("  • Proving a new version is better than old one")
    print("  • Tracking improvements month-to-month")
    print("  • Identifying which improvements worked")
    print("\nKey metrics:")
    print("  • pass_rate_improvement: % points better")
    print("  • average_score_improvement: Score increase")
    print("  • metrics_improvement: Per-metric changes")
    
    print("\n" + "="*70)
    print("HOW TO USE THESE PATTERNS IN YOUR PROJECT")
    print("="*70)
    print("\n1. FIND the pattern that matches your system")
    print("   (RAG system → Pattern 1, Agent → Pattern 2, etc.)")
    print("\n2. COPY the pattern function to your project")
    print("\n3. REPLACE the TODO placeholder with your actual system:")
    print("   # TODO: Replace with your actual RAG from Module 4")
    print("   # from module-04 import RAGRetriever")
    print("\n4. ADAPT the test cases to match your scenarios")
    print("\n5. RUN the evaluation and collect metrics")
    print("\n6. ITERATE: Improve your system, re-run, track progress")
    print("\nAll pattern functions are defined at the end of this file!")


def run_interactive_cli():
    """Run interactive menu-driven CLI for evaluation framework."""
    
    print("\n" + "="*70)
    print("LESSON 7.5: INTERACTIVE EVALUATION FRAMEWORK EXPLORER")
    print("="*70)
    print("\nWelcome! This tool demonstrates a PRODUCTION-READY evaluation")
    print("framework. You can run different evaluation types, view results,")
    print("and explore benchmarking capabilities.")
    
    # Store frameworks for benchmarking comparison
    frameworks = {}
    last_framework = None
    last_results = None
    
    while True:
        os.system("clear" if os.name == "posix" else "cls")
        display_main_menu()
        choice = input("Enter your choice (1-7, Q to quit): ").strip().lower()
        
        if choice == "q":
            print("\n" + "="*70)
            print("THANK YOU FOR EXPLORING EVALUATION FRAMEWORKS!")
            print("="*70)
            print("\nKey Takeaways:")
            print("  1. Define comprehensive test cases with expected outcomes")
            print("  2. Build evaluation frameworks for ANY AI system")
            print("  3. Calculate meaningful metrics across 4 dimensions:")
            print("     - RAG: Retrieval precision, recall, relevance")
            print("     - Agent: Task success, tool success, goal completion")
            print("     - System: Latency, throughput, cost per request")
            print("     - Business: Workflow completion, time savings, ROI")
            print("  4. Track improvement over time using benchmarks")
            print("  5. Compare against baselines for continuous improvement")
            print("  6. Generate reports for stakeholders")
            print("\nNext: Module 8 - Production AI Systems")
            print("  • Deployment strategies")
            print("  • Security & reliability")
            print("  • Observability & monitoring")
            break
        
        elif choice == "1":
            os.system("clear" if os.name == "posix" else "cls")
            print("\n" + "-"*70)
            framework = demo_rag_evaluation()
            frameworks["rag"] = framework
            last_framework = framework
            last_results = framework.evaluation_history[-1]
            print("-"*70)
            print("\nFramework stored. You can compare against this in Benchmark Tracking!")
            input("Press Enter to continue...")
        
        elif choice == "2":
            os.system("clear" if os.name == "posix" else "cls")
            print("\n" + "-"*70)
            framework = demo_agent_evaluation()
            frameworks["agent"] = framework
            last_framework = framework
            last_results = framework.evaluation_history[-1]
            print("-"*70)
            print("\nFramework stored. You can compare against this in Benchmark Tracking!")
            input("Press Enter to continue...")
        
        elif choice == "3":
            os.system("clear" if os.name == "posix" else "cls")
            print("\n" + "-"*70)
            framework = demo_system_evaluation()
            frameworks["system"] = framework
            last_framework = framework
            last_results = framework.evaluation_history[-1]
            print("-"*70)
            print("\nFramework stored. You can compare against this in Benchmark Tracking!")
            input("Press Enter to continue...")
        
        elif choice == "4":
            os.system("clear" if os.name == "posix" else "cls")
            print("\n" + "-"*70)
            framework = demo_business_evaluation()
            frameworks["business"] = framework
            last_framework = framework
            last_results = framework.evaluation_history[-1]
            print("-"*70)
            print("\nFramework stored. You can compare against this in Benchmark Tracking!")
            input("Press Enter to continue...")
        
        elif choice == "5":
            os.system("clear" if os.name == "posix" else "cls")
            if not last_framework:
                print("\n⚠️  Please run an evaluation first (options 1-4)")
                print("   Benchmark tracking requires baseline results to compare against.")
                input("Press Enter to continue...")
            else:
                print("\n" + "-"*70)
                framework = demo_benchmark_tracking()
                frameworks["tracking"] = framework
                print("-"*70)
                print("\nBenchmark comparison complete!")
                if last_results:
                    print("\nComparing against your previous evaluation...")
                    comparison = framework.compare_to_baseline(last_results)
                    print("\nComparison Results:")
                    print(f"  Previous Pass Rate: {comparison['pass_rate_change']['baseline']}")
                    print(f"  Current Pass Rate: {comparison['pass_rate_change']['current']}")
                    print(f"  Improvement: {comparison['pass_rate_change']['improvement']}")
                input("Press Enter to continue...")
        
        elif choice == "6":
            display_framework_info()
            input("\nPress Enter to continue...")
        
        elif choice == "7":
            display_real_world_patterns()
            input("\nPress Enter to continue...")
        
        else:
            print("\n❌ Invalid choice. Please enter 1-7 or Q to quit.")
            input("Press Enter to continue...")


# ============================================================================
# SECTION: REAL-WORLD USAGE PATTERNS
# ============================================================================
# This section shows how to apply the evaluation framework to actual
# systems built in earlier modules. These are code patterns (not executed)
# that learners can copy and adapt to their own projects.
# ============================================================================


# PATTERN 1: Evaluate a RAG System (from Module 4)
# ============================================================================
def example_rag_evaluation_pattern():
    """
    This pattern shows how to evaluate a RAG retrieval system built in Module 4.
    The learner would replace 'my_rag_retriever' with their actual RAG system.
    
    Key Steps:
    1. Define test cases based on real queries and expected documents
    2. Create a wrapper function that calls your RAG system
    3. Create evaluation framework with RAG type
    4. Run evaluation and get results
    """
    
    # Step 1: Real test cases from actual use cases
    rag_test_cases = [
        TestCase(
            test_id="rag_retrieval_001",
            test_type="retrieval",
            input_data={"query": "How do I reset my password?"},
            # Expected output: system should find password reset documentation
            expected_output={"docs_retrieved": 3, "top_match": "password_reset_guide.md"},
            success_criteria="Finds 3+ relevant docs with correct top match"
        ),
        TestCase(
            test_id="rag_retrieval_002",
            test_type="retrieval",
            input_data={"query": "Enterprise billing invoice format"},
            # Expected output: system should retrieve billing documentation
            expected_output={"docs_retrieved": 2, "top_match": "enterprise_billing.md"},
            success_criteria="Finds 2+ billing docs in top 5 results"
        ),
        TestCase(
            test_id="rag_relevance_001",
            test_type="relevance",
            input_data={"query": "API authentication methods"},
            # Expected output: documents should be highly relevant to API authentication
            expected_output={"avg_relevance": 0.85, "docs_relevant": 4},
            success_criteria="Average relevance score >= 0.85"
        ),
    ]
    
    # Step 2: Wrapper function that calls YOUR actual RAG system
    # Replace this with your real RAG implementation from Module 4
    def evaluate_my_rag_system(test_input: Dict) -> Dict:
        """
        Wrapper function for your RAG system.
        This function receives test input and returns actual output from your system.
        """
        # TODO: Replace with your actual RAG retriever from Module 4
        # Example pattern:
        #   from module-04 import RAGRetriever
        #   retriever = RAGRetriever(knowledge_base="my_docs")
        #   results = retriever.search(test_input["query"], top_k=5)
        #   return {
        #         "docs_found": len(results),
        #         "contains": results[0]["content"] if results else "",
        #         "precision": calculate_precision(results)
        #   }
        
        # For now, simulate the output
        query = test_input["query"]
        docs_found = 3 if "password" in query.lower() else 2
        top_doc = "password_reset_guide.md" if "password" in query.lower() else "enterprise_billing.md"
        
        return {
            "docs_retrieved": docs_found,
            "top_match": top_doc,
            "avg_relevance": 0.87,
            "docs_relevant": docs_found - 1
        }
    
    # Step 3: Create evaluation framework for RAG type
    rag_framework = create_evaluation_framework(
        framework_name="My RAG System Evaluation",
        evaluation_types=["rag"],
        test_dataset=rag_test_cases,
        metrics_config={
            "retrieval": {
                "name": "Retrieval Accuracy",
                "target": 0.90
            }
        }
    )
    
    # Step 4: Run evaluation on your system
    rag_results = rag_framework.evaluate_system(
        system_fn=evaluate_my_rag_system,
        evaluation_type="rag"
    )
    
    # Step 5: Review results
    # Print results to see how your RAG system is performing:
    #   rag_results.pass_rate  # What % of tests passed?
    #   rag_results.average_score  # Average accuracy score
    #   rag_results.metrics_summary  # Per-metric breakdown
    
    return rag_framework


# PATTERN 2: Evaluate an Agent System (from Module 6)
# ============================================================================
def example_agent_evaluation_pattern():
    """
    This pattern shows how to evaluate an autonomous agent built in Module 6.
    The learner would replace 'my_agent' with their actual agent implementation.
    
    Key Steps:
    1. Define test cases based on agent tasks and expected outcomes
    2. Create a wrapper function that executes your agent
    3. Create evaluation framework with AGENT type
    4. Run evaluation and get results
    """
    
    # Step 1: Real test cases for agent task execution
    agent_test_cases = [
        TestCase(
            test_id="agent_task_001",
            test_type="task_completion",
            input_data={"task": "Find all overdue invoices from Q3", "customer_id": "cust_123"},
            # Expected output: agent successfully finds and lists invoices
            expected_output={"task_completed": True, "invoices_found": 3, "status": "success"},
            success_criteria="Agent successfully finds overdue invoices"
        ),
        TestCase(
            test_id="agent_task_002",
            test_type="task_completion",
            input_data={"task": "Generate payment reminder for client", "client_name": "Acme Corp"},
            # Expected output: agent generates and sends reminder
            expected_output={"task_completed": True, "reminder_sent": True, "status": "success"},
            success_criteria="Agent generates and sends reminder successfully"
        ),
        TestCase(
            test_id="agent_error_handling_001",
            test_type="error_handling",
            input_data={"task": "Fetch data from nonexistent customer", "customer_id": "invalid_999"},
            # Expected output: agent handles error gracefully
            expected_output={"task_completed": False, "error_handled": True, "error_message": "Customer not found"},
            success_criteria="Agent handles errors gracefully without crashing"
        ),
    ]
    
    # Step 2: Wrapper function that executes YOUR actual agent
    # Replace this with your real agent from Module 6
    def evaluate_my_agent(task_input: Dict) -> Dict:
        """
        Wrapper function for your agent.
        This function receives a task and returns the agent's output.
        """
        # TODO: Replace with your actual agent from Module 6
        # Example pattern:
        #   from module-06 import create_agent_with_memory
        #   agent = create_agent_with_memory(name="TaskAgent", memory_size=10)
        #   result = agent.execute_task(task_input["task"])
        
        # For now, simulate agent execution
        task = task_input.get("task", "").lower()
        
        if "invalid" in task:
            # Simulate error handling
            return {
                "task_completed": False,
                "error_handled": True,
                "error_message": "Customer not found"
            }
        else:
            # Simulate successful task completion
            return {
                "task_completed": True,
                "invoices_found": 3 if "overdue" in task else 0,
                "reminder_sent": True if "reminder" in task else False,
                "status": "success"
            }
    
    # Step 3: Create evaluation framework for AGENT type
    agent_framework = create_evaluation_framework(
        framework_name="My Agent System Evaluation",
        evaluation_types=["agent"],
        test_dataset=agent_test_cases,
        metrics_config={
            "task_success": {
                "name": "Task Completion Rate",
                "target": 0.90
            },
            "error_handling": {
                "name": "Error Recovery Rate",
                "target": 0.95
            }
        }
    )
    
    # Step 4: Run evaluation on your agent
    agent_results = agent_framework.evaluate_system(
        system_fn=evaluate_my_agent,
        evaluation_type="agent"
    )
    
    # Step 5: Review agent performance
    # Print results to understand agent reliability:
    #   agent_results.pass_rate  # What % of tasks completed successfully?
    #   agent_results.average_score  # Overall agent performance score
    #   agent_results.failed_tests  # Which tasks failed? Why?
    
    return agent_framework


# PATTERN 3: System Evaluation (Latency, Throughput, Cost)
# ============================================================================
def example_system_evaluation_pattern():
    """
    This pattern shows how to evaluate system-level performance metrics
    (response time, throughput, computational cost).
    
    This applies to ANY AI system - RAG, Agent, Chatbot, etc.
    
    Key Steps:
    1. Define test cases that measure performance characteristics
    2. Instrument your system to measure latency and resource usage
    3. Create evaluation framework with SYSTEM type
    4. Run evaluation and get performance report
    """
    
    # Step 1: Test cases focused on system performance
    system_test_cases = [
        TestCase(
            test_id="system_latency_001",
            test_type="latency",
            input_data={"query": "Short query", "complexity": "low"},
            # Expected output: system responds quickly for simple queries
            expected_output={"response_time_seconds": 0.5, "within_sla": True},
            success_criteria="Response time <= 0.5 seconds"
        ),
        TestCase(
            test_id="system_latency_002",
            test_type="latency",
            input_data={"query": "Complex multi-document query", "complexity": "high"},
            # Expected output: system responds within acceptable time even for complex queries
            expected_output={"response_time_seconds": 2.0, "within_sla": True},
            success_criteria="Response time <= 2 seconds even for complex queries"
        ),
        TestCase(
            test_id="system_throughput_001",
            test_type="throughput",
            input_data={"num_requests": 100, "time_window_seconds": 60},
            # Expected output: system can handle multiple requests per second
            expected_output={"requests_per_second": 1.5, "achieved_throughput": 1.7},
            success_criteria="Achieve >= 1.5 requests per second"
        ),
        TestCase(
            test_id="system_cost_001",
            test_type="cost_efficiency",
            input_data={"request_type": "simple_query", "tokens_estimated": 500},
            # Expected output: cost is within budget per request
            expected_output={"cost_per_request": 0.002, "within_budget": True},
            success_criteria="Cost per request <= $0.002"
        ),
    ]
    
    # Step 2: Wrapper function that measures performance
    def evaluate_system_performance(test_input: Dict) -> Dict:
        """
        Wrapper function that executes your system and measures performance.
        This function simulates response timing and resource usage.
        """
        import time
        
        # Simulate system execution with timing
        start_time = time.time()
        
        # TODO: Replace with your actual system call
        # complexity = test_input.get("complexity", "low")
        # response = your_system.query(test_input.get("query", ""))
        
        # Simulate different latencies based on complexity
        if test_input.get("complexity") == "high":
            time.sleep(0.05)  # Simulate 50ms latency
            response_time = 1.8
        else:
            time.sleep(0.01)  # Simulate 10ms latency
            response_time = 0.3
        
        elapsed = time.time() - start_time
        
        return {
            "response_time_seconds": response_time,
            "within_sla": response_time <= 2.0,
            "requests_per_second": 1.7,
            "achieved_throughput": 1.7,
            "cost_per_request": 0.0015,
            "within_budget": True
        }
    
    # Step 3: Create evaluation framework for SYSTEM metrics
    system_framework = create_evaluation_framework(
        framework_name="My System Performance Evaluation",
        evaluation_types=["system"],
        test_dataset=system_test_cases,
        metrics_config={
            "latency": {
                "name": "Response Time",
                "target": 1.0  # Target: 1 second average
            },
            "throughput": {
                "name": "Requests Per Second",
                "target": 2.0  # Target: 2 RPS
            },
            "cost": {
                "name": "Cost Efficiency",
                "target": 0.002  # Target: $0.002 per request
            }
        }
    )
    
    # Step 4: Run system performance evaluation
    system_results = system_framework.evaluate_system(
        system_fn=evaluate_system_performance,
        evaluation_type="system"
    )
    
    # Step 5: Review system performance
    # Use results to monitor:
    #   system_results.metrics_summary  # All performance metrics
    #   Are we meeting SLA (latency <= 2s)?
    #   Is throughput acceptable (>= 1.5 RPS)?
    #   Is cost per request within budget (<= $0.002)?
    
    return system_framework


# PATTERN 4: Business Evaluation (Workflow Outcomes)
# ============================================================================
def example_business_evaluation_pattern():
    """
    This pattern shows how to measure the business impact of your AI system.
    Instead of just "does it work technically?", ask "does it create business value?"
    
    Key Steps:
    1. Define business outcomes (time saved, quality improved, revenue, etc.)
    2. Create test cases that measure real business metrics
    3. Run evaluation and show business impact
    """
    
    # Step 1: Business-focused test cases
    business_test_cases = [
        TestCase(
            test_id="business_workflow_001",
            test_type="workflow_completion",
            input_data={"workflow": "invoice_processing", "num_invoices": 50},
            # Expected output: system completes workflow with business success
            expected_output={
                "workflow_completed": True,
                "time_hours": 0.5,  # How long did it take?
                "manual_review_reduced": True,
                "accuracy_percent": 95  # Business metric: accuracy %
            },
            success_criteria="Complete workflow in < 1 hour with 90%+ accuracy"
        ),
        TestCase(
            test_id="business_roi_001",
            test_type="business_impact",
            input_data={"scenario": "customer_support_deflection", "tickets": 100},
            # Expected output: system deflects tickets, saves money
            expected_output={
                "tickets_resolved_by_ai": 75,  # 75% deflection rate
                "manual_tickets_saved": 75,
                "cost_saved_dollars": 450,  # $6 per manual ticket
                "roi_percent": 180  # 180% ROI on AI system
            },
            success_criteria="Deflect 70%+ of support tickets, achieve 150%+ ROI"
        ),
        TestCase(
            test_id="business_quality_001",
            test_type="quality_improvement",
            input_data={"metric": "document_classification_error_rate"},
            # Expected output: system improves quality vs. baseline
            expected_output={
                "error_rate_before": 0.15,  # 15% errors before AI
                "error_rate_after": 0.03,   # 3% errors after AI
                "quality_improvement_percent": 80  # 80% error reduction
            },
            success_criteria="Reduce error rate by 70%+ compared to baseline"
        ),
    ]
    
    # Step 2: Wrapper function that calculates business impact
    def evaluate_business_impact(test_input: Dict) -> Dict:
        """
        Wrapper function that measures business outcomes.
        This simulates running a business workflow and measuring results.
        """
        workflow = test_input.get("workflow", "").lower()
        
        if "invoice" in workflow:
            return {
                "workflow_completed": True,
                "time_hours": 0.45,  # Faster than 1 hour SLA
                "manual_review_reduced": True,
                "accuracy_percent": 96  # High accuracy
            }
        elif "support" in test_input.get("scenario", "").lower():
            return {
                "tickets_resolved_by_ai": 78,  # 78% deflection
                "manual_tickets_saved": 78,
                "cost_saved_dollars": 468,  # 78 * $6
                "roi_percent": 195  # Strong ROI
            }
        else:
            return {
                "error_rate_before": 0.15,
                "error_rate_after": 0.025,  # Better than target
                "quality_improvement_percent": 83  # 83% improvement
            }
    
    # Step 3: Create evaluation framework for BUSINESS metrics
    business_framework = create_evaluation_framework(
        framework_name="My Business Impact Evaluation",
        evaluation_types=["business"],
        test_dataset=business_test_cases,
        metrics_config={
            "workflow_speed": {
                "name": "Workflow Time Saved",
                "target": 0.5  # Target: complete in 30 minutes
            },
            "cost_savings": {
                "name": "Cost Savings per Workflow",
                "target": 400  # Target: save $400 per workflow
            },
            "quality": {
                "name": "Quality Improvement",
                "target": 0.75  # Target: 75% improvement
            }
        }
    )
    
    # Step 4: Run business impact evaluation
    business_results = business_framework.evaluate_system(
        system_fn=evaluate_business_impact,
        evaluation_type="business"
    )
    
    # Step 5: Present business metrics to stakeholders
    # business_results shows:
    #   - Time saved per workflow
    #   - Cost savings
    #   - Revenue impact
    #   - ROI percentage
    #   - Quality improvements
    # These are the metrics that matter to business leaders!
    
    return business_framework


# PATTERN 5: Benchmark Tracking (Compare Improvements)
# ============================================================================
def example_benchmark_tracking_pattern():
    """
    This pattern shows how to track improvements over time.
    Compare a new version against a baseline to measure progress.
    
    Use Case:
    - Version 1.0 of your RAG system has 85% accuracy
    - You improve it to Version 1.1
    - Use benchmarks to verify it's actually better (87% accuracy)
    - Track improvements month-to-month
    """
    
    # Baseline results from your current system (v1.0)
    baseline_test_cases = [
        TestCase(
            test_id="baseline_001",
            test_type="retrieval",
            input_data={"query": "How do I reset password?"},
            expected_output={"docs_found": 2, "relevance": 0.82},
            success_criteria="Baseline retrieval"
        ),
    ]
    
    # New/improved system (v1.1)
    improved_test_cases = [
        TestCase(
            test_id="improved_001",
            test_type="retrieval",
            input_data={"query": "How do I reset password?"},
            expected_output={"docs_found": 3, "relevance": 0.91},
            success_criteria="Improved retrieval with better ranking"
        ),
    ]
    
    # Step 1: Evaluate baseline system
    def baseline_system(test_input: Dict) -> Dict:
        # Current system performance
        return {
            "docs_found": 2,
            "relevance": 0.82,  # 82% relevance score
            "response_time": 1.2
        }
    
    baseline_framework = create_evaluation_framework(
        framework_name="My System v1.0",
        evaluation_types=["rag"],
        test_dataset=baseline_test_cases
    )
    baseline_results = baseline_framework.evaluate_system(baseline_system, "rag")
    baseline_benchmark = baseline_framework.evaluation_history[-1]
    
    # Step 2: Evaluate improved system
    def improved_system(test_input: Dict) -> Dict:
        # Improved system with better retrieval
        return {
            "docs_found": 3,  # Found more relevant docs
            "relevance": 0.91,  # Higher relevance score
            "response_time": 1.1  # Also faster
        }
    
    improved_framework = create_evaluation_framework(
        framework_name="My System v1.1",
        evaluation_types=["rag"],
        test_dataset=improved_test_cases
    )
    improved_results = improved_framework.evaluate_system(improved_system, "rag")
    improved_benchmark = improved_framework.evaluation_history[-1]
    
    # Step 3: Compare improvements
    comparison = improved_framework.compare_to_baseline(baseline_benchmark)
    
    # Step 4: Track metrics over time
    # Print improvement summary:
    #   - Baseline pass rate: 85%
    #   - Improved pass rate: 92%
    #   - Improvement: +7% better
    #   - Relevance score: 0.82 -> 0.91 (+11%)
    #   - Response time: 1.2s -> 1.1s (9% faster)
    # Use this to justify improvements to stakeholders
    
    return improved_framework


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    run_interactive_cli()
