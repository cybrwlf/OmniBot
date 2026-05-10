import cv2
import requests
import numpy as np
import time
import os

# Configuration
BACKEND_URL = "http://localhost:8080"
# Path to your face PNGs relative to the app.py static root
FACE_ASSET_PATH = "/face/" 

def get_emotion():
    try:
        # Polling the backend for the current expression
        response = requests.get(f"{BACKEND_URL}/ping")
        if response.status_code == 200:
            # You can expand this to hit a specific /status endpoint later
            return "love" # Defaulting to love.png for your test
        return "neutral"
    except:
        return "disconnected"

def main():
    window_name = "OmniBot Face"
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    print("👀 OmniBot Face is watching...")

    while True:
        emotion = get_emotion()
        # Extension is uppercase because we saw .PNG in your logs earlier
        img_url = f"{BACKEND_URL}{FACE_ASSET_PATH}{emotion}.PNG"
        
        try:
            resp = requests.get(img_url)
            if resp.status_code == 200:
                # Convert the image bytes to a format OpenCV understands
                arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
                img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
                
                if img is not None:
                    cv2.imshow(window_name, img)
        except Exception as e:
            print(f"Error loading face: {e}")

        # Press 'q' to exit
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
