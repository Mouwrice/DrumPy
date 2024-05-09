from typing import Self

from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark  # pyright: ignore

from drumpy.drum.drum import Drum
from drumpy.drum.sound import SnareDrum, HiHat, KickDrum, HiHatFoot, Cymbal
from drumpy.tracking.marker_tracker_wrapper import MarkerTrackerWrapper, Foot, Hand


class DrumTrackers:
    """
    Class that contains the drum and trackers for the hands and feet
    Objects of this class are used to update the positions of the trackers
    """

    def __init__(self) -> None:
        snare_drum = SnareDrum()
        hi_hat = HiHat()
        kick_drum = KickDrum()
        hi_hat_foot = HiHatFoot()
        cymbal = Cymbal()

        self.drum = Drum([snare_drum, hi_hat, kick_drum, cymbal])
        self.drum.auto_calibrate()

        self.trackers: list[MarkerTrackerWrapper] = [
            Hand.left_hand(self.drum, [snare_drum, hi_hat, cymbal]),
            Hand.right_hand(self.drum, [snare_drum, hi_hat, cymbal]),
            Foot.left_foot(self.drum, [hi_hat_foot]),
            Foot.right_foot(self.drum, [kick_drum]),
        ]

    def update(
        self: Self, markers: list[NormalizedLandmark], timestamp_ms: float
    ) -> None:
        for tracker in self.trackers:
            tracker.update(markers, timestamp_ms)
