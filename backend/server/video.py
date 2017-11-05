from pytube import YouTube
import cv2
from backend.server.timestamp import Timestamp
from backend.server.frame import Frame
from backend.server.word import Word
from backend.server.line import Line
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
                if current_frame > 5400:
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
        # of the vid_2 video
        with open('test_vid_2.json') as data_file:
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

    def update_relevant_frames_2(self) -> None:
        """
        Method which selects frames that represent a full chalkboard,
        and populates the relevant_frames list with these frames

        """

        # Analyze each frame and store the frame with the most words.
        # While you're analyzing, check if this current frame has
        # less than half the words of the max frame. If it does, that
        # means at this stage, we can assume the board is being erased.
        # And so, we select the previous maximum frame as a relevant frame.

        max_words = -1
        max_frame = None

        for i in range(0, len(self.frames)):
            if i >= 840:
                frame = self.frames[i]
                words_in_frame = self._get_num_words(frame)

                if words_in_frame > max_words:
                    max_words = words_in_frame
                    max_frame = frame

                # current iterated frame has half the words
                # of the max frame, so we count the last
                # max frame as relevent, and restart
                elif max_words // 2 > words_in_frame:
                    self.relevant_frames.append(max_frame)
                    max_words = -1
                    max_frame = None

    def update_relevant_frames_3(self) -> None:
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
            if frame.frame_num <= first.frame_num + 1000 and i != len(max_frames)-1:
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
        for frame in self.relevant_frames:
            image = cv2.imread(frame.picture_directory, 0)
            cv2.imshow('image', image)
            cv2.waitKey(0)

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

            cv2.destroyAllWindows()

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