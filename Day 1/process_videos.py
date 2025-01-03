import cv2
import mediapipe as mp
import pandas as pd
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

# Function to extract keypoints from a video
def extract_keypoints(video_path, skip_frames=5, significant_keypoints=None):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)
    
    keypoints_list = []
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % skip_frames == 0:  # Process only every 'skip_frames' frame
            results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if results.pose_landmarks:
                keypoints = [(landmark.x, landmark.y, landmark.z) for landmark in results.pose_landmarks.landmark]
                if significant_keypoints:
                    keypoints = [keypoints[i] for i in significant_keypoints]  # Select significant keypoints
                keypoints_list.append(keypoints)
        
        frame_count += 1
    
    cap.release()
    return keypoints_list

# Function to save keypoints to a CSV file
def save_keypoints_to_csv(keypoints, output_path):
    flat_keypoints = [np.array(frame).flatten().tolist() for frame in keypoints]
    df = pd.DataFrame(flat_keypoints)
    df.to_csv(output_path, index=False)

# Function to compare two keypoint sequences using FastDTW
def compare_keypoints(seq1, seq2):
    # Flatten keypoints into a single 1D array for each frame
    flat_seq1 = [np.array(frame).flatten() for frame in seq1]
    flat_seq2 = [np.array(frame).flatten() for frame in seq2]
    
    # Use FastDTW for approximate similarity computation
    distance, _ = fastdtw(flat_seq1, flat_seq2, dist=euclidean)
    return distance

# Main function
if __name__ == "__main__":
    # Update video paths with your file locations
    video_paths = ['data/video 1.mp4', 'data/video 2.mp4']
    all_keypoints = []

    # Indices of significant keypoints to reduce computation
    significant_keypoints = [0, 11, 12, 23, 24]  # Example: Nose, shoulders, and hips
    
    for i, video_path in enumerate(video_paths):
        print(f"Processing video: {video_path}")
        keypoints = extract_keypoints(video_path, skip_frames=5, significant_keypoints=significant_keypoints)
        print(f"Extracted {len(keypoints)} frames of keypoints from {video_path}")
        all_keypoints.append(keypoints)
        save_keypoints_to_csv(keypoints, f"data/video_{i + 1}_keypoints.csv")
    
    # Compare keypoints of the two videos
    if all_keypoints[0] and all_keypoints[1]:
        print("Starting similarity computation...")
        similarity_score = compare_keypoints(all_keypoints[0], all_keypoints[1])
        print(f"Similarity Score (FastDTW): {similarity_score}")
    else:
        print("One or both keypoint sequences are empty.")
