# Time-Series Variation Analysis:

## Video 1 (First Plot):


Shows relatively stable X and Y coordinates (blue and orange lines) around 0.6 and 0.55 respectively



The Z coordinate (green line) shows more dramatic variation:

1. Initial gradual increase from -0.2 to 0
2. Sharp dip around frame 10-15
3. Two distinct peaks around frames 20 and 25
4. Stabilizes after frame 30 around 0.05




## Video 2 (Second Plot):


Higher X coordinate values (blue line) around 0.8, very stable throughout

Y coordinates (orange line) stable around 0.5

Z coordinate (green line) shows similar pattern to Video 1 but:

1. Less dramatic variations
2. More stable after frame 25
3. Longer duration (80 frames vs 45 frames in Video 1)




## DTW Alignment Path Heatmap (Third Plot):


1. Shows the Dynamic Time Warping alignment between the two videos
2. The diagonal dark blue line indicates a good temporal alignment between the sequences
3. Distance measure of 23.95 suggests moderate similarity
4. The straight diagonal pattern suggests consistent timing between the two videos without major temporal distortions

## Key Findings:

1. The two videos appear to be capturing similar motions/movements but at different scales or from different perspectives
2. Both show most stability in X and Y coordinates while Z coordinates show the most variation
3. Video 2 appears to be a longer, more stable version of a similar motion pattern seen in Video 1
4. The DTW alignment suggests good temporal correspondence between the two sequences despite their differences in absolute values