import numpy as np

from marker import Marker, Tracker


class Hand:
    def __init__(self, wrist_out: Marker, hand_out: Marker, hand_in: Marker, tracker: Tracker):
        self.wrist_out: Marker = wrist_out
        self.hand_out: Marker = hand_out
        self.hand_in: Marker = hand_in

        self.tracker: Tracker = tracker

        self.position = np.array([0, 0, 0])

    def update(self, markers):
        self.wrist_out.pos = np.array(markers[self.wrist_out.index])
        self.hand_out.pos = np.array(markers[self.hand_out.index])
        self.hand_in.pos = np.array(markers[self.hand_in.index])

        direction = self.wrist_out.pos + (self.hand_in.pos - self.wrist_out.pos) + (
                self.hand_out.pos - self.wrist_out.pos)

        self.position = direction + 50

        self.tracker.update((self.position[0], self.position[1], self.position[2]))
