from ultralytics import YOLO
import cv2
import os

# Paths
MODEL_PATH = "../models/dataset4_best.pt"  # change if needed
IMAGE_DIR = "../data/images"
OUTPUT_DIR = "../results"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load model
model = YOLO(MODEL_PATH)

# Run detection on each image
for img_name in os.listdir(IMAGE_DIR):
    img_path = os.path.join(IMAGE_DIR, img_name)
    if not img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue

    results = model(img_path)
    annotated_frame = results[0].plot()

    output_path = os.path.join(OUTPUT_DIR, img_name)
    cv2.imwrite(output_path, annotated_frame)

    print(f" Processed {img_name}")

print(" Detection completed. Results saved in /results")
