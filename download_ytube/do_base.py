import argparse
import os

from pytubefix import YouTube
from pytubefix.innertube import InnerTube
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

x= ""
# x= "test"

parser = argparse.ArgumentParser(description="Download youtube")
parser.add_argument("-u", "--url", help="URL of youtube")  #  required=True,
if x == "test":
    testurl = "https://youtu.be/3e1_XdqN3jg?si=TR8fYAeKcuEjueAf"
    #testurl = "https://youtu.be/3e1_XdqN3jg"
    args = parser.parse_args(["-u", testurl])
else:
    args = parser.parse_args()

yt = YouTube(args.url, use_oauth=False, allow_oauth_cache=True)
yt.innertube = InnerTube(client='WEB')

streamList = yt.streams.filter(mime_type="video/mp4")
# stream = streamList.get_highest_resolution()
# stream = streamsList.filter(progressive=True).order_by('resolution').last()
streams_high_res = []
for stream in streamList:
    # print(f"stream: {stream}")
    if stream.resolution and int(stream.resolution[:-1]) >= 720:
        streams_high_res.append(stream)

for i, stream in enumerate(streams_high_res):
    #print(f" {i} :: {stream}")
    stream_info = str(stream).replace(f"itag=\"{stream.itag}\" ", "").replace(f"type=\"{stream.type}\"", "").replace(f"mime_type=\"{stream.mime_type}\" ", "")
    print(f" {i} :: {stream_info}")

s = input('press number key to select video index :  ')
final_video_stream = streams_high_res[int(s)]


output_path = os.path.expanduser("~/Downloads")
if final_video_stream.is_progressive:
    print("Downloading progressive stream")
    streams_high_res[int(s)].download(output_path)
    print(f"Downloaded: {yt.title}")
    exit()
else:
    audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by('abr').desc().first()
    video_file = final_video_stream.download(output_path=output_path, filename='video.mp4')
    audio_file = audio_stream.download(output_path=output_path, filename='audio.mp4')
    # Merge video and audio
    video_clip = VideoFileClip(video_file)
    audio_clip = AudioFileClip(audio_file)
    final_clip = video_clip.with_audio(audio_clip)
    final_clip.write_videofile(
        os.path.join(output_path, f"{yt.title}.mp4"), codec='libx264')

    # Clean up temporary files
    video_clip.close()
    audio_clip.close()
    os.remove(video_file)
    os.remove(audio_file)
    print(f"Downloaded and merged: {yt.title}")