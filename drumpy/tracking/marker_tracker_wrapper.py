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
        self,
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
        wrist_pos = landmark_to_position(markers[self.wrist])
        pinky_pos = landmark_to_position(markers[self.pinky])
        index_pos = landmark_to_position(markers[self.index])

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
    def __init__(self, toe_tip: MarkerEnum, drum: Drum, sounds: list[Sound]) -> None:
        self.toe_tip = toe_tip
        self.position: Position = np.array([0, 0, 0])
        self.tracker = MarkerTracker(
            MarkerEnum.LEFT_FOOT_INDEX,
            drum=drum,
            sounds=sounds,
            downward_trend=-0.003,
            upward_trend=0.0,
        )

    def update(self: Self, markers: list[Landmark]) -> None:
        self.position = landmark_to_position(markers[self.toe_tip])

        self.tracker.update(self.position)

    @staticmethod
    def left_foot(drum: Drum, sounds: list[Sound]) -> MarkerTrackerWrapper:
        return Foot(MarkerEnum.LEFT_FOOT_INDEX, drum, sounds)

    @staticmethod
    def right_foot(drum: Drum, sounds: list[Sound]) -> MarkerTrackerWrapper:
        return Foot(MarkerEnum.RIGHT_FOOT_INDEX, drum, sounds)


class Hand(MarkerTrackerWrapper):
    def __init__(self, wrist: MarkerEnum, drum: Drum, sounds: list[Sound]) -> None:
        self.wrist = wrist
        self.position: Position = np.array([0, 0, 0])
        self.tracker = MarkerTracker(wrist, drum=drum, sounds=sounds)

    def update(self: Self, markers: list[Landmark]) -> None:
        self.position = landmark_to_position(markers[self.wrist])

        self.tracker.update(self.position)

    @staticmethod
    def left_hand(drum: Drum, sounds: list[Sound]) -> MarkerTrackerWrapper:
        return Hand(MarkerEnum.LEFT_WRIST, drum, sounds)

    @staticmethod
    def right_hand(drum: Drum, sounds: list[Sound]) -> MarkerTrackerWrapper:
        return Hand(MarkerEnum.RIGHT_WRIST, drum, sounds)
