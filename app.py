from flask import Flask, request, render_template, send_file
from pytube import YouTube
import os
from moviepy.editor import AudioFileClip

app = Flask(__name__)

def convert_mp4_to_mp3(mp4_path):
    audio = AudioFileClip(mp4_path)
    mp3_path = mp4_path.replace(".mp4", ".mp3")
    audio.write_audiofile(mp3_path)
    return mp3_path

@app.route('/', methods=['GET', 'POST'])
def download_video():
    if request.method == 'POST':
        url = request.form.get('url')  # Get the URL from the form
        print(f"URL: {url}")  # Print out the value of 'url'
        if url is None:  # Check if 'url' is None
            return "Error: No URL provided. Please enter a URL."

        yt = YouTube(url)

        download_type = request.form.get('download_type')

        if download_type == 'Video':
            # If 'video' key exists in form data, download video
            stream = yt.streams.get_highest_resolution()
        elif download_type == 'Audio':
            # If 'audio' key exists in form data, download audio
            stream = yt.streams.get_audio_only()
        else:
            return "Error: No download type selected."

        output_path = os.path.expanduser("~/Downloads")
        filepath = os.path.join(output_path, stream.default_filename)
        stream.download(output_path=output_path)

        # Convert to mp3 if the download type is 'Audio'
        if download_type == 'Audio':
            filepath = convert_mp4_to_mp3(filepath)

        return send_file(filepath, as_attachment=True, download_name=os.path.basename(filepath))
    return render_template('index.html')  # Render the form
