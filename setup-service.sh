#!/bin/bash

# Setup Resume Tailor as a systemd service

echo "🚀 Setting up Resume Tailor as a systemd service..."

# Stop Docker container if running
echo "🛑 Stopping Docker container if running..."
docker-compose down 2>/dev/null || true
docker stop $(docker ps -q --filter "ancestor=resume-tailor") 2>/dev/null || true
docker rm $(docker ps -aq --filter "ancestor=resume-tailor") 2>/dev/null || true

# Wait a moment for port to be freed
sleep 3

# Check if port 5000 is free
if netstat -tuln | grep :5000; then
    echo "⚠️ Port 5000 is still in use. Killing process..."
    sudo lsof -ti:5000 | xargs sudo kill -9 2>/dev/null || true
    sleep 2
fi

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ app.py not found. Make sure you're in the resume-tailor directory."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Create temp directory
mkdir -p temp

# Copy service file to systemd
echo "🔧 Installing systemd service..."
sudo cp resume-tailor.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable the service
sudo systemctl enable resume-tailor

# Start the service
sudo systemctl start resume-tailor

# Check status
echo "📊 Service status:"
sudo systemctl status resume-tailor --no-pager

echo "✅ Resume Tailor service installed and started!"
echo "📱 Access your application at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):5000"
echo ""
echo "📋 Useful commands:"
echo "  Check status: sudo systemctl status resume-tailor"
echo "  View logs: sudo journalctl -u resume-tailor -f"
echo "  Restart: sudo systemctl restart resume-tailor"
echo "  Stop: sudo systemctl stop resume-tailor" 