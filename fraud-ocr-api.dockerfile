# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your FastAPI app and models
COPY . .

# Expose FastAPI's default port
EXPOSE 8000

# Run FastAPI using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]