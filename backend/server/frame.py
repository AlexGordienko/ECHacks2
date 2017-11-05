from typing import List
import requests
import json
from backend.server.timestamp import Timestamp
from backend.server.line import Line
from backend.server.word import Word
from backend.server.diagram import Diagram


class Frame:
    """Represents a single picture frame in the video.

    picture_directory: location of the frame on the device
    time_stamp: time of the frame in the video
    lines: lines of text in the frame
    """
    picture_directory: str
    time_stamp: 'Timestamp'
    lines: List['Line']
    return_url: str
    diagram: 'Diagram'

    def __init__(self, picture_directory: str, time_stamp: 'Timestamp') -> None:
        self.picture_directory = picture_directory
        self.time_stamp = time_stamp
        self.lines = []
        self.return_url = ''
        self.diagram = None

    def get_ocr_prediction(self) -> None:
        """Gets the OCR prediction of the frame from Microsoft

        https://westus.dev.cognitive.microsoft.com/docs/services/
        56f91f2d778daf23d8ec6739/operations/56f91f2e778daf14a499e1fc"""

        api_key = '8b171262b47349bc9ab7967726fb5d96'
        headers = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': api_key}
        data = open(self.picture_directory, 'rb')

        r = requests.post('https://eastus.api.cognitive.microsoft.com/vision/v1.0/recognizeText?handwriting=true',
                          headers=headers,
                          data=data.read())

        data.flush()
        data.close()

        if 'Operation-Location' in r.headers:
            self.return_url = r.headers['Operation-Location']
        else:
            self.return_url = None

    def update_stats(self) -> None:
        """
        Takes a dictionary of statistics given by microsoft,
        and converts it into both a list of lines, and a list of words
        """
        if self.return_url is None:
            return

        api_key = '8b171262b47349bc9ab7967726fb5d96'
        r = requests.get(self.return_url,
                         headers={'Ocp-Apim-Subscription-Key': api_key})

        stats = json.loads(r.text)

        print(r.text + ",")

        result = stats['recognitionResult']
        lines = result['lines']
        for line in lines:
            words = line['words']
            wl = []
            for word in words:
                bb = self._make_bounding_box(word['boundingBox'])
                wl.append(Word(word['text'], bb))
            bb = self._make_bounding_box(line['boundingBox'])
            self.lines.append(Line(line['text'], bb, wl))

    def _make_bounding_box(self, coordinates: tuple()) -> tuple():
        """Helper function to calculate bounding box coordinates

        return format (x,y,width,height)
        """

        return coordinates[0], coordinates[1], coordinates[2] - coordinates[0], coordinates[5] - coordinates[1]

    # def crop_frame(self):
    #     """
    #     Create a box around the board of this frame.
    #     We do this by finding the word that is the most to the top-left,
    #     and finding the word that is most to the bottom right,
    #     and drawing a rectangle with everything inbetween these words
    #
    #     """
    #
    #     # open the image and get it's dimensions
    #     img = Image.open(self.picture_directory)
    #     img_dimensions = img.size  # return value is a tuple, ex.: (1200, 800)
    #
    #     # initialize topleft to origin,
    #     # botright to the bot right corner
    #     topleft_x = 0
    #     topleft_y = 0
    #     botright_x = img_dimensions[0]
    #     botright_y = img_dimensions[1]
    #
    #     # the bottom right sum, we're looking for the greatest x,y sum
    #     # top left sum, we're looking for the smallest
    #     botright_sum = 0
    #     topleft_sum = 99999
    #
    #     for line in self.lines:
    #         for word in line.words:
    #             word_x, word_y = word.bounding_box[0], word.bounding_box[1]
    #
    #             if word_x + word_y < topleft_sum:
    #                 topleft_x = word_x
    #                 topleft_y = word_y
    #                 topleft_sum = word_x + word_y
    #
    #             elif word_x + word_y > botright_sum:
    #                 botright_x = word_x
    #                 botright_y = word_y
    #                 botright_sum = word_x + word_y
    #
    #     # crop this frame
    #     img = img.crop(topleft_x, topleft_y, botright_x, botright_y)

