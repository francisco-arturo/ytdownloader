from flask import Flask, request, render_template, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        url = request.form.get('url')  # Get the URL from the form
        print(f"URL: {url}")  # Print out the value of 'url'
        if url is None:  # Check if 'url' is None
            return "Error: No URL provided. Please enter a URL."
        
        yt = YouTube(url)
        
        if 'video' in request.form:
            # If 'video' key exists in form data, download video
            stream = yt.streams.get_highest_resolution()
        elif 'audio' in request.form:
            # If 'audio' key exists in form data, download audio
            stream = yt.streams.get_audio_only()
        else:
            return "Error: No download type selected."
        
        output_path = os.path.expanduser("~/Downloads")
        filepath = os.path.join(output_path, stream.default_filename)
        stream.download(output_path=output_path)
        return send_file(filepath, as_attachment=True, download_name=stream.default_filename)
    return render_template('index.html')  # Render the form

if __name__ == "__main__":
    app.run(debug=True)
