# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install basic system dependencies (optional, remove if not needed)
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libasound2 \
    libglib2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Copy only backend requirements
COPY backend/requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only backend code
COPY backend/ ./backend/

# Expose port
EXPOSE 8000

# Run backend app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
