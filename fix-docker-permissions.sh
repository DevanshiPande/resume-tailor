#!/bin/bash

# Quick fix for Docker permission issues on EC2

echo "🔧 Fixing Docker permissions..."

# Add user to docker group
sudo usermod -aG docker $USER

# Restart Docker service
sudo systemctl restart docker
sudo systemctl enable docker

# Wait for Docker to start
sleep 3

# Test Docker access
if docker info &> /dev/null; then
    echo "✅ Docker is now accessible!"
    echo "💡 You may need to reconnect to SSH for changes to take effect:"
    echo "   exit"
    echo "   ssh -i your-key.pem ubuntu@your-ec2-ip"
else
    echo "⚠️ Docker still not accessible. Trying alternative methods..."
    
    # Method 1: Use sudo for Docker commands
    echo "🔄 Using sudo for Docker commands..."
    sudo docker info
    
    # Method 2: Start new shell session
    echo "🔄 Starting new shell session..."
    exec sg docker -c "$0 $*"
fi

echo "📋 If Docker still doesn't work, try these commands manually:"
echo "   sudo usermod -aG docker $USER"
echo "   sudo systemctl restart docker"
echo "   exit"
echo "   ssh -i your-key.pem ubuntu@your-ec2-ip"
echo "   docker info" 