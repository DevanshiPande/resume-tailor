#!/bin/bash

# Docker build script with fallback options

echo "🐳 Building Resume Tailor Docker image..."

# Function to build with specific Dockerfile
build_with_dockerfile() {
    local dockerfile=$1
    local tag=$2
    
    echo "🔨 Building with $dockerfile..."
    if docker build -f $dockerfile -t resume-tailor:$tag .; then
        echo "✅ Build successful with $dockerfile"
        return 0
    else
        echo "❌ Build failed with $dockerfile"
        return 1
    fi
}

# Try main Dockerfile first
if build_with_dockerfile "Dockerfile" "latest"; then
    echo "🎉 Main build successful!"
    exit 0
fi

echo "⚠️ Main build failed, trying lightweight version..."

# Try lightweight Dockerfile
if build_with_dockerfile "Dockerfile.lightweight" "lightweight"; then
    echo "🎉 Lightweight build successful!"
    
    # Update docker-compose to use lightweight image
    sed -i 's/build: \./build:\n      dockerfile: Dockerfile.lightweight/' docker-compose.yml
    
    echo "📝 Updated docker-compose.yml to use lightweight image"
    exit 0
fi

echo "❌ All builds failed. Trying manual TeX Live installation..."

# Create minimal Dockerfile as last resort
cat > Dockerfile.minimal << 'EOF'
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Install only essential packages
RUN apt-get update && apt-get install -y \
    texlive-base \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-latex-recommended \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000
CMD ["python", "app.py"]
EOF

if build_with_dockerfile "Dockerfile.minimal" "minimal"; then
    echo "🎉 Minimal build successful!"
    echo "📝 Using minimal TeX Live installation"
    exit 0
fi

echo "❌ All build attempts failed."
echo "💡 Troubleshooting tips:"
echo "   1. Check internet connection"
echo "   2. Try building with more memory: docker build --memory=4g"
echo "   3. Try building with no cache: docker build --no-cache"
echo "   4. Check available disk space: df -h"
echo "   5. Try installing TeX Live manually on the host"

exit 1 