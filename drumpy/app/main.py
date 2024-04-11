import pygame
import pygame.camera
from mediapipe.tasks.python import BaseOptions
from pygame_gui import UIManager

from drumpy.app.camera_display import VideoDisplay
from drumpy.app.fps_display import FPSDisplay
from drumpy.app.video_source import CameraSource, VideoFileSource, Source
from drumpy.mediapipe_pose import MediaPipePose, LandmarkerModel
from typing import Optional


class App:
    """
    Main application class
    """

    def __init__(
        self,
        source: Source = Source.CAMERA,
        camera_id: str | int = "/dev/video0",
        file_path: Optional[str] = None,
        live_stream: bool = True,
        model: LandmarkerModel = LandmarkerModel.FULL,
        delegate: BaseOptions.Delegate = BaseOptions.Delegate.GPU,
        plot: bool = False,
        log_file: None | str = None,
        world_landmarks: bool = False,
    ) -> None:
        """
        Initialize the application
        :param live_stream: Whether the pose estimation is in live stream mode, causing the result to be
        returned asynchronously and frames can be dropped
        :param model: The model to use for the pose estimation
        :param log_file: The file to log the landmarks to, if None no logging will be done
        :delegate: The delegate to use for the pose estimation, Either CPU or GPU
        :param plot: Whether to plot the results or not
        :param world_landmarks: Whether to use world landmarks or not
        """

        self.model = model

        self.plot = plot

        pygame.init()
        pygame.camera.init()

        print(pygame.camera.get_backends())
        cameras = pygame.camera.list_cameras()
        print(cameras)

        pygame.display.set_caption("DrumPy")
        initial_window_size = (1300, 900) if self.plot else (900, 900)
        self.window_surface = pygame.display.set_mode(initial_window_size)
        self.manager = UIManager(initial_window_size)

        self.media_pipe_pose = MediaPipePose(
            live_stream=live_stream,
            model=model,
            log_file=log_file,
            delegate=delegate,
            world_landmarks=world_landmarks,
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

        rect = pygame.Rect((400, 50), (900, 900)) if self.plot else pygame.Rect((0, 50), (900, 900))

        self.video_display = VideoDisplay(
            video_source=self.video_source,
            media_pipe_pose=self.media_pipe_pose,
            rect=rect,
            window=self.window_surface,
            source=source,
        )

    def start(self) -> None:
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
        live_stream=False,
        plot=False,
        delegate=BaseOptions.Delegate.GPU,
        world_landmarks=True,
    )
    app.start()


if __name__ == "__main__":
    main()
