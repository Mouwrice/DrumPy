from time import sleep

import numpy as np
import numpy.typing as npt

from src.sound import Sound, SoundState
from src.util import print_float_array


class DrumPresets:
    """
    A collection of drum presets
    """

    @staticmethod
    def first_qtm_recording() -> dict[str, tuple[float, float, float]]:
        """
        :return: A dictionary of drum presets with positions calibrated for the first QTM recording
        """
        return {
            "snare": (-150, 0, 600),
            "hi_hat": (-199, -219, 876),
            "kick": (-514, 208, 37),
            "hi_hat_foot": (-422, -359, 36),
            "tom1": (-350, 20, 700),
            "tom2": (-350, 100, 750),
            "cymbal": (-75, 500, 925),
        }


class Drum:
    """
    A drum kit consists of multiple sounds
    The drum kit is responsible for initializing the sounds and calibrating them
    Presets can be passed to the constructor with sound positions
    """

    def __init__(
        self,
        margin: float,
        min_margin: float,
        presets: dict[str, tuple[float, float, float]] | None = None,
        no_sleep: bool = False,
    ):
        """
        :param presets:
        :param no_sleep: Whether to sleep between calibrations or not
        """
        snare_drum = Sound(
            "Snare Drum",
            "./DrumSamples/Snare/CKV1_Snare Loud.wav",
            margin=margin,
            min_margin=min_margin,
            position=presets["snare"] if presets is not None else None,
        )
        hi_hat = Sound(
            "High Hat",
            "./DrumSamples/HiHat/CKV1_HH Closed Loud.wav",
            margin=margin,
            min_margin=min_margin,
            position=presets["hi_hat"] if presets is not None else None,
        )
        kick_drum = Sound(
            "Kick Drum",
            "./DrumSamples/Kick/CKV1_Kick Loud.wav",
            margin=margin,
            min_margin=min_margin,
            position=presets["kick"] if presets is not None else None,
        )
        _hi_hat_foot = Sound(
            "High Hat Foot",
            "./DrumSamples/HiHat/CKV1_HH Foot.wav",
            margin=margin,
            min_margin=min_margin,
            position=presets["hi_hat_foot"] if presets is not None else None,
        )
        _tom1 = Sound(
            "Tom 1",
            "./DrumSamples/Perc/Tom1.wav",
            margin=margin,
            min_margin=min_margin,
            position=presets["tom1"] if presets is not None else None,
        )
        _tom2 = Sound(
            "Tom 2",
            "./DrumSamples/Perc/Tom2.wav",
            margin=margin,
            min_margin=min_margin,
            position=presets["tom2"] if presets is not None else None,
        )
        cymbal = Sound(
            "Cymbal",
            "./DrumSamples/cymbals/Hop_Crs.wav",
            margin=margin,
            min_margin=min_margin,
            position=presets["cymbal"] if presets is not None else None,
        )

        self.sounds = [
            snare_drum,
            hi_hat,
            kick_drum,
            cymbal,
        ]  # , hi_hat_foot, tom1, tom2, cymbal]

        # Queue to keep track of sounds that need to be calibrated
        self.auto_calibrations = []

        self.no_sleep = no_sleep

    def __str__(self):
        return "\n".join([str(sound) for sound in self.sounds])

    def find_and_play_sound(
        self,
        position: npt.NDArray[np.float64],
        marker_label: str,
        sounds: list[int] | None = None,
    ):
        """
        Find the closest sound to the given position and play it
        If the drum is calibrating sounds, the to be calibrated sound will be played
        :param marker_label: The label of the marker that is hitting the sound
        :param sounds: List of sounds to consider, if None, all sounds will be considered
        :param position: A 3D position as a numpy array
        :return:
        """

        closest_sound = None
        closest_distance = float("inf")
        for i in sounds:
            sound = self.sounds[i]
            if (distance := sound.is_hit(position)) is not None:
                # Check if the sound is calibrating
                if sound.state == SoundState.CALIBRATING:
                    sound.hit(position)
                    print(
                        f"\t{marker_label}: {sound.name} with distance {distance:.3f} at {print_float_array(position)}"
                    )
                    return

                if distance < closest_distance:
                    closest_sound = sound
                    closest_distance = distance

        if closest_sound is not None:
            closest_sound.hit(position)
            print(
                f"{marker_label}: {closest_sound.name} with distance {closest_distance:.3f} ] at {print_float_array(position)}"
            )
        else:
            print(
                f"{marker_label}: No sound found for position {print_float_array(position)} with distance {closest_distance:.3f}"
            )

    def auto_calibrate(self, sounds: list[int] | None = None):
        """
        Automatically calibrate all sounds
        :param sounds: List of sounds to calibrate, if None, all sounds will be calibrated in order
        :return:
        """
        if sounds is None:
            sounds = list(range(len(self.sounds)))

        self.auto_calibrations = sounds

    def check_calibrations(self):
        """
        Check if there are any sounds that need to be calibrated
        :return:
        """
        if len(self.auto_calibrations) == 0:
            return

        sound = self.sounds[self.auto_calibrations[0]]

        if sound.state == SoundState.UNINITIALIZED:
            sound.calibrate()
            if not self.no_sleep:
                sleep(2)

        if sound.state == SoundState.READY:
            self.auto_calibrations.pop(0)
            return
