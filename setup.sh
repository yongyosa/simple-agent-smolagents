#!/bin/bash

echo "🚀 Setting up Simple Agent with Calculator Tool"
echo "=============================================="

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "To activate the environment and run the agent:"
echo "  source venv/bin/activate"
echo "  python simple_agent.py"
