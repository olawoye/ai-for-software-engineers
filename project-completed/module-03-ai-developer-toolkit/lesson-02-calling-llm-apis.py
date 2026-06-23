"""
Lesson 3.2: Calling LLM APIs - Learn by Doing

Interactive script teaching practical API integration patterns.
Students run real demonstrations, see live API responses, understand costs,
then copy patterns into their own projects.

Run: python lesson-02-calling-llm-apis.py
Requires: export OPENROUTER_API_KEY='your-key-here'
"""

import os
import sys
import time
from shared.llm_client import LLMClient
from shared.config import MODELS, DEFAULT_MODEL, TEMP_PRECISE, TEMP_BALANCED, TEMP_CREATIVE


def clear_screen():
    """Clear terminal screen."""
    os.system("clear" if os.name == "posix" else "cls")


def validate_api_key():
    """Check if API key is set. Exit if not."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("\n" + "=" * 60)
        print("❌ OPENROUTER_API_KEY not set")
        print("=" * 60)
        print("\nSetup required:")
        print("  export OPENROUTER_API_KEY='your-key-here'")
        print("\nGet free API key:")
        print("  https://openrouter.io (supports 100+ models)")
        print("\n" + "=" * 60)
        sys.exit(1)


def display_code(lines: list, title: str = ""):
    """Display code with line numbers."""
    if title:
        print(f"\n📝 {title}\n")
    for i, line in enumerate(lines, 1):
        print(f"  {i:2} | {line}")


def pattern_1_basic():
    """PATTERN 1: Basic Synchronous Call"""
    clear_screen()
    print("\n" + "=" * 70)
    print("PATTERN 1: Basic Synchronous Call")
    print("=" * 70)

    code_lines = [
        "from shared.llm_client import LLMClient",
        "",
        "# >>> CUSTOMIZE: Choose your model",
        "model = \"gpt-3.5-turbo\"",
        "",
        "# >>> CUSTOMIZE: Your prompt here",
        "prompt = \"What are Large Language Models?\"",
        "",
        "# >>> REFERENCE: Initialize client and call API",
        "client = LLMClient(model=model)",
        "response = client.complete(prompt, temperature=0.7, max_tokens=100)",
        "print(f\"Response: {response}\")",
    ]

    display_code(code_lines, "Code Pattern:")

    print("\n💡 What you'll learn:")
    print("  • How to initialize LLMClient")
    print("  • Making a simple completion request")
    print("  • Parsing the response")
    print("  • Measuring latency and token usage")

    print("\n" + "-" * 70)
    input("Press [ENTER] to run this pattern with real API...")

    try:
        # >>> CUSTOMIZE: Choose your model
        model = "gpt-3.5-turbo"

        # >>> CUSTOMIZE: Your prompt here
        prompt = "What are Large Language Models in one sentence?"

        # >>> REFERENCE: Initialize client and call API
        client = LLMClient(model=model)
        start = time.time()
        response = client.complete(prompt, temperature=0.7, max_tokens=100)
        elapsed = time.time() - start

        print("\n✓ Response received!\n")
        print(f"📝 Response:\n  \"{response[:100]}...\"")
        print(f"\n📊 Metrics:")
        print(f"  Latency: {elapsed:.2f}s")
        print(f"  Model: {model}")
        print(f"  Temperature: 0.7")

    except Exception as e:
        print(f"\n❌ Error: {e}")

    print("\n" + "-" * 70)
    print("✅ Pattern complete. Return to menu.")


def pattern_2_provider_switching():
    """PATTERN 2: Provider Switching"""
    clear_screen()
    print("\n" + "=" * 70)
    print("PATTERN 2: Provider Switching - Same Code, Different Models")
    print("=" * 70)

    code_lines = [
        "from shared.llm_client import LLMClient",
        "",
        "# >>> CUSTOMIZE: Model choices",
        "models = [\"gpt-3.5-turbo\", \"gpt-4\", \"claude-3-sonnet\"]",
        "",
        "prompt = \"Explain RAG in one sentence\"",
        "",
        "# >>> REFERENCE: Same code works with all models",
        "for model in models:",
        "    client = LLMClient(model=model)",
        "    response = client.complete(prompt, temperature=0.7, max_tokens=50)",
        "    print(f\"{model}: {response}\")",
    ]

    display_code(code_lines, "Code Pattern:")

    print("\n💡 What you'll learn:")
    print("  • How to switch between different providers")
    print("  • Same code works with GPT-3.5, GPT-4, Claude, etc.")
    print("  • Trade-offs: speed, cost, quality")
    print("  • How to choose the right model")

    print("\n" + "-" * 70)
    input("Press [ENTER] to run with multiple models...")

    try:
        # >>> CUSTOMIZE: Model choices
        models = ["gpt-3.5-turbo", "claude-3-sonnet"]

        prompt = "Explain Retrieval-Augmented Generation in one sentence"

        print("\n🔄 Running with multiple models...\n")

        # >>> REFERENCE: Same code works with all models
        for model in models:
            try:
                client = LLMClient(model=model)
                start = time.time()
                response = client.complete(prompt, temperature=0.7, max_tokens=50)
                elapsed = time.time() - start

                print(f"✓ {model} ({elapsed:.2f}s):")
                print(f"  \"{response[:70]}...\"")
                print()
            except Exception as e:
                print(f"✗ {model}: {e}\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")

    print("-" * 70)
    print("✅ Pattern complete. Return to menu.")


def pattern_3_temperature():
    """PATTERN 3: Temperature Effect"""
    clear_screen()
    print("\n" + "=" * 70)
    print("PATTERN 3: Temperature Effect - Precise vs Creative")
    print("=" * 70)

    code_lines = [
        "from shared.llm_client import LLMClient",
        "",
        "# >>> CUSTOMIZE: Temperature settings",
        "temps = [(0.3, 'Precise'), (0.7, 'Balanced'), (0.9, 'Creative')]",
        "",
        "prompt = \"Write a creative sentence about AI\"",
        "",
        "# >>> REFERENCE: Same prompt, different temperatures",
        "for temp, label in temps:",
        "    client = LLMClient(model=\"gpt-3.5-turbo\")",
        "    response = client.complete(prompt, temperature=temp, max_tokens=50)",
        "    print(f\"[{label}] {response}\")",
    ]

    display_code(code_lines, "Code Pattern:")

    print("\n💡 What you'll learn:")
    print("  • Temperature controls response variation")
    print("  • 0.0 = precise, deterministic")
    print("  • 0.5 = balanced")
    print("  • 1.0 = creative, random")
    print("  • Choose temperature based on your use case")

    print("\n" + "-" * 70)
    input("Press [ENTER] to see temperature in action...")

    try:
        # >>> CUSTOMIZE: Temperature settings
        temps = [(0.3, "Precise"), (0.7, "Balanced"), (0.9, "Creative")]

        prompt = "Complete this: The future of AI is..."

        print("\n🔄 Running with different temperatures...\n")

        # >>> REFERENCE: Same prompt, different temperatures
        for temp, label in temps:
            try:
                client = LLMClient(model="gpt-3.5-turbo")
                start = time.time()
                response = client.complete(prompt, temperature=temp, max_tokens=50)
                elapsed = time.time() - start

                print(f"[{label:12}] ({elapsed:.2f}s)")
                print(f"  \"{response[:65]}...\"")
                print()
            except Exception as e:
                print(f"[{label:12}] Error: {e}\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")

    print("-" * 70)
    print("✅ Pattern complete. Return to menu.")


def pattern_4_use_case():
    """PATTERN 4: Use Case - Text Classification"""
    clear_screen()
    print("\n" + "=" * 70)
    print("PATTERN 4: Real-World Use Case - Text Classification")
    print("=" * 70)

    code_lines = [
        "from shared.llm_client import LLMClient",
        "",
        "# >>> CUSTOMIZE: Classification prompt",
        "prompt_template = \"Classify this ticket: {ticket}\"",
        "",
        "tickets = [",
        "    \"The app crashes when I save\",",
        "    \"How do I reset my password?\",",
        "    \"Great product, love the features!\"",
        "]",
        "",
        "# >>> REFERENCE: Classify each ticket",
        "client = LLMClient(model=\"gpt-3.5-turbo\")",
        "for ticket in tickets:",
        "    prompt = prompt_template.format(ticket=ticket)",
        "    category = client.complete(prompt, temperature=0.3, max_tokens=20)",
        "    print(f\"{ticket} → {category}\")",
    ]

    display_code(code_lines, "Code Pattern:")

    print("\n💡 What you'll learn:")
    print("  • How to use LLMs for classification")
    print("  • Template-based prompts")
    print("  • Processing multiple items")
    print("  • Real production pattern")

    print("\n" + "-" * 70)
    input("Press [ENTER] to classify support tickets...")

    try:
        # >>> CUSTOMIZE: Classification prompt
        prompt_template = "Classify as: BUG, FEATURE_REQUEST, or SUPPORT\nTicket: {ticket}\nAnswer:"

        tickets = [
            "The app crashes when I save documents",
            "Can we add dark mode?",
            "How do I export my data?",
        ]

        print("\n🔄 Classifying tickets...\n")

        # >>> REFERENCE: Classify each ticket
        client = LLMClient(model="gpt-3.5-turbo")
        for ticket in tickets:
            try:
                prompt = prompt_template.format(ticket=ticket)
                category = client.complete(prompt, temperature=0.3, max_tokens=20)
                category_clean = category.strip().split("\n")[0]
                print(f"✓ \"{ticket[:40]}...\"")
                print(f"  → {category_clean}")
                print()
            except Exception as e:
                print(f"✗ \"{ticket[:40]}...\": {e}\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")

    print("-" * 70)
    print("✅ Pattern complete. Return to menu.")


def pattern_5_error_handling():
    """PATTERN 5: Error Handling"""
    clear_screen()
    print("\n" + "=" * 70)
    print("PATTERN 5: Error Handling - What Can Go Wrong")
    print("=" * 70)

    code_lines = [
        "from shared.llm_client import LLMClient",
        "",
        "# >>> CONFIGURE: Validate API key",
        "api_key = os.getenv('OPENROUTER_API_KEY')",
        "if not api_key:",
        "    print('Error: Missing API key')",
        "    return",
        "",
        "# >>> REFERENCE: Try/except for error handling",
        "try:",
        "    client = LLMClient(model='gpt-3.5-turbo')",
        "    response = client.complete('Hello')",
        "except ValueError as e:",
        "    print(f'Config error: {e}')",
        "except Exception as e:",
        "    print(f'API error: {e}')",
    ]

    display_code(code_lines, "Code Pattern:")

    print("\n💡 What you'll learn:")
    print("  • Checking for required configuration")
    print("  • Handling different error types")
    print("  • User-friendly error messages")
    print("  • Graceful degradation")

    print("\n" + "-" * 70)
    print("Demonstrating error scenarios...\n")

    # Scenario 1: API key validation
    print("✓ Scenario 1: API Key Check")
    print("  Status: PASS - OPENROUTER_API_KEY is set")
    print()

    # Scenario 2: Try a real call with error handling
    print("✓ Scenario 2: Graceful Error Handling")
    try:
        client = LLMClient(model="gpt-3.5-turbo")
        response = client.complete("Test", max_tokens=10)
        print("  Status: PASS - API call succeeded")
    except ValueError as e:
        print(f"  Config error caught: {e}")
    except Exception as e:
        print(f"  API error caught: {type(e).__name__}")
    print()

    # Scenario 3: Invalid model handling
    print("✓ Scenario 3: Invalid Model Handling")
    try:
        client = LLMClient(model="invalid-model-xyz")
        print("  Status: Would fail at API call")
    except Exception as e:
        print(f"  Error: {type(e).__name__}")
    print()

    print("-" * 70)
    print("✅ Pattern complete. Return to menu.")


def show_menu():
    """Display main menu."""
    clear_screen()
    print("\n" + "=" * 70)
    print("🚀 LESSON 3.2: CALLING LLM APIS - Learn by Doing".center(70))
    print("=" * 70)
    print()
    print("  Choose a pattern to learn:\n")
    print("    [1] DEMO: Basic Synchronous Call")
    print("        → Simple completion, response parsing, timing\n")
    print("    [2] DEMO: Provider Switching")
    print("        → Same code with different models (GPT, Claude, etc)\n")
    print("    [3] DEMO: Temperature Effect")
    print("        → Precise vs Creative - same prompt, different variation\n")
    print("    [4] USE CASE: Text Classification")
    print("        → Real-world pattern: classify support tickets\n")
    print("    [5] ERROR HANDLING: What Can Go Wrong")
    print("        → API keys, network errors, graceful degradation\n")
    print("    [Q] Quit\n")
    print("=" * 70)


def main():
    """Main interactive loop."""
    # Validate API key before starting
    validate_api_key()

    patterns = {
        "1": pattern_1_basic,
        "2": pattern_2_provider_switching,
        "3": pattern_3_temperature,
        "4": pattern_4_use_case,
        "5": pattern_5_error_handling,
    }

    while True:
        show_menu()
        choice = input("Choose [1-5] or [Q] to quit: ").strip().lower()

        if choice == "q":
            clear_screen()
            print("\n✅ Thanks for learning! Remember to:")
            print("   • Copy code patterns into your projects")
            print("   • Try different models and temperatures")
            print("   • Handle errors gracefully")
            print("\n")
            break

        if choice in patterns:
            try:
                patterns[choice]()
            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupted. Returning to menu.\n")
            except Exception as e:
                clear_screen()
                print(f"\n❌ Error: {e}\n")

            input("\nPress [ENTER] to return to menu...")
        else:
            print("❌ Invalid choice. Try again.")
            input("Press [ENTER]...")


if __name__ == "__main__":
    main()
