class Word:
    """Represents a word in a frame

    text: text of the word
    bounding_box: a rectangle which surrounds this
    line. Tuple of (x, y, length, width), where
    x, y are the top left corner
    """
    text: str
    bounding_box: tuple()

    def __init__(self, text: str, box: tuple()) -> None:
        self.text = text
        self.bounding_box = box

    def __eq__(self, other: 'Word') -> bool:
        """
        Check for equality between two Word objects.
        Two words are equal if they have the same text.
        """
        if self.text == other.text:
            return True
        else:
            return False
