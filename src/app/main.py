import pygame
import pygame.camera
from pygame import Rect
from pygame_gui import UIManager
from pygame_gui.core import UIContainer

from app.fps_display import FPSDisplay
from app.camera_display import CameraDisplay
from app.fps_graph import FPSGraph
from tracker.mediapipe_pose import MediaPipePose


def main():
    pygame.init()
    pygame.camera.init()

    print(pygame.camera.get_backends())
    print(pygame.camera.list_cameras())

    pygame.display.set_caption("DrumPy")
    initial_window_size = (800, 600)
    window_surface = pygame.display.set_mode(initial_window_size, pygame.RESIZABLE)
    ui_manager = UIManager(initial_window_size)

    media_pipe_pose = MediaPipePose()

    # Split the window into three panels
    left_panel = UIContainer(
        Rect(0, 0, 200, -1),
        manager=ui_manager,
        anchors={"top": "top", "left": "left", "bottom": "bottom"},
    )

    right_panel = UIContainer(
        Rect(0, 0, 200, -1),
        manager=ui_manager,
        anchors={"top": "top", "right": "right", "bottom": "bottom"},
    )

    middle_panel = UIContainer(
        Rect(0, 0, 600, 600),
        manager=ui_manager,
        anchors={
            "top": "top",
            "left_target": left_panel,
            "right_target": right_panel,
            "bottom": "bottom",
        },
    )

    FPSDisplay(
        ui_manager=ui_manager,
        container=middle_panel,
        media_pipe_pose=media_pipe_pose,
    )

    CameraDisplay(
        image_surface=pygame.Surface((640, 480)),
        camera_id="/dev/video0",
        ui_manager=ui_manager,
        media_pipe_pose=media_pipe_pose,
    )

    fps_graph = FPSGraph(screen=window_surface)

    frame = 0
    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        frame += 1
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    is_running = False
                case pygame.VIDEORESIZE:
                    ui_manager.set_window_resolution(window_surface.get_size())

            ui_manager.process_events(event)

        ui_manager.update(time_delta)
        window_surface.fill(pygame.Color("#000000"))
        # fps_graph.update(frame, time_delta)
        fps_graph.figure.line("Chart1", [1, 2, 3, 4, 6, 20, 24], [3, 5, 7, 2, 7, 9, 1])
        fps_graph.figure.draw()
        ui_manager.draw_ui(window_surface)

        pygame.display.update()


if __name__ == "__main__":
    main()
