import subprocess
import os

def extract_frames(video_path, output_dir, fps=1):
    
    os.makedirs(output_dir, exist_ok=True)
    
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"fps={fps}",
        "-q:v", "2",
        os.path.join(output_dir, "frame_%05d.jpg")
    ]
    
    print(f"Extracting frames from: {video_path}")
    print(f"Output directory: {output_dir}")
    print(f"Frame rate: {fps} fps")
    print("-" * 40)
    
    subprocess.run(command, check=True)
    
    frame_count = len([f for f in os.listdir(output_dir) if f.endswith(".jpg")])
    print("-" * 40)
    print(f"Done! {frame_count} frames extracted to {output_dir}")


if __name__ == "__main__":
    VIDEO_PATH = r"C:\Users\sankr\Videos\IVP\IVP_Project\data\raw\rlcs_match_01.mp4"
    OUTPUT_DIR = r"C:\Users\sankr\Videos\IVP\IVP_Project\data\frames\match_01"
    FPS = 1

    extract_frames(VIDEO_PATH, OUTPUT_DIR, FPS)