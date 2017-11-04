from flask import Flask
app = Flask(__name__)


@app.route('/new-video')
def new_video():
    # TODO: Invoke new video upload
    pass


if __name__ == '__main__':
    app.run()