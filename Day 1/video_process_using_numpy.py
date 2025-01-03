# this file was not needed but I created becouse I wanted to try out numpy and it 
# giving quick response.




import cv2
import mediapipe as mp
import pandas as pd
import numpy as np  # Import NumPy for distance calculations

# Function to extract keypoints from a video
def extract_keypoints(video_path):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)
    
    keypoints_list = []
    
    cap = cv2.VideoCapture(video_path)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process the frame and extract keypoints
        results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.pose_landmarks:
            keypoints = [(landmark.x, landmark.y, landmark.z) for landmark in results.pose_landmarks.landmark]
            keypoints_list.append(keypoints)
    
    cap.release()
    return keypoints_list

# Function to save keypoints to a CSV file
def save_keypoints_to_csv(keypoints, output_path):
    df = pd.DataFrame(keypoints)
    df.to_csv(output_path, index=False)

# Function to calculate Euclidean distance between two keypoint sequences
def calculate_similarity(seq1, seq2):
    # Convert sequences to NumPy arrays
    arr1 = np.array(seq1)
    arr2 = np.array(seq2)
    
    # Ensure the sequences are the same length for comparison
    min_length = min(len(arr1), len(arr2))
    
    # Calculate Euclidean distance
    distance = np.linalg.norm(arr1[:min_length] - arr2[:min_length])
    return distance

# Main function
if __name__ == "__main__":
    video_paths = ['data/video 1.mp4', 'data/video 2.mp4']  # Update with your video paths
    all_keypoints = []
    
    for video_path in video_paths:
        keypoints = extract_keypoints(video_path)
        print(f"Extracted {len(keypoints)} keypoints from {video_path}")  # Debugging output
        all_keypoints.append(keypoints)
        save_keypoints_to_csv(keypoints, f"{video_path}_keypoints.csv")
    
    # Compare keypoints of the two videos
    if all_keypoints[0] and all_keypoints[1]:  # Check if both sequences are non-empty
        similarity_score = calculate_similarity(all_keypoints[0], all_keypoints[1])
        print(f"Similarity Score (Euclidean Distance): {similarity_score}")
    else:
        print("One or both keypoint sequences are empty.")