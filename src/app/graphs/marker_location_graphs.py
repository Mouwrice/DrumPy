from multiprocessing import Pool

import pygame

from app.graphs.marker_location_graph import MarkerLocationGraph
from drum_tracking.mediapipe_markers import Marker
from tracker.mediapipe_pose import MediaPipePose


class MarkerLocationGraphs:
    """
    Instantiates a graph for both the wrists and feet
    """

    def __init__(self, pool: Pool, media_pipe_pose: MediaPipePose):
        MarkerLocationGraph(
            Marker.LEFT_WRIST.value,
            pygame.Rect(0, 50, 400, 300),
            pygame.Surface((400, 300)),
            pool,
            media_pipe_pose,
            "Left Wrist Location Graph",
        )
        MarkerLocationGraph(
            Marker.RIGHT_WRIST.value,
            pygame.Rect(0, 350, 400, 300),
            pygame.Surface((400, 300)),
            pool,
            media_pipe_pose,
            "Right Wrist Location Graph",
        )
        MarkerLocationGraph(
            Marker.LEFT_FOOT.value,
            pygame.Rect(1400, 350, 400, 300),
            pygame.Surface((400, 300)),
            pool,
            media_pipe_pose,
            "Left Foot Location Graph",
        )
        MarkerLocationGraph(
            Marker.RIGHT_FOOT.value,
            pygame.Rect(1400, 650, 400, 300),
            pygame.Surface((400, 300)),
            pool,
            media_pipe_pose,
            "Right Foot Location Graph",
        )
