from typing import Self

from mediapipe.tasks.python.vision import RunningMode  # type: ignore
from pygame import Rect
from pygame_gui import UIManager  # type: ignore
from pygame_gui.elements import UILabel  # type: ignore

from drumpy.mediapipe_pose.mediapipe_pose import MediaPipePose

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
        match media_pipe_pose.options.running_mode:  # type: ignore
            case RunningMode.LIVE_STREAM:  # type: ignore
                mode = "Async Mode"
            case RunningMode.VIDEO:  # type: ignore
                mode = "Blocking Mode"
            case _:  # type: ignore
                pass

        self.model = media_pipe_pose.model
        super().__init__(
            Rect((0, 0), (900, 50)),
            f"UI FPS: -:--  Camera FPS: -:--   {mode}  Model: {self.model}",
            manager=ui_manager,
            anchors={"top": "top", "left": "left"},
        )

        self.ui_time_deltas: list[float] = []
        self.mediapipe_time_deltas: list[int] = []

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
        match self.media_pipe_pose.options.running_mode:  # type: ignore
            case RunningMode.LIVE_STREAM:  # type: ignore
                mode = "Async Mode"
            case RunningMode.VIDEO:  # type: ignore
                mode = "Blocking Mode"
            case _:  # type: ignore
                pass

        self.set_text(
            f"UI FPS: {ui_fps:.2f}  Camera FPS: {camera_fps:.2f}   {mode}  Model: {self.model}"
        )
