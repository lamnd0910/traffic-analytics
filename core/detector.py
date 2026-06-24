# core/detector.py
from dataclasses import dataclass
from ultralytics import YOLO


@dataclass
class Detection:
    track_id: int
    label: str
    box: tuple              # (x1, y1, x2, y2)

    @property
    def center_y(self):
        _, y1, _, y2 = self.box
        return (y1 + y2) // 2


class VehicleDetector:
    def __init__(self, model_path="yolo11s.pt", classes=(2, 3, 5, 7), conf=0.3):
        self.model = YOLO(model_path)
        self.classes = list(classes)
        self.conf = conf

    def detect(self, frame):
        results = self.model.track(frame, persist=True, classes=self.classes,
                                   conf=self.conf, agnostic_nms=True, verbose=False)
        detections = []
        for box in results[0].boxes:
            if box.id is None:
                continue
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            track_id = int(box.id[0])
            label = results[0].names[int(box.cls[0])]
            detections.append(Detection(track_id, label, (x1, y1, x2, y2)))
        return detections