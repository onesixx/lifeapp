import argparse
import os
import time
from urllib.error import HTTPError

from pytubefix import YouTube
from pytubefix.innertube import InnerTube
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

def download_youtube_video(url, title, output_path):
    try:
        yt = YouTube(url, use_oauth=False, allow_oauth_cache=True)
        yt.innertube = InnerTube(client='WEB')
        stream = yt.streams.get_highest_resolution()
        if stream:
            stream.download(output_path, filename=f"{title}.mp4")
            print(f"Downloaded: {yt.title} <=== {title}")
        else:
            print("No suitable stream found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # default_url = "https://youtu.be/wf0D82bBsJY"  # for testing
    # url = input(f"Enter the YouTube video URL: ") or default_url
    # download_youtube_video(url, os.path.expanduser("~/Downloads"))

    bulk_urls = [
        "https://youtu.be/wf0D82bBsJY",  #
        "https://youtu.be/GXFznjMiCw8",
        "https://youtu.be/1co4xCV-nTI",
        "https://youtu.be/Y8tQRMe-jV8",
        "https://youtu.be/u43X5lpQg4Q",
        "https://youtu.be/nCJVSSWjwv4",
        "https://youtu.be/nw7sCDHZaZQ",
        "https://youtu.be/KdKvUb_xIiU",
        "https://youtu.be/O_haUyEJDXw",
        "https://youtu.be/5mUDxY0GkGQ",
        "https://youtu.be/IydMr5pcN4w",
        "https://youtu.be/y7DrTcWEgD0",
        "https://youtu.be/DfltqlAl7KI",
        "https://youtu.be/2dSdD4ubFEs",
        "https://youtu.be/RcdlKXzitwE",
        "https://youtu.be/DtRLgLYiTkI",
        "https://youtu.be/XN8Vf9IREwA",
        "https://youtu.be/vkWQrLzQ5DA",
        "https://youtu.be/7vQV8XajHCc"
    ]
    titles =[
        "01.wimpy_Diary of a Wimpy Kid (2007)",
        "02.wimpy_Rodrick Rules (2008)",
        "03.wimpy_The Last Straw (2009)",
        "04.wimpy_Dog Days (2009)",
        "05.wimpy_The Ugly Truth (2010)",
        "06.wimpy_Cabin Fever (2011)",
        "07.wimpy_The Third Wheel (2012)",
        "08.wimpy_Hard Luck (2013)",
        "09.wimpy_The Long Haul (2014)",
        "10.wimpy_Old School (2015)",
        "11.wimpy_Double Down (2016)",
        "12.wimpy_The Getaway (2017)",
        "13.wimpy_The Meltdown (2018)",
        "14.wimpy_Wrecking Ball (2019)",
        "15.wimpy_The Deep End (2020)",
        "16.wimpy_Big Shot (2021)",
        "17.wimpy_Diper Överlöde (2022)",
        "18.wimpy_No Brainer (2023)",
        "19.wimpy_Hot Mess (2024)378",
    ]
    for url, title in zip(bulk_urls, titles):
        download_youtube_video(url, title, os.path.expanduser("~/Downloads"))
