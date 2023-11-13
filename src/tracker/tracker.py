from abc import ABC


class Tracker(ABC):
    def __init__(self):
        self.left_hand = None
        self.right_hand = None
        self.left_foot = None
        self.right_foot = None

    async def start_capture(self):
        """
        Start streaming frames from a tracking source
        :return:
        """

    def stop_capture(self):
        """
        Stop streaming frames from a tracking source
        :return:
        """
