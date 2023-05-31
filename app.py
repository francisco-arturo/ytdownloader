from flask import Flask, request, render_template, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def download_video():
    if request.method == 'POST':
        url = request.form.get('url')  # Get the URL from the form
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        output_path = os.path.expanduser("~/Downloads")
        filepath = os.path.join(output_path, stream.default_filename)
        stream.download(output_path=output_path)
        return send_file(filepath, as_attachment=True, download_name=stream.default_filename)
    return render_template('index.html')  # Render the form

if __name__ == "__main__":
    app.run(debug=True)
