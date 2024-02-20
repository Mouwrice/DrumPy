import pygame.time
from pygame import Surface, surfarray, camera, Rect
from pygame_gui import UIManager
from pygame_gui.elements import UIImage

from tracker.mediapipe_pose import MediaPipePose


class CameraDisplay(UIImage):
    """
    Pygame GUI element to display the camera feed and the pose landmarks
    Automatically resizes the camera feed to fit the window size
    """

    def __init__(
        self,
        image_surface: Surface,
        camera_id: str | int,
        ui_manager: UIManager,
        media_pipe_pose: MediaPipePose,
    ):
        super().__init__(
            relative_rect=Rect(400, 50, 600, 550),
            image_surface=image_surface,
            manager=ui_manager,
        )

        self.ui_manager = ui_manager
        self.camera = camera.Camera(camera_id)
        self.media_pipe_pose = media_pipe_pose
        self.camera.start()

        print(self.camera.get_controls())

        self._size = self.camera.get_size()

    def __fit_and_center_rect(self):
        """
        Fits the camera image to the window size without stretching.
        Centers the camera image in the window.
        :return:
        """
        # Get the dimensions of the container
        image_width, image_height = self._size

        if self.rect.width / self.rect.height > image_width / image_height:
            self.set_dimensions(
                (self.rect.height * image_width / image_height, self.rect.height)
            )
        else:
            self.set_dimensions(
                (self.rect.width, self.rect.width * image_height / image_width)
            )

    def update(self, time_delta: float):
        super().update(time_delta)
        self.__fit_and_center_rect()

        if self.camera is not None and self.camera.query_image():
            image = self.camera.get_image()

            # Convert the image to a numpy array
            image_array = surfarray.array3d(image)
            timestamp_ms = pygame.time.get_ticks()
            self.media_pipe_pose.process_image(image_array, timestamp_ms)

            image = self.media_pipe_pose.image_landmarks
            if image is not None:
                self.set_image(surfarray.make_surface(image))
