from pytube import YouTube
import cv2
from backend.server.timestamp import Timestamp
from backend.server.frame import Frame
from backend.server.word import Word
from backend.server.line import Line
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
                if current_frame > 3000:
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

    def _get_num_words(self, frame: 'Frame') -> int:
        """
        A helper function which returns the number
        of words in a frame
        """
        num_words = 0
        for line in frame.lines:
            for _ in line.words:
                num_words += 1
        return num_words

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