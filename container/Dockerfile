FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (only what's needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 🔧 Upgrade pip & setuptools early (fixes CVEs)
RUN pip install --no-cache-dir --upgrade pip setuptools

# Copy requirements and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# 🔒 Create a non-root user and switch
RUN useradd -m appuser
USER appuser

# Expose port
EXPOSE 8000

# Run app with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
