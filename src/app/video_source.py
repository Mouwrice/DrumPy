from abc import ABC
from enum import Enum
from multiprocessing import Pool

import cv2
import pygame.transform
from numpy import ndarray
from pygame import camera, surfarray


class Source(Enum):
    """
    Enumeration for the different sources of video
    """

    CAMERA = 0
    FILE = 1


class VideoSource(ABC):
    """
    Abstract base class for a video source
    """

    def __init__(self, pool: Pool):
        self.pool = pool
        self.stopped = False

    def get_fps(self) -> float:
        """
        Get the frames per second of the video
        :return: The frames per second
        """
        pass

    def get_frame(self) -> ndarray | None:
        """
        Get the next frame from the video
        :return: The frame and the timestamp
        """
        pass

    def release(self):
        """
        Release the video source
        :return:
        """
        pass

    def get_size(self) -> tuple[int, int]:
        """
        Get the size of the video source
        :return: The width and height of the video source
        """
        pass

    def get_timestamp_ms(self) -> int:
        """
        Get the timestamp of the current frame
        :return: The timestamp of the current frame
        """
        pass


class VideoFileSource(VideoSource):
    """
    Class to handle a video source from a file
    """

    def __init__(self, file_path: str, pool: Pool):
        super().__init__(pool)
        self.file_path = file_path
        self.cap = cv2.VideoCapture(file_path)
        self.source_fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.source_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.source_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.pool: Pool = None

    def get_fps(self) -> float:
        """
        Get the frames per second of the video
        :return: The frames per second
        """
        return self.source_fps

    def get_frame(self) -> ndarray | None:
        """
        Get the next frame from the video
        :return: The frame and the timestamp
        """
        ret, frame = self.cap.read()
        if not ret or frame is None:
            self.stopped = True
            return None

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    def release(self):
        """
        Release the video capture
        :return:
        """
        self.cap.release()

    def get_size(self) -> tuple[int, int]:
        """
        Get the size of the video source
        :return: The width and height of the video source
        """
        return self.source_width, self.source_height

    def get_timestamp_ms(self) -> int:
        """
        Get the timestamp of the current frame
        :return: The timestamp of the current frame
        """
        return int(self.cap.get(cv2.CAP_PROP_POS_MSEC))


class CameraSource(VideoSource):
    """
    Class to handle a video source from a camera
    """

    def __init__(self, camera_id: int | str, pool: Pool):
        super().__init__(pool)
        self.camera_id = camera_id
        self.camera = camera.Camera(camera_id)
        self.size = self.camera.get_size()
        self.camera.start()

    def get_fps(self) -> float:
        """
        Return a default value of 60 fps for the camera
        """
        return 60

    def get_frame(self) -> ndarray | None:
        """
        Get the next frame from the video
        :return: The frame and the timestamp
        """
        if self.camera.query_image():
            image = self.camera.get_image()
            image = pygame.transform.flip(image, True, False)
            frame = surfarray.array3d(image)

            return frame

        return None

    def release(self):
        """
        Release the video capture
        :return:
        """
        pass

    def get_size(self) -> tuple[int, int]:
        return self.size

    def get_timestamp_ms(self) -> int:
        """
        Get the timestamp of the current frame
        :return: The timestamp of the current frame
        """
        return pygame.time.get_ticks()

    def is_opened(self):
        return True
