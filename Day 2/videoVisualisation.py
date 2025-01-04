import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def process_and_visualize(video_path1, video_path2, output_path):
    # Open video files
    cap1 = cv2.VideoCapture(video_path1)
    cap2 = cv2.VideoCapture(video_path2)
    
    # Check if videos loaded successfully
    if not cap1.isOpened() or not cap2.isOpened():
        print("Error: Unable to open one or both videos.")
        return

    # Get video properties for saving
    frame_width = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap1.get(cv2.CAP_PROP_FPS))
    min_frames = min(int(cap1.get(cv2.CAP_PROP_FRAME_COUNT)), int(cap2.get(cv2.CAP_PROP_FRAME_COUNT)))

    # Define codec and create VideoWriter object
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width * 2, frame_height))

    with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        for frame_idx in range(min_frames):
            # Read frames from both videos
            ret1, frame1 = cap1.read()
            ret2, frame2 = cap2.read()

            if not ret1 or not ret2:
                print(f"Error reading frames at index {frame_idx}")
                break

            # Convert frames to RGB (required by MediaPipe)
            rgb_frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            rgb_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)

            # Process frames to detect keypoints
            result1 = pose.process(rgb_frame1)
            result2 = pose.process(rgb_frame2)

            # Draw keypoints and connections on the frames
            if result1.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame1, result1.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2))
            
            if result2.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame2, result2.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2))

            # Concatenate the frames horizontally for comparison
            combined_frame = np.hstack((frame1, frame2))

            # Write the combined frame to the output video
            out.write(combined_frame)

            # Save a frame periodically for debugging (optional)
            if frame_idx % 100 == 0:  # Save every 100th frame
                cv2.imwrite(f"debug_frame_{frame_idx}.png", combined_frame)

    # Release resources
    cap1.release()
    cap2.release()
    out.release()
    print(f"Output video saved to {output_path}")

# Example usage
if __name__ == "__main__":
    video_path1 = "/home/pratyush/Documents/Internship assesment/aadiyog internship assesment/data/video 1.mp4"
    video_path2 = "/home/pratyush/Documents/Internship assesment/aadiyog internship assesment/data/video 2.mp4"
    output_path = "/home/pratyush/Documents/Internship assesment/aadiyog internship assesment/Day 2/output.avi"

    process_and_visualize(video_path1, video_path2, output_path)
