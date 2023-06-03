import os
from flask import Flask, request, send_file
import yt_dlp

app = Flask(__name__)


def download(video_url, type):
    delete_file()
    ydl_opts = {}

    if type == 'mp3':
        ydl_opts['format'] = 'm4a/bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    elif type == 'mp4':
        ydl_opts['format'] = 'mp4'

    name = ''

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        info_dict = ydl.extract_info(video_url, download=False)
        name = info_dict.get('title', None)

    for file in os.listdir():
        if file.endswith(f'.{type}'):
            name = file
            break

    formatted_name = name.replace(" ", "_").lower()

    os.rename(name, formatted_name)

    return send_file(f'{formatted_name}', as_attachment=True)


@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    type = request.args.get('type')

    return download(video_url, type)


@app.route('/')
def hello_world():
    return 'Hello, World!'


def delete_file():
    for file in os.listdir():
        if file.endswith('.mp3') or file.endswith('.mp4'):
            os.remove(file)


if __name__ == '__main__':
    app.run()
