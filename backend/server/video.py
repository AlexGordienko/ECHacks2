from pytube import YouTube


class Video:
    """ Represents a uploaded youtube video

    link: URL link to the youtube video
    directory: Location of video on the server
    frames: list of the frames of the video
    """
    link: str
    directory: str
    frames: ['Frame']

    def __init__(self, link: str) -> None:
        """Initializes a video object"""
        self.link = link
        self.directory = None
        self.frames = []

    def download(self) -> None:
        """Downloads a youtube video to the drive"""
        stream = YouTube(self.link).streams.first()
        stream.download('./')
        self.directory = './' + stream.default_filename

    def parse_frames(self) -> None:
        """Computes the frames of the video"""
        # TODO: parse the frames
        pass
