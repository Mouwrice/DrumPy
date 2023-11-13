from sound import Sound, SoundState


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
    A drum kit with sounds
    """

    def __init__(self, presets: dict[str, tuple[float, float, float]] | None = None):
        self.snare_drum = Sound("Snare Drum", "./DrumSamples/Snare/CKV1_Snare Loud.wav",
                                presets["snare"] if presets is not None else None)
        self.hi_hat = Sound("High Hat", "./DrumSamples/HiHat/CKV1_HH Closed Loud.wav",
                            presets["hi_hat"] if presets is not None else None)
        self.kick_drum = Sound("Kick Drum", "./DrumSamples/Kick/CKV1_Kick Loud.wav",
                               presets["kick"] if presets is not None else None)
        self.hi_hat_foot = Sound("High Hat Foot", "./DrumSamples/HiHat/CKV1_HH Foot.wav",
                                 presets["hi_hat_foot"] if presets is not None else None)
        self.tom1 = Sound("Tom 1", "./DrumSamples/Perc/Tom1.wav", presets["tom1"] if presets is not None else None)
        self.tom2 = Sound("Tom 2", "./DrumSamples/Perc/Tom2.wav", presets["tom2"] if presets is not None else None)
        self.cymbal = Sound("Cymbal", "./DrumSamples/cymbals/Hop_Crs.wav",
                            presets["cymbal"] if presets is not None else None)

    def initialize(self):
        """
        Initialize the drum kit
        :return:
        """
        print("Initializing drum kit")
        self.snare_drum.state = SoundState.CALIBRATING
        print(self)

    def __str__(self):
        return (
            f"Drum kit with sounds:\n"
            f"{self.snare_drum.name}: {self.snare_drum.state}\n"
            f"{self.hi_hat.name}: {self.hi_hat.state}\n"
            f"{self.kick_drum.name}: {self.kick_drum.state}\n"
            f"{self.hi_hat_foot.name}: {self.hi_hat_foot.state}\n"
            f"{self.tom1.name}: {self.tom1.state}\n"
            f"{self.tom2.name}: {self.tom2.state}\n"
            f"{self.cymbal.name}: {self.cymbal.state}\n"
        )
