import csv
import os

CSV_PATH = "/home/aloith/Data/Lectures/Projects/AI/TRUESIGHT_AI/data/annotations.csv"
IMAGES_DIR = "/home/aloith/Data/Lectures/Projects/AI/TRUESIGHT_AI/data/images"
LABELS_DIR = "/home/aloith/Data/Lectures/Projects/AI/TRUESIGHT_AI/data/labels"

os.makedirs(LABELS_DIR, exist_ok=True)

class_map = {
    "normal-action": 0,
    "suspicious-suspect": 1,
    "victim": 2,
    "weapon": 3,
    "luggage": 4 
}


with open(CSV_PATH, newline="") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        image_name = os.path.splitext(os.path.basename(row["image_path"]))[0]
        label_path = os.path.join(LABELS_DIR, f"{image_name}.txt")

        cls_id = class_map[row["class"]]

        line = f"{cls_id} {row['x_center']} {row['y_center']} {row['width']} {row['height']}"

        with open(label_path, "a") as f:
            f.write(line + "\n")

print(" CSV converted back to YOLO labels")
