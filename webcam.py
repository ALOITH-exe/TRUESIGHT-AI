from ultralytics import YOLO
import cv2
import time
import threading
import pygame

# ================= CONFIG =================
MODEL_PATH = "models/best.pt"
CONF_THRESHOLD = 0.35
IOU_THRESHOLD = 0.5
ALARM_COOLDOWN = 3  # seconds
ALARM_SOUND = "assets/alarm.wav"

CLASS_NAMES = [
    "normal-action",
    "suspicious-suspect",
    "victim",
    "weapon",
    "luggage"
]

COLORS = {
    "normal-action": (0, 255, 0),
    "suspicious-suspect": (0, 0, 255),
    "victim": (255, 0, 0),
    "weapon": (0, 255, 255),
    "luggage": (255, 0, 255)
}

HIGH_RISK_CLASSES = ["weapon", "suspicious-suspect"]

# ================= AUDIO INIT =================
pygame.mixer.init()
alarm_sound = pygame.mixer.Sound(ALARM_SOUND)
alarm_sound.set_volume(0.8)

last_alarm_time = 0

def trigger_alarm():
    global last_alarm_time
    now = time.time()
    if now - last_alarm_time > ALARM_COOLDOWN:
        last_alarm_time = now
        alarm_sound.play()

# ================= LOAD MODEL =================
model = YOLO(MODEL_PATH)

# ================= WEBCAM =================
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

if not cap.isOpened():
    print(" Could not open webcam")
    exit()

prev_time = 0

# ================= MAIN LOOP =================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(
        frame,
        conf=CONF_THRESHOLD,
        iou=IOU_THRESHOLD,
        verbose=False,
        device="cpu"
    )

    threat_detected = False

    for result in results:
        if result.boxes is None:
            continue

        for box in result.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = CLASS_NAMES[cls_id]

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            color = COLORS[label]
            thickness = 4 if label in HIGH_RISK_CLASSES else 2

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
            cv2.putText(
                frame,
                f"{label} {conf:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

            if label in HIGH_RISK_CLASSES:
                threat_detected = True

    # ================= ALERT =================
    if threat_detected:
        trigger_alarm()
        cv2.putText(
            frame,
            " THREAT DETECTED",
            (frame.shape[1] // 2 - 220, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 0, 255),
            3
        )

    # ================= FPS =================
    curr_time = time.time()
    fps = int(1 / (curr_time - prev_time)) if prev_time else 0
    prev_time = curr_time

    cv2.putText(
        frame,
        f"FPS: {fps}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    # ================= DISPLAY =================
    cv2.imshow("TRUESIGHT AI | Live Surveillance", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ================= CLEANUP =================
cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
