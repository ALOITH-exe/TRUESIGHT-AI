from ultralytics import YOLO
import cv2

# Load trained model
MODEL_PATH = "../models/dataset2_best.pt"  # change if needed
model = YOLO(MODEL_PATH)

# Open webcam (0 = default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print(" Error: Webcam not accessible")
    exit()

print(" TRUESIGHT AI Webcam started. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print(" Failed to grab frame")
        break

    # Run YOLO inference
    results = model(frame, stream=True)

    for r in results:
        annotated_frame = r.plot()

        cv2.imshow("TRUESIGHT AI - Live Detection", annotated_frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print(" TRUESIGHT AI Webcam stopped.")