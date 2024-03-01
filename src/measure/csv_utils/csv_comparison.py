from bokeh.io import output_file
from bokeh.plotting import figure

from measure.csv_utils.csv_row import CSVRow
from measure.frame import Frame


def plot_axis(
    axis1: list[float],
    axis2: list[float],
    axis: str,
    marker1: int,
    marker2: int,
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

    title = f"{plot_file_prefix}_{label1}_{marker1}_{label2}_{marker2}_{axis}_positions"

    plot = figure(
        title=title,
        x_axis_label="Frame",
        y_axis_label="Position",
        sizing_mode="stretch_both",
    )
    plot.line(list(range(len(axis1))), axis1, legend_label=label1, line_color="red")
    plot.line(list(range(len(axis2))), axis2, legend_label=label2, line_color="blue")

    output_file(f"{title}.html")


def plot_positions(
    positions1: list[list[CSVRow]],
    positions2: list[list[CSVRow]],
    marker1: int,
    marker2: int,
    label1: str = "qtm",
    label2: str = "mediapipe",
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
        x2.append(positions2[i].x)
        y2.append(positions2[i].y)
        z2.append(positions2[i].z)

    plot_axis(
        x1,
        x2,
        "x",
        marker1,
        marker2,
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
