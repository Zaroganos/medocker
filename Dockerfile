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

# Create necessary directories first
RUN mkdir -p /app/src /app/config /app/templates /app/static /app/playbooks

# Create empty __init__.py file
RUN touch /app/src/__init__.py

# Create a simple README.md file
RUN echo "# Medocker" > /app/README.md

# Install Poetry
RUN pip install --no-cache-dir poetry==1.5.1

# Create a simplified pyproject.toml
RUN echo '[tool.poetry]\n\
name = "medocker"\n\
version = "0.1.0"\n\
description = "A comprehensive Docker packaging of all the software a medical practice needs"\n\
authors = ["Iliya Yaroshevskiy <iliya.yaroshevskiy@gmail.com>"]\n\
packages = [{include = "src"}]\n\
\n\
[tool.poetry.dependencies]\n\
python = ">=3.11,<3.14"\n\
PyYAML = "^6.0"\n\
flask = "^2.2.3"\n\
flask-wtf = "^1.1.1"\n\
wtforms = "^3.0.1"\n\
waitress = "^2.1.2"\n\
paramiko = "^3.3.1"\n\
ansible-runner = "^2.3.4"\n\
jinja2 = "^3.1.3"\n\
Flask-Session = "^0.5.0"\n\
flask-cors = "^4.0.0"\n\
\n\
[build-system]\n\
requires = ["poetry-core"]\n\
build-backend = "poetry.core.masonry.api"\n\
\n\
[tool.poetry.scripts]\n\
medocker = "src.medocker:main"\n\
medocker-config = "src.configure:main"\n\
medocker-web = "src.run_web:main"' > /app/pyproject.toml

# Configure poetry to not use virtualenv
RUN poetry config virtualenvs.create false

# Generate a fresh lock file and install dependencies
RUN poetry lock --no-update && poetry install --only main --no-interaction --no-ansi

# Now copy the rest of the application (except poetry.lock and pyproject.toml which we've already generated)
COPY . /app/

# Restore our custom pyproject.toml to avoid overwriting any customizations
RUN mv /app/pyproject.toml /app/pyproject.toml.docker
COPY pyproject.toml /app/

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

# Expose port
EXPOSE 9876

# Run the application with the simple script
CMD ["python", "/app/start_app.py"] 