import os

# ===== CONFIG =====
LABELS_DIR = "/home/aloith/Data/Lectures/Projects/Datasets/Weapons.v2i.yolov8/train/labels"   # path to current dataset labels
CLASS_ID_MAP = {
    0: 3,
    1: 3
}
# ==================

for file in os.listdir(LABELS_DIR):
    if not file.endswith(".txt"):
        continue

    path = os.path.join(LABELS_DIR, file)
    new_lines = []

    with open(path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 5:
                continue

            old_id = int(parts[0])

            if old_id not in CLASS_ID_MAP:
                continue  # skip unknown classes safely

            new_id = CLASS_ID_MAP[old_id]
            new_line = " ".join([str(new_id)] + parts[1:])
            new_lines.append(new_line)

    with open(path, "w") as f:
        f.write("\n".join(new_lines))
