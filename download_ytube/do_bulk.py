import os
from urllib.error import HTTPError

from pytubefix import YouTube
from pytubefix.innertube import InnerTube
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

def download_youtube_video(url, title, output_path):
    try:
        yt = YouTube(url, use_oauth=False, allow_oauth_cache=True)
        yt.innertube = InnerTube(client='WEB')

        video_streams = yt.streams.filter(mime_type="video/mp4", adaptive=True)
        streams_high_res = []
        for stream in video_streams:
            if stream.resolution and int(stream.resolution[:-1]) >= 720:
                streams_high_res.append(stream)

        print(f"Info: H.264(avc1.4d401f)은 (구)장비호환이 좋고, AV1(av01.0.05M.08)은 더 좋은 화질을 제공할 가능성이 높습니다.")
        for i, stream in enumerate(streams_high_res):
            stream_info = str(stream).replace(f"itag=\"{stream.itag}\" ", "").replace(f"type=\"{stream.type}\" ", "")
            print(f" {i} :: {stream_info}")

        s = input('Press number key to select video index: ')
        selected_stream = streams_high_res[int(s)]

        if selected_stream.is_progressive:
            print("Downloading progressive stream")
            selected_stream.download(output_path)
            print(f"Downloaded: {yt.title}")
        else:
            print("==> Downloading adaptive streams and merging")
            audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by('abr').desc().first()

            video_file = selected_stream.download(output_path=output_path, filename='video.mp4')
            audio_file = audio_stream.download(output_path=output_path, filename='audio.mp4')

            # Merge video and audio
            video_clip = VideoFileClip(video_file)
            audio_clip = AudioFileClip(audio_file)
            final_clip = video_clip.with_audio(audio_clip)
            # final_clip.write_videofile(os.path.join(output_path, f"{yt.title}.mp4"), codec='libx264')
            final_clip.write_videofile(os.path.join(output_path, f"{title}.mp4"), codec='libx264')

            # Clean up temporary files
            video_clip.close()
            audio_clip.close()
            os.remove(video_file)
            os.remove(audio_file)
            print(f"Downloaded and merged: {yt.title} <===")
    except HTTPError as e:
        if e.code == 403:
            print("HTTP Error 403: Forbidden. Retrying with different client...")
        else:
            print(f"HTTP Error: {e}")

if __name__ == "__main__":
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