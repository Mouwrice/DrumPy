import csv

from bokeh.io import show, output_file
from bokeh.plotting import figure

qtm_to_mediapipe = {
    0: 19,  # left index
    1: 15,  # left wrist
    2: 20,  # right index
    3: 16,  # right wrist
    4: 31,  # left foot index
    5: 32,  # right foot index
}


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


def plot_positions(positions: list[list[CSVRow]], markers: list[int] = None):
    """
    Plot the positions of the markers over time
    :param markers: Filter for markers, if None all markers are plotted, else only the markers in the list are plotted
    :param positions:
    :return:
    """

    if markers is None:
        markers = range(len(positions[0]))
    for i in markers:
        plot = figure(title=f"Position of marker {i} over time", x_axis_label='Frame', y_axis_label='Position',
                      sizing_mode="stretch_both")
        plot.line(list(range(len(positions))), [position[i].x for position in positions], legend_label="x",
                  line_color="red")
        plot.line(list(range(len(positions))), [position[i].y for position in positions], legend_label="y",
                  line_color="green")
        plot.line(list(range(len(positions))), [position[i].z for position in positions], legend_label="z",
                  line_color="blue")
        output_file(f"marker_{i}.html")
        show(plot)


def plot_distances(distances: list[list[float]], mapping: list[int] = None):
    """
    Plot the distances between markers over time
    :param distances:
    :return:
    """
    plot = figure(title="Distance between markers over time", x_axis_label='Frame', y_axis_label='Distance',
                  sizing_mode="stretch_both")
    colors = ["red", "blue", "green", "orange", "purple", "brown", "pink", "gray", "black"]
    for i in range(len(distances[0])):
        plot.line(list(range(len(distances))), [distance[i] for distance in distances],
                  legend_label=f"Marker {i}-{mapping[i]}",
                  line_color=colors[i % len(colors)])
    output_file("distances.html")
    show(plot)


def row_distance(row1: CSVRow, row2: CSVRow) -> float:
    """
    Calculate the distance between two rows
    :param row1:
    :param row2:
    :return:
    """
    return ((row1.x - row2.x) ** 2 + (row1.y - row2.y) ** 2 + (row1.z - row2.z) ** 2) ** 0.5


def compare_and_plot_csv_files(csv1: str, csv2: str, frame_offset1: int = 0, frame_offset2: int = 0,
                               mapping: dict = None):
    """
    Compare two CSV files and plot the differences
    :param csv1: path to the first CSV file
    :param csv2: path to the second CSV file
    :param frame_offset1: offset for the first CSV file
    :param frame_offset2: offset for the second CSV file
    :param mapping: mapping from trackers of the first CSV file to the second CSV file
    if None, all trackers are compared based on their index
    """
    frames1 = into_frames(csv1)
    frames2 = into_frames(csv2)

    frames1_index = frame_offset1
    frames2_index = frame_offset2
    time_offset = frames1[frames1_index].time_ms - frames2[frames2_index].time_ms

    distances = []

    frame1 = frames1[frames1_index]
    frame2 = frames2[frames2_index]
    positions1 = []
    positions2 = []
    while frames1_index < len(frames1) - 1 and frames2_index < len(frames2) - 1:
        frame1_next = frames1[frames1_index + 1]
        frame2_next = frames2[frames2_index + 1]
        frame2_offset_time = frame2.time_ms + time_offset
        if frame1.time_ms < frame2_offset_time:
            frames1_index += 1
            frame1 = frame1_next
        elif frame1.time_ms > frame2_offset_time:
            frames2_index += 1
            frame2 = frame2_next
        else:
            frames1_index += 1
            frames2_index += 1
            frame1 = frame1_next
            frame2 = frame2_next

        positions1.append(frame1.rows)
        positions2.append(frame2.rows)

        if mapping is None:
            frame_distances = []
            for i in range(min(len(frame1.rows), len(frame2.rows))):
                row1 = frame1.rows[i]
                row2 = frame2.rows[i]
                distance = row_distance(row1, row2)
                frame_distances.append(distance)
                # print(f"Frame: {frame1.frame}, Marker: {row1.index}, "
                #       f"Distance: {distance}")
            distances.append(frame_distances)
        else:
            frame_distances = []
            for key, value in mapping.items():
                row1 = frame1.rows[key]
                row2 = frame2.rows[value]
                distance = row_distance(row1, row2)
                frame_distances.append(distance)
                # print(f"Frame: {frame1.frame}, Marker: {row1.index} - {row2.index}, "
                #       f"Distance: {distance}")
            distances.append(frame_distances)

        # print(f"Frame: {frame1.frame}, Time: {frame1.time_ms}, Time: {frame2.time_ms + time_offset}")
        # print()
    plot_positions(positions1, markers=[0, 1, 2, 3, 4, 5])
    plot_positions(positions2, markers=[19])
    plot_distances(distances, mapping=list(qtm_to_mediapipe.values()))


if __name__ == '__main__':
    compare_and_plot_csv_files("qtm_multicam_1.csv", "mediapipe_LITE_multicam_1_left.csv", frame_offset1=5,
                               mapping=qtm_to_mediapipe)
