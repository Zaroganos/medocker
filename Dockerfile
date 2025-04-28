FROM python:3.11-slim

WORKDIR /app

# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=9876 \
    HOST=0.0.0.0 \
    FLASK_ENV=production

# Install Poetry
RUN pip install --no-cache-dir poetry==1.5.1

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock* /app/

# Create a dummy src package to satisfy Poetry
RUN mkdir -p /app/src && \
    touch /app/src/__init__.py

# Configure poetry to not use virtualenv
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --only main --no-interaction --no-ansi

# Create necessary directories
RUN mkdir -p /app/config /app/templates /app/static /app/playbooks

# Now copy the real project files
COPY . /app/

# Expose port
EXPOSE 9876

# Run the application
CMD ["python", "-m", "src.run_web"] 