from enum import auto, Enum
from time import sleep
from typing import Self, Optional


from drumpy.drum.sound import Sound, SoundState
from drumpy.util import print_float_array, Position


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


class SleepOption(Enum):
    """
    Options for sleeping between calibrations
    """

    NO_SLEEP = auto()
    SLEEP = auto()


class Drum:
    """
    A drum kit consists of multiple sounds
    The drum kit is responsible for initializing the sounds and calibrating them
    Presets can be passed to the constructor with sound positions
    """

    def __init__(
        self: Self,
        sounds: list[Sound],
        sleep_option: SleepOption = SleepOption.SLEEP,
    ) -> None:
        self.sounds = sounds

        # Queue to keep track of sounds that need to be calibrated
        self.auto_calibrations = []

        self.sleep_option = sleep_option

    def __str__(self: Self) -> str:
        return "\n".join([str(sound) for sound in self.sounds])

    def find_and_play_sound(
        self: Self,
        position: Position,
        marker_label: str,
        sounds: Optional[list[Sound]],
    ) -> None:
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
        sounds = sounds if sounds is not None else self.sounds
        for sound in sounds:
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
                f"{marker_label}: {closest_sound.name} with distance {closest_distance:.3f} "
                f"at {print_float_array(position)}"
            )
        else:
            print(
                f"{marker_label}: No sound found for position {print_float_array(position)} "
                f"with distance {closest_distance:.3f}"
            )

    def auto_calibrate(self: Self, sounds: Optional[list[int]] = None) -> None:
        """
        Automatically calibrate all sounds
        :param sounds: List of sounds to calibrate, if None, all sounds will be calibrated in order
        :return:
        """
        if sounds is None:
            sounds = list(range(len(self.sounds)))

        self.auto_calibrations = sounds

    def check_calibrations(self: Self) -> None:
        """
        Check if there are any sounds that need to be calibrated
        :return:
        """
        if len(self.auto_calibrations) == 0:
            return

        sound = self.sounds[self.auto_calibrations[0]]

        match sound.state.value:
            case SoundState.UNINITIALIZED.value:
                sound.calibrate()
                if self.sleep_option == SleepOption.SLEEP:
                    sleep(2)

            case SoundState.READY.value:
                self.auto_calibrations.pop(0)
                return
