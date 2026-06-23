"""
Lesson 3.5: DevOps for AI Apps

Learn deployment strategies, environment management, and operational concerns.
Move from "it works on my machine" to "it works in production."

Run: python lesson-05-devops-for-ai-apps.py
Requires: export OPENROUTER_API_KEY='your-key-here'
"""

import os
import sys
import time


def clear_screen():
    """Clear terminal screen."""
    os.system("clear" if os.name == "posix" else "cls")


def print_section(title: str):
    """Print formatted section header."""
    print(f"\n{'=' * 70}")
    print(f"{title.center(70)}")
    print(f"{'=' * 70}\n")


def print_success(msg: str):
    """Print success message."""
    print(f"✅ {msg}")


def print_warning(msg: str):
    """Print warning message."""
    print(f"⚠️  {msg}")


def print_info(msg: str):
    """Print info message."""
    print(f"ℹ️  {msg}")


def check_api_key():
    """
    VALIDATION 1: Check if API key is set.

    >>> REFERENCE: Why this matters
    Your app needs an API key to call LLMs. Forgetting to set it is the
    most common deployment failure. Catch this early.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        print_success(f"OPENROUTER_API_KEY is set ({len(api_key)} chars)")
        return True
    else:
        print_warning("OPENROUTER_API_KEY not set")
        print("\nSetup:")
        print("  export OPENROUTER_API_KEY='your-key-here'")
        return False


def check_dependencies():
    """
    VALIDATION 2: Check if key dependencies are installed.

    >>> REFERENCE: Why this matters
    If dependencies aren't installed, production will fail with "ModuleNotFoundError".
    Check early, fix locally, then deploy.
    """
    dependencies = {
        "streamlit": "streamlit",
        "requests": "requests",
    }

    all_found = True
    for name, import_name in dependencies.items():
        try:
            __import__(import_name)
            print_success(f"{name} is installed")
        except ImportError:
            print_warning(f"{name} is NOT installed")
            print(f"  Install: pip install {name}")
            all_found = False

    return all_found


def check_network():
    """
    VALIDATION 3: Check network connectivity to API.

    >>> REFERENCE: Why this matters
    Network issues (firewall, DNS, proxy) are common in cloud environments.
    Test connectivity before deploying.
    """
    try:
        import requests
        response = requests.get("https://api.openrouter.ai", timeout=5)
        print_success("Network connectivity to API verified")
        return True
    except Exception as e:
        print_warning(f"Network check failed: {e}")
        return False


def run_pre_deployment_checklist():
    """
    PHASE 1: Pre-deployment validation.

    Checks: API keys, dependencies, network connectivity.
    """
    print_section("PRE-DEPLOYMENT CHECKLIST")

    print("📋 Configuration Checks:\n")
    checks = {
        "API Key": check_api_key(),
        "Dependencies": check_dependencies(),
        "Network": check_network(),
    }

    print("\n" + "-" * 70)
    passed = sum(checks.values())
    total = len(checks)
    print(f"\n✓ Passed: {passed}/{total}")

    if passed == total:
        print_success("Ready to deploy!")
        return True
    else:
        print_warning("Fix issues above before deploying")
        return False


def show_environment_setup():
    """
    PHASE 2: Environment variable management.

    >>> REFERENCE: Why this matters
    Never commit secrets to git. Use .env files locally, environment
    variables in production. This pattern keeps credentials safe.
    """
    print_section("ENVIRONMENT VARIABLES")

    print("Production apps need environment variables for:")
    print("  • API keys and secrets")
    print("  • Configuration (model, temperature, etc.)")
    print("  • Feature flags (debug mode, rate limits)")
    print()

    # Generate .env.example
    env_example = """# >>> CONFIGURE: Copy to .env and fill in your values
# NEVER commit .env to git!

# API Configuration
OPENROUTER_API_KEY=your-key-here

# App Configuration
APP_MODEL=gpt-3.5-turbo
APP_TEMPERATURE=0.7
APP_MAX_TOKENS=500

# Deployment (for production)
DEBUG=false
LOG_LEVEL=info
"""

    print("📄 Recommended: Create .env.example (template for deployment):\n")
    print(env_example)

    print("-" * 70)
    print("\n✓ In production:")
    print("  • AWS/GCP/DO: Set environment variables in platform UI")
    print("  • Streamlit Cloud: Secrets tab in dashboard")
    print("  • Docker: Pass via --env flag or docker-compose")

    return env_example


def show_docker_templates():
    """
    PHASE 2: Docker containerization.

    >>> REFERENCE: Why this matters
    Docker ensures your app runs the same everywhere (laptop, CI/CD, production).
    It eliminates "works on my machine" problems.
    """
    print_section("DOCKER TEMPLATES")

    dockerfile = """# >>> REFERENCE: Multi-stage build (production best practice)
# Stage 1: Build
FROM python:3.11-slim as builder

WORKDIR /app

# >>> CONFIGURE: Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime (smaller image)
FROM python:3.11-slim

WORKDIR /app

# >>> REFERENCE: Copy only what's needed from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# >>> CUSTOMIZE: Copy your app
COPY . .

# >>> REFERENCE: Expose port for web apps
EXPOSE 8501

# >>> REFERENCE: Health check (production pattern)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
  CMD python -c "import requests; requests.get('http://localhost:8501')" || exit 1

# >>> CUSTOMIZE: Run command (Streamlit, FastAPI, etc.)
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""

    docker_compose = """# >>> REFERENCE: Local testing - runs your Docker image
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      # >>> CUSTOMIZE: Pass your environment variables
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - APP_MODEL=gpt-3.5-turbo
      - DEBUG=false
    volumes:
      # >>> REFERENCE: Volume for code changes (dev mode)
      - .:/app
    restart: unless-stopped
"""

    print("📦 Dockerfile (ensures consistent environment):\n")
    print(dockerfile)

    print("\n" + "-" * 70)
    print("\n🐳 docker-compose.yml (local testing):\n")
    print(docker_compose)

    print("-" * 70)
    print("\n✓ Usage:")
    print("  docker build -t my-ai-app .")
    print("  docker run -e OPENROUTER_API_KEY='...' -p 8501:8501 my-ai-app")
    print("\nOr with compose:")
    print("  docker-compose up")

    return dockerfile, docker_compose


def show_deployment_comparison():
    """
    PHASE 3: Compare deployment platforms.

    >>> REFERENCE: Why this matters
    Different platforms have different tradeoffs:
    - Cost: $0 → $5 → $50/month
    - Control: Managed ← → Full VM
    - Complexity: Trivial ← → DevOps required
    - Scaling: Automatic ← → Manual
    """
    print_section("DEPLOYMENT OPTIONS")

    platforms = {
        "streamlit": {
            "name": "Streamlit Cloud",
            "cost": "$0 (free tier)",
            "ease": "⭐⭐⭐⭐⭐ (1-click GitHub)",
            "control": "None (managed)",
            "best_for": "Streamlit apps, minimal DevOps",
            "pros": ["Free tier", "1-click deploy", "GitHub integration", "Custom domains"],
            "cons": ["Limited to Streamlit", "No background jobs", "Cold starts"],
            "url": "https://streamlit.io/cloud",
        },
        "railway": {
            "name": "Railway.app",
            "cost": "$5-20/month",
            "ease": "⭐⭐⭐⭐ (simple PaaS)",
            "control": "Container (Docker)",
            "best_for": "Any containerized app, fast deployment",
            "pros": ["GitHub integration", "Docker support", "Simple UI", "Affordable"],
            "cons": ["Smaller ecosystem", "Less enterprise features"],
            "url": "https://railway.app",
        },
        "do-app": {
            "name": "Digital Ocean App Platform",
            "cost": "$12+/month",
            "ease": "⭐⭐⭐⭐ (PaaS)",
            "control": "Container (Docker)",
            "best_for": "Reliable container apps, transparent pricing",
            "pros": ["GitHub integration", "Docker support", "Predictable costs", "Good docs"],
            "cons": ["Higher minimum than Railway", "Less free tier"],
            "url": "https://www.digitalocean.com/products/app-platform",
        },
        "do-droplet": {
            "name": "Digital Ocean Droplets",
            "cost": "$4-6/month (budget friendly)",
            "ease": "⭐⭐ (full VM control)",
            "control": "Full control",
            "best_for": "Budget setups, custom requirements",
            "pros": ["Very affordable", "Full control", "Simple VPS", "Good docs"],
            "cons": ["Manual setup", "You manage scaling", "No auto-restart"],
            "url": "https://www.digitalocean.com/products/droplets",
        },
        "gcp": {
            "name": "GCP Cloud Run",
            "cost": "$0-5/month (scales to 0)",
            "ease": "⭐⭐⭐ (container + serverless)",
            "control": "Container (Docker)",
            "best_for": "Variable load, cost-efficient",
            "pros": ["Scales to 0", "Pay-per-request", "Docker support", "Good free tier"],
            "cons": ["Steeper learning curve", "Cold starts for free tier"],
            "url": "https://cloud.google.com/run",
        },
        "aws": {
            "name": "AWS Lambda/EC2",
            "cost": "$0-50+/month",
            "ease": "⭐ (complex)",
            "control": "High",
            "best_for": "Enterprise, complex infrastructure",
            "pros": ["Most flexible", "Most powerful", "Huge ecosystem"],
            "cons": ["Steep learning curve", "Pricing complexity", "Overkill for simple apps"],
            "url": "https://aws.amazon.com",
        },
        "vercel": {
            "name": "Vercel",
            "cost": "$0-20/month",
            "ease": "⭐⭐⭐⭐ (super simple)",
            "control": "Limited",
            "best_for": "Next.js apps, frontend-heavy",
            "pros": ["Extremely simple", "Great free tier", "Next.js optimized"],
            "cons": ["NOT ideal for Streamlit", "Limited backend options"],
            "url": "https://vercel.com",
        },
    }

    print("💰 QUICK COMPARISON:\n")
    print(f"{'Platform':<20} {'Cost':<15} {'Ease':<20} {'Best For':<25}")
    print("-" * 80)

    for key, info in platforms.items():
        print(f"{info['name']:<20} {info['cost']:<15} {info['ease']:<20} {info['best_for']:<25}")

    print("\n" + "=" * 70)
    print("DETAILED BREAKDOWN:\n")

    for key, info in platforms.items():
        print(f"\n{info['name'].upper()}")
        print(f"Cost: {info['cost']}")
        print(f"Ease: {info['ease']}")
        print(f"Control: {info['control']}")
        print(f"Pros: {', '.join(info['pros'])}")
        print(f"Cons: {', '.join(info['cons'])}")
        print(f"Learn more: {info['url']}")

    print("\n" + "=" * 70)


def select_deployment_platform():
    """
    PHASE 3: Interactive platform selection.

    >>> REFERENCE: Why this matters
    Different projects need different platforms. Help students choose
    based on their constraints and priorities.
    """
    print_section("PLATFORM SELECTION")

    print("Based on your priorities, here's what we recommend:\n")

    print("🎯 RECOMMENDATION FOR THIS COURSE:\n")
    print("→ FOR LEARNING: Streamlit Cloud (free, 1-click, focus on code)")
    print("→ FOR PRODUCTION: Railway.app ($5/mo, simple, reliable)")
    print("→ FOR BUDGET: DO Droplets ($4-6/mo, full control)")
    print("→ FOR SCALE: GCP Cloud Run (pay-per-request, auto-scale)")

    print("\n" + "=" * 70)

    return "railway"


def generate_deployment_instructions(platform: str):
    """
    PHASE 3: Generate platform-specific deployment instructions.

    >>> REFERENCE: Why this matters
    Each platform has different steps. Automate the guidance so students
    don't get confused by differences.
    """
    print_section(f"DEPLOYMENT INSTRUCTIONS: {platform.upper()}")

    instructions = {
        "streamlit": """
STREAMLIT CLOUD (Recommended for learning)

1. Push code to GitHub:
   git add .
   git commit -m "Add Streamlit AI app"
   git push

2. Visit https://streamlit.io/cloud
   - Click "New app"
   - Select your GitHub repo
   - Select branch and main file
   - Click "Deploy"

3. Configure secrets:
   - Settings → Secrets
   - Add: OPENROUTER_API_KEY = your-key-here

4. Your app is live! Share the URL.

⏱️  Time: 2 minutes
💰 Cost: FREE
""",
        "railway": """
RAILWAY.APP (Recommended for production)

1. Create Dockerfile (use template from above)

2. Push to GitHub with Dockerfile

3. Visit https://railway.app
   - Click "New Project" → "Deploy from GitHub"
   - Select your repo
   - Railway auto-detects Dockerfile
   - Configure environment variables
   - Click "Deploy"

4. Add environment variables:
   - Project → Variables
   - Add: OPENROUTER_API_KEY = your-key-here
   - Add: APP_MODEL = gpt-3.5-turbo

5. Get public URL from "Deployments"

⏱️  Time: 5 minutes
💰 Cost: $5/month (scales with usage)
""",
        "do-app": """
DIGITAL OCEAN APP PLATFORM

1. Create Dockerfile

2. Push to GitHub with Dockerfile

3. Visit https://cloud.digitalocean.com/apps
   - Click "Create App"
   - Select GitHub repo
   - Configure app
   - Review & create

4. Set environment variables in UI

⏱️  Time: 10 minutes
💰 Cost: $12/month (predictable)
""",
        "do-droplet": """
DIGITAL OCEAN DROPLETS (Budget option)

1. Create Droplet ($4-6/month)
   - Ubuntu 22.04 LTS
   - Basic (cheapest) option

2. SSH into droplet:
   ssh root@your-droplet-ip

3. Install dependencies:
   apt update && apt upgrade -y
   apt install python3-pip docker.io -y

4. Clone your repo:
   git clone https://github.com/yourname/yourapp

5. Build and run Docker:
   docker build -t myapp .
   docker run -e OPENROUTER_API_KEY='...' -p 80:8501 myapp

6. Access via http://your-droplet-ip

⏱️  Time: 20 minutes (more hands-on)
💰 Cost: $4-6/month
""",
        "gcp": """
GCP CLOUD RUN

1. Create Dockerfile

2. Install gcloud CLI:
   curl https://sdk.cloud.google.com | bash

3. Authenticate:
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID

4. Build and deploy:
   gcloud run deploy myapp --source . --platform managed

5. Set environment variables when prompted

⏱️  Time: 10 minutes
💰 Cost: FREE (scales to 0) + $0.00002 per request
""",
    }

    print(instructions.get(platform, "Platform instructions not found"))


def show_production_patterns():
    """
    PHASE 3: Production best practices.

    >>> REFERENCE: Why this matters
    Deployed apps fail for predictable reasons. Document common issues
    and patterns to avoid them.
    """
    print_section("PRODUCTION PATTERNS")

    patterns = """
ERROR HANDLING
- ✅ Try/except around API calls
- ✅ Graceful error messages
- ✅ Automatic retries with backoff
- ✅ Log errors for debugging

MONITORING
- ✅ Health checks (is app alive?)
- ✅ Error rate tracking
- ✅ Response time metrics
- ✅ Cost monitoring (API spending)

SECURITY
- ✅ Never commit secrets (use env vars)
- ✅ Validate user input
- ✅ Rate limit to prevent abuse
- ✅ Use HTTPS (all platforms provide)

PERFORMANCE
- ✅ Cache when possible (API responses)
- ✅ Set reasonable timeouts
- ✅ Monitor token usage (costs $)
- ✅ Scale gradually, test load

LOGGING
- ✅ Log requests/responses (debug production issues)
- ✅ Use structured logging (JSON)
- ✅ Keep logs for 30 days minimum
- ✅ Alert on errors
"""

    print(patterns)


def main():
    """Main interactive flow."""
    clear_screen()
    print_section("LESSON 3.5: DEVOPS FOR AI APPS")

    print("""
This lesson teaches deployment strategies and operational concerns.
Move from "it works on my machine" to "it works in production."

We'll cover:
1. Pre-deployment validation (checklist)
2. Environment management (secrets)
3. Docker containerization (reproducibility)
4. Platform comparison (find the right fit)
5. Deployment instructions (step-by-step)
6. Production patterns (avoid common mistakes)
""")

    input("Press [ENTER] to start...")

    # PHASE 1: Pre-deployment checklist
    if not run_pre_deployment_checklist():
        input("\nFix issues above, then re-run this script.")
        return

    input("\n[ENTER] to continue to environment setup...")

    # PHASE 2: Environment management
    env_example = show_environment_setup()
    input("\n[ENTER] to continue to Docker templates...")

    # PHASE 2: Docker templates
    dockerfile, docker_compose = show_docker_templates()
    input("\n[ENTER] to compare deployment platforms...")

    # PHASE 3: Platform comparison
    show_deployment_comparison()
    input("\n[ENTER] to select your deployment platform...")

    # PHASE 3: Platform selection
    platform = select_deployment_platform()
    input(f"\n[ENTER] to see {platform.upper()} deployment instructions...")

    # PHASE 3: Deployment instructions
    generate_deployment_instructions(platform)
    input("\n[ENTER] to see production patterns...")

    # PHASE 3: Production patterns
    show_production_patterns()

    # PHASE 3: Summary
    print_section("NEXT STEPS")
    print("""
✅ Pre-deployment checklist passed
✅ Environment variables configured
✅ Docker templates generated
✅ Platform selected
✅ Deployment instructions ready

Now:
1. Create .env file (from template above)
2. Test locally: docker-compose up
3. Deploy to your chosen platform
4. Monitor for errors
5. Celebrate! 🎉

Remember: Production is just code + monitoring + logs.
Start simple, add complexity as needed.
""")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted. Bye!")
        sys.exit(0)
