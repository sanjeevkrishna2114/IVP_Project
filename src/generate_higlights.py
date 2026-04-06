import json
import os
import subprocess

VIDEO_PATH  = r"C:\Users\sankr\Videos\IVP\IVP_Project\data\raw\rlcs_match_01.mp4"
JSON_PATH   = r"C:\Users\sankr\Videos\IVP\IVP_Project\outputs\match_01_highlights.json"
OUTPUT_DIR  = r"C:\Users\sankr\Videos\IVP\IVP_Project\outputs\clips"

def extract_clip(video_path, start_sec, end_sec, output_path):
    duration = end_sec - start_sec
    command  = [
        "ffmpeg",
        "-ss", str(start_sec),
        "-i", video_path,
        "-t", str(duration),
        "-c:v", "libx264",
        "-c:a", "aac",
        "-y",
        output_path
    ]
    subprocess.run(command, check=True,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)

def generate_highlights(json_path, video_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    with open(json_path, "r") as f:
        results = json.load(f)

    categories = {
        "premium":  "PREMIUM",
        "feature":  "DEMO",
        "standard": "STANDARD"
    }

    total = 0

    for category, label in categories.items():
        clips = results[category]
        print(f"\nGenerating {len(clips)} {label} clips...")
        print("-" * 50)

        for i, clip in enumerate(clips, 1):
            start    = clip["clip_start"]
            end      = clip["clip_end"]
            filename = f"{label}_{i:02d}_{start}s_{end}s.mp4"
            out_path = os.path.join(output_dir, filename)

            print(f"  Cutting {filename} ({start}s → {end}s)...")
            extract_clip(video_path, start, end, out_path)
            print(f"  Saved → {out_path}")
            total += 1

    print("\n" + "=" * 50)
    print(f"Done! {total} highlight clips saved to {output_dir}")

if __name__ == "__main__":
    generate_highlights(JSON_PATH, VIDEO_PATH, OUTPUT_DIR)