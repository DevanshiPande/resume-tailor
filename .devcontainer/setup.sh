#!/bin/bash

# Update package list
sudo apt-get update

# Install TeX Live (full installation for LaTeX compilation)
echo "Installing TeX Live..."
sudo apt-get install -y texlive-full

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create temp directory
mkdir -p temp

# Set up environment variables (you'll need to add your API keys)
echo "Setting up environment variables..."
if [ ! -f .env ]; then
    cat > .env << EOF
# Add your API keys here
OPENROUTER_API_KEY=your_openrouter_api_key_here
CEREBRAS_API_KEY=your_cerebras_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_secret_key_here
EOF
    echo "Created .env file - please add your API keys!"
fi

# Make the script executable
chmod +x .devcontainer/setup.sh

echo "Setup complete! You can now run: python app.py" 