from flask import Flask, request, render_template, send_file
from pytube import YouTube, Playlist
import os
import zipfile
from moviepy.editor import AudioFileClip

app = Flask(__name__)

def convert_mp4_to_mp3(mp4_path):
    audio = AudioFileClip(mp4_path)
    mp3_path = mp4_path.replace(".mp4", ".mp3")
    audio.write_audiofile(mp3_path)
    return mp3_path

def zip_playlists(output_path, playlist_title):
    zipf = zipfile.ZipFile(f'{playlist_title}', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(output_path):
        for file in files:
            zipf.write(os.path.join(root, file), os.path.basename(os.path.join(root, file)))
    zipf.close()
    return os.path.realpath(zipf.filename)

def download_playlist(url):
    playlist = Playlist(url)
    playlist_title = playlist.title  # Get the playlist title
    output_path = os.path.expanduser(f"~/Downloads/{playlist_title}")
    os.makedirs(output_path, exist_ok=True)
    for video_url in playlist.video_urls:
        try:
            yt = YouTube(video_url)
            stream = yt.streams.get_highest_resolution()
            video_title = yt.title
            safe_filename = "".join([c for c in video_title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
            if os.path.isfile(os.path.join(output_path, safe_filename + ".mp4")):
                print(f"Video {video_title} already exists in your directory, skipping...")
                continue
            print(f"Downloading: {video_title}")
            stream.download(output_path=output_path, filename=safe_filename)
        except Exception as e:
            print(f"An error occurred while downloading the video: {str(e)}")
            continue
    print("Download complete!")
    zip_filepath = zip_playlists(output_path, playlist_title)
    # Remove downloaded videos
    for filename in os.listdir(output_path):
        os.remove(os.path.join(output_path, filename))
    os.rmdir(output_path)
    return zip_filepath


@app.route('/', methods=['GET', 'POST'])
def download_video():
    download_type = None
    if request.method == 'POST':
        url = request.form.get('url')
        print(f"URL: {url}")
        if url is None:
            return "Error: No URL provided. Please enter a URL."
        download_type = request.form.get('download_type')
        if download_type == 'Video' or download_type == 'Audio':
            yt = YouTube(url)
            if download_type == 'Video':
                stream = yt.streams.get_highest_resolution()
            elif download_type == 'Audio':
                stream = yt.streams.get_audio_only()
            output_path = os.path.expanduser("~/Downloads")
            filepath = os.path.join(output_path, stream.default_filename)
            stream.download(output_path=output_path)
            if download_type == 'Audio':
                filepath = convert_mp4_to_mp3(filepath)
            return send_file(filepath, as_attachment=True, download_name=os.path.basename(filepath))
        elif download_type == 'Playlist':
            zip_filepath = download_playlist(url)
            return send_file(zip_filepath, as_attachment=True, download_name=f'{os.path.basename(zip_filepath)}.zip')

        else:
            return "Error: No download type selected."
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
