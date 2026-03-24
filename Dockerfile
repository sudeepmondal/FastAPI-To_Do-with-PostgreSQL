# ============================================================
# Dockerfile - FastAPI To-Do API
# ============================================================

FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy and install dependencies first (for Docker cache efficiency)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code
COPY . .

# Expose port 8000
EXPOSE 8000

# Run the FastAPI app using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]