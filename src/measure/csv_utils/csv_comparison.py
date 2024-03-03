from bokeh.io import output_file, save, show
from bokeh.plotting import figure
from matplotlib import pyplot as plt

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
    show_plot: bool = False,
):
    """
    Plot the positions of the markers over time for a certain axis.
    Normalizes the values between 0 and 1
    :return:
    """

    # Remove the average offset from the data
    avg_offset = 0
    for i in range(len(axis1)):
        avg_offset += axis2[i] - axis1[i]
    avg_offset /= len(axis1)

    for i in range(len(axis1)):
        axis2[i] -= avg_offset

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
    if show_plot:
        show(plot)
    else:
        save(plot)


def row_deviations_boxplot(
    baseline: list[CSVRow],
    comparison: list[CSVRow],
    baseline_marker: int,
    comparison_marker: int,
    baseline_label: str = "qtm",
    comparison_label: str = "mediapipe",
    plot_file_prefix: str = "",
    show_plot: bool = False,
):
    """
    Plot the absolute sum of deviations of each CSVRow for a certain marker
    as a matploblib boxplot
    """

    # First calculate the average offset of the comparison to the baseline
    avg_offset_x = 0
    avg_offset_y = 0
    avg_offset_z = 0
    for i in range(len(baseline)):
        avg_offset_x += comparison[i].x - baseline[i].x
        avg_offset_y += comparison[i].y - baseline[i].y
        avg_offset_z += comparison[i].z - baseline[i].z
    avg_offset_x /= len(baseline)
    avg_offset_y /= len(baseline)
    avg_offset_z /= len(baseline)

    deviations_seperate = [[], [], []]

    # The Euclidean distance of the deviations
    deviations = []
    for i in range(len(baseline)):
        deviations_seperate[0].append(
            abs(comparison[i].x - baseline[i].x - avg_offset_x)
        )
        deviations_seperate[1].append(
            abs(comparison[i].y - baseline[i].y - avg_offset_y)
        )
        deviations_seperate[2].append(
            abs(comparison[i].z - baseline[i].z - avg_offset_z)
        )
        deviations.append(
            (
                (comparison[i].x - baseline[i].x - avg_offset_x) ** 2
                + (comparison[i].y - baseline[i].y - avg_offset_y) ** 2
                + (comparison[i].z - baseline[i].z - avg_offset_z) ** 2
            )
            ** 0.5
        )

    title = f"{plot_file_prefix}_{baseline_label}_{baseline_marker}_{comparison_label}_{comparison_marker}_deviations_seperate"

    fig, ax = plt.subplots()
    ax.boxplot(deviations_seperate, patch_artist=True, vert=True)
    ax.set_title(title)
    ax.set_ylabel("Deviation (mm)")
    ax.set_xticklabels(["x", "y", "z"])

    # increase the dpi for better quality
    fig.set_dpi(300)

    # make the plot bigger
    fig.set_size_inches(10, 5)

    # Save the plot
    plt.savefig(f"{title}.png")
    if show_plot:
        plt.show()

    # Plot the Euclidean distance of the deviations
    title = f"{plot_file_prefix}_{baseline_label}_{baseline_marker}_{comparison_label}_{comparison_marker}_deviations"
    fig, ax = plt.subplots()
    ax.boxplot(deviations, patch_artist=True, vert=True)
    ax.set_title(title)
    ax.set_ylabel("Deviation (mm)")
    ax.set_xticklabels(["euclidean distance based"])

    # increase the dpi for better quality
    fig.set_dpi(300)

    # make the plot bigger
    fig.set_size_inches(10, 5)

    # Save the plot
    plt.savefig(f"{title}.png")
    if show_plot:
        plt.show()


def plot_marker_trajectories(
    positions1: list[CSVRow],
    positions2: list[CSVRow],
    marker1: int,
    marker2: int,
    label1: str = "qtm",
    label2: str = "mediapipe",
    plot_file_prefix: str = "",
    show_plot: bool = False,
):
    """
    Plot the positions of the markers over time
    """
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
        show_plot=show_plot,
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
        show_plot=show_plot,
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
        show_plot=show_plot,
    )


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
