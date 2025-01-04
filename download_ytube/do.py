import os
from urllib.error import HTTPError

from pytubefix import YouTube
from pytubefix.innertube import InnerTube
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

def download_youtube_video(url, output_path):
    try:
        yt = YouTube(url, use_oauth=False, allow_oauth_cache=True)
        yt.innertube = InnerTube(client='WEB')

        video_streams = yt.streams.filter(mime_type="video/mp4", adaptive=True)
        streams_high_res = []
        for stream in video_streams:
            if stream.resolution and int(stream.resolution[:-1]) >= 720:
                streams_high_res.append(stream)

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
            final_clip.write_videofile(os.path.join(output_path, f"{yt.title}.mp4"), codec='libx264')
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
    # for testing
    default_url = "https://youtu.be/3e1_XdqN3jg?si=TR8fYAeKcuEjueAf"
    url = input(f"Enter the YouTube video URL: ") or default_url

    #url = input(f"Enter the YouTube video URL: ")
    download_youtube_video(url, os.path.expanduser("~/Downloads"))