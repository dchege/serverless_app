# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /

# Copy test input for local testing
COPY test_input.json .

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY rp_handler.py .

# Expose the port RunPod will use
EXPOSE 8080

# Command to run the serverless handler
CMD ["python", "rp_handler.py"]
