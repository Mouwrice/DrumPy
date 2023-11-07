import numpy as np

from marker import Marker
from tracker.marker_tracker import MarkerTracker


class Foot:
    def __init__(self, toe_tip: Marker, tracker: MarkerTracker):
        self.toe_tip: Marker = toe_tip
        self.pos: np.array = np.array([0, 0, 0])
        self.tracker = tracker

    def update(self, markers):
        self.toe_tip.pos = np.array(markers[self.toe_tip.index])
        self.pos = self.toe_tip.pos

        self.tracker.update((self.pos[0], self.pos[1], self.pos[2]))
