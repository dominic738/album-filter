import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

load_dotenv()

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI")
    )
)

def get_all_playlist_tracks(sp, playlist_id):
    tracks = []
    offset = 0

    results = sp.playlist_items(
        playlist_id,
        additional_types=["track"],
        limit=100
    )

    while results:
        batch = results["items"]
        tracks.extend(batch)

        start = offset + 1
        end = offset + len(batch)
        print(f"got tracks {start} - {end}")

        offset += len(batch)
        results = sp.next(results) if results["next"] else None

    return tracks


def get_album_info(tracks):

    albums = {}

    for item in tracks:

        track = item['track']

        if track is None:
            continue

        album = track['album']
        album_id = album['id']

        if album_id in albums:
            continue

        albums[album_id] = {
            "album_name": album["name"],
            "artists": [a["name"] for a in album["artists"]],
            "image_url": album["images"][0]["url"] if album["images"] else None,
            "release_date": album["release_date"],
        }

    return albums



def main():


    good_songs_id = "3YSjPnz6QuHs5BOFh1z3zE"

    tracks = get_all_playlist_tracks(sp, good_songs_id)
    info = get_album_info(tracks)

    with open("albums.json", "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2)


if __name__ == "__main__":
    main()

