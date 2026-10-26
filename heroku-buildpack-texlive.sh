#!/bin/bash

# Install TeX Live on Heroku
echo "Installing TeX Live..."

# Add TeX Live repository
apt-get update
apt-get install -y texlive-full

# Verify installation
pdflatex --version

echo "TeX Live installation complete!" 