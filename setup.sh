#!/bin/bash

# Setup script for LLM Analysis Quiz project

echo "Setting up LLM Analysis Quiz project..."

# Create virtual environment
echo "\n1. Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "\n2. Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "\n3. Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "\n4. Installing requirements..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "\n5. Creating .env file..."
    cp .env.example .env
    echo "Please edit .env file with your credentials"
else
    echo "\n5. .env file already exists"
fi

# Create necessary directories
echo "\n6. Creating necessary directories..."
mkdir -p downloads temp

echo "\n✓ Setup complete!"
echo "\nNext steps:"
echo "1. Edit .env file with your credentials"
echo "2. Run 'source venv/bin/activate' to activate the virtual environment"
echo "3. Run 'python app.py' to start the server"
echo "4. Run 'python test_endpoint.py' to test your endpoint"