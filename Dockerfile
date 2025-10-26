# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install runtime and testing dependencies
RUN pip install --upgrade pip \
    && pip install chatgpt-apps-sdk openai pytest

# Copy application source
COPY app ./app
COPY tests ./tests
COPY README.md ./README.md

EXPOSE 8000

# Default command starts the ChatGPT Apps dev server.
CMD ["chatgpt-apps", "dev", "--host", "0.0.0.0", "--port", "8000"]
