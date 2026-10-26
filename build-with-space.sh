#!/bin/bash

# Docker build script with space management

echo "🐳 Building Resume Tailor with space optimization..."

# Clean up Docker system first
echo "🧹 Cleaning Docker system..."
docker system prune -f
docker builder prune -f

# Check available space
echo "💾 Checking available space..."
df -h

# Build with space optimization
echo "🔨 Building with space optimization..."

# Create a temporary Dockerfile with space optimization
cat > Dockerfile.temp << 'EOF'
# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install TeX Live in stages to manage space
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    texlive-base \
    texlive-latex-base \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    texlive-latex-recommended \
    texlive-fonts-recommended \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    texlive-latex-extra \
    texlive-science \
    texlive-publishers \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    texlive-xetex \
    texlive-luatex \
    lmodern \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Run the application
CMD ["python", "app.py"]
EOF

# Build with the temporary Dockerfile
if docker build -f Dockerfile.temp -t resume-tailor:latest .; then
    echo "✅ Build successful with space optimization!"
    rm Dockerfile.temp
    exit 0
else
    echo "❌ Build failed with space optimization"
    rm Dockerfile.temp
    
    echo "🔄 Trying alternative approach with minimal TeX Live..."
    
    # Create minimal Dockerfile
    cat > Dockerfile.minimal << 'EOF'
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Install minimal TeX Live
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    texlive-base \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-latex-recommended \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000
CMD ["python", "app.py"]
EOF

    if docker build -f Dockerfile.minimal -t resume-tailor:minimal .; then
        echo "✅ Minimal build successful!"
        rm Dockerfile.minimal
        exit 0
    else
        echo "❌ All build attempts failed"
        rm Dockerfile.minimal
        echo "💡 Try these solutions:"
        echo "   1. Increase Docker disk space: docker system prune -a"
        echo "   2. Build on host with texlive-full installed"
        echo "   3. Use a larger EC2 instance (t3.small instead of t2.micro)"
        exit 1
    fi
fi 