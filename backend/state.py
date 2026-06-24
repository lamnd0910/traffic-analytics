# backend/state.py
import threading


class SharedState:
    def __init__(self):
        self._lock = threading.Lock()
        self.frame = None     # khung hình JPEG mới nhất (dạng bytes)
        self.count = 0        # số xe đã đếm

    def update(self, frame_bytes, count):
        with self._lock:
            self.frame = frame_bytes
            self.count = count

    def read(self):
        with self._lock:
            return self.frame, self.count


# một thể hiện dùng chung cho cả app
state = SharedState()