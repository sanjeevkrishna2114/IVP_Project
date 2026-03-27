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
    return np.sum(bright_mask) / bright_mask.size

def get_frame_delta(hsv_prev, hsv_curr):
    v_prev = hsv_prev[:, :, 2].astype(np.float32)
    v_curr = hsv_curr[:, :, 2].astype(np.float32)
    return np.mean(np.abs(v_curr - v_prev))

FRAMES_DIR = r"C:\Users\sankr\Videos\IVP\IVP_Project\data\frames\match_01"

frames = sorted([f for f in os.listdir(FRAMES_DIR) if f.endswith(".jpg")])

all_results = []
prev_hsv_crop = None

print(f"Scanning {len(frames)} frames...")

for frame_file in frames:
    frame_path = os.path.join(FRAMES_DIR, frame_file)
    processed = preprocess_frame(frame_path)
    hsv = processed["hsv"]
    center_crop = get_center_crop(hsv, crop_ratio=0.4)
    bright_ratio = get_bright_pixel_ratio(center_crop)

    delta_score = 0.0
    if prev_hsv_crop is not None:
        delta_score = get_frame_delta(prev_hsv_crop, center_crop)

    all_results.append({
        "frame": frame_file,
        "bright_ratio": bright_ratio,
        "delta_score": delta_score
    })
    prev_hsv_crop = center_crop

top_bright = sorted(all_results, key=lambda x: x["bright_ratio"], reverse=True)[:10]
top_delta = sorted(all_results, key=lambda x: x["delta_score"], reverse=True)[:10]

print()
print("TOP 10 HIGHEST BRIGHT RATIO FRAMES")
print("-" * 50)
for r in top_bright:
    print(f"{r['frame']}  bright_ratio: {r['bright_ratio']:.4f}  delta: {r['delta_score']:.4f}")

print()
print("TOP 10 HIGHEST DELTA FRAMES")
print("-" * 50)
for r in top_delta:
    print(f"{r['frame']}  bright_ratio: {r['bright_ratio']:.4f}  delta: {r['delta_score']:.4f}")

print()
print(f"Max bright_ratio : {max(r['bright_ratio'] for r in all_results):.4f}")
print(f"Max delta_score  : {max(r['delta_score'] for r in all_results):.4f}")
print(f"Avg bright_ratio : {np.mean([r['bright_ratio'] for r in all_results]):.4f}")
print(f"Avg delta_score  : {np.mean([r['delta_score'] for r in all_results]):.4f}")