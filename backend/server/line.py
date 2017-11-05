from typing import List
from backend.server.word import Word
import enchant


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

    def fix_text(self):
        """
        Go through each word in the line_text, and make sure each
        word is an actual word ( and not mispelled / misinterpreted )
        If it's misspelt, try to fix it.
        """
        words_in_line = self.text.split(" ")
        d = enchant.Dict("en_US")
        # if the current iterated word is NOT a word
        for i in range(0, len(words_in_line)):
            wordtext = words_in_line[i]
            if not d.check(wordtext) and wordtext not in "!@#$%^&*()?":
                # try to fix it, if you can, and replace it
                suggestions = d.suggest(wordtext)
                if len(suggestions) != 0:
                    words_in_line[i] = d.suggest(wordtext)[0]

        # rebuild the text of the line
        new_line_text = ""
        for wordtext in words_in_line:
            new_line_text += wordtext + " "
        new_line_text = new_line_text[:-1]
        self.text = new_line_text

    def fix_words(self):
        for word in self.words:
            wordtext = word.text
            d = enchant.Dict("en_US")
            # check if this word is actually a word. if not, try to fix it
            if not d.check(wordtext) and wordtext not in "!@#$%^&*()?":
                suggestions = d.suggest(wordtext)
                if (len(suggestions) != 0):
                    wordtext = suggestions[0]

            word.text = wordtext
