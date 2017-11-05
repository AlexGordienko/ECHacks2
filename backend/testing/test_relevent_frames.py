from backend.server.video import Video
import unittest
import enchant


class TestReleventFrames(unittest.TestCase):

    def test_relevant_frames(self):

        d = enchant.Dict("en_US")

        new_vid = Video("insertlinkhere", "lecture1")
        new_vid.directory = "./test_vid_4.mp4"
        new_vid.fps = 30

        new_vid.parse_frames_without_saving()
        new_vid.read_preloaded_frame_data()
        new_vid.update_relevant_frames()

        for frame in new_vid.relevant_frames:
            for line in frame.lines:
                for word in line.words:
                    print(word.text)
                    print(d.check(word.text))
                    if not d.check(word.text):
                        print(d.suggest(word.text))
        #new_vid.parse_diagram()

    def test_stats(self):
        new_vid = Video("https://youtu.be/2ceKYagf2h0", "lecture1")
        new_vid.directory = "./test_vid_4.mp4"
        new_vid.fps = 30

        new_vid.parse_frames_without_saving()
        new_vid.read_preloaded_frame_data()
        new_vid.update_relevant_frames()

        print(new_vid.compile_stats())

if __name__ == '__main__':
    unittest.main()