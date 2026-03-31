import cv2
import numpy as np
import os

OUTPUT_DIR = r"C:\Users\sankr\Videos\IVP\IVP_Project\data\debug_crops"
FRAMES_DIR = r"C:\Users\sankr\Videos\IVP\IVP_Project\data\frames\match_01"

# Orange team score (left)
ORANGE_X1, ORANGE_Y1 = 264, 4
ORANGE_X2, ORANGE_Y2 = 284, 24

# Blue team score (right)
BLUE_X1, BLUE_Y1 = 356, 6
BLUE_X2, BLUE_Y2 = 376, 26
frame_path = os.path.join(FRAMES_DIR, "frame_00001.jpg")
frame      = cv2.imread(frame_path)
frame      = cv2.resize(frame, (640, 360))

crop = frame[ORANGE_Y1:ORANGE_Y2, ORANGE_X1:ORANGE_X2]

# Step 1 — scale up first
scaled = cv2.resize(crop, (crop.shape[1] * 8, crop.shape[0] * 8),
                    interpolation=cv2.INTER_CUBIC)

# Step 2 — convert to grayscale
gray = cv2.cvtColor(scaled, cv2.COLOR_BGR2GRAY)

# Step 3 — threshold to isolate bright white digit
_, binary_simple = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

# Step 4 — otsu thresholding
_, binary_otsu = cv2.threshold(gray, 0, 255,
                               cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Step 5 — adaptive threshold
adaptive = cv2.adaptiveThreshold(gray, 255,
                                 cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 11, 2)
# After binary_otsu line add:
inverted = cv2.bitwise_not(binary_otsu)
cv2.imwrite(os.path.join(OUTPUT_DIR, "crop_inverted.jpg"), inverted)
# Save all versions so we can compare
cv2.imwrite(os.path.join(OUTPUT_DIR, "crop_scaled.jpg"),        scaled)
cv2.imwrite(os.path.join(OUTPUT_DIR, "crop_gray.jpg"),          gray)
cv2.imwrite(os.path.join(OUTPUT_DIR, "crop_binary_simple.jpg"), binary_simple)
cv2.imwrite(os.path.join(OUTPUT_DIR, "crop_binary_otsu.jpg"),   binary_otsu)
cv2.imwrite(os.path.join(OUTPUT_DIR, "crop_adaptive.jpg"),      adaptive)

print("Saved 5 versions to debug_crops folder")
print("Check which one makes the digit most clear and readable")