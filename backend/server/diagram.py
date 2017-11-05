

class Diagram:
    """Represents a Diagram on a whiteboard that someone would draw

    image_dir: location of the image
    bounding_box: bounding coordinates of the diagram in (x, y, length, width) format
    """
    image_dir: str
    bounding_box: tuple()

    def __init__(self, image_dir: str, box: tuple()):
        """Initializes the Diagram object"""
        self.image_dir = image_dir
        self.bounding_box = box

    def get_image_bytes(self):
        """Gets the diagram image and returns the bytes for http requests"""
        file = open(self.image_dir, 'rb')
        data = file.read()
        file.close()
        return data