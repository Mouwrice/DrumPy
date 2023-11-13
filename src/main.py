from abc import ABC
import pygame
import asyncio

from drum import Drum
from tracker.mediapipe_tracker import MediaPipeTracker


def main():
    drum = Drum()
    drum.initialize()
    # await QTMTracker(drum).start_capture()
    pose_tracker = MediaPipeTracker(drum)
    pose_tracker.start_capture()


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.set_num_channels(32)
    main()

    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.create_task(main())
    # loop.run_forever()
