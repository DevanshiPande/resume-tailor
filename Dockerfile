# Use Python 3.11 base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including TeX Live
RUN apt-get update && apt-get install -y \
    texlive-full \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create temp directory
RUN mkdir -p temp

# Expose port
EXPOSE 5000

# Set environment variables
ENV PYTHONPATH=/app
ENV TEMP_DIR=/app/temp

# Run the application
CMD ["python", "app.py"] 