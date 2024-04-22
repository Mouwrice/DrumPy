from typing import Optional, Self

import pygame
import pygame.camera
from mediapipe.tasks.python import BaseOptions  # type: ignore
from mediapipe.tasks.python.vision import RunningMode  # type: ignore
from pygame_gui import UIManager  # type: ignore

from drumpy.app.camera_display import VideoDisplay
from drumpy.app.fps_display import FPSDisplay
from drumpy.app.video_source import CameraSource, VideoFileSource, Source
from drumpy.mediapipe_pose.landmark_type import LandmarkType
from drumpy.mediapipe_pose.landmarker_model import LandmarkerModel
from drumpy.mediapipe_pose.mediapipe_pose import MediaPipePose
from drumpy.tracking.drum_trackers import DrumTrackers


class App:
    """
    Main application class
    """

    def __init__(
        self,
        source: Source = Source.CAMERA,
        file_path: Optional[str] = None,
        running_mode: RunningMode = RunningMode.LIVE_STREAM,  # type: ignore
        model: LandmarkerModel = LandmarkerModel.FULL,
        delegate: BaseOptions.Delegate = BaseOptions.Delegate.CPU,  # type: ignore
        log_file: Optional[str] = None,
        landmark_type: LandmarkType = LandmarkType.WORLD_LANDMARKS,
        camera_index: int = 0,
        disable_drum: bool = False,  # noqa: FBT001, FBT002
    ) -> None:
        """
        Initialize the application
        :param model: The model to use for the pose estimation
        :param log_file: The file to log the landmarks to, if None no logging will be done
        :delegate: The delegate to use for the pose estimation, Either CPU or GPU
        """
        self.model = model

        pygame.init()

        pygame.display.set_caption("DrumPy")
        initial_window_size = (900, 900)
        self.window_surface = pygame.display.set_mode(initial_window_size)
        self.manager = UIManager(initial_window_size)

        self.drum_trackers: Optional[DrumTrackers] = None
        if not disable_drum:
            self.drum_trackers = DrumTrackers()

        self.media_pipe_pose = MediaPipePose(
            running_mode=running_mode,  # type: ignore
            model=model,
            log_file=log_file,
            delegate=delegate,  # type: ignore
            landmark_type=landmark_type,
            drum_trackers=self.drum_trackers,
        )

        FPSDisplay(
            ui_manager=self.manager,
            media_pipe_pose=self.media_pipe_pose,
        )

        match source:
            case Source.CAMERA:
                self.video_source = CameraSource(camera_index=camera_index)
            case Source.FILE:
                assert file_path is not None, "File path must be provided"
                self.video_source = VideoFileSource(file_path)

        self.fps = self.video_source.get_fps()
        self.video_display = VideoDisplay(
            video_source=self.video_source,
            media_pipe_pose=self.media_pipe_pose,
            rect=pygame.Rect((0, 50), (900, 900)),
            window=self.window_surface,
            source=source,
        )

    def start(self: Self) -> None:
        clock = pygame.time.Clock()
        running = True
        while running and not self.video_source.stopped:
            time_delta_ms = clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                self.manager.process_events(event)

            self.window_surface.fill(pygame.Color("#000000"))
            self.video_display.update()
            self.manager.update(time_delta_ms / 1000.0)
            self.manager.draw_ui(self.window_surface)

            pygame.display.update()

        self.video_source.release()
        pygame.quit()


def main() -> None:
    app = App(
        source=Source.CAMERA,
        running_mode=RunningMode.LIVE_STREAM,  # type: ignore
        model=LandmarkerModel.FULL,
        delegate=BaseOptions.Delegate.CPU,  # type: ignore
        landmark_type=LandmarkType.WORLD_LANDMARKS,
        file_path="../data/Recordings/multicam_asil_01_front.mkv",
        # log_file="test.csv",
        disable_drum=False,
    )
    app.start()


if __name__ == "__main__":
    main()
