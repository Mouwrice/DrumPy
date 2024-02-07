import numpy as np


class Marker:
    """
    A marker is a point on the body that can be tracked by QTM.
    """

    def __init__(self, label: str, index: int):
        self.label = label
        # index is the index of the marker in the QTM project
        # because the python SDK is made by baboons, the label is not available
        self.index = index

        # the position of the marker in 3D space, X, Y, Z
        self.pos = np.array((0, 0, 0))
