import numpy as np
import numpy.typing as npt
import pygame.time
from pygame import Surface

from drumpy.app.video_source import VideoSource, Source
from drumpy.mediapipe_pose.mediapipe_pose import MediaPipePose


class VideoDisplay:
    """
    Pygame GUI element to display a video source and the pose landmarks
    Automatically resizes the camera feed to fit the window size
    """

    def __init__(
        self,
        video_source: VideoSource,
        media_pipe_pose: MediaPipePose,
        window: Surface,
        source: Source,
        rect: pygame.Rect,  # dimensions Rect((left, top), (width, height))
    ) -> None:
        self.source = source
        self.rect = rect
        self.window = window
        self.media_pipe_pose = media_pipe_pose
        self.video_source = video_source
        self.prev_surface = None

    def update(self) -> None:
        result: npt.NDArray[np.float32] | None = self.video_source.get_frame()
        assert (
            result is None or result.shape[0] == result.shape[1]
        ), "Frame is not square"

        # There is no new frame to display
        if result is None and self.prev_surface is not None:
            self.window.blit(self.prev_surface, self.rect.topleft)
            return

        # There is no new frame to display and no previous frame to display
        if result is None and self.prev_surface is None:
            return

        if result is not None:
            frame: npt.NDArray[np.float32] = result
            timestamp_ms = self.video_source.get_timestamp_ms()

            self.media_pipe_pose.process_image(frame, timestamp_ms)

            # Draw the landmarks on the image
            if self.media_pipe_pose.visualisation is not None:
                frame = self.media_pipe_pose.visualisation

            if self.source == Source.CAMERA:
                frame = frame.swapaxes(0, 1)

            image_surface = pygame.image.frombuffer(
                frame.tobytes(), (frame.shape[0], frame.shape[0]), "RGB"
            )

            # # Rotate the image 90 degrees
            # if self.source == Source.CAMERA:
            #     image_surface = pygame.transform.rotate(image_surface, -90)

            # Scale the image to fit the window
            image_surface = pygame.transform.scale(image_surface, self.rect.size)

            self.prev_surface = image_surface
            self.window.blit(image_surface, self.rect.topleft)
