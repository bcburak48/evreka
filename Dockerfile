FROM python:3.9-slim

WORKDIR /app

# Install dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set the PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/app"


# Expose port 80
EXPOSE 80

# Default command (overridden by docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
