from flask import Flask, request, render_template, send_file
from pytube import YouTube, Playlist
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def download_media():
    if request.method == 'POST':
        url = request.form.get('url')  # Get the URL from the form
        download_type = request.form.get('download_type')  # Get the selected download type

        if download_type == 'Video':
            # Download video
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            output_path = os.path.expanduser("~/Downloads")
            filepath = os.path.join(output_path, stream.default_filename)
            stream.download(output_path=output_path)
            return send_file(filepath, as_attachment=True, attachment_filename=stream.default_filename)

        elif download_type == 'Audio':
            # Download audio
            yt = YouTube(url)
            stream = yt.streams.get_audio_only()
            output_path = os.path.expanduser("~/Downloads")
            filepath = os.path.join(output_path, stream.default_filename)
            stream.download(output_path=output_path)
            return send_file(filepath, as_attachment=True, attachment_filename=stream.default_filename)

        elif download_type == 'Playlist':
            # Download playlist
            playlist = Playlist(url)
            output_path = os.path.expanduser("~/Downloads")
            os.makedirs(output_path, exist_ok=True)

            for video_url in playlist.video_urls:
                try:
                    yt = YouTube(video_url)
                    stream = yt.streams.get_highest_resolution()
                    video_title = yt.title
                    safe_filename = "".join([c for c in video_title if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
                    filepath = os.path.join(output_path, safe_filename + ".mp4")

                    if not os.path.isfile(filepath):
                        stream.download(output_path=output_path, filename=safe_filename)

                except Exception as e:
                    print(f"An error occurred while downloading the video: {str(e)}")
                    continue

            return "Download Complete!"

    return render_template('index.html')  # Render the form

if __name__ == "__main__":
    app.run(debug=True)
