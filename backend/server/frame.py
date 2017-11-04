from typing import List
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
    return_url: str

    def __init__(self, picture_directory: str, time_stamp: 'Timestamp') -> None:
        self.picture_directory = picture_directory
        self.time_stamp = time_stamp
        self.lines = []
        self.return_url = ''

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

        print(r.headers)
        print(r.headers.keys())

        if 'Operation-Location' in r.headers:
            print("Found")
            self.return_url = r.headers['Operation-Location']
        else:
            print("not Found")
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
