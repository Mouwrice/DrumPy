from statistics import mean
from typing import Self

from drumpy.drum.sound import Sound
from drumpy.drum.drum import Drum
from drumpy.util import Position

MAX_DISTANCE = 100


class MarkerTracker:
    """
    A tracker keeps track of the markers on the body and determines when a hit is registered.
    """

    def __init__(
        self: Self,
        label: str,
        drum: Drum,
        sounds: list[Sound],
        memory: int = 15,
        downward_trend: float = -2,
        upward_trend: float = 1,
    ) -> None:
        self.label = label

        # the sounds that can be played by this marker
        self.sounds: list[Sound] = sounds

        # keep track of the last 10 velocities on the z-axis
        self.velocities = []

        # keep track of the last 10 positions
        self.positions: list[Position] = []

        # time until next hit can be registered
        self.time_until_next_hit = 0

        # how many positions to keep track of
        self.memory = memory
        # how many positions to look ahead to determine if a hit is registered
        # should be smaller than memory
        self.look_ahead = 5
        assert self.look_ahead < self.memory

        # thresholds for registering a hit
        self.downward_trend = downward_trend
        self.upward_trend = upward_trend

        self.drum = drum

    def update(self: Self, position: Position) -> None:
        if self.time_until_next_hit > 0:
            self.time_until_next_hit -= 1

        # add the new position to the list of positions
        self.positions.append(position)
        if len(self.positions) > self.memory:
            self.positions.pop(0)

        velocity = self.get_velocity()
        self.velocities.append(velocity)
        if len(self.velocities) > self.memory:
            self.velocities.pop(0)

        if self.is_hit():
            position = self.positions[-self.look_ahead]

            self.time_until_next_hit = self.memory
            self.drum.find_and_play_sound(
                self.positions[-self.look_ahead], self.label, self.sounds
            )

    def get_velocity(self: Self) -> float:
        if len(self.positions) < 2:  # noqa: PLR2004
            return 0

        return self.positions[-1][2] - self.positions[-2][2]

    def is_hit(self: Self) -> bool:
        """
        A hit occurs when the z-axis has a downward trend followed by an upward trend
        :return:
        """
        if len(self.positions) < self.memory:
            return False

        if len(self.velocities) < self.look_ahead:
            return False

        avg_z_vel = mean(self.velocities[: -self.look_ahead])
        avg_z_look_ahead = mean(self.velocities[-self.look_ahead :])

        return (
            avg_z_vel < self.downward_trend
            and avg_z_look_ahead > self.upward_trend
            and self.time_until_next_hit == 0
        )

    def __str__(self: Self) -> str:
        return "{}: \n{}  {}".format(
            self.label, self.positions[-1], self.velocities[-1]
        )