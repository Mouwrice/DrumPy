import csv
from typing import Optional


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
            "normalized",
        ]
        self.file = open(path, "w", newline="")
        self.writer = csv.DictWriter(self.file, fieldnames=fieldnames)
        self.writer.writeheader()

    def write(
        self,
        frame: int,
        time: int,
        index: int,
        x: float,
        y: float,
        z: float,
        visibility: Optional[float] = None,
        presence: Optional[float] = None,
        normalized: bool = False,
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
                "normalized": normalized,
            }
        )

    def close(self) -> None:
        self.file.flush()
        self.file.close()
