import cv2
import os

FRAMES_DIR = r"C:\Users\sankr\Videos\IVP\IVP_Project\data\frames\match_01"
OUTPUT_DIR = r"C:\Users\sankr\Videos\IVP\IVP_Project\data\debug_crops"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Orange team score (left)
ORANGE_X1, ORANGE_Y1 = 264, 4
ORANGE_X2, ORANGE_Y2 = 284, 24

# Blue team score (right)
BLUE_X1, BLUE_Y1 = 356, 6
BLUE_X2, BLUE_Y2 = 376, 26
frames = sorted([f for f in os.listdir(FRAMES_DIR) if f.endswith(".jpg")])[:10]

for frame_file in frames:
    frame_path = os.path.join(FRAMES_DIR, frame_file)
    frame      = cv2.imread(frame_path)
    frame      = cv2.resize(frame, (640, 360))

    orange_crop = frame[ORANGE_Y1:ORANGE_Y2, ORANGE_X1:ORANGE_X2]
    blue_crop   = frame[BLUE_Y1:BLUE_Y2,     BLUE_X1:BLUE_X2]

    # Scale up so we can actually see them clearly
    orange_big = cv2.resize(orange_crop, (orange_crop.shape[1] * 8, orange_crop.shape[0] * 8),
                            interpolation=cv2.INTER_NEAREST)
    blue_big   = cv2.resize(blue_crop,   (blue_crop.shape[1] * 8,   blue_crop.shape[0] * 8),
                            interpolation=cv2.INTER_NEAREST)

    frame_name = frame_file.replace(".jpg", "")
    cv2.imwrite(os.path.join(OUTPUT_DIR, f"{frame_name}_orange.jpg"), orange_big)
    cv2.imwrite(os.path.join(OUTPUT_DIR, f"{frame_name}_blue.jpg"),   blue_big)

print(f"Saved crops to {OUTPUT_DIR}")
print("Open the debug_crops folder and check if digits are visible")