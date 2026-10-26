#!/bin/bash

# Resume Tailor Deployment Script for AWS EC2
# This script sets up the application on an EC2 instance

set -e

echo "🚀 Starting Resume Tailor deployment..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo "Docker installed successfully"
else
    echo "Docker already installed"
fi

# Ensure user is in docker group and restart Docker service
echo "🔧 Configuring Docker permissions..."
sudo usermod -aG docker $USER
sudo systemctl restart docker
sudo systemctl enable docker

# Wait a moment for Docker to start
sleep 5

# Verify Docker is working
if ! docker info &> /dev/null; then
    echo "⚠️ Docker not accessible. Trying alternative approach..."
    # Start a new shell session to pick up group changes
    exec sg docker -c "$0 $*"
fi

# Install Docker Compose
echo "📦 Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "Docker Compose installed successfully"
else
    echo "Docker Compose already installed"
fi

# Create application directory
echo "📁 Setting up application directory..."
sudo mkdir -p /opt/resume-tailor
sudo chown $USER:$USER /opt/resume-tailor

# Copy application files (assuming you're running this from the project directory)
echo "📋 Copying application files..."
cp -r . /opt/resume-tailor/
cd /opt/resume-tailor

# Create environment file
echo "🔧 Creating environment file..."
cat > .env << EOF
FLASK_ENV=production
SECRET_KEY=$(openssl rand -hex 32)
OPENROUTER_API_KEY=your_openrouter_key_here
CEREBRAS_API_KEY=your_cerebras_key_here
GEMINI_API_KEY=your_gemini_key_here
EOF

# Build and start the application
echo "🔨 Building Docker image..."
chmod +x build-docker.sh
./build-docker.sh

if [ $? -eq 0 ]; then
    echo "✅ Docker build successful"
else
    echo "❌ Docker build failed. Trying alternative approach..."
    # Try building with more memory and no cache
    docker build --memory=4g --no-cache -t resume-tailor:latest .
fi

echo "🚀 Starting the application..."
docker-compose up -d

# Wait for application to start
echo "⏳ Waiting for application to start..."
sleep 30

# Check if application is running
if curl -f http://localhost:5000/ > /dev/null 2>&1; then
    echo "✅ Application deployed successfully!"
    echo "🌐 Access your application at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):5000"
else
    echo "❌ Application failed to start. Check logs with: docker-compose logs"
    exit 1
fi

echo "📋 Useful commands:"
echo "  View logs: docker-compose logs -f"
echo "  Stop app: docker-compose down"
echo "  Restart app: docker-compose restart"
echo "  Update app: git pull && docker-compose up -d --build"
echo "  Cleanup storage: ./cleanup.sh"

# Set up automated cleanup (weekly)
echo "🔄 Setting up automated cleanup..."
chmod +x cleanup.sh
(crontab -l 2>/dev/null; echo "0 2 * * 0 /opt/resume-tailor/cleanup.sh") | crontab - 