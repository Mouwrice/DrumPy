from matplotlib import pyplot as plt
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
from mediapipe.tasks.python.vision import PoseLandmarkerOptions

from tracker.tracker import Tracker


class MediaPipeTracker(Tracker):
    def __init__(self):
        super().__init__()

    def start_capture(self):
        model_path = './pose_landmarker_full.task'

        options = PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=vision.RunningMode.IMAGE,
            output_segmentation_masks=True)

        landmarker = vision.PoseLandmarker.create_from_options(options)

        # STEP 3: Load the input image.
        image = mp.Image.create_from_file("./image.jpg")

        # STEP 4: Detect pose landmarks from the input image.
        detection_result = landmarker.detect(image)

        # STEP 5: Process the detection result. In this case, visualize it.
        annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)
        plt.imshow(annotated_image, interpolation='nearest')
        plt.show()

        segmentation_mask = detection_result.segmentation_masks[0].numpy_view()
        plt.imshow(segmentation_mask, interpolation='nearest')
        plt.show()


def draw_landmarks_on_image(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)

    # Loop through the detected poses to visualize.
    for idx in range(len(pose_landmarks_list)):
        pose_landmarks = pose_landmarks_list[idx]

        # Draw the pose landmarks.
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
        ])
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style())
    return annotated_image
