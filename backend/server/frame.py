from typing import List, Dict
import requests
import json
from backend.server.timestamp import Timestamp
from backend.server.line import Line
from backend.server.word import Word


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

        r = requests.post('https://eastus.api.cognitive.microsoft.com/vision/v1.0/recognizeText?handwriting',
                          headers=headers,
                          data=data)

        print(r.text)
        self.update_stats(json.loads(r.text))

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
