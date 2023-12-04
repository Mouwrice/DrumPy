import csv
from dataclasses import dataclass


class CSVRow:
    def __init__(self, frame: int, time: int, index: int, x: float, y: float, z: float, visibility: float | None,
                 presence: float | None, normalized: bool):
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


def parse_row(row) -> CSVRow:
    frame = int(row['frame'])
    time = int(row['time'])
    index = int(row['index'])
    x = float(row['x'])
    y = float(row['y'])
    z = float(row['z'])
    visibility = row['visibility']
    presence = row['presence']
    normalized = row['normalized']

    return CSVRow(frame, time, index, x, y, z, visibility, presence, normalized)


class Frame:
    """
    A frame consistens of multiple CSVRow, each CSVRow is a marker at a certain frame
    """

    def __init__(self):
        self.rows: list[CSVRow] = []
        self.time_ms: int = 0
        self.frame: int = 0


def into_frames(csv_file: str) -> list[Frame]:
    """
    Read a CSV file and return a list of frames
    """
    frames: list[Frame] = []
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        row = parse_row(next(reader))
        frame = Frame()
        frame.frame = row.frame
        frame.time_ms = row.time
        frame.rows.append(row)
        for row in reader:
            row = parse_row(row)
            if row.frame == frame.frame:
                frame.rows.append(row)
            else:
                frames.append(frame)
                frame = Frame()
                frame.frame = row.frame
                frame.time_ms = row.time
                frame.rows.append(row)
    return frames


def compare_and_plot_csv_files(csv1: str, csv2: str, frame_offset1: int = 0, frame_offset2: int = 0):
    """
    Compare two CSV files and plot the differences
    """
    frames1 = into_frames(csv1)
    frames2 = into_frames(csv2)

    frames1_index = frame_offset1
    frames2_index = frame_offset2
    time_offset = frames1[frames1_index].time_ms - frames2[frames2_index].time_ms

    frame1 = frames1[frames1_index]
    frame2 = frames2[frames2_index]
    while frames1_index < len(frames1) - 1 and frames2_index < len(frames2) - 1:
        frame1_next = frames1[frames1_index + 1]
        frame2_next = frames2[frames2_index + 1]
        if frame1.time_ms < frame2.time_ms + time_offset:
            frames1_index += 1
            frame1 = frame1_next
        elif frame1.time_ms > frame2.time_ms + time_offset:
            frames2_index += 1
            frame2 = frame2_next
        else:
            frames1_index += 1
            frames2_index += 1
            frame1 = frame1_next
            frame2 = frame2_next

        for row1 in frame1.rows:
            for row2 in frame2.rows:
                if row1.index == row2.index:
                    print(f"Frame: {frame1.frame}, Marker: {row1.index}, "
                          f"Distance: {((row1.x - row2.x) ** 2 + (row1.y - row2.y) ** 2 + (row1.z - row2.z) ** 2) ** 0.5}")
        print(f"Frame: {frame1.frame}, Time: {frame1.time_ms}, Time: {frame2.time_ms + time_offset}")
        print()


if __name__ == '__main__':
    compare_and_plot_csv_files("qtm_multicam_1.csv", "mediapipe_LITE_multicam_1_left.csv", frame_offset1=5)
