from typing import List
import requests
import json
from backend.server.timestamp import Timestamp
from backend.server.line import Line
from backend.server.word import Word
from backend.server.diagram import Diagram
from PIL import Image
import enchant

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
    frame_num: int
    keywords: list

    def __init__(self, picture_directory: str, time_stamp: 'Timestamp', frame_number: int) -> None:
        self.picture_directory = picture_directory
        self.time_stamp = time_stamp
        self.lines = []
        self.return_url = ''
        self.diagram = None
        self.frame_num = frame_number
        self.keywords = []

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

        result = stats['recognitionResult']
        lines = result['lines']
        for line in lines:
            # each line is a dictionary containing this line's stats

            # the bounding box for this line
            line_box = self._make_bounding_box(line["boundingBox"])

            # the text for this line
            line_text = line['text']

            # the list of Word objects for this line
            line_wordslist = []
            d = enchant.Dict("en_US")
            words = line['words']
            for word in words:
                word_box = self._make_bounding_box(word["boundingBox"])
                wordtext = word['text']
                # check if this word is actually a word. if not, try to fix it
                if not d.check(wordtext):
                    suggestions = d.suggest(wordtext)
                    if (len(suggestions) != 0):
                        wordtext = suggestions[0]

                line_wordslist.append(Word(wordtext, word_box))

            # line_wordslist is now filled with word objects.

            # create this new Line object
            new_line = Line(line_text, line_box, line_wordslist)

            # fix it's text if needed
            new_line.fix_text()

            # add this new Line object to the current iterated frame
            self.lines.append(new_line)

    def _make_bounding_box(self, coordinates: tuple()) -> tuple():
        """Helper function to calculate bounding box coordinates

        return format (x,y,width,height)
        """

        return coordinates[0], coordinates[1], coordinates[2] - coordinates[0], coordinates[5] - coordinates[1]

    def mark_keywords(self):
        """
        Algorithm which marks the key words in a frame.
        These are words that start with capital letters,
        with the exception of words which start a sentence
        and my name (Sid Gupta).
        Also, if two keywords are right beside each other, they
        probably belong together (like Prototype Theory). So deal
        with that case at the end.
        """
        # list to help determine caps
        caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        for line in self.lines:
            # iterate through the words in this line
            for i in range(1, len(line.words)):
                word = line.words[i]
                if word.text[0] in caps and len(word.text) != 1:
                    # Now check to make sure it doesn't
                    # begin at the start of a sentence.
                    # That is, the last word didn't end in a period
                    last_word = line.words[i-1]
                    if last_word.text[-1] != '.':
                        self.keywords.append(word)

        # Analyze consequetive keywords (go backwards)
        for i in range(len(self.keywords)-1, 0, -1):
            word1 = self.keywords[i]
            word2 = self.keywords[i-1]

            word1_pos = word1.bounding_box
            word2_pos = word2.bounding_box

            # if the y position of the words is less than a difference of 5px,
            # then consider them beside each other.
            if abs(word1_pos[1] - word2_pos[1]) < 20:

                # merge these two keywords into one keyword. this new word will be stored
                # in word_2's position so it can be analyzed again, and word_2 / word_1
                # will be popped
                new_keyword = Word(word2.text + " " + word1.text,
                                   (word2_pos[0], word2_pos[1], word2_pos[2] + word1_pos[2], word2_pos[3]))
                self.keywords.insert(i - 1, new_keyword)
                self.keywords.remove(word2)
                self.keywords.remove(word1)

    def filter_keywords_from_lines(self):
        """filter out the text of the keywords
         from the lines in the frame"""

        for line in self.lines:
            for keyword in self.keywords:
                line.text = line.text.replace(keyword.text, " "*len(keyword.text))


