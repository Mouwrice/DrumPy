import numpy.typing as npt
import numpy as np
from mediapipe.tasks.python.components.containers.landmark import Landmark
from nptyping import NDArray, Shape, Float64


def print_float_array(array: npt.NDArray[np.float64]) -> str:
    """
    Print a float array with 3 decimal places
    :param array:
    :return:
    """
    return f"[{', '.join([f'{x:.3f}' for x in array])}]"


def landmark_to_numpy(landmark: Landmark) -> np.array:
    """
    Convert a mediapipe landmark to a numpy array
    Also switches some axes around:
    x -> y, the horizontal axis
    y -> z, the vertical axis
    z -> x, the depth axis
    """
    return np.array([landmark.y, landmark.z, landmark.x])


# Type for a 3D position, x, y, z
Position = NDArray[Shape["3"], Float64]
# Type for a 3D velocity, x, y, z
Velocity = NDArray[Shape["3"], Float64]
