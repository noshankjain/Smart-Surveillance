import React, { useEffect, useState, useRef } from 'react';
import './App.css';
import { FaExclamationTriangle, FaUserSecret, FaVideo, FaUsers } from 'react-icons/fa';

function App() {
  const [alerts, setAlerts] = useState([]);
  const [liveCount, setLiveCount] = useState(0); // Simplified state
  const canvasRef = useRef(null);
  
  // FIXED RESOLUTION (Must match Python)
  const VIDEO_WIDTH = 640; 
  const VIDEO_HEIGHT = 480;

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws");
    
    ws.onmessage = (event) => {
      const response = JSON.parse(event.data);
      if (response.type === "TRACKS") {
        const tracks = JSON.parse(response.payload);
        
        // Update Live Count Only
        setLiveCount(tracks.length);

        requestAnimationFrame(() => drawTracks(tracks));
      } else if (response.type === "ALERTS") {
        const newAlerts = JSON.parse(response.payload);
        setAlerts(prev => [...newAlerts, ...prev].slice(0, 50)); 
      }
    };
    return () => ws.close();
  }, []);

  const drawTracks = (tracks) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    tracks.forEach(track => {
      const [x1, y1, x2, y2] = track.bbox;
      const width = x2 - x1;
      const height = y2 - y1;

      // Professional Box Styling
      ctx.strokeStyle = '#00FF00';
      ctx.lineWidth = 2;
      ctx.strokeRect(x1, y1, width, height);

      // Semi-transparent background for ID
      ctx.fillStyle = 'rgba(0, 255, 0, 0.7)';
      ctx.fillRect(x1, y1 - 25, 80, 25);
      
      ctx.fillStyle = '#000000';
      ctx.font = 'bold 14px Segoe UI';
      ctx.fillText(`ID: ${track.id}`, x1 + 5, y1 - 7);
    });
  };

  return (
    <div className="dashboard">
      {/* 1. Header */}
      <header className="header">
        <div className="logo">
          <FaUserSecret size={24} /> 
          <span>Smart Surveillance</span>
        </div>
        <div className="status-badge live">
          <div className="pulse-dot"></div> SYSTEM LIVE
        </div>
      </header>
      
      {/* 2. Top Stats Bar (Now only 2 items) */}
      <div className="stats-container">
        <div className="stat-card">
          <div className="stat-icon-box"><FaUsers /></div>
          <div className="stat-info">
            <h2>{liveCount}</h2>
            <p>Live Persons</p>
          </div>
        </div>
        
        {/* Removed Total Visitors Card */}

        <div className="stat-card">
          <div className="stat-icon-box red"><FaVideo /></div>
          <div className="stat-info">
            <h2>CAM-01</h2>
            <p>Active Feed</p>
          </div>
        </div>
      </div>

      <div className="main-layout">
        
        {/* 3. Main Video Stage */}
        <div className="video-stage">
           <div className="stage-header">LIVE SURVEILLANCE FEED</div>
           
           <div className="video-frame" style={{width: VIDEO_WIDTH, height: VIDEO_HEIGHT}}>
              <img src="http://localhost:5000/video_feed" alt="Stream" className="video-layer" />
              <canvas ref={canvasRef} width={VIDEO_WIDTH} height={VIDEO_HEIGHT} className="canvas-layer" />
              
              <div className="corner c-tl"></div>
              <div className="corner c-tr"></div>
              <div className="corner c-bl"></div>
              <div className="corner c-br"></div>
           </div>
        </div>

        {/* 4. Alerts Sidebar */}
        <div className="sidebar">
          <div className="sidebar-header">
            <FaExclamationTriangle className="alert-icon"/> Security Alerts
          </div>
          <div className="alert-feed">
            {alerts.length === 0 ? (
              <div className="empty-state">System Secure. No threats detected.</div>
            ) : (
              alerts.map((alert, idx) => (
                <div key={idx} className={`alert-item ${alert.level}`}>
                  <div className="time">{alert.timestamp}</div>
                  <div className="title">{alert.type}</div>
                  <div className="desc">{alert.msg}</div>
                </div>
              ))
            )}
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;