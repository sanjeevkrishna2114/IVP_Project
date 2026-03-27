import cv2
import numpy as np
import os
from preprocess import preprocess_frame

def get_center_crop(frame, crop_ratio=0.4):
    h, w = frame.shape[:2]
    cx, cy = w // 2, h // 2
    crop_w = int(w * crop_ratio) // 2
    crop_h = int(h * crop_ratio) // 2
    return frame[cy - crop_h:cy + crop_h, cx - crop_w:cx + crop_w]

def get_bright_pixel_ratio(hsv_crop, v_threshold=200):
    v_channel = hsv_crop[:, :, 2]
    bright_mask = v_channel > v_threshold
    ratio = np.sum(bright_mask) / bright_mask.size
    return ratio

def get_frame_delta(hsv_prev, hsv_curr):
    v_prev = hsv_prev[:, :, 2].astype(np.float32)
    v_curr = hsv_curr[:, :, 2].astype(np.float32)
    delta = np.mean(np.abs(v_curr - v_prev))
    return delta

def run_on_all_frames(frames_dir, bright_threshold=0.35, delta_threshold=80.0):
    frames = sorted([
        f for f in os.listdir(frames_dir) if f.endswith(".jpg")
    ])

    results = []
    explosions = []
    prev_hsv_crop = None

    print(f"Running v3 explosion detector on {len(frames)} frames...")
    print(f"Bright pixel threshold : {bright_threshold}")
    print(f"Delta threshold        : {delta_threshold}")
    print("-" * 40)

    for frame_file in frames:
        frame_path = os.path.join(frames_dir, frame_file)
        processed = preprocess_frame(frame_path)
        hsv = processed["hsv"]

        center_crop = get_center_crop(hsv, crop_ratio=0.4)
        bright_ratio = get_bright_pixel_ratio(center_crop)

        delta_score = 0.0
        if prev_hsv_crop is not None:
            delta_score = get_frame_delta(prev_hsv_crop, center_crop)

        both_triggered = (
            bright_ratio > bright_threshold and
            delta_score > delta_threshold
        )

        result = {
            "frame": frame_file,
            "bright_ratio": round(bright_ratio, 4),
            "delta_score": round(delta_score, 4),
            "explosion_detected": both_triggered
        }
        results.append(result)

        if both_triggered:
            explosions.append(result)
            print(f"EXPLOSION → {frame_file} | bright_ratio: {bright_ratio:.4f} | delta: {delta_score:.4f}")

        prev_hsv_crop = center_crop

    print("-" * 40)
    print(f"Done! {len(explosions)} explosion events out of {len(frames)} frames")
    return results, explosions

if __name__ == "__main__":
    FRAMES_DIR = r"C:\Users\sankr\Videos\IVP\IVP_Project\data\frames\match_01"

    results, explosions = run_on_all_frames(
        FRAMES_DIR,
        bright_threshold=0.35,
        delta_threshold=80.0
    )