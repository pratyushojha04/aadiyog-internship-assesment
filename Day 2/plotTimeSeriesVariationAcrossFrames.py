# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import numpy as np
# from dtaidistance import dtw

# # Function to read keypoints from CSV files
# def read_keypoints_from_csv(file_path):
#     return pd.read_csv(file_path).values

# # Function to plot time-series variation
# def plot_time_series(keypoints1, keypoints2):
#     # Create time-series plots for the first video
#     plt.figure(figsize=(12, 6))
#     plt.plot(keypoints1[:, 0], label='Video 1 X', color='blue')
#     plt.plot(keypoints1[:, 1], label='Video 1 Y', color='orange')
#     plt.plot(keypoints1[:, 2], label='Video 1 Z', color='green')
#     plt.title('Time-Series Variation for Video 1')
#     plt.xlabel('Frame')
#     plt.ylabel('Keypoint Coordinates')
#     plt.legend()
#     plt.show()

#     # Create time-series plots for the second video
#     plt.figure(figsize=(12, 6))
#     plt.plot(keypoints2[:, 0], label='Video 2 X', color='blue')
#     plt.plot(keypoints2[:, 1], label='Video 2 Y', color='orange')
#     plt.plot(keypoints2[:, 2], label='Video 2 Z', color='green')
#     plt.title('Time-Series Variation for Video 2')
#     plt.xlabel('Frame')
#     plt.ylabel('Keypoint Coordinates')
#     plt.legend()
#     plt.show()

# # Function to plot DTW heatmap
# def plot_dtw_heatmap(seq1, seq2):
#     # Calculate DTW distance matrix
#     dtw_distance = dtw.distance(seq1, seq2)
#     dtw_matrix = dtw.distance_matrix(seq1, seq2)

#     plt.figure(figsize=(10, 8))
#     sns.heatmap(dtw_matrix, cmap='viridis')
#     plt.title('DTW Alignment Heatmap')
#     plt.xlabel('Video 2 Frames')
#     plt.ylabel('Video 1 Frames')
#     plt.show()

# # Main function
# if __name__ == "__main__":
#     # Load keypoints from CSV files
#     keypoints1 = read_keypoints_from_csv('data/video_1_keypoints.csv')
#     keypoints2 = read_keypoints_from_csv('data/video_2_keypoints.csv')
    
#     print(f"Loaded {len(keypoints1)} keypoints from video 1.")
#     print(f"Loaded {len(keypoints2)} keypoints from video 2.")
    
#     # Plot time-series variation
#     plot_time_series(keypoints1, keypoints2)
    
#     # Plot DTW heatmap
#     plot_dtw_heatmap(keypoints1, keypoints2)


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

# Function to read keypoints from CSV files
def read_keypoints_from_csv(file_path):
    return pd.read_csv(file_path).values

# Function to flatten keypoints (X, Y, Z) into a 1D array per frame
def flatten_keypoints(keypoints):
    return np.hstack(keypoints)  # Combine X, Y, Z coordinates into a single array

# Function to plot time-series variation
def plot_time_series(keypoints1, keypoints2):
    # Create time-series plots for the first video
    plt.figure(figsize=(12, 6))
    plt.plot(keypoints1[:, 0], label='Video 1 X', color='blue')
    plt.plot(keypoints1[:, 1], label='Video 1 Y', color='orange')
    plt.plot(keypoints1[:, 2], label='Video 1 Z', color='green')
    plt.title('Time-Series Variation for Video 1')
    plt.xlabel('Frame')
    plt.ylabel('Keypoint Coordinates')
    plt.legend()
    plt.show()

    # Create time-series plots for the second video
    plt.figure(figsize=(12, 6))
    plt.plot(keypoints2[:, 0], label='Video 2 X', color='blue')
    plt.plot(keypoints2[:, 1], label='Video 2 Y', color='orange')
    plt.plot(keypoints2[:, 2], label='Video 2 Z', color='green')
    plt.title('Time-Series Variation for Video 2')
    plt.xlabel('Frame')
    plt.ylabel('Keypoint Coordinates')
    plt.legend()
    plt.show()

# Function to plot DTW heatmap showing alignment between frames of two videos
def plot_fastdtw_heatmap(seq1, seq2):
    # Flatten the keypoints for both sequences (flatten per frame)
    seq1_flat = np.array([flatten_keypoints(frame) for frame in seq1])
    seq2_flat = np.array([flatten_keypoints(frame) for frame in seq2])

    # Ensure both sequences have the same number of frames (by trimming the longer one)
    min_len = min(len(seq1_flat), len(seq2_flat))
    seq1_flat = seq1_flat[:min_len]
    seq2_flat = seq2_flat[:min_len]
    
    # Calculate DTW distance and alignment path using fastdtw
    distance, path = fastdtw(seq1_flat, seq2_flat, dist=euclidean)  # FastDTW distance calculation
    print(f"DTW distance: {distance}")
    
    # Prepare the DTW distance matrix for heatmap
    dtw_matrix = np.zeros((len(seq1_flat), len(seq2_flat)))
    for i in range(len(path)):
        dtw_matrix[path[i][0], path[i][1]] = distance  # Fill the matrix with the DTW distance value

    # Plot the heatmap of the DTW distance matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(dtw_matrix, cmap='YlGnBu', cbar=False, xticklabels=False, yticklabels=False)
    plt.title(f'DTW Alignment Path Heatmap (Distance: {distance:.2f})')
    plt.xlabel('Video 2 Frames')
    plt.ylabel('Video 1 Frames')
    plt.show()

# Main function
if __name__ == "__main__":
    # Load keypoints from CSV files
    keypoints1 = read_keypoints_from_csv('data/video_1_keypoints.csv')
    keypoints2 = read_keypoints_from_csv('data/video_2_keypoints.csv')
    
    print(f"Loaded {len(keypoints1)} keypoints from video 1.")
    print(f"Loaded {len(keypoints2)} keypoints from video 2.")
    
    # Plot time-series variation
    plot_time_series(keypoints1, keypoints2)
    
    # Plot DTW heatmap
    plot_fastdtw_heatmap(keypoints1, keypoints2)
