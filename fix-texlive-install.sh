#!/bin/bash

# Fix TeX Live installation issues

echo "🔧 Fixing TeX Live installation..."

# Update package lists
sudo apt-get update

# Install TeX Live in smaller chunks
echo "📦 Installing TeX Live base packages..."
sudo apt-get install -y \
    texlive-base \
    texlive-latex-base \
    texlive-fonts-recommended

echo "📦 Installing TeX Live recommended packages..."
sudo apt-get install -y \
    texlive-latex-recommended \
    texlive-latex-extra

echo "📦 Installing TeX Live additional packages..."
sudo apt-get install -y \
    texlive-science \
    texlive-publishers \
    texlive-xetex \
    texlive-luatex

echo "📦 Installing fonts..."
sudo apt-get install -y \
    lmodern \
    fonts-liberation \
    fonts-liberation-sans \
    fonts-liberation-serif \
    fonts-liberation-mono

# Clean up
sudo apt-get clean
sudo apt-get autoremove -y

# Test TeX Live installation
echo "🧪 Testing TeX Live installation..."
if which pdflatex; then
    echo "✅ pdflatex found: $(which pdflatex)"
    pdflatex --version | head -1
else
    echo "❌ pdflatex not found"
fi

if which xelatex; then
    echo "✅ xelatex found: $(which xelatex)"
else
    echo "❌ xelatex not found"
fi

if which lualatex; then
    echo "✅ lualatex found: $(which lualatex)"
else
    echo "❌ lualatex not found"
fi

echo "✅ TeX Live installation completed!" 