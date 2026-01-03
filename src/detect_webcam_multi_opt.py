from ultralytics import YOLO
import cv2
import numpy as np
import time

# -------------------------------
# CONFIG
# -------------------------------
MODEL_PATHS = [
    "../models/dataset1_best.pt",  # luggage
    "../models/dataset2_best.pt",  # weapon
    "../models/dataset3_best.pt",  # victim
    "../models/dataset4_best.pt"   # suspect
]

MODEL_NAMES = ["Luggage", "Weapon", "Victim", "Suspect"]
COLORS = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255)]
CONF_THRESHOLD = 0.45
IOU_THRESHOLD = 0.4   # NMS IoU threshold
FRAME_SKIP = 1

# -------------------------------
# LOAD MODELS
# -------------------------------
models = [YOLO(path) for path in MODEL_PATHS]

# -------------------------------
# OPEN WEBCAM
# -------------------------------
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print(" Webcam not accessible")
    exit()

print(" TRUESIGHT AI Multi-Model + NMS Started — Press 'q' to quit")

frame_count = 0
prev_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % FRAME_SKIP != 0:
        continue

    all_boxes = []
    all_labels = []
    all_colors = []
    all_scores = []

    # -------------------------------
    # RUN MODELS
    # -------------------------------
    for idx, model in enumerate(models):
        results = model(frame, stream=True)
        for r in results:
            for box in r.boxes:
                conf = float(box.conf[0])
                if conf < CONF_THRESHOLD:
                    continue
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                all_boxes.append([x1, y1, x2, y2])
                all_scores.append(conf)
                all_labels.append(MODEL_NAMES[idx])
                all_colors.append(COLORS[idx])

    # -------------------------------
    # APPLY NMS
    # -------------------------------
    if len(all_boxes) > 0:
        boxes_np = np.array(all_boxes)
        scores_np = np.array(all_scores)
        indices = cv2.dnn.NMSBoxes(
            bboxes=boxes_np.tolist(),
            scores=scores_np.tolist(),
            score_threshold=CONF_THRESHOLD,
            nms_threshold=IOU_THRESHOLD
        )

        # DRAW FINAL BOXES
        for i in indices.flatten():
            x1, y1, x2, y2 = boxes_np[i]
            label = all_labels[i]
            color = all_colors[i]
            conf = scores_np[i]
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                frame,
                f"{label} {conf:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

    # -------------------------------
    # FPS DISPLAY
    # -------------------------------
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("TRUESIGHT AI - Multi Model Optimized + NMS", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
