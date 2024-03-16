import pygame
import pygame.camera
from mediapipe.tasks.python import BaseOptions
from pygame_gui import UIManager

from drumpy.app.camera_display import VideoDisplay
from drumpy.app.fps_display import FPSDisplay
from drumpy.app.video_source import CameraSource, VideoFileSource, Source
from drumpy.mediapipe_pose import MediaPipePose, LandmarkerModel


class App:
    """
    Main application class
    """

    def __init__(
        self,
        source: Source = Source.CAMERA,
        camera_id: str | int = "/dev/video0",
        file_path: str = None,
        live_stream: bool = True,
        model: LandmarkerModel = LandmarkerModel.FULL,
        delegate: BaseOptions.Delegate = BaseOptions.Delegate.GPU,
        plot: bool = False,
        log_file: None | str = None,
    ):
        """
        Initialize the application
        :param live_stream: Whether the pose estimation is in live stream mode, causing the result to be
        returned asynchronously and frames can be dropped
        :param model: The model to use for the pose estimation
        :param log_file: The file to log the landmarks to, if None no logging will be done
        :delegate: The delegate to use for the pose estimation, Either CPU or GPU
        """

        self.model = model

        self.plot = plot

        pygame.init()
        pygame.camera.init()

        print(pygame.camera.get_backends())
        print(pygame.camera.list_cameras())

        pygame.display.set_caption("DrumPy")
        initial_window_size = (1800, 1000)
        self.window_surface = pygame.display.set_mode(initial_window_size)
        self.manager = UIManager(initial_window_size)

        self.media_pipe_pose = MediaPipePose(
            live_stream=live_stream, model=model, log_file=log_file, delegate=delegate
        )

        FPSDisplay(
            ui_manager=self.manager,
            media_pipe_pose=self.media_pipe_pose,
        )

        self.video_source = None
        match source:
            case Source.CAMERA:
                self.video_source = CameraSource(camera_id)
            case Source.FILE:
                self.video_source = VideoFileSource(file_path)

        self.fps = self.video_source.get_fps()

        self.video_display = VideoDisplay(
            video_source=self.video_source,
            media_pipe_pose=self.media_pipe_pose,
            dimensions=(1000, 800) if self.plot else (1800, 950),
            offset=(400, 50) if self.plot else (0, 50),
            window=self.window_surface,
            source=source,
        )

    def start(self):
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


def main():
    app = App(
        source=Source.CAMERA,
        file_path="../recordings/multicam_asil_01_front.mkv",
        live_stream=True,
        plot=False,
        delegate=BaseOptions.Delegate.GPU,
    )
    app.start()


if __name__ == "__main__":
    main()
