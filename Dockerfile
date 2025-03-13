FROM python:3.9

# Install system dependencies (fix OpenCV error)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*  # Cleanup to reduce image size


# Copy files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set working directory
WORKDIR /app
# Run the script when the container starts
# CMD ["python", "main.py"]
