from ultralytics import YOLO
import os

MODEL_PATH = "models/best.pt"
SOURCE = "data/test"

BASE_DIR = "/home/aloith/Data/Lectures/Projects/TRUESIGHT_AI"
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
RUN_NAME = "detections"

model = YOLO(MODEL_PATH)

os.makedirs(OUTPUT_DIR, exist_ok=True)

results = model.predict(
    source=SOURCE,
    conf=0.25,
    save=True,
    project=OUTPUT_DIR,   # absolute path
    name=RUN_NAME,
    exist_ok=True
)

print(f"Detection complete. Check {OUTPUT_DIR}/{RUN_NAME}/")
