from statistics import mean

import numpy as np
import numpy.typing as npt

from src.drum import Drum


class MarkerTracker:
    """
    A tracker keeps track of the markers on the body and determines when a hit is registered.
    """

    def __init__(
        self,
        label: str,
        sounds: list[int],
        drum: Drum,
        memory: int = 15,
        downward_trend: float = -2,
        upward_trend: float = 1,
    ):
        self.label = label

        # the sounds that can be played by this marker
        # sounds are identified by their index in the drum
        self.sounds: list[int] = sounds

        # keep track of the last 10 velocities on the z-axis
        self.velocities = []

        # keep track of the last 10 positions
        self.positions: [npt.NDArray[np.float64]] = []

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

        # clustering the hit positions
        self.hits = dict()

        self.drum = drum

    def update(self, position: npt.NDArray[np.float64]):
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
            hit = self.positions[-self.look_ahead]
            pos_tuple = (hit[0], hit[1], hit[2])
            self.register_hit(pos_tuple)

            self.time_until_next_hit = self.memory
            self.drum.find_and_play_sound(
                self.positions[-self.look_ahead], self.label, self.sounds
            )

    def register_hit(self, position: tuple[float, float, float]):
        closest_hit = None
        closest_distance = float("inf")
        for key in self.hits:
            distance = np.linalg.norm(np.array(key) - np.array(position))
            if distance < closest_distance and distance < 100:
                closest_hit = key
                closest_distance = distance

        if closest_hit is not None:
            occurrences = self.hits[closest_hit]
            # create a new element with the new updated average position
            new_key = (occurrences * np.array(closest_hit) + np.array(position)) / (
                occurrences + 1
            )
            new_key = tuple(new_key)
            self.hits[new_key] = occurrences + 1
            del self.hits[closest_hit]
        else:
            self.hits[position] = 1

    def get_velocity(self) -> float:
        if len(self.positions) < 2:
            return 0

        return self.positions[-1][2] - self.positions[-2][2]

    def is_hit(self) -> bool:
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

    def __str__(self):
        return "{}: \n{}  {}".format(
            self.label, self.positions[-1], self.velocities[-1]
        )
