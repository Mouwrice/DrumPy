from abc import ABC, abstractmethod
from enum import Enum
from multiprocessing import Pool
from pathlib import Path
from typing import Self, Optional

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

    def __init__(self: Self) -> None:
        self.stopped = False

    @abstractmethod
    def get_fps(self: Self) -> float:
        """
        Get the frames per second of the video
        :return: The frames per second
        """

    @abstractmethod
    def get_frame(self: Self) -> Optional[ndarray]:
        """
        Get the next frame from the video
        :return: The frame and the timestamp
        """

    @abstractmethod
    def release(self: Self) -> None:
        """
        Release the video source
        :return:
        """

    @abstractmethod
    def get_size(self: Self) -> tuple[int, int]:
        """
        Get the size of the video source
        :return: The width and height of the video source
        """

    @abstractmethod
    def get_timestamp_ms(self: Self) -> int:
        """
        Get the timestamp of the current frame
        :return: The timestamp of the current frame
        """


class VideoFileSource(VideoSource):
    """
    Class to handle a video source from a file
    """

    def __init__(self: Self, file_path: str) -> None:
        super().__init__()

        assert Path(file_path).exists(), f"File {file_path} does not exist"

        self.file_path = file_path
        self.cap = cv2.VideoCapture(file_path)
        self.source_fps = self.cap.get(cv2.CAP_PROP_FPS)
        source_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        source_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        smallest = min(source_width, source_height)
        self.size = (smallest, smallest)
        self.left_offset = (source_width - smallest) // 2
        self.top_offset = (source_height - smallest) // 2
        self.pool: Pool = None

    def get_fps(self: Self) -> float:
        """
        Get the frames per second of the video
        :return: The frames per second
        """
        return self.source_fps

    def get_frame(self: Self) -> Optional[ndarray]:
        """
        Get the next frame from the video
        :return: The frame and the timestamp
        """
        ret, frame = self.cap.read()
        if not ret or frame is None:
            self.stopped = True
            return None

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Crop the image to a square aspect ratio
        return frame[
            self.top_offset : self.top_offset + self.size[1],
            self.left_offset : self.left_offset + self.size[0],
        ].copy()

    def release(self: Self) -> None:
        """
        Release the video capture
        :return:
        """
        self.cap.release()

    def get_size(self: Self) -> tuple[int, int]:
        """
        Get the size of the video source
        :return: The width and height of the video source
        """
        return self.size

    def get_timestamp_ms(self: Self) -> int:
        """
        Get the timestamp of the current frame
        :return: The timestamp of the current frame
        """
        return int(self.cap.get(cv2.CAP_PROP_POS_MSEC))


class CameraSource(VideoSource):
    """
    Class to handle a video source from a camera
    """

    def __init__(self: Self, camera_id: int | str) -> None:
        super().__init__()
        self.camera_id = camera_id
        self.camera = camera.Camera(camera_id)
        self.camera.start()
        original_size = self.camera.get_size()
        # Crop the image to a square aspect ratio
        min_size = min(original_size)
        self.size = (min_size, min_size)
        self.left_offset = (original_size[0] - min_size) // 2
        self.top_offset = (original_size[1] - min_size) // 2

    def get_fps(self: Self) -> float:
        """
        Return a default value of 60 fps for the camera
        """
        return 60

    def get_frame(self: Self) -> Optional[ndarray]:
        """
        Get the next frame from the video
        :return: The frame and the timestamp
        """
        if self.camera.query_image():
            frame = pygame.Surface(self.size)
            image = self.camera.get_image()
            frame.blit(image, (0, 0), ((self.left_offset, self.top_offset), self.size))
            return surfarray.array3d(frame)

        return None

    def release(self: Self) -> None:
        """
        Release the video capture
        :return:
        """

    def get_size(self: Self) -> tuple[int, int]:
        return self.size

    def get_timestamp_ms(self: Self) -> int:
        """
        Get the timestamp of the current frame
        :return: The timestamp of the current frame
        """
        return pygame.time.get_ticks()
