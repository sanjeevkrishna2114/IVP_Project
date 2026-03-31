import cv2
import os

FRAMES_DIR = r"C:\Users\sankr\Videos\IVP\IVP_Project\data\frames\match_01"
OUTPUT_DIR = r"C:\Users\sankr\Videos\IVP\IVP_Project\data\debug_crops"

os.makedirs(OUTPUT_DIR, exist_ok=True)

BLUE_X1, BLUE_Y1 = 358, 8
BLUE_X2, BLUE_Y2 = 375, 23

frame_path = os.path.join(FRAMES_DIR, "frame_00001.jpg")
frame      = cv2.imread(frame_path)
frame      = cv2.resize(frame, (640, 360))

blue_crop = frame[BLUE_Y1:BLUE_Y2, BLUE_X1:BLUE_X2]

# Scale up to see clearly
blue_big = cv2.resize(blue_crop, (blue_crop.shape[1] * 8, blue_crop.shape[0] * 8),
                      interpolation=cv2.INTER_NEAREST)

cv2.imwrite(os.path.join(OUTPUT_DIR, "blue_crop_check.jpg"), blue_big)
print("Saved blue_crop_check.jpg — open it and check if the digit is visible")