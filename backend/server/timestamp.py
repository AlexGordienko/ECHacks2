class Timestamp:
    """Timestamp object for a video

    mins: minutes of the timestamp
    sec: seconds of the timestamp"""
    mins: int
    sec: int

    def __init__(self, mins: int, sec: int) -> None:
        """Initialize the Timestamp"""
        self.mins = mins
        self.sec = sec

    def __str__(self) -> str:
        """Prints the timestamp"""
        return str(self.mins) + 'm' + str(self.sec) + 's'

    def to_secs(self) -> int:
        """Takes Timestamp and converts it to seconds"""
        return self.mins * 60 + self.sec
