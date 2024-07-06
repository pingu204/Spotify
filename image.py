import os
from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from PIL import Image, ImageDraw, ImageFont
import image
import urllib.request 

# client secrets
load_dotenv()
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

# connect to Spotify API
auth_manager = SpotifyClientCredentials(client_id = SPOTIPY_CLIENT_ID, client_secret = SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (100,100,100)

# fonts
PRODUCT_SANS_BLACK = "Fonts/ProductSans-Black.ttf"
PRODUCT_SANS_BOLD = "Fonts/ProductSans-Bold.ttf"
PRODUCT_SANS_MEDIUM = "Fonts/ProductSans-Medium.ttf"
PRODUCT_SANS_REGULAR = "Fonts/ProductSans-Regular.ttf"
PRODUCT_SANS_THIN = "Fonts/ProductSans-Thin.ttf"

def add_text(img, text, font, topleft, size, color):
    font = ImageFont.truetype(font, size=size)
    draw = ImageDraw.Draw(img)
    draw.text(topleft, text, font=font, fill=color)
    return img

def get_album_cover(artist_name, song):
    results = sp.search(q=f"artist:{artist_name}", type="artist")
    artist = results["artists"]["items"][0] if len(results) > 0 else results

    albums = []
    query = sp.artist_albums(artist["id"])
    albums.extend(query["items"])
    while query["next"]:
        query = sp.next(query)
        albums.extend(query["items"])

    for album in albums:
        if song in [s["name"] for s in sp.album_tracks(album["id"])["items"]]:
            return album["images"][0]["url"]

def convert_time(seconds):
    hours = int(seconds/3600)
    mins = int((seconds%3600)/60)

    return f'{hours} hours, {mins} mins'

def generate_list(sorted_list):
    with Image.open("Images/blank.png") as img:
        # title
        img = add_text(img, "Jopeth's", PRODUCT_SANS_BLACK, (291,273), 100, BLACK)
        
        # subtitle
        img = add_text(img, "2024 Hits", PRODUCT_SANS_BLACK, (291,350), 240, BLACK)

        for i in range(10):
            song = sorted_list[i]

            # column and row offsets
            offset_x = (i>=5)*1250
            offset_y = (i%5)*250

            # rank
            img = add_text(
                img = img, 
                text = f"{str(i+1).zfill(2)}", 
                font = PRODUCT_SANS_MEDIUM,
                topleft = (291 + offset_x, 788 + offset_y),
                size = 50,
                color = GRAY
                )
            
            # song title
            img = add_text(
                img = img,
                text = song.title[:25] + ("..." if len(song.title) > 25 else ""),
                font = PRODUCT_SANS_BOLD, 
                topleft = (650 + offset_x, (770 if len(song.title)<17 else 785) + offset_y), 
                size = 80 if len(song.title)<17 else 60,
                color = BLACK
                )

            # artist name
            img = add_text(
                img = img, 
                text = song.artist.upper(),
                font = PRODUCT_SANS_BOLD,
                topleft = (650 + offset_x, (750 if len(song.title)<17 else 765) + offset_y),
                size = 25,
                color = BLACK
                )

            # duration
            img = add_text(
                img = img,
                text = f"{convert_time(song.seconds)}",
                font = PRODUCT_SANS_MEDIUM,
                topleft = (650 + offset_x, 868 + offset_y),
                size = 40,
                color = BLACK
                )
            
            # cover image
            urllib.request.urlretrieve(get_album_cover(song.artist, song.title),"Images/cover.png")
            cover = Image.open("Images/cover.png")
            cover = cover.resize((180,180))
            img.paste(cover, (425 + offset_x, 740 + offset_y))
            os.remove("Images/cover.png")

        img.save("Images/saved.png")