import numpy as np

from marker import Marker, Tracker


class Foot:
    def __init__(self, toe_tip: Marker, tracker: Tracker):
        self.toe_tip: Marker = toe_tip
        self.pos: np.array = np.array([0, 0, 0])
        self.tracker = tracker

    def update(self, markers):
        self.toe_tip.pos = np.array(markers[self.toe_tip.index])
        self.pos = self.toe_tip.pos

        self.tracker.update((self.pos[0], self.pos[1], self.pos[2]))
