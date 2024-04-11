from enum import Enum


class LandmarkType(Enum):
    """
    From the MediaPipe documentation:

    The output contains both normalized coordinates (Landmarks) and world coordinates (WorldLandmarks)
        for each landmark.

    The output contains the following normalized coordinates (Landmarks):
        - x and y: Landmark coordinates normalized between 0.0 and 1.0 by the image width (x) and height (y).
        - z: The landmark depth, with the depth at the midpoint of the hips as the origin. The smaller the value,
            the closer the landmark is to the camera. The magnitude of z uses roughly the same scale as x.
        - visibility: The likelihood of the landmark being visible within the image.

    The output contains the following world coordinates (WorldLandmarks):
        - x, y, and z: Real-world 3-dimensional coordinates in meters, with the midpoint of the hips as the origin.
        - visibility: The likelihood of the landmark being visible within the image.
    """

    LANDMARKS = 0
    WORLD_LANDMARKS = 1
