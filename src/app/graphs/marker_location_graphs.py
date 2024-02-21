from multiprocessing import Pool

import pygame

from app.graphs.marker_location_graph import MarkerLocationGraph
from tracker.mediapipe_pose import MediaPipePose


class MarkerLocationGraphs:
    """
    Instantiates a graph for both the wrists and feet
    """

    def __init__(self, pool: Pool, media_pipe_pose: MediaPipePose):
        MarkerLocationGraph(
            15,
            pygame.Rect(0, 50, 400, 300),
            pygame.Surface((400, 300)),
            pool,
            media_pipe_pose,
        )
        MarkerLocationGraph(
            16,
            pygame.Rect(0, 350, 400, 300),
            pygame.Surface((400, 300)),
            pool,
            media_pipe_pose,
        )
        MarkerLocationGraph(
            31,
            pygame.Rect(1100, 350, 400, 300),
            pygame.Surface((400, 300)),
            pool,
            media_pipe_pose,
        )
        MarkerLocationGraph(
            32,
            pygame.Rect(1100, 650, 400, 300),
            pygame.Surface((400, 300)),
            pool,
            media_pipe_pose,
        )
