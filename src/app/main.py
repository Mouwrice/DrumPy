import pygame
import pygame.camera
from pygame_gui import UIManager

from app.camera_container import FPSDisplay
from app.camera_display import CameraDisplay
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

    FPSDisplay(
        ui_manager=ui_manager,
        media_pipe_pose=media_pipe_pose,
    )

    CameraDisplay(
        image_surface=pygame.Surface((640, 480)),
        camera_id="/dev/video0",
        ui_manager=ui_manager,
        media_pipe_pose=media_pipe_pose,
    )

    clock = pygame.time.Clock()
    is_running = True

    while is_running:
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
        ui_manager.draw_ui(window_surface)

        pygame.display.update()


if __name__ == "__main__":
    main()
