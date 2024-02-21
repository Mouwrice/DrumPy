import io
from multiprocessing import Pool

import pygame
from pygame_gui.elements import UIImage

from app.graphs.ui_constants import GRAPH_FRAME_RANGE
from tracker.mediapipe_pose import MediaPipePose


def plot_latency_graph(
    ui_latencies: [float], mediapipe_latencies: [float], frame: int
) -> io.BytesIO:
    """
    Plots the latency graph using matplotlib writing the plot to a BytesIO object
    Cannot be a method of the LatencyGraph class because it is used in a multiprocessing Pool
    :param frame: The current frame number
    :param ui_latencies: The UI latencies to plot
    :param mediapipe_latencies: The mediapipe inference latency to plot
    """
    import matplotlib.pyplot as plt
    import io
    import numpy as np

    fig, ax = plt.subplots()

    # generate x values
    x = np.arange(frame - len(ui_latencies), frame)
    # Plot ui latencies in blue and mediapipe latencies in orange
    ax.plot(x, ui_latencies, label="UI Latency", color="blue")
    ax.plot(x, mediapipe_latencies, label="MediaPipe Latency", color="orange")

    ax.set_xlabel("Frame")
    ax.set_ylabel("Latency (ms)")
    ax.set_title("Latency Graph")

    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    plt.close(fig)

    return buf


class LatencyGraph(UIImage):
    """
    Plots the latency between frames using matplotlib and converts the plot to a pygame surface
    """

    def __init__(
        self,
        pool: Pool,
        media_pipe_pose: MediaPipePose,
    ):
        super().__init__(
            relative_rect=pygame.Rect(1100, 50, 400, 300),
            image_surface=pygame.Surface((400, 300)),
        )

        self.ui_latencies = []
        self.mediapipe_latencies = []
        self.pool = pool
        self.plot_async_result = None
        self.media_pipe_pose = media_pipe_pose
        self.frame = 0

    def update(self, time_delta: float):
        super().update(time_delta)

        self.frame += 1

        self.ui_latencies.append(time_delta * 1000)
        if len(self.ui_latencies) > GRAPH_FRAME_RANGE:
            self.ui_latencies.pop(0)

        self.mediapipe_latencies.append(self.media_pipe_pose.latency)
        if len(self.mediapipe_latencies) > GRAPH_FRAME_RANGE:
            self.mediapipe_latencies.pop(0)

        # If the plot is not being generated, start the process
        if self.plot_async_result is None:
            self.plot_async_result = self.pool.apply_async(
                plot_latency_graph,
                (self.ui_latencies, self.mediapipe_latencies, self.frame),
            )
        # If the plot is ready, set the image
        elif self.plot_async_result.ready():
            image = self.plot_async_result.get()
            self.set_image(pygame.image.load(image))
            self.plot_async_result = self.pool.apply_async(
                plot_latency_graph,
                (self.ui_latencies, self.mediapipe_latencies, self.frame),
            )
