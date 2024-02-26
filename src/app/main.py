from multiprocessing import Pool

import pygame
import pygame.camera
from pygame_gui import UIManager

from app.camera_display import VideoDisplay
from app.fps_display import FPSDisplay
from app.graphs.latency_graph import LatencyGraph
from app.graphs.marker_location_graphs import MarkerLocationGraphs
from app.video_source import CameraSource, VideoFileSource, Source
from tracker.mediapipe_pose import MediaPipePose


class App:
    """
    Main application class
    """

    def __init__(
        self,
        pool: Pool,
        source: Source = Source.CAMERA,
        camera_id: str | int = "/dev/video0",
        file_path: str = None,
        live_stream: bool = True,
    ):
        self.pool = pool  # Pool of processes for multiprocessing, required to not block the main thread

        pygame.init()
        pygame.camera.init()

        print(pygame.camera.get_backends())
        print(pygame.camera.list_cameras())

        pygame.display.set_caption("DrumPy")
        initial_window_size = (1800, 1000)
        self.window_surface = pygame.display.set_mode(initial_window_size)
        self.manager = UIManager(initial_window_size)
        self.media_pipe_pose = MediaPipePose(live_stream=live_stream)

        FPSDisplay(
            ui_manager=self.manager,
            media_pipe_pose=self.media_pipe_pose,
        )

        self.video_source = None
        match source:
            case Source.CAMERA:
                self.video_source = CameraSource(camera_id, pool)
            case Source.FILE:
                self.video_source = VideoFileSource(file_path, pool)

        self.fps = self.video_source.get_fps()

        self.video_display = VideoDisplay(
            video_source=self.video_source,
            media_pipe_pose=self.media_pipe_pose,
            dimensions=(1000, 800),
            window=self.window_surface,
            source=source,
        )

    def start(self):
        # Apply multiprocessing using Pool
        # Can be used to execute long-running tasks in parallel without blocking the main thread

        LatencyGraph(
            pool=self.pool,
            media_pipe_pose=self.media_pipe_pose,
        )

        MarkerLocationGraphs(self.pool, self.media_pipe_pose)

        frame = 0
        clock = pygame.time.Clock()
        running = True
        while running:
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
    with Pool(processes=6) as pool:
        app = App(
            pool,
            source=Source.FILE,
            file_path="../recordings/multicam_asil_01_left.mkv",
            live_stream=True,
        )
        app.start()


if __name__ == "__main__":
    main()
