#!/bin/bash
# Setup script for AI For Software Engineers course
# One-time setup to create virtual environment and install dependencies

set -e

echo "🚀 Setting up AI For Software Engineers course environment..."

# Check Python availability
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $PYTHON_VERSION found"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created at .venv/"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install base dependencies and all modules (2-7)
if [ -f "requirements.txt" ]; then
    echo "📥 Installing base dependencies..."
    pip install -r requirements.txt
fi

# Install all module dependencies upfront (Modules 2-7)
for MODULE in 2 3 4 5 6 7; do
    if [ -f "requirements-module-${MODULE}.txt" ]; then
        echo "📥 Installing Module ${MODULE} dependencies..."
        pip install -r requirements-module-${MODULE}.txt
    fi
done

echo ""
echo "✨ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Activate environment: source .venv/bin/activate"
echo "2. Run Lesson 2.2: streamlit run project-completed/module-02-ai-fundamentals/lesson-02-tokens-context-completion.py"
echo "3. Set API key: export OPENROUTER_API_KEY='your-key-here'"
echo ""
echo "📌 Module 9 (Fine-Tuning):"
echo "   When ready, install heavy dependencies separately:"
echo "   pip install -r requirements-module-09.txt"
echo ""
