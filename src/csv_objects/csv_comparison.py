import csv

from bokeh.io import show, output_file
from bokeh.plotting import figure


class CSVRow:
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


def parse_row(row) -> CSVRow:
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
    with open(csv_file, newline="") as csvfile:
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


def plot_axis(
    axis1: list[float],
    axis2: list[float],
    axis: str,
    marker1: int,
    marker2: int,
    smoothing: int = 1,
    label1: str = "qtm",
    label2: str = "mediapipe",
    plot_file_prefix: str = "",
):
    """
    Plot the positions of the markers over time for a certain axis.
    Normalizes the values between 0 and 1
    :return:
    """

    if label1 == "qtm":
        axis1 = [axis / 1000 for axis in axis1]

    # smooth axis1 and axis2
    axis1 = [
        sum(axis1[i : i + smoothing]) / smoothing for i in range(len(axis1) - smoothing)
    ]
    axis2 = [
        sum(axis2[i : i + smoothing]) / smoothing for i in range(len(axis2) - smoothing)
    ]

    # get the difference between axis1 and axis2
    difference = [abs(axis1[i] - axis2[i]) for i in range(len(axis2))]
    # get the average difference
    average_difference = sum(difference) / len(difference)
    print(
        f"Average difference between {label1} {marker1} and {label2} {marker2} on axis {axis}: {average_difference}"
    )
    # get the first derivative of the difference
    difference_derivative = [
        difference[i + 1] - difference[i] for i in range(len(difference) - 1)
    ]
    difference_derivative.append(0)
    # get the average difference derivative
    average_difference_derivative = sum(difference_derivative) / len(
        difference_derivative
    )
    print(
        f"Average difference derivative between {label1} {marker1} and {label2} {marker2} on axis {axis}: "
        f"{average_difference_derivative}"
    )

    title = f"{plot_file_prefix}_{label1}_{marker1}_{label2}_{marker2}_{axis}_positions"

    plot = figure(
        title=title,
        x_axis_label="Frame",
        y_axis_label="Position",
        sizing_mode="stretch_both",
    )
    plot.line(list(range(len(axis1))), axis1, legend_label=label1, line_color="red")
    plot.line(list(range(len(axis2))), axis2, legend_label=label2, line_color="blue")
    # plot.line(list(range(len(axis2))), difference_derivative, legend_label="difference derivative", line_color="black")
    output_file(f"{title}.html")
    show(plot)


def plot_positions(
    positions1: list[list[CSVRow]],
    positions2: list[list[CSVRow]],
    marker1: int,
    marker2: int,
    label1: str = "qtm",
    label2: str = "mediapipe",
    smoothing: int = 1,
    plot_file_prefix: str = "",
):
    """
    Plot the positions of the markers over time
    """
    positions1 = [position[marker1] for position in positions1]
    positions2 = [position[marker2] for position in positions2]
    assert len(positions1) == len(
        positions2
    ), "Length of positions1 is not equal to length of positions2"

    x1 = []
    y1 = []
    z1 = []
    x2 = []
    y2 = []
    z2 = []
    for i in range(len(positions1)):
        x1.append(positions1[i].x)
        y1.append(positions1[i].y)
        z1.append(positions1[i].z)
        if label2 == "mediapipe":  # mediapipe has z mirrored
            x2.append(-positions2[i].x - 0.7)
            y2.append(positions2[i].y)
            z2.append(-positions2[i].z + 0.6)
        else:
            x2.append(positions2[i].x)
            y2.append(positions2[i].y)
            z2.append(positions2[i].z)

    plot_axis(
        x1,
        x2,
        "x",
        marker1,
        marker2,
        smoothing,
        label1,
        label2,
        plot_file_prefix=plot_file_prefix,
    )
    plot_axis(
        y1,
        y2,
        "y",
        marker1,
        marker2,
        smoothing,
        label1,
        label2,
        plot_file_prefix=plot_file_prefix,
    )
    plot_axis(
        z1,
        z2,
        "z",
        marker1,
        marker2,
        smoothing,
        label1,
        label2,
        plot_file_prefix=plot_file_prefix,
    )


def row_distance(row1: CSVRow, row2: CSVRow) -> float:
    return (
        (row1.x - row2.x) ** 2 + (row1.y - row2.z) ** 2 + (row1.z - row2.y) ** 2
    ) ** 0.5


def get_closest_frame_index(frames: list[Frame], frame: int) -> int:
    """
    Get the index of the frame with the closest frame number
    :param frames:
    :param frame:
    :return:
    """
    found = min(range(len(frames)), key=lambda i: abs(frames[i].frame - frame))
    print(f"Found frame {frames[found].frame} at index {found}")
    return found


def compare_and_plot_csv_files(
    csv1: str,
    csv2: str,
    start1: int,
    start2: int,
    mapping: dict = None,
    plot_file_prefix: str = "",
    label1: str = "qtm",
    label2: str = "mediapipe",
):
    """
    Compare two CSV files and plot the differences
    :param plot_file_prefix: Prefix for the plot file
    :param csv1: path to the first CSV file
    :param csv2: path to the second CSV file
    :param start1: start frame of the first CSV file
    :param start2: start frame of the second CSV file
    :param mapping: mapping from trackers of the first CSV file to the second CSV file
    if None, all trackers are compared based on their index
    """
    frames1 = into_frames(csv1)
    frames2 = into_frames(csv2)

    assert len(frames1) > 0, "No frames found in CSV file 1"
    assert len(frames2) > 0, "No frames found in CSV file 2"
    assert (
        start1 >= frames1[0].frame
    ), "Start frame 1 is smaller than the first frame in the CSV file 1"
    assert (
        start2 >= frames2[0].frame
    ), "Start frame 2 is smaller than the first frame in the CSV file 2"

    frames1_index = get_closest_frame_index(frames1, start1)
    frames2_index = get_closest_frame_index(frames2, start2)
    frames1_time_offset = frames1[frames1_index].time_ms
    frames2_time_offset = frames2[frames2_index].time_ms

    frame1 = frames1[frames1_index]
    frame2 = frames2[frames2_index]
    positions1 = []
    positions2 = []
    while frames1_index < len(frames1) - 1 and frames2_index < len(frames2) - 1:
        frame1_next = frames1[frames1_index + 1]
        frame2_next = frames2[frames2_index + 1]
        frame1_time = frame1.time_ms - frames1_time_offset
        frame2_time = frame2.time_ms - frames2_time_offset
        if frame1_time < frame2_time:
            frames1_index += 1
            frame1 = frame1_next
        elif frame1_time > frame2_time:
            frames2_index += 1
            frame2 = frame2_next
        else:
            frames1_index += 1
            frames2_index += 1
            frame1 = frame1_next
            frame2 = frame2_next

        positions1.append(frame1.rows)
        positions2.append(frame2.rows)

    for key, value in mapping.items():
        plot_positions(
            positions1,
            positions2,
            key,
            value,
            label1,
            label2,
            plot_file_prefix=plot_file_prefix,
            smoothing=1,
        )


qtm_to_mediapipe = {
    0: 15,  # left wrist
    1: 16,  # right wrist
    2: 19,  # left index
    3: 20,  # right index
    4: 31,  # left foot index
    5: 32,  # right foot index
}


def compare_resolutions_and_models_axil_01_front_right_wrist(mapping: dict):
    start1 = 5
    start2 = 72
    compare_and_plot_csv_files(
        "./data/multicam_asil_01/qtm_multicam_asil_01.csv",
        "./data/multicam_asil_01/mediapipe_multicam_asil_01_front_480_270_LITE_video.csv",
        start1,
        start2,
        mapping=qtm_to_mediapipe,
        plot_file_prefix="./data/multicam_asil_01/mediapipe_multicam_asil_01_front_480_270_LITE_video",
    )

    compare_and_plot_csv_files(
        "./data/multicam_asil_01/qtm_multicam_asil_01.csv",
        "./data/multicam_asil_01/mediapipe_multicam_asil_01_front_480_270_FULL_video.csv",
        start1,
        start2,
        mapping=qtm_to_mediapipe,
        plot_file_prefix="./data/multicam_asil_01/mediapipe_multicam_asil_01_front_480_270_FULL_video",
    )

    compare_and_plot_csv_files(
        "./data/multicam_asil_01/qtm_multicam_asil_01.csv",
        "./data/multicam_asil_01/mediapipe_multicam_asil_01_front_960_540_LITE_video.csv",
        start1,
        start2,
        mapping=qtm_to_mediapipe,
        plot_file_prefix="./data/multicam_asil_01/mediapipe_multicam_asil_01_front_960_540_LITE_video",
    )

    compare_and_plot_csv_files(
        "./data/multicam_asil_01/qtm_multicam_asil_01.csv",
        "./data/multicam_asil_01/mediapipe_multicam_asil_01_front_960_540_FULL_video.csv",
        start1,
        start2,
        mapping=qtm_to_mediapipe,
        plot_file_prefix="./data/multicam_asil_01/mediapipe_multicam_asil_01_front_960_540_FULL_video",
    )

    compare_and_plot_csv_files(
        "./data/multicam_asil_01/qtm_multicam_asil_01.csv",
        "./data/multicam_asil_01/mediapipe_multicam_asil_01_front_1440_810_LITE_video.csv",
        start1,
        start2,
        mapping=qtm_to_mediapipe,
        plot_file_prefix="./data/multicam_asil_01/mediapipe_multicam_asil_01_front_1440_810_LITE_video",
    )

    compare_and_plot_csv_files(
        "./data/multicam_asil_01/qtm_multicam_asil_01.csv",
        "./data/multicam_asil_01/mediapipe_multicam_asil_01_front_1440_810_FULL_video.csv",
        start1,
        start2,
        mapping=qtm_to_mediapipe,
        plot_file_prefix="./data/multicam_asil_01/mediapipe_multicam_asil_01_front_1440_810_FULL_video",
    )


def compare_resolutions():
    """
    Compare the resolutions of the mediapipe models
    """
    mapping = {16: 16}
    compare_and_plot_csv_files(
        "./data/multicam_asil_01/mediapipe_multicam_asil_01_front_1440_810_LITE_video.csv",
        "./data/multicam_asil_01/mediapipe_multicam_asil_01_front_480_270_LITE_video.csv",
        72,
        72,
        mapping=mapping,
        label1="1440x810",
        label2="480x270",
        plot_file_prefix="./data/multicam_asil_01/mediapipe_multicam_asil_01_front_LITE_video",
    )

    compare_and_plot_csv_files(
        "./data/multicam_asil_01/mediapipe_multicam_asil_01_front_1440_810_FULL_video.csv",
        "./data/multicam_asil_01/mediapipe_multicam_asil_01_front_480_270_FULL_video.csv",
        72,
        72,
        mapping=mapping,
        label1="1440x810",
        label2="480x270",
        plot_file_prefix="./data/multicam_asil_01/mediapipe_multicam_asil_01_front_FULL_video",
    )


if __name__ == "__main__":
    # compare_resolutions_and_models_axil_01_front_right_wrist(mapping=qtm_to_mediapipe)
    # compare_resolutions()
    compare_and_plot_csv_files(
        "./data/multicam_asil_01/qtm_multicam_asil_01.csv",
        "./data/multicam_asil_01/mediapipe_multicam_asil_01_left_1440x810_LITE_video.csv",
        5,
        120,
        mapping={0: 15},
        plot_file_prefix="./data/multicam_asil_01/mediapipe_multicam_asil_01_left_1440x810_LITE_video",
    )
