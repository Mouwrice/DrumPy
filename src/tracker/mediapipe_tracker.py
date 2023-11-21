import time
from enum import Enum

import cv2
from mediapipe import solutions, Image, ImageFormat
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
from mediapipe.tasks.python.vision import PoseLandmarkerOptions, PoseLandmarkerResult

from csv_object import CSVObject
from drum import Drum
from tracker.marker import Marker
from tracker.marker_tracker import MarkerTracker


class LandmarkerModel(Enum):
    LITE = "./pose_landmarker_lite.task"
    FULL = "./pose_landmarker_full.task"
    HEAVY = "./pose_landmarker_heavy.task"


class MediaPipeTracker:
    def __init__(self, drum: Drum, normalize: bool = False, log_to_file: bool = False,
                 model: LandmarkerModel = LandmarkerModel.FULL):
        """
        :param drum:
        :param normalize: Whether to use normalized coordinates or not
        :param log_to_file: Whether to log the coordinates to a CSV file
        """
        super().__init__()
        self.drum = drum
        self.normalize = normalize

        self.model = model
        self.detection_result: PoseLandmarkerResult | None = None

        if not normalize:
            self.left_wrist_marker = Marker("Left Wrist", 15)
            self.left_wrist_tracker = MarkerTracker("Left Wrist",
                                                    [0, 1, 3],  # 5, 6],
                                                    drum,
                                                    memory=10,
                                                    downward_trend=-0.02, upward_trend=0.01)

            self.right_wrist_marker = Marker("Right Wrist", 16)
            self.right_wrist_tracker = MarkerTracker("Right Wrist",
                                                     [0, 1, 3],  # 5, 6],
                                                     drum,
                                                     memory=10,
                                                     downward_trend=-0.02, upward_trend=0.01)

            self.left_foot_marker = Marker("Left Foot", 31)
            self.left_foot_tracker = MarkerTracker("Left Foot", [],  # 3]
                                                   downward_trend=-0.005,
                                                   upward_trend=-0.001,
                                                   drum=drum)

            self.right_foot_marker = Marker("Right Foot", 32)
            self.right_foot_tracker = MarkerTracker("Right Foot", [2],
                                                    downward_trend=-0.005,
                                                    upward_trend=-0.001,
                                                    drum=drum)

        else:
            self.left_wrist_marker = Marker("Left Wrist", 15)
            self.left_wrist_tracker = MarkerTracker("Left Wrist", [0, 1, 3],  # 5, 6],
                                                    drum,
                                                    memory=10,
                                                    downward_trend=-0.04,
                                                    upward_trend=0.02)

            self.right_wrist_marker = Marker("Right Wrist", 16)
            self.right_wrist_tracker = MarkerTracker("Right Wrist", [0, 1, 3],  # 5, 6],
                                                     drum,
                                                     memory=10,
                                                     downward_trend=-0.035,
                                                     upward_trend=0.015)

            self.left_foot_marker = Marker("Left Foot", 31)
            self.left_foot_tracker = MarkerTracker("Left Foot", [],  # 3]
                                                   downward_trend=-0.005,
                                                   upward_trend=-0.002,
                                                   drum=drum)

            self.right_foot_marker = Marker("Right Foot", 32)
            self.right_foot_tracker = MarkerTracker("Right Foot", [2],
                                                    downward_trend=-0.005,
                                                    upward_trend=-0.002,
                                                    drum=drum)

        self.csv_writer = None
        if log_to_file is not None:
            log_file = f"./{time.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
            self.csv_writer = CSVObject(log_file)

    def result_callback(self, result: PoseLandmarkerResult, frame: int):
        """
        Callback function to receive the detection result.
        """
        self.detection_result = result

        if result is None or result.pose_world_landmarks is None or len(result.pose_world_landmarks) == 0:
            return

        if result.pose_landmarks is None or len(result.pose_landmarks) == 0:
            return

        if self.normalize:
            landmarks = result.pose_landmarks[0]
        else:
            landmarks = result.pose_world_landmarks[0]
        left_hand = landmarks[self.left_wrist_marker.index]
        right_hand = landmarks[self.right_wrist_marker.index]
        left_foot = landmarks[self.left_foot_marker.index]
        right_foot = landmarks[self.right_foot_marker.index]

        self.left_wrist_tracker.update(np.array([left_hand.z, left_hand.x, left_hand.y]))
        self.right_wrist_tracker.update(np.array([right_hand.z, right_hand.x, right_hand.y]))
        self.left_foot_tracker.update(np.array([left_foot.z, left_foot.x, left_foot.y]))
        self.right_foot_tracker.update(np.array([right_foot.z, right_foot.x, right_foot.y]))

        if self.csv_writer is not None:
            self.write_landmarks(result, frame)

    def write_landmarks(self, result: PoseLandmarkerResult, frame: int):
        if self.normalize:
            landmarks = result.pose_landmarks[0]
        else:
            landmarks = result.pose_world_landmarks[0]

        for i, landmark in enumerate(landmarks):
            self.csv_writer.write(frame, time.time_ns(), i, landmark.z, landmark.x, landmark.y)

    def start_capture(self):
        # Variables to calculate FPS
        counter, fps = 0, 0
        start_time = time.time()

        # Start capturing video input from the camera
        cap = cv2.VideoCapture(0)

        # Visualization parameters
        row_size = 20  # pixels
        left_margin = 24  # pixels
        text_color = (0, 255, 0)  # green
        font_size = 1
        font_thickness = 1
        fps_avg_frame_count = 10

        # Create a pose landmarker instance
        options = PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=self.model.value, delegate=BaseOptions.Delegate.CPU),
            running_mode=vision.RunningMode.IMAGE,
            output_segmentation_masks=True,
            # result_callback=self.result_callback
        )

        landmarker = vision.PoseLandmarker.create_from_options(options)
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened():
            raise Exception("Could not open video device")

        while video_capture.isOpened():
            success, frame = video_capture.read()
            if not success:
                raise Exception("Could not read frame")

            counter += 1

            mp_image = mp.Image(image_format=ImageFormat.SRGB, data=frame)
            # landmarker.detect_async(mp_image, int((time.time_ns() - start_time) / 1e6))
            self.detection_result = landmarker.detect(mp_image)
            self.result_callback(self.detection_result, counter)

            # Calculate the FPS
            if counter % fps_avg_frame_count == 0:
                end_time = time.time()
                fps = fps_avg_frame_count / (end_time - start_time)
                start_time = time.time()

                self.drum.check_calibrations()

            # Show the FPS
            fps_text = 'FPS = {:.1f}'.format(fps)
            text_location = (left_margin, row_size)
            cv2.putText(frame, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                        font_size, text_color, font_thickness)

            if self.detection_result is not None:
                vis_image = self.visualize(frame)
                cv2.imshow('object_detector', vis_image)
            else:
                cv2.imshow('object_detector', frame)

            # Stop the program if the ESC key is pressed.
            if cv2.waitKey(1) == 27:
                break

        landmarker.close()
        cap.release()
        cv2.destroyAllWindows()

    def visualize(self, rgb_image):
        pose_landmarks_list = self.detection_result.pose_landmarks
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
