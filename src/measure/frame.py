import csv

from measure.csv_utils.csv_row import CSVRow


class Frame:
    """
    A frame consistens of multiple CSVRow, each CSVRow is a marker at a certain frame
    """

    def __init__(self):
        self.rows: list[CSVRow] = []
        self.time_ms: int = 0
        self.frame: int = 0

    @staticmethod
    def frames_from_csv(csv_file: str):
        """
        Read a CSV file and return a list of frames
        """
        frames: list[Frame] = []
        with open(csv_file, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            row = CSVRow.parse_row(next(reader))
            frame = Frame()
            frame.frame = row.frame
            frame.time_ms = row.time
            frame.rows.append(row)
            for row in reader:
                row = CSVRow.parse_row(row)
                if row.frame == frame.frame:
                    frame.rows.append(row)
                else:
                    frames.append(frame)
                    frame = Frame()
                    frame.frame = row.frame
                    frame.time_ms = row.time
                    frame.rows.append(row)
        return frames
