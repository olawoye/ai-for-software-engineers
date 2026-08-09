"""
Lesson 3.5: DevOps for AI Apps — TODO Scaffold

Learn deployment strategies, environment management, and operational concerns.
Understand how to move AI apps from development to production safely and reliably.

BUSINESS SCENARIO:
AI applications need more than great code—they need reliable deployment, monitoring,
and operational support. This lesson teaches practical DevOps patterns for AI systems.

Run: python lesson-05-devops-for-ai-apps.py
Requires: export OPENROUTER_API_KEY='your-key-here'
"""

import os
import sys

# ============================================================================
# STAGE 1: Helper Functions & Output Formatting
# ============================================================================
# Build terminal utilities for formatted output and section headers.
# Available utilities: os.system(), print formatting, color/emoji helpers
# TODO: Add your Stage 1 implementation here


# ============================================================================
# STAGE 2: Pre-Deployment Checklist
# ============================================================================
# Implement validation checks for API keys, dependencies, and connectivity.
# Available utilities: os.getenv(), __import__() for package checking, requests
# TODO: Add your Stage 2 implementation here


# ============================================================================
# STAGE 3: Environment Setup & Templates
# ============================================================================
# Build .env templates and Docker configuration files.
# Available utilities: string templates, docstring examples
# TODO: Add your Stage 3 implementation here


# ============================================================================
# STAGE 4: Deployment Platform Comparison
# ============================================================================
# Document deployment platforms with pros/cons and cost analysis.
# Available utilities: dict structures for platform metadata, print formatting
# TODO: Add your Stage 4 implementation here
#   * "railway" → 5 steps + time + cost
#   * "do-app" → 4 steps + time + cost
#   * "do-droplet" → 6 steps + time + cost
#   * "gcp" → 5 steps + time + cost
# - Print instructions for selected platform


# TODO PHASE 3: Implement show_production_patterns()
# Logic:
# - Print section header
# - Display categories:
#   * ERROR HANDLING (try/except, retries, graceful messages)
#   * MONITORING (health checks, error rates, metrics, cost)
#   * SECURITY (no secrets in git, validate input, rate limit)
#   * PERFORMANCE (cache, timeouts, token usage, load test)
#   * LOGGING (structured logs, persistence, alerts)


# ============================================================================
# MAIN FLOW - MENU DRIVEN (with Q to exit)
# ============================================================================

# TODO PHASE 1-3: Implement show_menu()
# Display: Menu header with 6 selectable phases + [R]un all + [Q]uit
# Reference: See completed version for menu layout
# Return: Nothing (just prints)

# TODO PHASE 1-3: Implement main()
# Flow:
# 1. Loop forever (until user selects Q)
# 2. show_menu() displays all options
# 3. Get user input: [1-6] for specific phase, [R] for full walkthrough, [Q] to quit
# 4. If Q: print goodbye message and break loop
# 5. If R: run all phases sequentially (old main() flow)
# 6. If 1-6: run selected phase only
# 7. After each choice: input("[ENTER] to return to menu...")
# 8. Loop back to show_menu()

# >>> REFERENCE: See completed version for full menu implementation
# - Uses show_menu() function with loop
# - Each phase can run independently
# - [R]un all runs complete flow
# - [Q]uit exits gracefully (no Ctrl+C needed)

# TODO PHASE 1-3: Add try/except for KeyboardInterrupt
# Print: "\n\n⚠️  Interrupted. Bye!"
# Also catch general Exception: print error and exit with code 1
# Exit with sys.exit(0) or sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted. Bye!")
        sys.exit(0)
