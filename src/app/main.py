import pygame
import pygame.camera
import pygame_gui

from tracker.mediapipe_pose import MediaPipePose, visualize_landmarks

"""
Uses Pygame Camera module to display a webcam in a window 
"""


class CameraDisplay(pygame_gui.elements.UIImage):
    def __init__(
        self,
        image_surface: pygame.Surface,
        camera_id: str | int,
        ui_manager: pygame_gui.UIManager,
        media_pipe_pose: MediaPipePose,
    ):
        # Construct the relative rectangle
        relative_rect = pygame.Rect((0, 0), (0, 0))

        super().__init__(relative_rect, image_surface, ui_manager)

        self.ui_manager = ui_manager
        self.camera = pygame.camera.Camera(camera_id)
        self.media_pipe_pose = media_pipe_pose
        self.camera.start()

        print(self.camera.get_controls())

        self._size = self.camera.get_size()
        self.__fit_and_center_rect()
        self.set_image(self.camera.get_image())

    def __fit_and_center_rect(self):
        """
        Fits the camera image to the window size without stretching.
        Centers the camera image in the window.
        :return:
        """
        window_width, window_height = self.ui_manager.window_resolution
        image_width, image_height = self.camera.get_size()

        if window_width / window_height > image_width / image_height:
            self.set_dimensions(
                (window_height * image_width / image_height, window_height)
            )
        else:
            self.set_dimensions(
                (window_width, window_width * image_height / image_width)
            )

        self.rect.center = (window_width // 2, window_height // 2)

    def update(self, time_delta: float):
        super().update(time_delta)
        self.__fit_and_center_rect()

        if self.camera is not None:
            image = self.camera.get_image()

            # Convert the image to a numpy array
            image_array = pygame.surfarray.array3d(image)
            self.media_pipe_pose.process_image(image_array)

            # Draw the landmarks on the image
            image = visualize_landmarks(
                image_array, self.media_pipe_pose.process_image(image_array)
            )
            self.set_image(pygame.surfarray.make_surface(image))


def main():
    pygame.init()
    pygame.camera.init()

    print(pygame.camera.get_backends())
    print(pygame.camera.list_cameras())

    pygame.display.set_caption("DrumPy")
    initial_window_size = (800, 600)
    window_surface = pygame.display.set_mode(initial_window_size, pygame.RESIZABLE)
    ui_manager = pygame_gui.UIManager(initial_window_size)

    media_pipe_pose = MediaPipePose()

    num_connected_cameras = 1
    cam_names = pygame.camera.list_cameras()
    for cam_name in cam_names[:num_connected_cameras]:
        CameraDisplay(
            camera_id=cam_name,
            image_surface=window_surface,
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
                    window_surface.fill(pygame.Color("#000000"))

            ui_manager.process_events(event)

        ui_manager.update(time_delta)
        ui_manager.draw_ui(window_surface)
        pygame.display.update()


if __name__ == "__main__":
    main()
