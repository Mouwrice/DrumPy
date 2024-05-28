import csv
from typing import Optional, Self

from drumpy.pose.landmark_type import LandmarkType


class TrajectoryFile:
    """
    Class to read and write the captured data to a CSV file.
    """

    def __init__(self, path: str) -> None:
        fieldnames = [
            "frame",
            "time",
            "index",
            "x",
            "y",
            "z",
            "visibility",
            "presence",
            "landmark_type",
        ]
        self.file = open(path, "w", newline="")  # noqa: SIM115
        self.writer = csv.DictWriter(self.file, fieldnames=fieldnames)
        self.writer.writeheader()

    def write(
        self: Self,
        frame: int,
        time: int,
        index: int,
        x: float,
        y: float,
        z: float,
        landmark_type: LandmarkType,
        visibility: Optional[float] = None,
        presence: Optional[float] = None,
    ) -> None:
        """
        Write a line to the CSV file
        """
        self.writer.writerow(
            {
                "frame": frame,
                "time": time,
                "index": index,
                "x": x,
                "y": y,
                "z": z,
                "visibility": visibility,
                "presence": presence,
                "landmark_type": landmark_type.value,
            }
        )

    def close(self: Self) -> None:
        self.file.flush()
        self.file.close()
