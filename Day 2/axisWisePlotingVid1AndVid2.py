import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist
import seaborn as sns
from fastdtw import fastdtw




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

# Function to compare X, Y, Z axes of two videos and plot them separately
def plot_xyz_comparison(keypoints1, keypoints2):
    axes = ['X', 'Y', 'Z']
    colors = ['blue', 'orange', 'green']
    
    # Separate the axes and plot comparisons
    for i, axis in enumerate(axes):
        plt.figure(figsize=(12, 6))
        plt.plot(keypoints1[:, i], label=f'Video 1 {axis}', color=colors[i], linestyle='-')
        plt.plot(keypoints2[:, i], label=f'Video 2 {axis}', color=colors[i], linestyle='--')
        plt.title(f'{axis}-Axis Comparison Between Video 1 and Video 2')
        plt.xlabel('Frame')
        plt.ylabel(f'{axis}-Coordinate')
        plt.legend()
        plt.show()

def plot_fastdtw_heatmap(keypoints1, keypoints2):
    # Calculate the pairwise distances between frames
    distances = cdist(keypoints1, keypoints2, metric='euclidean')

    # Plot the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(distances, cmap='viridis', cbar=True)
    plt.title('DTW Heatmap Between Video 1 and Video 2')
    plt.xlabel('Video 2 Frames')
    plt.ylabel('Video 1 Frames')
    plt.show()

    # Compute the DTW alignment using FastDTW
    _, path = fastdtw(keypoints1, keypoints2, dist=lambda x, y: np.linalg.norm(x - y))

    # Visualize the alignment path on the heatmap
    alignment_x, alignment_y = zip(*path)
    plt.figure(figsize=(10, 8))
    sns.heatmap(distances, cmap='viridis', cbar=True)
    plt.plot(alignment_y, alignment_x, color='red', label='Alignment Path')
    plt.title('DTW Alignment Path Over Heatmap')
    plt.xlabel('Video 2 Frames')
    plt.ylabel('Video 1 Frames')
    plt.legend()
    plt.show()

# Main function
if __name__ == "__main__":
    # Load keypoints from CSV files
    keypoints1 = pd.read_csv('data/video_1_keypoints.csv').values
    keypoints2 = pd.read_csv('data/video_2_keypoints.csv').values
    
    print(f"Loaded {len(keypoints1)} keypoints from video 1.")
    print(f"Loaded {len(keypoints2)} keypoints from video 2.")
    
    # Plot time-series variation
    plot_time_series(keypoints1, keypoints2)
    
    # Plot X, Y, Z axis comparisons
    plot_xyz_comparison(keypoints1, keypoints2)

    # Plot DTW heatmap
    plot_fastdtw_heatmap(keypoints1, keypoints2)
