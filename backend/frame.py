from typing import List, Dict, Tuple

class Frame:
    """
    Represents a single picture frame in the video

    """

    picture_url: str
    time: float
    lines: List[Line]

    def __init__(self, url: str, time: float) -> None:
        self.picture_url = url
        self.time = time
        self.lines = []

    def update_stats(self, stats: Dict['String']) -> None:
        """
        Takes a dictionary of statistics given by microsoft,
        and converts it into both a list of lines, and a list of words

        """

        # modify the dictionary given by microsoft,
        # so we're just dealing with a list of stats
        # for each 'line' (block of text) in the picture

        list_of_lines = stats["lines"]

        for line_stats in list_of_lines:
            # text of this line
            line_text = line_stats["text"]

            # get the list containing the line's bounding box position
            position_list = line_stats["boundingBox"]

            # convert this into a tuple of (x, y, length, width) of the current line's BB
            bounding_box = (position_list[0], position_list[1], position_list[2] - position_list[0],
                                 position_list[5] - position_list[1])

            # create and fill a list of words of the current line
            list_of_words = []

            # the words for this line
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
    """
    Represents a single line

    text: the text of this line
    bounding_box: a rectangle which surrounds this
    line. Tuple of (x, y, length, width), where
    x, y are the top left corner

    """

    text: str
    bounding_box: Tuple(int, int, int, int)
    words: List[Word]

    def __init__(self, text, box, list_of_words) -> None:
        self.text = text
        self.bounding_box = box
        self.words = list_of_words


class Word:
    """
    Represents a word, which has the same properties of a line
    (except list of words)

    """

    text: str
    bounding_box: Tuple(int, int, int, int)

    def __init__(self, text, box) -> None:
        self.text = text
        self.bounding_box = box
