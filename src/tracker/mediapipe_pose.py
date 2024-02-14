from enum import Enum

from mediapipe import Image, ImageFormat
from mediapipe.framework.formats import landmark_pb2
from mediapipe.python import solutions
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import (
    PoseLandmarkerOptions,
    PoseLandmarker,
    PoseLandmarkerResult,
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

    def __init__(self):
        options = PoseLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path=LandmarkerModel.LITE.value,
                delegate=BaseOptions.Delegate.GPU,
            )
        )

        self.landmarker_model = PoseLandmarker.create_from_options(options)

    def process_image(self, image_array: ndarray) -> PoseLandmarkerResult:
        """
        Process the image and return the landmarks
        :param image_array: The image to process
        :return: The landmarks
        """
        image_array = Image(image_format=ImageFormat.SRGB, data=image_array)
        return self.landmarker_model.detect(image_array)
