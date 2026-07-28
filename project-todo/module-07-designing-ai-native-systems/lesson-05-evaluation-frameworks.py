"""
Lesson 7.5 TODO: Evaluation & Performance Frameworks for AI Systems

This is a PRODUCTION-READY tool you can extract and use in your own projects.

Business Scenario:
  A company deployed an AI assistant but can't measure if it's working. They need
  to systematically evaluate: retrieval quality (RAG), task completion (agents),
  system performance (latency/cost), and business outcomes (workflow completion).

Learning Goals:
  1. Design reusable test datasets with meaningful test cases
  2. Build evaluation frameworks for any AI system
  3. Calculate relevant metrics (precision, recall, latency, cost, success rate)
  4. Compare systems using benchmarks
  5. Track improvement over time
  6. Extract this as a reusable tool for your own projects

PART 1: Core Data Structures (TestCase, Metric, EvaluationResult, Benchmark)
PART 2: EvaluationFramework Container
PART 3: Core Template Method & Factory Function
PART 4: Demonstrations (5 total)

REFERENCE:
  - Completed: project-completed/module-07-designing-ai-native-systems/lesson-05-evaluation-frameworks.py
"""

import json
import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Callable, Tuple
from enum import Enum
from datetime import datetime
from collections import defaultdict


# ============================================================================
# PART 1: Core Data Structures (Reusable)
# ============================================================================

class EvaluationType(Enum):
    """TODO: Define evaluation types your framework supports.
    
    Common types:
    - RAG: Retrieval quality evaluation
    - AGENT: Task completion evaluation
    - SYSTEM: Performance evaluation (latency, throughput, cost)
    - BUSINESS: Business outcome evaluation (workflow completion, ROI)
    """
    pass


@dataclass
class TestCase:
    """TODO: Define a single test case for evaluation.
    
    Should include:
    - test_id: Unique identifier
    - test_type: Type of test (e.g., "retrieval_search", "agent_task")
    - input_data: Dict with test input
    - expected_output: Expected result
    - success_criteria: String describing success
    - metadata: Optional metadata (latency, cost, etc.)
    """
    pass


@dataclass
class Metric:
    """TODO: Define a measurable performance metric.
    
    Should include:
    - name: Metric name (e.g., "precision", "latency_p95")
    - calculation_fn: Function to calculate metric
    - unit: Unit of measurement (percentage, seconds, dollars, etc.)
    - target_value: Optional target value for comparison
    """
    pass


@dataclass
class EvaluationResult:
    """TODO: Result of evaluating a single test case.
    
    Should track:
    - test_case: The TestCase that was evaluated
    - actual_output: Output from system being evaluated
    - passed: Boolean if test passed
    - score: Numeric score (0.0 to 1.0)
    - metrics: Dict of metric_name -> value
    - duration: Execution time
    - error: Optional error message
    - timestamp: When evaluation occurred
    """
    pass


@dataclass
class Benchmark:
    """TODO: Represent benchmark results from complete evaluation run.
    
    Aggregates results across multiple test cases:
    - benchmark_id: Unique identifier
    - evaluation_name: Name of this evaluation
    - evaluation_type: EvaluationType (RAG, agent, system, business)
    - total_tests: Number of tests run
    - passed_tests: Number that passed
    - failed_tests: Number that failed
    - average_score: Average score across all tests
    - metrics_summary: Aggregated metrics
    - duration: Total evaluation time
    - results: List of individual EvaluationResult objects
    
    Methods:
    - pass_rate: Calculate pass rate (passed / total)
    - to_dict(): Convert to dictionary
    """
    pass


# ============================================================================
# PART 2: Evaluation Framework Container (Reusable)
# ============================================================================

class EvaluationFramework:
    """TODO: Build the main reusable evaluation framework.
    
    This is the container that orchestrates evaluation for any AI system.
    
    Constructor Args:
    - framework_name: Name for this framework
    - evaluation_types: List of types this framework supports
    - test_dataset: List of TestCase objects
    - metrics_config: Optional dict of Metric configurations
    
    Key Methods:
    - evaluate_system(system_fn, evaluation_type): Run evaluation
    - _score_result(test_case, actual_output): Score a result
    - generate_report(): Create evaluation report
    - compare_to_baseline(baseline): Compare to previous results
    - get_summary(): Get framework summary
    
    Implementation Notes:
    - Store evaluation history for benchmarking
    - Filter test cases by evaluation type
    - Aggregate metrics across test cases
    - Track both individual results and summaries
    """
    
    def __init__(self, framework_name: str, evaluation_types: List[str], 
                 test_dataset: List[TestCase], metrics_config=None):
        """TODO: Initialize the evaluation framework.
        
        Steps:
        1. Store framework configuration
        2. Initialize evaluation history list
        3. Set up evaluator functions for different types
        """
        pass
    
    def evaluate_system(self, system_fn: Callable, evaluation_type: str) -> Benchmark:
        """TODO: Run evaluation on a system.
        
        Steps:
        1. Filter test cases for evaluation_type
        2. Loop through each test case:
           - Call system_fn with test input
           - Score the result using _score_result()
           - Create EvaluationResult
           - Track pass/fail and metrics
        3. Aggregate results into Benchmark
        4. Store in evaluation_history
        5. Return Benchmark
        """
        pass
    
    def _score_result(self, test_case: TestCase, 
                     actual_output: Any) -> Tuple[float, Dict[str, float]]:
        """TODO: Score a test result (0.0 to 1.0).
        
        This is extensible - customize for your system.
        
        Handle different output types:
        - Dict: Compare keys and values
        - String: Use similarity matching
        - Boolean: Exact match
        - Numbers: Check within tolerance
        
        Extract metrics from test_case.metadata and include in result.
        """
        pass
    
    def generate_report(self) -> Dict:
        """TODO: Generate evaluation report from latest benchmark.
        
        Should include:
        - Framework name and evaluation type
        - Summary: total tests, passed, failed, pass rate, average score
        - Metrics: aggregated metric values
        - Test results: individual test outcomes
        - Timestamp when report was generated
        """
        pass
    
    def compare_to_baseline(self, baseline_benchmark: Benchmark) -> Dict:
        """TODO: Compare current results to baseline benchmark.
        
        Should show:
        - Baseline pass rate and average score
        - Current pass rate and average score
        - Improvement percentages and absolute changes
        - Per-metric comparisons
        """
        pass
    
    def get_summary(self) -> Dict:
        """TODO: Return framework summary and history.
        
        Should include:
        - Framework name and evaluation types
        - Total benchmarks run
        - Test cases count
        - Benchmark history with timestamps and pass rates
        """
        pass


# ============================================================================
# PART 3: Core Template Method (Reusable Pattern)
# ============================================================================

def create_evaluation_framework(
    framework_name: str,
    evaluation_types: List[str],
    test_dataset: Optional[List[TestCase]] = None,
    metrics_config: Optional[Dict[str, Metric]] = None,
) -> EvaluationFramework:
    """TODO: Core template method - Create evaluation framework.
    
    This is the PRIMARY reusable pattern to extract into your projects.
    
    Args:
        framework_name: Name for evaluation framework
        evaluation_types: List of evaluation types ["rag", "agent", "system", "business"]
        test_dataset: List of TestCase objects (None creates defaults)
        metrics_config: Optional metric configurations
    
    Returns:
        EvaluationFramework: Ready to evaluate systems
    
    Implementation:
    1. If test_dataset is None, create default dataset
    2. Create and return EvaluationFramework instance
    
    EXAMPLE USAGE (for learner projects):
        ```python
        # Define test cases
        test_cases = [
            TestCase(
                test_id="rag_001",
                test_type="retrieval_search",
                input_data={"query": "customer data"},
                expected_output={"documents_found": 2},
                success_criteria="Find 2+ documents"
            ),
            # ... more test cases
        ]
        
        # Create framework
        framework = create_evaluation_framework(
            framework_name="My RAG Evaluator",
            evaluation_types=["rag"],
            test_dataset=test_cases
        )
        
        # Evaluate your system
        results = framework.evaluate_system(my_rag_system, "rag")
        
        # Generate report
        report = framework.generate_report()
        ```
    """
    pass


def _create_default_test_dataset() -> List[TestCase]:
    """TODO: Create default test dataset for demonstrations.
    
    Return list of TestCase objects covering:
    - 2 RAG tests (retrieval_search type)
    - 2 agent tests (agent_task type)
    - 1 system test (system_latency type)
    - 1 business test (business_flow type)
    
    Each should have:
    - Unique test_id
    - Appropriate test_type
    - Input data matching expected output
    - Success criteria description
    - Relevant metadata
    """
    pass


# ============================================================================
# PART 4: Demonstrations (5 Total)
# ============================================================================

def demo_rag_evaluation():
    """TODO: Demo 1 - Evaluate RAG system retrieval quality.
    
    Steps:
    1. Create 2-3 TestCase objects for RAG evaluation
    2. Create framework with create_evaluation_framework()
    3. Define mock_rag_system(query_input) that returns docs
    4. Call framework.evaluate_system(mock_rag_system, "rag")
    5. Print results: total tests, passed, pass rate, average score
    6. Print key metrics (latency, precision, etc.)
    """
    pass


def demo_agent_evaluation():
    """TODO: Demo 2 - Evaluate agent task completion.
    
    Steps:
    1. Create 3 TestCase objects for agent tasks
    2. Create framework
    3. Define mock_agent_system(task_input) that completes tasks
    4. Evaluate
    5. Print results with per-task breakdown
    6. Show each task: PASS/FAIL and score
    """
    pass


def demo_system_evaluation():
    """TODO: Demo 3 - Evaluate system performance metrics.
    
    Steps:
    1. Create 3 TestCase objects:
       - Latency test (P95 response time)
       - Throughput test (requests per second)
       - Cost test (cost per request)
    2. Create framework
    3. Define mock_system(perf_input) that returns metrics
    4. Evaluate
    5. Print results with performance metrics breakdown
    """
    pass


def demo_business_evaluation():
    """TODO: Demo 4 - Evaluate business outcomes.
    
    Steps:
    1. Create 2 TestCase objects for business workflows
    2. Create framework
    3. Define mock_business_system(workflow_input)
    4. Evaluate
    5. Print results: workflow completion, success rate, business impact
    6. Show metrics like time_saved_hours or revenue_impact
    """
    pass


def demo_benchmark_tracking():
    """TODO: Demo 5 - Track improvement across multiple evaluation runs.
    
    Steps:
    1. Create test dataset
    2. Create framework
    3. Define system_fn that "improves" over calls (latency decreases)
    4. Run framework.evaluate_system() 3 times
    5. Compare run 1 (baseline) to run 3 (current)
    6. Use framework.compare_to_baseline() to show improvement
    7. Print comparison: pass rate change, score change, metrics changes
    8. Print framework summary and history
    """
    pass


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # TODO: Print lesson title
    # TODO: Call all 5 demonstrations in order
    # TODO: Print separator lines between demos
    # TODO: Print completion summary with key takeaways
    pass
