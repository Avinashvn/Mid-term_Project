# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY web_service.py .
COPY model_random_forest.bin .

# Expose the API port
EXPOSE 9696

# Run the Flask service
CMD ["python", "web_service.py"]
