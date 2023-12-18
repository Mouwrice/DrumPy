import time
from enum import Enum

import cv2
import pygame
from mediapipe import solutions, ImageFormat
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
from mediapipe.tasks.python.vision import PoseLandmarkerOptions, PoseLandmarkerResult

from csv_objects.csv_object import CSVWriter
from cv2_utils.cv2_utils import overlay
from drum import Drum
from tracker.marker import Marker
from tracker.marker_tracker import MarkerTracker


class LandmarkerModel(Enum):
    LITE = "./pose_landmarker_lite.task"
    FULL = "./pose_landmarker_full.task"
    HEAVY = "./pose_landmarker_heavy.task"


class MediaPipeTracker:
    def __init__(self, drum: Drum, normalize: bool = False, log_to_file: bool = False,
                 model: LandmarkerModel = LandmarkerModel.FULL, source: int | str = 0, scale: float = 1.0,
                 filename: str = None):
        """
        :param drum:
        :param normalize: Whether to use normalized coordinates or not
        :param log_to_file: Whether to log the coordinates to a CSV file
        :param model: Which model to use for the pose landmarker
        :param source: The source for the video capture
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
        if log_to_file:
            self.log_file = filename if filename is not None \
                else f"./data/mediapipe_{self.model.name}_{time.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
            self.csv_writer = CSVWriter(self.log_file)

        self.source = source
        self.frame_count = 0
        self.video_time_ms = 0

        self.scale = scale

    def result_callback(self, result: PoseLandmarkerResult, _, timestamp_ms: int):
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
            self.write_landmarks(result, timestamp_ms)

    def write_landmarks(self, result: PoseLandmarkerResult, timestamp_ms: int):
        pose_landmarsks = result.pose_landmarks[0] if self.normalize else result.pose_world_landmarks[0]

        for i, landmark in enumerate(pose_landmarsks):
            self.csv_writer.write(self.frame_count, timestamp_ms, i, landmark.z, landmark.x, landmark.y,
                                  landmark.visibility,
                                  landmark.presence, normalized=self.normalize)

    def start_capture(self):
        # Variables to calculate FPS
        fps = 0
        start_time = time.time()
        fps_avg_frame_count = 5

        # Create a pose landmarker instance
        options = PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=self.model.value, delegate=BaseOptions.Delegate.GPU),
            running_mode=vision.RunningMode.VIDEO,
            output_segmentation_masks=True,
            # result_callback=self.result_callback
        )

        landmarker = vision.PoseLandmarker.create_from_options(options)
        video_capture = cv2.VideoCapture(self.source)
        source_fps = video_capture.get(cv2.CAP_PROP_FPS)
        source_width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        source_height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(f"FPS: {source_fps}")
        if not video_capture.isOpened():
            raise Exception("Could not open video device")

        video_out = None
        if self.csv_writer is not None:
            video_file_name = self.log_file.replace(".csv", ".mp4")
            video_out = cv2.VideoWriter(video_file_name, cv2.VideoWriter_fourcc(*'mp4v'), source_fps,
                                        (int(source_width * self.scale), int(source_height * self.scale)))

        while video_capture.isOpened():

            success, frame = video_capture.read()
            if not success:
                print("Could not read frame. End of stream reached?")
                break

            width = int(source_width * self.scale)
            height = int(source_height * self.scale)
            frame = cv2.resize(frame, (width, height))

            self.frame_count += 1
            self.video_time_ms = int(video_capture.get(cv2.CAP_PROP_POS_MSEC))
            mp_image = mp.Image(image_format=ImageFormat.SRGB, data=frame)
            # landmarker.detect_async(mp_image, self.video_time_ms)
            self.detection_result = landmarker.detect_for_video(mp_image, self.video_time_ms)
            self.result_callback(self.detection_result, None, self.video_time_ms)

            # Calculate the FPS
            if self.frame_count % fps_avg_frame_count == 0:
                end_time = time.time()
                fps = fps_avg_frame_count / (end_time - start_time)
                start_time = time.time()
                self.drum.check_calibrations()

            # Overlay the FPS and other information
            overlay(frame, source_fps, fps, self.frame_count, self.video_time_ms, self.model, width, height)
            if self.detection_result is not None:
                vis_image = self.visualize(frame)
                if video_out is not None:
                    video_out.write(vis_image)
                cv2.imshow('object_detector', vis_image)
            else:
                if video_out is not None:
                    video_out.write(frame)
                cv2.imshow('object_detector', frame)

            # Stop the program if the ESC key is pressed.
            if cv2.waitKey(1) == 27:
                break

        landmarker.close()
        cv2.destroyAllWindows()
        video_capture.release()
        if video_out is not None:
            video_out.release()
        if self.csv_writer is not None:
            self.csv_writer.close()

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


def track_recordings():
    recordings = [
        # "../recordings/multicam_asil_01_front.mkv",
        "../recordings/multicam_asil_01_left.mkv",
        "../recordings/multicam_asil_02_front.mkv",
        "../recordings/multicam_asil_02_left.mkv",
        "../recordings/multicam_asil_03_front.mkv",
        "../recordings/multicam_asil_03_left.mkv",
        "../recordings/multicam_ms_01_front.mkv",
        "../recordings/multicam_ms_01_right.mkv",
        "../recordings/multicam_ms_02_front.mkv",
        "../recordings/multicam_ms_02_right.mkv",
    ]

    scales = [0.25]

    models = [LandmarkerModel.LITE]

    for recording in recordings:
        for scale in scales:
            for model in models:
                file_name = recording.split("/")[-1].replace(".mkv", "")
                # omit everything after th second underscore
                directory = "_".join(file_name.split("_")[:3])
                print(f"Recording: {recording}, Scale: {scale}, Model: {model}")
                width = int(1920 * scale)
                height = int(1080 * scale)
                pose_tracker = MediaPipeTracker(drum, normalize=False, log_to_file=False, model=model,
                                                source=recording, scale=scale,
                                                filename=f"./data/{directory}/mediapipe_{file_name}_{width}_{height}_{model.name}_video.csv")
                pose_tracker.start_capture()


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.set_num_channels(64)
    drum = Drum(no_sleep=True, margin=0.1, min_margin=0.001)
    # drum.auto_calibrate()
    #
    # pose_tracker = MediaPipeTracker(drum, normalize=False, log_to_file=False, model=LandmarkerModel.FULL,
    #                                 source=0)
    # pose_tracker.start_capture()
    track_recordings()
