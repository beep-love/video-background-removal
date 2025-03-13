import cv2
import numpy as np
import os
from rembg import remove
from PIL import Image

# Paths
INPUT_DIR = "input"
OUTPUT_DIR = "output"
OUTPUT_VIDEO = os.path.join(INPUT_DIR, "input.mp4")
OUTPUT_VIDEO = os.path.join(OUTPUT_DIR, "output.mp4")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load the video
cap = cv2.VideoCapture(INPUT_VIDEO)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define output video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4 format
out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, fps, (frame_width, frame_height))

# Process each frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to PIL image
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Remove background using rembg (FBA Matting)
    processed_img = remove(img)

    # Convert back to OpenCV format
    processed_frame = cv2.cvtColor(np.array(processed_img), cv2.COLOR_RGB2BGR)

    # Write the processed frame
    out.write(processed_frame)

# Release resources
cap.release()
out.release()

print(f"Background removal complete. Output saved at {OUTPUT_VIDEO}")
