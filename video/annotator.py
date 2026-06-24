# video/annotator.py
import cv2


def draw_detection(frame, det):
    x1, y1, x2, y2 = det.box
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(frame, f"{det.label} #{det.track_id}", (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)


def draw_line(frame, line_y, width):
    cv2.line(frame, (0, line_y), (width, line_y), (0, 0, 255), 2)


def draw_count(frame, count):
    cv2.putText(frame, f"Count: {count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)