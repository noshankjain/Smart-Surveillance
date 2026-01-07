# backend/agents/behavior_agent.py
import redis
import json
import time
import sys
import os

# Import config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import *

# Connect to Redis
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
p = r.pubsub()
p.subscribe(CH_TRACKS)

# Memory for tracking duration (for loitering)
loiter_times = {}
LOITER_THRESHOLD = 5  # Seconds (Keep it short for testing)

print("🕵️ Behavior Agent Running... Waiting for data.")

for message in p.listen():
    if message['type'] != 'message':
        continue
    
    # Parse the tracking data
    tracks = json.loads(message['data'])
    current_ids = set()
    alerts = []

    for obj in tracks:
        tid = obj['id']
        current_ids.add(tid)
        
        # --- LOGIC 1: FALL DETECTION (Simple Aspect Ratio Check) ---
        bbox = obj['bbox'] # [x1, y1, x2, y2]
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        
        # If width is much larger than height, person might be lying down
        if width > height * 1.2:
            alerts.append({
                "id": tid,
                "type": "FALL DETECTED",
                "msg": f"Person {tid} has fallen!",
                "level": "critical",
                "timestamp": time.strftime("%H:%M:%S")
            })

        # --- LOGIC 2: LOITERING DETECTION ---
        if tid not in loiter_times:
            loiter_times[tid] = time.time()
        
        duration = time.time() - loiter_times[tid]
        
        if duration > LOITER_THRESHOLD:
            alerts.append({
                "id": tid,
                "type": "LOITERING",
                "msg": f"Person {tid} loitering for {int(duration)}s",
                "level": "warning",
                "timestamp": time.strftime("%H:%M:%S")
            })

    # Cleanup: Remove IDs that left the frame
    for old_id in list(loiter_times.keys()):
        if old_id not in current_ids:
            del loiter_times[old_id]

    # Publish Alerts if any generated
    if alerts:
        print(f"⚠️ Generated Alerts: {alerts}")
        r.publish(CH_ALERTS, json.dumps(alerts))