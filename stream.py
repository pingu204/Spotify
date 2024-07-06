import json
import os
from datetime import datetime
from image import generate_list
from key import *

class Track():
    title:str
    artist:str
    streams:int
    seconds:int

    def __init__(self, title, artist, seconds):
        self.title = title
        self.artist = artist
        self.seconds = seconds
        self.streams = 1

if __name__ == "__main__":
    print("hello!")
    # get filenames
    file_names = [f for f in os.listdir("Files/2024") if os.path.isfile(f"Files/2024/{f}")]
    
    # initialize records
    artists = {}
    songs = {}

    for dir in file_names:
        with open(f'Files/2024/{dir}', encoding='utf8') as json_file:
            # load JSON from file
            data = json.load(json_file)
            
            for song in data:
                # fields
                title = song["trackName"]
                artist = song["artistName"]
                seconds = int(song["msPlayed"]/1000)
                year = datetime.strptime(song["endTime"], "%Y-%m-%d %H:%M").year
                
                if year == 2024: # filter
                    if title not in songs.keys():
                        songs[title] = Track(title, artist, seconds if seconds >= 30 else 0)
                    else:
                        songs[title].seconds += seconds if seconds >= 30 else 0
                        songs[title].streams += 1 if seconds >= 30 else 0

                    if artist not in artists.keys():
                        artists[artist] = 1
                    else:
                        artists[artist] += 1 if seconds >= 30 else 0

    sorted_songs = sorted(songs.values(), key=get_seconds, reverse=True)
    sorted_artists = sorted([(artist,streams) for artist,streams in artists.items()], key=get_count, reverse=True)

    generate_list(sorted_songs)

    print("Top Artist [2024]")
    for n in range(20):
        (artist, streams) = sorted_artists[n]
        top_songs = []
        for song in sorted_songs:
            if song.artist == artist:
                top_songs.append(song)

        print(f"{n+1}. {artist} [Streamed {streams} times]")
        for i in range(10 if len(top_songs) >= 10 else len(top_songs)):
            print(f"\t({i+1}) {top_songs[i].title}")
