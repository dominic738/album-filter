import json
import numpy as np
from scipy.spatial import cKDTree
import cv2 as cv


def precompute_resized_albums(album_images, bw, bh):
    resized = {}
    for album_id, img in album_images.items():
        print(f"Resizing Img: {album_id}")
        resized[album_id] = cv.resize(
            img, (bw, bh), interpolation=cv.INTER_AREA
        )
    return resized

def album_mosaic(frame_rgb, tree, album_ids, resized_albums, grid=32):
    H, W, _ = frame_rgb.shape

    bh = H // grid
    bw = W // grid

    small = cv.resize(
        frame_rgb, (grid, grid), interpolation=cv.INTER_AREA
    ).astype(np.float32)

    output = np.zeros_like(frame_rgb)

    for i in range(grid):
        for j in range(grid):
            block_rgb = small[i, j]


            _, idx = tree.query(block_rgb)
            album_id = album_ids[idx]
            album = resized_albums[album_id]

            y0 = i * bh
            x0 = j * bw
            output[y0:y0+bh, x0:x0+bw] = album
    return output


def main():

    with open("album_colors.json", "r") as f:
        album_colors = json.load(f)

    album_ids = []
    palette = []

    for album_id, d in album_colors.items():
        album_ids.append(album_id)
        palette.append(d["avg_rgb"])

    palette = np.array(palette, dtype=np.float32)
    tree = cKDTree(palette)


    album_images = {}

    for album_id, d in album_colors.items():
    
        

        img = cv.imread(d["file_path"])

        if img is None:
            continue

        print(f"Loading Image From: {d["file_path"]}")

        img = img[..., ::-1] 
        album_images[album_id] = img



    capture = cv.VideoCapture(0)
    capture.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
    cv.namedWindow("Album Mosaic", cv.WINDOW_NORMAL)
    cv.resizeWindow("Album Mosaic", 1280, 1280)

    print("Starting Capture!")

    ret, frame = capture.read()
    H, W, _ = frame.shape

    grid = 48
    bh = H // grid
    bw = W // grid

    resized_albums = precompute_resized_albums(album_images, bw, bh)

    while True:
        ret, frame = capture.read()
        if not ret:
            break

        frame_rgb = frame[..., ::-1]

        mosaic = album_mosaic(
            frame_rgb,
            tree,
            album_ids,
            resized_albums,
            grid=48
        )

        cv.imshow("Album Mosaic", mosaic[..., ::-1])

        if cv.waitKey(1) & 0xFF == ord('q'):
            break




if __name__ == "__main__":
    main()