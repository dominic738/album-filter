import json
import requests
import re
import os


with open("albums.json", "r") as file:
    albums = json.load(file)


def extract_images(albums):
    
    for id, d in albums.items():

        url = d.get('image_url')
        if not url:
            continue

        artists = ", ".join(d['artists'])
        name = d['album_name']

        filename = f"{id}.jpg"

        path = os.path.join('album-art/', filename)

        if os.path.exists(path):
            continue 

        try:
            img_data = requests.get(url, timeout=10).content
            with open(path, "wb") as handler:
                handler.write(img_data)
            print(f"Downloaded {filename}!")
        except Exception as e:
            print(f"Failed {id}: {e}")


extract_images(albums)