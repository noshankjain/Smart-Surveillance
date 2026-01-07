# 🛡️ Smart Surveillance – Real-Time Collaborative Security System

**Smart Surveillance** is a modular, event-driven video analytics platform designed for intelligent monitoring.  
It uses multiple intelligent agents to detect, track, and analyze human behavior in real time.

Built using **YOLOv8 + DeepSORT**, **Redis Pub/Sub**, and a **React live dashboard**, it converts any camera feed into a smart security system capable of detecting **loitering** and **falls**.

---

## 🚀 Key Features

- **Multi-Agent Architecture**  
  Decoupled Vision and Behavior agents communicate using Redis.

- **Real-Time Detection**  
  YOLOv8 for person detection, DeepSORT for persistent tracking.

- **Behavior Analysis**
  - ⚠️ Loitering detection  
  - 🚨 Fall detection using bounding-box posture analysis

- **Live Dashboard**
  React frontend displaying live feed, bounding boxes and alerts.

- **Camera Support**
  Works with Laptop Webcam, CCTV RTSP streams, and **DroidCam phone camera**.

---

## 🛠️ Tech Stack

| Layer      | Technology                              |
|------------|------------------------------------------|
| Frontend   | React.js, HTML5 Canvas, WebSockets       |
| Backend    | Python, FastAPI, Flask                  |
| AI / CV    | Ultralytics YOLOv8, DeepSORT, OpenCV     |
| Broker     | Redis (Pub/Sub)                          |
| Database   | Redis                                   |
| Deployment | Docker (Redis Container)                |

---

## ⚙️ Prerequisites

- Python 3.8+
- Node.js & npm
- Docker Desktop (for Redis)
- DroidCam App (optional – for phone camera)

---

## 📦 Installation

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/smart-surveillance.git
cd smart-surveillance
```

---

### 2. Setup Backend
```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac

pip install -r backend/requirements.txt
```

---

### 3. Setup Frontend
```bash
cd frontend
npm install
cd ..
```

---

### 4. Start Redis (Docker)
```bash
docker run -d -p 6379:6379 --name redis-server redis
```

---

## 📷 Camera Configuration

Open `backend/config.py`

### Laptop Webcam
```python
VIDEO_SOURCE = 0
```

### DroidCam Phone Camera
1. Install DroidCam on phone
2. Connect phone & laptop to same WiFi
3. Get phone IP and port from DroidCam app

```python
VIDEO_SOURCE = "http://192.168.1.9:4747/video"
```

---

## ▶️ Running the System

Open **five terminals**.

### Terminal 1 – Redis
```bash
docker start redis-server
```

### Terminal 2 – Vision Agent
```bash
python backend/agents/vision_agent.py
```

### Terminal 3 – Behavior Agent
```bash
python backend/agents/behavior_agent.py
```

### Terminal 4 – API Server
```bash
uvicorn backend.api.server:app --reload --port 8000
```

### Terminal 5 – Frontend
```bash
cd frontend
npm start
```

Open browser at  
👉 `http://localhost:3000`

---

## ⚠️ Troubleshooting

| Error | Fix |
|------|-----|
| Redis connection refused | Run `docker start redis-server` |
| Failed to read frame | Check camera IP or close other camera apps |
| Frontend disconnected | Ensure API server is running |

---

## 🔄 Switching Cameras Easily

OpenCV supports both webcam index and URL.

In `vision_agent.py`:

```python
cap = cv2.VideoCapture(VIDEO_SOURCE)
```

Now you only change `VIDEO_SOURCE` in `config.py`.

| Camera Type | Config Value |
|------------|--------------|
| Laptop Webcam | `0` |
| DroidCam | `"http://192.168.X.X:4747/video"` |
