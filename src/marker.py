from statistics import mean

from sound import Sound


class Marker(object):
    def __init__(self, label: str, index: int, sounds: list[Sound], memory: int = 15, downward_trend: float = -2,
                 upward_trend: float = 1):
        self.label = label
        # index is the index of the marker in the QTM project
        # because the python SDK is made by baboons, the label is not available
        self.index = index

        self.sounds: list[Sound] = sounds

        # keep track of the last 10 velocities on the z-axis
        self.velocities = []

        # keep track of the last 10 positions
        self.positions = []

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

    def update(self, position: tuple[float, float, float]):
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
            print("Hit detected: {}".format(self))
            # print("Velocity: {} {}".format(self.velocities, mean(self.velocities[:-self.look_ahead])))
            self.find_and_play_sound(self.positions[-self.look_ahead])

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

        avg_z_vel = mean(self.velocities[:-self.look_ahead])
        avg_z_look_ahead = mean(self.velocities[-self.look_ahead:])

        return (avg_z_vel < self.downward_trend and avg_z_look_ahead > self.upward_trend
                and self.time_until_next_hit == 0)

    def find_and_play_sound(self, position: tuple[float, float, float]):
        """
        Plays the sound that is closest to the given position
        :param position:
        """
        closest_sound = None
        closest_distance = float("inf")
        for sound in self.sounds:
            if distance := sound.is_hit(position) is not None:
                if distance < closest_distance:
                    closest_sound = sound
                    closest_distance = distance

        if closest_sound is not None:
            closest_sound.hit(position)

    def __str__(self):
        return "{}: \n{}  {}".format(self.label, self.positions[-1], self.velocities[-1])
