from pytube import YouTube
import cv2
from backend.server.timestamp import Timestamp
from backend.server.frame import Frame
from backend.server.word import Word
from backend.server.line import Line
from backend.server.diagram import Diagram
import json
from typing import List

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
        self.relevant_frames = []

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
                new_frame = Frame(name, time_stamp, current_frame)
                self.frames.append(new_frame)

    def parse_frames_without_saving(self):
        """
        Parses the frames without saving them as jpeg files
        (since they're probably already saved on there)
        """
        success = True
        current_frame = 0
        while success:
            current_frame += 1
            # Go through every second of the video
            if current_frame % self.fps == 0:
                # Get the name of this current frame
                name = self.name + "frame%d.jpg" % current_frame
                secs = current_frame // self.fps
                time_stamp = Timestamp(secs // 60, secs % 60)
                new_frame = Frame(name, time_stamp, current_frame)
                self.frames.append(new_frame)

            if current_frame == 10740:
                success = False

    def ocr_frames(self) -> None:
        """Performs OCR on each frame"""
        for frame in self.frames:
            frame.get_ocr_prediction()

        for frame in self.frames:
            frame.update_stats()

    def read_preloaded_frame_data(self):
        """
        A function which updates the data for each frame of the video
        using preloaded statistics from a past microsoft CV run

        """

        # open the JSON file and read the statistics
        # of the vid_4 video
        with open('test_vid_4.json') as data_file:
            stats = json.load(data_file)

            # frames is a list of each individual frame
            frames = stats["data"]

            # the section of frames which actually represents
            # a frame (and not a confirmation message)
            for i in range(0, len(self.frames)):

                section = frames[i]
                # a dictionary which represents this frame's stats
                current_frame = section["recognitionResult"]
                # the actual frame object
                actual_frame = self.frames[i]
                # the lines of this frame
                lines = current_frame["lines"]
                for line in lines:

                    # each line is a dictionary containing this line's stats

                    # the bounding box for this line
                    line_box = Frame._make_bounding_box(actual_frame, line["boundingBox"])

                    # the text for this line
                    line_text = line['text']

                    # the list of Word objects for this line
                    line_wordslist = []

                    words = line['words']
                    for word in words:
                        word_box = Frame._make_bounding_box(actual_frame, word["boundingBox"])
                        line_wordslist.append(Word(word['text'], word_box))

                    # line_wordslist is now filled with word objects.
                    # add this line to the current iterated frame
                    actual_frame.lines.append(Line(line_text, line_box, line_wordslist))

    def update_relevant_frames(self) -> None:
        """
        Method which selects frames that represent a full chalkboard,
        and populates the relevant_frames list with these frames
        """

        # First, get the maximum amount of words that ever occur on
        # the board
        max_words_on_board = self._get_max_words()

        max_frames = []
        # Store all the frames which contain this number within
        # minus 2 words
        for frame in self.frames:
            words_in_frame = self._get_num_words(frame)
            if words_in_frame >= max_words_on_board - 3:
                max_frames.append(frame)

        max_frames = self._remove_repeats(max_frames)
        self.relevant_frames.extend(max_frames)

    def _remove_repeats(self, max_frames: List['Frame']):
        """
        Remove the frames which come close together to each other
        If there are a lot who are close together to each other,
        pick the one that has the most number of words.
        """

        first = max_frames[0]
        same = [first]
        new_max_frames = []
        for i in range(1, len(max_frames)):
            frame = max_frames[i]
            if frame.frame_num <= first.frame_num + 1500 and i != len(max_frames)-1:
                same.append(frame)

            else:
                # if same is not empty, then we JUST reached a guy
                # who isn't part of this interval of same frames.
                if len(same) != 0:
                    # choose the element in same who has the most words,
                    # and add him to the new_max_frames list.
                    # afterwards, reset same and first for this new guy
                    new_max_frames.append(self._choose_best_in_same(same))
                    first = frame
                    same = [first]

        return new_max_frames

    def _choose_best_in_same(self, same: list):

        # create a parallel list of each element in same's number of words
        num_words = []
        for frame in same:
            num_words.append(self._get_num_words(frame))

        # return the first maximum number of words guy
        return same[num_words.index(max(num_words))]

    def _get_num_words(self, frame: 'Frame') -> int:
        """
        A helper function which returns the number
        of words in a frame
        """
        num_words = 0
        for line in frame.lines:
            num_words += len(line.words)
        return num_words

    def _get_max_words(self) -> int:
        """
        A helper function which returns the maximum
        number of words that ever appear on the board
        """
        max_words = 0
        for frame in self.frames:
            words_in_frame = self._get_num_words(frame)

            if words_in_frame > max_words:
                max_words = words_in_frame

        return max_words

    def parse_diagram(self):
        """Parses out diagrams from best frames"""
        for i, frame in enumerate(self.relevant_frames):
            image = cv2.imread(frame.picture_directory, 0)
            image = cv2.fastNlMeansDenoising(image, 10, 10, 7, 21)
            edges = cv2.Canny(image, 100, 200)

            right = 0
            left = edges.shape[1]
            top = edges.shape[0]
            bottom = 0

            for line in frame.lines:
                bb = self._make_bounding_box(line['boundingBox'])
                if bb[1] < top:
                    top = bb[1]
                if bb[1] + bb[3] > bottom:
                    bottom = bb[1] + bb[3]
                if bb[0] < left:
                    left = bb[0]
                if bb[0] + bb[2] > right:
                    right = bb[0] + bb[2]
                edges[bb[1]:bb[1] + bb[3], bb[0]:bb[0] + bb[2]] = 0

            edges[:, :left] = 255
            edges[:, right:] = 255
            edges[bottom:, :] = 255
            edges[:top, :] = 255

            edges[top:bottom, left:right] = cv2.bitwise_not(edges[top:bottom, left:right])

            image = edges[top:bottom, left:right]

            cv2.imwrite(self.name + "Processedframe%d.jpg" % i, image)

            frame.diagram = Diagram(self.name + "Processedframe%d.jpg" % i, [top, left, right - left, bottom - top])

    def _make_bounding_box(self, coordinates: tuple()) -> tuple():
        """Helper function to calculate bounding box coordinates

        return format (x,y,width,height)
        """
        return coordinates[0], coordinates[1], coordinates[2] - coordinates[0], coordinates[5] - coordinates[1]

    def find_first_occurance(self, line: 'Line') -> Frame:
        """
        Return the first frame which contains this Line object

        Return None if this Line object is not in any frames
        """

        first_frame = None
        for frame in self.frames:
            if line in frame.lines:
                first_frame = frame

        return first_frame