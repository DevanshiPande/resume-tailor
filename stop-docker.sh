#!/bin/bash

# Stop Docker container and clean up

echo "🛑 Stopping Docker container..."

# Stop and remove the container
docker-compose down

# Also stop any standalone containers
docker stop $(docker ps -q --filter "ancestor=resume-tailor") 2>/dev/null || true
docker rm $(docker ps -aq --filter "ancestor=resume-tailor") 2>/dev/null || true

# Remove the image
docker rmi resume-tailor:latest 2>/dev/null || true

# Clean up Docker system
echo "🧹 Cleaning up Docker resources..."
docker system prune -f

echo "✅ Docker container stopped and cleaned up!"
echo "📊 Current Docker status:"
docker ps -a

echo "🔍 Checking if port 5000 is free:"
if netstat -tuln | grep :5000; then
    echo "⚠️ Port 5000 is still in use. You may need to:"
    echo "   - Wait a moment for Docker to fully stop"
    echo "   - Or manually kill the process: sudo lsof -ti:5000 | xargs sudo kill -9"
else
    echo "✅ Port 5000 is free!"
fi 