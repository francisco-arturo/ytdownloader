from pytube import YouTube
import os

# Specify the YouTube video URL /
url = input("Enter the YouTube URL: ")

# Create a YouTube object
yt = YouTube(url)

# Select the highest resolution stream available
stream = yt.streams.get_highest_resolution()

# Get the path to the "Videos" directory in your home directory
output_path = os.path.expanduser("~/Downloads")

# Download the video to the specified location
stream.download(output_path=output_path)
print("Download Complete!")