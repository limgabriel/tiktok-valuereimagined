# Use official Python slim image (Debian bookworm)
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for Playwright
RUN apt-get update && \
    apt-get install -y curl wget gnupg unzip libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
                       libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libpango-1.0-0 \
                       libgtk-3-0 libxshmfence1 libgl1 libgles2 && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code including start.py
COPY backend/ ./backend/

# Install Playwright and Chromium
RUN pip install --no-cache-dir playwright && \
    playwright install --with-deps chromium

# Helpful envs
ENV PYTHONPATH=/app \
    PLAYWRIGHT_BROWSERS_PATH=/root/.cache/ms-playwright \
    UVICORN_HOST=0.0.0.0

# Expose port for local dev
EXPOSE 8000

# Start backend using the script inside backend/
CMD ["python", "backend/start.py"]
