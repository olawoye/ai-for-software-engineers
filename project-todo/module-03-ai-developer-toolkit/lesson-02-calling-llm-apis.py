"""
Lesson 3.2: Calling LLM APIs — TODO Scaffold

Learn practical API integration patterns through interactive demonstrations.

PHASE 1: Menu structure and API key validation
PHASE 2: Implement 5 pattern demonstrations
PHASE 3: Error handling and user experience

Run: python lesson-02-calling-llm-apis.py
Requires: export OPENROUTER_API_KEY='your-key-here'
"""

import os
import sys
import time

# TODO PHASE 1: Import required modules
# from shared.llm_client import LLMClient
# from shared.config import ...


def clear_screen():
    """Clear terminal screen."""
    # TODO: Implement using os.system()
    pass


def validate_api_key():
    """
    PHASE 1: Check if API key is set.

    TODO:
    - Get OPENROUTER_API_KEY from environment
    - If missing, print error message with setup instructions
    - Exit if not found
    """
    pass


def display_code(lines: list, title: str = ""):
    """
    PHASE 2: Display code with line numbers for easy reference.

    TODO:
    - Print title
    - Loop through lines with enumerate (start=1)
    - Print formatted: "  {line_num:2} | {code_line}"
    """
    pass


def pattern_1_basic():
    """
    PHASE 2: Demonstrate basic synchronous API call.

    TODO:
    - Clear screen and show heading
    - Display code pattern with line numbers
    - Show learning objectives
    - Initialize LLMClient with "gpt-3.5-turbo"
    - Call complete() with a sample prompt
    - Measure timing with time.time()
    - Display response and metrics
    - Return to menu
    """
    pass


def pattern_2_provider_switching():
    """
    PHASE 2: Show how same code works with different models.

    TODO:
    - Clear screen and show heading
    - Display code pattern
    - Initialize with multiple models: ["gpt-3.5-turbo", "claude-3-sonnet"]
    - Loop through each model
    - Call complete() for each
    - Display response and timing
    - Show trade-offs between models
    """
    pass


def pattern_3_temperature():
    """
    PHASE 2: Demonstrate temperature effect on responses.

    TODO:
    - Clear screen and show heading
    - Display code pattern
    - Test same prompt with different temperatures: [0.3, 0.7, 0.9]
    - For each temperature:
      - Call complete(prompt, temperature=temp, max_tokens=50)
      - Display response labeled [Precise/Balanced/Creative]
      - Show difference in variation
    """
    pass


def pattern_4_use_case():
    """
    PHASE 2: Real-world use case - text classification.

    TODO:
    - Clear screen and show heading
    - Display code pattern
    - Create classification prompt template
    - Define sample tickets/texts to classify
    - For each ticket:
      - Format prompt
      - Call complete()
      - Extract and display category
    - Show production pattern
    """
    pass


def pattern_5_error_handling():
    """
    PHASE 3: Demonstrate error scenarios and handling.

    TODO:
    - Clear screen and show heading
    - Display code pattern
    - Show scenarios:
      1. API key validation check
      2. Try/except for API errors
      3. Invalid model handling
    - Use try/except blocks
    - Display status for each scenario
    """
    pass


def show_menu():
    """
    PHASE 1: Display interactive menu.

    TODO:
    - Clear screen
    - Print formatted menu with title
    - Show 5 patterns: [1-5]
    - Show quit option: [Q]
    - Print separator lines
    """
    pass


def main():
    """
    PHASE 1-3: Main interactive loop.

    TODO:
    - Call validate_api_key() at start
    - Infinite loop:
      - Show menu
      - Get user input
      - If 'q': exit gracefully with message
      - If '1-5': call corresponding pattern function
      - Handle errors and return to menu
      - Handle KeyboardInterrupt
    """
    pass


if __name__ == "__main__":
    main()
