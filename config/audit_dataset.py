import os

LABELS_DIR = "/home/aloith/Data/Lectures/Projects/Datasets/Weapons.v2i.yolov8/train/labels"
MAX_CLASS_ID = 4

empty = 0
bad = 0
total = 0

for f in os.listdir(LABELS_DIR):
    if not f.endswith(".txt"):
        continue

    total += 1
    path = os.path.join(LABELS_DIR, f)

    with open(path) as file:
        lines = file.readlines()

        if not lines:
            empty += 1

        for line in lines:
            cls = int(line.split()[0])
            if cls > MAX_CLASS_ID:
                bad += 1

print("Total label files:", total)
print("Empty label files:", empty)
print("Invalid class IDs:", bad)
