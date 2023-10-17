import numpy as np
import pygame


class Sound:
    """
    Represents a part of the drum kit.
    When a hit is registered, the marker has to look at the possible sounds that can be played, and find the
    closest one to hit impact.
    """

    def __init__(self, path: str, position: tuple[float, float, float]):
        self.sound = pygame.mixer.Sound(path)

        self.position = np.array(position)

        # the maximum and minimum distance from the sound to the hit that we allow
        self.min_margin: float = 100
        self.margin: float = 300  # the current margin will move towards the minimum margin over time

    def is_hit(self, position: tuple[float, float, float]) -> None | float:
        """
        Returns whether the given position is close enough to the sound to be considered a hit
        :param position:
        :return: None if the position is not close enough, otherwise the distance to the sound
        """
        distance = np.linalg.norm(np.array(self.position) - np.array(position))
        if distance < self.margin:
            return distance

        return None

    def hit(self, position: tuple[float, float, float]):
        """
        Update the position of the sound slowly to the given position and play it
        :param position:
        :return:
        """
        self.sound.play()
        self.position = 0.99 * np.array(self.position) + 0.01 * np.array(position)
        self.margin = max(self.min_margin, 0.99 * self.margin)
