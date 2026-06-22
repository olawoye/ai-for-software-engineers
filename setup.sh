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

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "📥 Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
fi

if [ -f "requirements-module-02.txt" ]; then
    echo "📥 Installing Module 2 dependencies..."
    pip install -r requirements-module-02.txt
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Activate environment: source .venv/bin/activate"
echo "2. Run Lesson 2.2: streamlit run project-completed/module-02-ai-fundamentals/lesson-02-tokens-context-completion.py"
echo "3. Set API key: export OPENROUTER_API_KEY='your-key-here'"
echo ""
