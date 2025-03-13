FROM python:3.9

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
COPY main.py .
COPY input .
COPY output .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the script when the container starts
CMD ["python", "main.py"]
