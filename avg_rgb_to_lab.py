import os
import json
import numpy as np
from PIL import Image
import cv2 as cv
from skimage.color import rgb2lab

from pathlib import Path

album_dir = Path("album-art")

def get_average_rgb(image_path, size=(32, 32)):
    img = Image.open(image_path).convert("RGB").resize(size)
    img_np = np.array(img, dtype=np.float32)
    avg_rgb = img_np.mean(axis=(0, 1))
    return avg_rgb

album_colors = {}


for img_path in album_dir.iterdir():

    album_id = img_path.stem
    avg_rgb = get_average_rgb(img_path)


    lab = rgb2lab((avg_rgb / 255.0).reshape(1, 1, 3)).astype(np.float32)


    print(f"{img_path}, RGB: {avg_rgb}, LAB: {lab[0][0]}")

    album_colors[album_id] = {
        "file_path" : str(img_path),
        "avg_rgb" : list(map(float, avg_rgb)),
        "lab" : list(map(float, lab[0][0]))
    }


with open("album_colors.json", "w", encoding="utf-8") as f:
    json.dump(album_colors, f, indent=2)




