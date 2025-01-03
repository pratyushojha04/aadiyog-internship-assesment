# Documentation for Video Similarity Analysis Using Keypoints and Distance Metrics using MediaPipe Pose 

### Overview:
This project involves analyzing the similarity between two videos by extracting keypoints using **MediaPipe Pose**, calculating the **Distance** between keypoint sequences using two different methods: **FastDTW (Dynamic Time Warping)(FastDTW make fast computation as it skips frames like skip every 5 frames)** and **Euclidean Distance**. The goal is to quantify how similar or dissimilar the movements in the two videos are based on keypoint data.

### NOTE : 
   Here I use FastDtW to make fast computation it is just like DTW and I have involved one more comparision method which is Euclidean Distance. becouse initially I was using DTW and it was taking too much time so I have used Euclidean Distance then after I came to know about FastDTW . So decided to use both FastDTW and Euclidean Distance.
### Steps and Approach:

#### 1. **Video Input and Keypoint Extraction:**
   - The first step is to **extract keypoints** from each video. We use **MediaPipe Pose** for this purpose, which provides a set of predefined landmarks (33 in total) representing the human body.
   - For each frame in the video, **MediaPipe Pose** processes the image and returns the 3D coordinates (x, y, z) of the landmarks hence in total we have 33*3 = 99 coordinates.
   but here we are limiting keypoints to 20 to reduce unnecessary calculation hence 20*3 = 60
   - We **skip frames** in order to reduce computation time and focus on representative frames (e.g., every 5th frame).
   - Optionally, we can select only **significant keypoints** (e.g., head, shoulders, and hips) to focus on the most relevant movements and further reduce the data's dimensionality.
   # NOTE :
   ## Here we are limiting keypoints to 20 to reduce unnecessary calculation hence 20*3 = 60.(only those keypoints which was exposing during yoga.)

#### 2. **Storing Keypoints:**
   - After extracting the keypoints, we **flatten** the coordinates of each keypoint into a 1D array for each frame.
   - The flattened keypoints for each frame are stored in a **CSV file**, providing a structured format for further analysis.

#### 3. **Similarity Calculation (FastDTW Approach):**
   - To compare the two keypoint sequences, we use **FastDTW (Dynamic Time Warping)**, an approximate method for computing the similarity between time series data. 
   - FastDTW compares the **temporal alignment** of two sequences and computes a distance metric that accounts for possible shifts in time between corresponding frames. 
   - A **lower distance score** from FastDTW indicates a higher degree of similarity between the keypoint sequences from the two videos. The computed score reflects how closely the motion patterns in the videos match, considering both the movements and temporal alignment **usually less than 50 is considered similar but not identical 0 is identical and above 100 is dissimilar overall below 50 is considered similar**.


   - **FastDTW Workflow:**
     1. **Flatten** the keypoints of each frame into a 1D array.
     2. **Align** the two sequences using FastDTW, allowing for time shifts between frames.
     3. The result is a **similarity score** that quantifies the overall alignment of the two sequences.

   - **Interpretation of FastDTW Score:**
     - A **low FastDTW score** indicates that the two videos are **very similar**, as their keypoint sequences align well both spatially and temporally.
     - A **high FastDTW score** suggests significant differences between the keypoint sequences, indicating that the two videos are **dissimilar**.
     - Example Result: **Similarity Score (FastDTW)** = **40.2**.
       - This score is considered moderate similarity, implying that the motion in the two videos is somewhat similar but not identical.

#### 4. **Similarity Calculation (Euclidean Distance Approach):**
   - As a comparison, we also calculate the similarity using **Euclidean Distance**, which measures the spatial difference between corresponding keypoints in the two sequences.
   - The keypoint sequences are **converted into NumPy arrays**, and the Euclidean distance between corresponding frames is calculated.
   - **Euclidean distance** between two points (keypoints) is the straight-line distance in 3D space (x, y, z) and is calculated as:
     \[
     \text{Distance} = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2 + (z_1 - z_2)^2}
     \]
   - The similarity score is calculated as the **total Euclidean distance** between the two sequences.

   - **Interpretation of Euclidean Distance Score:**
     - A **smaller Euclidean distance** indicates that the keypoints between the two videos are **closer together** in space, suggesting greater similarity in their poses.
     - A **larger Euclidean distance** implies that the keypoints are farther apart, suggesting greater dissimilarity in the body poses of the two videos.
     - Example Result: **Similarity Score (Euclidean Distance)** = **21.84**.
       - This score indicates that the two videos are **moderately similar means not exactly same** based on the Euclidean distance between their keypoint sequences.

#### 5. **Analysis and Interpretation of Scores:**
   - **FastDTW vs. Euclidean Distance:**
     - Both methods provide a similarity score, but they capture different aspects of similarity:
       - **FastDTW** accounts for **temporal alignment** and can detect shifts in the time axis, making it more suitable for analyzing sequences that may have small temporal variations.
       - **Euclidean Distance**, on the other hand, measures the **spatial difference** between corresponding keypoints, which can be useful for comparing the overall position of the body in each frame.
     - In the current case:
       - The **FastDTW score (40.2)** suggests **moderate similarity** with some temporal shifts, meaning the movements in both videos are similar but not perfectly aligned.
       - The **Euclidean Distance score (21.84)** also suggests **moderate similarity**, primarily considering the spatial alignment of keypoints.

   - **What these scores depict:**
     - **Similarity Score (FastDTW)**: This indicates the **degree of alignment in movement patterns** between the two videos. A score of 37.81 suggests the videos have a **moderate similarity** in terms of pose transitions, but they are not identical.
     - **Similarity Score (Euclidean Distance)**: This measures the **spatial similarity** between keypoints. A score of 21.84 suggests that the poses in both videos are **reasonably similar** in terms of body position, but there may be some differences in the posture or alignment of body parts.

#### 6. **Conclusion and Further Improvements:**
   - The calculated similarity scores provide a numerical measure of how similar or dissimilar the two videos are based on their extracted keypoints.As per my analysis I found both the videos are similar but not identical means the motion in the two videos is somewhat similar but not identical.
   - These scores can be used to:
     - **Classify videos** as similar or dissimilar for tasks like action recognition, gesture classification, or video alignment.
     - **Quantify the degree of similarity** between different videos for further analysis. 
     
   - For further improvement:
     - **Normalization** of the similarity scores can be applied to adjust for video length or the number of frames processed.
     - **Benchmarking** with a larger dataset of labeled video pairs will help define a clearer threshold for similarity based on domain-specific applications (e.g., exercise recognition, dance moves, etc.).
     - **Optimizing keypoint extraction** by selecting only a few keypoints of interest (e.g., head, shoulders, legs) may speed up the process and further improve the similarity computation's efficiency.

## Console Image for DTW


![alt text](image.png)

---
