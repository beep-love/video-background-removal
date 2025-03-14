FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

RUN apt-get update && apt-get install -y python3 python3-pip

# Install system dependencies (fix OpenCV error)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*  # Cleanup to reduce image size

RUN pip3 install --no-cache-dir \
    opencv-python \
    numpy \
    torch \
    torchvision \
    rembg \
    pillow \
    onnx \
    onnxruntime-gpu \
    insightface
# Set working directory
WORKDIR /app
# Run the script when the container starts
# CMD ["python", "main.py"]
