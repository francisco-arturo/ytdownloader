import yt_dlp as youtube_dl
import os

# Specify the YouTube playlist URL
url = input("Enter the YouTube playlist URL: ")

# Setup the options for youtube_dl
ydl_opts = {
    'outtmpl': os.path.join(os.path.expanduser('~/Downloads'), '%(title)s.%(ext)s'),
    'format': 'best',  # Select the highest quality.
    'noplaylist' : False,  # This is required when downloading playlists
}

# Use youtube_dl to download the playlist
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("Download Complete!")