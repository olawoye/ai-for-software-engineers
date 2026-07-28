# Module 7: Designing AI-Native Systems

**Objective:** Learn how to think like an AI system architect rather than an AI application developer. Design scalable AI-native platforms, evaluate architectural tradeoffs, engineer context effectively, and build systems that remain reliable and measurable.

**Core Concept:** Architecture = Context engineering + Design patterns + Human oversight + Systematic evaluation

---

## Module Overview

This module bridges **building AI systems** (Modules 3-6) with **operating AI systems** (Modules 8-9):

```
Modules 3-6: Building AI Systems
     ↓
Module 7: Designing AI-Native Systems (ARCHITECTURE)
     ↓
Modules 8-9: Operating & Optimizing AI Systems
```

### Lessons

| Lesson | Type | Status | Focus |
|--------|------|--------|-------|
| 7.1 | Talking Head | Planned | Architectural patterns & application types |
| 7.2 | Talking Head | Planned | Context engineering discipline |
| 7.3 | Talking Head | Planned | Design patterns for AI systems |
| 7.4 | Talking Head | Planned | Human-in-the-loop mechanisms |
| 7.5 | Code | ✅ COMPLETE | Evaluation frameworks & benchmarking |

---

## Lesson 7.5: Evaluation & Performance Frameworks

**Status:** ✅ Complete and verified (1200+ lines production code, 400+ lines TODO scaffold)

**Type:** Code Screencast (Production-Ready Tool)

### Core Concept

**This is NOT a one-time course tool — it's a PRODUCTION-READY framework you can extract and use in your own projects.**

Systematic evaluation distinguishes:
- **Subjective Assessment:** "The system seems to be working"
- **Professional Evaluation:** "The system has 92% retrieval precision, processes 95 RPS, costs $0.005/request, and saves 2.5 hours/week"

### Core Template Method

```python
framework = create_evaluation_framework(
    framework_name="My AI System Evaluator",
    evaluation_types=["rag", "agent", "system", "business"],
    test_dataset=test_cases,  # List[TestCase]
)

# Evaluate your system
results = framework.evaluate_system(my_system_fn, "rag")

# Compare to baseline
improvement = framework.compare_to_baseline(baseline_results)

# Generate report
report = framework.generate_report()
```

### Architecture

**Reusable Components:**

1. **TestCase** — Define a single test scenario
   - Input data, expected output, success criteria
   - Metadata (latency, cost, time savings)
   - Extensible for any AI system

2. **Metric** — Define a measurable performance metric
   - Name, calculation function, unit, target value
   - Examples: precision, recall, latency_p95, cost_per_request, success_rate

3. **EvaluationResult** — Score for a single test
   - Test case reference, actual output, pass/fail, numeric score (0.0-1.0)
   - Metrics calculated, execution duration, any errors

4. **Benchmark** — Aggregate results from evaluation run
   - Total tests, passed/failed counts, pass rate, average score
   - Aggregated metrics summary, execution time

5. **EvaluationFramework** — Main reusable container
   - Orchestrates evaluation across test cases
   - Scores results, aggregates metrics
   - Tracks evaluation history for benchmarking
   - Compares current vs. baseline results

### Evaluation Types

Framework supports 4 evaluation types (extensible):

| Type | Use Case | Example Metrics |
|------|----------|-----------------|
| **RAG** | Retrieval quality | Precision, Recall, F1 Score |
| **AGENT** | Task completion | Task success rate, tool success rate, goal completion |
| **SYSTEM** | Performance | P95 Latency, Throughput (RPS), Cost per request |
| **BUSINESS** | Business outcomes | Workflow completion, Time saved, Revenue impact, User satisfaction |

### Business Scenario

"A company deployed AI agents from Module 6 but can't measure whether the system is working:
- Does retrieval find relevant documents? (RAG evaluation)
- Do agents complete tasks? (Agent evaluation)
- How fast does it run? How much does it cost? (System evaluation)
- Does it save time and money? (Business evaluation)

Solution: Systematic evaluation framework that measures all four dimensions."

### Demonstrations (5 Total)

#### Demo 1: RAG Evaluation
Measure retrieval quality of knowledge-based systems.
- 2 test cases: different queries
- Mock RAG system returns documents
- Results: 2/2 passing, 100% precision

**Output:**
```
✓ Total Tests: 2
✓ Passed: 2
✓ Pass Rate: 100.0%
✓ Average Score: 1.00
Key Metrics:
  • latency: 0.300s
```

#### Demo 2: Agent Evaluation
Measure agent task completion rates.
- 3 test cases: different task types (find overdue accounts, analyze feedback, create report)
- Mock agent system completes each task
- Results: 3/3 passing

**Output:**
```
✓ Total Tasks: 3
✓ Completed: 3
✓ Completion Rate: 100.0%
✓ Average Quality: 1.00

Agent Performance Breakdown:
  1. Task agent_1: ✓ PASS (Score: 1.00)
  2. Task agent_2: ✓ PASS (Score: 1.00)
  3. Task agent_3: ✓ PASS (Score: 1.00)
```

#### Demo 3: System Evaluation
Measure system performance metrics.
- 3 test cases: latency, throughput, cost
- Mock system returns performance data
- Results: 3/3 passing

**Output:**
```
✓ Tests Run: 3
✓ Passed: 3
✓ Pass Rate: 100.0%

System Metrics:
  • P95 Latency: 0.420s
  • Throughput: 95 RPS
  • Cost per Request: $0.0048
```

#### Demo 4: Business Evaluation
Measure business outcomes and ROI.
- 2 test cases: daily reports (save 2.5 hours), account recovery (improve recovery rate)
- Mock business system shows outcomes
- Results: 2/2 passing

**Output:**
```
✓ Workflows Evaluated: 2
✓ Successful: 2
✓ Success Rate: 100.0%
✓ Average Impact Score: 1.00

Business Outcomes:
  • Total Time Saved: 3.2 hours
  • User Satisfaction: 92%
```

#### Demo 5: Benchmark Tracking
Track improvement across multiple evaluation runs.
- Run framework 3 times (simulating gradual improvement)
- Compare baseline (run 1) to current (run 3)
- Show improvement analysis

**Output:**
```
Baseline (Run 1):
  Pass Rate: 100.0%
  Average Score: 1.00

Current (Run 3):
  Pass Rate: 100.0%
  Average Score: 1.00

Framework Summary:
  Total Benchmarks: 3
  Test Cases: 2
```

### Run Instructions

```bash
cd project-completed/module-07-designing-ai-native-systems
python3 lesson-05-evaluation-frameworks.py
```

**Output:** All 5 demonstrations execute with 100% pass rates across all evaluation types.

### Key Classes & Methods

**Core Template Method:**
```python
create_evaluation_framework(
    framework_name: str,
    evaluation_types: List[str],  # ["rag", "agent", "system", "business"]
    test_dataset: Optional[List[TestCase]] = None,
    metrics_config: Optional[Dict[str, Metric]] = None,
) -> EvaluationFramework
```

**Primary Methods:**
- `framework.evaluate_system(system_fn, evaluation_type)` — Run evaluation
- `framework.generate_report()` — Create evaluation report
- `framework.compare_to_baseline(baseline)` — Compare to previous results
- `framework.get_summary()` — Get framework summary and history

**Data Classes:**
- `TestCase` — Single test scenario
- `Metric` — Performance metric definition
- `EvaluationResult` — Score for single test
- `Benchmark` — Aggregated results from evaluation run
- `EvaluationType` — Enum: RAG, AGENT, SYSTEM, BUSINESS

### Scoring Logic

**Score Calculation (0.0 to 1.0):**
- Dict matching: Percentage of keys matching and values within tolerance
- String matching: Word overlap similarity (Jaccard index)
- Boolean matching: Exact equality
- Fallback: 0.6 partial credit for attempting

**Pass Criteria:** Score >= 0.8 (80%) passes the test

### Extensibility

**Customize for your systems:**

1. **Add new evaluation types:**
   ```python
   def _evaluate_custom(self, test_input):
       return {"custom_metric": value}
   ```

2. **Override scoring logic:**
   ```python
   def _score_result(self, test_case, actual_output):
       # Your custom scoring
       return score, metrics
   ```

3. **Add new metrics:**
   - Define in `metrics_config` when creating framework
   - Include in test case metadata

### Integration Points

**Works with:**
- Module 6 agents (evaluate agent task completion)
- RAG systems (evaluate retrieval quality)
- Any callable system (evaluate performance, business outcomes)
- Historical data (benchmark tracking)

### Reusable Pattern for Your Projects

Extract this lesson into your projects:

```python
# Step 1: Define test cases
test_cases = [
    TestCase(
        test_id="eval_001",
        test_type="retrieval_search",
        input_data={"query": "your query"},
        expected_output={"result": "expected"},
        success_criteria="Criteria description",
        metadata={"latency": 0.35}
    ),
    # ... more test cases
]

# Step 2: Create framework
framework = create_evaluation_framework(
    framework_name="My Custom Evaluator",
    evaluation_types=["rag"],
    test_dataset=test_cases
)

# Step 3: Evaluate your system
results = framework.evaluate_system(your_system_function, "rag")

# Step 4: Generate insights
report = framework.generate_report()
improvement = framework.compare_to_baseline(baseline)

# Step 5: Use data for decision-making
print(f"Pass rate: {results.pass_rate:.1%}")
print(f"Average score: {results.average_score:.2f}")
print(f"Improvement vs baseline: {improvement}")
```

### Files

- **Completed:** [lesson-05-evaluation-frameworks.py](lesson-05-evaluation-frameworks.py) (1200+ lines, verified working)
- **TODO Scaffold:** [project-todo/module-07-designing-ai-native-systems/lesson-05-evaluation-frameworks.py](../../project-todo/module-07-designing-ai-native-systems/lesson-05-evaluation-frameworks.py) (400+ lines, phase-based guidance)
- **Tests:** 5 demonstrations covering all evaluation types

### Learning Outcomes

After this lesson, you will understand:

1. ✅ How to design systematic evaluation for AI systems
2. ✅ How to define meaningful test cases and metrics
3. ✅ How to measure retrieval quality, agent performance, system efficiency, and business impact
4. ✅ How to compare systems using benchmarks
5. ✅ How to track improvement over time
6. ✅ How to build and extract production-ready evaluation tools

### Next Steps

**Module 8: Production AI Systems**
- Lesson 8.1: Deployment strategies
- Lesson 8.2: Security & reliability
- Lesson 8.3: Observability & monitoring

---

## Module-Level Architecture

```
Lesson 7.1 (Talking Head)
Architectural Patterns & Application Types
         ↓
Lesson 7.2 (Talking Head)
Context Engineering Discipline
         ↓
Lesson 7.3 (Talking Head)
Design Patterns for AI Systems
         ↓
Lesson 7.4 (Talking Head)
Human-in-the-Loop Mechanisms
         ↓
Lesson 7.5 (Code) ✅
Evaluation & Performance Frameworks
         ↓
Module 8 Foundation: Production AI Systems
```

---

## Business Value

By completing this module, learners can:

- **Design** scalable, maintainable AI-native systems
- **Architect** systems that balance automation, cost, and reliability
- **Evaluate** AI systems using professional measurement standards
- **Compare** different AI approaches quantitatively
- **Track** improvement over time with benchmarks
- **Make** data-driven decisions about system changes

These are the skills associated with **senior AI architects**, **technical leads**, and **platform engineers** responsible for designing enterprise-grade AI systems.
