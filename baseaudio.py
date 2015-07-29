"""Base audio class"""

class BaseAudio(object):
    """Contain an audio data and methods to clean it and extract feature.

    Attributes
    ----------
    sampling_rate : frequency of the recording

    stroke_length : length of a stroke to determin onsets

    audio_fname : path of the audio file

    audio : numpy array of the audio signal
    """

    def __init__(self, **kwargs):
        """
        Load the audio file and determin the features
        """
        # Some parameters
        # sampling rate 44100 is essentia's default
        self.sampling_rate = kwargs.get('sampling_rate', 44100)
        self.audio_fname = None


if __name__=="__main__":
    a = BaseAudio()
    print(a)
