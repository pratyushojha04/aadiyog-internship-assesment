import cv2
import mediapipe as mp
import pandas as pd
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

# Function to extract keypoints from a video
def extract_keypoints(video_path, skip_frames=5):
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
                keypoints_list.append(keypoints)
        
        frame_count += 1
    
    cap.release()
    return keypoints_list

# Function to save keypoints to a CSV file
def save_keypoints_to_csv(keypoints, output_path):
    flat_keypoints = [np.array(frame).flatten().tolist() for frame in keypoints]
    df = pd.DataFrame(flat_keypoints)
    df.to_csv(output_path, index=False)

# Function to normalize the keypoints (scale the values between 0 and 1)
def normalize_keypoints(keypoints_list):
    """
    Normalize the keypoints to a range [0, 1] based on the max values of the x, y, z coordinates.
    """
    # Extract all keypoints from the list
    all_keypoints = np.array([kp for frame in keypoints_list for kp in frame])
    
    # Get the min and max values for x, y, z
    min_vals = np.min(all_keypoints, axis=0)
    max_vals = np.max(all_keypoints, axis=0)
    
    # Normalize each keypoint
    normalized_keypoints_list = []
    for frame in keypoints_list:
        normalized_frame = [
            [(kp[0] - min_vals[0]) / (max_vals[0] - min_vals[0]),
             (kp[1] - min_vals[1]) / (max_vals[1] - min_vals[1]),
             (kp[2] - min_vals[2]) / (max_vals[2] - min_vals[2])] for kp in frame]
        normalized_keypoints_list.append(normalized_frame)
    
    return normalized_keypoints_list

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
    
    for i, video_path in enumerate(video_paths):
        print(f"Processing video: {video_path}")
        keypoints = extract_keypoints(video_path, skip_frames=5)
        print(f"Extracted {len(keypoints)} frames of keypoints from {video_path}")
        all_keypoints.append(keypoints)
        save_keypoints_to_csv(keypoints, f"data/video_{i + 1}_keypoints.csv")
    
    # Normalize keypoints before comparing
    all_keypoints[0] = normalize_keypoints(all_keypoints[0])
    all_keypoints[1] = normalize_keypoints(all_keypoints[1])

    # Compare keypoints of the two videos
    if all_keypoints[0] and all_keypoints[1]:
        print("Starting similarity computation...")
        similarity_score = compare_keypoints(all_keypoints[0], all_keypoints[1])
        print(f"Similarity Score (FastDTW): {similarity_score}")
    else:
        print("One or both keypoint sequences are empty.")
