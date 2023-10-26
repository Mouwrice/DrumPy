import pygame

import qtm_rt
import asyncio

from foot import Foot
from hand import Hand
from marker import Tracker, Marker

from sound import Sound


class Drum:
    def __init__(self):
        snare_drum = Sound("Snare Drum", "./DrumSamples/Snare/CKV1_Snare Loud.wav", (-100, 0, 600))
        hi_hat = Sound("High Hat", "./DrumSamples/HiHat/CKV1_HH Closed Loud.wav", (-220, -200, 800))
        kick_drum = Sound("Kick Drum", "./DrumSamples/Kick/CKV1_Kick Loud.wav", (-475, 200, 30))
        hi_hat_foot = Sound("High Hat Foot", "./DrumSamples/HiHat/CKV1_HH Foot.wav", (-420, -350, 30))
        tom1 = Sound("Tom 1", "./DrumSamples/Perc/Tom1.wav", (-350, 0, 700))
        tom2 = Sound("Tom 2", "./DrumSamples/Perc/Tom2.wav", (-350, 100, 750))
        cymbal = Sound("Tom 3", "./DrumSamples/cymbals/Hop_Crs.wav", (-50, 500, 925))

        self.left_hand = Hand(
            wrist_out=Marker("WristOut_L", 14),
            hand_out=Marker("HandOut_L", 17),
            hand_in=Marker("HandIn_L", 16),
            tracker=Tracker("Left Hand", [snare_drum, hi_hat, tom1, tom2, cymbal]))

        self.right_hand = Hand(
            wrist_out=Marker("WristOut_R", 19),
            hand_out=Marker("HandOut_R", 21),
            hand_in=Marker("HandIn_R", 22),
            tracker=Tracker("Right Hand", [snare_drum, hi_hat, tom1, tom2, cymbal]))

        self.left_foot = Foot(toe_tip=Marker("ToeTip_L", 39),
                              tracker=Tracker("Left Foot", [hi_hat_foot], downward_trend=-1.5, upward_trend=-0.5))

        self.right_foot = Foot(toe_tip=Marker("ToeTip_R", 36),
                               tracker=Tracker("Right Foot", [kick_drum], downward_trend=-1.5, upward_trend=-0.5))

    def on_packet(self, packet: qtm_rt.QRTPacket):
        """ Callback function that is called everytime a data packet arrives from QTM """
        _, markers = packet.get_3d_markers()

        # self.left_foot.update(markers)
        # self.right_foot.update(markers)
        # self.left_hand.update(markers)
        self.right_hand.update(markers)


async def main():
    connection = await qtm_rt.connect("127.0.0.1")
    if connection is None:
        return

    tracker = Drum()

    await connection.stream_frames(components=["3d"], on_packet=tracker.on_packet)


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.set_num_channels(32)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(main())
    loop.run_forever()
