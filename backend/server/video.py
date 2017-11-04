from pytube import YouTube
import cv2
import time
from typing import List
from backend.server.frame import Frame

class Video:
    """ Represents a uploaded youtube video

    link: URL link to the youtube video
    directory: Location of video on the server
    frames: list of the frames of the video
    """
    link: str
    directory: str
    frames: ['Frame']
    name: str
    fps: int
    time: int

    def __init__(self, link: str, name: str) -> None:
        """Initializes a video object"""
        self.link = link
        self.directory = None
        self.frames = []
        self.name = name

    def download(self) -> None:
        """Downloads a youtube video to the drive"""
        stream = YouTube(self.link).streams.first()
        stream.download('./')
        self.directory = './' + stream.default_filename

    def parse_frames(self) -> None:
        """
        saves every tenth frame as a jpeg file in the 'server' directory,
        and parses this video into a list of Frame objects

        """

        # openCV code used to read the frames in the video
        vidcap = cv2.VideoCapture(self.directory)
        success, image = vidcap.read()
        current_frame = 0
        while success:
            success, image = vidcap.read()
            current_frame += 1
            # go through every tenth frame
            if current_frame % 10 == 0:

                # save frame as JPEG file
                cv2.imwrite(self.name + "frame%d.jpg" % current_frame, image)

                # get the name of this current frame
                name = self.name + "frame%d.jpg"
                time = current_frame * self.fps
                new_frame = Frame(name, time)
                new_frame.get_ocr_prediction()
                self.frames.append(new_frame)
