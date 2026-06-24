# backend/server.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import time
from fastapi.responses import StreamingResponse
from backend.worker import start_worker
from backend.state import state
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from storage import db
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

VIDEO_PATH = "data/samples/Traffic IP Camera video [Gr0HpDM8Ki8].mp4"


@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <h1>Traffic Analytics 🚦</h1>
    <p id="count" style="font-size:24px; font-weight:bold;">Count: --</p>
    <img src="/video_feed" width="800">
    <script>
      const ws = new WebSocket("ws://127.0.0.1:8000/ws/stats");
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        document.getElementById("count").innerText = "Count: " + data.count;
      };
    </script>
    """


@app.get("/status")
def status():
    frame, count = state.read()
    return {"count": count, "has_frame": frame is not None}

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(
        mjpeg_generator(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )

@app.websocket("/ws/stats")
async def stats_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            _, count = state.read()
            await websocket.send_json({"count": count})
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        pass

@app.get("/stats/history")
def stats_history():
    rows = db.get_counts_per_minute()
    return [{"minute": minute, "count": count} for minute, count in rows]

def mjpeg_generator():
    while True:
        frame, _ = state.read()
        if frame is None:
            time.sleep(0.05)
            continue
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
        time.sleep(0.03)

if __name__ == "__main__":
    start_worker(VIDEO_PATH)
    uvicorn.run(app, host="127.0.0.1", port=8000)