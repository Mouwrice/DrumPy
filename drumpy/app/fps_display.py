from typing import Self

from mediapipe.tasks.python.vision import RunningMode
from pygame import Rect
from pygame_gui import UIManager
from pygame_gui.elements import UILabel

from drumpy.tracking.mediapipe_pose import MediaPipePose

MEMORY = 30


class FPSDisplay(UILabel):
    """
    UILabel to display the UI FPS and the camera FPS
    """

    def __init__(
        self: Self,
        ui_manager: UIManager,
        media_pipe_pose: MediaPipePose,
    ) -> None:
        mode = ""
        match media_pipe_pose.options.running_mode:
            case RunningMode.LIVE_STREAM:
                mode = "Async Mode"
            case RunningMode.VIDEO:
                mode = "Blocking Mode"
        self.model = media_pipe_pose.model
        super().__init__(
            Rect((0, 0), (900, 50)),
            f"UI FPS: -:--  Camera FPS: -:--   {mode}  Model: {self.model}",
            manager=ui_manager,
            anchors={"top": "top", "left": "left"},
        )

        self.ui_time_deltas = []
        self.mediapipe_time_deltas = []

        self.media_pipe_pose = media_pipe_pose
        self.ui_manager = ui_manager

    def update(self: Self, time_delta: float) -> None:
        super().update(time_delta)

        self.ui_time_deltas.append(time_delta)
        if len(self.ui_time_deltas) > MEMORY:
            self.ui_time_deltas.pop(0)

        self.mediapipe_time_deltas.append(self.media_pipe_pose.latency)
        if len(self.mediapipe_time_deltas) > MEMORY:
            self.mediapipe_time_deltas.pop(0)

        if len(self.ui_time_deltas) == 0 or len(self.mediapipe_time_deltas) == 0:
            return

        ui_time_deltas_sum = sum(self.ui_time_deltas)
        if ui_time_deltas_sum <= 0:
            return

        ui_fps = 1 / (ui_time_deltas_sum / len(self.ui_time_deltas))

        mediapipe_time_deltas_sum = sum(self.mediapipe_time_deltas)
        if mediapipe_time_deltas_sum <= 0:
            return
        camera_fps = 1000 / (
            mediapipe_time_deltas_sum / len(self.mediapipe_time_deltas)
        )

        mode = ""
        match self.media_pipe_pose.options.running_mode:
            case RunningMode.LIVE_STREAM:
                mode = "Async Mode"
            case RunningMode.VIDEO:
                mode = "Blocking Mode"
        self.set_text(
            f"UI FPS: {ui_fps:.2f}  Camera FPS: {camera_fps:.2f}   {mode}  Model: {self.model}"
        )
