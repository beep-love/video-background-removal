import cv2
import numpy as np

# RetinaFace from InsightFace
from insightface.app import FaceAnalysis

def blur_background_faces(
    input_video_path: str,
    output_video_path: str,
    max_foreground_faces: int = 4,
    blur_kernel_size: int = 51
):
    """
    Detect faces in video with RetinaFace and blur background faces.
    
    :param input_video_path: Path to input video
    :param output_video_path: Path to save output video
    :param max_foreground_faces: How many largest faces to keep unblurred
    :param blur_kernel_size: Size of Gaussian blur kernel
    """
    # Initialize FaceAnalysis with RetinaFace model
    face_detector = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
    face_detector.prepare(ctx_id=0, det_size=(640, 640)) 
    # Depending on your hardware, you might need ctx_id=-1 for CPU only
    
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {input_video_path}")
        return
    
    # Prepare output writer
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect faces (returns a list of face objects)
        faces = face_detector.get(frame)
        
        # If no faces, just write the frame as is
        if len(faces) == 0:
            out.write(frame)
            continue
        
        # Sort faces by bounding box area (descending)
        # face.bbox is [x1, y1, x2, y2]
        faces_sorted = sorted(
            faces, 
            key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]), 
            reverse=True
        )
        
        # Keep top N largest faces as "foreground"
        foreground_faces = faces_sorted[:max_foreground_faces]
        
        # Mark background faces as all faces except the top N largest
        background_faces = faces_sorted[max_foreground_faces:]
        
        # Blur background faces
        for f in background_faces:
            x1, y1, x2, y2 = [int(coord) for coord in f.bbox]
            
            # Clip coordinates to frame boundaries
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(width, x2)
            y2 = min(height, y2)
            
            face_roi = frame[y1:y2, x1:x2]
            # Apply Gaussian blur
            face_roi = cv2.GaussianBlur(face_roi, (blur_kernel_size, blur_kernel_size), 0)
            frame[y1:y2, x1:x2] = face_roi
        
        out.write(frame)
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    input_path = "input/shot-movie.mp4"
    output_path = "output/bg_face_blur_output_video.mp4"
    
    # We keep 1 biggest face unblurred (the "main" subject), and blur all others
    blur_background_faces(
        input_video_path=input_path,
        output_video_path=output_path,
        max_foreground_faces=1,
        blur_kernel_size=51
    )
    print("Finished processing. The output video is saved at:", output_path)
