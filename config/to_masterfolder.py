import shutil
import os
import uuid

SRC_IMAGES = "/home/aloith/Data/Lectures/Projects/Datasets/Weapons.v2i.yolov8/train/images"
SRC_LABELS = "/home/aloith/Data/Lectures/Projects/Datasets/Weapons.v2i.yolov8/train/labels"

DST_IMAGES = "/home/aloith/Data/Lectures/Projects/Datasets/MasterDataset/images"
DST_LABELS = "/home/aloith/Data/Lectures/Projects/Datasets/MasterDataset/labels"

os.makedirs(DST_IMAGES, exist_ok=True)
os.makedirs(DST_LABELS, exist_ok=True)

for img in os.listdir(SRC_IMAGES):
    uid = uuid.uuid4().hex
    ext = os.path.splitext(img)[1]

    new_img = f"{uid}{ext}"
    new_lbl = f"{uid}.txt"

    shutil.copy(
        os.path.join(SRC_IMAGES, img),
        os.path.join(DST_IMAGES, new_img)
    )

    shutil.copy(
        os.path.join(SRC_LABELS, img.replace(ext, ".txt")),
        os.path.join(DST_LABELS, new_lbl)
    )
