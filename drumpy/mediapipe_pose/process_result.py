from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark
from mediapipe.tasks.python.vision import PoseLandmarkerResult


class ResultProcessor:
    """
    Process the result of the pose estimation.
    Tries to predict the position of the result based on the previous positions.
    The more plausible the positions are, the more likely the result is correct.
    Major deviations from the previous positions are considered outliers and will be corrected.
    """

    def __init__(self, memory: int = 5, threshold: float = 0.08) -> None:
        self.memory: int = memory
        self.threshold: float = threshold
        self.results: list[PoseLandmarkerResult] = []
        self.timestamps_ms: list[float] = []  # timestamps of the results, in ms
        self.time_deltas_ms: list[float] = []  # time deltas between the results, in ms
        self.time_duration_ms: float = 0.0  # duration of the time deltas, in ms

    def process_result(
        self, result: PoseLandmarkerResult, timestamp_ms: float
    ) -> PoseLandmarkerResult:
        """
        Process the result of the pose estimation
        """
        for i, landmark in enumerate(result.pose_landmarks[0]):
            result.pose_landmarks[0][i] = self.process_normalized_landmark(
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

    def process_normalized_landmark(
        self, landmark: NormalizedLandmark, index: int, timestamp_ms: float
    ) -> NormalizedLandmark:
        if len(self.results) < 2:  # noqa: PLR2004
            return landmark

        # Calculate the average difference between the current and previous positions
        diffs = [
            self.calculate_diff(
                self.results[i].pose_landmarks[0][index],  # current position
                self.results[i - 1].pose_landmarks[0][index],  # previous position
            )
            for i in range(1, len(self.results))
        ]

        # Calculate the average difference over time
        # The average difference is the average movement of the landmark per millisecond
        avg_diff = NormalizedLandmark()
        avg_diff.x = sum(diff.x for diff in diffs) / self.time_duration_ms
        avg_diff.y = sum(diff.y for diff in diffs) / self.time_duration_ms
        avg_diff.z = sum(diff.z for diff in diffs) / self.time_duration_ms

        # Predict the current position by adding the average difference to the previous position
        # This is the expected position of the landmark based on the previous positions
        predicted = NormalizedLandmark()
        time_delta = timestamp_ms - self.timestamps_ms[-1]
        predicted.x = (
            self.results[-1].pose_landmarks[0][index].x + avg_diff.x * time_delta
        )
        predicted.y = (
            self.results[-1].pose_landmarks[0][index].y + avg_diff.y * time_delta
        )
        predicted.z = (
            self.results[-1].pose_landmarks[0][index].z + avg_diff.z * time_delta
        )
        # print(f"Predicted: {predicted.x}, {predicted.y}, {predicted.z}")
        # print(f"Current: {landmark.x}, {landmark.y}, {landmark.z}\n")

        # Calculate the difference between the predicted and current position
        diff = self.calculate_diff(landmark, predicted)

        # If the difference is too large, the current position is considered an outlier
        # The current position is corrected by the predicted position
        if abs(diff.x) > self.threshold:
            print(f"Corrected x: {landmark.x} -> {predicted.x}")
            landmark.x = predicted.x
        if abs(diff.y) > self.threshold:
            print(f"Corrected y: {landmark.y} -> {predicted.y}")
            landmark.y = predicted.y
        if abs(diff.z) > self.threshold:
            # print(f"Corrected z: {landmark.z} -> {predicted.z}")
            landmark.z = predicted.z

        return landmark

    @staticmethod
    def calculate_diff(
        current: NormalizedLandmark, previous: NormalizedLandmark
    ) -> NormalizedLandmark:
        """
        Calculate the difference between the current and previous positions
        """
        diff = NormalizedLandmark()
        diff.x = current.x - previous.x
        diff.y = current.y - previous.y
        diff.z = current.z - previous.z
        return diff
