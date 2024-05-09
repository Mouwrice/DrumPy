from typing import TypeAlias

import numpy as np
import numpy.typing as npt
from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark  # type: ignore

# Type for a 3D position, x, y, z
Position: TypeAlias = npt.NDArray[np.float64]


def position_str(position: Position) -> str:
    """
    Print a position with 3 decimal places
    """
    return f"[{', '.join([f'{x:.3f}' for x in position])}]"


def landmark_to_position(landmark: NormalizedLandmark) -> Position:
    """
    Convert a mediapipe landmark to a numpy array
    Also switches some axes around:
    x = z
    y = y
    z = -x
    """
    assert landmark.x is not None
    assert landmark.y is not None
    assert landmark.z is not None
    x = landmark.z
    y = landmark.y
    z = -landmark.x
    return np.array([x, y, z])


def distance_no_depth(a: Position, b: Position) -> float:
    """
    Calculate the distance between two 3D positions without considering the depth, the x-axis
    :param a:
    :param b:
    :return:
    """
    return float(np.linalg.norm(a[1:] - b[1:]))
