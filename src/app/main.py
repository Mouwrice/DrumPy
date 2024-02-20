from multiprocessing import Pool

import pygame
import pygame.camera

from pygame import Rect
from pygame_gui import UIManager

from app.fps_display import FPSDisplay
from app.camera_display import CameraDisplay
from app.graphs.latency_graph import LatencyGraph

from app.graphs.marker_location_graphs import MarkerLocationGraphs
from tracker.mediapipe_pose import MediaPipePose


def main():
    pygame.init()
    pygame.camera.init()

    print(pygame.camera.get_backends())
    print(pygame.camera.list_cameras())

    pygame.display.set_caption("DrumPy")
    initial_window_size = (1400, 800)
    window_surface = pygame.display.set_mode(initial_window_size)
    manager = UIManager(initial_window_size)

    media_pipe_pose = MediaPipePose()

    FPSDisplay(
        ui_manager=manager,
        media_pipe_pose=media_pipe_pose,
    )

    CameraDisplay(
        image_surface=pygame.Surface((600, 550)),
        camera_id="/dev/video0",
        ui_manager=manager,
        media_pipe_pose=media_pipe_pose,
    )

    # Apply multiprocessing using Pool
    # Can be used to execute long-running tasks in parallel without blocking the main thread
    with Pool(processes=4) as pool:
        LatencyGraph(
            relative_rect=Rect(1000, 50, 400, 300),
            image_surface=pygame.Surface((400, 300)),
            pool=pool,
            media_pipe_pose=media_pipe_pose,
        )

        MarkerLocationGraphs(pool, media_pipe_pose)

        frame = 0
        clock = pygame.time.Clock()
        while True:
            frame += 1
            time_delta_ms = clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                manager.process_events(event)

            window_surface.fill(pygame.Color("#000000"))
            manager.update(time_delta_ms / 1000.0)
            manager.draw_ui(window_surface)

            pygame.display.update()


if __name__ == "__main__":
    main()
