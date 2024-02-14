from pygame import Rect
from pygame_gui import UIManager
from pygame_gui.elements import UILabel

from tracker.mediapipe_pose import MediaPipePose


class FPSDisplay(UILabel):
    """
    UILabel to display the UI FPS and the camera FPS
    """

    def __init__(self, ui_manager: UIManager, media_pipe_pose: MediaPipePose):
        super().__init__(
            Rect((10, 10), (300, 30)),
            "UI FPS: -:--  Camera FPS: -:--",
            ui_manager,
            anchors={"top": "top", "left": "left"},
        )

        self.time_deltas = []

        self.media_pipe_pose = media_pipe_pose
        self.ui_manager = ui_manager

    def update(self, time_delta: float):
        super().update(time_delta)

        self.time_deltas.append(time_delta)
        if len(self.time_deltas) > 30:
            self.time_deltas.pop(0)

        fps = 1 / (sum(self.time_deltas) / len(self.time_deltas))

        ui_fps = fps
        camera_fps = fps

        self.set_text(f"UI FPS: {ui_fps:.2f}  Camera FPS: {camera_fps:.2f}")
