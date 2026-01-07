# backend/api/server.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as redis
import asyncio
import sys
import os

# Import config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import *

app = FastAPI()

# Allow React to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ Client connected to WebSocket")
    
    # Connect to Redis asynchronously
    r = redis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
    pubsub = r.pubsub()
    await pubsub.subscribe(CH_TRACKS, CH_ALERTS)

    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                channel = message['channel'].decode('utf-8')
                data = message['data'].decode('utf-8')
                
                # Tag the message type so Frontend knows how to handle it
                msg_type = "TRACKS" if channel == CH_TRACKS else "ALERTS"
                
                await websocket.send_json({
                    "type": msg_type,
                    "payload": data
                })
    except WebSocketDisconnect:
        print("❌ Client Disconnected")
    finally:
        await r.close()