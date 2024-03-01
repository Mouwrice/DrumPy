from pygame import Rect
from pygame_gui import UIManager
from pygame_gui.elements import UILabel

from tracker.mediapipe_pose import MediaPipePose


class FPSDisplay(UILabel):
    """
    UILabel to display the UI FPS and the camera FPS
    """

    def __init__(
        self,
        ui_manager: UIManager,
        media_pipe_pose: MediaPipePose,
    ):
        mode = "Async Mode" if media_pipe_pose.live_stream else "Blocking Mode"
        self.model = media_pipe_pose.model
        super().__init__(
            Rect((0, 0), (800, 50)),
            f"UI FPS: -:--  Camera FPS: -:--   {mode}  Model: {self.model}",
            manager=ui_manager,
            anchors={"top": "top", "left": "left"},
        )

        self.ui_time_deltas = []
        self.mediapipe_time_deltas = []

        self.media_pipe_pose = media_pipe_pose
        self.ui_manager = ui_manager

    def update(self, time_delta: float):
        super().update(time_delta)

        self.ui_time_deltas.append(time_delta)
        if len(self.ui_time_deltas) > 30:
            self.ui_time_deltas.pop(0)

        self.mediapipe_time_deltas.append(self.media_pipe_pose.latency)
        if len(self.mediapipe_time_deltas) > 30:
            self.mediapipe_time_deltas.pop(0)

        ui_fps = 1 / (sum(self.ui_time_deltas) / len(self.ui_time_deltas))
        camera_fps = 1000 / (
            sum(self.mediapipe_time_deltas) / len(self.mediapipe_time_deltas)
        )

        mode = "Async Mode" if self.media_pipe_pose.live_stream else "Blocking Mode"
        self.set_text(
            f"UI FPS: {ui_fps:.2f}  Camera FPS: {camera_fps:.2f}   {mode}  Model: {self.model}"
        )
