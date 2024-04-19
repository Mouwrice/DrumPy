from enum import IntEnum
from typing import Self


class MarkerEnum(IntEnum):
    """
    From the documentation:
    0 - nose
    1 - left eye (inner)
    2 - left eye
    3 - left eye (outer)
    4 - right eye (inner)
    5 - right eye
    6 - right eye (outer)
    7 - left ear
    8 - right ear
    9 - mouth (left)
    10 - mouth (right)
    11 - left shoulder
    12 - right shoulder
    13 - left elbow
    14 - right elbow
    15 - left wrist
    16 - right wrist
    17 - left pinky
    18 - right pinky
    19 - left index
    20 - right index
    21 - left thumb
    22 - right thumb
    23 - left hip
    24 - right hip
    25 - left knee
    26 - right knee
    27 - left ankle
    28 - right ankle
    29 - left heel
    30 - right heel
    31 - left foot index
    32 - right foot index
    """

    NOSE = 0
    LEFT_EYE_INNER = 1
    LEFT_EYE = 2
    LEFT_EYE_OUTER = 3
    RIGHT_EYE_INNER = 4
    RIGHT_EYE = 5
    RIGHT_EYE_OUTER = 6
    LEFT_EAR = 7
    RIGHT_EAR = 8
    MOUTH_LEFT = 9
    MOUTH_RIGHT = 10
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_ELBOW = 13
    RIGHT_ELBOW = 14
    LEFT_WRIST = 15
    RIGHT_WRIST = 16
    LEFT_PINKY = 17
    RIGHT_PINKY = 18
    LEFT_INDEX = 19
    RIGHT_INDEX = 20
    LEFT_THUMB = 21
    RIGHT_THUMB = 22
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_KNEE = 25
    RIGHT_KNEE = 26
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28
    LEFT_HEEL = 29
    RIGHT_HEEL = 30
    LEFT_FOOT_INDEX = 31
    RIGHT_FOOT_INDEX = 32

    # Some own additions
    LEFT_DRUM_STICK = 33
    RIGHT_DRUM_STICK = 34
    LEFT_FOOT = 35
    RIGHT_FOOT = 36

    @staticmethod
    def from_qtm_label(label: str) -> "MarkerEnum":  # noqa: PLR0911
        match label:
            case "Nose":
                return MarkerEnum.NOSE
            case "Eye_Inner_L":
                return MarkerEnum.LEFT_EYE_INNER
            case "Eye_L":
                return MarkerEnum.LEFT_EYE
            case "Eye_Outer_L":
                return MarkerEnum.LEFT_EYE_OUTER
            case "Eye_Inner_R":
                return MarkerEnum.RIGHT_EYE_INNER
            case "Eye_R":
                return MarkerEnum.RIGHT_EYE
            case "Eye_Outer_R":
                return MarkerEnum.RIGHT_EYE_OUTER
            case "Ear_L":
                return MarkerEnum.LEFT_EAR
            case "Ear_R":
                return MarkerEnum.RIGHT_EAR
            case "Mouth_L":
                return MarkerEnum.MOUTH_LEFT
            case "Mouth_R":
                return MarkerEnum.MOUTH_RIGHT
            case "Shoulder_L":
                return MarkerEnum.LEFT_SHOULDER
            case "Shoulder_R":
                return MarkerEnum.RIGHT_SHOULDER
            case "Elbow_L":
                return MarkerEnum.LEFT_ELBOW
            case "Elbow_R":
                return MarkerEnum.RIGHT_ELBOW
            case "Wrist_L":
                return MarkerEnum.LEFT_WRIST
            case "Wrist_R":
                return MarkerEnum.RIGHT_WRIST
            case "Pinky_L":
                return MarkerEnum.LEFT_PINKY
            case "Pinky_R":
                return MarkerEnum.RIGHT_PINKY
            case "Index_L":
                return MarkerEnum.LEFT_INDEX
            case "Index_R":
                return MarkerEnum.RIGHT_INDEX
            case "Thumb_L":
                return MarkerEnum.LEFT_THUMB
            case "Thumb_R":
                return MarkerEnum.RIGHT_THUMB
            case "Hip_L":
                return MarkerEnum.LEFT_HIP
            case "Hip_R":
                return MarkerEnum.RIGHT_HIP
            case "Knee_L":
                return MarkerEnum.LEFT_KNEE
            case "Knee_R":
                return MarkerEnum.RIGHT_KNEE
            case "Ankle_L":
                return MarkerEnum.LEFT_ANKLE
            case "Ankle_R":
                return MarkerEnum.RIGHT_ANKLE
            case "Heel_L":
                return MarkerEnum.LEFT_HEEL
            case "Heel_R":
                return MarkerEnum.RIGHT_HEEL
            case "Foot_Index_L":
                return MarkerEnum.LEFT_FOOT_INDEX
            case "Foot_Index_R":
                return MarkerEnum.RIGHT_FOOT_INDEX
            case _:
                raise ValueError(f"Unknown label: {label}")

    def __str__(self: Self) -> str:
        return self.name.replace("_", " ").title()
