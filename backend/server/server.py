from backend.server.video import Video
from flask import Flask
app = Flask(__name__)


@app.route('/new-video/<int:url>')
def new_video(url: str) -> None:
    video = Video(url)
    video.download()


if __name__ == '__main__':
    app.run()