import pygame.time
from pygame import Surface

from drumpy.app.video_source import VideoSource, Source
from drumpy.mediapipe_pose import MediaPipePose


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
        dimensions: tuple[int, int],  # (width, height)
        offset: tuple[int, int] = (0, 0),  # (x, y)
    ):
        self.source = source
        self.dimensions = dimensions
        self.offset = offset
        self.window = window
        self.media_pipe_pose = media_pipe_pose
        self.video_source = video_source
        self._size = self.video_source.get_size()
        self.prev_surface = None

    def update(self):
        frame = self.video_source.get_frame()

        # There is no new frame to display
        if frame is None and self.prev_surface is not None:
            self.window.blit(self.prev_surface, self.offset)
            return

        # There is no new frame to display and no previous frame to display
        if frame is None and self.prev_surface is None:
            return

        timestamp_ms = self.video_source.get_timestamp_ms()

        self.media_pipe_pose.process_image(frame, timestamp_ms)

        # Draw the landmarks on the image
        if self.media_pipe_pose.visualisation is not None:
            frame = self.media_pipe_pose.visualisation

        if self.source == Source.CAMERA:
            size = frame.shape[0], frame.shape[1]
            frame = frame.swapaxes(0, 1)
        else:
            size = frame.shape[1], frame.shape[0]

        image_surface = pygame.image.frombuffer(frame.flatten(), size, "RGB")

        # # Rotate the image 90 degrees
        # if self.source == Source.CAMERA:
        #     image_surface = pygame.transform.rotate(image_surface, -90)

        # Resize the image to fit the window but maintain the aspect ratio
        if size[0] > size[1]:
            new_width = self.dimensions[0]
            new_height = int(size[1] * (new_width / size[0]))
        else:
            new_height = self.dimensions[1]
            new_width = int(size[0] * (new_height / size[1]))

        image_surface = pygame.transform.scale(image_surface, (new_width, new_height))

        self.prev_surface = image_surface
        self.window.blit(image_surface, self.offset)
