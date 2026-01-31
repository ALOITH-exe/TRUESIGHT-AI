import os
from collections import Counter

labels_path = '/home/aloith/Data/Lectures/Projects/Datasets/MasterDataset/labels'  # adjust path
all_labels = []

for file in os.listdir(labels_path):
    if file.endswith('.txt'):
        with open(os.path.join(labels_path, file)) as f:
            for line in f:
                cls_id = int(line.split()[0])
                all_labels.append(cls_id)

count = Counter(all_labels)
print("Class distribution:")
for cls_id, c in count.items():
    print(f"{cls_id}: {c}")
