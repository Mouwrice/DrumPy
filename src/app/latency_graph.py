import pygame
from pygame_gui.elements import UIImage


class LatencyGraph(UIImage):
    """
    Plots the latency between frames using matplotlib and converts the plot to a pygame surface
    """

    def __init__(
        self, relative_rect: pygame.Rect, image_surface: pygame.surface.Surface
    ):
        super().__init__(relative_rect, image_surface)
        self.latencies = []

    def plot_latency_graph(self) -> pygame.surface.Surface:
        """
        Plots the latency graph using matplotlib and converts the plot to a pygame surface
        """
        import matplotlib.pyplot as plt
        import io
        import numpy as np

        fig, ax = plt.subplots()
        ax.plot(np.arange(len(self.latencies)), self.latencies)
        ax.set_xlabel("Frames")
        ax.set_ylabel("Latency (s)")
        ax.set_title("Latency Graph")

        buf = io.BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        plt.close(fig)

        return pygame.image.load(buf)

    def update(self, time_delta: float):
        super().update(time_delta)

        self.latencies.append(time_delta)
        if len(self.latencies) > 30:
            self.latencies.pop(0)

        self.set_image(self.plot_latency_graph())
