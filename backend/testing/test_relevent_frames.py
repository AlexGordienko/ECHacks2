from backend.server.video import Video
import unittest


class TestReleventFrames(unittest.TestCase):

    def test_relevant_frames(self):

        new_vid = Video("insertlinkhere", "lecture1")
        new_vid.directory = "./test_vid_4.mp4"
        new_vid.fps = 30

        new_vid.parse_frames_without_saving()
        new_vid.read_preloaded_frame_data()
        new_vid.update_relevant_frames()
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