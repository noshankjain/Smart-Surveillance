# backend/config.py
import os

# --- REDIS SETTINGS ---
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

# --- COMMUNICATION CHANNELS ---
# The Vision Agent publishes to this channel
CH_TRACKS = "channel:tracks"    
# The Behavior Agent publishes to this channel
CH_ALERTS = "channel:alerts"    

# --- CAMERA SETTINGS ---
# Use 0 for your default Webcam.
# If you have an external USB camera, try 1.
# If you have a CCTV, put the RTSP URL here (e.g., "rtsp://user:pass@192.168.1.55...")
# Use the DroidCam WiFi URL
VIDEO_SOURCE = "http://192.168.1.9:4747/video"

# Resolution for processing (Lower = Faster)
FRAME_WIDTH = 640
FRAME_HEIGHT = 480