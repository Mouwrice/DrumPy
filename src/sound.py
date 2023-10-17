import pygame


class Sound:
    """
    Represents a part of the drum kit.
    When a hit is registered, the marker has to look at the possible sounds that can be played, and find the
    closest one to hit impact.
    """

    def __init__(self, path: str):
        self.sound = pygame.mixer.Sound(path)
        self.position = (0, 0, 0)

    def play(self):
        self.sound.play()
