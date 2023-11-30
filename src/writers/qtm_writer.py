import time

import qtm_rt

from writers.csv_object import CSVObject


class QTMWriter:
    """
    Class to write the captured data to a CSV file.
    """

    def __init__(self, path: str):
        self.csv_writer = CSVObject(path)

    def on_packet(self, packet: qtm_rt.QRTPacket):
        """ Callback function that is called everytime a data packet arrives from QTM """
        _, markers = packet.get_3d_markers()
        # packets at 100 Hz so time is frame number * 10 ms
        packet_time = packet.framenumber * 10
        if self.csv_writer is not None:
            for i, marker in enumerate(markers):
                self.csv_writer.write(packet.framenumber, packet_time, i, marker.x, marker.y, marker.z)


async def main():
    connection = await qtm_rt.connect("127.0.0.1")
    if connection is None:
        return

    writer = QTMWriter("qtm_multicam_7.csv")

    await connection.stream_frames(components=["3d"], on_packet=writer.on_packet)


if __name__ == "__main__":
    import asyncio

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(main())
    loop.run_forever()
