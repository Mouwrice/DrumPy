from enum import Enum

import numpy as np
import pygame


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

    def __init__(self, name: str, path: str, position: tuple[float, float, float] | None = None):
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
        self.min_margin: float = 100
        self.margin: float = 300  # the current margin will move towards the minimum margin over time

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
            self.position = np.mean(self.hits, axis=0)

            # if we have enough hits, we can stop calibrating
            if len(self.hits) > 10:
                self.state = SoundState.READY

        distance = np.linalg.norm(self.position - position)
        if distance < self.margin:
            return distance

        return None

    def hit(self, position: np.array):
        """
        Update the position of the sound slowly to the given position and play it
        :param position:
        :return:
        """
        self.sound.play()
        self.hit_count += 1
        self.position = 0.99 * self.position + 0.01 * position
        self.margin = max(self.min_margin, 0.99 * self.margin)
