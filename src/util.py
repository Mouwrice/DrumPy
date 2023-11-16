import numpy.typing as npt
import numpy as np


def print_float_array(array: npt.NDArray[np.float64]) -> str:
    return f"[{', '.join([f'{x:.3f}' for x in array])}]"
