from multiprocessing import Pool

from app.main import App
from app.video_source import Source
from tracker.mediapipe_pose import LandmarkerModel

"""
File to track the recordings
and output the results to a csv file
"""


def track_redcordings():
    recordings = [
        # "../recordings/multicam_asil_01_front.mkv",
        "../recordings/multicam_asil_01_left.mkv",
        # "../recordings/multicam_asil_01_right.mkv",
        # "../recordings/multicam_asil_02_front.mkv",
        # "../recordings/multicam_asil_02_left.mkv",
        # "../recordings/multicam_asil_02_right.mkv",
        # "../recordings/multicam_asil_03_front.mkv",
        # "../recordings/multicam_asil_03_left.mkv",
        # "../recordings/multicam_asil_03_right.mkv",
        # "../recordings/multicam_ms_01_front.mkv",
        # "../recordings/multicam_ms_01_left.mkv",
        # "../recordings/multicam_ms_01_right.mkv",
        # "../recordings/multicam_ms_02_front.mkv",
        # "../recordings/multicam_ms_02_left.mkv",
        # "../recordings/multicam_ms_02_right.mkv",
    ]

    models = [LandmarkerModel.LITE, LandmarkerModel.FULL, LandmarkerModel.HEAVY]

    for recording in recordings:
        for model in models:
            file_name = recording.split("/")[-1].replace(".mkv", "")
            # omit everything after th second underscore
            directory = "_".join(file_name.split("_")[:3])
            print(f"Recording: {recording}, Model: {model}, Async")

            with Pool(processes=6) as pool:
                app = App(
                    pool,
                    source=Source.FILE,
                    file_path=recording,
                    live_stream=True,
                    model=model,
                    log_file=f"./data/{directory}/mediapipe_{file_name}_{model.name}_async_video.csv",
                )
                app.start()


if __name__ == "__main__":
    track_redcordings()
