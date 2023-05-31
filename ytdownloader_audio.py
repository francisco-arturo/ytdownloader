from pytube import YouTube
import os

# Specify the YouTube video URL
url = input("Enter the YouTube URL: ")

# Create a YouTube object
yt = YouTube(url)

# Select the audio-only stream
stream = yt.streams.get_audio_only()

# Get the path to the "Videos" directory in your home directory
output_path = os.path.expanduser("~/Downloads")

# Download the audio to the specified location
stream.download(output_path=output_path)
print("Download Complete!")
