from pygame import Surface, Rect, surfarray, camera
from pygame_gui import UIManager
from pygame_gui.elements import UIImage

from tracker.mediapipe_pose import MediaPipePose, visualize_landmarks


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
        # Construct the relative rectangle
        relative_rect = Rect((0, 0), (0, 0))

        super().__init__(relative_rect, image_surface, ui_manager)

        self.ui_manager = ui_manager
        self.camera = camera.Camera(camera_id)
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
            image_array = surfarray.array3d(image)
            self.media_pipe_pose.process_image(image_array)

            # Draw the landmarks on the image
            image = visualize_landmarks(
                image_array, self.media_pipe_pose.process_image(image_array)
            )
            self.set_image(surfarray.make_surface(image))
