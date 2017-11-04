from typing import List
from backend.server.word import Word


class Line:
    """Represents a single line of text in a frame

    text: the text of this line
    bounding_box: a rectangle which surrounds this
    line. Tuple of (x, y, length, width), where
    x, y are the top left corner
    words: list of word objects that make up a line
    """
    text: str
    bounding_box: tuple()
    words: List['Word']

    def __init__(self, text: str, box: tuple(), list_of_words: List['Word']) -> None:
        self.text = text
        self.bounding_box = box
        self.words = list_of_words

    def __eq__(self, other: 'Line') -> bool:
        """
        Check for equality between two Line objects.
        Two lines are equal if they have the same text.
        """
        if self.text == other.text:
            return True
        else:
            return False
