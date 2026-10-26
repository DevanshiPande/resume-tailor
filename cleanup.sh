#!/bin/bash

# Storage cleanup script for Resume Tailor EC2 instance

echo "🧹 Starting storage cleanup..."

# Clean Docker system
echo "🐳 Cleaning Docker..."
docker system prune -f
docker volume prune -f
docker image prune -f

# Clean temp files
echo "🗂️ Cleaning temp files..."
find /opt/resume-tailor/temp -name "*.pdf" -mtime +1 -delete
find /opt/resume-tailor/temp -name "*.tex" -mtime +1 -delete
find /opt/resume-tailor/temp -name "*.aux" -delete
find /opt/resume-tailor/temp -name "*.log" -delete

# Clean system logs
echo "📋 Cleaning system logs..."
sudo journalctl --vacuum-time=7d

# Clean apt cache
echo "📦 Cleaning apt cache..."
sudo apt-get clean
sudo apt-get autoremove -y

# Show disk usage
echo "💾 Current disk usage:"
df -h

echo "✅ Cleanup completed!" 