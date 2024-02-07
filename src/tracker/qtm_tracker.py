import asyncio
import time

import pygame
import qtm_rt

from src.csv_objects.csv_object import CSVWriter
from src.drum import Drum, DrumPresets
from src.tracker.foot import Foot
from src.tracker.hand import Hand
from src.tracker.marker import Marker
from src.tracker.marker_tracker import MarkerTracker


class QTMFullTracker:
    def __init__(self, drum: Drum, log_to_file: bool = False):
        self.left_hand = Hand(
            wrist_out=Marker("WristOut_L", 14),
            hand_out=Marker("HandOut_L", 17),
            hand_in=Marker("HandIn_L", 16),
            tracker=MarkerTracker(
                "Left Hand",
                [0, 1, 3],  # 5, 6],
                drum,
            ),
        )

        self.right_hand = Hand(
            wrist_out=Marker("WristOut_R", 19),
            hand_out=Marker("HandOut_R", 21),
            hand_in=Marker("HandIn_R", 22),
            tracker=MarkerTracker(
                "Right Hand",
                [0, 1, 3],  # 5, 6],
                drum,
            ),
        )

        self.left_foot = Foot(
            toe_tip=Marker("ToeTip_L", 39),
            tracker=MarkerTracker(
                "Left Foot",
                [],  # 3],
                drum,
                downward_trend=-1.5,
                upward_trend=-0.5,
            ),
        )

        self.right_foot = Foot(
            toe_tip=Marker("ToeTip_R", 36),
            tracker=MarkerTracker(
                "Right Foot", [2], drum, downward_trend=-1.5, upward_trend=-0.5
            ),
        )

        self.csv_writer = None
        if log_to_file:
            log_file = f"./qtm-{time.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
            self.csv_writer = CSVWriter(log_file)

    def on_packet(self, packet: qtm_rt.QRTPacket):
        """Callback function that is called everytime a data packet arrives from QTM"""
        _, markers = packet.get_3d_markers()

        self.left_foot.update(markers)
        self.right_foot.update(markers)
        self.left_hand.update(markers)
        self.right_hand.update(markers)

        if packet.framenumber % 1000 == 0:
            print(self.left_hand.tracker.hits)
            print(self.right_hand.tracker.hits)
            print(self.left_foot.tracker.hits)
            print(self.right_foot.tracker.hits)

        packet_time = time.time_ns()
        if self.csv_writer is not None:
            for i, marker in enumerate(markers):
                self.csv_writer.write(
                    packet.framenumber, packet_time, i, marker.x, marker.y, marker.z
                )

    async def start_capture(self):
        """Start streaming frames from QTM"""
        connection = await qtm_rt.connect("127.0.0.1")
        if connection is None:
            return

        await connection.stream_frames(components=["3d"], on_packet=self.on_packet)


async def main():
    drum = Drum(200, 40, no_sleep=True, presets=DrumPresets.first_qtm_recording())
    await QTMFullTracker(drum, log_to_file=True).start_capture()


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.set_num_channels(64)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(main())
    loop.run_forever()
