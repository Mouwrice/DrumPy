import pygame

import qtm_rt
import asyncio

from marker import Marker
from sound import Sound


class Tracker:
    def __init__(self):
        snare_drum = Sound("../DrumSamples/Snare/CKV1_Snare Loud.wav", (-100, 0, 600))
        hi_hat = Sound("../DrumSamples/HiHat/CKV1_HH Closed Loud.wav", (-220, -200, 800))
        kick_drum = Sound("../DrumSamples/Kick/CKV1_Kick Loud.wav", (-475, 200, 30))
        hi_hat_foot = Sound("../DrumSamples/HiHat/CKV1_HH Foot.wav", (-420, -350, 30))
        tom1 = Sound("../DrumSamples/Perc/Tom1.wav", (-320, 0, 800))
        tom2 = Sound("../DrumSamples/Perc/Tom2.wav", (-320, 100, 850))
        cymbal = Sound("../DrumSamples/cymbals/Hop_Crs.wav", (-50, 500, 925))

        self.markers: list[Marker] = [
            Marker("WristOut_L", 14, [snare_drum, hi_hat, tom1, tom2, cymbal], downward_trend=-3, upward_trend=0.5),
            Marker("WristOut_R", 19, [snare_drum, hi_hat, tom1, tom2, cymbal]),
            Marker("ToeTip_L", 39, [hi_hat_foot], downward_trend=-1.5, upward_trend=-0.5),
            Marker("ToeTip_R", 36, [kick_drum], downward_trend=-1.5, upward_trend=-0.5)
        ]

    def __str__(self):
        return "\n".join([str(marker) for marker in self.markers])

    def on_packet(self, packet: qtm_rt.QRTPacket):
        """ Callback function that is called everytime a data packet arrives from QTM """
        _, markers = packet.get_3d_markers()
        for marker in self.markers:
            position = markers[marker.index]
            marker.update((position.x, position.y, position.z))


async def main():
    connection = await qtm_rt.connect("127.0.0.1")
    if connection is None:
        return

    tracker = Tracker()

    await connection.stream_frames(components=["3d"], on_packet=tracker.on_packet)


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.set_num_channels(32)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(main())
    loop.run_forever()
