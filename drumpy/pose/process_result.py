import math

from mediapipe.tasks.python.components.containers.landmark import (
    NormalizedLandmark,
    Landmark,
)
from mediapipe.tasks.python.vision import PoseLandmarkerResult

from drumpy.pose.landmark_type import LandmarkType


class ResultProcessor:
    """
    Process the result of the pose estimation.
    Tries to predict the position of the result based on the previous positions.
    The more plausible the positions are, the more likely the result is correct.
    Major deviations from the previous positions are considered outliers and will be corrected.
    """

    def __init__(self, landmark_type: LandmarkType) -> None:
        self.landmark_type: LandmarkType = landmark_type

        self.memory: int = 2
        self.peak: float = (
            0.02  # Deviations at this value are considered completely plausible
        )
        # The mollifier function will be 1 at this value
        self.tightness: float = (
            0.7  # How tight the mollifier function is around the peak
        )
        # Higher values will make the mollifier function tighter

        self.results: list[PoseLandmarkerResult] = []
        self.timestamps_ms: list[float] = []  # timestamps of the results, in ms
        self.time_deltas_ms: list[float] = []  # time deltas between the results, in ms
        self.time_duration_ms: float = 0.0  # duration of the time deltas, in ms

    def mollifier(self, x: float) -> float:
        """
        The mollifier function
        """
        if x <= 0:
            return 0

        return math.exp((-(math.log(x / self.peak) ** 2)) * self.tightness)

    def process_result(
        self, result: PoseLandmarkerResult, timestamp_ms: float
    ) -> PoseLandmarkerResult:
        """
        Process the result of the pose estimation
        """
        if result.pose_landmarks is None or len(result.pose_landmarks) == 0:
            return result

        for i, landmark in enumerate(result.pose_landmarks[0]):
            result.pose_landmarks[0][i] = self.process_landmark(
                landmark, i, timestamp_ms
            )

        self.results.append(result)
        if len(self.results) > self.memory:
            self.results.pop(0)

        self.timestamps_ms.append(timestamp_ms)
        if len(self.timestamps_ms) > self.memory:
            self.timestamps_ms.pop(0)

        if len(self.timestamps_ms) > 1:
            time_delta = self.timestamps_ms[-1] - self.timestamps_ms[-2]
            self.time_deltas_ms.append(time_delta)
            self.time_duration_ms += time_delta
            if len(self.time_deltas_ms) > self.memory:
                self.time_duration_ms -= self.time_deltas_ms.pop(0)

        return result

    def average_difference(
        self, diffs: list[NormalizedLandmark | Landmark]
    ) -> tuple[float, float, float]:
        """
        Calculate the average difference between the current and previous positions
        The average difference is the average movement of the landmark per millisecond, in x, y, z
        """
        x = sum(diff.x for diff in diffs) / self.time_duration_ms
        y = sum(diff.y for diff in diffs) / self.time_duration_ms
        z = sum(diff.z for diff in diffs) / self.time_duration_ms
        return x, y, z

    def predict_position(
        self, avg_diff: tuple[float, float, float], index: int, timestamp_ms: float
    ) -> tuple[float, float, float]:
        """
        Predict the current position by adding the average difference to the previous position
        This is the expected position of the landmark based on the previous positions
        """

        time_delta = timestamp_ms - self.timestamps_ms[-1]
        x = self.results[-1].pose_landmarks[0][index].x + avg_diff[0] * time_delta
        y = self.results[-1].pose_landmarks[0][index].y + avg_diff[1] * time_delta
        z = self.results[-1].pose_landmarks[0][index].z + avg_diff[2] * time_delta

        return x, y, z

    def apply_mollifier(
        self,
        diff_landmark_predicted: NormalizedLandmark | Landmark,
        landmark: NormalizedLandmark | Landmark,
        predicted: NormalizedLandmark | Landmark,
    ) -> NormalizedLandmark | Landmark:
        """
        If the difference with the previous position is below the minimum deviation, smooth it out
        This is to prevent small jittering of the landmarks
        Else apply clamp the difference to be within the maximum deviation
        """
        ratio_x = self.mollifier(abs(diff_landmark_predicted.x))
        ratio_y = self.mollifier(abs(diff_landmark_predicted.y))
        ratio_z = self.mollifier(abs(diff_landmark_predicted.z))
        landmark.x = predicted.x * (1 - ratio_x) + landmark.x * ratio_x
        landmark.y = predicted.y * (1 - ratio_y) + landmark.y * ratio_y
        landmark.z = predicted.z * (1 - ratio_z) + landmark.z * ratio_z
        return landmark

    def process_landmark(
        self, landmark: NormalizedLandmark | Landmark, index: int, timestamp_ms: float
    ) -> NormalizedLandmark:
        if len(self.results) < 2:  # noqa: PLR2004
            return landmark

        # Calculate the average difference between the current and previous positions
        diffs = (
            [
                self.calculate_diff(
                    self.results[i].pose_landmarks[0][index],  # current position
                    self.results[i - 1].pose_landmarks[0][index],  # previous position
                )
                for i in range(1, len(self.results))
            ]
            if self.landmark_type == LandmarkType.LANDMARKS
            else [
                self.calculate_diff(
                    self.results[i].pose_world_landmarks[0][index],  # current position
                    self.results[i - 1].pose_world_landmarks[0][
                        index
                    ],  # previous position
                )
                for i in range(1, len(self.results))
            ]
        )

        avg_diff = self.average_difference(diffs)

        pos = self.predict_position(avg_diff, index, timestamp_ms)
        predicted = Landmark(x=pos[0], y=pos[1], z=pos[2])

        # Calculate the difference between the predicted and current position
        diff_landmark_predicted = self.calculate_diff(landmark, predicted)

        return self.apply_mollifier(diff_landmark_predicted, landmark, predicted)

    @staticmethod
    def calculate_diff(
        current: NormalizedLandmark | Landmark, previous: NormalizedLandmark | Landmark
    ) -> NormalizedLandmark:
        """
        Calculate the difference between the current and previous positions
        """
        diff = NormalizedLandmark()
        diff.x = current.x - previous.x
        diff.y = current.y - previous.y
        diff.z = current.z - previous.z
        return diff
