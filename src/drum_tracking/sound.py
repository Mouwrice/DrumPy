from enum import Enum

import numpy as np
import numpy.typing as npt
import pygame
from termcolor import cprint

from src.util import print_float_array


class SoundState(Enum):
    UNINITIALIZED = 0
    READY = 1
    CALIBRATING = 2


class Sound:
    """
    Represents a part of the drum kit.
    When a hit is registered, the marker has to look at the possible sounds that can be played, and find the
    closest one to hit impact.
    """

    def __init__(
        self,
        name: str,
        path: str,
        min_margin: float,
        margin: float,
        position: tuple[float, float, float] | None = None,
    ):
        self.name = name
        self.sound = pygame.mixer.Sound(path)

        self.position: np.ndarray = np.array([0, 0, 0])
        self.state: SoundState = SoundState.UNINITIALIZED

        if position is not None:
            self.position = np.array(position)
            self.state = SoundState.READY

        # the number of hits that have been registered
        self.hit_count = 0
        self.hits = []

        # the maximum and minimum distance from the sound to the hit that we allow
        self.min_margin: float = min_margin
        self.margin: float = (
            margin  # the current margin will move towards the minimum margin over time
        )

    def calibrate(self):
        """
        Set the sound to calibrate mode
        """
        cprint("\n{} calibration start".format(self.name), color="blue", attrs=["bold"])
        self.state = SoundState.CALIBRATING
        self.hit_count = 0
        self.hits = []
        self.position = np.array([0, 0, 0])

    def is_hit(self, position: np.array) -> None | float:
        """
        Returns whether the given position is close enough to the sound to be considered a hit.
        If the sound position is being calibrated, the position is automatically set to running average of the hits
        :param position:
        :return: None if the position is not close enough, otherwise the distance to the sound
        """
        if self.state == SoundState.UNINITIALIZED:
            return None

        if self.state == SoundState.CALIBRATING:
            self.hits.append(position)
            prev_position = self.position
            self.position = np.mean(self.hits, axis=0)

            # the sound is calibrated when the position is stable and the hit count is high enough
            if (
                np.linalg.norm(self.position - prev_position) < 0.01
                and self.hit_count > 10
            ):
                self.state = SoundState.READY
                cprint(f"\n{self.name} calibration done", color="green", attrs=["bold"])
            else:
                cprint(f"\nCalibrating {self.name}", color="blue")

            print(f"\tPosition: {print_float_array(self.position)}")
            print(f"\tHit count: {self.hit_count}")

        distance = np.linalg.norm(self.position - position)
        if distance < self.margin or self.state == SoundState.CALIBRATING:
            return distance

        return None

    def hit(self, position: npt.NDArray[np.float64]):
        """
        Update the position of the sound slowly to the given position and play it
        :param position:
        """
        self.sound.play()
        self.hit_count += 1
        self.position = 0.99 * self.position + 0.01 * position
        self.margin = max(self.min_margin, 0.99 * self.margin)
