FROM python:3.12-slim

# Set the working directory to the project root
WORKDIR /medocker

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

# Install uv
RUN pip install --no-cache-dir uv

# Copy the entire application first
COPY . /medocker/

# Install dependencies using uv and make them available system-wide
RUN uv sync --frozen --no-dev && \
    uv pip install --system pyyaml flask flask-wtf wtforms waitress paramiko ansible-runner jinja2 flask-session flask-cors

# Create a simple Flask application script that works with the new package structure
RUN echo "import os\n\
import sys\n\
\n\
# Add src directory to the Python path so we can import medocker package\n\
sys.path.insert(0, '/medocker/src')\n\
\n\
# Print available modules for debugging\n\
print('Current directory:', os.getcwd())\n\
print('Directory contents:', os.listdir('.'))\n\
print('src directory contents:', os.listdir('./src'))\n\
print('src/medocker directory contents:', os.listdir('./src/medocker'))\n\
print('Python path:', sys.path)\n\
\n\
try:\n\
    from medocker.web import app\n\
    print('Successfully imported app from medocker package')\n\
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
" > /medocker/start_app.py

# Expose port
EXPOSE 9876

# Run the application with the simple script
CMD ["python", "/medocker/start_app.py"] 