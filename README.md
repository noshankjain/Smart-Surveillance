# 🛡️ Smart Surveillance: Real-Time Collaborative Security System

**Smart Surveillance** is a modular, event-driven video analytics platform designed for intelligent monitoring. It uses multiple intelligent agents to detect, track, and analyze human behavior in real-time.

Built with **Python (YOLOv8 + DeepSORT)**, **Redis (Pub/Sub)**, and **React**, it transforms any standard camera feed into a smart security system capable of detecting anomalies like **loitering** and **falls**.

![Smart Surveillance Dashboard](https://via.placeholder.com/800x400?text=Project+Screenshot+Here)
*(Replace this link with a real screenshot of your dashboard after uploading)*

---

## 🚀 Key Features

* **Multi-Agent Architecture:** Decoupled "Vision" and "Behavior" agents communicating via Redis.
* **Real-Time Detection:** Uses **YOLOv8** for human detection and **DeepSORT** for persistent tracking across frames.
* **Behavior Analysis:** Automatically detects suspicious activities:
    * ⚠️ **Loitering:** Alerts if a person stays in the frame too long.
    * 🚨 **Fall Detection:** Identifies when a person falls based on bounding box aspect ratio.
* **Live Dashboard:** A high-performance **React** frontend displaying the live feed, tracking overlays, and instant alerts.
* **Camera Support:** Works with standard Webcams, CCTV (RTSP), and DroidCam.

---

## 🛠️ Tech Stack

* **Frontend:** React.js, HTML5 Canvas, WebSocket API
* **Backend:** Python 3.10+, FastAPI (WebSockets), Flask (Video Streaming)
* **AI/CV:** Ultralytics YOLOv8, DeepSORT, OpenCV
* **Data Broker:** Redis (Pub/Sub) for inter-process communication
* **Containerization:** Docker (for Redis)

---

## ⚙️ Prerequisites

Before running the project, ensure you have the following installed:

1.  **Python 3.8+**
2.  **Node.js & npm** (for the frontend)
3.  **Docker Desktop** (Recommended for running Redis) **OR** a local Redis server.

---

## 📦 Installation Guide

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/smart-surveillance.git](https://github.com/YOUR_USERNAME/smart-surveillance.git)
cd smart-surveillance

2. Setup Backend (Python)
Create a virtual environment and install dependencies.
# Windows
python -m venv venv
.\venv\Scripts\activate
# Mac/Linux
python3 -m venv venv
source venv/bin/activate
# Install Libraries
pip install -r backend/requirements.txt

3. Setup Frontend (React)
cd frontend
npm install
cd ..

4. Start Redis
If using Docker (easiest method):
docker run -d -p 6379:6379 --name redis-server redis

Camera Configuration (Webcam vs. DroidCam)
You can use either your built-in laptop webcam or a high-quality phone camera via DroidCam.
Option A: Using Laptop Webcam (Default)
Open backend/config.py.
Set VIDEO_SOURCE to 0 (zero).
python:
VIDEO_SOURCE = 0
Option B: Using DroidCam (Recommended)
This method connects your phone via WiFi for better quality and mobility.
Download the DroidCam app on your phone.
Ensure your phone and laptop are on the same WiFi.
Open the app and note the WiFi IP and Port (e.g., 192.168.1.9 and 4747).
Open backend/config.py and set the URL:
Python:
# Format: http://<IP>:<PORT>/video
VIDEO_SOURCE = "[http://192.168.1.9:4747/video](http://192.168.1.9:4747/video)"

How to Run the System
The system consists of independent components. You need to run them in separate terminal windows.

Terminal 1: Redis Database Ensure Redis is running:
docker start redis-server
Terminal 2: The Eye (Vision Agent) Captures video, detects people, and tracks them
# Activate venv first!
python backend/agents/vision_agent.py
Terminal 3: The Brain (Behavior Agent) Analyzes data for falls and loitering.
# Activate venv first!
python backend/agents/behavior_agent.py
Terminal 4: The Mouth (API Server) Bridges Redis data to the Frontend.
# Activate venv first!
uvicorn backend.api.server:app --reload --port 8000
Terminal 5: The Face (Frontend) Launches the Dashboard.
cd frontend
npm start
Open your browser at http://localhost:3000 to see Smart Surveillance in action!

⚠️ Troubleshooting
Error: "Redis Connection Refused"
Make sure your Docker container is running (docker ps).
Error: "Failed to read frame from camera"
If using DroidCam: Check if the IP address in config.py matches your phone's current IP.
If using Webcam: Ensure no other app (Zoom, Teams) is using the camera.
Frontend shows "Disconnected"
Ensure the API Server (Terminal 4) is running.

---

### **Part 2: How to Handle Code Changes (Webcam vs. DroidCam)**

You don't need to change the Python code logic manually every time. Modern OpenCV (`cv2`) is smart enough to handle both numbers (webcams) and strings (URLs) using the same function.

**Ensure your `backend/agents/vision_agent.py` capture line looks like this:**

```python
# backend/agents/vision_agent.py (around line 41)

# This single line handles both integer indices (0) and URL strings
cap = cv2.VideoCapture(VIDEO_SOURCE)

Then, simply change backend/config.py as described in the README:
For Webcam: VIDEO_SOURCE = 0
For DroidCam: VIDEO_SOURCE = "http://192.168.X.X:4747/video"
This makes it very easy for new users to switch without touching the core code.