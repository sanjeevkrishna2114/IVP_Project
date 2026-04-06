# Rocket League Match Analyzer

An automated computer vision pipeline designed to analyze Rocket League Championship Series (RLCS) match footage. This project automates frame extraction, detects goal events via visual "explosions," and tracks real-time scores using Optical Character Recognition (OCR).

---

## Architecture Diagram
<img width="1024" height="768" alt="DL Architecture Sub (1)" src="https://github.com/user-attachments/assets/12184623-0c21-4f3f-957d-c84a4ff177e3" />

## Features

* **Frame Extraction**: Automated conversion of `.mp4` match videos into image sequences at a specified FPS using FFmpeg.
* **Goal Detection**: High-accuracy detection of "Goal Explosions" using localized brightness analysis and frame-to-frame intensity deltas.
* **Scoreboard Tracking**: Real-time score extraction for Orange and Blue teams using localized ROI cropping and OCR.
* **Robust Logic**: Persistent score tracking that filters out OCR noise by only accepting logical increments ($CurrentScore + 1$).
* **Calibration Suite**: Interactive tools for coordinate mapping and preprocessing optimization (Otsu, Adaptive thresholding).

---

## Tech Stack

* **Language**: Python 3.x
* **Vision**: OpenCV (`cv2`)
* **OCR**: EasyOCR
* **Video Utilities**: FFmpeg (via `subprocess`)
* **Math/Processing**: NumPy

---

## Project Structure

* `extract_frames.py`: Converts raw match videos into frame datasets.
* `preprocess.py`: Core utilities for resizing, blurring, and color space transformations (HSV/Gray).
* `detect_explosion.py`: The logic for detecting goals based on visual "flashes".
* `detect_score.py`: The main driver for scoreboard tracking and series management.
* **Debug Tools**:
    * `debug_scoreboard.py`: Interactive $X,Y$ coordinate finder.
    * `debug_explosion.py`: Statistical analysis of brightness and delta values for threshold tuning.
    * `preprocess_crop.py`: Visualization tool for testing OCR thresholding techniques.
    * `debug_score.py`: Benchmarking OCR performance across specific frame ranges.

---

## Methodology

### 1. Explosion Detection
The system monitors a center-screen Region of Interest (ROI) for sudden visual spikes. A goal is flagged if:
1.  **Bright Pixel Ratio**: The percentage of pixels in the HSV "Value" channel exceeding 200 is above a threshold (default: $0.35$).
2.  **Frame Delta**: The average intensity change between the current and previous frame exceeds a threshold (default: $80.0$).

### 2. Scoreboard OCR Pipeline
Digits are processed through a specific pipeline to maximize OCR accuracy:
1.  **Cropping**: Isolate team-specific score regions (Orange: $[264, 4]$ to $[284, 24]$ | Blue: $[358, 8]$ to $[375, 23]$).
2.  **Upscaling**: $8\times$ cubic interpolation to provide the OCR engine with higher-definition input.
3.  **Binarization**: Application of **Otsu’s Thresholding** to isolate digits from team-colored backgrounds.

---

## Usage Workflow

1.  **Extract Frames**: Update `VIDEO_PATH` in `extract_frames.py` and run it to prepare your data.
2.  **Calibrate**: If using different resolutions, run `debug_scoreboard.py` to find the correct ROI coordinates.
3.  **Analyze**: Run `detect_score.py` to process the match. It will log goals, timestamps, and game transitions automatically.

> [!IMPORTANT]
> This project requires **FFmpeg** to be installed and added to your system's PATH. Update all hardcoded file paths in the scripts to match your local environment before execution.

---

**Author**: Sanjeev Krishna S.  
**Institution**: Shiv Nadar University, Chennai
