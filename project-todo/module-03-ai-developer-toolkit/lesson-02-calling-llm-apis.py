"""
Lesson 3.2: Calling LLM APIs — TODO Scaffold

Learn practical API integration patterns through interactive demonstrations.
Understand how to initialize clients, handle different models, and manage API responses.

BUSINESS SCENARIO:
Developers need practical knowledge of calling LLMs to build production AI systems.
This lesson teaches core patterns through interactive demonstrations.

Run: python lesson-02-calling-llm-apis.py
Requires: export OPENROUTER_API_KEY='your-key-here'
"""

import os
import sys
import time

# ============================================================================
# STAGE 1: Setup & Validation
# ============================================================================
# Initialize API connection and validate credentials.
# Available utilities: shared.llm_client (LLMClient), os module for env vars
# TODO: Add your Stage 1 implementation here


def clear_screen():
    """Clear terminal screen."""
    pass


def validate_api_key():
    """Check if API key is set."""
    pass


def display_code(lines: list, title: str = ""):
    """Display code with line numbers for easy reference."""
    pass


# ============================================================================
# STAGE 2: Pattern 1 - Basic API Call
# ============================================================================
# Implement basic synchronous API call demonstration.
# Available utilities: LLMClient.complete(), time module for measurements
# TODO: Add your Stage 2 implementation here

def pattern_1_basic():
    """Pattern 1: Basic synchronous API call."""
    pass


def pattern_2_provider_switching():
    """Pattern 2: Show how same code works with different models."""
    pass


# ============================================================================
# STAGE 3: Pattern 3-5 - Temperature, Use Cases, Error Handling
# ============================================================================
# Implement temperature effects, real-world classification, and error handling.
# Available utilities: temperature parameter, try/except blocks, prompt formatting
# TODO: Add your Stage 3 implementation here

def pattern_3_temperature():
    """Pattern 3: Demonstrate temperature effect on responses."""
    pass


def pattern_4_use_case():
    """Pattern 4: Real-world use case - text classification."""
    pass


def pattern_5_error_handling():
    """Pattern 5: Demonstrate error scenarios and handling."""
    pass


def show_menu():
    """Display interactive menu."""
    pass


# ============================================================================
# STAGE 4: Interactive Menu Loop
# ============================================================================
# Build interactive CLI for users to explore patterns.
# Available utilities: show_menu(), pattern functions, user input handling
# TODO: Add your Stage 4 implementation here

def main():
    """Main interactive loop."""
    pass


if __name__ == "__main__":
    main()
