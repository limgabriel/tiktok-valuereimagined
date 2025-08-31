# Use official Python slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Playwright
RUN apt-get update && \
    apt-get install -y curl wget gnupg unzip libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
                       libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libpango-1.0-0 \
                       libgtk-3-0 libxshmfence1 libgl1 libgles2 && \
    rm -rf /var/lib/apt/lists/*


# Install Python dependencies
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy only backend code
COPY backend/ ./backend/

# Install Playwright browsers
RUN pip install --no-cache-dir playwright && \
    playwright install --with-deps chromium

# Copy only backend code
COPY backend/ ./backend/

# Set environment variable for module path (optional but helps imports)
ENV PYTHONPATH=/app

# Expose backend port
EXPOSE 8000

# Start the backend
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
