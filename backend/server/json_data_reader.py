from backend.server.video import Video
from backend.server.word import Word
from backend.server.line import Line
from backend.server.frame import Frame
from typing import List
import json

def json_data_reader() -> List['Frame']:



                all_frames.append(Line(line['text'], bb, wl))