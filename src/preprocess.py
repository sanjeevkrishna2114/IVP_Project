import cv2
import numpy as np
import os

def load_frame(frame_path):
    frame = cv2.imread(frame_path)
    return frame

def resize_frame(frame, width=640):
    height = int(frame.shape[0] * (width / frame.shape[1]))
    return cv2.resize(frame, (width, height))

def convert_to_hsv(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

def convert_to_gray(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def apply_gaussian_blur(frame, kernel_size=5):
    return cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)

def crop_roi(frame, x, y, w, h):
    return frame[y:y+h, x:x+w]

def preprocess_frame(frame_path):
    frame = load_frame(frame_path)
    frame = resize_frame(frame, width=640)
    blurred = apply_gaussian_blur(frame)
    hsv = convert_to_hsv(blurred)
    gray = convert_to_gray(blurred)
    
    return {
        "original": frame,
        "blurred": blurred,
        "hsv": hsv,
        "gray": gray
    }

if __name__ == "__main__":
    FRAMES_DIR = r"C:\Users\sankr\Videos\IVP\IVP_Project\data\frames\match_01"
    
    test_frame = os.path.join(FRAMES_DIR, "frame_00001.jpg")
    result = preprocess_frame(test_frame)
    
    print(f"Original shape : {result['original'].shape}")
    print(f"HSV shape      : {result['hsv'].shape}")
    print(f"Gray shape     : {result['gray'].shape}")
    print("Preprocessing working correctly!")