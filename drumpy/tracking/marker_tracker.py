from statistics import mean
from typing import Self

from drumpy.drum.drum import Drum
from drumpy.drum.sound import Sound
from drumpy.util import Position
from drumpy.mediapipe_pose.mediapipe_markers import MarkerEnum

MAX_DISTANCE = 100


class MarkerTracker:
    """
    A tracker keeps track of the markers on the body and determines when a hit is registered.
    """

    def __init__(
        self,
        marker: MarkerEnum,
        drum: Drum,
        sounds: list[Sound],
        memory: int = 15,
        downward_trend: float = -2,
        upward_trend: float = 1,
    ) -> None:
        """
        Initialize the marker tracker
        :param marker: The marker to track
        :param drum: The drum to play the sounds on
        :param sounds: The sounds that can be played by this marker
        :param memory: How many positions to keep track of
        :param downward_trend: The threshold for a downward trend on the z-axis
        :param upward_trend: The threshold for an upward trend on the z-axis
        """
        self.marker: MarkerEnum = marker

        # the sounds that can be played by this marker
        self.sounds: list[Sound] = sounds

        self.velocities: list[float] = []
        self.positions: list[Position] = []

        # time until next hit can be registered
        self.time_until_next_hit = 0

        self.memory = memory

        # how many positions to look ahead to determine if a hit is registered
        # should be smaller than memory
        self.look_ahead = 5
        assert self.look_ahead < self.memory

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
            self.time_until_next_hit = self.memory
            self.drum.find_and_play_sound(
                self.positions[-self.look_ahead], self.marker, self.sounds
            )

    def get_velocity(self: Self) -> float:
        if len(self.positions) < 2:  # noqa: PLR2004
            return 0

        return float(self.positions[-1][2]) - float(self.positions[-2][2])

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
