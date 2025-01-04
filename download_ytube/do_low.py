import argparse
import os
import time
from urllib.error import HTTPError

from pytubefix import YouTube
from pytubefix.innertube import InnerTube
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

def download_youtube_video(url, output_path):
    try:
        yt = YouTube(url, use_oauth=False, allow_oauth_cache=True)
        yt.innertube = InnerTube(client='WEB')
        stream = yt.streams.get_highest_resolution()
        if stream:
            stream.download(output_path)
            print(f"Downloaded: {yt.title}")
        else:
            print("No suitable stream found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    output_path = os.path.expanduser("~/Downloads")
    # for testing
    # default_url = "https://youtu.be/3e1_XdqN3jg?si=TR8fYAeKcuEjueAf"
    # url = input(f"Enter the YouTube video URL: ") or default_url
    url = input(f"Enter the YouTube video URL: ")
    download_youtube_video(url, output_path)