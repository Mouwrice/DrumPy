from pygame import display
from pygame_chart import Figure


class FPSGraph:
    def __init__(self, screen: display):
        self.figure = Figure(screen, 0, 0, 200, 100)
        self.time_deltas = []
        self.frames = []

    def update(self, frame: int, time_delta: float):
        self.frames.append(frame)
        if len(self.frames) > 30:
            self.frames.pop(0)
        self.time_deltas.append(time_delta)
        if len(self.time_deltas) > 30:
            self.time_deltas.pop(0)
        self.figure.line("FPS", self.frames, self.time_deltas)

        if len(self.frames) > 3:
            self.figure.draw()
