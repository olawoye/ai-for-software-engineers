# Module 9: Advanced Capabilities & Specializations

**Objective:** Learn advanced AI topics that experienced engineers increasingly encounter when building differentiated, production-grade AI systems. This module covers fine-tuning for domain specialization, mechanistic interpretability, alignment, and ethical considerations.

**Core Concept:** Beyond generic LLMs → Specialized models for competitive advantage

---

## Module Overview

This module addresses the advanced knowledge gaps that practitioners encounter when building cutting-edge AI solutions:

```
Building AI Systems (Modules 3-6)
     ↓
Designing AI Architecture (Module 7)
     ↓
Operating at Scale (Module 8)
     ↓
Advanced Specialization (Module 9) ← YOU ARE HERE
     ↓
Career & Business (Module 10)
```

---

## ⚠️ Installation Requirements

**Module 9 is OPTIONAL and has separate dependency requirements.**

The main setup script (`setup.sh`) installs dependencies for **Modules 2-7 only** to keep initial setup lightweight.

When you're ready to work on Module 9 (Lesson 9.2 - Fine-Tuning), install the optional dependencies:

```bash
# Only required for PATH 1 (Local Lightweight Fine-Tuning)
pip install -r requirements-module-09.txt
```

**What's in requirements-module-09.txt:**
- `torch>=2.0.0` (PyTorch library, ~2GB)
- `transformers>=4.30.0` (HuggingFace models, ~500MB)

**Which PATH requires which dependencies:**

| Path | Requires Module 9 Deps? | Notes |
|------|-------------------------|-------|
| PATH 1: Local Fine-Tuning | ✅ Yes | Requires `torch` and `transformers` |
| PATH 2: Mock Cloud API | ❌ No | Pure Python simulation, no extra deps |
| PATH 3: Production Templates | ⚠️ Optional | Only if using those cloud APIs |

**Recommendation:** Start with PATH 2 or PATH 3 before installing heavy dependencies. Install Module 9 requirements only when you need local fine-tuning.

---

### Lessons

| Lesson | Type | Status | Focus |
|--------|------|--------|-------|
| 9.1 | Talking Head | Planned | Advanced ML & mechanistic interpretability |
| 9.2 | Code | ✅ COMPLETE | Fine-tuning models for specialization |
| 9.3 | Talking Head | Planned | LoRA & QLoRA for efficient fine-tuning |
| 9.4 | Talking Head | Planned | RLHF & Model Alignment |
| 9.5 | Talking Head | Planned | Ethical AI & Bias |

---

## Lesson 9.2: Fine-Tuning Models for Specialized Use Cases

**Status:** ✅ Complete and verified (1400+ lines production code, 400+ lines TODO scaffold)

**Type:** Code Screencast (Production-Ready Tool with 3 Implementation Paths)

### Core Concept

**This is NOT a one-time lesson tool — it's a PRODUCTION-READY toolkit you can extract and use in your own projects.**

#### Business Scenario

A legal consulting firm needs specialized LLM for contract drafting. Challenge: Generic LLMs don't follow firm conventions. Solution: Fine-tune on firm-specific examples to create specialized model.

#### When to Fine-Tune?

| Approach | Use When | Cost | Time | Quality |
|----------|----------|------|------|---------|
| **Fine-Tuning** | Need domain-specific behavior (50+ examples) | $2-50 | 5min-1hr | ⭐⭐⭐⭐⭐ |
| **RAG** | Reference knowledge base | $0-10 | 1-5min | ⭐⭐⭐⭐ |
| **Prompt Engineering** | Quick prototyping, limited data | $0-5 | min-hrs | ⭐⭐⭐ |
| **Hybrid** | Maximum quality, both approaches | $10-50 | 1-2hrs | ⭐⭐⭐⭐⭐ |

### Three Implementation Paths

This lesson provides **three distinct paths** for fine-tuning:

#### PATH 1: Local Lightweight Fine-Tuning

**Run immediately on your machine (CPU-friendly)**

```bash
python lesson-02-fine-tuning-models.py
# Select: 1 - Local Lightweight Demo
```

- **Model:** DistilGPT-2 (4.4M parameters, CPU-friendly)
- **Dataset:** 10 legal contract examples
- **Output:** Before/after quality comparison
- **Cost:** $0 (local processing)
- **Setup:** `pip install transformers torch`
- **Time:** ~30 seconds

**What you'll learn:**
- Dataset preparation in instruction-following format
- How fine-tuning changes model behavior
- Quality improvement metrics (baseline vs. fine-tuned)

#### PATH 2: Mock Cloud API Simulation

**Realistic workflow without cloud costs**

```bash
python lesson-02-fine-tuning-models.py
# Select: 2 - Mock Cloud API Simulation
```

- **Simulates:** OpenAI/Anthropic fine-tuning API
- **Shows:** Job submission, status polling, cost calculation
- **Cost:** $0 (mock only)
- **Time:** ~5 seconds
- **Setup:** No dependencies

**What you'll learn:**
- Real API workflow (queue → process → complete)
- Job tracking and status monitoring
- Cost estimation for your dataset

#### PATH 3: Production Code Templates

**Copy-paste ready code for real fine-tuning services**

```bash
python lesson-02-fine-tuning-models.py
# Select: 3 - Production Code Templates
```

Provides ready-to-use code for:

1. **OpenAI Fine-Tuning API**
   - Models: GPT-3.5-turbo, GPT-4
   - Cost: $3 per 1M training tokens
   - Setup: `pip install openai` + API key

2. **Together.ai Fine-Tuning**
   - Models: Llama 2, Mistral (open-source)
   - Cost: $2.50 per job
   - Setup: `pip install together` + API key

3. **Replicate Fine-Tuning**
   - Serverless training (no GPU setup needed)
   - Cost: $1.00 per job
   - Setup: `pip install replicate` + API key

**Each template includes:**
- Dependency installation
- Dataset preparation (JSON-L format)
- Job submission
- Polling for completion
- Model usage example

### Decision Framework

**When to use fine-tuning vs. alternatives:**

```python
# Decision Tree
if "Need domain-specific behavior" and "Have 50+ examples":
    → Fine-tune
elif "Need to reference knowledge base":
    → Use RAG (faster, cheaper)
elif "Need quick prototype" or "Limited data":
    → Prompt engineering
elif "Maximum quality required":
    → Combine fine-tune + RAG (hybrid)
```

### Cost Calculator

Interactive tool to estimate costs for your dataset:

```bash
python lesson-02-fine-tuning-models.py
# Select: 5 - Cost Calculator
```

Compares:
- Local GPU training ($0.50/hour)
- OpenAI ($3 per 1M tokens)
- Together.ai ($2.50/job)
- Replicate ($1.00/job)

---

## Running Lesson 9.2

### Prerequisites

**Minimum (to run all paths):**
```bash
# No dependencies required for mock API simulation
python lesson-02-fine-tuning-models.py
```

**Optional (for local fine-tuning):**
```bash
pip install transformers torch
# Then select PATH 1 for local demo
```

**For production (real cloud APIs):**
```bash
pip install openai  # For OpenAI
pip install together  # For Together.ai
pip install replicate  # For Replicate
```

### Quick Start

```bash
# Run interactive menu
python project-completed/module-09-advanced-capabilities-specializations/lesson-02-fine-tuning-models.py

# Choose path:
# 1 = Local demo (requires transformers, torch)
# 2 = Mock API simulation (no dependencies)
# 3 = Production templates (step-by-step code)
# 4 = Decision framework
# 5 = Cost calculator
```

### Example: Production Setup

For OpenAI fine-tuning:

```bash
# 1. Install OpenAI client
pip install openai

# 2. Set API key
export OPENAI_API_KEY="your-api-key"

# 3. Copy template from lesson
python lesson-02-fine-tuning-models.py
# Select: 3 - Production Code Templates → 1. OpenAI

# 4. Customize and run
# (See template for step-by-step code)
```

---

## Key Reusable Components

### Core Data Structures

```python
# Define a training example
FineTuningExample(
    instruction="Draft a legal clause",
    input_text="non-disclosure agreement",
    output="Confidential information shared..."
)

# Create dataset
dataset = FineTuningDataset(
    name="legal_contracts_v1",
    examples=[ex1, ex2, ex3],
    domain="legal",
    source="curated"
)
```

### Local Fine-Tuning Pattern

```python
from lesson-02-fine-tuning-models import LocalFineTuner

tuner = LocalFineTuner()
job, evaluations = tuner.fine_tune(dataset, epochs=3)

print(f"Model: {job.fine_tuned_model}")
for eval in evaluations:
    print(f"Improvement: +{eval.improvement:.2f}")
```

### Mock API Workflow

```python
from lesson-02-fine-tuning-models import MockCloudAPI

api = MockCloudAPI()
job = api.submit_fine_tuning_job(dataset, model_name="gpt-3.5-turbo")

# Poll for completion
while api.get_job_status(job.job_id).status != "completed":
    time.sleep(30)

result = api.retrieve_fine_tuned_model(job.job_id)
```

### Production Template (OpenAI)

See `lesson-02-fine-tuning-models.py` → `get_openai_fine_tuning_template()`

---

## Resource Scripts

### `resource_fine_tuning_utils.py`

Production-grade utilities for fine-tuning:

```python
from resource_fine_tuning_utils import (
    prepare_dataset_for_openai,
    estimate_fine_tuning_cost,
    compare_fine_tuning_services,
    evaluate_cost_benefit,
)

# Prepare dataset
examples = [{"prompt": "...", "completion": " ..."}]
jsonl_str = prepare_dataset_for_openai(examples)

# Estimate costs
costs = estimate_fine_tuning_cost(
    num_training_examples=100,
    avg_tokens_per_example=200
)

# Compare services
comparison = compare_fine_tuning_services()

# Analyze ROI
roi = evaluate_cost_benefit(
    fine_tuning_cost=5.00,
    improvement_percentage=25.0
)
```

**Key functions:**
- `prepare_dataset_for_openai()` — JSON-L formatting
- `prepare_dataset_for_together_ai()` — Instruction-following format
- `validate_dataset()` — Check quality before fine-tuning
- `estimate_fine_tuning_cost()` — Compare all services
- `calculate_improvement()` — Measure quality gains
- `evaluate_cost_benefit()` — ROI analysis
- `get_fine_tuning_checklist()` — Pre-fine-tuning validation
- `get_common_mistakes()` — Best practices

**Run examples:**
```bash
python resource_fine_tuning_utils.py
```

---

## Learning Objectives

After completing Lesson 9.2, you will understand:

1. **When to fine-tune** — Decision framework for choosing approaches
2. **How to prepare data** — Instruction-following format, validation
3. **Fine-tuning workflow** — Submit → poll → evaluate
4. **Cost-benefit analysis** — Compare services, calculate ROI
5. **Production patterns** — Extract and use templates in projects
6. **Evaluation methods** — Compare baseline vs. fine-tuned models

---

## Business Scenarios Covered

1. **Legal Consulting Firm** (primary)
   - Fine-tune for specialized contract drafting
   - Domain-specific formatting and clauses
   - Consistency with firm standards

2. **Technical Documentation** (alternative)
   - Fine-tune for API documentation writing
   - Technical terminology consistency
   - Code examples integration

3. **Customer Support** (alternative)
   - Fine-tune for brand voice consistency
   - Knowledge base integration
   - Response formatting

---

## Next Steps

### Continue Learning

- **Lesson 9.3:** LoRA & QLoRA (efficient fine-tuning)
- **Lesson 9.4:** RLHF & Alignment (reinforcement learning)
- **Lesson 9.5:** Ethical AI & Bias (responsible AI)
- **Module 10:** Career & Business (monetization)

### Build Projects

Use fine-tuning templates to:
- Fine-tune model for your domain
- Compare baseline vs. fine-tuned quality
- Calculate ROI and cost-benefit
- Deploy to production

### Hybrid Approaches

Combine with Module 4 (RAG):
```
Fine-tuned model (domain behavior)
         ↓
       RAG (domain knowledge)
         ↓
Maximum quality + up-to-date info
```

---

## Common Mistakes & Solutions

| Mistake | Problem | Solution |
|---------|---------|----------|
| Too few examples | Overfitting | Collect 50-100+ examples |
| Inconsistent format | Model learns noise | Standardize all examples |
| Duplicates | Overfitting | Remove duplicates |
| Sensitive data | Privacy leak | Remove PII, credentials |
| No baseline eval | Can't measure improvement | Evaluate base model first |
| Wrong LR | Model diverges | Start with defaults, tune gradually |

---

## File Structure

```
project-completed/module-09-advanced-capabilities-specializations/
├── lesson-02-fine-tuning-models.py          # Main lesson (1400+ lines)
├── resource_fine_tuning_utils.py            # Reusable utilities
├── README.md                                # This file

project-todo/module-09-advanced-capabilities-specializations/
├── lesson-02-fine-tuning-models.py          # Phase-based scaffold (400+ lines)
```

---

## Cost Reference

**Estimating fine-tuning costs:**

```
Dataset: 100 examples × 200 tokens/example × 3 epochs = 60,000 tokens

Service          Cost              Time      Setup
OpenAI           $0.18             1-5 min   Easy
Together.ai      $2.50             1-5 min   Easy
Replicate        $1.00             1-5 min   Easy
Local GPU        $0.60             10 min    Complex
```

---

## Verification

✅ Lesson 9.2 syntax verified  
✅ Menu-driven CLI functional  
✅ All 3 paths implemented  
✅ Resource utilities working  
✅ Production templates ready  

Run verification:
```bash
python3 -m py_compile project-completed/module-09-advanced-capabilities-specializations/lesson-02-fine-tuning-models.py
python3 project-completed/module-09-advanced-capabilities-specializations/resource_fine_tuning_utils.py
```

---

## Key Takeaways

1. **Fine-tuning creates specialized models** for competitive advantage
2. **Decision framework matters** — not all use cases need fine-tuning
3. **Real-world fine-tuning uses cloud APIs** — start with mock simulation
4. **Cost-benefit analysis is critical** — ROI must justify investment
5. **Three implementation paths** cater to different learning stages
6. **Production templates are extraction-ready** — copy into your projects

---

## Next Module

**Module 10: Career Transition & Monetization**
- Build AI portfolio with fine-tuned models
- Monetize AI skills
- Career paths for AI engineers
