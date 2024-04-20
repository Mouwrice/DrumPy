from typing import Self

from mediapipe.tasks.python.components.containers.landmark import Landmark  # pyright: ignore

from drumpy.drum.drum import Drum
from drumpy.drum.sound import SnareDrum, HiHat, KickDrum
from drumpy.tracking.marker_tracker_wrapper import MarkerTrackerWrapper, DrumStick, Foot


class DrumTrackers:
    """
    Class that contains the drum and trackers for the hands and feet
    Objects of this class are used to update the positions of the trackers
    """

    def __init__(self) -> None:
        snare_drum = SnareDrum()
        hi_hat = HiHat()
        kick_drum = KickDrum()

        self.drum = Drum([snare_drum, hi_hat, kick_drum])
        self.drum.auto_calibrate()

        self.trackers: list[MarkerTrackerWrapper] = [
            DrumStick.left_hand(self.drum, [snare_drum, hi_hat]),
            DrumStick.right_hand(self.drum, [snare_drum, hi_hat]),
            Foot.left_foot(self.drum, [kick_drum]),
            Foot.right_foot(self.drum, [kick_drum]),
        ]

    def update(self: Self, markers: list[Landmark]) -> None:
        for tracker in self.trackers:
            tracker.update(markers)
