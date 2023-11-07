import qtm_rt

from drum import Drum
from tracker.foot import Foot
from tracker.hand import Hand
from tracker.marker import Marker
from tracker.marker_tracker import MarkerTracker
from tracker.tracker import Tracker


class QTMTracker(Tracker):
    def __init__(self, drum: Drum):
        super().__init__()
        self.left_hand = Hand(
            wrist_out=Marker("WristOut_L", 14),
            hand_out=Marker("HandOut_L", 17),
            hand_in=Marker("HandIn_L", 16),
            tracker=MarkerTracker("Left Hand", [drum.snare_drum, drum.hi_hat, drum.tom1, drum.tom2, drum.cymbal]))

        self.right_hand = Hand(
            wrist_out=Marker("WristOut_R", 19),
            hand_out=Marker("HandOut_R", 21),
            hand_in=Marker("HandIn_R", 22),
            tracker=MarkerTracker("Right Hand", [drum.snare_drum, drum.hi_hat, drum.tom1, drum.tom2, drum.cymbal]))

        self.left_foot = Foot(toe_tip=Marker("ToeTip_L", 39),
                              tracker=MarkerTracker("Left Foot", [drum.hi_hat_foot], downward_trend=-1.5,
                                                    upward_trend=-0.5))

        self.right_foot = Foot(toe_tip=Marker("ToeTip_R", 36),
                               tracker=MarkerTracker("Right Foot", [drum.kick_drum], downward_trend=-1.5,
                                                     upward_trend=-0.5))

    def on_packet(self, packet: qtm_rt.QRTPacket):
        """ Callback function that is called everytime a data packet arrives from QTM """
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

    async def start_capture(self):
        """ Start streaming frames from QTM """
        connection = await qtm_rt.connect("127.0.0.1")
        if connection is None:
            return

        await connection.stream_frames(components=["3d"], on_packet=self.on_packet)
