from backend.server.video import Video
from flask import Flask
app = Flask(__name__)


@app.route('/new-video/<path:url>')
def new_video(url: str) -> None:
    video = Video(url, 'Test')
    video.download()
    print('Downloaded')
    video.parse_frames()


if __name__ == '__main__':
    app.run()