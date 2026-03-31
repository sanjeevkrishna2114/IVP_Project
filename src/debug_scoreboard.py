import cv2
import os

FRAMES_DIR = r"C:\Users\sankr\Videos\IVP\IVP_Project\data\frames\match_01"
FRAME_PATH = os.path.join(FRAMES_DIR, "frame_00001.jpg")

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        frame_copy = param.copy()
        cv2.putText(frame_copy, f"x:{x} y:{y}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Find Coordinates", frame_copy)

frame = cv2.imread(FRAME_PATH)
frame = cv2.resize(frame, (640, 360))

cv2.imshow("Find Coordinates", frame)
cv2.setMouseCallback("Find Coordinates", mouse_callback, frame)

print("Hover over the white digit area")
print("Note down the coordinates")
print("Press Q to quit")

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()