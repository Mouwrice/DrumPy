import os

from measure.csv_utils.csv_comparison import get_closest_frame_index, plot_positions
from measure.frame import Frame


def plot_all():
    """
    Plots every mediapipe csv file in the data directory against the corresponding qtm csv file in the same directory
    """
    # For every directory in the data directory
    for directory in os.listdir("data"):
        # If the directory is not a directory
        if not os.path.isdir(f"data/{directory}"):
            continue

        # If the corresponding qtm file does not exist
        if not os.path.exists(f"data/{directory}/qtm_{directory}.csv"):
            continue

        qtm = f"data/{directory}/qtm_{directory}.csv"
        # Parse the qtm csv file.
        qtm_data: list[Frame] = Frame.frames_from_csv(qtm)

        # For every file in the directory
        for file in os.listdir(f"data/{directory}"):
            # If the file is not a csv file
            if not file.endswith(".csv"):
                continue
            # If the file is a mediapipe csv file
            if file.startswith("mediapipe"):
                # Parse the mediapipe csv file
                mediapipe_data: list[Frame] = Frame.frames_from_csv(
                    f"data/{directory}/{file}"
                )

                mediapipe_offset = offsets.get(file, 0)
                qtm_offset = offsets.get(qtm, 0)

                # Compare the mediapipe and qtm data
                compare_qtm_mediapipe(
                    mediapipe_data,
                    qtm_data,
                    mediapipe_offset,
                    qtm_offset,
                    plot_file_prefix=f"data/{directory}/{file[:-4]}",
                    mapping={0: 15},
                )


offsets = {
    "mediapipe_multicam_asil_01_front_LITE_async_video.csv": 0,
    "qtm_multicam_asil_01.csv": 0,
}

qtm_to_mediapipe = {
    0: 15,  # left wrist
    1: 16,  # right wrist
    2: 19,  # left index
    3: 20,  # right index
    4: 31,  # left foot index
    5: 32,  # right foot index
}


def compare_qtm_mediapipe(
    mediapipe_data: list[Frame],
    qtm_data: list[Frame],
    mediapipe_offset,
    qtm_offset,
    plot_file_prefix="plot",
    mapping=None,
):
    """
    Compare the mediapipe and qtm data
    """

    assert len(mediapipe_data) > 0, "No frames found in QTM file"
    assert len(qtm_data) > 0, "No frames found in Mediapipe file"

    mediapipe_offset = min(mediapipe_offset, mediapipe_data[0].frame)
    qtm_offset = min(qtm_offset, qtm_data[0].frame)

    mp_idx = get_closest_frame_index(mediapipe_data, mediapipe_offset)
    qtm_idx = get_closest_frame_index(qtm_data, qtm_offset)
    mp_time_offset = mediapipe_data[mp_idx].time_ms
    qtm_time_offset = qtm_data[qtm_idx].time_ms

    mp_frame = mediapipe_data[mp_idx]
    qtm_frame = qtm_data[qtm_idx]
    mp_pos = []
    qtm_pos = []
    while mp_idx < len(mediapipe_data) - 1 and qtm_idx < len(qtm_data) - 1:
        mp_next = mediapipe_data[mp_idx + 1]
        qtm_next = qtm_data[qtm_idx + 1]
        mp_time = mp_frame.time_ms - mp_time_offset
        qtm_time = qtm_frame.time_ms - qtm_time_offset
        if mp_time < qtm_time:
            mp_idx += 1
            mp_frame = mp_next
        elif mp_time > qtm_time:
            qtm_idx += 1
            qtm_frame = qtm_next
        else:
            mp_idx += 1
            qtm_idx += 1
            mp_frame = mp_next
            qtm_frame = qtm_next

        mp_pos.append(mp_frame.rows)
        qtm_pos.append(qtm_frame.rows)

    mp_to_qtm_basis(mp_pos)

    for key, value in mapping.items():
        plot_positions(
            qtm_pos,
            mp_pos,
            key,
            value,
            "qtm",
            "mediapipe",
            plot_file_prefix=plot_file_prefix,
            show_plot=True,
        )


def mp_to_qtm_basis(mp_pos):
    """
    MP uses a different basis, convert to QTM basis
    """
    for frame in mp_pos:
        for row in frame:
            row.x, row.y, row.z = row.z, -row.x, row.y


if __name__ == "__main__":
    plot_all()
