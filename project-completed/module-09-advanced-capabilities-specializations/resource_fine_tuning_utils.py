"""
resource_fine_tuning_utils.py

Reusable utilities for fine-tuning language models.
Extract and use these functions in your own projects.

This module provides production-ready helpers for:
  • Dataset preparation and validation
  • Fine-tuning service comparison
  • Cost calculation and estimation
  • Model performance evaluation
  • Common deployment patterns

USAGE:
  from resource_fine_tuning_utils import (
      prepare_dataset_for_openai,
      estimate_fine_tuning_cost,
      compare_fine_tuning_services,
      evaluate_model_improvement
  )
"""

import json
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


# ============================================================================
# DATASET PREPARATION
# ============================================================================

@dataclass
class TrainingExample:
    """Single training example."""
    instruction: str
    input_text: str = ""
    output: str = ""


def prepare_dataset_for_openai(examples: List[Dict]) -> str:
    """
    Prepare dataset in OpenAI fine-tuning JSON-L format.
    
    WHY: OpenAI requires specific JSON-L format for fine-tuning
    WHAT: Converts list of dicts to JSON-L lines
    HOW:
      1. Validate each example has 'prompt' and 'completion'
      2. Format as JSON objects
      3. Join with newlines
    
    Args:
        examples: List of dicts with 'prompt' and 'completion' keys
    
    Returns:
        JSON-L formatted string (one JSON object per line)
    
    Example:
        examples = [
            {"prompt": "Draft a clause", "completion": " Confidential..."},
            {"prompt": "Write terms", "completion": " Terms are..."}
        ]
        jsonl_str = prepare_dataset_for_openai(examples)
        # Save to file
        with open("training.jsonl", "w") as f:
            f.write(jsonl_str)
    """
    
    jsonl_lines = []
    for i, ex in enumerate(examples):
        if "prompt" not in ex or "completion" not in ex:
            raise ValueError(f"Example {i} missing 'prompt' or 'completion' key")
        
        # Ensure completion starts with a space (OpenAI convention)
        completion = ex["completion"]
        if completion and not completion.startswith(" "):
            completion = " " + completion
        
        line = json.dumps({
            "prompt": ex["prompt"],
            "completion": completion
        })
        jsonl_lines.append(line)
    
    return "\n".join(jsonl_lines)


def prepare_dataset_for_together_ai(examples: List[Dict]) -> str:
    """
    Prepare dataset for Together.ai fine-tuning (instruction-following format).
    
    WHY: Together.ai uses instruction-following format with input/output
    WHAT: Converts to {"instruction": ..., "input": ..., "output": ...} format
    HOW:
      1. Map fields to instruction-following format
      2. Validate required fields
      3. Format as JSON-L
    
    Args:
        examples: List of dicts with 'instruction', 'input', 'output' keys
    
    Returns:
        JSON-L formatted string
    
    Example:
        examples = [
            {
                "instruction": "Draft a legal clause",
                "input": "non-disclosure agreement",
                "output": "Confidential information..."
            }
        ]
        jsonl_str = prepare_dataset_for_together_ai(examples)
    """
    
    jsonl_lines = []
    for i, ex in enumerate(examples):
        required = ["instruction", "output"]
        if not all(k in ex for k in required):
            raise ValueError(f"Example {i} missing required fields: {required}")
        
        line = json.dumps({
            "instruction": ex["instruction"],
            "input": ex.get("input", ""),
            "output": ex["output"]
        })
        jsonl_lines.append(line)
    
    return "\n".join(jsonl_lines)


def validate_dataset(
    examples: List[Dict],
    min_examples: int = 10,
    max_prompt_length: int = 2048,
    max_completion_length: int = 512
) -> Dict:
    """
    Validate fine-tuning dataset.
    
    Checks:
      • Minimum number of examples
      • Prompt/completion field presence
      • Text length limits
      • Diversity (prevents overfitting to small datasets)
    
    Args:
        examples: Training examples to validate
        min_examples: Minimum examples required
        max_prompt_length: Max characters in prompt
        max_completion_length: Max characters in completion
    
    Returns:
        Dict with validation results and warnings
    
    Example:
        validation = validate_dataset(my_examples)
        if validation["is_valid"]:
            print(f"✓ Dataset valid: {validation['example_count']} examples")
        else:
            print(f"✗ Validation errors:")
            for error in validation["errors"]:
                print(f"  - {error}")
    """
    
    errors = []
    warnings = []
    
    # Check example count
    if len(examples) < min_examples:
        errors.append(f"Need at least {min_examples} examples, got {len(examples)}")
    
    # Check each example
    for i, ex in enumerate(examples):
        if "prompt" not in ex and "instruction" not in ex:
            errors.append(f"Example {i}: Missing prompt or instruction field")
        
        if "completion" not in ex and "output" not in ex:
            errors.append(f"Example {i}: Missing completion or output field")
        
        # Check lengths
        prompt = ex.get("prompt") or ex.get("instruction") or ""
        completion = ex.get("completion") or ex.get("output") or ""
        
        if len(prompt) > max_prompt_length:
            warnings.append(f"Example {i}: Prompt exceeds {max_prompt_length} chars")
        
        if len(completion) > max_completion_length:
            warnings.append(f"Example {i}: Completion exceeds {max_completion_length} chars")
    
    return {
        "is_valid": len(errors) == 0,
        "example_count": len(examples),
        "errors": errors,
        "warnings": warnings,
    }


# ============================================================================
# COST CALCULATION
# ============================================================================

@dataclass
class PricingInfo:
    """Pricing for fine-tuning services."""
    service: str
    price_per_1m_training_tokens: Optional[float] = None
    price_per_1m_usage_tokens: Optional[float] = None
    fixed_price_per_job: Optional[float] = None
    gpu_hourly_rate: Optional[float] = None
    description: str = ""


def estimate_fine_tuning_cost(
    num_training_examples: int,
    avg_tokens_per_example: int = 150,
    num_training_epochs: int = 3,
    approach: str = "cloud_api"
) -> Dict:
    """
    Estimate fine-tuning costs across different approaches.
    
    WHY: Help choose most cost-effective fine-tuning service
    WHAT: Calculate costs for local GPU, OpenAI, Together.ai, Replicate
    HOW:
      1. Calculate total training tokens
      2. Apply service-specific pricing
      3. Compare options with recommendations
    
    Args:
        num_training_examples: Number of training examples
        avg_tokens_per_example: Average tokens per example (default 150)
        num_training_epochs: Number of training epochs (default 3)
        approach: "cloud_api" (default) or "local_gpu"
    
    Returns:
        Dict with cost breakdown for each service
    
    Example:
        costs = estimate_fine_tuning_cost(
            num_training_examples=100,
            avg_tokens_per_example=200,
            num_training_epochs=3
        )
        print(f"OpenAI cost: ${costs['openai']['total_cost']:.2f}")
        print(f"Together.ai cost: ${costs['together_ai']['total_cost']:.2f}")
    """
    
    # Calculate total tokens
    total_tokens = num_training_examples * avg_tokens_per_example * num_training_epochs
    
    # Service pricing
    pricing = {
        "openai": {
            "name": "OpenAI Fine-Tuning",
            "price_per_1m": 3.00,
            "models": ["gpt-3.5-turbo"],
        },
        "together_ai": {
            "name": "Together.ai",
            "fixed_price": 2.50,
            "models": ["Llama 2", "Mistral"],
        },
        "replicate": {
            "name": "Replicate",
            "fixed_price": 1.00,
            "models": ["Any model"],
        },
        "local_gpu": {
            "name": "Local GPU (EC2, Lambda)",
            "hourly_rate": 0.50,
            "tokens_per_hour": 50000,
        },
    }
    
    # Calculate costs
    costs = {}
    
    # OpenAI
    openai_cost = (total_tokens / 1_000_000) * pricing["openai"]["price_per_1m"]
    costs["openai"] = {
        "service": pricing["openai"]["name"],
        "total_cost": openai_cost,
        "breakdown": f"${openai_cost:.2f}",
    }
    
    # Together.ai
    costs["together_ai"] = {
        "service": pricing["together_ai"]["name"],
        "total_cost": pricing["together_ai"]["fixed_price"],
        "breakdown": f"${pricing['together_ai']['fixed_price']:.2f} (fixed)",
    }
    
    # Replicate
    costs["replicate"] = {
        "service": pricing["replicate"]["name"],
        "total_cost": pricing["replicate"]["fixed_price"],
        "breakdown": f"${pricing['replicate']['fixed_price']:.2f} (fixed)",
    }
    
    # Local GPU
    hours_needed = total_tokens / pricing["local_gpu"]["tokens_per_hour"]
    local_cost = hours_needed * pricing["local_gpu"]["hourly_rate"]
    costs["local_gpu"] = {
        "service": pricing["local_gpu"]["name"],
        "total_cost": local_cost,
        "breakdown": f"${local_cost:.2f} ({hours_needed:.1f} hours @ $0.50/hr)",
    }
    
    return {
        "total_tokens": total_tokens,
        "num_examples": num_training_examples,
        "epochs": num_training_epochs,
        "costs": costs,
    }


def compare_fine_tuning_services() -> Dict:
    """
    Compare major fine-tuning services.
    
    Returns matrix of: Cost, Setup Time, Quality, Effort
    
    Example:
        comparison = compare_fine_tuning_services()
        for service, details in comparison.items():
            print(f"{service}:")
            print(f"  Cost: {details['cost']}")
            print(f"  Quality: {details['quality']}")
    """
    
    return {
        "OpenAI": {
            "cost": "$3 per 1M tokens",
            "setup_time": "5 minutes",
            "quality": "⭐⭐⭐⭐⭐",
            "effort": "Low",
            "pros": ["Easiest API", "Best documentation", "Popular"],
            "cons": ["Most expensive per token", "Limited to OpenAI models"],
        },
        "Together.ai": {
            "cost": "$2.50 per job",
            "setup_time": "5 minutes",
            "quality": "⭐⭐⭐⭐⭐",
            "effort": "Low",
            "pros": ["Cheapest fixed price", "Open-source models", "Good docs"],
            "cons": ["Only works with specific models", "Smaller community"],
        },
        "Replicate": {
            "cost": "$1.00 per job",
            "setup_time": "5 minutes",
            "quality": "⭐⭐⭐⭐",
            "effort": "Low",
            "pros": ["Cheapest option", "Simple API", "No GPU setup"],
            "cons": ["Limited customization", "Smaller community"],
        },
        "Local GPU": {
            "cost": "$0.50 per hour",
            "setup_time": "30 minutes",
            "quality": "⭐⭐⭐⭐⭐",
            "effort": "High",
            "pros": ["Most control", "Can optimize hyperparameters", "No per-use cost"],
            "cons": ["Complex setup", "Infrastructure maintenance", "GPU cost"],
        },
    }


# ============================================================================
# MODEL EVALUATION
# ============================================================================

def calculate_improvement(
    baseline_scores: List[float],
    fine_tuned_scores: List[float]
) -> Dict:
    """
    Calculate improvement after fine-tuning.
    
    Args:
        baseline_scores: Model scores before fine-tuning
        fine_tuned_scores: Model scores after fine-tuning
    
    Returns:
        Dict with improvement metrics
    
    Example:
        improvement = calculate_improvement(
            baseline_scores=[0.6, 0.65, 0.62],
            fine_tuned_scores=[0.92, 0.88, 0.90]
        )
        print(f"Average improvement: +{improvement['average_improvement']:.2f}")
    """
    
    if len(baseline_scores) != len(fine_tuned_scores):
        raise ValueError("Baseline and fine-tuned scores must have same length")
    
    improvements = [ft - bl for bl, ft in zip(baseline_scores, fine_tuned_scores)]
    
    return {
        "average_improvement": sum(improvements) / len(improvements),
        "max_improvement": max(improvements),
        "min_improvement": min(improvements),
        "improvement_percentage": (sum(improvements) / len(improvements)) * 100,
    }


def evaluate_cost_benefit(
    fine_tuning_cost: float,
    improvement_percentage: float,
    daily_api_calls: int = 1000,
    cost_per_1k_calls_baseline: float = 0.015,
    cost_per_1k_calls_fine_tuned: float = 0.015,
) -> Dict:
    """
    Evaluate cost-benefit of fine-tuning.
    
    Considers:
      • One-time fine-tuning cost
      • Improved quality reducing need for retries
      • ROI from quality improvement
    
    Example:
        roi = evaluate_cost_benefit(
            fine_tuning_cost=5.00,
            improvement_percentage=25.0,
            daily_api_calls=1000
        )
        payback_days = roi["payback_period_days"]
        print(f"ROI positive in {payback_days} days")
    """
    
    # Estimate monthly savings from quality improvement
    # Better model = fewer retries needed
    monthly_calls = daily_api_calls * 30
    monthly_api_cost = (monthly_calls / 1000) * cost_per_1k_calls_baseline
    
    # Savings from quality improvement (fewer retries)
    # Example: 25% improvement = 25% fewer retries needed
    monthly_savings = monthly_api_cost * (improvement_percentage / 100) * 0.5  # Conservative
    
    payback_days = fine_tuning_cost / (monthly_savings / 30) if monthly_savings > 0 else float('inf')
    
    return {
        "fine_tuning_cost": fine_tuning_cost,
        "estimated_monthly_savings": monthly_savings,
        "payback_period_days": payback_days,
        "profitable": payback_days < 90,  # ROI within 90 days = good
        "recommendation": "Proceed with fine-tuning" if payback_days < 90 else "Consider alternatives",
    }


# ============================================================================
# COMMON PATTERNS FOR LEARNERS
# ============================================================================

def get_fine_tuning_checklist() -> List[str]:
    """
    Pre-fine-tuning checklist.
    
    Returns:
        List of items to verify before fine-tuning
    """
    
    return [
        "✓ Dataset has 50+ quality examples (minimum 10)",
        "✓ Examples are representative of production use cases",
        "✓ Examples are diverse (not repetitive)",
        "✓ Prompts and completions are well-formatted",
        "✓ No sensitive data in training examples",
        "✓ Base model chosen (GPT-3.5-turbo vs. Claude vs. open-source)",
        "✓ Cost estimated and approved",
        "✓ Evaluation metrics defined (how to measure quality improvement)",
        "✓ Baseline model evaluated (before fine-tuning)",
        "✓ API credentials secured (never hardcode keys)",
    ]


def get_common_mistakes() -> Dict:
    """
    Common fine-tuning mistakes and how to avoid them.
    
    Returns:
        Dict of mistake -> solution
    """
    
    return {
        "Too few examples": {
            "problem": "Fine-tuning with <10 examples leads to overfitting",
            "solution": "Collect at least 50-100 representative examples",
        },
        "Inconsistent formatting": {
            "problem": "Model learns inconsistent patterns if examples vary",
            "solution": "Standardize all prompts and completions format",
        },
        "Duplicates in dataset": {
            "problem": "Duplicates cause overfitting",
            "solution": "Remove duplicates before fine-tuning",
        },
        "Sensitive data": {
            "problem": "Fine-tuning can leak sensitive information",
            "solution": "Remove PII, credentials, and confidential info",
        },
        "No baseline evaluation": {
            "problem": "Can't measure if fine-tuning actually helped",
            "solution": "Evaluate base model first, then compare fine-tuned",
        },
        "Wrong hyperparameters": {
            "problem": "Learning rate too high → model diverges",
            "solution": "Start with default hyperparameters, tune gradually",
        },
    }


# ============================================================================
# MAIN: Example usage
# ============================================================================

if __name__ == "__main__":
    print("Fine-Tuning Utilities Examples\n")
    print("="*70)
    
    # Example 1: Validate dataset
    print("\n1. DATASET VALIDATION")
    print("-"*70)
    examples = [
        {"prompt": "Draft a clause", "completion": " Confidential information..."},
        {"prompt": "Write terms", "completion": " Terms include..."},
        {"prompt": "Legal document", "completion": " This agreement..."},
    ]
    validation = validate_dataset(examples, min_examples=3)
    print(f"Valid: {validation['is_valid']}")
    print(f"Examples: {validation['example_count']}")
    
    # Example 2: Estimate costs
    print("\n2. COST ESTIMATION")
    print("-"*70)
    costs = estimate_fine_tuning_cost(100, avg_tokens_per_example=200)
    print(f"Total tokens: {costs['total_tokens']:,}")
    for service, cost_info in costs['costs'].items():
        print(f"  {cost_info['service']}: {cost_info['breakdown']}")
    
    # Example 3: Compare services
    print("\n3. SERVICE COMPARISON")
    print("-"*70)
    comparison = compare_fine_tuning_services()
    for service, details in comparison.items():
        print(f"\n{service}:")
        print(f"  Cost: {details['cost']}")
        print(f"  Quality: {details['quality']}")
    
    # Example 4: Evaluate improvement
    print("\n4. IMPROVEMENT EVALUATION")
    print("-"*70)
    improvement = calculate_improvement(
        baseline_scores=[0.6, 0.65, 0.62],
        fine_tuned_scores=[0.92, 0.88, 0.90]
    )
    print(f"Average improvement: +{improvement['average_improvement']:.2f}")
    
    # Example 5: Cost-benefit analysis
    print("\n5. COST-BENEFIT ANALYSIS")
    print("-"*70)
    roi = evaluate_cost_benefit(
        fine_tuning_cost=5.00,
        improvement_percentage=25.0,
        daily_api_calls=1000
    )
    print(f"Payback period: {roi['payback_period_days']:.1f} days")
    print(f"Recommendation: {roi['recommendation']}")
    
    # Example 6: Pre-fine-tuning checklist
    print("\n6. PRE-FINE-TUNING CHECKLIST")
    print("-"*70)
    checklist = get_fine_tuning_checklist()
    for item in checklist:
        print(f"  {item}")
    
    print("\n" + "="*70)
    print("✅ Fine-tuning utilities ready to use in your projects!")
