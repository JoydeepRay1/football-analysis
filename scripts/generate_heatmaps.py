import cv2
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

def generate_heatmap(frames_folder, output_folder):
    # Create an empty heatmap
    heatmap = None
    frame_count = 0

    # Iterate over all frames
    for frame_file in os.listdir(frames_folder):
        frame_path = os.path.join(frames_folder, frame_file)
        frame = cv2.imread(frame_path)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if heatmap is None:
            heatmap = np.zeros_like(frame_gray, dtype=np.float32)
        heatmap += frame_gray
        frame_count += 1

    # Normalize heatmap
    heatmap /= frame_count
    heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    
    # Save the heatmap
    plt.imshow(heatmap, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.savefig(os.path.join(output_folder, 'heatmap.png'))

if __name__ == "__main__":
    frames_folder = sys.argv[1]
    output_folder = sys.argv[2]
    generate_heatmap(frames_folder, output_folder)
