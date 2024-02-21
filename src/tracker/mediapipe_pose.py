from enum import Enum

import numpy as np
from mediapipe import Image, ImageFormat
from mediapipe.framework.formats import landmark_pb2
from mediapipe.python import solutions
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import (
    PoseLandmarkerOptions,
    PoseLandmarker,
    PoseLandmarkerResult,
    RunningMode,
)
from numpy import ndarray


class LandmarkerModel(Enum):
    LITE = "./pose_landmarker_lite.task"
    FULL = "./pose_landmarker_full.task"
    HEAVY = "./pose_landmarker_heavy.task"


def visualize_landmarks(
    rgb_image: ndarray, detection_result: PoseLandmarkerResult
) -> ndarray:
    """
    Visualize the landmarks on the image given the landmarks and the image
    """
    rgb_image = np.copy(rgb_image)  # Make a copy of the image
    pose_landmarks_list = detection_result.pose_landmarks

    # Loop through the detected poses to visualize.
    for idx in range(len(pose_landmarks_list)):
        pose_landmarks = pose_landmarks_list[idx]

        # Draw the pose landmarks.
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend(
            [
                landmark_pb2.NormalizedLandmark(
                    x=landmark.x, y=landmark.y, z=landmark.z
                )
                for landmark in pose_landmarks
            ]
        )
        solutions.drawing_utils.draw_landmarks(
            rgb_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style(),
        )
    return rgb_image


class MediaPipePose:
    """
    Class to handle the pose estimation using MediaPipe
    """

    def __init__(self, live_stream: bool = True):
        options = PoseLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path=LandmarkerModel.FULL.value,
                delegate=BaseOptions.Delegate.GPU,
            ),
            running_mode=RunningMode.LIVE_STREAM if live_stream else RunningMode.VIDEO,
            result_callback=self.result_callback if live_stream else None,
        )

        self.landmarker = PoseLandmarker.create_from_options(options)
        self.result = None
        self.image_landmarks: ndarray | None = (
            None  # The image with the landmarks represented as an array
        )
        self.latest_timestamp: int = (
            0  # The timestamp of the latest frame that was processed
        )
        self.latency: int = 1  # The latency of the pose estimation, in milliseconds
        self.live_stream = (
            live_stream  # Whether the pose estimation is in live stream mode
        )

    def result_callback(
        self, result: PoseLandmarkerResult, image: Image, timestamp_ms: int
    ):
        """
        Callback method to receive the result of the pose estimation
        :param result:
        :param image: Original image the landmarks were detected on
        :param timestamp_ms: The timestamp of the frame
        :return:
        """
        self.result = result
        image_landmarks = visualize_landmarks(image.numpy_view(), result)
        self.image_landmarks = image_landmarks
        self.latency = timestamp_ms - self.latest_timestamp
        self.latest_timestamp = timestamp_ms

    def process_image(self, image_array: ndarray, timestamp_ms: int):
        """
        Process the image
        :param timestamp_ms: The timestamp of the frame
        :param image_array: The image to process
        :return: The landmarks
        """
        image = Image(image_format=ImageFormat.SRGB, data=image_array)
        if self.live_stream:
            self.landmarker.detect_async(image, timestamp_ms)
        else:
            result = self.landmarker.detect_for_video(image, timestamp_ms)
            self.result_callback(result, image, timestamp_ms)
