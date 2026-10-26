#!/bin/bash

# Run Resume Tailor directly on host (no Docker)

echo "🚀 Running Resume Tailor on host system..."

# Check if TeX Live is installed
if ! command -v pdflatex &> /dev/null; then
    echo "❌ TeX Live not found. Installing..."
    sudo apt-get update
    sudo apt-get install -y texlive-full
else
    echo "✅ TeX Live found: $(which pdflatex)"
fi

# Check if Python dependencies are installed
if ! python3 -c "import flask" &> /dev/null; then
    echo "📦 Installing Python dependencies..."
    pip3 install -r requirements.txt
fi

# Create temp directory
mkdir -p temp

# Set environment variables
export FLASK_ENV=production
export FLASK_APP=app.py

# Run the application
echo "🌐 Starting Resume Tailor application..."
echo "📱 Access at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):5000"
echo "🛑 Press Ctrl+C to stop"

python3 app.py 