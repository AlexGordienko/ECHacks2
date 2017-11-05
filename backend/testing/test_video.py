import unittest
from backend.server.video import Video


class TestVideo(unittest.TestCase):

    def test_frames(self):
        v = Video('', 'Video')
        v.directory = './test_vid_4.mp4'
        v.fps = 30
        v.parse_frames()
        v.ocr_frames()


if __name__ == '__main__':
    unittest.main()