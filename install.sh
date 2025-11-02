#!/bin/bash
# Installation script for Orunmila AI Agent

set -e

echo "================================================"
echo "  Orunmila AI Agent - Installation Script"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.11.0"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "❌ Error: Python 3.11+ is required. Found version $python_version"
    exit 1
fi
echo "✅ Python version $python_version is compatible"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✅ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -e . > /dev/null 2>&1
echo "✅ Dependencies installed"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your OPENAI_API_KEY"
    echo ""
else
    echo "✅ .env file exists"
    echo ""
fi

# Check if OpenAI API key is set
if grep -q "OPENAI_API_KEY=$" .env || grep -q "OPENAI_API_KEY=your_openai_api_key_here" .env; then
    echo "⚠️  WARNING: OPENAI_API_KEY is not set in .env"
    echo "   Please edit .env and add your OpenAI API key"
    echo "   Get one at: https://platform.openai.com/api-keys"
    echo ""
    
    read -p "Do you want to set your OpenAI API key now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your OpenAI API key: " api_key
        sed -i "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$api_key/" .env
        echo "✅ API key set in .env"
    fi
    echo ""
fi

echo "================================================"
echo "  Installation Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Ensure your OpenAI API key is set in .env"
echo "3. Run verification: python test_setup.py"
echo "4. Start the server: python main.py"
echo "5. Visit http://localhost:8000/docs"
echo ""
echo "For more information, see:"
echo "- QUICKSTART.md for getting started"
echo "- README.md for full documentation"
echo "- API_EXAMPLES.md for API usage examples"
echo ""
echo "Ẹ káàbọ̀! (Welcome!)"
echo ""
