from pytube import YouTube
import cv2
from typing import List, Dict, Tuple
import requests
import json


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
    relevant_frames: ['Frame']

    def __init__(self, link: str, name: str) -> None:
        """Initializes a video object"""
        self.link = link
        self.directory = None
        self.frames = []
        self.name = name
        self.fps = -1

    def download(self) -> None:
        """Downloads a youtube video to the drive"""
        stream = YouTube(self.link).streams.first()
        stream.download('./')
        self.fps = stream.fps
        self.directory = './' + stream.default_filename

    def parse_frames(self) -> None:
        """
        saves every tenth frame as a jpeg file in the 'server' directory,
        and parses this video into a list of Frame objects

        """
        # OpenCV code used to read the frames in the video
        vidcap = cv2.VideoCapture(self.directory)
        success, image = vidcap.read()
        current_frame = 0
        while success:
            success, image = vidcap.read()
            current_frame += 1
            # Go through every second of the video
            if current_frame % self.fps == 0:
                # Save frame as JPEG file
                cv2.imwrite(self.name + "frame%d.jpg" % current_frame, image)

                # Get the name of this current frame
                name = self.name + "frame%d.jpg" % current_frame
                secs = current_frame // self.fps
                time_stamp = Timestamp(secs // 60, secs % 60)
                new_frame = Frame(name, time_stamp)
                self.frames.append(new_frame)

                # TODO: Make this none blocking
                new_frame.get_ocr_prediction()

    def update_relevant_frames(self) -> None:
        """
        Method which selects frames that represent a full chalkboard,
        and populates the relevant_frames list with these frames
        """

        # Analyze first and fourth elements, and look for a
        # increase / decrease in words count.
        # An increase in words imply the prof is writing something
        # A decrease in words imply he/she is erasing something

        start = 0
        end = 4
        while end < len(self.frames):
            start_frame = self.frames[start]
            end_frame = self.frames[end]
            start_frame_words = self._get_num_words(start_frame)
            end_frame_words = self._get_num_words(end_frame)

            # Decreasing behavior, so start_frame words
            # is likely the board when it is being erased
            if end_frame_words < start_frame_words:
                # Check if the decrease is significant.
                # That is, one third the words are removed within
                # these four seconds
                words_removed = end_frame_words - start_frame_words
                if words_removed >= (start_frame_words // 3):
                    # The board first frame is likely a relevant frame
                    # being cleared.
                    self.relevant_frames.append(start_frame)

            start += 1
            end += 1

    def _get_num_words(self, frame: 'Frame') -> int:
        """
        A helper function which returns the number
        of words in a frame

        """
        num_words = 0
        for line in frame.lines:
            for word in line.words:
                num_words += 1
        return num_words


class Frame:
    """Represents a single picture frame in the video.

    picture_directory: location of the frame on the device
    time_stamp: time of the frame in the video
    lines: lines of text in the frame
    """
    picture_directory: str
    time_stamp: 'Timestamp'
    lines: List['Line']

    def __init__(self, picture_directory: str, time_stamp: 'Timestamp') -> None:
        self.picture_directory = picture_directory
        self.time_stamp = time_stamp
        self.lines = []

    def get_ocr_prediction(self):
        """Gets the OCR prediction of the frame from Microsoft

        https://westus.dev.cognitive.microsoft.com/docs/services/
        56f91f2d778daf23d8ec6739/operations/56f91f2e778daf14a499e1fc"""

        api_key = '8b171262b47349bc9ab7967726fb5d96'
        headers = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': api_key}
        data = open(self.picture_directory, 'rb').read()

        r = requests.post('https://eastus.api.cognitive.microsoft.com/vision/v1.0/ocr?language=en',
                          headers=headers,
                          data=data)

        print(r.text)
        self.update_stats(json.loads(r.text))

    # TODO: Clean up
    def update_stats(self, stats: Dict) -> None:
        """
        Takes a dictionary of statistics given by microsoft,
        and converts it into both a list of lines, and a list of words
        """
        regions = stats['regions']
        for region in regions:
            lines = region['lines']
            for line in lines:
                words = line['words']
                wl = []
                line_text = ''
                for word in words:
                    line_text += ' ' + word['text']
                    bb = tuple(map(int, word['boundingBox'].split(',')))
                    wl.append(Word(word['text'], bb))
                bb = tuple(map(int, line['boundingBox'].split(',')))
                self.lines.append(Line(line_text, bb, wl))


class Line:
    """Represents a single line of text in a frame

    text: the text of this line
    bounding_box: a rectangle which surrounds this
    line. Tuple of (x, y, length, width), where
    x, y are the top left corner
    words: list of word objects that make up a line
    """
    text: str
    bounding_box: tuple()
    words: List['Word']

    def __init__(self, text: str, box: tuple(), list_of_words: List['Word']) -> None:
        self.text = text
        self.bounding_box = box
        self.words = list_of_words


class Word:
    """Represents a word in a frame

    text: text of the word
    bounding_box: a rectangle which surrounds this
    line. Tuple of (x, y, length, width), where
    x, y are the top left corner
    """
    text: str
    bounding_box: tuple()

    def __init__(self, text: str, box: tuple()) -> None:
        self.text = text
        self.bounding_box = box


class Timestamp:
    """Timestamp object for a video

    mins: minutes of the timestamp
    sec: seconds of the timestamp"""
    mins: int
    sec: int

    def __init__(self, mins: int, sec: int) -> None:
        """Initialize the Timestamp"""
        self.mins = mins
        self.sec = sec

    def __str__(self) -> str:
        """Prints the timestamp"""
        return str(self.mins) + 'm' + str(self.sec) + 's'

    def to_secs(self) -> int:
        """Takes Timestamp and converts it to seconds"""
        return self.mins * 60 + self.sec

