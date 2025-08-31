# Use official Python slim image (Debian bookworm)
FROM python:3.10-slim

# Noninteractive apt
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1) System deps, with apt validity workarounds (prevents "Release file is not yet valid")
RUN apt-get update -o Acquire::Check-Valid-Until=false -o Acquire::Check-Date=false && \
    apt-get install -y --no-install-recommends \
      ca-certificates curl wget gnupg \
      # Playwright/Chromium runtime deps:
      libnss3 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxdamage1 libxext6 \
      libxfixes3 libxrandr2 libxrender1 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
      libdrm2 libgbm1 libasound2 libpangocairo-1.0-0 libpango-1.0-0 libcairo2 \
      libgtk-3-0 fonts-liberation libu2f-udev libvulkan1 \
    && rm -rf /var/lib/apt/lists/*

# 2) Install Python deps first (leverage Docker layer caching)
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 3) Install Playwright browsers (Chromium is the one TikTokApi needs)
#    --with-deps pulls any additional missing libs if needed
RUN playwright install --with-deps chromium

# 4) Copy backend code
COPY backend/ ./backend/

# 5) Helpful envs
ENV PYTHONPATH=/app \
    # Playwright runs as root in containers; no-sandbox reduces random crashes
    PLAYWRIGHT_BROWSERS_PATH=/root/.cache/ms-playwright \
    UVICORN_HOST=0.0.0.0 \
    UVICORN_PORT=8000

EXPOSE 8000

# 6) Start API
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]