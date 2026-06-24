import threading
import cv2
from storage import db
from core.detector import VehicleDetector
from core.counter import LineCounter
from video import annotator
from backend.state import state

def run_pipeline(video_path):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    detector = VehicleDetector("yolo11s.pt")
    line_y = height // 2
    counter = LineCounter(line_y)
    db.init_db() 


    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)   # hết video -> tua về đầu, phát lại
            continue

        detections = detector.detect(frame)
        for det in detections:
            counted = counter.update(det.track_id, det.center_y)
            if counted: 
                db.record_crossing(det.label)
            annotator.draw_detection(frame, det)

        annotator.draw_line(frame, line_y, width)
        annotator.draw_count(frame, counter.count)

        ok, buffer = cv2.imencode(".jpg", frame)   # khung -> JPEG bytes
        if ok:
            state.update(buffer.tobytes(), counter.count)


def start_worker(video_path):
    t = threading.Thread(target=run_pipeline, args=(video_path,), daemon=True)
    t.start()