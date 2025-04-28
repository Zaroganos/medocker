FROM python:3.11-slim

WORKDIR /app

# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=9876 \
    HOST=0.0.0.0 \
    FLASK_ENV=production

# Install Poetry
RUN pip install --no-cache-dir poetry==1.5.1

# Copy the entire project for a more reliable build
COPY . /app/

# Configure poetry to not use virtualenv
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --only main --no-interaction --no-ansi

# Create a simple Flask application script that doesn't rely on complex imports
RUN echo "import os\n\
import sys\n\
\n\
# Add app directory to the Python path\n\
sys.path.insert(0, '/app')\n\
\n\
# Print available modules for debugging\n\
print('Current directory:', os.getcwd())\n\
print('Directory contents:', os.listdir('.'))\n\
print('src directory contents:', os.listdir('./src'))\n\
print('Python path:', sys.path)\n\
\n\
try:\n\
    from src.web import app\n\
    print('Successfully imported app')\n\
except ImportError as e:\n\
    print(f'ImportError: {e}')\n\
    print(f'Error details: {str(e)}')\n\
    sys.exit(1)\n\
\n\
# Get port from environment variable\n\
port = int(os.environ.get('PORT', 9876))\n\
host = os.environ.get('HOST', '0.0.0.0')\n\
\n\
print(f'Starting Medocker on {host}:{port}')\n\
\n\
if __name__ == '__main__':\n\
    from waitress import serve\n\
    serve(app, host=host, port=port, threads=20)\n\
" > /app/start_app.py

# Create necessary directories
RUN mkdir -p /app/config /app/templates /app/static /app/playbooks

# Expose port
EXPOSE 9876

# Run the application with the simple script
CMD ["python", "/app/start_app.py"] 