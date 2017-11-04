from pytube import YouTube
import cv2
from backend.server.timestamp import Timestamp
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

        for frame in self.frames:
            frame.get_ocr_prediction()

        for frame in self.frames:
            frame.update_stats()

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

        # Analyze each frame and store the frame with the most words
        # While you're analyzing, check if this current frame has
        # less than half the words of the max frame. At this stage,
        # we can assume the board is being erased. And so, we select
        # the previous maximum frame as a relevant frame.

        max_words = -1
        max_frame = None

        for frame in self.frames:

            words_in_frame = self._get_num_words(frame)

            if words_in_frame > max_words:
                max_words = words_in_frame
                max_frame = frame

            # current iterated frame has half the words
            # of the max frame, so we count the last
            # max frame as relevent, and restart
            elif max_frame // 2 > words_in_frame:
                self.relevant_frames.append(max_frame)
                max_words = -1
                max_frame = None

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