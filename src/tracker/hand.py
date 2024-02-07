import numpy as np

from src.tracker.marker import Marker
from src.tracker.marker_tracker import MarkerTracker


class Hand:
    def __init__(
        self,
        wrist_out: Marker,
        hand_out: Marker,
        hand_in: Marker,
        tracker: MarkerTracker,
    ):
        self.wrist_out: Marker = wrist_out
        self.hand_out: Marker = hand_out
        self.hand_in: Marker = hand_in

        self.tracker: MarkerTracker = tracker

        self.position = np.array([0, 0, 0])

    def update(self, markers):
        self.wrist_out.pos = np.array(markers[self.wrist_out.index])
        self.hand_out.pos = np.array(markers[self.hand_out.index])
        self.hand_in.pos = np.array(markers[self.hand_in.index])

        direction = (
            self.wrist_out.pos
            + (self.hand_in.pos - self.wrist_out.pos)
            + (self.hand_out.pos - self.wrist_out.pos)
        )

        # increase the length of the direction vector by 50
        self.position = self.wrist_out.pos + 50 * direction / np.linalg.norm(direction)

        self.tracker.update(self.position)
