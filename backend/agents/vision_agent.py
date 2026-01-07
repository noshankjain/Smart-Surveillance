# backend/agents/vision_agent.py
import cv2
import json
import redis
import threading
import sys
import os
import time
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from flask import Flask, Response

# --- SETUP PATH TO IMPORT CONFIG ---
# This line allows us to import config.py from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import *

# --- INITIALIZE ---
# 1. Connect to Redis
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# 2. Load AI Models
print("🧠 Loading YOLOv8 Model (this might take a moment)...")
model = YOLO('yolov8n.pt') 
tracker = DeepSort(max_age=30, n_init=3)

# 3. Web Stream Setup
app = Flask(__name__)
output_frame = None
lock = threading.Lock()

def process_video():
    """
    Main loop: Captures video, runs AI, publishes to Redis.
    """
    global output_frame, lock

    # Standard capture for Network/WiFi cameras
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    
    # Set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    print(f"📷 Vision Agent Started. Source: {VIDEO_SOURCE}")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to read frame from camera. Exiting...")
            break

        # --- A. DETECTION (YOLO) ---
        # Run YOLO on the frame. stream=True is faster.
        results = model(frame, stream=True, verbose=False)
        
        detections = []
        for result in results:
            for box in result.boxes:
                # Get box coordinates
                x1, y1, x2, y2 = box.xyxy[0]
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                
                # Class 0 = Person. We only care about people.
                if cls == 0 and conf > 0.5:
                    w = x2 - x1
                    h = y2 - y1
                    # DeepSORT expects [left, top, w, h]
                    detections.append(([float(x1), float(y1), float(w), float(h)], conf, "Person"))

        # --- B. TRACKING (DeepSORT) ---
        tracks = tracker.update_tracks(detections, frame=frame)
        
        track_payload = []
        
        for track in tracks:
            if not track.is_confirmed(): continue
            
            track_id = track.track_id
            ltrb = track.to_ltrb() # Left, Top, Right, Bottom
            
            # Save data to send to Redis
            track_payload.append({
                "id": track_id,
                "bbox": [float(x) for x in ltrb]
            })

            # Draw generic box on the stream (Visualization)
            cv2.rectangle(frame, (int(ltrb[0]), int(ltrb[1])), (int(ltrb[2]), int(ltrb[3])), (0, 255, 0), 2)
            cv2.putText(frame, f"ID: {track_id}", (int(ltrb[0]), int(ltrb[1])-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # --- C. PUBLISH TO REDIS ---
        # Only publish if we found people
        if track_payload:
            message = json.dumps(track_payload)
            r.publish(CH_TRACKS, message)
            # print(f"📤 Published: {message}") # Uncomment to debug

        # Update global frame for the web stream
        with lock:
            output_frame = frame.copy()
        
        # Small sleep to prevent CPU overheating
        time.sleep(0.01)

    cap.release()

def generate_mjpeg():
    """Generates the video stream for the browser."""
    global output_frame, lock
    while True:
        with lock:
            if output_frame is None: continue
            (flag, encodedImage) = cv2.imencode(".jpg", output_frame)
            if not flag: continue
        
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
              bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
    return Response(generate_mjpeg(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
    # Start the Video Processing in a separate background thread
    t = threading.Thread(target=process_video)
    t.daemon = True
    t.start()
    
    # Start the Web Server
    print("🚀 Streaming at http://localhost:5000/video_feed")
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)