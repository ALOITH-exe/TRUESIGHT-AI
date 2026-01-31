import os
import csv

DATASET_PATH = "/home/aloith/Data/Lectures/Projects/AI/Datasets/dataset4/train"
IMAGES_PATH = os.path.join(DATASET_PATH, "images")
LABELS_PATH = os.path.join(DATASET_PATH, "labels")

OUTPUT_CSV = "annotations.csv"

class_names = [
    "normal-action",
    "suspicious-suspect",
    "victim",
    "weapon",
    "luggage"      
]

with open(OUTPUT_CSV, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "image_path", "class", "x_center", "y_center", "width", "height"
    ])

    for label_file in os.listdir(LABELS_PATH):
        if not label_file.endswith(".txt"):
            continue

        image_file = label_file.replace(".txt", ".jpg")
        image_path = os.path.join("images", image_file)

        with open(os.path.join(LABELS_PATH, label_file)) as f:
            for line in f:
                values = line.strip().split()

                # YOLO detection = first 5 values
                if len(values) < 5:
                    continue

                cls, x, y, w, h = values[:5]

                writer.writerow([
                    image_path,
                    class_names[int(cls)],
                    x, y, w, h
                ])

print(" CSV created successfully:", OUTPUT_CSV)
