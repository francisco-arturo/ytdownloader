import yt_dlp as youtube_dl
import os

# Specify the YouTube video URL
url = input("Enter the YouTube URL: ")

# Setup the options for youtube_dl
ydl_opts = {
    'outtmpl': os.path.join(os.path.expanduser('~/Downloads'), '%(title)s.%(ext)s'),
    'format': 'bestaudio/best',  # Select the highest quality.
    'postprocessors': [{  # Specify that we want to convert the video to an mp3
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

# Use youtube_dl to download the video
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("Download Complete!")
