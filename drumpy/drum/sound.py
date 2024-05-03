from enum import IntEnum
from typing import Self, Optional

import numpy as np
import pygame
from termcolor import cprint

from drumpy.util import position_str, Position, distance_no_depth

MARGIN = 0.15  # 20 cm, the margin that the sound can be hit with
MIN_HIT_COUNT = 10


class SoundState(IntEnum):
    UNINITIALIZED = 0
    READY = 1
    CALIBRATING = 2


class Sound:
    """
    Represents a part of the drum kit.
    The Sound can be in one of three states:
    UNINITIALIZED: The sound has not been hit yet
    READY: The sound is ready to be hit
    CALIBRATING: The sound is being calibrated

    The sound can be hit with a position, which will update the position of the sound towards the given position
    """

    def __init__(
        self,
        name: str,
        path: str,
        margin: float,
        position: Optional[Position] = None,
        velocity_multiplier: float = 20,
    ) -> None:
        """
        Initialize the sound
        :param name: The name of the sound
        :param path: The path to the sound file
        :param margin: The accepted distance to the sound, aka the sound radius
        :param position: The initial position of the sound, if None the sound will be uninitialized
        """
        self.name = name
        self.sound = pygame.mixer.Sound(path)

        self.position: Position = (
            position if position is not None else np.array([0, 0, 0])
        )
        self.state: SoundState = (
            SoundState.READY if position is not None else SoundState.UNINITIALIZED
        )

        # the number of hits that have been registered
        self.hit_count = 0
        self.hits: list[Position] = []

        self.velocity_multiplier = velocity_multiplier

        # the margin that the sound can be hit with, aka the distance to the sound, or the size of the sound area
        self.margin: float = margin

    def calibrate(self: Self) -> None:
        """
        Set the sound to calibrate mode
        """
        cprint("\n{} calibration start".format(self.name), color="blue", attrs=["bold"])
        self.state = SoundState.CALIBRATING
        self.hit_count = 0
        self.hits = []
        self.position = np.array([0, 0, 0])

    def is_hit(self: Self, position: Position) -> Optional[float]:
        """
        Returns whether the given position is close enough to the sound to be considered a hit.
        If the sound position is being calibrated, the position is automatically set to running average of the hits
        :param position: The position of the hit
        :return: None if the position is not close enough, otherwise the distance to the sound
        """
        match self.state:
            case SoundState.UNINITIALIZED:
                return None

            case SoundState.CALIBRATING:
                self.hits.append(position)
                mean_position = np.mean(self.hits, axis=0)
                self.position = mean_position
                distance = distance_no_depth(mean_position, position)

                # the sound is calibrated when the position is stable and the hit count is high enough
                if self.hit_count >= MIN_HIT_COUNT and distance <= self.margin:
                    self.state = SoundState.READY
                    cprint(
                        f"\n{self.name} calibration done", color="green", attrs=["bold"]
                    )
                else:
                    cprint(f"\nCalibrating {self.name}", color="blue")

                print(f"\tPosition: {position_str(self.position)}")
                print(f"\tHit count: {self.hit_count}")

                return distance

            case SoundState.READY:
                distance = distance_no_depth(self.position, position)
                if distance < self.margin:
                    return distance
                return None

    def hit(self: Self, position: Position, velocity: float) -> None:
        """
        Update the position of the sound slowly to the given position and play it
        :param position: The position of the hit
        :param velocity: The velocity of the hit, used to determine the volume of the sound
        """
        # print(f"\n{self.name} hit at {position_str(position)} with velocity {velocity}")
        volume = min(1.0, max(0.0, abs(velocity) * self.velocity_multiplier))
        self.sound.set_volume(volume)
        self.sound.play()
        self.hit_count += 1
        self.position = 0.99 * self.position + 0.01 * position


class SnareDrum(Sound):
    def __init__(self) -> None:
        super().__init__(
            "Snare Drum",
            "./resources/sounds/CKV1_Snare Loud.wav",
            margin=MARGIN,
            velocity_multiplier=20,
        )


class HiHat(Sound):
    def __init__(self) -> None:
        super().__init__(
            "High Hat",
            "./resources/sounds/CKV1_HH Closed Loud.wav",
            margin=MARGIN,
            velocity_multiplier=20,
        )


class KickDrum(Sound):
    def __init__(self) -> None:
        super().__init__(
            "Kick Drum",
            "./resources/sounds/CKV1_Kick Loud.wav",
            margin=MARGIN,
            velocity_multiplier=40,
        )


class HiHatFoot(Sound):
    def __init__(self) -> None:
        super().__init__(
            "High Hat Foot",
            "./resources/sounds/CKV1_HH Foot.wav",
            margin=MARGIN,
            velocity_multiplier=40,
        )


class Tom1(Sound):
    def __init__(self) -> None:
        super().__init__(
            "Tom 1",
            "./DrumSamples/Tom1.wav",
            margin=MARGIN,
            velocity_multiplier=20,
        )


class Tom2(Sound):
    def __init__(self) -> None:
        super().__init__(
            "Tom 2",
            "./resources/sounds/Tom2.wav",
            margin=MARGIN,
            velocity_multiplier=20,
        )


class Cymbal(Sound):
    def __init__(self) -> None:
        super().__init__(
            "Cymbal",
            "./resources/sounds/Hop_Crs.wav",
            margin=MARGIN,
            velocity_multiplier=20,
        )
