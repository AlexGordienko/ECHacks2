from backend.server.video import Video
import unittest

def test_filter_lines():

    new_vid = Video("insertlinkhere", "lecture1")
    new_vid.directory = "./test_vid_4.mp4"
    new_vid.fps = 30

    new_vid.parse_frames_without_saving()
    new_vid.read_preloaded_frame_data()
    new_vid.update_relevant_frames()

    for frame in new_vid.relevant_frames:
        frame.mark_keywords()
        frame.filter_keywords_from_lines()
        for line in frame.lines:
            print(line.text)
        print("")
        print("")

if __name__ == '__main__':
    unittest.main()