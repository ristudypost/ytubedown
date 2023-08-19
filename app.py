import os
import tempfile
import pytube
import urllib.request
from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()


def download_video(url, save_path):
    youtube = pytube.YouTube(url)
    video_stream = youtube.streams.filter(progressive=True, file_extension='mp4').first()
    video_stream.download(output_path=save_path)
    return video_stream.title


def download_audio(url, save_path):
    youtube = pytube.YouTube(url)
    audio_stream = youtube.streams.filter(only_audio=True).first()
    audio_stream.download(output_path=save_path)
    return audio_stream.title


def download_thumbnail(url, save_path):
    youtube = pytube.YouTube(url)
    thumbnail_url = youtube.thumbnail_url
    thumbnail_file = os.path.join(save_path, "thumbnail.jpg")
    urllib.request.urlretrieve(thumbnail_url, thumbnail_file)
    return "thumbnail.jpg"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        option = request.form['option']

        if not url:
            return "Please provide a valid YouTube URL."

        save_path = app.config['UPLOAD_FOLDER']

        if option == 'video':
            title = download_video(url, save_path)
            return send_from_directory(save_path, title + ".mp4", as_attachment=True)
        elif option == 'audio':
            title = download_audio(url, save_path)
            return send_from_directory(save_path, title + ".mp3", as_attachment=True)
        elif option == 'thumbnail':
            thumbnail_file = download_thumbnail(url, save_path)
            return send_from_directory(save_path, thumbnail_file, as_attachment=True)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)




