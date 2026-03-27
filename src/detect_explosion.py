import cv2
import numpy as np
import os
from preprocess import preprocess_frame

def get_brightness_score(hsv_frame):
    v_channel = hsv_frame[:, :, 2]
    bright_pixels = np.sum(v_channel > 200)
    total_pixels = v_channel.size
    brightness_ratio = bright_pixels / total_pixels
    return brightness_ratio

def detect_explosion(frame_path, threshold=0.35):
    processed = preprocess_frame(frame_path)
    hsv = processed["hsv"]
    score = get_brightness_score(hsv)
    is_explosion = score > threshold
    return {
        "frame": os.path.basename(frame_path),
        "brightness_score": round(score, 4),
        "explosion_detected": is_explosion
    }

def run_on_all_frames(frames_dir, threshold=0.35):
    frames = sorted([
        f for f in os.listdir(frames_dir) if f.endswith(".jpg")
    ])
    
    results = []
    explosions = []

    print(f"Running explosion detector on {len(frames)} frames...")
    print("-" * 40)

    for frame_file in frames:
        frame_path = os.path.join(frames_dir, frame_file)
        result = detect_explosion(frame_path, threshold)
        results.append(result)

        if result["explosion_detected"]:
            explosions.append(result)
            print(f"EXPLOSION DETECTED → {result['frame']} | score: {result['brightness_score']}")

    print("-" * 40)
    print(f"Done! {len(explosions)} explosion events found out of {len(frames)} frames")
    return results, explosions

if __name__ == "__main__":
    FRAMES_DIR = r"C:\Users\sankr\Videos\IVP\IVP_Project\data\frames\match_01"
    THRESHOLD = 0.35

    results, explosions = run_on_all_frames(FRAMES_DIR, THRESHOLD)