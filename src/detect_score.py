import cv2
import numpy as np
import os
import easyocr

reader = easyocr.Reader(['en'], gpu=False)

# Score region coordinates
ORANGE_X1, ORANGE_Y1 = 264, 4
ORANGE_X2, ORANGE_Y2 = 284, 24
BLUE_X1,   BLUE_Y1   = 358, 8
BLUE_X2,   BLUE_Y2   = 375, 23

# Game boundaries (frame numbers)
GAME_BOUNDARIES = [
    {"game": 1, "start": 1,    "end": 358},
    {"game": 2, "start": 359,  "end": 622},
    {"game": 3, "start": 623,  "end": 768},
    {"game": 4, "start": 769,  "end": 1200},
]

def get_game_number(frame_num):
    for game in GAME_BOUNDARIES:
        if game["start"] <= frame_num <= game["end"]:
            return game["game"]
    return None

def crop_score_regions(frame):
    orange_crop = frame[ORANGE_Y1:ORANGE_Y2, ORANGE_X1:ORANGE_X2]
    blue_crop   = frame[BLUE_Y1:BLUE_Y2,     BLUE_X1:BLUE_X2]
    return orange_crop, blue_crop

def preprocess_orange(crop):
    scaled = cv2.resize(crop, (crop.shape[1] * 8, crop.shape[0] * 8),
                        interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(scaled, cv2.COLOR_BGR2GRAY)
    gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    _, binary = cv2.threshold(gray, 0, 255,
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary

def preprocess_blue(crop):
    scaled = cv2.resize(crop, (crop.shape[1] * 8, crop.shape[0] * 8),
                        interpolation=cv2.INTER_CUBIC)
    red_channel = scaled[:, :, 2]
    _, binary = cv2.threshold(red_channel, 0, 255,
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary

def read_digit(crop, preprocess_fn):
    processed = preprocess_fn(crop)
    result = reader.readtext(processed, allowlist='0123456789', detail=0)
    if result:
        try:
            return int(result[0].strip())
        except:
            return None
    return None

def run_on_all_frames(frames_dir):
    frames = sorted([
        f for f in os.listdir(frames_dir) if f.endswith(".jpg")
    ])

    # Tracked scores — persist across missed reads
    orange_score = 0
    blue_score   = 0
    current_game = 1
    goal_events  = []

    print(f"Running scoreboard detector on {len(frames)} frames...")
    print("-" * 50)

    for frame_file in frames:
        frame_num  = int(frame_file.replace("frame_", "").replace(".jpg", ""))
        frame_path = os.path.join(frames_dir, frame_file)
        frame      = cv2.imread(frame_path)
        frame      = cv2.resize(frame, (640, 360))

        # Reset scores at game boundaries
        game_num = get_game_number(frame_num)
        if game_num != current_game:
            print(f"\n--- Game {game_num} starts at frame {frame_num} ---\n")
            orange_score = 0
            blue_score   = 0
            current_game = game_num

        orange_crop, blue_crop = crop_score_regions(frame)

        orange_read = read_digit(orange_crop, preprocess_orange)
        blue_read   = read_digit(blue_crop,   preprocess_blue)

        # Only update if reading is valid and >= current score
        # Only accept reading if it is exactly current or current+1
        if orange_read is not None and orange_read in (orange_score, orange_score + 1):
            if orange_read == orange_score + 1:
                goal_events.append({
                    "frame":          frame_file,
                    "timestamp_sec":  frame_num,
                    "team":           "orange",
                    "orange_score":   orange_read,
                    "blue_score":     blue_score,
                    "game":           current_game
                })
                print(f"GOAL (orange) → {frame_file} | score: {orange_read} - {blue_score} | game {current_game}")
            orange_score = orange_read

        if blue_read is not None and blue_read in (blue_score, blue_score + 1):
            if blue_read == blue_score + 1:
                goal_events.append({
                    "frame":          frame_file,
                    "timestamp_sec":  frame_num,
                    "team":           "blue",
                    "orange_score":   orange_score,
                    "blue_score":     blue_read,
                    "game":           current_game
                })
                print(f"GOAL (blue)   → {frame_file} | score: {orange_score} - {blue_read} | game {current_game}")
            blue_score = blue_read

    print("-" * 50)
    print(f"Done! {len(goal_events)} goals detected across all games")
    return goal_events

if __name__ == "__main__":
    FRAMES_DIR = r"C:\Users\sankr\Videos\IVP\IVP_Project\data\frames\match_01"
    goal_events = run_on_all_frames(FRAMES_DIR)