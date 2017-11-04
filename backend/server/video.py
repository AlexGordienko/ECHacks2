from pytube import YouTube
import cv2
from typing import List, Dict, Tuple


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
        self.fps = int(stream.fps[:-3])
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
            # Go through every tenth frame
            if current_frame % 10 == 0:
                # Save frame as JPEG file
                cv2.imwrite(self.name + "frame%d.jpg" % current_frame, image)

                # Get the name of this current frame
                name = self.name + "frame%d.jpg"
                secs = current_frame // self.fps
                time_stamp = Timestamp(secs // 60, secs % 60)
                new_frame = Frame(name, time_stamp)
                self.frames.append(new_frame)

                # TODO: Make this none blocking
                new_frame.get_ocr_prediction()


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
        # TODO: Implement
        pass

    # TODO: Clean up
    def update_stats(self, stats: Dict['String']) -> None:
        """
        Takes a dictionary of statistics given by microsoft,
        and converts it into both a list of lines, and a list of words

        """
        list_of_lines = stats["lines"]
        for line_stats in list_of_lines:
            line_text = line_stats["text"]
            position_list = line_stats["boundingBox"]
            bounding_box = (position_list[0], position_list[1], position_list[2] - position_list[0],
                            position_list[5] - position_list[1])

            list_of_words = []
            words = line_stats["words"]
            for word_stats in words:
                self._add_word(list_of_words, word_stats)

            self.lines.append(Line(line_text, bounding_box, list_of_words))

    def _add_word(self, list_of_words: List[""], word_stats: Dict):
        position_list = word_stats["boundingBox"]

        bounding_box_line = (position_list[0], position_list[1], position_list[2] - position_list[0],
                             position_list[5] - position_list[1])

        list_of_words.append(Word(word_stats["text"], bounding_box_line))


class Line:
    """Represents a single line of text in a frame

    text: the text of this line
    bounding_box: a rectangle which surrounds this
    line. Tuple of (x, y, length, width), where
    x, y are the top left corner
    words: list of word objects that make up a line
    """
    text: str
    bounding_box: Tuple(int, int, int, int)
    words: List[Word]

    def __init__(self, text, box, list_of_words) -> None:
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
    bounding_box: Tuple(int, int, int, int)

    def __init__(self, text, box) -> None:
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
        return str(self.mins)+ "m" + str(self.sec) + "s"
