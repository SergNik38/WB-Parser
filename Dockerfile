FROM python:3.10-slim

WORKDIR /app

# Install system dependencies if needed (e.g. for build tools)
# RUN apt-get update && apt-get install -y gcc

# Copy requirements first for cache efficiency
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy logic
COPY . .

# Create export directory
RUN mkdir -p exports

# Expose port
EXPOSE 8000

# Run command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
