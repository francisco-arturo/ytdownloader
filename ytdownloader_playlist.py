from pytube import YouTube, Playlist
import os

# Specify the YouTube playlist URL
playlist_url = input("Enter the YouTube playlist URL: ")

# Create a Playlist object
playlist = Playlist(playlist_url)

# Specify the output path
output_path = os.path.expanduser("~/Downloads")

# Create the directory if it doesn't exist
os.makedirs(output_path, exist_ok=True)

# Iterate over each video in the playlist
for video_url in playlist.video_urls:
    try:
        # Create a YouTube object for the current video
        yt = YouTube(video_url)

        # Select the highest resolution stream available
        stream = yt.streams.get_highest_resolution()

        # Get the title of the video and sanitize it
        video_title = yt.title
        safe_filename = "".join([c for c in video_title if c.isalpha() or c.isdigit() or c==' ']).rstrip()

        # Check if the video file already exists
        if os.path.isfile(os.path.join(output_path, safe_filename + ".mp4")):
            print(f"Video {video_title} already exists in your directory, skipping...")
            continue

        # Download the video to the specified location
        print(f"Downloading: {video_title}")
        stream.download(output_path=output_path, filename=safe_filename)

    except Exception as e:
        print(f"An error occurred while downloading the video: {str(e)}")
        continue

print("Download complete!")