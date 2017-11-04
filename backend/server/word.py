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
