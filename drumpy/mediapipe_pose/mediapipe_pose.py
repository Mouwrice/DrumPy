from typing import Self, Optional

import numpy as np
import numpy.typing as npt
from drumpy.mediapipe_pose.landmark_type import LandmarkType
from drumpy.mediapipe_pose.landmarker_model import LandmarkerModel
from drumpy.tracking.drum_trackers import DrumTrackers
from drumpy.trajectory_file import TrajectoryFile
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
from drumpy.mediapipe_pose.process_result import ResultProcessor


def visualize_landmarks(
    rgb_image: npt.NDArray[np.float64], detection_result: PoseLandmarkerResult
) -> npt.NDArray[np.float64]:
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

    def __init__(
        self: Self,
        running_mode: RunningMode,
        landmark_type: LandmarkType,
        drum_trackers: Optional[DrumTrackers] = None,
        model: LandmarkerModel = LandmarkerModel.FULL,
        delegate: BaseOptions.Delegate = BaseOptions.Delegate.GPU,
        log_file: Optional[str] = None,
    ) -> None:
        """
        Initialize the MediaPipePose class
        :param running_mode: Whether the pose estimation is in live stream mode, causing the result to be
        returned asynchronously and frames can be dropped
        :param model: The model to use for the pose estimation
        :param log_file: The file to log the landmarks to, if None no logging will be done
        :param delegate: The delegate to use for the pose estimation, Either CPU or GPU
        """
        self.frame_count = 0
        self.model = model

        self.options = PoseLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path=self.model.value,
                delegate=delegate,
            ),
            running_mode=running_mode,
            result_callback=self.result_callback
            if running_mode == RunningMode.LIVE_STREAM
            else None,
        )

        self.landmarker = PoseLandmarker.create_from_options(self.options)
        self.detection_result = None
        self.latest_timestamp: int = (
            0  # The timestamp of the latest frame that was processed
        )
        self.latency: int = 0  # The latency of the pose estimation, in milliseconds
        self.visualisation: npt.NDArray[np.float32] | None = None

        self.landmark_type = landmark_type

        self.csv_writer = None
        if log_file is not None:
            self.log_file_path = log_file
            self.csv_writer = TrajectoryFile(self.log_file_path)

        self.drum_trackers = drum_trackers

        self.result_processor = ResultProcessor(landmark_type=self.landmark_type)

    def result_callback(
        self: Self, result: PoseLandmarkerResult, image: Image, timestamp_ms: int
    ) -> None:
        """
        Callback method to receive the result of the pose estimation
        :param result:
        :param image: Original image the landmarks were detected on
        :param timestamp_ms: The timestamp of the frame
        :return:
        """
        result = self.result_processor.process_result(result, timestamp_ms)
        self.detection_result = result
        self.latency = timestamp_ms - self.latest_timestamp
        self.latest_timestamp = timestamp_ms
        if self.drum_trackers is not None:
            self.drum_trackers.drum.check_calibrations()
        if (
            result.pose_world_landmarks is not None
            and len(result.pose_world_landmarks) > 0
            and self.drum_trackers is not None
        ):
            self.drum_trackers.update(result.pose_world_landmarks[0])

        self.visualisation = visualize_landmarks(
            image.numpy_view(), self.detection_result
        )

        self.frame_count += 1
        if self.csv_writer is not None:
            self.write_landmarks(result, timestamp_ms)

    def write_landmarks(
        self: Self, result: PoseLandmarkerResult, timestamp_ms: int
    ) -> None:
        """
        Write the landmarks to a file
        :param result: The result of the pose estimation
        :param timestamp_ms: The timestamp of the frame
        :return:
        """
        if result.pose_landmarks is None or len(result.pose_landmarks) == 0:
            return

        pose_landmarks = None
        match self.landmark_type:
            case LandmarkType.LANDMARKS:
                pose_landmarks = result.pose_landmarks[0]
            case LandmarkType.WORLD_LANDMARKS:
                pose_landmarks = result.pose_world_landmarks[0]

        for i, landmark in enumerate(pose_landmarks):
            self.csv_writer.write(
                self.frame_count,
                timestamp_ms,
                i,
                landmark.x,
                landmark.y,
                landmark.z,
                self.landmark_type,
                landmark.visibility,
                landmark.presence,
            )

    def process_image(
        self: Self, image_array: npt.NDArray[np.float32], timestamp_ms: int
    ) -> None:
        """
        Process the image
        :param timestamp_ms: The timestamp of the frame
        :param image_array: The image to process
        :return: The landmarks
        """
        image = Image(image_format=ImageFormat.SRGB, data=image_array)
        match self.options.running_mode:
            case RunningMode.LIVE_STREAM:
                self.landmarker.detect_async(image, timestamp_ms)
            case RunningMode.VIDEO:
                result = self.landmarker.detect_for_video(image, timestamp_ms)
                self.result_callback(result, image, timestamp_ms)
            case _:
                pass
