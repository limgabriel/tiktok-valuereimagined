# Use official Python slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install basic system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy only backend code
COPY backend/ ./backend/

# Set environment variable for module path (optional but helps imports)
ENV PYTHONPATH=/app

# Expose backend port
EXPOSE 8000

# Start the backend
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
