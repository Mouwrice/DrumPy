from multiprocessing import Pool
from typing import Any

import numpy as np
import pygame
from numpy import ndarray, dtype
from pygame_gui.elements import UIImage

from app.graphs.ui_constants import GRAPH_FRAME_RANGE
from tracker.mediapipe_pose import MediaPipePose


def plot_marker_location_graph(
    marker_locations: [(float, float, float)], frame: int, title: str
) -> ndarray | ndarray[Any, dtype[Any]]:
    """
    Plots the marker location graph using matplotlib writing the plot to a BytesIO object
    Cannot be a method of the MarkerLocationGraph class because it is used in a multiprocessing Pool
    :param frame: The current frame number
    :param marker_locations: The marker locations to plot
    """
    import matplotlib.pyplot as plt
    import io

    fig, ax = plt.subplots()
    # Generate frame numbers
    frame_range = np.arange(frame - len(marker_locations), frame)
    # Extract x, y, z from the marker locations
    x = [location[2] for location in marker_locations]
    y = [-location[0] for location in marker_locations]
    z = [location[1] for location in marker_locations]
    ax.plot(frame_range, x, label="X", color="red")
    ax.plot(frame_range, y, label="Y", color="green")
    ax.plot(frame_range, z, label="Z", color="blue")

    ax.set_xlabel("Frame")
    ax.set_ylabel("Location (m)")
    ax.legend()
    ax.set_title(title)

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return buf


class MarkerLocationGraph(UIImage):
    """
    Class to display the marker location as a graph using 3D coordinates as lines
    """

    def __init__(
        self,
        marker_idx: int,
        relative_rect: pygame.Rect,
        image_surface: pygame.surface.Surface,
        pool: Pool,
        media_pipe_pose: MediaPipePose,
        title: str,
    ):
        super().__init__(relative_rect, image_surface)
        self.marker_idx = marker_idx
        self.marker_locations: [(float, float, float)] = []
        self.media_pipe_pose = media_pipe_pose
        self.frame = 0
        self.plot_async_result = None
        self.pool = pool
        self.title = title

    def update(self, time_delta: float):
        super().update(time_delta)
        self.frame += 1

        if (
            self.media_pipe_pose.detection_result is not None
            and self.media_pipe_pose.detection_result.pose_world_landmarks is not None
        ):
            landmarks = self.media_pipe_pose.detection_result.pose_world_landmarks
            if len(landmarks) > 0:
                landmarks = landmarks[0]
                if self.marker_idx < len(landmarks):
                    landmark = landmarks[self.marker_idx]
                    self.marker_locations.append((landmark.x, landmark.y, landmark.z))
                    if len(self.marker_locations) > GRAPH_FRAME_RANGE:
                        self.marker_locations.pop(0)

        if self.plot_async_result is None:
            self.plot_async_result = self.pool.apply_async(
                plot_marker_location_graph,
                (self.marker_locations, self.frame, self.title),
            )
        elif self.plot_async_result.ready():
            image = self.plot_async_result.get()
            self.set_image(pygame.image.load(image))
            self.plot_async_result = self.pool.apply_async(
                plot_marker_location_graph,
                (self.marker_locations, self.frame, self.title),
            )
