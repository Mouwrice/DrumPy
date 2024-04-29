from abc import ABC, abstractmethod
from enum import IntEnum
from pathlib import Path
from typing import Self

import cv2
import numpy as np
import pygame.transform
import numpy.typing as npt
from pygame import camera, surfarray, Surface


class Source(IntEnum):
    """
    Enumeration for the different sources of video
    """

    CAMERA = 0
    FILE = 1

    @staticmethod
    def from_str(source: str) -> "Source":
        match source.lower():
            case "camera":
                return Source.CAMERA
            case "file":
                return Source.FILE
            case _:
                raise ValueError(f"Invalid source: {source}")


class VideoSource(ABC):
    """
    Abstract base class for a video source
    """

    def __init__(self) -> None:
        self.stopped = False

    @abstractmethod
    def get_fps(self: Self) -> float:
        """
        Get the frames per second of the video
        :return: The frames per second
        """

    @abstractmethod
    def get_frame(self: Self) -> npt.NDArray[np.float32] | None:
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

    def __init__(self, file_path: str) -> None:
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
        self.stopped = False

    def get_fps(self: Self) -> float:
        """
        Get the frames per second of the video
        :return: The frames per second
        """
        return self.source_fps

    def get_frame(self: Self) -> npt.NDArray[np.float32] | None:
        """
        Get the next frame from the video
        :return: The frame and the timestamp
        """
        ret, frame = self.cap.read()
        if not ret:
            self.stopped = True
            return None

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Crop the image to a square aspect ratio
        return frame[  # type: ignore
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

    def __init__(self, camera_index: int) -> None:
        super().__init__()
        camera.init()
        cameras = camera.list_cameras()
        print(f"Available cameras: {cameras}")
        assert camera_index < len(cameras), f"Invalid camera index: {camera_index}"

        self.camera_id = camera_index
        self.camera = camera.Camera(cameras[camera_index])
        self.camera.start()
        self.camera.set_controls(hflip=True)
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

    def get_frame(self: Self) -> npt.NDArray[np.float32] | None:
        """
        Get the next frame from the video
        :return: The frame and the timestamp
        """
        if self.camera.query_image():
            frame = Surface(self.size)
            image = self.camera.get_image()
            frame.blit(image, (0, 0), ((self.left_offset, self.top_offset), self.size))
            return surfarray.array3d(frame)  # type: ignore

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
