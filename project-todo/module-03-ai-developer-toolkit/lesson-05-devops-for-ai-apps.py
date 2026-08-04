"""
Lesson 3.5: DevOps for AI Apps — TODO Scaffold

Learn deployment strategies, environment management, and operational concerns.

PHASE 1: Pre-deployment validation (checklist)
PHASE 2: Environment variable management (templates)
PHASE 3: Docker templates & deployment platform comparison

Run: python lesson-05-devops-for-ai-apps.py
Requires: export OPENROUTER_API_KEY='your-key-here'

Reference: project-completed/module-03-ai-developer-toolkit/lesson-05-devops-for-ai-apps.py
"""

import os
import sys


# TODO PHASE 1: Helper functions for output formatting
# def clear_screen():
#     """Clear terminal screen."""
#     os.system("clear" if os.name == "posix" else "cls")
#
# def print_section(title: str):
#     """Print formatted section header."""
#     print(f"\n{'=' * 70}")
#     print(f"{title.center(70)}")
#     print(f"{'=' * 70}\n")
#
# def print_success(msg: str):
#     """Print success message (with ✅)."""
#
# def print_warning(msg: str):
#     """Print warning message (with ⚠️)."""


# ============================================================================
# PHASE 1: PRE-DEPLOYMENT CHECKLIST
# ============================================================================

# TODO PHASE 1: Implement check_api_key()
# Docstring:
# """Check if OPENROUTER_API_KEY environment variable is set."""
# Logic:
# - Get OPENROUTER_API_KEY from os.getenv()
# - If exists: print_success() and return True
# - If missing: print_warning() with setup instructions, return False

# TODO PHASE 1: Implement check_dependencies()
# Docstring:
# """Check if required packages (streamlit, requests) are installed."""
# Logic:
# - Try __import__("streamlit"), __import__("requests")
# - For each: print_success() if found, print_warning() if missing
# - Return True if all found, False otherwise

# TODO PHASE 1: Implement check_network()
# Docstring:
# """Test connectivity to API endpoint."""
# Logic:
# - Import requests
# - Try requests.get("https://openrouter.ai", timeout=5)
# - Return True if successful, False with error message if not

# TODO PHASE 1: Implement run_pre_deployment_checklist()
# Docstring:
# """Run all checks and report results."""
# Logic:
# - Print section header
# - Call each check function
# - Count passed/total
# - Return True if all passed, False otherwise


# ============================================================================
# PHASE 2: ENVIRONMENT SETUP
# ============================================================================

# TODO PHASE 2: Implement show_environment_setup()
# Return: .env.example template string
# Logic:
# - Print section header
# - Explain why env vars matter (secrets, config, feature flags)
# - Print .env.example content showing:
#   * OPENROUTER_API_KEY
#   * APP_MODEL
#   * APP_TEMPERATURE
#   * APP_MAX_TOKENS
#   * DEBUG
#   * LOG_LEVEL
# - Print production notes for each platform
# - Return env_example string


# TODO PHASE 2: Implement show_docker_templates()
# Return: (dockerfile_string, docker_compose_string)
# Logic:
# - Print section header
# - Print Dockerfile with comments explaining:
#   * Multi-stage build (why smaller is better)
#   * Python base image
#   * Copy requirements and install
#   * Expose port
#   * Health check
#   * Run command (Streamlit)
# - Print docker-compose.yml with comments explaining:
#   * Service definition
#   * Port mapping
#   * Environment variables (from .env)
#   * Volumes for development
# - Print usage examples
# - Return both templates


# ============================================================================
# PHASE 3: DEPLOYMENT PLATFORMS
# ============================================================================

# TODO PHASE 3: Implement show_deployment_comparison()
# Logic:
# - Print section header
# - Create platforms dict with keys:
#   * name, cost, ease, control, best_for, pros, cons, url
# - Print quick comparison table
# - Print detailed breakdown for each platform
# - Include all 7 platforms:
#   * Streamlit Cloud ($0, 1-click, managed)
#   * Railway.app ($5+, simple PaaS, Docker)
#   * Digital Ocean App Platform ($12+, PaaS, Docker)
#   * Digital Ocean Droplets ($4-6, full VM control)
#   * GCP Cloud Run ($0-5, serverless, scales to 0)
#   * AWS Lambda/EC2 ($0-50+, complex, most powerful)
#   * Vercel ($0-20, NOT ideal for Streamlit)


# TODO PHASE 3: Implement select_deployment_platform()
# Return: platform key string (default "railway")
# Logic:
# - Print section header
# - Show recommendation questions and answers
# - Print "FOR LEARNING", "FOR PRODUCTION", "FOR BUDGET", "FOR SCALE" recommendations
# - Return selected platform (or default to railway)


# TODO PHASE 3: Implement generate_deployment_instructions(platform: str)
# Logic:
# - Print section header with platform name
# - Create instructions dict with keys:
#   * "streamlit" → 4 steps + time + cost
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
