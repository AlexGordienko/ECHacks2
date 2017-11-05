from backend.server.video import Video
from backend.server.word import Word
from backend.server.line import Line
from backend.server.frame import Frame
import unittest

def test_read_preloaded():

    new_vid = Video("insertlinkhere", "lecture1")
    new_vid.directory = "./test_vid_5.mp4"
    new_vid.fps = 30

    new_vid.parse_frames_without_saving()
    new_vid.read_preloaded_frame_data()
    new_vid.update_relevant_frames()

    for frame in new_vid.relevant_frames:
        for line in frame.lines:
            line.fix_text()
            line.fix_words()

        for line in frame.lines:
            print(line.text)
        print("")
        print("")

if __name__ == '__main__':
    unittest.main()