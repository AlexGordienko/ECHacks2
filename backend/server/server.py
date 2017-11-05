from backend.server.video import Video
from flask import Flask
import threading
app = Flask(__name__)

videos = {}

@app.route('/new-video/<path:url>/<string:name>')
def new_video(url: str, name: str) -> str:
    t = threading.Thread(target=process_video, args=(url, name))
    t.daemon = True
    t.start()
    return 'Thanks!'


@app.route('/get-data/<string:name>')
def get_data(name: str) -> str:
    video = videos[name]
    return video.compile_stats()


def process_video(url, name) -> None:
    video = Video(url, name)
    videos[name] = video
    video.download()
    video.parse_frames()
    video.ocr_frames()
    video.update_relevant_frames()
    video.parse_diagram()


if __name__ == '__main__':
    app.run()