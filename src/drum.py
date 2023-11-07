from sound import Sound


class Drum:
    def __init__(self):
        self.snare_drum = Sound("Snare Drum", "./DrumSamples/Snare/CKV1_Snare Loud.wav", (-150, 0, 600))
        self.hi_hat = Sound("High Hat", "./DrumSamples/HiHat/CKV1_HH Closed Loud.wav", (-199, -219, 876))
        self.kick_drum = Sound("Kick Drum", "./DrumSamples/Kick/CKV1_Kick Loud.wav", (-514, 208, 37))
        self.hi_hat_foot = Sound("High Hat Foot", "./DrumSamples/HiHat/CKV1_HH Foot.wav", (-422, -359, 36))
        self.tom1 = Sound("Tom 1", "./DrumSamples/Perc/Tom1.wav", (-350, 20, 700))
        self.tom2 = Sound("Tom 2", "./DrumSamples/Perc/Tom2.wav", (-350, 100, 750))
        self.cymbal = Sound("Tom 3", "./DrumSamples/cymbals/Hop_Crs.wav", (-75, 500, 925))
