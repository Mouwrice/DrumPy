class CSVRow:
    """
    Represents a single row of a CSV file
    """

    def __init__(
        self,
        frame: int,
        time: int,
        index: int,
        x: float,
        y: float,
        z: float,
        visibility: float | None,
        presence: float | None,
        normalized: bool,
    ):
        """Class for storing a row of a CSV file"""
        self.frame: int = frame
        self.time: int = time
        self.index: int = index
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.visibility: float | None = visibility
        self.presence: float | None = presence
        self.normalized: bool = normalized

    @staticmethod
    def parse_row(row):
        frame = int(row["frame"])
        time = int(row["time"])
        index = int(row["index"])
        x = float(row["x"])
        y = float(row["y"])
        z = float(row["z"])
        visibility = row["visibility"]
        presence = row["presence"]
        normalized = row["normalized"]

        return CSVRow(frame, time, index, x, y, z, visibility, presence, normalized)
