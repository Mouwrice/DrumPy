from typing import Optional, Self

import pygame
import pygame.camera
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import RunningMode
from pygame_gui import UIManager

from drumpy.app.camera_display import VideoDisplay
from drumpy.app.fps_display import FPSDisplay
from drumpy.app.video_source import CameraSource, VideoFileSource, Source
from drumpy.tracking.mediapipe_pose import MediaPipePose
from drumpy.tracking.landmarker_model import LandmarkerModel
from drumpy.tracking.landmark_type import LandmarkType


class App:
    """
    Main application class
    """

    def __init__(
        self: Self,
        source: Source = Source.CAMERA,
        file_path: Optional[str] = None,
        running_mode: RunningMode = RunningMode.LIVE_STREAM,
        model: LandmarkerModel = LandmarkerModel.FULL,
        delegate: BaseOptions.Delegate = BaseOptions.Delegate.GPU,
        log_file: Optional[str] = None,
        landmark_type: LandmarkType = LandmarkType.WORLD_LANDMARKS,
    ) -> None:
        """
        Initialize the application
        :param model: The model to use for the pose estimation
        :param log_file: The file to log the landmarks to, if None no logging will be done
        :delegate: The delegate to use for the pose estimation, Either CPU or GPU
        """
        self.model = model

        pygame.init()
        pygame.camera.init()

        print(pygame.camera.get_backends())
        cameras = pygame.camera.list_cameras()
        print(cameras)

        pygame.display.set_caption("DrumPy")
        initial_window_size = (900, 900)
        self.window_surface = pygame.display.set_mode(initial_window_size)
        self.manager = UIManager(initial_window_size)

        self.media_pipe_pose = MediaPipePose(
            running_mode=running_mode,
            model=model,
            log_file=log_file,
            delegate=delegate,
            landmark_type=landmark_type,
        )

        FPSDisplay(
            ui_manager=self.manager,
            media_pipe_pose=self.media_pipe_pose,
        )

        self.video_source = None
        match source:
            case Source.CAMERA:
                self.video_source = CameraSource(cameras[0])
            case Source.FILE:
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
        frame = 0
        clock = pygame.time.Clock()
        running = True
        while running and not self.video_source.stopped:
            frame += 1
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
        source=Source.FILE,
        file_path="../../recordings/multicam_asil_01_front.mkv",
    )
    app.start()


if __name__ == "__main__":
    main()
