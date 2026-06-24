import cv2
import argparse
from core.detector import VehicleDetector
from core.counter import LineCounter
from video import annotator
parser = argparse.ArgumentParser(description="Phát hiện & vẽ box phương tiện trên video")
parser.add_argument("video", help="Đường dẫn tới file video đầu vào")
parser.add_argument("-o", "--output", default="output.mp4", help="Tên file video xuất ra")
args = parser.parse_args()


cap = cv2.VideoCapture(args.video)

if not cap.isOpened():
    print("Không thể mở camera/video")
else:
    # Sử dụng cap.get() để lấy thông tin
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    print(f"Độ phân giải video: {width} x {height}")
    print(f"Tốc độ khung hình (FPS): {fps}")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(args.output, fourcc, fps, (width, height))

    detector = VehicleDetector("yolo11s.pt")
    line_y = height // 2          # vị trí vạch (thử giữa khung trước, chỉnh sau)
    counter = LineCounter(line_y)                    # tổng số xe đã qua vạch

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detections = detector.detect(frame)
        for det in detections:
            counter.update(det.track_id, det.center_y)
            annotator.draw_detection(frame, det)

        annotator.draw_line(frame, line_y, width)
        annotator.draw_count(frame, counter.count)

        writer.write(frame)
        cv2.imshow("Detect", frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        # người dùng bấm nút X để đóng cửa sổ
        if cv2.getWindowProperty("Detect", cv2.WND_PROP_VISIBLE) < 1:
            break
# Nhớ giải phóng bộ nhớ sau khi dùng xong
cap.release()
writer.release()
cv2.destroyAllWindows()
