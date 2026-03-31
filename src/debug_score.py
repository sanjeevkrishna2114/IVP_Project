import cv2
import os
import easyocr

reader = easyocr.Reader(['en'], gpu=False)

FRAMES_DIR = r"C:\Users\sankr\Videos\IVP\IVP_Project\data\frames\match_01"

# Orange team score (left)
ORANGE_X1, ORANGE_Y1 = 264, 4
ORANGE_X2, ORANGE_Y2 = 284, 24

# Blue team score (right)
BLUE_X1, BLUE_Y1 = 356, 5
BLUE_X2, BLUE_Y2 = 376, 25

def preprocess_score_crop(crop):
    scaled = cv2.resize(crop, (crop.shape[1] * 8, crop.shape[0] * 8),
                        interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(scaled, cv2.COLOR_BGR2GRAY)
    gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    _, binary = cv2.threshold(gray, 0, 255,
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary

def preprocess_score_crop_blue(crop):
    scaled = cv2.resize(crop, (crop.shape[1] * 8, crop.shape[0] * 8),
                        interpolation=cv2.INTER_CUBIC)
    red_channel = scaled[:, :, 2]
    _, binary = cv2.threshold(red_channel, 0, 255,
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary

frames = sorted([f for f in os.listdir(FRAMES_DIR) if f.endswith(".jpg")])

print(f"{'Frame':<20} {'Orange Raw':>12} {'Blue Raw':>12}")
print("-" * 50)

for frame_file in frames:
    frame_path = os.path.join(FRAMES_DIR, frame_file)
    frame      = cv2.imread(frame_path)
    frame      = cv2.resize(frame, (640, 360))

    orange_crop = frame[ORANGE_Y1:ORANGE_Y2, ORANGE_X1:ORANGE_X2]
    blue_crop   = frame[BLUE_Y1:BLUE_Y2,     BLUE_X1:BLUE_X2]

    orange_proc = preprocess_score_crop(orange_crop)
    blue_proc   = preprocess_score_crop_blue(blue_crop)

    orange_raw = reader.readtext(orange_proc, allowlist='0123456789', detail=0)
    blue_raw   = reader.readtext(blue_proc,   allowlist='0123456789', detail=0)

    print(f"{frame_file:<20} {str(orange_raw):>12} {str(blue_raw):>12}")