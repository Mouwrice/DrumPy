from abc import ABC, abstractmethod
from typing import Self

import numpy as np
from mediapipe.tasks.python.components.containers.landmark import Landmark  # pyright: ignore

from drumpy.drum.drum import Drum
from drumpy.drum.sound import Sound
from drumpy.mediapipe_pose.mediapipe_markers import MarkerEnum
from drumpy.tracking.marker_tracker import MarkerTracker
from drumpy.util import landmark_to_position, Position


class MarkerTrackerWrapper(ABC):
    """
    Wrapper for a `MarkerTracker` that allows for extra clarity.
    Such as Hand and Foot trackers.
    """

    @abstractmethod
    def update(self: Self, markers: list[Landmark]) -> None:
        """
        Update the tracker with the new markers
        """


class DrumStick(MarkerTrackerWrapper):
    def __init__(
        self: Self,
        wrist: MarkerEnum,
        pinky: MarkerEnum,
        index: MarkerEnum,
        tracker: MarkerTracker,
    ) -> None:
        self.wrist = wrist
        self.pinky = pinky
        self.index = index

        self.tracker = tracker

        self.position = np.array([0, 0, 0])

    def update(self: Self, markers: list[Landmark]) -> None:
        wrist_landmark = markers[self.wrist.value]
        pinky_landmark = markers[self.pinky.value]
        index_landmark = markers[self.index.value]

        wrist_pos = landmark_to_position(wrist_landmark)
        pinky_pos = landmark_to_position(pinky_landmark)
        index_pos = landmark_to_position(index_landmark)

        direction = wrist_pos + (index_pos - pinky_pos) + (pinky_pos - wrist_pos)

        # increase the length of the direction vector by 50
        self.position = wrist_pos + 50 * direction / np.linalg.norm(direction)

        self.tracker.update(self.position)

    @staticmethod
    def left_hand(drum: Drum, sounds: list[Sound]) -> MarkerTrackerWrapper:
        wrist = MarkerEnum.LEFT_WRIST
        pinky = MarkerEnum.LEFT_PINKY
        index = MarkerEnum.LEFT_INDEX

        return DrumStick(
            wrist,
            pinky,
            index,
            MarkerTracker(MarkerEnum.LEFT_DRUM_STICK, drum=drum, sounds=sounds),
        )

    @staticmethod
    def right_hand(drum: Drum, sounds: list[Sound]) -> MarkerTrackerWrapper:
        wrist = MarkerEnum.RIGHT_WRIST
        pinky = MarkerEnum.RIGHT_PINKY
        index = MarkerEnum.RIGHT_INDEX

        return DrumStick(
            wrist,
            pinky,
            index,
            MarkerTracker(MarkerEnum.RIGHT_DRUM_STICK, drum=drum, sounds=sounds),
        )


class Foot(MarkerTrackerWrapper):
    def __init__(self: Self, toe_tip: MarkerEnum, tracker: MarkerTracker) -> None:
        self.toe_tip = toe_tip
        self.position: Position = np.array([0, 0, 0])
        self.tracker = tracker

    def update(self: Self, markers: list[Landmark]) -> None:
        self.position = landmark_to_position(markers[self.toe_tip.value])

        self.tracker.update(self.position)

    @staticmethod
    def left_foot(drum: Drum, sounds: list[Sound]) -> MarkerTrackerWrapper:
        toe_tip = MarkerEnum.LEFT_FOOT_INDEX
        return Foot(
            toe_tip, MarkerTracker(MarkerEnum.LEFT_FOOT, drum=drum, sounds=sounds)
        )

    @staticmethod
    def right_foot(drum: Drum, sounds: list[Sound]) -> MarkerTrackerWrapper:
        toe_tip = MarkerEnum.RIGHT_FOOT_INDEX
        return Foot(
            toe_tip, MarkerTracker(MarkerEnum.RIGHT_FOOT, drum=drum, sounds=sounds)
        )
