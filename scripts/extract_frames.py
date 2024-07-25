import cv2
import os
import sys

def extract_frames(video_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imwrite(f"{output_folder}/frame_{frame_count:05d}.jpg", frame)
        frame_count += 1
    
    cap.release()

if __name__ == "__main__":
    video_path = sys.argv[1]
    output_folder = sys.argv[2]
    extract_frames(video_path, output_folder)

