# core/counter.py

class LineCounter:
    def __init__(self, line_y):
        self.line_y = line_y
        self.track_history = {}
        self.counted_ids = set()
        self.count = 0

    def update(self, track_id, center_y):
        prev_y = self.track_history.get(track_id)
        if prev_y is not None:
            crossed = (prev_y < self.line_y) != (center_y < self.line_y)
            if crossed and track_id not in self.counted_ids:
                self.count += 1
                self.counted_ids.add(track_id)
        self.track_history[track_id] = center_y