from backend.server.video import Video
from flask import Flask, make_response
import threading
import json
app = Flask(__name__)

videos = {}


@app.route('/new-video/<path:url>/<string:name>')
def new_video(url: str, name: str) -> str:
    t = threading.Thread(target=process_video, args=(url, name))
    t.daemon = True
    #t.start()
    return json.dumps({'results': 'Thanks!'})


@app.route('/get-data/<string:name>')
def get_data(name: str) -> str:
    video = videos[name]
    resp = make_response(json.dumps(video.compile_stats()), 200)
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def process_video(url, name) -> None:
    video = Video(url, name)
    videos[name] = video
    video.download()
    video.parse_frames()
    video.ocr_frames()
    video.update_relevant_frames()
    video.parse_diagram()


def load_from_cache() -> None:
    new_vid = Video("https://youtu.be/2ceKYagf2h0", "lecture1")
    new_vid.directory = "./test_vid_4.mp4"
    new_vid.fps = 30

    new_vid.parse_frames_without_saving()
    new_vid.read_preloaded_frame_data()
    new_vid.update_relevant_frames()

    videos['lecture1'] = new_vid


if __name__ == '__main__':
    load_from_cache()
    app.run(host='0.0.0.0')
