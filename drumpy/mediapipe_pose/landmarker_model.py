from enum import Enum


class LandmarkerModel(Enum):
    LITE = "./resources/pose_landmarker_models/pose_landmarker_lite.task"
    FULL = "./pose_landmarker_models/pose_landmarker_full.task"
    HEAVY = "./pose_landmarker_models/pose_landmarker_heavy.task"
