import cv2
from ultralytics import YOLO
import argparse

parser = argparse.ArgumentParser(description="Phát hiện & vẽ box phương tiện trên video")
parser.add_argument("video", help="Đường dẫn tới file video đầu vào")
parser.add_argument("-o", "--output", default="output.mp4", help="Tên file video xuất ra")
args = parser.parse_args()

model = YOLO("yolo11n.pt")

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

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.track(frame, persist=True, classes=[2, 3, 5, 7], verbose=False)

        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls_id = int(box.cls[0])
            label = results[0].names[cls_id]

            if box.id is None:
                continue
            track_id = int(box.id[0])

            cv2.rectangle(frame, (x1, y1) , (x2, y2), (0, 255, 0), 3)
            text = f"{label} #{track_id}"
            cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

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
